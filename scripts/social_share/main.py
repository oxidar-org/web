"""Main orchestrator for social media sharing of new blog posts."""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import load_config, get_ai_provider_name, get_base_url
from detect import detect_new_posts
from ai import get_ai_provider
from platforms import get_enabled_platforms, ALL_PLATFORM_NAMES

logger = logging.getLogger("social_share")

DEFAULT_CONFIG_PATH = ".github/social-media-config.yaml"
FALLBACK_MAX_CHARS = 9999


def _generate_messages(posts: list[dict], ai, config: dict, platform_names: list[str]) -> list[dict]:
    """Generate messages for each post × platform. Returns list of {post, platform, text}."""
    messages = []
    for post in posts:
        for platform_name in platform_names:
            try:
                text = ai.generate(post, platform_name, config)
                max_chars = config.get("platforms", {}).get(platform_name, {}).get("max_chars", FALLBACK_MAX_CHARS)
                if len(text) > max_chars:
                    logger.warning("Text for %s exceeds limit (%d), truncating", platform_name, max_chars)
                    text = text[:max_chars]
                messages.append({"post": post, "platform": platform_name, "text": text})
            except Exception as e:
                logger.error("AI generation failed for %s/%s: %s", post["title"], platform_name, e)
    return messages


def _save_messages(messages: list[dict], path: str) -> None:
    """Write messages to JSON and post a Markdown summary to GitHub Step Summary if in CI."""
    Path(path).write_text(json.dumps(messages, ensure_ascii=False, indent=2))
    logger.info("Saved %d messages to %s", len(messages), path)

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    with open(summary_path, "a") as f:
        f.write("## Social Media Messages — Pending Approval\n\n")
        current_post = None
        for msg in messages:
            title = msg["post"]["title"]
            if title != current_post:
                current_post = title
                f.write(f"### {title}\n**URL:** {msg['post']['url']}\n\n")
            f.write(f"**{msg['platform'].upper()}**\n\n```\n{msg['text']}\n```\n\n")


def _publish_messages(messages: list[dict], platform_map: dict) -> list[tuple]:
    """Publish pre-generated messages to enabled platforms. Returns error tuples."""
    errors = []
    for msg in messages:
        platform = platform_map.get(msg["platform"])
        if not platform:
            logger.info("Skipping %s (not enabled)", msg["platform"])
            continue
        try:
            result = platform.publish(msg["text"], msg["post"])
            if result.success:
                logger.info("Published to %s: %s", msg["platform"], result.url)
            else:
                logger.error("Publish failed on %s: %s", msg["platform"], result.error)
                errors.append((msg["post"]["title"], msg["platform"], result.error))
        except Exception as e:
            logger.error("Publish error on %s: %s", msg["platform"], e)
            errors.append((msg["post"]["title"], msg["platform"], str(e)))
    return errors


def main():
    parser = argparse.ArgumentParser(description="Share new blog posts to social media")
    parser.add_argument("--posts-file", help="File with post paths (one per line)")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--dry-run", action="store_true", help="Generate text but do not publish")
    parser.add_argument("--save-messages", metavar="PATH", help="Generate messages, save to JSON, and exit")
    parser.add_argument("--from-messages", metavar="PATH", help="Publish from a previously saved messages JSON")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    config = load_config(args.config)
    errors = []

    if args.from_messages:
        messages = json.loads(Path(args.from_messages).read_text())
        logger.info("Loaded %d messages from %s", len(messages), args.from_messages)
        platform_map = {p.name: p for p in get_enabled_platforms()}
        errors = _publish_messages(messages, platform_map)

    else:
        posts = detect_new_posts(
            repo_root=os.getcwd(), base_url=get_base_url(config), posts_file=args.posts_file,
        )
        if not posts:
            logger.info("No new posts to share. Exiting.")
            return

        logger.info("Found %d new post(s):", len(posts))
        for p in posts:
            logger.info("  - %s (%s)", p["title"], p["url"])

        logger.info("Using AI provider: %s", get_ai_provider_name())
        ai = get_ai_provider()

        if args.save_messages or args.dry_run:
            # Generate for all platforms (full preview regardless of what's enabled)
            messages = _generate_messages(posts, ai, config, ALL_PLATFORM_NAMES)
            if args.save_messages:
                _save_messages(messages, args.save_messages)
                return
            for msg in messages:
                logger.info("[DRY RUN] [%s] %s:\n%s", msg["platform"].upper(), msg["post"]["title"], msg["text"])
            return

        platforms = get_enabled_platforms()
        if not platforms:
            logger.warning("No platforms enabled. Set *_ENABLED=true for at least one platform.")
            return
        platform_map = {p.name: p for p in platforms}
        messages = _generate_messages(posts, ai, config, list(platform_map.keys()))
        errors = _publish_messages(messages, platform_map)

    logger.info("=" * 60)
    if errors:
        logger.error("Completed with %d error(s):", len(errors))
        for title, platform, error in errors:
            logger.error("  - [%s] %s: %s", platform, title, error)
        sys.exit(1)
    else:
        logger.info("All posts shared successfully!")


if __name__ == "__main__":
    main()

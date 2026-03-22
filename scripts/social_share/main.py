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
from issue_formatter import (
    format_issue_body,
    format_issue_title,
    parse_issue_body,
    APPROVED_LABEL,
    PUBLISHED_LABEL,
    PENDING_LABEL,
)

logger = logging.getLogger("social_share")

DEFAULT_CONFIG_PATH = ".github/social-media-config.yaml"
FALLBACK_MAX_CHARS = 9999
GITHUB_API = "https://api.github.com"


def _github_headers() -> dict:
    token = os.environ.get("GITHUB_TOKEN", "")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


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


def _create_issues(messages: list[dict]) -> None:
    """Create one GitHub issue per post with formatted messages for review."""
    import requests

    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        logger.error("GITHUB_REPOSITORY not set — cannot create issues")
        return

    # Group messages by post URL
    posts: dict[str, dict] = {}
    for msg in messages:
        url = msg["post"]["url"]
        if url not in posts:
            posts[url] = {"post": msg["post"], "messages": []}
        posts[url]["messages"].append(msg)

    for data in posts.values():
        post = data["post"]
        body = format_issue_body(post, data["messages"])
        title = format_issue_title(post["title"])

        resp = requests.post(
            f"{GITHUB_API}/repos/{repo}/issues",
            headers=_github_headers(),
            json={"title": title, "body": body, "labels": [PENDING_LABEL]},
            timeout=30,
        )
        if resp.status_code == 201:
            issue = resp.json()
            logger.info("Created issue #%d: %s", issue["number"], issue["html_url"])
        else:
            logger.error("Failed to create issue for '%s': %s", post["title"], resp.text)


def _publish_from_issue(issue_number: int, platform_map: dict) -> list[tuple]:
    """Fetch issue body, check idempotency, parse messages, and publish."""
    import requests

    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        logger.error("GITHUB_REPOSITORY not set — cannot fetch issue")
        return [("unknown", "github", "GITHUB_REPOSITORY not set")]

    resp = requests.get(
        f"{GITHUB_API}/repos/{repo}/issues/{issue_number}",
        headers=_github_headers(),
        timeout=30,
    )
    if resp.status_code != 200:
        logger.error("Failed to fetch issue #%d: %s", issue_number, resp.text)
        return [("unknown", "github", f"Failed to fetch issue: {resp.text}")]

    issue = resp.json()
    labels = [label["name"] for label in issue.get("labels", [])]

    if PUBLISHED_LABEL in labels:
        logger.info("Issue #%d already published — skipping.", issue_number)
        return []

    if APPROVED_LABEL not in labels:
        logger.warning("Issue #%d does not have '%s' label — skipping.", issue_number, APPROVED_LABEL)
        return []

    _, messages = parse_issue_body(issue["body"])
    if not messages:
        logger.error("No messages parsed from issue #%d body.", issue_number)
        return [("unknown", "github", "No messages found in issue body")]

    logger.info("Parsed %d message(s) from issue #%d", len(messages), issue_number)
    return _publish_messages(messages, platform_map)


def main():
    parser = argparse.ArgumentParser(description="Share new blog posts to social media")
    parser.add_argument("--posts-file", help="File with post paths (one per line)")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--dry-run", action="store_true", help="Generate text but do not publish")
    parser.add_argument("--save-messages", metavar="PATH", help="Generate messages, save to JSON, and exit")
    parser.add_argument("--from-messages", metavar="PATH", help="Publish from a previously saved messages JSON")
    parser.add_argument("--create-issues", action="store_true", help="Generate messages and create GitHub issues for review")
    parser.add_argument("--from-issue", metavar="NUMBER", type=int, help="Publish from a GitHub issue body")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    config = load_config(args.config)
    errors = []

    if args.from_messages:
        messages = json.loads(Path(args.from_messages).read_text())
        logger.info("Loaded %d messages from %s", len(messages), args.from_messages)
        platform_map = {p.name: p for p in get_enabled_platforms()}
        errors = _publish_messages(messages, platform_map)

    elif args.from_issue is not None:
        platform_map = {p.name: p for p in get_enabled_platforms()}
        errors = _publish_from_issue(args.from_issue, platform_map)

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
            messages = _generate_messages(posts, ai, config, ALL_PLATFORM_NAMES)
            if args.save_messages:
                _save_messages(messages, args.save_messages)
                return
            for msg in messages:
                logger.info("[DRY RUN] [%s] %s:\n%s", msg["platform"].upper(), msg["post"]["title"], msg["text"])
            return

        if args.create_issues:
            messages = _generate_messages(posts, ai, config, ALL_PLATFORM_NAMES)
            _create_issues(messages)
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

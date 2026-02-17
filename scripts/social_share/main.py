"""Main orchestrator for social media sharing of new blog posts."""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add parent dir to path for imports when run as script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import load_config, get_ai_provider_name, get_base_url
from detect import detect_new_posts
from ai import get_ai_provider
from platforms import get_enabled_platforms

logger = logging.getLogger("social_share")

DEFAULT_CONFIG_PATH = ".github/social-media-config.yaml"
ALL_PLATFORMS = ["twitter", "linkedin", "bluesky", "telegram"]
FALLBACK_MAX_CHARS = 9999


def main():
    parser = argparse.ArgumentParser(description="Share new blog posts to social media")
    parser.add_argument(
        "--posts-file",
        help="File with list of post paths (one per line), instead of git diff detection",
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_PATH,
        help="Path to social media config YAML",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate text but do not publish",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    # Load configuration
    config = load_config(args.config)
    base_url = get_base_url(config)

    # Detect new posts
    posts = detect_new_posts(
        repo_root=os.getcwd(),
        base_url=base_url,
        posts_file=args.posts_file,
    )
    if not posts:
        logger.info("No new posts to share. Exiting.")
        return

    logger.info("Found %d new post(s) to share:", len(posts))
    for p in posts:
        logger.info("  - %s (%s)", p["title"], p["url"])

    # Initialize AI provider
    provider_name = get_ai_provider_name()
    logger.info("Using AI provider: %s", provider_name)
    ai = get_ai_provider()

    # Get enabled platforms
    platforms = get_enabled_platforms()
    if not platforms and not args.dry_run:
        logger.warning("No platforms enabled. Set *_ENABLED=true for at least one platform.")
        return

    # Build platform lookup for publishing
    platform_map = {p.name: p for p in platforms}
    target_names = list(platform_map.keys()) if platforms else ALL_PLATFORMS

    if args.dry_run and not platforms:
        logger.info("Dry-run mode: generating text for all platforms (none enabled)")

    # Process each post x platform
    errors = []
    for post in posts:
        logger.info("=" * 60)
        logger.info("Post: %s", post["title"])
        logger.info("URL:  %s", post["url"])

        for platform_name in target_names:
            logger.info("--- %s ---", platform_name.upper())
            try:
                text = ai.generate(post, platform_name, config)
            except Exception as e:
                logger.error("AI generation failed for %s: %s", platform_name, e)
                errors.append((post["title"], platform_name, f"AI error: {e}"))
                continue

            # Validate length
            max_chars = config.get("platforms", {}).get(platform_name, {}).get("max_chars", FALLBACK_MAX_CHARS)
            if len(text) > max_chars:
                logger.warning("Generated text (%d chars) exceeds limit (%d)", len(text), max_chars)
                text = text[:max_chars]

            logger.info("Generated (%d chars):\n%s", len(text), text)

            if args.dry_run:
                logger.info("[DRY RUN - not published]")
                continue

            platform = platform_map.get(platform_name)
            if not platform:
                logger.warning("Platform %s not found in enabled platforms", platform_name)
                continue

            try:
                result = platform.publish(text, post)
                if result.success:
                    logger.info("Published successfully! url=%s", result.url)
                else:
                    logger.error("Publish failed: %s", result.error)
                    errors.append((post["title"], platform_name, result.error))
            except Exception as e:
                logger.error("Publish error: %s", e)
                errors.append((post["title"], platform_name, str(e)))

    # Summary
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

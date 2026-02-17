"""Main orchestrator for social media sharing of new blog posts."""

import argparse
import os
import sys
from pathlib import Path

# Add parent dir to path for imports when run as script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import load_config, get_ai_provider_name, get_base_url
from detect import detect_new_posts
from ai import get_ai_provider
from platforms import get_enabled_platforms


def main():
    parser = argparse.ArgumentParser(description="Share new blog posts to social media")
    parser.add_argument(
        "--posts-file",
        help="File with list of post paths (one per line), instead of git diff detection",
    )
    parser.add_argument(
        "--config",
        default=".github/social-media-config.yaml",
        help="Path to social media config YAML",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate text but do not publish",
    )
    args = parser.parse_args()

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
        print("No new posts to share. Exiting.")
        return

    print(f"Found {len(posts)} new post(s) to share:")
    for p in posts:
        print(f"  - {p['title']} ({p['url']})")

    # Initialize AI provider
    provider_name = get_ai_provider_name()
    print(f"\nUsing AI provider: {provider_name}")
    ai = get_ai_provider()

    # Get enabled platforms
    platforms = get_enabled_platforms()
    if not platforms and not args.dry_run:
        print("No platforms enabled. Set *_ENABLED=true for at least one platform.")
        return

    platform_names = [p.name for p in platforms] if platforms else ["twitter", "linkedin", "bluesky", "telegram"]
    if args.dry_run and not platforms:
        print("Dry-run mode: generating text for all platforms (none enabled)")

    # Process each post x platform
    errors = []
    for post in posts:
        print(f"\n{'='*60}")
        print(f"Post: {post['title']}")
        print(f"URL:  {post['url']}")
        print(f"{'='*60}")

        target_names = platform_names if args.dry_run and not platforms else [p.name for p in platforms]

        for platform_name in target_names:
            print(f"\n--- {platform_name.upper()} ---")
            try:
                text = ai.generate(post, platform_name, config)
            except Exception as e:
                print(f"AI generation failed for {platform_name}: {e}")
                errors.append((post["title"], platform_name, f"AI error: {e}"))
                continue

            # Validate length
            max_chars = config.get("platforms", {}).get(platform_name, {}).get("max_chars", 9999)
            if len(text) > max_chars:
                print(f"WARNING: Generated text ({len(text)} chars) exceeds limit ({max_chars})")
                text = text[:max_chars]

            print(f"Generated ({len(text)} chars):")
            print(text)

            if args.dry_run:
                print("[DRY RUN - not published]")
                continue

            # Find the matching platform instance
            platform = next((p for p in platforms if p.name == platform_name), None)
            if not platform:
                continue

            try:
                result = platform.publish(text, post)
                if result.get("success"):
                    print(f"Published successfully! {result}")
                else:
                    print(f"Publish failed: {result.get('error')}")
                    errors.append((post["title"], platform_name, result.get("error")))
            except Exception as e:
                print(f"Publish error: {e}")
                errors.append((post["title"], platform_name, str(e)))

    # Summary
    print(f"\n{'='*60}")
    if errors:
        print(f"Completed with {len(errors)} error(s):")
        for title, platform, error in errors:
            print(f"  - [{platform}] {title}: {error}")
        sys.exit(1)
    else:
        print("All posts shared successfully!")


if __name__ == "__main__":
    main()

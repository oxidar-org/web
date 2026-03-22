"""Auto-translate new Spanish blog posts to English."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shared.detect import (  # noqa: E402
    get_new_post_files,
    filter_post_files,
    parse_front_matter,
    ENGLISH_TRANSLATION_SUFFIX,
)
from shared.ai import get_ai_provider  # noqa: E402
from translator import translate_post  # noqa: E402

logger = logging.getLogger("auto_translate")


def _english_path(post_path: str) -> Path:
    """Derive the .en.md path from a Spanish .md path.

    e.g. content/posts/2026.03.14-snakear/snakear.md
      -> content/posts/2026.03.14-snakear/snakear.en.md
    """
    p = Path(post_path)
    return p.with_name(p.stem + ENGLISH_TRANSLATION_SUFFIX)


def _needs_translation(post_path: str, repo_root: str) -> bool:
    """Return True if no .en.md sibling exists yet."""
    en_path = _english_path(post_path)
    # Path may be relative to repo root
    full = en_path if en_path.is_absolute() else Path(repo_root) / en_path
    return not full.exists()


def _detect_posts(posts_file: str | None, repo_root: str) -> list[str]:
    """Return list of Spanish post file paths that need translation."""
    if posts_file:
        path = Path(posts_file)
        if not path.exists():
            logger.error("Posts file not found: %s", posts_file)
            return []
        files = [line.strip() for line in path.read_text().strip().split("\n") if line.strip()]
    else:
        raw = get_new_post_files(repo_root)
        files = filter_post_files(raw)

    return [f for f in files if _needs_translation(f, repo_root)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-translate new Spanish posts to English")
    parser.add_argument("--posts-file", help="File with post paths (one per line)")
    parser.add_argument("--repo-root", default=os.getcwd(), help="Repository root directory")
    parser.add_argument("--dry-run", action="store_true", help="Print output without writing files")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    posts = _detect_posts(args.posts_file, args.repo_root)
    if not posts:
        logger.info("No posts need translation.")
        return

    logger.info("Found %d post(s) to translate:", len(posts))
    for p in posts:
        logger.info("  - %s", p)

    ai = get_ai_provider(default="github_models")
    translated_files: list[tuple[str, str]] = []  # (en_path, title)

    for post_path in posts:
        full_path = post_path if Path(post_path).is_absolute() else str(Path(args.repo_root) / post_path)
        fm = parse_front_matter(full_path)
        if fm is None:
            logger.error("Skipping (parse error): %s", post_path)
            continue

        if fm.get("draft"):
            logger.info("Skipping draft: %s", post_path)
            continue

        title = fm.get("title", post_path)
        logger.info("Translating: %s", title)

        try:
            content = translate_post(ai, fm)
        except Exception as e:
            logger.error("Translation failed for '%s': %s", title, e)
            continue

        en_path = _english_path(post_path)
        full_en = en_path if en_path.is_absolute() else Path(args.repo_root) / en_path

        if args.dry_run:
            logger.info("[DRY RUN] Would write: %s\n%s", full_en, content[:500])
        else:
            full_en.write_text(content, encoding="utf-8")
            logger.info("Written: %s", full_en)
            translated_files.append((str(en_path), title))

    # Print translated file paths to stdout for the workflow to pick up
    if translated_files:
        print("TRANSLATED_FILES_START")
        for en_path, title in translated_files:
            print(f"{en_path}|{title}")
        print("TRANSLATED_FILES_END")


if __name__ == "__main__":
    main()

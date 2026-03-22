"""Detect new blog posts from git diff and parse their front matter."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Allow importing from scripts/shared regardless of working directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shared.detect import (  # noqa: E402
    get_new_post_files,
    filter_post_files,
    parse_front_matter,
    ENGLISH_TRANSLATION_SUFFIX,
    INDEX_FILE_PREFIX,
)

logger = logging.getLogger("social_share")

BODY_EXCERPT_MAX_CHARS = 2000

__all__ = [
    "get_new_post_files",
    "filter_post_files",
    "parse_front_matter",
    "ENGLISH_TRANSLATION_SUFFIX",
    "INDEX_FILE_PREFIX",
]


def should_share(fm: dict) -> bool:
    """Return True unless the post is a draft, share=false, or hidden from home."""
    return not fm.get("draft") and fm.get("share") is not False and not fm.get("hiddenFromHomePage")


def derive_url(file_path: str, base_url: str) -> str:
    """Build post URL using Hugo's :filename permalink pattern."""
    return f"{base_url.rstrip('/')}/{Path(file_path).stem}/"


def detect_new_posts(
    repo_root: str | None = None,
    base_url: str = "https://oxidar.org",
    posts_file: str | None = None,
) -> list[dict]:
    """Detect and parse new posts ready for sharing."""
    if posts_file:
        path = Path(posts_file)
        if not path.exists():
            logger.error("Posts file not found: %s", posts_file)
            return []
        files = [line.strip() for line in path.read_text().strip().split("\n") if line.strip()]
    else:
        raw_files = get_new_post_files(repo_root)
        files = filter_post_files(raw_files)

    if not files:
        logger.info("No new posts detected.")
        return []

    posts = []
    for f in files:
        full_path = f if Path(f).is_absolute() else str(Path(repo_root or ".") / f)
        fm = parse_front_matter(full_path)
        if fm is None:
            continue
        if not should_share(fm):
            logger.info("Skipping (share disabled): %s", f)
            continue

        body = fm.get("_body", "")
        body_excerpt = body[:BODY_EXCERPT_MAX_CHARS]

        posts.append({
            "title": fm.get("title", ""),
            "description": fm.get("description", ""),
            "tags": fm.get("tags", []),
            "categories": fm.get("categories", []),
            "body": body_excerpt,
            "url": derive_url(f, base_url),
            "file": f,
        })

    return posts

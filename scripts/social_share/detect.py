"""Detect new blog posts from git diff and parse their front matter."""

from __future__ import annotations

import logging
import re
import subprocess
from pathlib import Path

logger = logging.getLogger("social_share")

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

BODY_EXCERPT_MAX_CHARS = 2000
ENGLISH_TRANSLATION_SUFFIX = ".en.md"
INDEX_FILE_PREFIX = "_"


def get_new_post_files(repo_root: str | None = None) -> list[str]:
    """Get list of newly added markdown files in content/posts/ from git diff."""
    cmd = [
        "git", "diff", "--name-only", "--diff-filter=A",
        "HEAD~1", "HEAD", "--", "content/posts/**/*.md",
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True,
        cwd=repo_root,
    )
    if result.returncode != 0:
        logger.error("git diff failed: %s", result.stderr)
        return []
    files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
    return files


def filter_post_files(files: list[str]) -> list[str]:
    """Filter out English translations, index files, etc."""
    filtered = []
    for f in files:
        basename = Path(f).name
        if basename.startswith(INDEX_FILE_PREFIX):
            continue
        if basename.endswith(ENGLISH_TRANSLATION_SUFFIX):
            continue
        filtered.append(f)
    return filtered


def parse_front_matter(file_path: str) -> dict | None:
    """Parse TOML front matter from a markdown file.

    Returns a dict with front matter fields, or None if parsing fails.
    """
    path = Path(file_path)
    try:
        content = path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
        logger.error("Cannot read %s: %s", file_path, e)
        return None

    # Match TOML front matter delimited by +++
    match = re.match(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)", content, re.DOTALL)
    if not match:
        logger.error("No TOML front matter found in: %s", file_path)
        return None

    toml_str = match.group(1)
    body = match.group(2)

    try:
        fm = tomllib.loads(toml_str)
    except tomllib.TOMLDecodeError as e:
        logger.error("TOML parse error in %s: %s", file_path, e)
        return None

    fm["_body"] = body
    fm["_file"] = file_path
    return fm


def should_share(fm: dict) -> bool:
    """Check if a post should be shared based on front matter flags."""
    if fm.get("draft", False):
        return False
    if fm.get("share") is False:
        return False
    if fm.get("hiddenFromHomePage", False):
        return False
    return True


def derive_url(file_path: str, base_url: str) -> str:
    """Derive the post URL from the file path using the permalink pattern.

    Hugo permalink for posts is :contentbasename, so the URL is the
    filename stem (without extension).
    """
    stem = Path(file_path).stem
    base = base_url.rstrip("/")
    return f"{base}/{stem}/"


def detect_new_posts(
    repo_root: str | None = None,
    base_url: str = "https://oxidar.org",
    posts_file: str | None = None,
) -> list[dict]:
    """Detect and parse new posts ready for sharing.

    Args:
        repo_root: Root of the git repository.
        base_url: Site base URL for building post URLs.
        posts_file: Optional file containing list of post paths (one per line),
                    used instead of git diff.

    Returns:
        List of post dicts with title, description, tags, categories, body, url.
    """
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

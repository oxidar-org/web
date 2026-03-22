"""Shared utilities for detecting and parsing new blog posts from git diff."""

from __future__ import annotations

import logging
import re
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

ENGLISH_TRANSLATION_SUFFIX = ".en.md"
INDEX_FILE_PREFIX = "_"


def get_new_post_files(repo_root: str | None = None) -> list[str]:
    """Get list of added or modified markdown files in content/posts/ from git diff."""
    cmd = [
        "git", "diff", "--name-only", "--diff-filter=AM",
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
    """Filter out English translations and index files."""
    return [f for f in files
            if not Path(f).name.startswith(INDEX_FILE_PREFIX)
            and not Path(f).name.endswith(ENGLISH_TRANSLATION_SUFFIX)]


def parse_front_matter(file_path: str) -> dict | None:
    """Parse TOML front matter from a markdown file.

    Returns a dict with front matter fields and special keys:
    - _body: the content after front matter
    - _file: the original file path
    - _raw_fm: the raw TOML front matter string (for reconstruction)
    """
    path = Path(file_path)
    try:
        content = path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
        logger.error("Cannot read %s: %s", file_path, e)
        return None

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
    fm["_raw_fm"] = toml_str
    return fm

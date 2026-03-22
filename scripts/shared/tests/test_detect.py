"""Tests for shared detect utilities."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from detect import (
    filter_post_files,
    parse_front_matter,
    ENGLISH_TRANSLATION_SUFFIX,
    INDEX_FILE_PREFIX,
)


def _write_post(tmp_path, filename, front_matter, body="Hello world"):
    path = tmp_path / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"+++\n{front_matter}\n+++\n{body}")
    return str(path)


# --- filter_post_files ---

class TestFilterPostFiles:
    def test_filters_english_translations(self):
        files = ["content/posts/foo/foo.md", "content/posts/foo/foo.en.md"]
        assert filter_post_files(files) == ["content/posts/foo/foo.md"]

    def test_filters_index_files(self):
        files = ["content/posts/_index.md", "content/posts/foo/foo.md"]
        assert filter_post_files(files) == ["content/posts/foo/foo.md"]

    def test_filters_english_index(self):
        files = ["content/posts/_index.en.md", "content/posts/foo/foo.md"]
        assert filter_post_files(files) == ["content/posts/foo/foo.md"]

    def test_keeps_regular_posts(self):
        files = [
            "content/posts/2025.06.12-wasm/wasm.md",
            "content/posts/2026.01.26-rustconf/rustconf.md",
        ]
        assert filter_post_files(files) == files

    def test_empty_list(self):
        assert filter_post_files([]) == []

    def test_all_filtered(self):
        files = ["content/posts/_index.md", "content/posts/foo/foo.en.md"]
        assert filter_post_files(files) == []


# --- parse_front_matter ---

class TestParseFrontMatter:
    def test_parses_title_and_draft(self, tmp_path):
        path = _write_post(tmp_path, "post.md", 'title = "My Post"\ndraft = false')
        fm = parse_front_matter(path)
        assert fm is not None
        assert fm["title"] == "My Post"
        assert fm["draft"] is False

    def test_body_is_accessible(self, tmp_path):
        path = _write_post(tmp_path, "post.md", 'title = "T"', body="Some content here")
        fm = parse_front_matter(path)
        assert "Some content here" in fm["_body"]

    def test_raw_fm_is_preserved(self, tmp_path):
        """_raw_fm must be present for the translator to reconstruct the file."""
        raw = 'title = "My Post"\ndraft = false'
        path = _write_post(tmp_path, "post.md", raw)
        fm = parse_front_matter(path)
        assert fm["_raw_fm"] == raw

    def test_file_path_stored(self, tmp_path):
        path = _write_post(tmp_path, "post.md", 'title = "T"')
        fm = parse_front_matter(path)
        assert fm["_file"] == path

    def test_parses_tags_and_categories(self, tmp_path):
        raw = 'title = "T"\ntags = ["rust", "wasm"]\ncategories = ["Tutoriales"]'
        path = _write_post(tmp_path, "post.md", raw)
        fm = parse_front_matter(path)
        assert fm["tags"] == ["rust", "wasm"]
        assert fm["categories"] == ["Tutoriales"]

    def test_returns_none_for_missing_file(self):
        assert parse_front_matter("/nonexistent/path/post.md") is None

    def test_returns_none_for_no_front_matter(self, tmp_path):
        path = tmp_path / "plain.md"
        path.write_text("Just plain markdown")
        assert parse_front_matter(str(path)) is None

    def test_returns_none_for_invalid_toml(self, tmp_path):
        path = tmp_path / "bad.md"
        path.write_text("+++\ninvalid = [broken toml\n+++\nBody")
        assert parse_front_matter(str(path)) is None

    def test_parses_date_field(self, tmp_path):
        raw = 'title = "T"\ndate = "2025-06-12T20:00:00-03:00"'
        path = _write_post(tmp_path, "post.md", raw)
        fm = parse_front_matter(path)
        assert fm is not None
        # date is returned as a datetime object by tomllib
        assert "date" in fm

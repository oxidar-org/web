"""Tests for post detection and front matter parsing."""

import tempfile
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from detect import (
    derive_url,
    filter_post_files,
    parse_front_matter,
    should_share,
    detect_new_posts,
)


def _write_post(tmp_path, filename, front_matter, body="Hello world"):
    """Helper to create a temporary markdown post file."""
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

    def test_keeps_regular_posts(self):
        files = [
            "content/posts/2025.06.12-wasm/wasm.md",
            "content/posts/2026.01.26-rustconf/rustconf.md",
        ]
        assert filter_post_files(files) == files

    def test_empty_list(self):
        assert filter_post_files([]) == []


# --- parse_front_matter ---

class TestParseFrontMatter:
    def test_parses_toml_front_matter(self, tmp_path):
        path = _write_post(tmp_path, "post.md", 'title = "My Post"\ndraft = false')
        fm = parse_front_matter(path)
        assert fm is not None
        assert fm["title"] == "My Post"
        assert fm["draft"] is False

    def test_includes_body(self, tmp_path):
        path = _write_post(tmp_path, "post.md", 'title = "Test"', body="Some content here")
        fm = parse_front_matter(path)
        assert "Some content here" in fm["_body"]

    def test_parses_tags_and_categories(self, tmp_path):
        front_matter = 'title = "Test"\ntags = ["rust", "wasm"]\ncategories = ["Tutoriales"]'
        path = _write_post(tmp_path, "post.md", front_matter)
        fm = parse_front_matter(path)
        assert fm["tags"] == ["rust", "wasm"]
        assert fm["categories"] == ["Tutoriales"]

    def test_returns_none_for_missing_file(self):
        assert parse_front_matter("/nonexistent/file.md") is None

    def test_returns_none_for_no_front_matter(self, tmp_path):
        path = tmp_path / "plain.md"
        path.write_text("Just a plain markdown file")
        assert parse_front_matter(str(path)) is None

    def test_returns_none_for_invalid_toml(self, tmp_path):
        path = tmp_path / "bad.md"
        path.write_text("+++\ninvalid = [toml\n+++\nBody")
        assert parse_front_matter(str(path)) is None


# --- should_share ---

class TestShouldShare:
    def test_default_post_should_share(self):
        assert should_share({"title": "Test", "draft": False}) is True

    def test_draft_should_not_share(self):
        assert should_share({"draft": True}) is False

    def test_share_false_should_not_share(self):
        assert should_share({"share": False}) is False

    def test_hidden_from_home_should_not_share(self):
        assert should_share({"hiddenFromHomePage": True}) is False

    def test_share_not_set_defaults_to_share(self):
        assert should_share({"title": "Test"}) is True

    def test_share_true_should_share(self):
        assert should_share({"share": True, "draft": False}) is True


# --- derive_url ---

class TestDeriveUrl:
    def test_basic_url(self):
        url = derive_url("content/posts/my-post/my-post.md", "https://oxidar.org")
        assert url == "https://oxidar.org/my-post/"

    def test_strips_trailing_slash(self):
        url = derive_url("content/posts/foo/foo.md", "https://oxidar.org/")
        assert url == "https://oxidar.org/foo/"

    def test_date_prefixed_folder(self):
        url = derive_url(
            "content/posts/2026.01.26-rustconf/rustconf-2026-cfp.md",
            "https://oxidar.org",
        )
        assert url == "https://oxidar.org/rustconf-2026-cfp/"


# --- detect_new_posts (with posts_file) ---

class TestDetectNewPosts:
    def test_detects_from_posts_file(self, tmp_path):
        post_path = _write_post(
            tmp_path, "content/posts/test/test.md",
            'title = "Test Post"\ndescription = "A test"\ntags = ["rust"]',
            body="Body content",
        )
        posts_file = tmp_path / "posts.txt"
        posts_file.write_text(post_path)

        posts = detect_new_posts(
            repo_root=str(tmp_path),
            base_url="https://oxidar.org",
            posts_file=str(posts_file),
        )
        assert len(posts) == 1
        assert posts[0]["title"] == "Test Post"
        assert posts[0]["description"] == "A test"
        assert posts[0]["tags"] == ["rust"]
        assert "Body content" in posts[0]["body"]

    def test_skips_draft_posts(self, tmp_path):
        post_path = _write_post(
            tmp_path, "content/posts/draft/draft.md",
            'title = "Draft"\ndraft = true',
        )
        posts_file = tmp_path / "posts.txt"
        posts_file.write_text(post_path)

        posts = detect_new_posts(
            repo_root=str(tmp_path),
            base_url="https://oxidar.org",
            posts_file=str(posts_file),
        )
        assert len(posts) == 0

    def test_empty_posts_file(self, tmp_path):
        posts_file = tmp_path / "empty.txt"
        posts_file.write_text("")
        posts = detect_new_posts(posts_file=str(posts_file))
        assert posts == []

    def test_missing_posts_file(self):
        posts = detect_new_posts(posts_file="/nonexistent/posts.txt")
        assert posts == []

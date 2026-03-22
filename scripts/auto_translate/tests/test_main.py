"""Tests for auto_translate main helpers."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from main import _english_path, _needs_translation, _detect_posts


# ---------------------------------------------------------------------------
# _english_path
# ---------------------------------------------------------------------------

class TestEnglishPath:
    def test_basic_conversion(self):
        result = _english_path("content/posts/foo/foo.md")
        assert result == Path("content/posts/foo/foo.en.md")

    def test_date_prefixed_folder(self):
        result = _english_path("content/posts/2026.03.14-snakear/snakear.md")
        assert result == Path("content/posts/2026.03.14-snakear/snakear.en.md")

    def test_already_absolute_path(self):
        result = _english_path("/repo/content/posts/foo/foo.md")
        assert result == Path("/repo/content/posts/foo/foo.en.md")

    def test_stem_only_no_extra_suffix(self):
        """snakear.md -> snakear.en.md, NOT snakear.en.en.md."""
        result = _english_path("content/posts/snakear/snakear.md")
        assert result.name == "snakear.en.md"

    def test_does_not_double_add_en(self):
        """Calling on an already-.en.md path is not a use case, but shouldn't infinitely recurse."""
        result = _english_path("content/posts/foo/foo.en.md")
        assert result.name == "foo.en.en.md"


# ---------------------------------------------------------------------------
# _needs_translation
# ---------------------------------------------------------------------------

class TestNeedsTranslation:
    def test_needs_translation_when_no_en_file(self, tmp_path):
        # Create only the Spanish file
        post_dir = tmp_path / "content" / "posts" / "foo"
        post_dir.mkdir(parents=True)
        (post_dir / "foo.md").write_text("+++\ntitle = 'T'\n+++\nBody")

        assert _needs_translation("content/posts/foo/foo.md", str(tmp_path)) is True

    def test_no_translation_needed_when_en_exists(self, tmp_path):
        post_dir = tmp_path / "content" / "posts" / "foo"
        post_dir.mkdir(parents=True)
        (post_dir / "foo.md").write_text("+++\ntitle = 'T'\n+++\nBody")
        (post_dir / "foo.en.md").write_text("+++\ntitle = 'T'\n+++\nBody")

        assert _needs_translation("content/posts/foo/foo.md", str(tmp_path)) is False


# ---------------------------------------------------------------------------
# _detect_posts
# ---------------------------------------------------------------------------

class TestDetectPosts:
    def _write_post(self, tmp_path, rel_path, front_matter, body="Body"):
        full = tmp_path / rel_path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(f"+++\n{front_matter}\n+++\n{body}")
        return rel_path

    def test_detects_post_without_en_sibling(self, tmp_path):
        rel = self._write_post(
            tmp_path, "content/posts/foo/foo.md",
            'title = "Test"\ndraft = false',
        )
        posts_file = tmp_path / "posts.txt"
        posts_file.write_text(rel)

        result = _detect_posts(str(posts_file), str(tmp_path))
        assert result == [rel]

    def test_skips_post_that_already_has_en_sibling(self, tmp_path):
        rel = self._write_post(
            tmp_path, "content/posts/foo/foo.md",
            'title = "Test"\ndraft = false',
        )
        # Create the .en.md sibling
        en = tmp_path / "content/posts/foo/foo.en.md"
        en.write_text("+++\ntitle = \"Test\"\n+++\nBody")

        posts_file = tmp_path / "posts.txt"
        posts_file.write_text(rel)

        result = _detect_posts(str(posts_file), str(tmp_path))
        assert result == []

    def test_returns_empty_for_missing_posts_file(self, tmp_path):
        result = _detect_posts("/nonexistent/posts.txt", str(tmp_path))
        assert result == []

    def test_returns_empty_for_empty_posts_file(self, tmp_path):
        posts_file = tmp_path / "empty.txt"
        posts_file.write_text("")
        result = _detect_posts(str(posts_file), str(tmp_path))
        assert result == []

    def test_returns_empty_when_no_posts_file_and_no_repo(self, tmp_path):
        # Without a posts_file, falls back to git diff which will return nothing in tmp_path
        result = _detect_posts(None, str(tmp_path))
        assert result == []

    def test_multiple_posts_only_untranslated_returned(self, tmp_path):
        rel_a = self._write_post(
            tmp_path, "content/posts/a/a.md", 'title = "A"'
        )
        rel_b = self._write_post(
            tmp_path, "content/posts/b/b.md", 'title = "B"'
        )
        # b already has a translation
        (tmp_path / "content/posts/b/b.en.md").write_text("+++\ntitle = \"B\"\n+++\nBody")

        posts_file = tmp_path / "posts.txt"
        posts_file.write_text(f"{rel_a}\n{rel_b}\n")

        result = _detect_posts(str(posts_file), str(tmp_path))
        assert result == [rel_a]

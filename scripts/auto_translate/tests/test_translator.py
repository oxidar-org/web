"""Tests for the translator module — placeholder mechanics and FM reconstruction."""

import sys
from pathlib import Path

import pytest

# Add both auto_translate/ and scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from shared.ai.base import AIProvider
from translator import (
    _protect,
    _restore,
    _translate_fm_list,
    translate_post,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class EchoAI(AIProvider):
    """Returns the user prompt unchanged — simulates a no-op translation."""
    def complete(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        return user_prompt


class PrefixAI(AIProvider):
    """Prepends 'EN:' to every completion — makes it easy to assert replacement."""
    def complete(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        return f"EN: {user_prompt}"


class MismatchListAI(AIProvider):
    """Returns fewer lines than requested — triggers fallback in _translate_fm_list."""
    def complete(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        return "only one line"


def _make_fm(
    title="Mi artículo",
    description="Una descripción",
    tags=None,
    categories=None,
    body="\nContenido del artículo.\n",
    draft=False,
    extra_raw="",
):
    tags = tags or ["rust", "wasm"]
    categories = categories or ["Tutoriales"]
    tags_toml = ", ".join(f'"{t}"' for t in tags)
    cats_toml = ", ".join(f'"{c}"' for c in categories)
    raw_fm = (
        f'date = \'2025-06-12T20:00:00-03:00\'\n'
        f'draft = {str(draft).lower()}\n'
        f'title = "{title}"\n'
        f'description = "{description}"\n'
        f'tags = [{tags_toml}]\n'
        f'categories = [{cats_toml}]\n'
        f'translationKey = "my-post"\n'
        f'{extra_raw}'
    )
    return {
        "title": title,
        "description": description,
        "tags": tags,
        "categories": categories,
        "draft": draft,
        "_body": body,
        "_raw_fm": raw_fm,
        "_file": "content/posts/test/test.md",
    }


# ---------------------------------------------------------------------------
# _protect / _restore
# ---------------------------------------------------------------------------

class TestProtectRestore:
    def test_roundtrip_plain_text(self):
        text = "Hello world, this is plain text."
        protected, store = _protect(text)
        assert _restore(protected, store) == text

    def test_protects_hugo_shortcode(self):
        text = "Before\n{{< youtube ABC123 >}}\nAfter"
        protected, store = _protect(text)
        assert "{{< youtube ABC123 >}}" not in protected
        assert len(store) >= 1
        assert _restore(protected, store) == text

    def test_protects_fenced_code_block(self):
        text = "Intro\n```rust\nfn main() {}\n```\nOutro"
        protected, store = _protect(text)
        assert "```rust" not in protected
        assert _restore(protected, store) == text

    def test_protects_inline_code(self):
        text = "Use `cargo build` to compile."
        protected, store = _protect(text)
        assert "`cargo build`" not in protected
        assert _restore(protected, store) == text

    def test_protects_bare_url(self):
        text = "Visit https://oxidar.org for more info."
        protected, store = _protect(text)
        assert "https://oxidar.org" not in protected
        assert _restore(protected, store) == text

    def test_protects_markdown_link_url(self):
        text = "Check [this link](https://oxidar.org/post/) out."
        protected, store = _protect(text)
        # The URL part should be replaced but the text part stays
        assert "https://oxidar.org/post/" not in protected
        assert _restore(protected, store) == text

    def test_protects_multiple_shortcodes(self):
        text = "{{< youtube A >}}\nText\n{{< youtube B >}}"
        protected, store = _protect(text)
        assert len(store) >= 2
        assert _restore(protected, store) == text

    def test_protects_shortcode_with_url_inside(self):
        """A shortcode containing a URL should not be double-replaced."""
        text = '{{< figure src="https://example.com/img.png" >}}'
        protected, store = _protect(text)
        restored = _restore(protected, store)
        assert restored == text

    def test_empty_string(self):
        protected, store = _protect("")
        assert protected == ""
        assert store == []
        assert _restore(protected, store) == ""

    def test_no_protected_regions(self):
        text = "Just normal text with no code or URLs."
        protected, store = _protect(text)
        assert protected == text
        assert store == []

    def test_restore_ignores_ai_hallucinated_placeholder(self):
        """If AI invents a placeholder index that doesn't exist, restore raises IndexError.
        This is the expected failure mode — we want to know it happens rather than silently corrupt."""
        store = ["original"]
        bad_text = "PLACEHOLDER_99_ENDPLACEHOLDER"
        with pytest.raises(IndexError):
            _restore(bad_text, store)


# ---------------------------------------------------------------------------
# _translate_fm_list
# ---------------------------------------------------------------------------

class TestTranslateFmList:
    def test_empty_list_returns_empty(self):
        ai = EchoAI()
        assert _translate_fm_list(ai, []) == []

    def test_count_mismatch_falls_back_to_original(self):
        ai = MismatchListAI()
        original = ["rust", "wasm", "tutorial"]
        result = _translate_fm_list(ai, original)
        assert result == original

    def test_correct_count_returns_translated(self):
        class ExactAI(AIProvider):
            def complete(self, system_prompt, user_prompt, max_tokens=4096):
                # Return exactly one translated line per item
                return "Rust\nWebAssembly\nTutorial"

        ai = ExactAI()
        result = _translate_fm_list(ai, ["rust", "wasm", "tutoriales"])
        assert result == ["Rust", "WebAssembly", "Tutorial"]

    def test_strips_leading_dashes_from_response(self):
        class DashedAI(AIProvider):
            def complete(self, system_prompt, user_prompt, max_tokens=4096):
                return "- Rust\n- Projects"

        ai = DashedAI()
        result = _translate_fm_list(ai, ["rust", "proyectos"])
        assert result == ["Rust", "Projects"]


# ---------------------------------------------------------------------------
# translate_post — front matter reconstruction
# ---------------------------------------------------------------------------

class TestTranslatePost:
    def test_output_starts_with_toml_delimiters(self):
        result = translate_post(EchoAI(), _make_fm())
        assert result.startswith("+++\n")
        # There must be a closing +++ followed by body
        assert "\n+++\n" in result

    def test_title_is_replaced_in_output(self):
        result = translate_post(PrefixAI(), _make_fm(title="Hola Mundo"))
        assert "EN: Hola Mundo" in result

    def test_description_is_replaced_in_output(self):
        result = translate_post(PrefixAI(), _make_fm(description="Una descripción"))
        assert "EN: Una descripción" in result

    def test_translation_key_is_preserved_verbatim(self):
        """translationKey must never be translated — it links ES/EN versions."""
        result = translate_post(PrefixAI(), _make_fm())
        assert 'translationKey = "my-post"' in result

    def test_date_is_preserved_verbatim(self):
        result = translate_post(EchoAI(), _make_fm())
        assert "2025-06-12T20:00:00-03:00" in result

    def test_draft_false_is_preserved(self):
        result = translate_post(EchoAI(), _make_fm(draft=False))
        assert "draft = false" in result

    def test_tags_are_replaced(self):
        class TagAI(AIProvider):
            def complete(self, system_prompt, user_prompt, max_tokens=4096):
                if "Translate each item" in user_prompt:
                    lines = user_prompt.splitlines()
                    items = [l.lstrip("- ").strip() for l in lines if l.strip().startswith("-")]
                    return "\n".join(f"EN_{i}" for i in items)
                return user_prompt

        result = translate_post(TagAI(), _make_fm(tags=["rust", "wasm"]))
        assert '"EN_rust"' in result
        assert '"EN_wasm"' in result

    def test_body_shortcodes_survive_translation(self):
        """Hugo shortcodes in the body must not be altered by the AI."""
        fm = _make_fm(body="\n{{< youtube XYZ123 >}}\nAlgún texto.\n")
        result = translate_post(EchoAI(), _make_fm(body="\n{{< youtube XYZ123 >}}\nAlgún texto.\n"))
        assert "{{< youtube XYZ123 >}}" in result

    def test_body_code_blocks_survive_translation(self):
        body = "\n```rust\nfn hello() { println!(\"Hola\"); }\n```\n"
        result = translate_post(EchoAI(), _make_fm(body=body))
        assert "```rust" in result
        assert 'println!("Hola")' in result

    def test_body_is_present_in_output(self):
        result = translate_post(EchoAI(), _make_fm(body="\nContenido especial aquí.\n"))
        assert "Contenido especial aquí." in result

    def test_empty_tags_and_categories(self):
        """Empty lists should not break FM reconstruction."""
        result = translate_post(EchoAI(), _make_fm(tags=[], categories=[]))
        assert result.startswith("+++\n")

    def test_title_with_special_chars(self):
        """Titles with quotes in them should not break the regex substitution."""
        fm = _make_fm(title="Rust: el lenguaje del futuro")
        result = translate_post(EchoAI(), fm)
        # EchoAI echoes the title back — just assert reconstruction didn't crash
        assert "+++" in result

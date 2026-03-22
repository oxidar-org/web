"""Translate a Spanish Hugo post to English using an AI provider."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shared.ai import AIProvider  # noqa: E402

# Front matter fields translated by the AI (values replaced verbatim for others)
_TRANSLATABLE_FM_FIELDS = ("title", "description")
# List fields translated element-by-element
_TRANSLATABLE_FM_LISTS = ("tags", "categories")

# Placeholder format used to hide Hugo shortcodes and fenced code blocks from the AI
_PLACEHOLDER = "PLACEHOLDER_{index}_ENDPLACEHOLDER"
_PLACEHOLDER_RE = re.compile(r"PLACEHOLDER_(\d+)_ENDPLACEHOLDER")

# Patterns to protect from translation (order matters)
_PROTECT_PATTERNS = [
    # Fenced code blocks (``` ... ```)
    re.compile(r"(```[\s\S]*?```)", re.MULTILINE),
    # Hugo shortcodes  {{< ... >}} and {{% ... %}}
    re.compile(r"(\{\{[<%].*?[>%]\}\})"),
    # Inline code `...`
    re.compile(r"(`[^`\n]+`)"),
    # URLs in markdown links [text](url) — protect the url part
    re.compile(r"(\]\(https?://[^\)]+\))"),
    # Bare URLs
    re.compile(r"(https?://\S+)"),
]

SYSTEM_PROMPT = """\
You are a professional technical translator specializing in Rust programming and software development.
Translate the given Spanish text to clear, natural English for a developer audience.

Rules:
- Preserve all markdown formatting exactly (headings, bold, italic, lists, tables)
- Never translate or modify placeholder tokens (PLACEHOLDER_N_ENDPLACEHOLDER) — keep them verbatim
- Translate technical terms only when a widely accepted English equivalent exists
- Keep proper nouns, project names, and brand names unchanged
- Respond ONLY with the translated text, no explanations
"""


def _protect(text: str) -> tuple[str, list[str]]:
    """Replace protected regions with placeholders. Returns modified text and store."""
    store: list[str] = []

    def replacer(m: re.Match) -> str:
        idx = len(store)
        store.append(m.group(0))
        return _PLACEHOLDER.format(index=idx)

    for pattern in _PROTECT_PATTERNS:
        text = pattern.sub(replacer, text)

    return text, store


def _restore(text: str, store: list[str]) -> str:
    """Restore placeholders back to original content."""
    def replacer(m: re.Match) -> str:
        return store[int(m.group(1))]
    return _PLACEHOLDER_RE.sub(replacer, text)


def _translate_text(ai: AIProvider, text: str) -> str:
    """Translate a block of text, protecting non-translatable regions."""
    protected, store = _protect(text)
    translated = ai.complete(SYSTEM_PROMPT, protected)
    return _restore(translated, store)


def _translate_fm_field(ai: AIProvider, value: str) -> str:
    """Translate a single front matter string field."""
    return ai.complete(SYSTEM_PROMPT, value).strip().strip('"').strip("'")


def _translate_fm_list(ai: AIProvider, items: list[str]) -> list[str]:
    """Translate a list of front matter tags/categories."""
    if not items:
        return items
    joined = "\n".join(f"- {item}" for item in items)
    prompt = f"Translate each item to English. Respond with one item per line, no dashes:\n{joined}"
    result = ai.complete(SYSTEM_PROMPT, prompt)
    translated = [line.strip().lstrip("- ").strip() for line in result.splitlines() if line.strip()]
    # Fall back to original list if count mismatches
    if len(translated) != len(items):
        return items
    return translated


def translate_post(ai: AIProvider, fm: dict) -> str:
    """Translate a parsed post (front matter + body) and return the full .en.md content."""
    # --- Translate front matter fields ---
    translated_title = _translate_fm_field(ai, fm.get("title", ""))
    translated_desc = _translate_fm_field(ai, fm.get("description", ""))
    translated_tags = _translate_fm_list(ai, fm.get("tags", []))
    translated_cats = _translate_fm_list(ai, fm.get("categories", []))

    # --- Rebuild TOML front matter ---
    # We reconstruct from the parsed values to keep it clean.
    # Fields not listed here are copied verbatim from _raw_fm.
    raw_fm: str = fm.get("_raw_fm", "")

    def _replace_fm_value(raw: str, key: str, new_value: str) -> str:
        """Replace a string value for `key = '...'` or `key = "..."` in raw TOML."""
        pattern = re.compile(
            rf'^({re.escape(key)}\s*=\s*)["\'].*?["\']',
            re.MULTILINE,
        )
        replacement = rf'\g<1>"{new_value}"'
        return pattern.sub(replacement, raw)

    def _replace_fm_list(raw: str, key: str, new_items: list[str]) -> str:
        """Replace an array value for `key = [...]` in raw TOML."""
        pattern = re.compile(
            rf'^({re.escape(key)}\s*=\s*)\[.*?\]',
            re.MULTILINE | re.DOTALL,
        )
        items_str = ", ".join(f'"{item}"' for item in new_items)
        replacement = rf'\g<1>[{items_str}]'
        return pattern.sub(replacement, raw)

    new_fm = raw_fm
    new_fm = _replace_fm_value(new_fm, "title", translated_title)
    new_fm = _replace_fm_value(new_fm, "description", translated_desc)
    new_fm = _replace_fm_list(new_fm, "tags", translated_tags)
    new_fm = _replace_fm_list(new_fm, "categories", translated_cats)

    # --- Translate body ---
    body = fm.get("_body", "")
    translated_body = _translate_text(ai, body)

    return f"+++\n{new_fm}\n+++\n{translated_body}"

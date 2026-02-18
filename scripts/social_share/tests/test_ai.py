"""Tests for AI provider base and factory."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai.base import AIProvider, build_user_prompt
from ai import get_ai_provider


class DummyProvider(AIProvider):
    """Concrete implementation for testing the base class."""

    def generate(self, post, platform_name, config):
        return "test"


class TestBuildUserPrompt:
    def setup_method(self):
        self.post = {
            "title": "Rust y WebAssembly",
            "description": "Tutorial de Rust con WASM",
            "tags": ["rust", "wasm"],
            "url": "https://oxidar.org/wasm/",
            "body": "Contenido del artículo...",
        }
        self.config = {
            "platforms": {
                "twitter": {
                    "max_chars": 280,
                    "prompt_addendum": "Sé conciso.",
                },
            },
        }

    def test_includes_post_title(self):
        prompt = build_user_prompt(self.post, "twitter", self.config)
        assert "Rust y WebAssembly" in prompt

    def test_includes_url(self):
        prompt = build_user_prompt(self.post, "twitter", self.config)
        assert "https://oxidar.org/wasm/" in prompt

    def test_includes_tags(self):
        prompt = build_user_prompt(self.post, "twitter", self.config)
        assert "rust" in prompt
        assert "wasm" in prompt

    def test_includes_platform_rules(self):
        prompt = build_user_prompt(self.post, "twitter", self.config)
        assert "280" in prompt
        assert "Sé conciso." in prompt

    def test_handles_missing_platform_config(self):
        prompt = build_user_prompt(self.post, "bluesky", self.config)
        assert "Rust y WebAssembly" in prompt


class TestGetAiProvider:
    def test_raises_on_unknown_provider(self, monkeypatch):
        monkeypatch.setenv("AI_PROVIDER", "unknown")
        with pytest.raises(ValueError, match="Unknown AI provider"):
            get_ai_provider()

    @pytest.mark.skipif(
        not __import__("importlib").util.find_spec("anthropic"),
        reason="anthropic SDK not installed",
    )
    def test_anthropic_requires_api_key(self, monkeypatch):
        monkeypatch.setenv("AI_PROVIDER", "anthropic")
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
            get_ai_provider()

    @pytest.mark.skipif(
        not __import__("importlib").util.find_spec("openai"),
        reason="openai SDK not installed",
    )
    def test_openai_requires_api_key(self, monkeypatch):
        monkeypatch.setenv("AI_PROVIDER", "openai")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            get_ai_provider()

"""Tests for shared AI provider factory."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai import get_ai_provider
from ai.base import AIProvider


class DummyProvider(AIProvider):
    def complete(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        return "ok"


class TestGetAiProvider:
    def test_raises_on_unknown_provider(self, monkeypatch):
        monkeypatch.setenv("AI_PROVIDER", "nonexistent_provider")
        with pytest.raises(ValueError, match="Unknown AI provider"):
            get_ai_provider()

    def test_default_is_github_models(self, monkeypatch):
        monkeypatch.delenv("AI_PROVIDER", raising=False)
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        # Should attempt github_models and fail on missing token
        with pytest.raises(ValueError, match="GITHUB_TOKEN"):
            get_ai_provider(default="github_models")

    def test_github_models_requires_token(self, monkeypatch):
        monkeypatch.setenv("AI_PROVIDER", "github_models")
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        with pytest.raises(ValueError, match="GITHUB_TOKEN"):
            get_ai_provider()

    def test_anthropic_requires_api_key(self, monkeypatch):
        monkeypatch.setenv("AI_PROVIDER", "anthropic")
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
            get_ai_provider()

    def test_openai_requires_api_key(self, monkeypatch):
        monkeypatch.setenv("AI_PROVIDER", "openai")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            get_ai_provider()


class TestAIProviderInterface:
    def test_dummy_provider_implements_complete(self):
        provider = DummyProvider()
        result = provider.complete("system", "user")
        assert result == "ok"

    def test_cannot_instantiate_abstract_base(self):
        with pytest.raises(TypeError):
            AIProvider()

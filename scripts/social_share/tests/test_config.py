"""Tests for configuration loading."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import load_config, get_ai_provider_name, get_base_url


class TestLoadConfig:
    def test_loads_valid_yaml(self, tmp_path):
        config_file = tmp_path / "config.yaml"
        config_file.write_text("community:\n  name: Test\n  website: https://example.com\n")
        config = load_config(str(config_file))
        assert config["community"]["name"] == "Test"

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_config("/nonexistent/config.yaml")


class TestGetAiProviderName:
    def test_defaults_to_anthropic(self, monkeypatch):
        monkeypatch.delenv("AI_PROVIDER", raising=False)
        assert get_ai_provider_name() == "anthropic"

    def test_reads_from_env(self, monkeypatch):
        monkeypatch.setenv("AI_PROVIDER", "openai")
        assert get_ai_provider_name() == "openai"


class TestGetBaseUrl:
    def test_extracts_from_config(self):
        config = {"community": {"website": "https://oxidar.org"}}
        assert get_base_url(config) == "https://oxidar.org"

    def test_defaults_when_missing(self):
        assert get_base_url({}) == "https://oxidar.org"

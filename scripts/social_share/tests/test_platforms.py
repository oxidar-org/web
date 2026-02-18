"""Tests for platform factory."""

import importlib
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from platforms import get_enabled_platforms

_has_platform_deps = all(
    importlib.util.find_spec(mod) for mod in ["tweepy", "requests", "atproto"]
)

# Fake credentials for testing platform init validation
_FAKE_CREDS = {
    "TWITTER_API_KEY": "fake",
    "TWITTER_API_SECRET": "fake",
    "TWITTER_ACCESS_TOKEN": "fake",
    "TWITTER_ACCESS_SECRET": "fake",
    "LINKEDIN_ACCESS_TOKEN": "fake",
    "LINKEDIN_ORG_ID": "fake",
    "BLUESKY_HANDLE": "fake",
    "BLUESKY_APP_PASSWORD": "fake",
    "TELEGRAM_BOT_TOKEN": "fake",
    "TELEGRAM_CHAT_ID": "fake",
}


def _set_fake_creds(monkeypatch):
    for key, val in _FAKE_CREDS.items():
        monkeypatch.setenv(key, val)


class TestGetEnabledPlatforms:
    def test_no_platforms_by_default(self, monkeypatch):
        for key in ["TWITTER_ENABLED", "LINKEDIN_ENABLED", "BLUESKY_ENABLED", "TELEGRAM_ENABLED"]:
            monkeypatch.delenv(key, raising=False)
        platforms = get_enabled_platforms()
        assert platforms == []

    @pytest.mark.skipif(not _has_platform_deps, reason="platform SDKs not installed")
    def test_enables_telegram(self, monkeypatch):
        _set_fake_creds(monkeypatch)
        monkeypatch.setenv("TELEGRAM_ENABLED", "true")
        for key in ["TWITTER_ENABLED", "LINKEDIN_ENABLED", "BLUESKY_ENABLED"]:
            monkeypatch.delenv(key, raising=False)
        platforms = get_enabled_platforms()
        assert len(platforms) == 1
        assert platforms[0].name == "telegram"

    @pytest.mark.skipif(not _has_platform_deps, reason="platform SDKs not installed")
    def test_enables_multiple(self, monkeypatch):
        _set_fake_creds(monkeypatch)
        monkeypatch.setenv("TWITTER_ENABLED", "true")
        monkeypatch.setenv("TELEGRAM_ENABLED", "true")
        monkeypatch.delenv("LINKEDIN_ENABLED", raising=False)
        monkeypatch.delenv("BLUESKY_ENABLED", raising=False)
        platforms = get_enabled_platforms()
        names = [p.name for p in platforms]
        assert "twitter" in names
        assert "telegram" in names
        assert len(platforms) == 2

    @pytest.mark.skipif(not _has_platform_deps, reason="platform SDKs not installed")
    def test_case_insensitive(self, monkeypatch):
        _set_fake_creds(monkeypatch)
        monkeypatch.setenv("BLUESKY_ENABLED", "True")
        for key in ["TWITTER_ENABLED", "LINKEDIN_ENABLED", "TELEGRAM_ENABLED"]:
            monkeypatch.delenv(key, raising=False)
        # Bluesky.from_env() calls client.login() — mock to avoid a real network call
        with patch("platforms.bluesky.Client"):
            platforms = get_enabled_platforms()
        assert len(platforms) == 1
        assert platforms[0].name == "bluesky"

    def test_false_disables(self, monkeypatch):
        monkeypatch.setenv("TWITTER_ENABLED", "false")
        monkeypatch.delenv("LINKEDIN_ENABLED", raising=False)
        monkeypatch.delenv("BLUESKY_ENABLED", raising=False)
        monkeypatch.delenv("TELEGRAM_ENABLED", raising=False)
        platforms = get_enabled_platforms()
        assert platforms == []

    @pytest.mark.skipif(not _has_platform_deps, reason="platform SDKs not installed")
    def test_missing_credentials_raises(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_ENABLED", "true")
        monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
        monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
        for key in ["TWITTER_ENABLED", "LINKEDIN_ENABLED", "BLUESKY_ENABLED"]:
            monkeypatch.delenv(key, raising=False)
        with pytest.raises(ValueError, match="Missing required environment variables"):
            get_enabled_platforms()

"""Tests for platform factory."""

import sys
from pathlib import Path

import importlib

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from platforms.base import get_enabled_platforms

_has_platform_deps = all(
    importlib.util.find_spec(mod) for mod in ["tweepy", "requests", "atproto"]
)


class TestGetEnabledPlatforms:
    def test_no_platforms_by_default(self, monkeypatch):
        for key in ["TWITTER_ENABLED", "LINKEDIN_ENABLED", "BLUESKY_ENABLED", "TELEGRAM_ENABLED"]:
            monkeypatch.delenv(key, raising=False)
        platforms = get_enabled_platforms()
        assert platforms == []

    @pytest.mark.skipif(not _has_platform_deps, reason="platform SDKs not installed")
    def test_enables_telegram(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_ENABLED", "true")
        for key in ["TWITTER_ENABLED", "LINKEDIN_ENABLED", "BLUESKY_ENABLED"]:
            monkeypatch.delenv(key, raising=False)
        platforms = get_enabled_platforms()
        assert len(platforms) == 1
        assert platforms[0].name == "telegram"

    @pytest.mark.skipif(not _has_platform_deps, reason="platform SDKs not installed")
    def test_enables_multiple(self, monkeypatch):
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
        monkeypatch.setenv("BLUESKY_ENABLED", "True")
        for key in ["TWITTER_ENABLED", "LINKEDIN_ENABLED", "TELEGRAM_ENABLED"]:
            monkeypatch.delenv(key, raising=False)
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

"""Tests for platform publish methods using mocks."""

import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from platforms.base import PublishResult

_has_tweepy = importlib.util.find_spec("tweepy") is not None
_has_requests = importlib.util.find_spec("requests") is not None
_has_atproto = importlib.util.find_spec("atproto") is not None

FAKE_POST = {
    "title": "Test Post",
    "description": "A test",
    "url": "https://oxidar.org/test/",
    "tags": ["rust"],
}


# --- Twitter ---

@pytest.mark.skipif(not _has_tweepy, reason="tweepy not installed")
class TestTwitterPublish:
    def _make_platform(self, monkeypatch):
        monkeypatch.setenv("TWITTER_API_KEY", "fake")
        monkeypatch.setenv("TWITTER_API_SECRET", "fake")
        monkeypatch.setenv("TWITTER_ACCESS_TOKEN", "fake")
        monkeypatch.setenv("TWITTER_ACCESS_SECRET", "fake")
        from platforms.twitter import TwitterPlatform
        return TwitterPlatform()

    @patch("platforms.twitter.tweepy.Client")
    def test_successful_tweet(self, mock_client_cls, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_client = mock_client_cls.return_value
        mock_client.create_tweet.return_value = MagicMock(data={"id": "12345"})

        result = platform.publish("Hello world", FAKE_POST)
        assert result.success is True
        assert "12345" in result.url

    @patch("platforms.twitter.tweepy.Client")
    def test_tweet_api_error(self, mock_client_cls, monkeypatch):
        import tweepy
        platform = self._make_platform(monkeypatch)
        mock_client = mock_client_cls.return_value
        mock_client.create_tweet.side_effect = tweepy.TweepyException("Rate limited")

        result = platform.publish("Hello", FAKE_POST)
        assert result.success is False
        assert "Rate limited" in result.error

    @patch("platforms.twitter.tweepy.Client")
    def test_tweet_malformed_response(self, mock_client_cls, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_client = mock_client_cls.return_value
        mock_client.create_tweet.return_value = MagicMock(data={})

        result = platform.publish("Hello", FAKE_POST)
        assert result.success is False


# --- Telegram ---

@pytest.mark.skipif(not _has_requests, reason="requests not installed")
class TestTelegramPublish:
    def _make_platform(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
        from platforms.telegram import TelegramPlatform
        return TelegramPlatform()

    @patch("platforms.telegram.requests.post")
    def test_successful_send(self, mock_post, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_post.return_value = MagicMock(
            json=lambda: {"ok": True, "result": {"message_id": 42}}
        )

        result = platform.publish("Hello", FAKE_POST)
        assert result.success is True
        assert result.url == "42"

    @patch("platforms.telegram.requests.post")
    def test_telegram_api_error(self, mock_post, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_post.return_value = MagicMock(
            json=lambda: {"ok": False, "description": "Bad Request: chat not found"}
        )

        result = platform.publish("Hello", FAKE_POST)
        assert result.success is False
        assert "chat not found" in result.error

    @patch("platforms.telegram.requests.post")
    def test_telegram_non_json_response(self, mock_post, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_post.return_value = MagicMock(
            json=MagicMock(side_effect=ValueError("No JSON"))
        )

        result = platform.publish("Hello", FAKE_POST)
        assert result.success is False
        assert "No JSON" in result.error

    @patch("platforms.telegram.requests.post")
    def test_telegram_network_error(self, mock_post, monkeypatch):
        import requests
        platform = self._make_platform(monkeypatch)
        mock_post.side_effect = requests.ConnectionError("Connection refused")

        result = platform.publish("Hello", FAKE_POST)
        assert result.success is False
        assert "Connection refused" in result.error

    @patch("platforms.telegram.requests.post")
    def test_telegram_malformed_ok_response(self, mock_post, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_post.return_value = MagicMock(
            json=lambda: {"ok": True}  # missing "result" key
        )

        result = platform.publish("Hello", FAKE_POST)
        assert result.success is True
        assert result.url == ""  # gracefully empty


# --- LinkedIn ---

@pytest.mark.skipif(not _has_requests, reason="requests not installed")
class TestLinkedInPublish:
    def _make_platform(self, monkeypatch):
        monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "fake-token")
        monkeypatch.setenv("LINKEDIN_ORG_ID", "12345")
        from platforms.linkedin import LinkedInPlatform
        return LinkedInPlatform()

    @patch("platforms.linkedin.requests.post")
    def test_successful_post(self, mock_post, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_post.return_value = MagicMock(
            status_code=201,
            json=lambda: {"id": "urn:li:share:123"},
        )

        result = platform.publish("Hello LinkedIn", FAKE_POST)
        assert result.success is True

    @patch("platforms.linkedin.requests.post")
    def test_linkedin_http_error(self, mock_post, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_post.return_value = MagicMock(
            status_code=403, text="Forbidden"
        )

        result = platform.publish("Hello", FAKE_POST)
        assert result.success is False
        assert "403" in result.error

    @patch("platforms.linkedin.requests.post")
    def test_linkedin_non_json_on_success(self, mock_post, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_post.return_value = MagicMock(
            status_code=201,
            json=MagicMock(side_effect=ValueError("No JSON")),
        )

        result = platform.publish("Hello", FAKE_POST)
        assert result.success is False
        assert "No JSON" in result.error


# --- Bluesky ---

@pytest.mark.skipif(not _has_atproto, reason="atproto not installed")
class TestBlueskyPublish:
    def _make_platform(self, monkeypatch):
        monkeypatch.setenv("BLUESKY_HANDLE", "test.bsky.social")
        monkeypatch.setenv("BLUESKY_APP_PASSWORD", "fake-password")
        from platforms.bluesky import BlueskyPlatform
        return BlueskyPlatform()

    @patch("platforms.bluesky.Client")
    def test_successful_post(self, mock_client_cls, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_client = mock_client_cls.return_value
        mock_client.send_post.return_value = MagicMock(uri="at://did:plc:123/post/456")

        result = platform.publish("Hello Bluesky", FAKE_POST)
        assert result.success is True
        assert "at://" in result.url

    @patch("platforms.bluesky.Client")
    def test_bluesky_login_failure(self, mock_client_cls, monkeypatch):
        platform = self._make_platform(monkeypatch)
        mock_client = mock_client_cls.return_value
        mock_client.login.side_effect = Exception("Invalid credentials")

        result = platform.publish("Hello", FAKE_POST)
        assert result.success is False
        assert "Invalid credentials" in result.error

"""Tests for platform publish methods using direct client injection."""

import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock

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
    def _make_platform(self, mock_client=None):
        from platforms.twitter import TwitterPlatform
        return TwitterPlatform(client=mock_client or MagicMock())

    def test_successful_tweet(self):
        mock_client = MagicMock()
        mock_client.create_tweet.return_value = MagicMock(data={"id": "12345"})

        result = self._make_platform(mock_client).publish("Hello world", FAKE_POST)
        assert result.success is True
        assert "12345" in result.url

    def test_tweet_api_error(self):
        import tweepy
        mock_client = MagicMock()
        mock_client.create_tweet.side_effect = tweepy.TweepyException("Rate limited")

        result = self._make_platform(mock_client).publish("Hello", FAKE_POST)
        assert result.success is False
        assert "Rate limited" in result.error

    def test_tweet_malformed_response(self):
        mock_client = MagicMock()
        mock_client.create_tweet.return_value = MagicMock(data={})

        result = self._make_platform(mock_client).publish("Hello", FAKE_POST)
        assert result.success is False


# --- Telegram ---

@pytest.mark.skipif(not _has_requests, reason="requests not installed")
class TestTelegramPublish:
    def _make_platform(self, mock_session=None):
        from platforms.telegram import TelegramPlatform
        return TelegramPlatform(bot_token="fake-token", chat_id="-100123", session=mock_session or MagicMock())

    def test_successful_send(self):
        mock_session = MagicMock()
        mock_session.post.return_value = MagicMock(
            json=lambda: {"ok": True, "result": {"message_id": 42}}
        )

        result = self._make_platform(mock_session).publish("Hello", FAKE_POST)
        assert result.success is True
        assert result.url == "42"

    def test_telegram_api_error(self):
        mock_session = MagicMock()
        mock_session.post.return_value = MagicMock(
            json=lambda: {"ok": False, "description": "Bad Request: chat not found"}
        )

        result = self._make_platform(mock_session).publish("Hello", FAKE_POST)
        assert result.success is False
        assert "chat not found" in result.error

    def test_telegram_non_json_response(self):
        mock_session = MagicMock()
        mock_session.post.return_value = MagicMock(
            json=MagicMock(side_effect=ValueError("No JSON"))
        )

        result = self._make_platform(mock_session).publish("Hello", FAKE_POST)
        assert result.success is False
        assert "No JSON" in result.error

    def test_telegram_network_error(self):
        import requests
        mock_session = MagicMock()
        mock_session.post.side_effect = requests.ConnectionError("Connection refused")

        result = self._make_platform(mock_session).publish("Hello", FAKE_POST)
        assert result.success is False
        assert "Connection refused" in result.error

    def test_telegram_malformed_ok_response(self):
        mock_session = MagicMock()
        mock_session.post.return_value = MagicMock(
            json=lambda: {"ok": True}  # missing "result" key
        )

        result = self._make_platform(mock_session).publish("Hello", FAKE_POST)
        assert result.success is True
        assert result.url == ""  # gracefully empty


# --- LinkedIn ---

@pytest.mark.skipif(not _has_requests, reason="requests not installed")
class TestLinkedInPublish:
    def _make_platform(self, mock_session=None):
        from platforms.linkedin import LinkedInPlatform
        return LinkedInPlatform(access_token="fake-token", org_id="12345", session=mock_session or MagicMock())

    def test_successful_post(self):
        mock_session = MagicMock()
        mock_session.post.return_value = MagicMock(
            status_code=201,
            json=lambda: {"id": "urn:li:share:123"},
        )

        result = self._make_platform(mock_session).publish("Hello LinkedIn", FAKE_POST)
        assert result.success is True

    def test_linkedin_http_error(self):
        mock_session = MagicMock()
        mock_session.post.return_value = MagicMock(
            status_code=403, text="Forbidden"
        )

        result = self._make_platform(mock_session).publish("Hello", FAKE_POST)
        assert result.success is False
        assert "403" in result.error

    def test_linkedin_non_json_on_success(self):
        mock_session = MagicMock()
        mock_session.post.return_value = MagicMock(
            status_code=201,
            json=MagicMock(side_effect=ValueError("No JSON")),
        )

        result = self._make_platform(mock_session).publish("Hello", FAKE_POST)
        assert result.success is False
        assert "No JSON" in result.error


# --- Bluesky ---

@pytest.mark.skipif(not _has_atproto, reason="atproto not installed")
class TestBlueskyPublish:
    def _make_platform(self, mock_client=None):
        from platforms.bluesky import BlueskyPlatform
        return BlueskyPlatform(client=mock_client or MagicMock())

    def test_successful_post(self):
        mock_client = MagicMock()
        mock_client.send_post.return_value = MagicMock(uri="at://did:plc:123/post/456")

        result = self._make_platform(mock_client).publish("Hello Bluesky", FAKE_POST)
        assert result.success is True
        assert "at://" in result.url

    def test_bluesky_send_failure(self):
        mock_client = MagicMock()
        mock_client.send_post.side_effect = Exception("Service unavailable")

        result = self._make_platform(mock_client).publish("Hello", FAKE_POST)
        assert result.success is False
        assert "Service unavailable" in result.error

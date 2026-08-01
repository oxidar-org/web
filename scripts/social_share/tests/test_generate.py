"""Tests for message generation, length limits, and failure handling."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import _generate_messages

POST = {"title": "Rust en DebConf 26", "url": "https://oxidar.org/post/"}
CONFIG = {"platforms": {"bluesky": {"max_chars": 50}, "telegram": {"max_chars": 4096}}}


class FakeAI:
    """Returns canned text per platform, or raises if the value is an Exception."""

    def __init__(self, by_platform: dict):
        self._by_platform = by_platform

    def generate(self, post, platform_name, config):
        value = self._by_platform[platform_name]
        if isinstance(value, Exception):
            raise value
        return value


class TestLengthLimit:
    def test_keeps_message_within_limit(self):
        ai = FakeAI({"bluesky": "corto", "telegram": "largo pero permitido"})
        messages = _generate_messages([POST], ai, CONFIG, ["bluesky", "telegram"])
        assert [m["text"] for m in messages] == ["corto", "largo pero permitido"]

    def test_drops_over_limit_message_instead_of_truncating(self):
        # Truncation used to cut the trailing URL mid-string, publishing a dead link.
        long_text = "x" * 40 + " https://oxidar.org/why-who-where-rust-debconf26/"
        ai = FakeAI({"bluesky": long_text, "telegram": "ok"})
        messages = _generate_messages([POST], ai, CONFIG, ["bluesky", "telegram"])

        assert [m["platform"] for m in messages] == ["telegram"]
        assert all(m["text"] != long_text[:50] for m in messages)

    def test_message_exactly_at_limit_is_kept(self):
        ai = FakeAI({"bluesky": "y" * 50})
        messages = _generate_messages([POST], ai, CONFIG, ["bluesky"])
        assert len(messages) == 1


class TestFailureHandling:
    def test_partial_failure_returns_remaining_messages(self):
        ai = FakeAI({"bluesky": RuntimeError("410 Gone"), "telegram": "ok"})
        messages = _generate_messages([POST], ai, CONFIG, ["bluesky", "telegram"])
        assert [m["platform"] for m in messages] == ["telegram"]

    def test_exits_nonzero_when_every_attempt_fails(self):
        # A retired or misconfigured provider must fail the job, not pass as a no-op.
        ai = FakeAI({"bluesky": RuntimeError("410 Gone"), "telegram": RuntimeError("410 Gone")})
        with pytest.raises(SystemExit) as exc:
            _generate_messages([POST], ai, CONFIG, ["bluesky", "telegram"])
        assert exc.value.code == 1

    def test_exits_nonzero_when_all_messages_dropped_for_length(self):
        ai = FakeAI({"bluesky": "z" * 500})
        with pytest.raises(SystemExit) as exc:
            _generate_messages([POST], ai, CONFIG, ["bluesky"])
        assert exc.value.code == 1

    def test_no_posts_does_not_exit(self):
        assert _generate_messages([], FakeAI({}), CONFIG, ["bluesky"]) == []

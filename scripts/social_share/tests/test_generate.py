"""Tests for message generation, length limits, and failure handling."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import _generate_messages

POST = {"title": "Rust en DebConf 26", "url": "https://oxidar.org/post/"}
# include_url is off here so these cases exercise the length rules in isolation;
# URL reservation has its own suite in test_url_budget.py.
CONFIG = {
    "platforms": {
        "bluesky": {"max_chars": 50, "include_url": False},
        "telegram": {"max_chars": 4096, "include_url": False},
    }
}


class FakeAI:
    """Returns canned text per platform, or raises if the value is an Exception.

    A list value yields one entry per call, so retries can return something
    different from the first attempt.
    """

    def __init__(self, by_platform: dict):
        self._by_platform = {k: list(v) if isinstance(v, list) else [v] for k, v in by_platform.items()}
        self.calls: list[tuple[str, str]] = []

    def generate(self, post, platform_name, config, feedback=""):
        self.calls.append((platform_name, feedback))
        queue = self._by_platform[platform_name]
        value = queue.pop(0) if len(queue) > 1 else queue[0]
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


class TestRetryOnOvershoot:
    def test_does_not_retry_when_first_attempt_fits(self):
        ai = FakeAI({"bluesky": "corto"})
        _generate_messages([POST], ai, CONFIG, ["bluesky"])
        assert len(ai.calls) == 1
        assert ai.calls[0][1] == ""  # no feedback on a first attempt

    def test_retries_once_when_over_budget(self):
        ai = FakeAI({"bluesky": ["x" * 80, "corto"]})
        messages = _generate_messages([POST], ai, CONFIG, ["bluesky"])
        assert len(ai.calls) == 2
        assert [m["text"] for m in messages] == ["corto"]

    def test_retry_feedback_states_measured_overshoot(self):
        ai = FakeAI({"bluesky": ["x" * 80, "corto"]})
        _generate_messages([POST], ai, CONFIG, ["bluesky"])

        feedback = ai.calls[1][1]
        assert "80" in feedback  # what it actually wrote
        assert "50" in feedback  # the budget
        assert "30" in feedback  # how far over

    def test_drops_when_retry_also_overshoots(self):
        # telegram succeeds so this exercises the drop, not the all-failed exit.
        ai = FakeAI({"bluesky": ["x" * 80, "y" * 70], "telegram": "ok"})
        messages = _generate_messages([POST], ai, CONFIG, ["bluesky", "telegram"])

        bluesky_calls = [c for c in ai.calls if c[0] == "bluesky"]
        assert len(bluesky_calls) == 2  # retried exactly once, no loop
        assert [m["platform"] for m in messages] == ["telegram"]

    def test_retry_failure_propagates_as_generation_failure(self):
        ai = FakeAI({"bluesky": ["x" * 80, RuntimeError("boom")], "telegram": "ok"})
        messages = _generate_messages([POST], ai, CONFIG, ["bluesky", "telegram"])
        assert [m["platform"] for m in messages] == ["telegram"]


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

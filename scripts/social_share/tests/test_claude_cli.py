"""Tests for the Claude Code CLI AI provider (social_share)."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai import get_ai_provider
from ai.claude_cli_provider import ClaudeCLIProvider


def _completed(stdout: str, returncode: int = 0, stderr: str = ""):
    return subprocess.CompletedProcess(args=["claude"], returncode=returncode, stdout=stdout, stderr=stderr)


POST = {
    "title": "Rust en DebConf 26",
    "description": "Charla de Oxidar",
    "tags": ["rust"],
    "url": "https://oxidar.org/post/",
    "body": "Contenido del post.",
}

CONFIG = {
    "ai": {"system_prompt": "Eres el community manager de Oxidar.", "claude_cli": {"model": "sonnet"}},
    "platforms": {"twitter": {"max_chars": 280, "prompt_addendum": "Formato Twitter"}},
}


@pytest.fixture
def authed(monkeypatch):
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "test-token")
    monkeypatch.setattr("ai.claude_cli_provider.shutil.which", lambda _: "/usr/bin/claude")


class TestGenerate:
    def test_returns_generated_text(self, authed, monkeypatch):
        monkeypatch.setattr(subprocess, "run", lambda *a, **kw: _completed(json.dumps({"result": "¡Nuevo post!"})))
        assert ClaudeCLIProvider.from_env().generate(POST, "twitter", CONFIG) == "¡Nuevo post!"

    def test_uses_system_prompt_and_platform_rules(self, authed, monkeypatch):
        captured = {}

        def fake_run(cmd, **kwargs):
            captured["cmd"] = cmd
            captured["input"] = kwargs.get("input")
            return _completed(json.dumps({"result": "ok"}))

        monkeypatch.setattr(subprocess, "run", fake_run)
        ClaudeCLIProvider.from_env().generate(POST, "twitter", CONFIG)

        assert "Eres el community manager de Oxidar." in captured["cmd"]
        assert captured["cmd"][captured["cmd"].index("--model") + 1] == "sonnet"
        # Platform rules and post data ride in the user prompt.
        assert "Formato Twitter" in captured["input"]
        assert "Rust en DebConf 26" in captured["input"]
        # The budget shown is max_chars minus the reserved URL, not max_chars.
        assert str(280 - len(POST["url"]) - 2) in captured["input"]

    def test_falls_back_to_default_model(self, authed, monkeypatch):
        captured = {}

        def fake_run(cmd, **kwargs):
            captured["cmd"] = cmd
            return _completed(json.dumps({"result": "ok"}))

        monkeypatch.setattr(subprocess, "run", fake_run)
        ClaudeCLIProvider.from_env().generate(POST, "twitter", {"platforms": {}})
        assert captured["cmd"][captured["cmd"].index("--model") + 1] == "sonnet"

    def test_propagates_cli_failure(self, authed, monkeypatch):
        monkeypatch.setattr(subprocess, "run", lambda *a, **kw: _completed("", returncode=1, stderr="auth expired"))
        with pytest.raises(ValueError, match="auth expired"):
            ClaudeCLIProvider.from_env().generate(POST, "twitter", CONFIG)


class TestFromEnv:
    def test_requires_token_in_ci(self, monkeypatch):
        monkeypatch.setenv("CI", "true")
        monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.setattr("ai.claude_cli_provider.shutil.which", lambda _: "/usr/bin/claude")
        with pytest.raises(ValueError, match="CLAUDE_CODE_OAUTH_TOKEN"):
            ClaudeCLIProvider.from_env()

    def test_registered_in_factory(self, authed, monkeypatch):
        monkeypatch.setenv("AI_PROVIDER", "claude_cli")
        assert isinstance(get_ai_provider(), ClaudeCLIProvider)

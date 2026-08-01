"""Tests for the Claude Code CLI AI provider (shared)."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai import get_ai_provider
from ai.claude_cli_provider import ClaudeCLIProvider, run_claude_cli


def _completed(stdout: str, returncode: int = 0, stderr: str = ""):
    return subprocess.CompletedProcess(args=["claude"], returncode=returncode, stdout=stdout, stderr=stderr)


@pytest.fixture
def authed(monkeypatch):
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "test-token")
    monkeypatch.setattr("ai.claude_cli_provider.shutil.which", lambda _: "/usr/bin/claude")


class TestRunClaudeCli:
    def test_returns_result_text(self, monkeypatch):
        monkeypatch.setattr(
            subprocess, "run", lambda *a, **kw: _completed(json.dumps({"result": "  hola  ", "is_error": False}))
        )
        assert run_claude_cli("sys", "user", "sonnet") == "hola"

    def test_passes_prompts_and_disables_tools(self, monkeypatch):
        captured = {}

        def fake_run(cmd, **kwargs):
            captured["cmd"] = cmd
            captured["input"] = kwargs.get("input")
            return _completed(json.dumps({"result": "ok"}))

        monkeypatch.setattr(subprocess, "run", fake_run)
        run_claude_cli("SYSTEM", "USER", "sonnet")

        assert captured["input"] == "USER"
        assert "SYSTEM" in captured["cmd"]
        assert "--print" in captured["cmd"]
        # Tools must be off: this is a completion, not an agent session.
        assert captured["cmd"][captured["cmd"].index("--allowed-tools") + 1] == ""
        assert "--strict-mcp-config" in captured["cmd"]

    def test_raises_on_nonzero_exit(self, monkeypatch):
        monkeypatch.setattr(subprocess, "run", lambda *a, **kw: _completed("", returncode=1, stderr="boom"))
        with pytest.raises(ValueError, match="boom"):
            run_claude_cli("sys", "user", "sonnet")

    def test_raises_on_non_json_output(self, monkeypatch):
        monkeypatch.setattr(subprocess, "run", lambda *a, **kw: _completed("not json"))
        with pytest.raises(ValueError, match="non-JSON"):
            run_claude_cli("sys", "user", "sonnet")

    def test_raises_when_cli_reports_error(self, monkeypatch):
        monkeypatch.setattr(
            subprocess, "run", lambda *a, **kw: _completed(json.dumps({"is_error": True, "result": "rate limited"}))
        )
        with pytest.raises(ValueError, match="rate limited"):
            run_claude_cli("sys", "user", "sonnet")

    def test_raises_on_empty_result(self, monkeypatch):
        monkeypatch.setattr(subprocess, "run", lambda *a, **kw: _completed(json.dumps({"result": "   "})))
        with pytest.raises(ValueError, match="Empty response"):
            run_claude_cli("sys", "user", "sonnet")


class TestFromEnv:
    def test_requires_cli_on_path(self, monkeypatch):
        monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "test-token")
        monkeypatch.setattr("ai.claude_cli_provider.shutil.which", lambda _: None)
        with pytest.raises(ValueError, match="claude CLI not found"):
            ClaudeCLIProvider.from_env()

    def test_requires_token_in_ci(self, monkeypatch):
        monkeypatch.setenv("CI", "true")
        monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.setattr("ai.claude_cli_provider.shutil.which", lambda _: "/usr/bin/claude")
        with pytest.raises(ValueError, match="CLAUDE_CODE_OAUTH_TOKEN"):
            ClaudeCLIProvider.from_env()

    def test_allows_missing_token_outside_ci(self, monkeypatch):
        # Local runs rely on the CLI's own stored credentials.
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.setattr("ai.claude_cli_provider.shutil.which", lambda _: "/usr/bin/claude")
        assert isinstance(ClaudeCLIProvider.from_env(), ClaudeCLIProvider)

    def test_succeeds_when_authed(self, authed):
        assert isinstance(ClaudeCLIProvider.from_env(), ClaudeCLIProvider)

    def test_registered_in_factory(self, authed, monkeypatch):
        monkeypatch.setenv("AI_PROVIDER", "claude_cli")
        assert isinstance(get_ai_provider(), ClaudeCLIProvider)


class TestComplete:
    def test_complete_returns_text(self, authed, monkeypatch):
        monkeypatch.setattr(subprocess, "run", lambda *a, **kw: _completed(json.dumps({"result": "texto"})))
        assert ClaudeCLIProvider.from_env().complete("sys", "user") == "texto"

    def test_model_overridable_by_env(self, authed, monkeypatch):
        captured = {}

        def fake_run(cmd, **kwargs):
            captured["cmd"] = cmd
            return _completed(json.dumps({"result": "ok"}))

        monkeypatch.setattr(subprocess, "run", fake_run)
        monkeypatch.setenv("CLAUDE_CLI_MODEL", "opus")
        ClaudeCLIProvider.from_env().complete("sys", "user")
        assert captured["cmd"][captured["cmd"].index("--model") + 1] == "opus"

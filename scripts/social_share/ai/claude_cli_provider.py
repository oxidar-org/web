"""Claude Code CLI provider — uses a Claude subscription instead of an API key.

Authenticates via CLAUDE_CODE_OAUTH_TOKEN (generate one with `claude setup-token`),
so no ANTHROPIC_API_KEY is needed. The CLI is invoked in headless print mode with
tools disabled: this is a plain text-in/text-out completion, not an agent session.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess

from .base import AIProvider, build_user_prompt

DEFAULT_MODEL = "sonnet"
DEFAULT_TIMEOUT = 180


def run_claude_cli(
    system_prompt: str,
    user_prompt: str,
    model: str,
    binary: str = "claude",
    timeout: int = DEFAULT_TIMEOUT,
) -> str:
    """Invoke `claude -p` and return the assistant's text response."""
    cmd = [
        binary,
        "--print",
        "--output-format", "json",
        "--model", model,
        "--system-prompt", system_prompt,
        # Pure completion: no tools, no MCP servers, no session persistence.
        "--allowed-tools", "",
        "--strict-mcp-config",
    ]
    proc = subprocess.run(
        cmd,
        input=user_prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise ValueError(f"claude CLI failed (exit {proc.returncode}): {proc.stderr.strip()}")

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise ValueError(f"claude CLI returned non-JSON output: {proc.stdout[:200]}") from e

    if payload.get("is_error"):
        raise ValueError(f"claude CLI reported an error: {payload.get('result', '')}")

    text = (payload.get("result") or "").strip()
    if not text:
        raise ValueError("Empty response from claude CLI")
    return text


class ClaudeCLIProvider(AIProvider):
    """Generate social media text by shelling out to the Claude Code CLI."""

    def __init__(self, binary: str = "claude"):
        self._binary = binary

    @classmethod
    def from_env(cls) -> ClaudeCLIProvider:
        binary = os.environ.get("CLAUDE_CLI_BINARY", "claude")
        if not shutil.which(binary):
            raise ValueError(
                f"claude CLI not found on PATH (looked for '{binary}'). "
                "Install it with: npm install -g @anthropic-ai/claude-code"
            )
        # In CI there is no interactive login to fall back on, so demand a token
        # up front rather than failing once per platform. Locally, defer to
        # whatever credentials the CLI already has (keychain, `claude auth`).
        has_token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")
        if os.environ.get("CI") and not has_token:
            raise ValueError(
                "CLAUDE_CODE_OAUTH_TOKEN environment variable is required in CI "
                "(generate one with `claude setup-token`)"
            )
        return cls(binary=binary)

    def generate(self, post: dict, platform_name: str, config: dict) -> str:
        ai_config = config.get("ai", {}).get("claude_cli", {})
        model = ai_config.get("model", DEFAULT_MODEL)
        system_prompt = config.get("ai", {}).get("system_prompt", "")
        user_prompt = build_user_prompt(post, platform_name, config)
        return run_claude_cli(system_prompt, user_prompt, model, binary=self._binary)

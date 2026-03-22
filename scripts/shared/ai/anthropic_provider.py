"""Anthropic (Claude) AI provider implementation."""

from __future__ import annotations

import os

import anthropic

from .base import AIProvider, DEFAULT_MAX_TOKENS

DEFAULT_MODEL = "claude-sonnet-4-5-20250929"


class AnthropicProvider(AIProvider):
    """Generate text using Claude."""

    def __init__(self, client: anthropic.Anthropic):
        self._client = client

    @classmethod
    def from_env(cls) -> AnthropicProvider:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        return cls(client=anthropic.Anthropic(api_key=api_key))

    def complete(self, system_prompt: str, user_prompt: str, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
        model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
        message = self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        if not message.content:
            raise ValueError("Empty response from Anthropic API")
        return message.content[0].text.strip()

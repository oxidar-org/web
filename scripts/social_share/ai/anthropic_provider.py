"""Anthropic (Claude) AI provider implementation."""

import os

import anthropic

from .base import AIProvider, DEFAULT_MAX_TOKENS


class AnthropicProvider(AIProvider):
    """Generate social media text using Claude."""

    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, post: dict, platform_name: str, config: dict) -> str:
        ai_config = config.get("ai", {}).get("anthropic", {})
        model = ai_config.get("model", "claude-sonnet-4-5-20250929")
        system_prompt = config.get("ai", {}).get("system_prompt", "")
        user_prompt = self._build_user_prompt(post, platform_name, config)

        message = self.client.messages.create(
            model=model,
            max_tokens=DEFAULT_MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return message.content[0].text.strip()

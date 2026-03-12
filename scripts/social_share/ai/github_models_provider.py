"""GitHub Models AI provider implementation (OpenAI-compatible)."""

from __future__ import annotations

import os

import openai

from .base import AIProvider, DEFAULT_MAX_TOKENS, build_user_prompt

GITHUB_MODELS_BASE_URL = "https://models.github.ai/inference"
DEFAULT_MODEL = "openai/gpt-4.1-mini"


class GitHubModelsProvider(AIProvider):
    """Generate social media text using GitHub Models (OpenAI-compatible API)."""

    def __init__(self, client: openai.OpenAI):
        self._client = client

    @classmethod
    def from_env(cls) -> GitHubModelsProvider:
        api_key = os.environ.get("GITHUB_TOKEN")
        if not api_key:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        return cls(client=openai.OpenAI(base_url=GITHUB_MODELS_BASE_URL, api_key=api_key))

    def generate(self, post: dict, platform_name: str, config: dict) -> str:
        ai_config = config.get("ai", {}).get("github_models", {})
        model = ai_config.get("model", DEFAULT_MODEL)
        system_prompt = config.get("ai", {}).get("system_prompt", "")
        user_prompt = build_user_prompt(post, platform_name, config)

        response = self._client.chat.completions.create(
            model=model,
            max_tokens=DEFAULT_MAX_TOKENS,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        if not response.choices:
            raise ValueError("Empty response from GitHub Models API")
        return response.choices[0].message.content.strip()

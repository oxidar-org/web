"""OpenAI AI provider implementation."""

from __future__ import annotations

import os

import openai

from .base import AIProvider, DEFAULT_MAX_TOKENS

DEFAULT_MODEL = "gpt-4o"


class OpenAIProvider(AIProvider):
    """Generate text using OpenAI."""

    def __init__(self, client: openai.OpenAI):
        self._client = client

    @classmethod
    def from_env(cls) -> OpenAIProvider:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return cls(client=openai.OpenAI(api_key=api_key))

    def complete(self, system_prompt: str, user_prompt: str, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
        model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
        response = self._client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        if not response.choices:
            raise ValueError("Empty response from OpenAI API")
        return response.choices[0].message.content.strip()

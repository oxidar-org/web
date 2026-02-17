"""OpenAI AI provider implementation."""

import os

import openai

from .base import AIProvider


class OpenAIProvider(AIProvider):
    """Generate social media text using OpenAI."""

    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = openai.OpenAI(api_key=api_key)

    def generate(self, post: dict, platform_name: str, config: dict) -> str:
        ai_config = config.get("ai", {}).get("openai", {})
        model = ai_config.get("model", "gpt-4o")
        system_prompt = config.get("ai", {}).get("system_prompt", "")
        user_prompt = self._build_user_prompt(post, platform_name, config)

        response = self.client.chat.completions.create(
            model=model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content.strip()

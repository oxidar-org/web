"""Abstract AI provider interface and factory."""

import os
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract base class for AI text generation providers."""

    @abstractmethod
    def generate(self, post: dict, platform_name: str, config: dict) -> str:
        """Generate social media text for a post on a given platform.

        Args:
            post: Dict with title, description, tags, body, url.
            platform_name: Name of the target platform (twitter, linkedin, etc.).
            config: Full config dict from social-media-config.yaml.

        Returns:
            Generated text ready to publish.
        """

    def _build_user_prompt(self, post: dict, platform_name: str, config: dict) -> str:
        """Build the user prompt combining post data and platform rules."""
        platform_config = config.get("platforms", {}).get(platform_name, {})
        max_chars = platform_config.get("max_chars", 280)
        addendum = platform_config.get("prompt_addendum", "")

        return f"""Genera una publicación para {platform_name}.

Datos del artículo:
- Título: {post['title']}
- Descripción: {post['description']}
- Tags: {', '.join(post.get('tags', []))}
- URL: {post['url']}

Extracto del contenido:
{post['body']}

Reglas de la plataforma (máximo {max_chars} caracteres):
{addendum}

Responde SOLO con el texto de la publicación."""


def get_ai_provider() -> AIProvider:
    """Factory: create the appropriate AI provider based on AI_PROVIDER env var."""
    provider_name = os.environ.get("AI_PROVIDER", "anthropic").lower()

    if provider_name == "anthropic":
        from .anthropic_provider import AnthropicProvider
        return AnthropicProvider()
    elif provider_name == "openai":
        from .openai_provider import OpenAIProvider
        return OpenAIProvider()
    else:
        raise ValueError(f"Unknown AI provider: {provider_name}")

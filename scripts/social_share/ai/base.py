"""Abstract AI provider interface and prompt builder."""

from abc import ABC, abstractmethod

DEFAULT_MAX_CHARS = 280
DEFAULT_MAX_TOKENS = 1024

# Registry mapping provider name -> (module, class name)
_AI_REGISTRY: dict[str, tuple[str, str]] = {
    "anthropic": (".anthropic_provider", "AnthropicProvider"),
    "openai": (".openai_provider", "OpenAIProvider"),
}


def build_user_prompt(post: dict, platform_name: str, config: dict) -> str:
    """Build the user prompt combining post data and platform rules."""
    platform_config = config.get("platforms", {}).get(platform_name, {})
    max_chars = platform_config.get("max_chars", DEFAULT_MAX_CHARS)
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


class AIProvider(ABC):
    """Abstract base class for AI text generation providers."""

    @abstractmethod
    def generate(self, post: dict, platform_name: str, config: dict) -> str:
        """Generate social media text for a post on a given platform."""

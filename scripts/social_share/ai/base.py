"""Abstract AI provider interface and prompt builder."""

from abc import ABC, abstractmethod

DEFAULT_MAX_CHARS = 280
DEFAULT_MAX_TOKENS = 1024

# Registry mapping provider name -> (module, class name)
_AI_REGISTRY: dict[str, tuple[str, str]] = {
    "anthropic": (".anthropic_provider", "AnthropicProvider"),
    "openai": (".openai_provider", "OpenAIProvider"),
    "github_models": (".github_models_provider", "GitHubModelsProvider"),
    "claude_cli": (".claude_cli_provider", "ClaudeCLIProvider"),
}


URL_SEPARATOR = "\n\n"
MIN_TEXT_BUDGET = 50


def url_policy(post: dict, platform_name: str, config: dict) -> tuple[bool, int]:
    """Return (append_url, chars_the_url_will_consume) for a platform.

    The URL is the one component whose length is known exactly before
    generation, so its cost is reserved here rather than left to the model to
    count. `url_cost` overrides the real length where a platform rewrites
    links (Twitter shortens every link to 23 chars via t.co).
    """
    platform_config = config.get("platforms", {}).get(platform_name, {})
    if not platform_config.get("include_url", True):
        return False, 0
    url = post.get("url", "")
    if not url:
        return False, 0
    cost = platform_config.get("url_cost")
    if cost is None:
        cost = len(url)
    return True, cost + len(URL_SEPARATOR)


def text_budget(post: dict, platform_name: str, config: dict) -> int:
    """Characters available for generated prose, once the URL is reserved."""
    platform_config = config.get("platforms", {}).get(platform_name, {})
    max_chars = platform_config.get("max_chars", DEFAULT_MAX_CHARS)
    _, url_cost = url_policy(post, platform_name, config)
    return max(max_chars - url_cost, MIN_TEXT_BUDGET)


def effective_length(text: str, post: dict, platform_name: str, config: dict) -> int:
    """Length of `text` as the platform itself counts it.

    Twitter rewrites links to a fixed width, so a raw len() overstates the
    real cost. Must use the same cost model as `text_budget`, or messages get
    dropped for exceeding a limit they actually fit.
    """
    platform_config = config.get("platforms", {}).get(platform_name, {})
    override = platform_config.get("url_cost")
    url = post.get("url", "")
    if override is None or not url or url not in text:
        return len(text)
    return len(text) - len(url) + override


def append_url(text: str, post: dict, platform_name: str, config: dict) -> str:
    """Append the article URL, unless the platform opts out or it is already there."""
    should_append, _ = url_policy(post, platform_name, config)
    url = post.get("url", "")
    if not should_append or url in text:
        return text
    return f"{text.rstrip()}{URL_SEPARATOR}{url}"


def build_length_feedback(previous_length: int, budget: int) -> str:
    """Correction block telling the model exactly how far over it went.

    A concrete measurement lands better than restating the abstract budget,
    which the model already failed to hit once.
    """
    excess = previous_length - budget
    return (
        f"CORRECCIÓN: tu respuesta anterior tenía {previous_length} caracteres, "
        f"{excess} más que el límite de {budget}.\n"
        f"Escribí una versión más corta que quepa en {budget} caracteres. "
        f"Sacá hashtags, adjetivos o una oración entera si hace falta."
    )


def build_user_prompt(post: dict, platform_name: str, config: dict, feedback: str = "") -> str:
    """Build the user prompt combining post data and platform rules."""
    platform_config = config.get("platforms", {}).get(platform_name, {})
    addendum = platform_config.get("prompt_addendum", "")
    budget = text_budget(post, platform_name, config)
    should_append, _ = url_policy(post, platform_name, config)

    if should_append:
        url_rule = (
            "El enlace al artículo se agrega automáticamente al final del texto. "
            "NO incluyas ninguna URL en tu respuesta."
        )
    else:
        url_rule = "NO incluyas ninguna URL en tu respuesta."

    return f"""Genera una publicación para {platform_name}.

Datos del artículo:
- Título: {post['title']}
- Descripción: {post['description']}
- Tags: {', '.join(post.get('tags', []))}

Extracto del contenido:
{post['body']}

Reglas de la plataforma:
{addendum}

{url_rule}

LÍMITE ESTRICTO: tu respuesta debe tener {budget} caracteres o menos.
Antes de responder, contá los caracteres y acortá el texto si te pasaste.
Es preferible un mensaje más corto que uno que exceda el límite.
{feedback}

Responde SOLO con el texto de la publicación."""


class AIProvider(ABC):
    """Abstract base class for AI text generation providers."""

    @abstractmethod
    def generate(self, post: dict, platform_name: str, config: dict, feedback: str = "") -> str:
        """Generate social media text for a post on a given platform."""

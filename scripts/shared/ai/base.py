"""Abstract AI provider interface."""

from abc import ABC, abstractmethod

DEFAULT_MAX_TOKENS = 4096

# Registry mapping provider name -> (module, class name)
_AI_REGISTRY: dict[str, tuple[str, str]] = {
    "anthropic": (".anthropic_provider", "AnthropicProvider"),
    "openai": (".openai_provider", "OpenAIProvider"),
    "github_models": (".github_models_provider", "GitHubModelsProvider"),
}


class AIProvider(ABC):
    """Abstract base class for AI text generation providers."""

    @abstractmethod
    def complete(self, system_prompt: str, user_prompt: str, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
        """Send a completion request and return the response text."""

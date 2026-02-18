"""AI provider registry and factory."""

from __future__ import annotations

import importlib
import os

from .base import AIProvider, _AI_REGISTRY

__all__ = ["get_ai_provider", "AIProvider"]


def get_ai_provider() -> AIProvider:
    """Factory: create the appropriate AI provider based on AI_PROVIDER env var."""
    provider_name = os.environ.get("AI_PROVIDER", "anthropic").lower()
    if provider_name not in _AI_REGISTRY:
        raise ValueError(f"Unknown AI provider: {provider_name}")
    module_path, class_name = _AI_REGISTRY[provider_name]
    mod = importlib.import_module(module_path, package=__package__)
    cls = getattr(mod, class_name)
    return cls.from_env()

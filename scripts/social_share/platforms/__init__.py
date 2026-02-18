"""Platform registry and factory."""

from __future__ import annotations

import importlib
import os

from .base import Platform, PublishResult

# Registry mapping env-var prefix -> (module, class name)
_PLATFORM_REGISTRY: dict[str, tuple[str, str]] = {
    "TWITTER": (".twitter", "TwitterPlatform"),
    "LINKEDIN": (".linkedin", "LinkedInPlatform"),
    "BLUESKY": (".bluesky", "BlueskyPlatform"),
    "TELEGRAM": (".telegram", "TelegramPlatform"),
}

ALL_PLATFORM_NAMES: list[str] = [key.lower() for key in _PLATFORM_REGISTRY]

__all__ = ["get_enabled_platforms", "ALL_PLATFORM_NAMES", "Platform", "PublishResult"]


def get_enabled_platforms() -> list[Platform]:
    """Return platform instances that are enabled via *_ENABLED env vars."""
    platforms = []
    for env_key, (module_path, class_name) in _PLATFORM_REGISTRY.items():
        if os.environ.get(f"{env_key}_ENABLED", "false").lower() == "true":
            mod = importlib.import_module(module_path, package=__package__)
            cls = getattr(mod, class_name)
            platforms.append(cls.from_env())
    return platforms

"""Abstract platform interface and factory."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PublishResult:
    """Standardized result from publishing to a platform."""
    success: bool
    url: str = ""
    error: str = ""


class Platform(ABC):
    """Abstract base class for social media platforms."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Platform name identifier."""

    @abstractmethod
    def publish(self, text: str, post: dict) -> PublishResult:
        """Publish text to this platform.

        Args:
            text: The generated social media text.
            post: The original post dict for additional context.

        Returns:
            PublishResult with success status, url or error.
        """


# Registry mapping env var prefix -> (module, class name)
_PLATFORM_REGISTRY: dict[str, tuple[str, str]] = {
    "TWITTER": (".twitter", "TwitterPlatform"),
    "LINKEDIN": (".linkedin", "LinkedInPlatform"),
    "BLUESKY": (".bluesky", "BlueskyPlatform"),
    "TELEGRAM": (".telegram", "TelegramPlatform"),
}


def get_enabled_platforms() -> list[Platform]:
    """Return list of platform instances that are enabled via env vars."""
    import importlib

    platforms = []
    for env_key, (module_path, class_name) in _PLATFORM_REGISTRY.items():
        if os.environ.get(f"{env_key}_ENABLED", "false").lower() == "true":
            mod = importlib.import_module(module_path, package=__package__)
            cls = getattr(mod, class_name)
            platforms.append(cls())
    return platforms

"""Abstract platform interface and factory."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod


class Platform(ABC):
    """Abstract base class for social media platforms."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Platform name identifier."""

    @abstractmethod
    def publish(self, text: str, post: dict) -> dict:
        """Publish text to this platform.

        Args:
            text: The generated social media text.
            post: The original post dict for additional context.

        Returns:
            Dict with 'success' bool and optional 'url' or 'error'.
        """


def get_enabled_platforms() -> list[Platform]:
    """Return list of platform instances that are enabled via env vars."""
    platforms = []

    if os.environ.get("TWITTER_ENABLED", "false").lower() == "true":
        from .twitter import TwitterPlatform
        platforms.append(TwitterPlatform())

    if os.environ.get("LINKEDIN_ENABLED", "false").lower() == "true":
        from .linkedin import LinkedInPlatform
        platforms.append(LinkedInPlatform())

    if os.environ.get("BLUESKY_ENABLED", "false").lower() == "true":
        from .bluesky import BlueskyPlatform
        platforms.append(BlueskyPlatform())

    if os.environ.get("TELEGRAM_ENABLED", "false").lower() == "true":
        from .telegram import TelegramPlatform
        platforms.append(TelegramPlatform())

    return platforms

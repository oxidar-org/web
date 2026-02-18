"""Abstract platform interface and shared utilities."""

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


def require_env(*names: str) -> dict[str, str]:
    """Read env vars and raise ValueError if any are missing or empty."""
    values = {name: os.environ.get(name, "") for name in names}
    missing = [name for name, val in values.items() if not val]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    return values

"""Instagram platform — snippet generation only (manual posting required)."""

from __future__ import annotations

from .base import Platform, PublishResult


class InstagramPlatform(Platform):
    @classmethod
    def from_env(cls) -> InstagramPlatform:
        return cls()

    @property
    def name(self) -> str:
        return "instagram"

    def publish(self, text: str, post: dict) -> PublishResult:
        return PublishResult(success=False, error="Instagram requires manual posting.")

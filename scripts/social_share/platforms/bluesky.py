"""Bluesky platform implementation using AT Protocol."""

from __future__ import annotations

from atproto import Client

from .base import Platform, PublishResult, require_env


class BlueskyPlatform(Platform):
    def __init__(self, client: Client):
        self._client = client

    @classmethod
    def from_env(cls) -> BlueskyPlatform:
        creds = require_env("BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD")
        client = Client()
        client.login(creds["BLUESKY_HANDLE"], creds["BLUESKY_APP_PASSWORD"])
        return cls(client=client)

    @property
    def name(self) -> str:
        return "bluesky"

    def publish(self, text: str, post: dict) -> PublishResult:
        try:
            response = self._client.send_post(text=text)
            return PublishResult(success=True, url=response.uri)
        except Exception as e:
            return PublishResult(success=False, error=str(e))

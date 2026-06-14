"""Bluesky platform implementation using AT Protocol."""

from __future__ import annotations

import requests as req

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

    _MAX_IMAGE_BYTES = 2_000_000  # Bluesky blob limit

    def publish(self, text: str, post: dict) -> PublishResult:
        try:
            image_url = post.get("image_url")
            if image_url:
                resp = req.get(image_url, timeout=15)
                resp.raise_for_status()
                if len(resp.content) <= self._MAX_IMAGE_BYTES:
                    response = self._client.send_image(text=text, image=resp.content, image_alt="")
                else:
                    response = self._client.send_post(text=text)
            else:
                response = self._client.send_post(text=text)
            return PublishResult(success=True, url=response.uri)
        except Exception as e:
            return PublishResult(success=False, error=str(e))

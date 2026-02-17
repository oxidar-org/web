"""Bluesky platform implementation using AT Protocol."""

import os

from atproto import Client

from .base import Platform


class BlueskyPlatform(Platform):
    def __init__(self):
        self._handle = os.environ.get("BLUESKY_HANDLE")
        self._app_password = os.environ.get("BLUESKY_APP_PASSWORD")
        missing = [
            name for name, val in [
                ("BLUESKY_HANDLE", self._handle),
                ("BLUESKY_APP_PASSWORD", self._app_password),
            ] if not val
        ]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    @property
    def name(self) -> str:
        return "bluesky"

    def publish(self, text: str, post: dict) -> dict:
        try:
            client = Client()
            client.login(self._handle, self._app_password)
            response = client.send_post(text=text)
            return {
                "success": True,
                "url": response.uri,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

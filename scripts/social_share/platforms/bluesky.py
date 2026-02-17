"""Bluesky platform implementation using AT Protocol."""

import os
from datetime import datetime, timezone

from atproto import Client

from .base import Platform


class BlueskyPlatform(Platform):
    @property
    def name(self) -> str:
        return "bluesky"

    def publish(self, text: str, post: dict) -> dict:
        handle = os.environ["BLUESKY_HANDLE"]
        app_password = os.environ["BLUESKY_APP_PASSWORD"]

        try:
            client = Client()
            client.login(handle, app_password)
            response = client.send_post(text=text)
            return {
                "success": True,
                "uri": response.uri,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

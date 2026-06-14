"""Bluesky platform implementation using AT Protocol."""

from __future__ import annotations

from io import BytesIO

import requests as req

from atproto import Client

from .base import Platform, PublishResult, require_env


class BlueskyPlatform(Platform):
    _MAX_IMAGE_BYTES = 2_000_000  # Bluesky blob limit

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

    def _compress_image(self, data: bytes) -> bytes:
        from PIL import Image
        img = Image.open(BytesIO(data))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        for quality in (85, 70, 55, 40):
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=quality)
            if len(buf.getvalue()) <= self._MAX_IMAGE_BYTES:
                return buf.getvalue()
        # Still too large — scale down dimensions
        while True:
            w, h = img.size
            img = img.resize((int(w * 0.75), int(h * 0.75)), Image.LANCZOS)
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=40)
            if len(buf.getvalue()) <= self._MAX_IMAGE_BYTES:
                return buf.getvalue()

    def publish(self, text: str, post: dict) -> PublishResult:
        try:
            image_url = post.get("image_url")
            if image_url:
                resp = req.get(image_url, timeout=15)
                resp.raise_for_status()
                image_data = resp.content
                if len(image_data) > self._MAX_IMAGE_BYTES:
                    image_data = self._compress_image(image_data)
                response = self._client.send_image(text=text, image=image_data, image_alt="")
            else:
                response = self._client.send_post(text=text)
            return PublishResult(success=True, url=response.uri)
        except Exception as e:
            return PublishResult(success=False, error=str(e))

"""Telegram platform implementation using Bot API."""

from __future__ import annotations

import requests

from .base import Platform, PublishResult, require_env


class TelegramPlatform(Platform):
    def __init__(self, bot_token: str, chat_id: str, session: requests.Session | None = None):
        self._bot_token = bot_token
        self._chat_id = chat_id
        self._session = session or requests.Session()

    @classmethod
    def from_env(cls) -> TelegramPlatform:
        creds = require_env("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID")
        return cls(bot_token=creds["TELEGRAM_BOT_TOKEN"], chat_id=creds["TELEGRAM_CHAT_ID"])

    @property
    def name(self) -> str:
        return "telegram"

    def publish(self, text: str, post: dict) -> PublishResult:
        image_url = post.get("image_url")
        if image_url:
            return self._send_photo(image_url, text)
        return self._send_message(text)

    _CAPTION_LIMIT = 1024

    def _send_photo(self, image_url: str, caption: str) -> PublishResult:
        url = f"https://api.telegram.org/bot{self._bot_token}/sendPhoto"
        # If caption fits, send as one message; otherwise send photo then text separately
        if len(caption) <= self._CAPTION_LIMIT:
            payload = {"chat_id": self._chat_id, "photo": image_url, "caption": caption, "parse_mode": "Markdown"}
            try:
                resp = self._session.post(url, json=payload, timeout=30)
                data = resp.json()
            except (requests.RequestException, ValueError) as e:
                return PublishResult(success=False, error=str(e))
            if data.get("ok"):
                return PublishResult(success=True, url=str(data.get("result", {}).get("message_id", "")))
            return PublishResult(success=False, error=data.get("description", "Unknown Telegram error"))
        else:
            # Send photo without caption, then full text as follow-up
            try:
                resp = self._session.post(url, json={"chat_id": self._chat_id, "photo": image_url}, timeout=30)
                data = resp.json()
                if not data.get("ok"):
                    return PublishResult(success=False, error=data.get("description", "Unknown Telegram error"))
            except (requests.RequestException, ValueError) as e:
                return PublishResult(success=False, error=str(e))
            return self._send_message(caption)

    def _send_message(self, text: str) -> PublishResult:
        url = f"https://api.telegram.org/bot{self._bot_token}/sendMessage"
        payload = {
            "chat_id": self._chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False,
        }
        try:
            resp = self._session.post(url, json=payload, timeout=30)
            data = resp.json()
        except (requests.RequestException, ValueError) as e:
            return PublishResult(success=False, error=str(e))

        if data.get("ok"):
            msg_id = data.get("result", {}).get("message_id", "")
            return PublishResult(success=True, url=str(msg_id))
        return PublishResult(success=False, error=data.get("description", "Unknown Telegram error"))

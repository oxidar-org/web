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
        else:
            return PublishResult(
                success=False,
                error=data.get("description", "Unknown Telegram error"),
            )

"""Telegram platform implementation using Bot API."""

import os

import requests

from .base import Platform


class TelegramPlatform(Platform):
    def __init__(self):
        self._bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self._chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        missing = [
            name for name, val in [
                ("TELEGRAM_BOT_TOKEN", self._bot_token),
                ("TELEGRAM_CHAT_ID", self._chat_id),
            ] if not val
        ]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    @property
    def name(self) -> str:
        return "telegram"

    def publish(self, text: str, post: dict) -> dict:
        url = f"https://api.telegram.org/bot{self._bot_token}/sendMessage"
        payload = {
            "chat_id": self._chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False,
        }

        try:
            resp = requests.post(url, json=payload, timeout=30)
            data = resp.json()
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}

        if data.get("ok"):
            msg_id = data["result"]["message_id"]
            return {"success": True, "url": str(msg_id)}
        else:
            return {
                "success": False,
                "error": data.get("description", "Unknown Telegram error"),
            }

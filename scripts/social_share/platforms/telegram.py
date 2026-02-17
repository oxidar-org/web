"""Telegram platform implementation using Bot API."""

import os

import requests

from .base import Platform


class TelegramPlatform(Platform):
    @property
    def name(self) -> str:
        return "telegram"

    def publish(self, text: str, post: dict) -> dict:
        bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHAT_ID"]

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False,
        }

        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        if data.get("ok"):
            msg_id = data["result"]["message_id"]
            return {"success": True, "message_id": msg_id}
        else:
            return {
                "success": False,
                "error": data.get("description", "Unknown Telegram error"),
            }

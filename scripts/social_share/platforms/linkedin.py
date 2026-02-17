"""LinkedIn platform implementation using REST API v2."""

import os

import requests

from .base import Platform, PublishResult


class LinkedInPlatform(Platform):
    def __init__(self):
        self._access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
        self._org_id = os.environ.get("LINKEDIN_ORG_ID")
        missing = [
            name for name, val in [
                ("LINKEDIN_ACCESS_TOKEN", self._access_token),
                ("LINKEDIN_ORG_ID", self._org_id),
            ] if not val
        ]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    @property
    def name(self) -> str:
        return "linkedin"

    def publish(self, text: str, post: dict) -> PublishResult:
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }
        payload = {
            "author": f"urn:li:organization:{self._org_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "originalUrl": post["url"],
                            "title": {"text": post["title"]},
                            "description": {"text": post.get("description", "")},
                        }
                    ],
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
        except requests.RequestException as e:
            return PublishResult(success=False, error=str(e))

        if resp.status_code == 201:
            post_id = resp.json().get("id", "")
            return PublishResult(success=True, url=post_id)
        else:
            return PublishResult(success=False, error=f"HTTP {resp.status_code}: {resp.text}")

"""LinkedIn platform implementation using REST API v2."""

from __future__ import annotations

import requests

from .base import Platform, PublishResult, require_env


class LinkedInPlatform(Platform):
    def __init__(self, access_token: str, org_id: str, session: requests.Session | None = None):
        self._access_token = access_token
        self._org_id = org_id
        self._session = session or requests.Session()

    @classmethod
    def from_env(cls) -> LinkedInPlatform:
        creds = require_env("LINKEDIN_ACCESS_TOKEN", "LINKEDIN_ORG_ID")
        return cls(access_token=creds["LINKEDIN_ACCESS_TOKEN"], org_id=creds["LINKEDIN_ORG_ID"])

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
            resp = self._session.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 201:
                post_id = resp.json().get("id", "")
                return PublishResult(success=True, url=post_id)
            else:
                return PublishResult(success=False, error=f"HTTP {resp.status_code}: {resp.text}")
        except (requests.RequestException, ValueError) as e:
            return PublishResult(success=False, error=str(e))

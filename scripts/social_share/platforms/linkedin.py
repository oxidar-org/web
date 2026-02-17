"""LinkedIn platform implementation using REST API v2."""

import os

import requests

from .base import Platform


class LinkedInPlatform(Platform):
    @property
    def name(self) -> str:
        return "linkedin"

    def publish(self, text: str, post: dict) -> dict:
        access_token = os.environ["LINKEDIN_ACCESS_TOKEN"]
        org_id = os.environ["LINKEDIN_ORG_ID"]

        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }
        payload = {
            "author": f"urn:li:organization:{org_id}",
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

        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 201:
            post_id = resp.json().get("id", "")
            return {"success": True, "id": post_id}
        else:
            return {
                "success": False,
                "error": f"HTTP {resp.status_code}: {resp.text}",
            }

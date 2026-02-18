"""Twitter/X platform implementation using tweepy."""

from __future__ import annotations

import tweepy

from .base import Platform, PublishResult, require_env


class TwitterPlatform(Platform):
    def __init__(self, client: tweepy.Client):
        self._client = client

    @classmethod
    def from_env(cls) -> TwitterPlatform:
        creds = require_env(
            "TWITTER_API_KEY", "TWITTER_API_SECRET",
            "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET",
        )
        client = tweepy.Client(
            consumer_key=creds["TWITTER_API_KEY"],
            consumer_secret=creds["TWITTER_API_SECRET"],
            access_token=creds["TWITTER_ACCESS_TOKEN"],
            access_token_secret=creds["TWITTER_ACCESS_SECRET"],
        )
        return cls(client=client)

    @property
    def name(self) -> str:
        return "twitter"

    def publish(self, text: str, post: dict) -> PublishResult:
        try:
            response = self._client.create_tweet(text=text)
            tweet_id = response.data["id"]
            return PublishResult(success=True, url=f"https://x.com/i/status/{tweet_id}")
        except (tweepy.TweepyException, KeyError) as e:
            return PublishResult(success=False, error=str(e))

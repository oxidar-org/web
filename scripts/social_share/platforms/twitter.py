"""Twitter/X platform implementation using tweepy."""

import os

import tweepy

from .base import Platform, PublishResult


class TwitterPlatform(Platform):
    def __init__(self):
        self._api_key = os.environ.get("TWITTER_API_KEY")
        self._api_secret = os.environ.get("TWITTER_API_SECRET")
        self._access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        self._access_secret = os.environ.get("TWITTER_ACCESS_SECRET")
        missing = [
            name for name, val in [
                ("TWITTER_API_KEY", self._api_key),
                ("TWITTER_API_SECRET", self._api_secret),
                ("TWITTER_ACCESS_TOKEN", self._access_token),
                ("TWITTER_ACCESS_SECRET", self._access_secret),
            ] if not val
        ]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    @property
    def name(self) -> str:
        return "twitter"

    def publish(self, text: str, post: dict) -> PublishResult:
        try:
            client = tweepy.Client(
                consumer_key=self._api_key,
                consumer_secret=self._api_secret,
                access_token=self._access_token,
                access_token_secret=self._access_secret,
            )
            response = client.create_tweet(text=text)
            tweet_id = response.data["id"]
            return PublishResult(success=True, url=f"https://x.com/i/status/{tweet_id}")
        except (tweepy.TweepyException, KeyError) as e:
            return PublishResult(success=False, error=str(e))

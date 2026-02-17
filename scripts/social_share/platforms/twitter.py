"""Twitter/X platform implementation using tweepy."""

import os

import tweepy

from .base import Platform


class TwitterPlatform(Platform):
    @property
    def name(self) -> str:
        return "twitter"

    def publish(self, text: str, post: dict) -> dict:
        try:
            client = tweepy.Client(
                consumer_key=os.environ["TWITTER_API_KEY"],
                consumer_secret=os.environ["TWITTER_API_SECRET"],
                access_token=os.environ["TWITTER_ACCESS_TOKEN"],
                access_token_secret=os.environ["TWITTER_ACCESS_SECRET"],
            )
            response = client.create_tweet(text=text)
            tweet_id = response.data["id"]
            return {
                "success": True,
                "url": f"https://x.com/i/status/{tweet_id}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

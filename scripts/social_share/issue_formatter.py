"""Format and parse GitHub issues for social media message review."""

from __future__ import annotations

import re

PLATFORM_EMOJIS: dict[str, str] = {
    "twitter": "🐦",
    "linkedin": "💼",
    "bluesky": "🦋",
    "telegram": "📢",
}

_EMOJI_TO_PLATFORM: dict[str, str] = {v: k for k, v in PLATFORM_EMOJIS.items()}

ISSUE_TITLE_PREFIX = "[Social]"
APPROVED_LABEL = "social: approved"
PUBLISHED_LABEL = "social: published"
PENDING_LABEL = "social: pending"


def format_issue_body(post: dict, messages: list[dict]) -> str:
    """Format messages for a single post into a GitHub issue body."""
    lines = [
        f"## {post['title']}",
        f"🔗 {post['url']}",
        "",
        "---",
        "",
    ]
    for msg in messages:
        platform = msg["platform"]
        emoji = PLATFORM_EMOJIS.get(platform, "")
        lines += [
            f"### {emoji} {platform.capitalize()}",
            "```",
            msg["text"],
            "```",
            "",
        ]
    lines += [
        "---",
        "> Edit the text inside each code block, then add the `social: approved` label to publish.",
    ]
    return "\n".join(lines)


def format_issue_title(post_title: str) -> str:
    return f"{ISSUE_TITLE_PREFIX} {post_title}"


def parse_issue_body(body: str) -> tuple[dict, list[dict]]:
    """Parse a GitHub issue body into (post, messages).

    Returns a post dict with title/url and a list of per-platform message dicts.
    """
    url_match = re.search(r"🔗\s+(https?://\S+)", body)
    url = url_match.group(1).strip() if url_match else ""

    title_match = re.search(r"^##\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""

    post = {"title": title, "url": url}
    messages = []

    # Match ### {emoji} {Platform}\n```\n{text}\n```
    for match in re.finditer(r"###\s+([^\n]+)\n```\n(.*?)\n```", body, re.DOTALL):
        header = match.group(1).strip()
        text = match.group(2).strip()

        platform = next(
            (plat for emoji, plat in _EMOJI_TO_PLATFORM.items() if emoji in header),
            None,
        )
        if platform is None:
            platform = next(
                (name for name in PLATFORM_EMOJIS if name.lower() in header.lower()),
                None,
            )

        if platform and text:
            messages.append({"post": post, "platform": platform, "text": text})

    return post, messages

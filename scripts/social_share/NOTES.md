# Social Media Sharing Pipeline

Automated social media posting when new blog posts are published on oxidar.org.

## How It Works

1. A new post is pushed to `main` and the Hugo deploy workflow succeeds
2. The `social-share.yaml` workflow triggers via `workflow_run`
3. New posts are detected using `git diff` (added `.md` files in `content/posts/`)
4. English translations (`*.en.md`), index files, drafts, and `share = false` posts are skipped
5. For each new post × each enabled platform, an AI provider generates platform-specific text in Spanish
6. The text is published to the enabled platforms

## Setup Required

### GitHub Secrets

| Secret | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API key (default AI provider) |
| `OPENAI_API_KEY` | OpenAI API key (alternative provider) |
| `TWITTER_API_KEY` | Twitter/X OAuth 1.0a consumer key |
| `TWITTER_API_SECRET` | Twitter/X OAuth 1.0a consumer secret |
| `TWITTER_ACCESS_TOKEN` | Twitter/X OAuth 1.0a access token |
| `TWITTER_ACCESS_SECRET` | Twitter/X OAuth 1.0a access secret |
| `LINKEDIN_ACCESS_TOKEN` | LinkedIn API access token |
| `LINKEDIN_ORG_ID` | LinkedIn organization ID |
| `BLUESKY_HANDLE` | Bluesky account handle |
| `BLUESKY_APP_PASSWORD` | Bluesky app password |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |
| `TELEGRAM_CHAT_ID` | Telegram channel/group chat ID |

### GitHub Variables (toggles)

| Variable | Default | Purpose |
|---|---|---|
| `AI_PROVIDER` | `anthropic` | AI provider (`anthropic` or `openai`) |
| `TWITTER_ENABLED` | `false` | Enable Twitter/X posting |
| `LINKEDIN_ENABLED` | `false` | Enable LinkedIn posting |
| `BLUESKY_ENABLED` | `false` | Enable Bluesky posting |
| `TELEGRAM_ENABLED` | `false` | Enable Telegram posting |

## Opting Out a Post

Add `share = false` to the post's TOML front matter:

```toml
+++
title = 'My Post'
share = false
+++
```

Posts with `draft = true` or `hiddenFromHomePage = true` are also skipped automatically.

## Local Testing

```bash
pip install -r scripts/social_share/requirements.txt

# Dry-run with a specific post
echo "content/posts/2026.01.26-rustconf-2026-cfp/rustconf-2026-cfp.md" > /tmp/test_posts.txt
export ANTHROPIC_API_KEY="sk-..."
python scripts/social_share/main.py \
  --posts-file /tmp/test_posts.txt \
  --config .github/social-media-config.yaml \
  --dry-run
```

## Recommended First Test

Start with Telegram — it has the simplest setup (bot token + chat ID, no OAuth).

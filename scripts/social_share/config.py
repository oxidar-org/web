"""Load configuration from YAML and environment variables."""

import os
from pathlib import Path

import yaml


def load_config(config_path: str) -> dict:
    """Load social media config from YAML file."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(path) as f:
        return yaml.safe_load(f)


def get_ai_provider_name() -> str:
    """Get the AI provider name from environment."""
    return os.environ.get("AI_PROVIDER", "anthropic")


def get_base_url(config: dict) -> str:
    """Get the site base URL from config."""
    return config.get("community", {}).get("website", "https://oxidar.org")

"""Persistent settings layer.

Reads/writes config.json next to this file. On first run (no config.json),
seeds values from a sibling .env file. Priority: config.json > .env > defaults.
Never writes to .env — it stays a read-only seed.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
ENV_PATH = BASE_DIR / ".env"

DEFAULTS = {
    "jira_url": "",
    "jira_email": "",
    "jira_api_token": "",
    "provider": "ollama",  # "ollama" | "groq"
    "ollama_url": "http://localhost:11434",
    "ollama_model": "gemma3:1b",
    "groq_api_key": "",
    "groq_model": "openai/gpt-oss-20b",
}


def _parse_env() -> dict:
    """Minimal KEY=VALUE parser for .env (comments and blanks ignored)."""
    if not ENV_PATH.exists():
        return {}
    parsed = {}
    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        parsed[key.strip()] = value.strip()
    return parsed


def load_settings() -> dict:
    """Return merged settings: config.json overrides .env overrides defaults."""
    settings = dict(DEFAULTS)

    env_map = _parse_env()
    env_settings = {
        "jira_url": env_map.get("JIRA_URL", "").strip(),
        "jira_email": env_map.get("JIRA_EMAIL", "").strip(),
        "jira_api_token": env_map.get("JIRA_API_TOKEN", "").strip(),
        "groq_api_key": env_map.get("GROQ_API_TOKEN", "").strip(),
    }

    config = {}
    if CONFIG_PATH.exists():
        try:
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            config = {}

    settings.update({k: v for k, v in env_settings.items() if v})
    settings.update({k: v for k, v in config.items() if v not in (None, "")})
    return settings


def save_settings(new: dict) -> dict:
    """Merge new values into existing settings and persist to config.json."""
    current = load_settings()
    current.update({k: v for k, v in new.items() if k in DEFAULTS and v not in (None, "")})
    CONFIG_PATH.write_text(
        json.dumps(current, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return current


def get(key: str) -> str:
    """Convenience accessor for a single setting."""
    return load_settings().get(key, "")


def reset_to_env() -> dict:
    """Drop config.json and re-seed from .env. Used by the Settings screen."""
    if CONFIG_PATH.exists():
        os.remove(CONFIG_PATH)
    return load_settings()

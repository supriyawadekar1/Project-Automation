#!/usr/bin/env python3
"""Groq chat-completions client (requests, no SDK).

Key resolution is done by the caller (ui/app.py). This module only talks to Groq
and maps HTTP/network errors to human-friendly messages. It never logs the key.
"""

from __future__ import annotations

import requests

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
TIMEOUT = 180


class GroqError(Exception):
    """Raised for any Groq failure with a user-friendly message."""


def chat(key: str, model: str, system_prompt: str, user_prompt: str) -> str:
    """Return the assistant text for one non-streamed completion."""
    if not key:
        raise GroqError(
            "Groq API key is missing. Add GROQ_API_TOKEN to .env or paste it in the sidebar."
        )
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 8192,
    }
    try:
        resp = requests.post(GROQ_CHAT_URL, json=payload, headers=headers, timeout=TIMEOUT)
    except requests.Timeout:
        raise GroqError("Groq timed out (180s). Try again — the model may be busy.")
    except requests.RequestException as exc:
        raise GroqError(f"Could not reach Groq: {exc}")

    if resp.status_code in (401, 403):
        raise GroqError("Groq authentication failed. Check the API key.")
    if resp.status_code == 404:
        raise GroqError(
            f"Groq model '{model}' is not available on this key. "
            "Try qwen/qwen3.8-27b or openai/gpt-oss-20b."
        )
    if resp.status_code == 429:
        raise GroqError("Groq rate limit hit (HTTP 429). Wait a moment and try again.")
    if resp.status_code >= 400:
        raise GroqError(f"Groq returned HTTP {resp.status_code}.")
    try:
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        content = (content or "").strip()
        if not content:
            raise GroqError(
                f"Groq model '{model}' returned an empty response. "
                "Try qwen/qwen3.8-27b, or retry."
            )
        return content
    except (ValueError, KeyError, IndexError) as exc:
        raise GroqError(f"Unexpected Groq response shape: {exc}")

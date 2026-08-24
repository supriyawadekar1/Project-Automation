"""LLM backend client: Ollama (local) with automatic Groq fallback.

Provider rules (from the spec):
- Default provider is Ollama (local, gemma3:1b).
- Groq is used ONLY when Ollama is unreachable/fails OR the user
  explicitly selects Groq in Settings.
"""

from __future__ import annotations

import requests

OLLAMA_TAGS_URL = "{base}/api/tags"
OLLAMA_GENERATE_URL = "{base}/api/generate"
GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"

OLLAMA_TIMEOUT = 5
GENERATE_TIMEOUT = 120


class LLMError(Exception):
    """Raised when no LLM backend could produce a response."""


def is_ollama_available(ollama_url: str = "http://localhost:11434") -> bool:
    """True if the local Ollama server responds (model presence not required)."""
    try:
        resp = requests.get(
            OLLAMA_TAGS_URL.format(base=ollama_url.rstrip("/")), timeout=3
        )
        return resp.status_code == 200
    except requests.RequestException:
        return False


def has_ollama_model(ollama_url: str, model: str) -> bool:
    """True if the named model is listed in the local Ollama server."""
    try:
        resp = requests.get(
            OLLAMA_TAGS_URL.format(base=ollama_url.rstrip("/")), timeout=3
        )
        if resp.status_code != 200:
            return False
        return any(m.get("name") == model for m in resp.json().get("models", []))
    except (requests.RequestException, ValueError):
        return False


def build_prompt(ticket: dict, template_text: str, num_cases: int) -> str:
    """Fill the template placeholders with the fetched ticket content."""
    replacements = {
        "[NUMBER]": str(num_cases),
        "[KEY]": ticket.get("key", ""),
        "[SUMMARY]": ticket.get("summary") or "Not specified",
        "[DESCRIPTION]": ticket.get("description") or "Not specified",
        "[ACCEPTANCE_CRITERIA]": ticket.get("acceptance_criteria")
        or "Not specified",
    }
    prompt = template_text
    for placeholder, value in replacements.items():
        prompt = prompt.replace(placeholder, value)
    return prompt


def _call_ollama(prompt: str, ollama_url: str, model: str) -> str:
    payload = {"model": model, "prompt": prompt, "stream": False}
    resp = requests.post(
        OLLAMA_GENERATE_URL.format(base=ollama_url.rstrip("/")),
        json=payload,
        timeout=GENERATE_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json().get("response", "").strip()


def _call_groq(prompt: str, groq_key: str, model: str) -> str:
    if not groq_key:
        raise LLMError("Groq API key is not configured. Add it in Settings.")
    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }
    resp = requests.post(
        GROQ_CHAT_URL, json=payload, headers=headers, timeout=GENERATE_TIMEOUT
    )
    if resp.status_code in (401, 403):
        raise LLMError("Groq authentication failed. Check the API key in Settings.")
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def generate_test_cases(
    ticket: dict,
    template_text: str,
    provider: str,
    groq_key: str = "",
    ollama_url: str = "http://localhost:11434",
    ollama_model: str = "gemma3:1b",
    groq_model: str = "openai/gpt-oss-20b",
    num_cases: int = 10,
) -> tuple[str, str]:
    """Generate test cases; returns (markdown_text, note).

    The note is a short human-readable status line appended to the chat
    message, e.g. '(Ollama unavailable — fell back to Groq)'.
    """
    prompt = build_prompt(ticket, template_text, num_cases)

    if provider == "groq":
        return _call_groq(prompt, groq_key, groq_model), "Provider: Groq"

    # Default path: Ollama, with automatic fallback to Groq.
    try:
        text = _call_ollama(prompt, ollama_url, ollama_model)
        return text, "Provider: Ollama"
    except requests.RequestException:
        pass  # fall through to Groq

    try:
        text = _call_groq(prompt, groq_key, groq_model)
        return text, "Ollama unavailable — fell back to Groq"
    except LLMError:
        raise LLMError(
            "Ollama is unreachable and Groq is not configured. "
            "Start Ollama or add a Groq API key in Settings."
        )

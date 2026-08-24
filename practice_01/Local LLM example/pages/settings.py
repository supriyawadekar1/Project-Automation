"""Screen 2 — Settings: configure and persist Jira/Groq credentials.

Secret fields are masked with a sentinel; typing a new value replaces the
stored one, leaving it blank keeps the existing value.
"""

from __future__ import annotations

import streamlit as st

import config_store
from llm_client import GROQ_CHAT_URL, is_ollama_available
import requests

MASKED = "\u2022\u2022\u2022\u2022 (saved)"


def _masked_default(stored: str) -> str:
    return MASKED if stored else ""


def _unmask(value: str, stored: str) -> str:
    """Return the value to persist: typed input wins, sentinel means 'keep'."""
    if not value or value == MASKED:
        return stored
    return value.strip()


def _test_groq(groq_key: str, model: str) -> str:
    try:
        resp = requests.post(
            GROQ_CHAT_URL,
            headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 5,
            },
            timeout=15,
        )
        return "OK" if resp.status_code == 200 else f"HTTP {resp.status_code}"
    except requests.RequestException as exc:
        return f"unreachable: {exc}"


st.set_page_config(page_title="Settings", page_icon="\u2699\ufe0f")
st.title("Settings")
st.caption("Credentials are stored in `config.json` next to the app, seeded from `.env` on first run. Never committed to version control.")

settings = config_store.load_settings()

with st.form("settings_form"):
    st.subheader("Jira")
    jira_url = st.text_input("Jira base URL", value=settings.get("jira_url", ""), placeholder="https://your-domain.atlassian.net")
    jira_email = st.text_input("Jira email ID", value=settings.get("jira_email", ""))
    jira_token = st.text_input(
        "Jira API token",
        type="password",
        value=_masked_default(settings.get("jira_api_token", "")),
        help="Leave blank to keep the saved token.",
    )

    st.subheader("LLM provider")
    provider = st.radio(
        "Provider",
        options=["ollama", "groq"],
        index=0 if settings.get("provider", "ollama") == "ollama" else 1,
        format_func=lambda p: "Ollama (local)" if p == "ollama" else "Groq (hosted fallback)",
    )
    groq_key = st.text_input(
        "Groq API key",
        type="password",
        value=_masked_default(settings.get("groq_api_key", "")),
        help="Used only when provider is Groq, or when Ollama is unavailable.",
    )

    with st.expander("Advanced (Ollama endpoint / model)"):
        ollama_url = st.text_input("Ollama URL", value=settings.get("ollama_url", "http://localhost:11434"))
        ollama_model = st.text_input("Ollama model", value=settings.get("ollama_model", "gemma3:1b"))

    col1, col2 = st.columns(2)
    submitted = col1.form_submit_button("Save settings", type="primary")
    test_conn = col2.form_submit_button("Test connection")

if submitted:
    config_store.save_settings(
        {
            "jira_url": jira_url.strip(),
            "jira_email": jira_email.strip(),
            "jira_api_token": _unmask(jira_token, settings.get("jira_api_token", "")),
            "provider": provider,
            "groq_api_key": _unmask(groq_key, settings.get("groq_api_key", "")),
            "ollama_url": ollama_url.strip() or "http://localhost:11434",
            "ollama_model": ollama_model.strip() or "gemma3:1b",
        }
    )
    st.success("Settings saved.")

if test_conn:
    st.subheader("Connection checks")
    ollama_ok = is_ollama_available(settings.get("ollama_url", "http://localhost:11434"))
    st.write(f"Ollama (`{settings.get('ollama_url', '')}`): {'**reachable**' if ollama_ok else '**unreachable**'}")
    if not ollama_ok:
        st.caption("Start Ollama locally; the app will fall back to Groq when it is down.")

    if settings.get("groq_api_key"):
        result = _test_groq(settings.get("groq_api_key"), settings.get("groq_model", "openai/gpt-oss-20b"))
        st.write(f"Groq: **{result}**")
    else:
        st.write("Groq: no API key saved yet.")

st.divider()
if st.button("Reset saved settings (re-seed from .env)"):
    config_store.reset_to_env()
    st.success("Reset to .env values.")
    st.rerun()

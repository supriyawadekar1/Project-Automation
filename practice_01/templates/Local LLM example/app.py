"""Screen 1 — Chat: ChatGPT-style interface.

The user types a natural-language request such as 'create test cases for
QA-102'. The app extracts the Jira key, fetches the ticket, fills the test
case template, and renders the LLM-generated test cases back in the chat.
"""

from __future__ import annotations

import re
from pathlib import Path

import streamlit as st

import config_store
import jira_client
import llm_client

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "templates" / "tc_template.md"

ISSUE_KEY_RE = re.compile(r"([A-Z][A-Z0-9_]+-\d+)")

st.set_page_config(page_title="Test Case Generator", layout="wide")
st.title("Test Case Generator")
st.caption("Type e.g. 'create test cases for QA-102' to generate test cases from a Jira ticket.")

settings = config_store.load_settings()


def _provider_status() -> str:
    if settings.get("provider") == "groq":
        return "Groq"
    ollama_ok = llm_client.is_ollama_available(settings.get("ollama_url"))
    return "Ollama (running)" if ollama_ok else "Ollama (unavailable - will fall back to Groq)"


def _render_messages() -> None:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def _generate(user_input: str) -> str:
    """Full pipeline: extract key -> fetch ticket -> template -> LLM."""
    match = ISSUE_KEY_RE.search(user_input)
    if not match:
        return (
            "I couldn't find a Jira issue key in your message. "
            "Try something like **'create test cases for QA-102'**."
        )
    issue_key = match.group(1)

    with st.spinner(f"Fetching {issue_key} from Jira..."):
        ticket = jira_client.fetch_issue(
            settings.get("jira_url"),
            settings.get("jira_email"),
            settings.get("jira_api_token"),
            issue_key,
        )

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    with st.spinner("Generating test cases..."):
        try:
            markdown, note = llm_client.generate_test_cases(
                ticket,
                template_text,
                provider=settings.get("provider", "ollama"),
                groq_key=settings.get("groq_api_key", ""),
                ollama_url=settings.get("ollama_url", "http://localhost:11434"),
                ollama_model=settings.get("ollama_model", "gemma3:1b"),
                groq_model=settings.get("groq_model", "openai/gpt-oss-20b"),
                num_cases=10,
            )
        except llm_client.LLMError as exc:
            return f"Generation failed: {exc}"

    return f"{markdown}\n\n---\n*{note}*"


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I turn Jira tickets into test case drafts. "
                "Type a request like **'create test cases for QA-102'**."
            ),
        }
    ]

with st.sidebar:
    st.subheader("Status")
    st.write(f"Provider: **{_provider_status()}**")
    if not settings.get("jira_api_token"):
        st.warning("Jira credentials not configured yet. Open **Settings** to add them.")
    st.divider()
    st.write("Configure Jira, Groq, and provider under **Settings** in the sidebar.")

_render_messages()

prompt = st.chat_input("Ask for test cases, e.g. 'create test cases for QA-102'...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        reply = _generate(prompt)
    except jira_client.JiraError as exc:
        reply = f"Jira error: {exc}"
    except Exception as exc:  # noqa: BLE001 — surface anything in-pane, don't crash
        reply = f"Unexpected error: {exc}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

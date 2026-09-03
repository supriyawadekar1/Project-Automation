#!/usr/bin/env python3
"""Streamlit UI — Test Plan Creator from a Jira ID.

User enters a Jira key → the app fetches the ticket via the deterministic
Node tool (tools/fetch_issue.js), drafts a test plan with Groq, shows it for
human editing, and can export Markdown + PDF.

Run (with the bundled interpreter that has streamlit):
  <python> -m streamlit run ui/app.py
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import streamlit as st

import export as export_mod
import groq_client
import prompt_builder

# ---------- paths ----------
CHAPTER_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = CHAPTER_DIR / "tools"
TMP_DIR = CHAPTER_DIR / ".tmp"
RULES_PATH = Path(__file__).resolve().parent / "prompt_template.md"
CHECKLIST_PATH = (
    CHAPTER_DIR.parent / ".command code" / "references" / "requirement_checklist"
)
ENV_CHAPTER = CHAPTER_DIR / ".env"
ENV_CH1 = CHAPTER_DIR.parent / "AI_chapter_01" / "Local LLM example" / ".env"

ISSUE_KEY_RE = re.compile(r"^[A-Z][A-Z0-9_]+-\d+$")
DEFAULT_MODEL = "qwen/qwen3.8-27b"
KNOWN_MODELS = ["qwen/qwen3.8-27b", "openai/gpt-oss-20b"]


def _read_env_key(path: Path, name: str) -> str:
    """Return the value for `name` in an .env file (BOM-tolerant)."""
    try:
        raw = path.read_text(encoding="utf-8").lstrip("\ufeff")
    except OSError:
        return ""
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        if key.strip() == name:
            return value.strip()
    return ""


def _groq_key() -> str:
    """Key priority: chapter .env -> chapter-1 .env -> UI override."""
    override = st.session_state.get("groq_key_override", "")
    if override:
        return override
    return _read_env_key(ENV_CHAPTER, "GROQ_API_TOKEN") or _read_env_key(
        ENV_CH1, "GROQ_API_TOKEN"
    )


def _load_rules() -> str:
    return RULES_PATH.read_text(encoding="utf-8")


def _load_checklist() -> str:
    try:
        return CHECKLIST_PATH.read_text(encoding="utf-8")
    except OSError:
        return ""


def _fetch_ticket(key: str) -> dict:
    """Run the deterministic Node fetch and return the normalized ticket dict."""
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["node", str(TOOLS_DIR / "fetch_issue.js"), key],
        capture_output=True,
        text=True,
        timeout=90,
        cwd=str(CHAPTER_DIR),
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise RuntimeError(detail or f"Fetch failed for {key}")
    norm_path = TMP_DIR / f"{key}.normalized.json"
    if not norm_path.exists():
        raise RuntimeError(f"Normalized file missing after fetch: {norm_path}")
    return json.loads(norm_path.read_text(encoding="utf-8"))


def _generate(key: str) -> tuple[str, str]:
    """Full pipeline. Returns (plan_markdown, status_note)."""
    ticket = _fetch_ticket(key)
    rules = _load_rules()
    checklist = _load_checklist()
    prompt = prompt_builder.build_prompt(ticket, rules, checklist)
    model = st.session_state.get("model", DEFAULT_MODEL)

    with st.spinner(f"Drafting the test plan with Groq ({model})..."):
        plan = groq_client.chat(_groq_key(), model, rules, prompt)

    note = (
        f"Ticket {key} — Groq `{model}` — {len(plan.split())} words. "
        "DRAFT — pending human review."
    )
    return plan, note


# ---------- page ----------
st.set_page_config(page_title="Test Plan Creator", layout="wide")
st.title("Test Plan Creator")
st.caption(
    "Enter a Jira ID (e.g. KAN-6) and click **Create Test Plan**. "
    "The ticket is fetched from Jira and drafted into a review-ready test plan by Groq."
)

with st.sidebar:
    st.subheader("Settings")
    model = st.text_input("Groq model", value=st.session_state.get("model", DEFAULT_MODEL))
    st.session_state["model"] = model
    st.caption("Models verified on this key: " + ", ".join(KNOWN_MODELS))

    groq_override = st.text_input(
        "Groq API key (override)",
        type="password",
        value=st.session_state.get("groq_key_override", ""),
        help="Leave blank to use GROQ_API_TOKEN from .env.",
    )
    st.session_state["groq_key_override"] = groq_override.strip()

    st.divider()
    st.subheader("Status")
    key_source = "chapter .env" if _read_env_key(ENV_CHAPTER, "GROQ_API_TOKEN") else (
        "chapter-1 .env" if _read_env_key(ENV_CH1, "GROQ_API_TOKEN") else "not set"
    )
    st.write(f"Groq key: **{key_source}**")
    st.write(f"Jira env: **{ENV_CHAPTER.name}**")

# ---------- main input ----------
col_key, col_btn = st.columns([3, 1])
with col_key:
    issue_key = st.text_input(
        "Jira issue key",
        placeholder="e.g. KAN-6",
        label_visibility="collapsed",
    )
with col_btn:
    st.write("")
    generate_clicked = st.button("Create Test Plan", type="primary", use_container_width=True)

if generate_clicked:
    key = (issue_key or "").strip()
    if not key:
        st.error("Enter a Jira issue key first (e.g. KAN-6).")
    elif not ISSUE_KEY_RE.match(key):
        st.error(f"'{key}' doesn't look like a Jira key. Expected e.g. KAN-6.")
    else:
        try:
            plan, note = _generate(key)
            st.session_state["plan"] = plan
            st.session_state["plan_key"] = key
            st.session_state["plan_note"] = note
            st.success(note)
        except (RuntimeError, groq_client.GroqError) as exc:
            st.error(f"{exc}")
        except Exception as exc:  # noqa: BLE001 — surface, don't crash
            st.error(f"Unexpected error: {exc}")

plan = st.session_state.get("plan")
if plan:
    st.subheader(f"Test Plan — {st.session_state.get('plan_key', '')}")
    edited = st.text_area(
        "Plan (editable before export)",
        value=plan,
        height=520,
        label_visibility="collapsed",
    )
    st.session_state["plan"] = edited

    c1, c2 = st.columns(2)
    if c1.button("Export Markdown"):
        try:
            md_path = export_mod.save_markdown(st.session_state["plan_key"], edited)
            st.success(f"Saved {md_path}")
        except OSError as exc:
            st.error(f"Could not write file: {exc}")

    if c2.button("Export PDF"):
        try:
            md_path = export_mod.save_markdown(st.session_state["plan_key"], edited)
            pdf_path = export_mod.save_pdf(md_path)
            if pdf_path:
                st.success(f"Saved {pdf_path}")
            else:
                st.error("No Chrome/Edge found for PDF export. Markdown was saved.")
        except (OSError, RuntimeError) as exc:
            st.error(f"PDF export failed: {exc}")

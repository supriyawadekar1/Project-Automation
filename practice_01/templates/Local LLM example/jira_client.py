"""Jira REST API client.

Fetches ticket details (summary, description, acceptance criteria) using
Basic auth. Tries the Cloud REST v3 endpoint first, then falls back to v2
(for Jira Server / Data Center instances).
"""

from __future__ import annotations

import re

import requests

TIMEOUT = 15


class JiraError(Exception):
    """Raised for connection/auth/not-found failures with a user-friendly message."""


def _adf_to_text(description) -> str:
    """Convert Atlassian Document Format JSON to plain text (recursively).

    Plain strings pass through unchanged. None becomes empty string.
    """
    if description is None:
        return ""
    if isinstance(description, str):
        return description

    parts = []

    def walk(node):
        node_type = node.get("type")
        content = node.get("content") or []

        if node_type == "text":
            text = node.get("text", "")
            marks = node.get("marks") or []
            if any(m.get("type") == "code" for m in marks):
                text = f"`{text}`"
            if any(m.get("type") == "strong" for m in marks):
                text = f"**{text}**"
            parts.append(text)
            return
        if node_type == "hardBreak":
            parts.append("\n")
            return
        if node_type in ("paragraph", "heading"):
            if parts and parts[-1] != "\n":
                parts.append("\n")
        for child in content:
            walk(child)
        if node_type in ("paragraph", "heading"):
            parts.append("\n")
        if node_type == "listItem":
            parts.append("\n")

    walk(description)
    text = "".join(parts)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _extract_acceptance_criteria(description: str) -> str | None:
    """Heuristic scan for an Acceptance Criteria section in the description.

    Matches headings/labels like 'Acceptance Criteria', 'Acceptance criteria:',
    or 'AC:' followed by content, and returns everything until the next
    section heading. Returns None when no section is found.
    """
    if not description:
        return None
    pattern = re.compile(
        r"(?im)^\s*(?:#{1,6}\s*)?(?:acceptance criteria|acceptance criterion|ac)\s*[:.-]?\s*$"
    )
    match = pattern.search(description)
    if not match:
        return None

    after = description[match.end():]
    # Stop at the next markdown/section-style heading.
    next_heading = re.search(r"(?im)^\s*(?:#{1,6}\s+|[A-Z][A-Za-z ]+:$)", after)
    criteria = after[: next_heading.start()] if next_heading else after
    criteria = criteria.strip()
    return criteria or None


def fetch_issue(jira_url: str, email: str, api_token: str, issue_key: str) -> dict:
    """Return {key, summary, description, acceptance_criteria} for a Jira issue."""
    jira_url = (jira_url or "").strip().rstrip("/")
    if not jira_url or not email or not api_token:
        raise JiraError("Jira credentials are not configured. Open Settings and save them.")

    auth = (email, api_token)
    headers = {"Accept": "application/json"}

    errors = []
    for api_version in ("3", "2"):
        url = f"{jira_url}/rest/api/{api_version}/issue/{issue_key}"
        try:
            resp = requests.get(url, auth=auth, headers=headers, timeout=TIMEOUT)
        except requests.RequestException as exc:
            errors.append(f"v{api_version}: {exc}")
            continue

        if resp.status_code == 200:
            data = resp.json()
            fields = data.get("fields") or {}
            description = _adf_to_text(fields.get("description"))
            return {
                "key": data.get("key") or issue_key,
                "summary": (fields.get("summary") or "").strip(),
                "description": description,
                "acceptance_criteria": _extract_acceptance_criteria(description),
            }
        if resp.status_code in (401, 403):
            raise JiraError(
                "Jira authentication failed. Check the email/API token in Settings."
            )
        if resp.status_code == 404:
            raise JiraError(f"Jira ticket '{issue_key}' was not found.")
        errors.append(f"v{api_version}: HTTP {resp.status_code}")

    raise JiraError(
        f"Could not reach Jira at {jira_url}. "
        f"Details: {'; '.join(errors) if errors else 'unknown error'}"
    )

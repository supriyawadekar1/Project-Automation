#!/usr/bin/env python3
"""Prompt assembly for the test-plan UI.

Combines the drafting rules (prompt_template.md), the gap-analysis checklist
(.command code/references/requirement_checklist), and the normalized ticket
facts into one user prompt for Groq.
"""

from __future__ import annotations


def build_prompt(ticket: dict, rules_text: str, checklist_text: str) -> str:
    """Compose the full user prompt from ticket facts + rules + checklist."""
    def _section(label: str) -> str:
        # Simple heuristic split on the first blank line after the label.
        return rules_text.split(label, 1)[-1].strip()

    description = (ticket.get("description") or "").strip() or "Not specified"
    ac = (ticket.get("acceptance_criteria") or "").strip() or "None found in the ticket"

    parts = [
        "## Ticket facts (fetched from Jira — ground truth)",
        f"- Key: {ticket.get('key', '?')}",
        f"- Summary: {ticket.get('summary', 'Not specified')}",
        f"- Type: {ticket.get('type', '?')}  | Project: {ticket.get('project', '?')}  | Status: {ticket.get('status', '?')}",
        "",
        "### Description",
        description,
        "",
        "### Acceptance Criteria",
        ac,
        "",
        "## Instructions",
        "Produce the TEST PLAN DRAFT now, following the output shape and rules above.",
        "Check the ticket against the gap-analysis checklist and include every "
        "⚠️/❌ finding as a row in 'Gaps & Questions for the author'.",
    ]
    return "\n".join(parts)

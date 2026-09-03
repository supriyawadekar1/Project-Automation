# 📜 LLM.md — Project Constitution

> **AI_chapter_02_blast** · Test Plan Creator from a Jira ID · B.L.A.S.T. / A.N.T.
> This is the binding reference for the LLM (me) while working on this project. Schemas, rules, and architecture live here. Update by agreement, not ad hoc.

---

## 1. Mission

Build a **test-plan creator**: user supplies a **Jira ticket key** (pilot target: **KAN-6**, user-confirmed 2026-09-03), the pipeline fetches the real ticket from Jira Cloud, extracts summary/description/acceptance criteria, and produces a **professional test-plan document** (Markdown → optional PDF) that is grounded in the ticket and clearly flags every unknown.

## 2. Data schemas

### 2.1 Input schema — what the pipeline accepts
```json
{
  "issue_key": "QA-102",
  "fields_filter": ["summary", "description", "status", "labels", "issuetype", "project"],
  "options": {
    "include_pdf": true,
    "output_dir": "output"
  }
}
```

### 2.2 Normalized ticket schema — the contract after fetch
```json
{
  "key": "QA-102",
  "summary": "…",
  "description": "plain text (ADF already flattened)",
  "acceptance_criteria": "… | null",
  "status": "In Progress",
  "labels": [],
  "issuetype": "Story",
  "project_key": "QA"
}
```

### 2.3 Test-plan output schema — the deliverable
```json
{
  "title": "Test Plan — QA-102 (…): <summary>",
  "status": "DRAFT — pending human review",
  "source_ticket": "QA-102",
  "sections": {
    "scope_and_objectives": { "in_scope": [], "out_of_scope": [], "objective": "…" },
    "gaps_and_questions": [ { "area": "", "finding": "⚠️/❌", "question_to_author": "" } ],
    "test_scenarios": [ { "id": "TS-1", "priority": "P0", "type": "pos|neg|boundary|security|perf|a11y|responsive|integration|compat", "scenario": "", "maps_to": "" } ],
    "test_data_and_env": { "data": [], "environment": [], "roles": [] },
    "risks_and_assumptions": { "assumptions": [], "risks": [] },
    "entry_exit_criteria": { "entry": [], "exit": [] }
  },
  "human_review_gate": { "assumed": [], "could_not_confirm": [], "open_questions": [] }
}
```

### 2.4 Allowed data sources
| Source | Allowed? |
|--------|----------|
| Jira `GET issue` fields (summary, description, comments, labels) | ✅ yes |
| Published house templates / prior approved test plans | ✅ yes |
| Anything the LLM "infers" that the ticket does not state | ❌ no — becomes a Gap/Question |

## 3. Behavioral rules (binding)

1. **No fabrication.** Never invent ticket content, requirements, URLs, or acceptance criteria. If a fact is needed and missing → record it in `gaps_and_questions` with a question to the author.
2. **Data-first.** No coding until schemas in §2 are agreed; if logic/data shape changes, update `LLM.md` and the SOP **before** code.
3. **Deterministic core.** Jira fetch, ADF flattening, AC extraction, file rendering = deterministic tools (Node.js in `tools/`). The LLM only drafts content within the schemas; never route, decide, or handle credentials probabilistically. (UI workstream: Python/Streamlit is the *shell*; the deterministic tools stay Node.)
4. **Secrets hygiene.** Credentials live in `.env` (git-ignored), never hardcoded, never pasted into docs unredacted.
5. **Atomic steps.** Each `tools/` script does one job, is independently testable, and writes intermediate files under `.tmp/`.
6. **Golden Rule.** If logic changes → update the SOP in `architecture/` first, then the code.
7. **Human Review Gate.** Every deliverable ends with a review gate listing assumed vs confirmed vs open questions; nothing is "approved" until a human signs off.
8. **Scope discipline.** Work only inside `AI_chapter_02_blast/` (+ final `output/` deliverables). Respect the chapter boundary.
9. **Local instructions rule.** The test-plan *shape* and gap-analysis rules come from the locally-installed `.command code/SKILL.md` (test-plan-generator): 6 sections + requirement checklist + Human Review Gate. The 14-section `references/templates/Test_Plan_Template` is the alternate master form — only use if a user explicitly asks.

## 4. Architecture

### 4.1 A.N.T. three layers (per BLAST.md)
- **Layer 1 — Architecture (`architecture/`):** Markdown SOPs documenting goals, inputs, tool logic, edge cases.
- **Layer 2 — Navigation (reasoning/LLM):** routes data between SOPs and tools in a fixed order; does not improvise business logic.
- **Layer 3 — Tools (`tools/`):** deterministic Node.js scripts. Atomic, testable, `.env` for secrets, `.tmp/` for intermediates.

### 4.2 Pipeline (fixed order)
```
issue_key
   → tools/fetch_issue.js    (Jira REST, v3, ADF→text, AC extract)      [deterministic, Node]
   → normalized_ticket.json  (.tmp/)
   → LLM drafting step       (Groq; fills the test-plan schema from ticket ONLY)  [creative, constrained]
   → tools/render_plan.js    (seed schema → Markdown; deterministic)    [deterministic, Node]
   → output/Test_Plan_<KEY>.md
   → tools/md2html.js + headless Chrome → output/Test_Plan_<KEY>.pdf     [deterministic]
```
UI variant (`ui/`): the same flow is wrapped by Streamlit; the LLM step calls
Groq directly (model `qwen/qwen3.8-27b`, `max_tokens 8192`) and the user can
export md/pdf from the browser.

### 4.3 Folder layout
```
AI_chapter_02_blast/
├── BLAST.md
├── prompt used.md
├── task_plan.md          ← phases / goals / checklists
├── findings.md           ← research, discoveries, curl examples
├── progress.md           ← timestamped activity log
├── LLM.md                ← THIS constitution
├── architecture/         ← technical SOPs (SOP-01 pipeline, SOP-02 UI)
├── tools/                ← deterministic Node scripts (fetch/render/md2html)
├── ui/                   ← Streamlit + Groq web UI
├── .env                  ← secrets (git-ignored)
└── .tmp/                 ← intermediate files
```
Final deliverables: `output/Test_Plan_<KEY>.md` + `.pdf` (house format).

### 4.4 Key design decisions & why
| Decision | Reason |
|----------|--------|
| Fetch in Python (`requests`), not raw curl | Easier v3/v2 fallback, ADF walker, error typing, reuse of proven prior code |
| Try `rest/api/3` then `rest/api/2` | Cloud + Server/Data Center compat |
| Flatten ADF to text inside the fetcher | The LLM should never see nested JSON, only clean ticket text |
| Extract ACs with a regex heuristic | Prior chapter proved it works; keeps "Acceptance Criteria" discoverable for scenario mapping |
| LLM constrained to the output schema | Guarantees every plan has scope/gaps/scenarios/data/risks/gate sections in the house format |
| Deterministic renderer | Markdown/PDF look identical run-to-run; no LLM drift in formatting |
| Human Review Gate always present | Team rule: never ship AI output as approved without a human |

### 4.5 Edge cases the architecture must handle
- Ticket not found / 404 → clear error, no partial plan.
- Auth 401 → instruct token refresh; stop before drafting (Link gate).
- Description missing / empty / only ADF headings → AC extraction returns `null`; gaps table flags it.
- No explicit ACs → scenarios keyed to gaps, like the VWO-49 plan.
- Non-Story issue types (Bug, Epic) → same pipeline; mapping sections adapt.
- Output path/PDF engine missing → degrade gracefully to Markdown-only and log it.

## 5. Version log
| Date | Change |
|------|--------|
| 2026-09-03 | v0.1 — Constitution initialized at Protocol 0 (schemas, rules, architecture draft). Pending Discovery answers. |
| 2026-09-03 | v0.2 — Pilot target confirmed: **KAN-6** (VWO Login Dashboard). Auth handshake failing (401); token refresh required before Phase 2 fetch. |
| 2026-09-03 | v0.3 — Direction locked: **regenerate from the live KAN-6 ticket**; VWO-49 plan serves only as the format reference. |
| 2026-09-03 | v0.4 — **Phase 2 (Link) passed**: handshake 200; KAN-6 fetched (Task, summary "VWO-49", full PRD in description); chapter `.env` + `.tmp/` created. Constraint: Python absent on PATH. |
| 2026-09-03 | v0.5 — **Phase 3 (Architect)**: Node.js `tools/` (fetch_issue.js, render_plan.js) + architecture/SOP-01; KAN-6 pipeline run → `output/Test_Plan_KAN-6.md`. |
| 2026-09-03 | v0.6 — **Phase 4 (Stylize)**: tools/md2html.js added; `output/Test_Plan_KAN-6.pdf` produced via headless Chrome. B.L.A.S.T. loop complete pending human sign-off. |
| 2026-09-03 | v1.0 — **HUMAN SIGN-OFF received** ("we are good", 19:35). KAN-6 run **COMPLETE**; pipeline reusable for any Jira key. |
| 2026-09-03 | v1.1 — **UI workstream added**: Streamlit UI in `ui/` (Groq provider). Local `.command code/SKILL.md` output shape governs the prompt. SOP-02 written. Model default `qwen/qwen3.8-27b` (verified), `max_tokens 8192`. Verified end-to-end. |

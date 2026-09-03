# 🗺️ task_plan.md — Test Plan Creator from a Jira ID

> Part of **AI_chapter_02_blast** · B.L.A.S.T. protocol run · Status: **Protocol 0 — Initialization**
> Created: 2026-09-03 19:07 · Source of truth: `BLAST.md`

---

## North Star (draft — confirm in Discovery)

Take a **single Jira ticket key** (e.g. `QA-102`, `VWO-49`) as input and produce a **professional, ready-to-review Test Plan document** (Markdown + optional PDF), grounded only in what the ticket actually says, with gaps/questions surfaced instead of invented.

## Master checklists

### 🟢 Protocol 0 — Initialization (IN PROGRESS)
- [x] Read `BLAST.md` and select Protocol 0
- [x] Identify chapter scope (folder `AI_chapter_02_blast` only)
- [x] Create `task_plan.md` (this file) — phases, goals, checklists
- [x] Create `findings.md` — research, discoveries, constraints, Jira fetch methods
- [x] Create `progress.md` — activity log (what/errors/results)
- [x] Create `LLM.md` — Project Constitution: schemas, rules, architecture
- [ ] ⛔ **HALT** — no code in `tools/` until Discovery answered + schema approved
- [x] ✅ Discovery partially answered via chat: pilot **KAN-6**, format reference = VWO-49 plan, regenerate from live ticket

### 🏗️ Phase 1 — Blueprint (Vision & Logic)
- [ ] Ask/answer the 5 Discovery Questions (North Star, Integrations, Source of Truth, Delivery Payload, Behavioral Rules)
- [x] Define JSON data schema (input/output shapes) in `LLM.md`
- [ ] Research: search GitHub + other DBs for existing Jira→test-plan resources
- [x] Write the technical SOP for the test-plan generator in `architecture/` (SOP-01)
- [ ] **Gate:** User approves Blueprint before any tools are built

### ⚡ Phase 2 — Link (Connectivity)
- [x] Confirm Jira credentials (now valid — token refreshed 2026-09-03)
- [x] Verify Jira REST connection with a minimal request (handshake → **HTTP 200**)
- [x] Fetch KAN-6 live → **HTTP 200**; payload saved `.tmp/kan6_raw.json`; content verified
- [x] Build minimal `tools/` fetch script; confirm ticket payload shape matches schema
- [x] **Gate:** Link works — proceed to full logic
- [x] ⚠️ Environment constraint resolved → chose **Node.js v24** over Python (user option **a**)

### ⚙️ Phase 3 — Architect (3-Layer Build)
- [x] Layer 1: Write `architecture/SOP-01-test-plan-pipeline.md`
- [x] Layer 2: Fixed pipeline defined (fetch → normalize → seed → render) — no probabilistic business logic
- [x] Layer 3: Build atomic, testable scripts in `tools/` (**Node.js**: `fetch_issue.js`, `render_plan.js`)
- [x] Use `.env` for secrets, `.tmp/` for intermediate files
- [x] Wire the LLM step into the pipeline (seed JSON authored from normalized ticket)
- [x] **Golden Rule:** SOP updated before code when logic changed
- [x] 🎉 **Pipeline end-to-end verified on KAN-6** → `output/Test_Plan_KAN-6.md` (34 scenarios, 17 gaps)

### ✨ Phase 4 — Stylize (Refinement & UI)
- [x] Format test-plan payload for professional delivery (tables, status headers, gap tables)
- [x] Render Markdown output (+ PDF via headless Chrome `--print-to-pdf`) → `output/Test_Plan_KAN-6.md` + `.pdf`
- [x] Present to user for feedback before final deployment → draft presented, PDF approved
- [ ] **Final:** human sign-off on the delivered test plan (HUMAN REVIEW GATE)
- [x] ✅ **APPROVED by user** (2026-09-03 19:35) — deliverables locked in `output/Test_Plan_KAN-6.{md,pdf}`

### 🖥️ UI workstream — Streamlit + Groq (added 20:11)
- [x] Follow local `.command code/SKILL.md` test-plan-generator instructions (6-section shape + checklist + gate)
- [x] Verify bundled Python + streamlit runtime (Python 3.11.9, streamlit 1.62)
- [x] Verify Groq key + available models (`qwen/qwen3.8-27b` works; `gpt-oss-20b` empty on long prompts; no llama-3.3-70b)
- [x] Write `architecture/SOP-02-test-plan-ui.md`
- [x] Build `ui/app.py`, `ui/groq_client.py`, `ui/prompt_builder.py`, `ui/prompt_template.md`, `ui/export.py`, `ui/requirements.txt`, `ui/README.md`
- [x] Add `GROQ_API_TOKEN` to chapter `.env`
- [x] Set `max_tokens: 8192` (fixes truncated Groq plans) + default model `qwen/qwen3.8-27b`
- [x] Verify end-to-end: Streamlit serves (health 200), fetch → Groq → Export md/pdf works
- [x] Restore approved KAN-6 deliverables overwritten during export test
- [ ] **User runs:** `streamlit run ui/app.py`, enters a Jira ID → Create Test Plan

---

## Goals
1. Fetch a real Jira ticket (summary, description, acceptance criteria) with authenticated API calls
2. Convert ticket content into a structured test-plan document following the established house format
3. Keep the pipeline deterministic: scripts in `tools/`, logic documented in `architecture/`, LLM only for creative/drafting steps
4. Never invent ticket content; surface every unknown as a gap/question for the human
5. Deliver Markdown + PDF into the `output` folder

## Deliverables map
| File | Purpose |
|------|---------|
| `task_plan.md` | Phases, goals, checklists (this file) |
| `findings.md` | Research, discoveries, constraints, curl/requests |
| `progress.md` | Timestamped log — what was done, errors, results |
| `LLM.md` | Project Constitution — schemas, rules, architecture |
| `architecture/` | (Phase 3) Technical SOPs |
| `tools/` | (Phase 3+) Deterministic Python scripts |
| `.env` / `.tmp/` | Secrets / intermediate files |
| `output/` | Final Markdown + PDF deliverables |

## Pending open questions (from Protocol 0/1)
- [x] **Which Jira ticket key is the first target for the pilot run?** → **KAN-6** (VWO Login Dashboard; user-confirmed 2026-09-03)
- [x] Test-plan format: reuse `output/Test_Plan_VWO-49.md` style, or a new template? → **Regenerate from the live KAN-6 ticket**, using VWO-49's format as the structure reference (user-confirmed 2026-09-03)
- [ ] Delivery: file only, or PDF too (per house preference)?
- [ ] Where do the credentials live for this chapter: `.env` in `AI_chapter_02_blast/`?

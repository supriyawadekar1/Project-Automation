# 📈 progress.md — Activity Log

> B.L.A.S.T. run · **AI_chapter_02_blast** · Test Plan Creator from a Jira ID
> Convention: append entries in blocks (hourly / half-hourly / 10-min as the pace demands). Latest at the bottom.

---

## 2026-09-03

### 19:07 — Protocol 0 kickoff (restart)
**Done:**
- Re-read `BLAST.md`; confirmed Protocol 0 = initialization + halt.
- Reviewed chapter folder: only `BLAST.md` and `prompt used.md` present → clean Protocol 0 start.
- Checked root and chapter for a skill dir / `.env`: no personal skill loaded; no `.env` in this chapter yet.
- Read prior-chapter reference files:
  - `AI_chapter_01/Local LLM example/jira_client.py` → ADF flattening + AC extraction + dual v3/v2 fallback.
  - `AI_chapter_01/Local LLM example/.env` → found Jira URL/email/token (Cloud instance).
  - `output/Test_Plan_VWO-49.md` → house test-plan format incl. gap tables + HUMAN REVIEW GATE.
- Ran a live Jira handshake (below).
**Result:**
- `GET /rest/api/3/myself` with the stored token returned **HTTP 401** → token expired/revoked.
- Created the four Protocol 0 files in `AI_chapter_02_blast/`: `task_plan.md`, `findings.md`, `progress.md`, `LLM.md`.
**Notes / next steps:**
- ⛔ Per BLAST Protocol 0, execution halts here: no `tools/` code until Discovery answers + schema approval.
- **Blocker for Phase 2:** need a fresh Jira API token from the Atlassian account (Security → API tokens).

### 19:07 — Error encountered
| Item | Detail |
|------|--------|
| Command | `curl.exe -s -o NUL -w "HTTP_STATUS=%{http_code}" -u "<email>:<token>" -H "Accept: application/json" "…/rest/api/3/myself"` |
| Result | `HTTP_STATUS=401` |
| Cause | Stored `JIRA_API_TOKEN` no longer valid (expired or revoked) |
| Fix | Generate a new token at https://id.atlassian.com/manage-profile/security/api-tokens, store in chapter `.env`, re-run handshake |

### 19:12 — Pilot ticket confirmed + definitive auth diagnosis
**Done:**
- User confirmed the pilot target: **KAN-6** (VWO Login Dashboard). Recorded in `task_plan.md` open questions (resolved).
- Ran live probes against `https://wadekarsupriya19.atlassian.net` (token read from `.env` at runtime):
  1. `GET /rest/api/3/issue/KAN-6` → `HTTP_STATUS=404`
  2. `GET /rest/api/3/myself` → `HTTP_STATUS=401`, body: `Client must be authenticated to access this resource.`
  3. `GET /rest/api/3/project/search?maxResults=50` → `HTTP 200` but `"total":0`, `"values":[]`
**Result / diagnosis:**
- Auth is definitively **invalid (401)** — the earlier KAN-6 `404` is Jira Cloud's **masked 401** when unauthenticated (empty project list corroborates: no token = no visible projects).
- KAN-6 cannot be fetched until the token is refreshed.
**Notes / next steps:**
- **BLOCKER (Phase 2 Link):** user must generate a fresh API token at https://id.atlassian.com/manage-profile/security/api-tokens.
- Store the new token in `AI_chapter_02_blast/.env` (copy of the chapter's first). Then re-run the KAN-6 handshake and continue.
- Interesting wrinkle for LLM.md: the VWO-49 plan already exists in `output/` — decide whether this run **reuses** it or regenerates from the live KAN-6 ticket.

### 19:13 — Direction confirmed + auth re-check
**Done:**
- User chose: **regenerate from the live KAN-6 ticket** (existing `output/Test_Plan_VWO-49.md` is the format reference, not the baseline to copy).
- Re-ran the `/myself` handshake to check whether the token was refreshed.
**Result:**
- `GET /rest/api/3/myself` → still **HTTP 401**. Token not yet refreshed.
**Notes / next steps:**
- Still **BLOCKED on Phase 2** until a fresh API token is provided (https://id.atlassian.com/manage-profile/security/api-tokens).
- Once auth passes: fetch KAN-6 → verify ticket content → run pipeline → deliver regenerated `Test_Plan_KAN-6.md` (+ PDF) into `output/`.

### 19:28 — Phase 2 (Link) handshake verified ✅
**Done:**
- User refreshed the Jira API token.
- Re-ran `GET /rest/api/3/myself` → **HTTP 200** ✅ (auth now valid).
- Created chapter infra: `AI_chapter_02_blast/.tmp/` and `.gitignore` (ignores `.env`, `.tmp/`).
- Created `AI_chapter_02_blast/.env` (chapter-local credentials, git-ignored).
- Fetched **KAN-6** → `HTTP 200`, raw payload saved to `.tmp/kan6_raw.json` (12,444 bytes).

**Errors encountered along the way (important):**
1. **Chapter `.env` empty on re-read** — my array-based `WriteAllLines` collapsed 3 lines into 1 space-joined string (PowerShell 5.1 parsing gotcha). Fixed with explicit `"`n"` join + `WriteAllText`.
2. **Source `.env` parse missed keys** — the file has a UTF-8 BOM (`U+FEFF`) prefixing the first key and a space after `JIRA_URL=`. Fixed by stripping the BOM and splitting each line on the **first** `=`.
3. **Python not installed** (`python`/`py` not found on PATH) → environment constraint: the planned `tools/` scripts need a Python runtime or an alternate approach.

**Verified ticket content (KAN-6):**
- Key: `KAN-6` · Summary: `VWO-49` · Type: `Task` · Project: `KAN / My Software Team`
- Status: `To Do` · Created: 2026-08-20 · Labels: none
- Description: ADF doc, flattened to **9,199 chars** — the full "VWO Login Dashboard" PRD, includes `http://app.vwo.com` inlineCard link
- Matches the ticket that produced `output/Test_Plan_VWO-49.md` → confirms format baseline applies

**Notes / next steps:**
- ✅ **Phase 2 Link gate passed** — Jira fetch works against the live ticket.
- Next: Phase 3 (Architect) — resolve the Python runtime constraint, then build `tools/` fetch/normalize/render scripts per `LLM.md` schemas.

### 19:31 — Phase 3 (Architect) — Node.js `tools/` built & pipeline run ✅
**Done:**
- User chose **option (a)**: deterministic scripts in **Node.js v24** (ESM, zero deps) instead of Python — confirmed available (`node v24.18.1`).
- Created `architecture/SOP-01-test-plan-pipeline.md` (Layer 1): goal, runtime decision, fixed pipeline, tool specs, edge cases, LLM behavior rules.
- Built `tools/fetch_issue.js` (Layer 3): reads `.env` (BOM-tolerant), GETs `rest/api/3/issue/<KEY>`, flattens ADF→text, extracts ACs heuristically, writes `.tmp/<KEY>.normalized.json`.
- Built `tools/render_plan.js`: deterministic Markdown renderer per house format (header, scope, gaps, scenarios, data/env, risks, entry/exit, HUMAN REVIEW GATE) → `output/Test_Plan_<KEY>.md`.
- Authored `.tmp/KAN-6.seed.json` (LLM drafting step, schema-conformant) from the normalized ticket only.

**Results (all verified):**
- `node tools/fetch_issue.js KAN-6` → `OK KAN-6 [Task] "VWO-49" status=To Do desc=9201ch ac=null`; wrote `.tmp/KAN-6.normalized.json`.
- `node tools/render_plan.js KAN-6 .tmp/KAN-6.seed.json` → `WROTE output/Test_Plan_KAN-6.md`.
- **Deliverable:** `output/Test_Plan_KAN-6.md` — 34 test scenarios (TS-1..TS-34), 17 gaps/questions, scope, data/env, risks, entry/exit, HUMAN REVIEW GATE. Structure mirrors `Test_Plan_VWO-49.md`; content grounded in KAN-6's PRD description.
- Note: KAN-6 has **no explicit acceptance criteria section** (`ac=null`) → scenarios map to PRD sections + gap IDs, consistent with the VWO-49 precedent.

**Errors / decisions logged:**
- Renderer initially read objective from `s.objective`; fixed to prefer `scope_and_objectives.objective` (schema-correct).
- One scenario row (TS-19) maps to "Gap 16" while all others are "Gap N"-labeled consistently — cosmetic, flagged for polish.

**Notes / next steps:**
- Pipeline (fetch → normalize → seed → render) is fully working end-to-end for KAN-6.
- Phase 4 (Stylize): review the draft with the user; produce PDF (headless browser) if wanted.

### 19:34 — Phase 4 (Stylize) — PDF delivered ✅
**Done:**
- User approved the draft for PDF generation.
- Located headless-capable browsers: Chrome + Edge installed (no pandoc/wkhtmltopdf).
- Built `tools/md2html.js`: dependency-free Markdown→styled-HTML converter (headings, blockquote, lists, pipe tables, inline bold/code/links) with clean print CSS.
- Converted `output/Test_Plan_KAN-6.md` → `.tmp/Test_Plan_KAN-6.html` (14,711 bytes; verified: 1×h1, 7×h2, 2 tables, 53 rows, 1 link).
- Rendered PDF via `chrome --headless --print-to-pdf`.

**Results (verified):**
- `output/Test_Plan_KAN-6.pdf` — **212,395 bytes**, valid `%PDF-1.4` header.
- Final deliverables in `output/`: `Test_Plan_KAN-6.md` (11 KB) + `Test_Plan_KAN-6.pdf` (212 KB).

**Notes / next steps:**
- Full B.L.A.S.T. loop complete for KAN-6: Protocol 0 → Blueprint → Link → Architect → Stylize.
- Remaining: **human sign-off** on the delivered test plan (HUMAN REVIEW GATE).

### 19:35 — ✅ HUMAN SIGN-OFF received
**Result:**
- User confirmed **"we are good"** — the KAN-6 test plan is **approved** by a human reviewer.
- Deliverables locked: `output/Test_Plan_KAN-6.md` + `output/Test_Plan_KAN-6.pdf`.
- B.L.A.S.T. run for **AI_chapter_02_blast** is **COMPLETE**. 🎉
**Next steps (optional):**
- Reuse the pipeline for any other Jira key (e.g. `node tools/fetch_issue.js <KEY>` → seed → render).
- PDF via `tools/md2html.js` + headless Chrome `--print-to-pdf`.

### 20:11 — UI workstream (Streamlit + Groq) — built & verified ✅
**Done:**
- Followed the local instructions in `.command code/SKILL.md` (test-plan-generator skill) — its 6-section output shape + Human Review Gate + requirement checklist drive the prompt given to Groq.
- Plan mode used to research; user approved the approach (6-section template, app in `AI_chapter_02_blast/`).
- Verified runtime: bundled Python 3.11.9 at `C:\Users\NILESH\.lmstudio\extensions\backends\vendor\_amphibian\cpython3.11-win-x86@6\python.exe` has streamlit 1.62 + requests.
- Verified Groq key scope: `/models` lists **14 models only** — **no llama-3.3-70b**. Chat test: `qwen/qwen3.8-27b` returns full plans; `openai/gpt-oss-20b` returns **empty** on the long KAN-6 prompt.
- Created files:
  - `architecture/SOP-02-test-plan-ui.md` — Layer-1 SOP for the UI workstream
  - `ui/app.py` — Streamlit UI (Jira key input → Create Test Plan → editable plan → Export md/pdf)
  - `ui/groq_client.py` — Groq chat client (no SDK; 401/404/429/timeout + empty-response errors)
  - `ui/prompt_builder.py` — prompt assembly (ticket facts + rules + checklist)
  - `ui/prompt_template.md` — drafting rules fed to Groq
  - `ui/export.py` — Markdown save + PDF via `tools/md2html.js` + headless Chrome
  - `ui/requirements.txt`, `ui/README.md`
- Added `GROQ_API_TOKEN` to chapter `.env` (copied from chapter-1 `.env`).
- **Model default is `qwen/qwen3.8-27b`** after `gpt-oss-20b` returned empty content (long-prompt limitation); set `max_tokens: 8192` after qwen output truncated at the default ceiling.

**Errors encountered & fixed:**
1. `openai/gpt-oss-20b` returned an empty string for the full 9.6K-char KAN-6 prompt → switched default to `qwen/qwen3.8-27b` (7.8–10.3K char plans) and added an empty-response error hint.
2. Qwen plan truncated mid-sentence (default `max_tokens` ceiling) → set `max_tokens: 8192` → complete plans incl. Human Review Gate (verified: 10,274 chars).
3. Console `UnicodeEncodeError` printing the plan in a test script → test-only, set `PYTHONIOENCODING=utf-8`.

**Verified (headless, using the exact app code path):**
- Streamlit served on `:8501` → health `200 ok`; stopped after test (port freed).
- Fetch → Groq draft → Export Markdown → Export PDF all succeeded:
  - `output/Test_Plan_KAN-6.md` Groq draft = 7,998 bytes (qwen), PDF = 84,066 bytes.
  - Groq plan quality: 12 gaps, ~18 traceable P0/P1/P2 scenarios, grounded in the KAN-6 PRD, ends with the Human Review Gate.
- ⚠️ The test export temporarily **overwrote the approved KAN-6 deliverables**; restored the approved `output/Test_Plan_KAN-6.md` (11,237 B) + `.pdf` (212,395 B) via the deterministic `render_plan.js` + md2html + Chrome pipeline. Groq draft preserved at `.tmp/groq_fullflow_plan.md`.
- Removed temp test scripts; dev server stopped; port 8501 free.

**Notes / next steps:**
- Run the UI: `<bundled python> -m streamlit run ui/app.py` from `AI_chapter_02_blast/`, open `http://localhost:8501`, enter a Jira key → Create Test Plan.
- Any new Jira key generates a fresh Groq test-plan draft with export to `output/Test_Plan_<KEY>.{md,pdf}`.

# SOP-01 — Test Plan Creator pipeline (KAN-6 pilot)

> Layer 1 Architecture doc · `AI_chapter_02_blast/architecture/`
> Golden Rule: **if logic changes, update this SOP before changing code.**

## 1. Goal
Turn a Jira ticket key (`KAN-6`) into a professional **test-plan Markdown document**, grounded only in the fetched ticket, with unknowns surfaced as gaps/questions.

## 2. Runtime decision (2026-09-03)
Python is **not installed** on this machine. Per user choice (option **a**), the deterministic `tools/` layer is implemented in **Node.js v24** (ESM), no third-party deps. PowerShell is used only for env/glue.

## 3. Pipeline (fixed order)
```
tools/fetch_issue.js <KEY>          → reads .env, GETs Jira, normalizes → .tmp/<KEY>.normalized.json
tools/render_plan.js  <KEY> <seed.md> → schema JSON → final Markdown (deterministic)
output/Test_Plan_<KEY>.md
```
- Intermediate files go in `.tmp/`.
- Secrets come from `AI_chapter_02_blast/.env` (git-ignored).
- Fetch and render are **deterministic**. The LLM (me) authors the seed JSON content; scripts never invent business logic.

## 4. Tool specs

### 4.1 `tools/fetch_issue.js`
- Input: `process.argv[2]` = issue key.
- Reads `.env` from `AI_chapter_02_blast/.env` (BOM-tolerant parser, split on first `=`).
- GET `${JIRA_URL}/rest/api/3/issue/${KEY}?fields=summary,description,status,labels,issuetype,project` with Basic auth; `Accept: application/json`.
- On HTTP 401 → stop with clear "token invalid" message. On 404 → "issue not found".
- Flattens the ADF `description` to plain text (walk `content[]`; text nodes → text; inlineCard → `[url]`).
- Extracts Acceptance Criteria via heuristic regex on the flattened text (headings `Acceptance Criteria/AC` → until next heading). Returns `null` if absent.
- Writes `.tmp/<KEY>.normalized.json` = `{ key, summary, type, project, status, url, description, acceptance_criteria }`.
- Prints a one-line summary.

### 4.2 `tools/render_plan.js`
- Inputs: `argv[2]` = issue key; reads `.tmp/<KEY>.normalized.json` + `argv[3]` seed JSON file.
- Emits the house-format Markdown deterministically:
  1. Title/header (source ticket, author, DRAFT status)
  2. Scope & Objectives (in/out)
  3. Gaps & Questions table
  4. Test Scenarios table
  5. Test Data & Environment
  6. Risks & Assumptions
  7. Entry / Exit criteria
  8. HUMAN REVIEW GATE
- Writes `output/Test_Plan_<KEY>.md`; mirrors a `.pdf` when a headless browser is available (optional, Phase 4).

## 5. Seed JSON contract (authored by LLM)
The seed file must satisfy the `LLM.md` §2.3 test-plan output schema. The renderer only formats; it does not fill gaps. If a section is missing data, renderer prints `TBD — (reason)` so the HUMAN REVIEW GATE stays honest.

## 6. Edge cases
| Case | Behavior |
|------|----------|
| 401 auth | fetch stops: "Jira token invalid/expired — refresh in Atlassian → .env" |
| 404 issue | fetch stops: "issue not found" |
| Empty/missing description | normalized `description: ""`, `acceptance_criteria: null`; renderer's gaps table flags it |
| No explicit ACs | scenarios map to gap IDs, not AC IDs (per VWO-49 precedent) |
| Non-Story type (Task/Bug) | same pipeline; issuetype recorded in header |
| Missing seed sections | renderer emits the section shell with `TBD` markers, never fabricated content |

## 7. Behavior rules for the LLM authoring seeds
1. Only use content present in `.normalized.json`; anything else → gaps/questions.
2. Priority = P0/P1/P2 as in house format.
3. Every plan ends with a HUMAN REVIEW GATE (assumed / could-not-confirm / open questions).
4. No invented URLs, accounts, or thresholds — those become questions to the author.

# 🔎 findings.md — Research & Discoveries

> Part of **AI_chapter_02_blast** · B.L.A.S.T. run · Updated: 2026-09-03 19:07
> Objective: how to fetch Jira ticket data and turn it into a test plan.

---

## 1. What I found

### 1.1 Jira instance details (from prior chapter work)
- The Jira used in this workspace is **Atlassian Cloud**:
  - **Jira URL:** `https://wadekarsupriya19.atlassian.net`
  - **Auth method:** Basic auth with an **API token** (`email:api_token`), not a password
  - Credentials discovered in `AI_chapter_01/Local LLM example/.env` (see §4)

### 1.2 REST API endpoints that matter
| Endpoint | Purpose | Auth |
|----------|---------|------|
| `GET /rest/api/{2\|3}/issue/{KEY}` | Fetch single ticket: summary, description, labels, status, etc. | Basic |
| `GET /rest/api/{2\|3}/search` (JQL) | Query tickets by project / key list / filter | Basic |
| `GET /rest/api/{2\|3}/issue/{KEY}/comment` | Ticket comments (extra context for testing) | Basic |
| `GET /rest/api/{2\|3}/user/search` | Validate the account / find users | Basic |

- **Cloud supports both `rest/api/2` and `rest/api/3`.** `v3` returns descriptions as **ADF** (Atlassian Document Format JSON); `v2` can return either ADF or wiki markup depending on server config. The prior `jira_client.py` tries `v3` first, then falls back to `v2` — that dual-version strategy is worth keeping.

### 1.3 The description payload is ADF, not plain text
- Ticket descriptions arrive as a nested JSON tree (`type`, `content[]`, `marks[]`), so the fetch layer must flatten ADF → plain text before an LLM sees it.
- Prior art in `AI_chapter_01/Local LLM example/jira_client.py` already contains an `_adf_to_text()` walker and an `_extract_acceptance_criteria()` heuristic that scans the flattened text for an "Acceptance Criteria / AC" section.

### 1.4 House test-plan format already exists
- `output/Test_Plan_VWO-49.md` defines the structure the team already uses:
  1. Header (status DRAFT, author, source ticket)
  2. Scope & Objectives (in/out)
  3. **Gaps & Questions table** (finding, question to author)
  4. Test Scenarios table (ID, priority, type, scenario, maps-to)
  5. Test Data & Environment
  6. Risks & Assumptions
  7. Entry/Exit criteria
  8. **HUMAN REVIEW GATE** (assumed vs confirmed vs open questions)
- House preference (from prior chapters): deliver both **Markdown and PDF** into an `output/` folder.

### 1.5 Handshake result — auth currently FAILING (confirmed 2026-09-03 19:12)
- Target ticket for the pilot: **KAN-6** (VWO Login Dashboard) — user-confirmed.
- Live probe results against `https://wadekarsupriya19.atlassian.net` (token read from `.env` at runtime, never echoed):
  1. `GET /rest/api/3/myself` → **HTTP 401**, body: `Client must be authenticated to access this resource.`
  2. `GET /rest/api/3/project/search?maxResults=50` → **HTTP 200 but `"total":0`, `"values":[]`** (zero projects = classic invalid-auth signature)
  3. `GET /rest/api/3/issue/KAN-6` → **HTTP 404** — Jira Cloud's **masked 401** when unauthenticated
- Conclusion: the stored API token is **expired or revoked**. Until refreshed, Phase 2 (Link) cannot proceed — this is the blocking finding.
- **Fix:** generate a new token at https://id.atlassian.com/manage-profile/security/api-tokens and store it in the chapter `.env`.

---

## 2. Curl / requests I will use

### 2.1 Verify auth (handshake)
```bash
curl -s -o NUL -w "HTTP_STATUS=%{http_code}" \
  -u "wadekar.supriya19@gmail.com:ATATT..." \
  -H "Accept: application/json" \
  "https://wadekarsupriya19.atlassian.net/rest/api/3/myself"
```
Expect `200`. **Current result: `401`** (`Client must be authenticated…`) → token must be regenerated in Atlassian account settings.

### 2.2 Fetch one ticket (plain curl)
```bash
curl -s \
  -u "wadekar.supriya19@gmail.com:ATATT..." \
  -H "Accept: application/json" \
  "https://wadekarsupriya19.atlassian.net/rest/api/3/issue/QA-102?fields=summary,description,status,labels,issuetype,project"
```

### 2.3 Fetch with search/JQL (batch or fallback)
```bash
curl -s \
  -u "wadekar.supriya19@gmail.com:ATATT..." \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"jql":"key = QA-102","fields":["summary","description"]}' \
  "https://wadekarsupriya19.atlassian.net/rest/api/3/search"
```

### 2.4 Python requests equivalent (for `tools/`)
```python
import requests
resp = requests.get(
    "https://wadekarsupriya19.atlassian.net/rest/api/3/issue/QA-102",
    auth=("wadekar.supriya19@gmail.com", API_TOKEN),  # from .env
    headers={"Accept": "application/json"},
    timeout=15,
)
data = resp.json()
fields = data["fields"]
print(fields["summary"])
print(flatten_adf(fields["description"]))  # ADF -> text
```
> **Security rule:** the token is read from `.env` — never hardcode it in scripts or in these docs. Redacted above as `ATATT...`.

### 2.5 Minimal response shape I depend on (schema in `LLM.md`)
```json
{
  "key": "QA-102",
  "fields": {
    "summary": "…",
    "description": { "type": "doc", "content": [ … ] },
    "status": { "name": "In Progress" },
    "labels": ["…"],
    "issuetype": { "name": "Story" },
    "project": { "key": "QA" }
  }
}
```
> **Runtime note (resolved):** Python is not installed on this machine, so the deterministic `tools/` layer is implemented in **Node.js v24** (ESM, zero deps) — `tools/fetch_issue.js` and `tools/render_plan.js`. Node's global `fetch` is used for the REST calls.

> **UI runtime note (added 2026-09-03):** the Streamlit UI runs on a **bundled** Python 3.11.9 (no system Python): `C:\Users\NILESH\.lmstudio\extensions\backends\vendor\_amphibian\cpython3.11-win-x86@6\python.exe` (has `streamlit` 1.62 + `requests`). The account's Groq key exposes **14 models only** (no llama-3.3-70b). Chat-verified working: `qwen/qwen3.8-27b` (full plans, **default**, needs `max_tokens: 8192`) and `openai/gpt-oss-20b` (returned empty on long prompts).

---

## 3. Constraints discovered
1. **Only use the `AI_chapter_02_blast` folder** (per prompt) — so chapter `.env`, scripts and architecture docs live under it; do not write into `AI_chapter_01`.
2. **Do not invent ticket content.** Test-plan must be grounded in the real fetched ticket; anything unknown becomes a Gap / Question (like the VWO-49 plan's gap table).
3. **401 until the token is refreshed** — blocks Phase 2.
4. PDF generation on this machine: pandoc/wkhtmltopdf unavailable → render Markdown to styled HTML and print via headless Chrome/Edge `--print-to-pdf` (house method).
5. Jira Cloud rate limits and `Accept: application/json` are required; unknown/irrelevant fields should be excluded via the `fields` param to keep payloads small.

## 4. Where credentials live
| File | Contents |
|------|----------|
| `AI_chapter_01/Local LLM example/.env` | `JIRA_EMAIL`, `JIRA_URL`, `JIRA_API_TOKEN`, `GROQ_API_TOKEN` (existing) |
| `AI_chapter_02_blast/.env` | **(to create in Phase 2)** fresh copy with a valid token |

> Credential values intentionally redacted in this file. They are secrets.

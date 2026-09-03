# Test Plan Creator UI (Streamlit + Groq)

A web UI inside `AI_chapter_02_blast/ui/` that turns a Jira ticket key into a
**review-ready test-plan draft**: fetch the ticket from Jira (deterministic Node
tool), draft the plan with **Groq**, edit it in the browser, and export
Markdown + PDF.

## Prerequisites
- Jira credentials + `GROQ_API_TOKEN` in `AI_chapter_02_blast/.env`
  (the app also falls back to `AI_chapter_01/Local LLM example/.env` for the Groq key).
- Node.js (for the deterministic fetch + PDF HTML conversion).
- Python with `streamlit` + `requests`. On this machine there is **no system
  Python**; the app was verified with the bundled interpreter:
  `C:\Users\NILESH\.lmstudio\extensions\backends\vendor\_amphibian\cpython3.11-win-x86@6\python.exe`

## Run
```bash
cd AI_chapter_02_blast
<python> -m streamlit run ui/app.py
```
Then open the printed URL (default `http://localhost:8501`).

## Use
1. Type a Jira key, e.g. `KAN-6`.
2. Click **Create Test Plan**. The app fetches the ticket, drafts the plan via Groq, and shows it in an editable box.
3. Edit if needed, then **Export Markdown** and/or **Export PDF** — files land in `../output/Test_Plan_<KEY>.md` / `.pdf`.
4. Every export is stamped DRAFT — a human approves the plan, never the tool.

## Settings sidebar
- **Groq model** — defaults to `qwen/qwen3.8-27b` (verified on this key to produce full structured plans). `openai/gpt-oss-20b` is also listed but can return empty on long prompts.
- **Groq API key (override)** — optional; leave blank to use `.env`.

## Files
| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI + orchestration |
| `groq_client.py` | Groq chat-completions client (requests, no SDK) |
| `prompt_builder.py` | Prompt assembly from ticket + rules + checklist |
| `prompt_template.md` | Test-plan drafting rules fed to Groq |
| `export.py` | Markdown save + PDF via `../tools/md2html.js` + headless Chrome |
| `requirements.txt` | `streamlit`, `requests` |

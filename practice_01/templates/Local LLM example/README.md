# Local LLM Test Case Generator

A lightweight Streamlit tool that turns a single Jira ticket into a draft test case table. Default LLM backend is local **Ollama** (`gemma3:1b`) with automatic fallback to **Groq** when Ollama is unreachable or the user explicitly selects Groq.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Then open the printed URL (default http://localhost:8501).

> On this machine (no system Python), use the bundled interpreter:
> ```
> C:\Users\NILESH\.lmstudio\extensions\backends\vendor\_amphibian\cpython3.11-win-x86@6\python.exe -m streamlit run app.py
> ```

## Screens

- **Chat** — type `create test cases for SAM1-1` (use a real key from your Jira instance, e.g. the `SAM1` project); the app fetches the ticket from Jira, fills the template, and renders the generated test cases in the chat pane.
- **Settings** — persist Jira URL, email, API token, LLM provider, and Groq API key. Values are saved to `config.json`, seeded from `.env` on first run.

## How it works

```
chat message  ->  extract issue key  ->  Jira REST API (v3, falls back to v2)
             ->  fill templates/tc_template.md  ->  Ollama (gemma3:1b) | Groq (openai/gpt-oss-20b)
             ->  render markdown table back in chat
```

- Credentials are stored in `config.json` (gitignored) and seeded from `.env`.
- Groq is only called when Ollama is unavailable or provider is set to `groq`.
- Template: `templates/tc_template.md` — table format `| Test ID | Description | Pre-conditions | Steps | Expected Result | Priority |`.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Chat screen (entry point) |
| `pages/settings.py` | Settings screen |
| `config_store.py` | `.env` seeding + `config.json` read/write |
| `jira_client.py` | Jira REST API fetch (ADF → plain text, acceptance criteria extraction) |
| `llm_client.py` | Ollama + Groq calls with fallback |
| `templates/tc_template.md` | Sample test case prompt template |
| `requirements.txt` | Python dependencies (`streamlit`, `requests`) |
| `.gitignore` | Excludes `.env`, `config.json`, `__pycache__/`, `.venv/` |
| `.env` | Seed credentials (never written by the app) |

## Security

`.env` and `config.json` are gitignored — keep them out of version control. Do not commit credentials.

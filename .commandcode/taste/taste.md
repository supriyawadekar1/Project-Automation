# Taste

## Environment & tooling
- Works on Windows (paths like `c:\Users\...\Desktop\cypress1`); prefers PowerShell for shell commands. Confidence: 0.9
- Maintains a personal `.command code\` skill directory (SKILL.md, `references\` templates like the test-plan template, `scripts\.env`, `fetch_jira.sh`) and expects the agent to load and follow that skill's templates and guardrails (e.g., "do not invent ticket content", Human Review Gate) rather than improvising. Confidence: 0.8
- Uses JIRA (Atlassian) with API-token auth; ticket references (e.g., "VWO-49") should be sourced by fetching the actual ticket rather than fabricated. Confidence: 0.8
- On this machine pandoc/wkhtmltopdf/Python are unavailable; PDFs are produced by rendering Markdown to styled HTML and printing via headless Chrome/Edge `--print-to-pdf`. Confidence: 0.6

## Deliverables
- Wants test-plan documents (and similar artifacts) delivered as both Markdown and PDF, written into an `output` folder in the project. Confidence: 0.9

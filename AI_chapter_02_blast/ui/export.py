#!/usr/bin/env python3
"""Export helpers for the test-plan UI.

Saves the generated plan as Markdown into output/ and optionally produces a PDF
by reusing the chapter's deterministic Node tools (md2html.js) + headless Chrome.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

CHAPTER_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = CHAPTER_DIR.parent / "output"
TOOLS_DIR = CHAPTER_DIR / "tools"
TMP_DIR = CHAPTER_DIR / ".tmp"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
]


def _find_chrome() -> str | None:
    for path in CHROME_CANDIDATES:
        expanded = os.path.expandvars(path)
        if Path(expanded).exists():
            return expanded
    return None


def save_markdown(key: str, content: str) -> Path:
    """Write output/Test_Plan_<KEY>.md and return its path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"Test_Plan_{key}.md"
    out_path.write_text(content.strip() + "\n", encoding="utf-8")
    return out_path


def save_pdf(md_path: Path) -> Path | None:
    """Convert the given .md to a .pdf next to it. Returns None if no browser."""
    chrome = _find_chrome()
    if chrome is None:
        return None

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    html_path = TMP_DIR / f"{md_path.stem}.html"
    pdf_path = md_path.with_suffix(".pdf")

    node_html = subprocess.run(
        ["node", str(TOOLS_DIR / "md2html.js"), str(md_path), str(html_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if node_html.returncode != 0:
        raise RuntimeError(f"md2html failed: {node_html.stderr.strip()}")

    chrome_run = subprocess.run(
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if chrome_run.returncode != 0:
        raise RuntimeError(f"Chrome PDF failed: {chrome_run.stderr.strip()}")
    return pdf_path if pdf_path.exists() else None

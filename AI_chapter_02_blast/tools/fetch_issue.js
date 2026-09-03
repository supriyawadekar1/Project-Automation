#!/usr/bin/env node
// fetch_issue.js <ISSUE_KEY>
// Deterministic Jira fetch + normalize. Reads AI_chapter_02_blast/.env.
// Writes .tmp/<KEY>.normalized.json and prints a one-line summary.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const CHAPTER = join(HERE, "..");
const TMP = join(CHAPTER, ".tmp");

// --- .env loader (BOM-tolerant, split on FIRST =, trim spaces) ---
function loadEnv(file) {
  const out = {};
  try {
    let raw = readFileSync(file, "utf8").replace(/^\uFEFF/, "");
    for (const line of raw.split(/\r?\n/)) {
      const t = line.trim();
      if (!t || t.startsWith("#")) continue;
      const idx = t.indexOf("=");
      if (idx > 0) {
        out[t.slice(0, idx).trim()] = t.slice(idx + 1).trim();
      }
    }
  } catch (_) {
    /* missing file → empty env */
  }
  return out;
}

// --- ADF → plain text ---
function adfToText(node) {
  if (node == null) return "";
  if (typeof node === "string") return node;
  if (node.type === "text") {
    let t = node.text ?? "";
    const marks = node.marks ?? [];
    if (marks.some((m) => m.type === "code")) t = `\`${t}\``;
    if (marks.some((m) => m.type === "strong")) t = `**${t}**`;
    return t;
  }
  if (node.type === "hardBreak") return "\n";
  if (node.type === "inlineCard") return ` [${node.attrs?.url ?? ""}] `;
  let body = "";
  if (Array.isArray(node.content)) {
    body = node.content.map(adfToText).join("");
  }
  if (["paragraph", "heading", "listItem"].includes(node.type)) body += "\n";
  return body;
}

// --- Acceptance Criteria extraction (heuristic) ---
function extractAC(text) {
  if (!text) return null;
  const re = /^\s*(?:#{1,6}\s*)?(?:acceptance criteria|acceptance criterion|ac)\s*[:.\-]?\s*$/gim;
  const match = re.exec(text);
  if (!match) return null;
  const after = text.slice(match.index + match[0].length);
  const nextHead = /^\s*(?:#{1,6}\s+|[A-Z][A-Za-z ]+:$)/gim.exec(after);
  const ac = (nextHead ? after.slice(0, nextHead.index) : after).trim();
  return ac || null;
}

async function main() {
  const key = process.argv[2];
  if (!key) {
    console.error("usage: node tools/fetch_issue.js <ISSUE_KEY>");
    process.exit(2);
  }
  const env = loadEnv(join(CHAPTER, ".env"));
  const { JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN } = env;
  if (!JIRA_URL || !JIRA_EMAIL || !JIRA_API_TOKEN) {
    console.error("ERROR: JIRA_URL / JIRA_EMAIL / JIRA_API_TOKEN missing in .env");
    process.exit(1);
  }
  const base = JIRA_URL.replace(/\/+$/, "");
  const fields =
    "summary,description,status,labels,issuetype,project";
  const url = `${base}/rest/api/3/issue/${encodeURIComponent(key)}?fields=${fields}`;
  const auth = Buffer.from(`${JIRA_EMAIL}:${JIRA_API_TOKEN}`).toString("base64");

  let resp;
  try {
    resp = await fetch(url, {
      headers: { Accept: "application/json", Authorization: `Basic ${auth}` },
    });
  } catch (e) {
    console.error("ERROR: network failure:", e.message);
    process.exit(1);
  }

  if (resp.status === 401 || resp.status === 403) {
    console.error("ERROR: Jira auth failed (401/403). Refresh token in Atlassian → .env");
    process.exit(1);
  }
  if (resp.status === 404) {
    console.error(`ERROR: Jira issue '${key}' not found (404).`);
    process.exit(1);
  }
  if (!resp.ok) {
    console.error(`ERROR: Jira returned HTTP ${resp.status}`);
    process.exit(1);
  }

  const data = await resp.json();
  const f = data.fields || {};
  const description = adfToText(f.description).replace(/\n{3,}/g, "\n\n").trim();

  const norm = {
    key: data.key || key,
    summary: (f.summary || "").trim(),
    type: f.issuetype?.name || "",
    project: f.project?.name || "",
    projectKey: f.project?.key || "",
    status: f.status?.name || "",
    labels: Array.isArray(f.labels) ? f.labels : [],
    url: base + "/browse/" + (data.key || key),
    description,
    acceptance_criteria: extractAC(description),
  };

  mkdirSync(TMP, { recursive: true });
  const outFile = join(TMP, `${norm.key}.normalized.json`);
  writeFileSync(outFile, JSON.stringify(norm, null, 2), "utf8");
  console.log(
    `OK ${norm.key} [${norm.type}] "${norm.summary}" status=${norm.status} ` +
      `desc=${norm.description.length}ch ac=${norm.acceptance_criteria ? "yes" : "null"} -> ${outFile}`
  );
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});

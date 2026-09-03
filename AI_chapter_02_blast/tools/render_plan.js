#!/usr/bin/env node
// render_plan.js <ISSUE_KEY> <SEED_JSON>
// Deterministic Markdown renderer. Reads .tmp/<KEY>.normalized.json (ticket facts)
// + SEED_JSON (LLM-authored draft) and writes output/Test_Plan_<KEY>.md.
// Never invents content: absent seed fields become explicit TBD markers.

import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const CHAPTER = join(HERE, "..");
const TMP = join(CHAPTER, ".tmp");
const OUT = join(CHAPTER, "..", "output");

function die(msg) {
  console.error("ERROR:", msg);
  process.exit(1);
}

const fmtList = (arr) =>
  Array.isArray(arr) && arr.length ? arr.map((s) => `- ${s}`).join("\n") : "TBD";

const esc = (s) =>
  String(s ?? "").replace(/\|/g, "\\|").replace(/\n/g, " ").trim();

async function main() {
  const key = process.argv[2];
  const seedPath = process.argv[3];
  if (!key || !seedPath) die("usage: node tools/render_plan.js <KEY> <seed.json>");
  if (!existsSync(seedPath)) die(`seed file not found: ${seedPath}`);

  const normPath = join(TMP, `${key}.normalized.json`);
  if (!existsSync(normPath)) die(`normalized file not found: ${normPath} — run fetch_issue.js first`);
  const t = JSON.parse(readFileSync(normPath, "utf8"));
  const s = JSON.parse(readFileSync(seedPath, "utf8"));

  // ---- helpers to stay schema-safe ----
  const g = (obj, key2) => (obj && obj[key2]) ?? [];
  const arr = (v) => (Array.isArray(v) ? v : []);
  const scope = s.scope_and_objectives ?? {};
  const gaps = arr(s.gaps_and_questions);
  const scenarios = arr(s.test_scenarios);
  const data = s.test_data_and_env ?? {};
  const risks = s.risks_and_assumptions ?? {};
  const entryExit = s.entry_exit_criteria ?? {};
  const gate = s.human_review_gate ?? {};

  // ---- header ----
  const L = [];
  L.push(`# Test Plan — ${key}: ${esc(t.summary)}`);
  L.push("");
  L.push(`> Status: **${esc(s.status ?? "DRAFT — pending human review")}**`);
  L.push(`> Author: ${esc(s.author ?? "QA")}`);
  L.push(`> Source ticket: [${key}](${t.url}) — ${esc(t.type)} in "${esc(t.project)}" (status: ${esc(t.status)})`);
  L.push("");
  if (esc(scope.objective ?? s.objective)) {
    L.push(`**Objective:** ${esc(scope.objective ?? s.objective)}`);
    L.push("");
  }

  // ---- 1. Scope ----
  L.push("## 1. Scope & Objectives");
  L.push("");
  L.push("- **In scope:**");
  L.push(fmtList(g(scope, "in_scope")));
  L.push("- **Out of scope:**");
  L.push(fmtList(g(scope, "out_of_scope")));
  L.push("");
  if (!arr(g(scope, "in_scope")).length) L.push("<!-- TBD: no in-scope items supplied in seed -->");

  // ---- 2. Gaps ----
  L.push("## 2. Gaps & Questions for the author");
  L.push("");
  if (gaps.length) {
    L.push("| # | Area | Finding (⚠️/❌) | Question to author |");
    L.push("|---|------|----------------|--------------------|");
    gaps.forEach((g2, i) => {
      L.push(`| ${i + 1} | ${esc(g2.area)} | ${esc(g2.finding)} | ${esc(g2.question)} |`);
    });
  } else {
    L.push("_No gaps identified._");
  }
  L.push("");

  // ---- 3. Scenarios ----
  L.push("## 3. Test Scenarios");
  L.push("");
  if (scenarios.length) {
    L.push("| ID | Priority | Type (pos/neg/boundary) | Scenario | Maps to (AC / gap) |");
    L.push("|----|----------|-------------------------|----------|--------------------|");
    scenarios.forEach((sc) => {
      L.push(
        `| ${esc(sc.id)} | ${esc(sc.priority)} | ${esc(sc.type)} | ${esc(sc.scenario)} | ${esc(sc.maps_to ?? "")} |`
      );
    });
  } else {
    L.push("_No test scenarios supplied._");
  }
  L.push("");

  // ---- 4. Data & Env ----
  L.push("## 4. Test Data & Environment");
  L.push("");
  L.push("- **Data:**");
  L.push(fmtList(g(data, "data")));
  L.push("- **Environment / flags:**");
  L.push(fmtList(g(data, "environment")));
  L.push("- **Roles / permissions:**");
  L.push(fmtList(g(data, "roles")));
  L.push("");

  // ---- 5. Risks ----
  L.push("## 5. Risks & Assumptions");
  L.push("");
  L.push("- **Assumptions made:**");
  L.push(fmtList(g(risks, "assumptions")));
  L.push("- **Risks:**");
  L.push(fmtList(g(risks, "risks")));
  L.push("");

  // ---- 6. Entry/Exit ----
  L.push("## 6. Entry / Exit criteria");
  L.push("");
  L.push("- **Entry:**");
  L.push(fmtList(g(entryExit, "entry")));
  L.push("- **Exit:**");
  L.push(fmtList(g(entryExit, "exit")));
  L.push("");

  // ---- Human review gate ----
  L.push("---");
  L.push("## HUMAN REVIEW GATE");
  L.push("");
  L.push("- **I assumed:**");
  L.push(fmtList(g(gate, "assumed")));
  L.push("- **I could not confirm:**");
  L.push(fmtList(g(gate, "could_not_confirm")));
  L.push("- **Open questions blocking sign-off:**");
  L.push(fmtList(g(gate, "open_questions")));
  L.push("");
  L.push("- ▶ **Approve, or edit, before I write test cases / automation.**");

  mkdirSync(OUT, { recursive: true });
  const outFile = join(OUT, `Test_Plan_${key}.md`);
  writeFileSync(outFile, L.join("\n"), "utf8");
  console.log(`WROTE ${outFile}`);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});

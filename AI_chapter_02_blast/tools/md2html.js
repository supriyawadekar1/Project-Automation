#!/usr/bin/env node
// md2html.js <INPUT.md> <OUTPUT.html>  — minimal, dependency-free Markdown→HTML
// Supports the subset used by the test-plan renderer: #/##/### headers, blockquote
// lines, bullet lists, pipe tables, hr, and bare paragraphs. Everything else is escaped.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

const esc = (s) =>
  s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

// Inline: **bold**, `code`, [text](url)
function inline(s) {
  let out = esc(s);
  out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/`([^`]+)`/g, "<code>$1</code>");
  out = out.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2">$1</a>');
  return out;
}

function mdToHtml(md) {
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const H = [];
  let i = 0;
  const block = (open, close) => (H.push(open), i);

  while (i < lines.length) {
    const line = lines[i];
    const t = line.trim();

    // blank
    if (!t) { i++; continue; }

    // heading
    const h = /^(#{1,6})\s+(.*)$/.exec(t);
    if (h) {
      H.push(`<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`);
      i++; continue;
    }

    // hr
    if (/^-{3,}$/.test(t)) { H.push("<hr>"); i++; continue; }

    // blockquote lines
    if (t.startsWith(">")) {
      const buf = [];
      while (i < lines.length && lines[i].trim().startsWith(">")) {
        buf.push(inline(lines[i].trim().replace(/^>\s?/, "")));
        i++;
      }
      H.push(`<blockquote>${buf.join("<br>")}</blockquote>`);
      continue;
    }

    // bullet list (loose: gather contiguous - items)
    if (/^[-*]\s+/.test(t)) {
      const buf = [];
      while (i < lines.length && /^[-*]\s+/.test(lines[i].trim())) {
        buf.push(`<li>${inline(lines[i].trim().replace(/^[-*]\s+/, ""))}</li>`);
        i++;
      }
      H.push(`<ul>${buf.join("")}</ul>`);
      continue;
    }

    // pipe table: header row, separator row, then data rows until non-| or blank
    if (t.includes("|") && i + 1 < lines.length && /^\s*\|?[\s:|-]+\|?\s*$/.test(lines[i + 1])) {
      const parseRow = (r) =>
        r
          .trim()
          .replace(/^\|/, "")
          .replace(/\|$/, "")
          .split("|")
          .map((c) => inline(c.trim()));
      const head = parseRow(t);
      i += 2; // skip header + separator
      const body = [];
      while (i < lines.length && lines[i].trim().includes("|")) {
        body.push(`<tr>${parseRow(lines[i]).map((c) => `<td>${c}</td>`).join("")}</tr>`);
        i++;
      }
      H.push(
        `<table><thead><tr>${head.map((c) => `<th>${c}</th>`).join("")}</tr></thead>` +
          `<tbody>${body.join("")}</tbody></table>`
      );
      continue;
    }

    // paragraph (accumulate until blank / block start)
    const para = [t];
    i++;
    while (
      i < lines.length &&
      lines[i].trim() &&
      !/^(#{1,6})\s/.test(lines[i]) &&
      !/^[-*]\s/.test(lines[i]) &&
      !/^>/.test(lines[i]) &&
      !/^\|/.test(lines[i])
    ) {
      para.push(lines[i].trim());
      i++;
    }
    H.push(`<p>${inline(para.join(" "))}</p>`);
  }
  return H.join("\n");
}

const input = process.argv[2];
const output = process.argv[3];
if (!input || !output) {
  console.error("usage: node tools/md2html.js <in.md> <out.html>");
  process.exit(2);
}
const md = readFileSync(input, "utf8");
const body = mdToHtml(md);
const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Test Plan</title>
<style>
  body { font-family: "Segoe UI", Arial, sans-serif; color: #1a1a1a; margin: 32px auto; max-width: 960px; padding: 0 24px; line-height: 1.5; }
  h1 { border-bottom: 3px solid #2c5aa0; padding-bottom: 8px; color: #2c5aa0; }
  h2 { border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 28px; color: #2c5aa0; }
  h3 { color: #333; }
  blockquote { background: #f4f6fa; border-left: 4px solid #2c5aa0; margin: 12px 0; padding: 8px 14px; color: #333; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 13px; }
  th, td { border: 1px solid #ccc; padding: 6px 9px; text-align: left; vertical-align: top; }
  th { background: #eef2f8; }
  tr:nth-child(even) td { background: #fafbfd; }
  ul { margin: 6px 0 12px; }
  li { margin: 2px 0; }
  code { background: #f2f2f2; padding: 1px 4px; border-radius: 3px; font-size: 90%; }
  a { color: #2c5aa0; text-decoration: none; }
  strong { color: #111; }
  hr { border: none; border-top: 2px solid #2c5aa0; margin: 24px 0; }
</style>
</head>
<body>
${body}
</body>
</html>
`;
mkdirSync(dirname(output), { recursive: true });
writeFileSync(output, html, "utf8");
console.log("WROTE " + output);

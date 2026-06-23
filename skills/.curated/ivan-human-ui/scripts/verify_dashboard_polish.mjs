#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const htmlPath = process.argv[2];
if (!htmlPath) {
  console.error("Usage: node verify_dashboard_polish.mjs <path/to/index.html>");
  process.exit(2);
}

const abs = path.resolve(htmlPath);
if (!fs.existsSync(abs)) {
  console.error(`Input file not found: ${abs}`);
  process.exit(2);
}

const html = fs.readFileSync(abs, "utf8");
const baseDir = path.dirname(abs);
const failures = [];

function requirePattern(pattern, message) {
  if (!pattern.test(html)) failures.push(message);
}

requirePattern(/data-layout=["']split["']/i, "Hero split layout missing.");
requirePattern(
  /data-ratio=["']3-5:2-5["']/i,
  "Hero ratio 3/5 and 2/5 missing.",
);
requirePattern(
  /data-heading-align=["']left["']/i,
  "Section heading left alignment signal missing.",
);
requirePattern(/data-gap=["']8["']/i, "8px spacing rhythm signal missing.");
requirePattern(
  /data-ring=["']outer-10["']/i,
  "Outer ring 10% treatment signal missing.",
);
requirePattern(
  /data-palette=["']neutral["']/i,
  "Neutral palette signal missing.",
);

if (/indigo|emerald|purple/i.test(html)) {
  failures.push("Disallowed palette tokens found: indigo/emerald/purple.");
}

const shotMatch = html.match(/data-screenshot=["']([^"']+)["']/i);
if (!shotMatch) {
  failures.push("Screenshot reference is missing.");
} else {
  const shotPath = shotMatch[1];
  if (/^https?:\/\//i.test(shotPath)) {
    failures.push("Screenshot must be a local asset, not remote URL.");
  } else {
    const resolved = path.resolve(baseDir, shotPath);
    if (!fs.existsSync(resolved)) {
      failures.push(`Screenshot asset missing: ${shotPath}`);
    }
  }
}

if (failures.length > 0) {
  for (const f of failures) console.error(`FAIL: ${f}`);
  process.exit(1);
}

console.log(
  "PASS: dashboard polish constraints satisfied (layout, palette, spacing, ring, screenshot asset).",
);

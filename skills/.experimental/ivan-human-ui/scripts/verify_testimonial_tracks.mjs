#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function fail(message) {
  console.error(`FAIL: ${message}`);
}

function normalizePath(input) {
  if (input.startsWith("http://") || input.startsWith("https://")) {
    return null;
  }
  return input;
}

const htmlPath = process.argv[2];
if (!htmlPath) {
  console.error("Usage: node verify_testimonial_tracks.mjs <path/to/index.html>");
  process.exit(2);
}

const absHtmlPath = path.resolve(htmlPath);
if (!fs.existsSync(absHtmlPath)) {
  console.error(`Input file not found: ${absHtmlPath}`);
  process.exit(2);
}

const html = fs.readFileSync(absHtmlPath, "utf8");
const htmlDir = path.dirname(absHtmlPath);
const requiredTracks = ["animal", "abstract", "business"];

const cardRegex = /<article\b([^>]*\bdata-track=["'][^"']+["'][^>]*)>/gi;
const cards = [];
let match;
while ((match = cardRegex.exec(html)) !== null) {
  cards.push(match[1]);
}

const findings = [];
if (cards.length === 0) {
  findings.push("No testimonial cards with data-track were found.");
}

const seenTracks = new Set();
for (const attrs of cards) {
  const trackMatch = attrs.match(/\bdata-track=["']([^"']+)["']/i);
  const bgMatch = attrs.match(/\bdata-bg=["']([^"']+)["']/i);
  const styleMatch = attrs.match(/\bstyle=["']([^"']+)["']/i);
  if (!trackMatch) {
    findings.push(`Card missing data-track: <article ${attrs}>`);
    continue;
  }
  const track = trackMatch[1].toLowerCase();
  seenTracks.add(track);

  if (!requiredTracks.includes(track)) {
    findings.push(`Unexpected track value: ${track}`);
  }

  if (!bgMatch) {
    findings.push(`Track "${track}" missing data-bg attribute.`);
  } else {
    const bgValue = bgMatch[1].trim();
    const normalized = normalizePath(bgValue);
    if (!normalized) {
      findings.push(`Track "${track}" uses remote URL; local stable file is required: ${bgValue}`);
    } else {
      const ext = path.extname(normalized).toLowerCase();
      if (![".png", ".jpg", ".jpeg", ".webp", ".svg"].includes(ext)) {
        findings.push(`Track "${track}" has unsupported extension: ${normalized}`);
      }
      const resolved = path.resolve(htmlDir, normalized);
      if (!fs.existsSync(resolved)) {
        findings.push(`Track "${track}" asset missing: ${normalized}`);
      }
    }
  }

  if (styleMatch) {
    const style = styleMatch[1].toLowerCase();
    if (
      style.includes("display:none") ||
      style.includes("visibility:hidden") ||
      style.includes("opacity:0")
    ) {
      findings.push(`Track "${track}" is visually hidden via inline style: ${styleMatch[1]}`);
    }
  }
}

for (const track of requiredTracks) {
  if (!seenTracks.has(track)) {
    findings.push(`Required track missing from markup: ${track}`);
  }
}

if (findings.length > 0) {
  for (const line of findings) {
    fail(line);
  }
  process.exit(1);
}

console.log(
  "PASS: all required tracks render constraints are satisfied (animal, abstract, business).",
);

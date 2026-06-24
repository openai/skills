#!/usr/bin/env node
// Shadow Tutor — thin read/write/validate script for the user knowledge profile.
// Deliberately thin: its only job is to keep ~/.shadow-tutor/knowledge.json from being
// corrupted by the model.
//
// Usage:
//   node knowledge.mjs get                      print the current profile (empty profile if none)
//   node knowledge.mjs init '<json>'            initialize from calibration (refuses if exists, unless --force)
//   node knowledge.mjs update '<json>'          merge-update the state/confidence of some concepts
//   node knowledge.mjs validate '<json>'        validate only, no write — for the model to self-check
//
// Concept state machine: unknown -> introduced -> learning -> mastered
//
// update input looks like:
//   { "concepts": { "react.useMemo": { "state": "learning", "confidence": 0.6,
//                                       "note": "can explain but didn't write it solo" } } }

import { readFileSync, writeFileSync, mkdirSync, existsSync, renameSync } from "node:fs";
import { homedir } from "node:os";
import { join, dirname } from "node:path";

const DIR = join(homedir(), ".shadow-tutor");
const FILE = join(DIR, "knowledge.json");
const SCHEMA_VERSION = 1;
const STATES = ["unknown", "introduced", "learning", "mastered"];

function emptyProfile() {
  return { version: SCHEMA_VERSION, concepts: {}, meta: { createdAt: null, updatedAt: null } };
}

function load() {
  if (!existsSync(FILE)) return emptyProfile();
  try {
    const p = JSON.parse(readFileSync(FILE, "utf8"));
    validateProfile(p); // validate even our own on-disk data; throw if corrupt
    return p;
  } catch (e) {
    throw new Error(`Existing profile is unparseable/invalid (${FILE}): ${e.message}. Please inspect manually to avoid losing data.`);
  }
}

// ---- validation: the model may write garbage; this is the only line of defense ----
function validateProfile(p) {
  if (typeof p !== "object" || p === null) throw new Error("profile must be an object");
  if (p.version !== SCHEMA_VERSION) throw new Error(`version must be ${SCHEMA_VERSION}`);
  if (typeof p.concepts !== "object" || p.concepts === null) throw new Error("concepts must be an object");
  for (const [id, c] of Object.entries(p.concepts)) validateConcept(id, c);
  return p;
}

function validateConcept(id, c) {
  if (!/^[a-z0-9][a-z0-9._-]{0,80}$/i.test(id)) throw new Error(`invalid concept id: ${id}`);
  if (typeof c !== "object" || c === null) throw new Error(`concept ${id} must be an object`);
  if (!STATES.includes(c.state)) throw new Error(`concept ${id} has invalid state: ${c.state} (expected ${STATES.join("/")})`);
  if (typeof c.confidence !== "number" || c.confidence < 0 || c.confidence > 1)
    throw new Error(`concept ${id} confidence must be 0..1`);
  if (c.note != null && typeof c.note !== "string") throw new Error(`concept ${id} note must be a string`);
}

function parseArg(raw, label) {
  if (!raw) throw new Error(`${label} requires a JSON argument`);
  let obj;
  try { obj = JSON.parse(raw); } catch (e) { throw new Error(`${label} JSON parse failed: ${e.message}`); }
  return obj;
}

function atomicWrite(profile) {
  validateProfile(profile);
  mkdirSync(dirname(FILE), { recursive: true });
  const now = new Date().toISOString();
  profile.meta ??= {};
  profile.meta.createdAt ??= now;
  profile.meta.updatedAt = now;
  const tmp = FILE + ".tmp";
  writeFileSync(tmp, JSON.stringify(profile, null, 2) + "\n", "utf8");
  renameSync(tmp, FILE); // atomic replace, avoids half-written files
}

// ---- subcommands ----
function cmdGet() {
  process.stdout.write(JSON.stringify(load(), null, 2) + "\n");
}

function cmdInit(raw, force) {
  if (existsSync(FILE) && !force) throw new Error(`profile already exists (${FILE}). Pass --force to overwrite.`);
  const incoming = parseArg(raw, "init");
  const p = emptyProfile();
  for (const [id, c] of Object.entries(incoming.concepts ?? {})) {
    p.concepts[id] = normalizeConcept(c);
  }
  atomicWrite(p);
  process.stdout.write(`Initialized profile with ${Object.keys(p.concepts).length} concept(s).\n`);
}

function cmdUpdate(raw) {
  const incoming = parseArg(raw, "update");
  if (typeof incoming.concepts !== "object" || incoming.concepts === null)
    throw new Error("update input must contain a concepts object");
  const p = load();
  let n = 0;
  for (const [id, c] of Object.entries(incoming.concepts)) {
    p.concepts[id] = { ...(p.concepts[id] ?? {}), ...normalizeConcept(c, p.concepts[id]) };
    n++;
  }
  atomicWrite(p);
  process.stdout.write(`Updated ${n} concept(s).\n`);
}

function cmdValidate(raw) {
  const incoming = parseArg(raw, "validate");
  // supports validating either a whole profile or a bag of concepts
  if (incoming.version != null) validateProfile(incoming);
  else for (const [id, c] of Object.entries(incoming.concepts ?? {})) validateConcept(id, normalizeConcept(c));
  process.stdout.write("OK: valid.\n");
}

function normalizeConcept(c, prev) {
  const out = {
    state: c.state ?? prev?.state ?? "introduced",
    confidence: c.confidence ?? prev?.confidence ?? 0.3,
    lastSeen: new Date().toISOString(),
  };
  if (c.note != null) out.note = c.note;
  else if (prev?.note != null) out.note = prev.note;
  validateConcept("x", out);
  return out;
}

function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const force = rest.includes("--force");
  const arg = rest.find((a) => !a.startsWith("--"));
  try {
    switch (cmd) {
      case "get": return cmdGet();
      case "init": return cmdInit(arg, force);
      case "update": return cmdUpdate(arg);
      case "validate": return cmdValidate(arg);
      default:
        process.stderr.write("usage: knowledge.mjs <get|init|update|validate> [json] [--force]\n");
        process.exit(2);
    }
  } catch (e) {
    process.stderr.write(`error: ${e.message}\n`);
    process.exit(1);
  }
}

main();

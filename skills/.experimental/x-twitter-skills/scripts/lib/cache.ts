/**
 * Simple file-based cache for X API results.
 */

import {
  existsSync,
  mkdirSync,
  readFileSync,
  writeFileSync,
  readdirSync,
  statSync,
  unlinkSync,
} from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import { createHash } from "crypto";
import type { Tweet } from "./api";

const THIS_DIR = dirname(fileURLToPath(import.meta.url));
const CACHE_DIR = join(THIS_DIR, "..", "..", "data", "cache");
const DEFAULT_TTL_MS = 15 * 60 * 1000;

function ensureDir() {
  if (!existsSync(CACHE_DIR)) mkdirSync(CACHE_DIR, { recursive: true });
}

function cacheKey(query: string, params: string = ""): string {
  return createHash("md5").update(`${query}|${params}`).digest("hex").slice(0, 12);
}

interface CacheEntry {
  query: string;
  params: string;
  timestamp: number;
  tweets: Tweet[];
}

export function get(query: string, params: string = "", ttlMs: number = DEFAULT_TTL_MS): Tweet[] | null {
  ensureDir();
  const path = join(CACHE_DIR, `${cacheKey(query, params)}.json`);
  if (!existsSync(path)) return null;

  try {
    const entry: CacheEntry = JSON.parse(readFileSync(path, "utf-8"));
    if (Date.now() - entry.timestamp > ttlMs) {
      unlinkSync(path);
      return null;
    }
    return entry.tweets;
  } catch {
    return null;
  }
}

export function set(query: string, params: string = "", tweets: Tweet[]): void {
  ensureDir();
  const path = join(CACHE_DIR, `${cacheKey(query, params)}.json`);
  const entry: CacheEntry = {
    query,
    params,
    timestamp: Date.now(),
    tweets,
  };
  writeFileSync(path, JSON.stringify(entry, null, 2));
}

export function prune(ttlMs: number = DEFAULT_TTL_MS): number {
  ensureDir();
  let removed = 0;

  for (const file of readdirSync(CACHE_DIR).filter((f) => f.endsWith(".json"))) {
    const path = join(CACHE_DIR, file);
    try {
      if (Date.now() - statSync(path).mtimeMs > ttlMs) {
        unlinkSync(path);
        removed++;
      }
    } catch {
      // Ignore per-file errors.
    }
  }

  return removed;
}

export function clear(): number {
  ensureDir();
  const files = readdirSync(CACHE_DIR).filter((f) => f.endsWith(".json"));
  for (const file of files) {
    try {
      unlinkSync(join(CACHE_DIR, file));
    } catch {
      // Ignore per-file errors.
    }
  }
  return files.length;
}

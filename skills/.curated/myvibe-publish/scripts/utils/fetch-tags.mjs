#!/usr/bin/env node

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import crypto from "node:crypto";
import chalk from "chalk";

import { VIBE_HUB_URL_DEFAULT, isMainModule } from "./constants.mjs";

// Cache configuration
const CACHE_DIR = join(homedir(), ".myvibe", "cache");
const CACHE_EXPIRY_DAYS = 7;

// Tag types to fetch
const TAG_TYPES = ["platform", "tech-stack", "model", "category"];

/**
 * Get cache file path for a hub URL
 * @param {string} hubUrl - Hub URL
 * @returns {string} Cache file path
 */
function getCacheFilePath(hubUrl) {
  const hash = crypto.createHash("md5").update(hubUrl).digest("hex").substring(0, 8);
  return join(CACHE_DIR, `tags-${hash}.json`);
}

/**
 * Ensure cache directory exists
 */
function ensureCacheDir() {
  if (!existsSync(CACHE_DIR)) {
    mkdirSync(CACHE_DIR, { recursive: true });
  }
}

/**
 * Check if cache is valid
 * @param {Object} cache - Cache object
 * @returns {boolean} True if cache is valid
 */
function isCacheValid(cache) {
  if (!cache || !cache.expiresAt) {
    return false;
  }
  return new Date(cache.expiresAt) > new Date();
}

/**
 * Load cache from file
 * @param {string} hubUrl - Hub URL
 * @returns {Object|null} Cache object or null
 */
function loadCache(hubUrl) {
  const cacheFile = getCacheFilePath(hubUrl);
  if (!existsSync(cacheFile)) {
    return null;
  }

  try {
    const content = readFileSync(cacheFile, "utf-8");
    return JSON.parse(content);
  } catch {
    return null;
  }
}

/**
 * Save cache to file
 * @param {string} hubUrl - Hub URL
 * @param {Object} tags - Tags object
 */
function saveCache(hubUrl, tags) {
  ensureCacheDir();
  const cacheFile = getCacheFilePath(hubUrl);

  const now = new Date();
  const expiresAt = new Date(now.getTime() + CACHE_EXPIRY_DAYS * 24 * 60 * 60 * 1000);

  const cache = {
    hub: hubUrl,
    fetchedAt: now.toISOString(),
    expiresAt: expiresAt.toISOString(),
    tags,
  };

  writeFileSync(cacheFile, JSON.stringify(cache, null, 2));
}

/**
 * Fetch tags from API
 * @param {string} hubUrl - Hub URL
 * @param {string} type - Tag type
 * @returns {Promise<Array>} Tags array
 */
async function fetchTagsByType(hubUrl, type) {
  const { origin } = new URL(hubUrl);
  const url = `${origin}/api/tags?type=${type}&isActive=true`;

  const response = await fetch(url, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch ${type} tags: ${response.status} ${response.statusText}`);
  }

  const result = await response.json();
  return result.data || [];
}

/**
 * Fetch all tags from API
 * @param {string} hubUrl - Hub URL
 * @returns {Promise<Object>} Tags object by type
 */
async function fetchAllTags(hubUrl) {
  const tags = {};

  for (const type of TAG_TYPES) {
    try {
      tags[type] = await fetchTagsByType(hubUrl, type);
    } catch (error) {
      console.error(chalk.yellow(`Warning: Failed to fetch ${type} tags: ${error.message}`));
      tags[type] = [];
    }
  }

  return tags;
}

/**
 * Get tags (from cache or fetch)
 * @param {Object} options - Options
 * @param {string} [options.hub] - Hub URL
 * @param {boolean} [options.refresh] - Force refresh cache
 * @param {boolean} [options.silent] - Suppress console output
 * @returns {Promise<Object>} Tags result
 */
export async function getTags(options = {}) {
  const { hub = VIBE_HUB_URL_DEFAULT, refresh = false, silent = false } = options;

  const log = silent ? () => {} : console.error.bind(console);

  // Try to load from cache first
  if (!refresh) {
    const cache = loadCache(hub);
    if (cache && isCacheValid(cache)) {
      log(chalk.gray(`Using cached tags (expires: ${cache.expiresAt})`));
      return {
        success: true,
        fromCache: true,
        hub: cache.hub,
        fetchedAt: cache.fetchedAt,
        expiresAt: cache.expiresAt,
        tags: cache.tags,
      };
    }
  }

  // Fetch from API
  log(chalk.cyan(`Fetching tags from ${hub}...`));

  try {
    const tags = await fetchAllTags(hub);

    // Save to cache
    saveCache(hub, tags);
    log(chalk.green(`Tags cached for ${CACHE_EXPIRY_DAYS} days`));

    const cache = loadCache(hub);
    return {
      success: true,
      fromCache: false,
      hub: cache.hub,
      fetchedAt: cache.fetchedAt,
      expiresAt: cache.expiresAt,
      tags: cache.tags,
    };
  } catch (error) {
    // Try to use expired cache as fallback
    const expiredCache = loadCache(hub);
    if (expiredCache) {
      log(chalk.yellow(`Failed to fetch tags, using expired cache`));
      return {
        success: true,
        fromCache: true,
        expired: true,
        hub: expiredCache.hub,
        fetchedAt: expiredCache.fetchedAt,
        expiresAt: expiredCache.expiresAt,
        tags: expiredCache.tags,
      };
    }

    return {
      success: false,
      error: error.message,
    };
  }
}

/**
 * Parse command line arguments
 */
function parseArgs(args) {
  const options = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    switch (arg) {
      case "--hub":
      case "-h":
        options.hub = nextArg;
        i++;
        break;
      case "--refresh":
      case "-r":
        options.refresh = true;
        break;
      case "--help":
        printHelp();
        process.exit(0);
        break;
    }
  }

  return options;
}

/**
 * Print help message
 */
function printHelp() {
  console.log(`
${chalk.bold("MyVibe Tags Fetcher")}

Fetch and cache available tags from MyVibe.

${chalk.bold("Usage:")}
  node fetch-tags.mjs [options]

${chalk.bold("Options:")}
  --hub, -h <url>    MyVibe URL (default: ${VIBE_HUB_URL_DEFAULT})
  --refresh, -r      Force refresh cache (ignore expiry)
  --help             Show this help message

${chalk.bold("Cache:")}
  Location: ~/.myvibe/cache/tags-{hash}.json
  Expiry: ${CACHE_EXPIRY_DAYS} days

${chalk.bold("Output:")}
  JSON object with tags grouped by type (platform, tech-stack, model, category)

${chalk.bold("Examples:")}
  # Get cached tags (or fetch if expired)
  node fetch-tags.mjs

  # Force refresh cache
  node fetch-tags.mjs --refresh

  # Use specific hub
  node fetch-tags.mjs --hub https://myvibe.example.com
`);
}

// CLI entry point
if (isMainModule(import.meta.url)) {
  const args = process.argv.slice(2);
  const options = parseArgs(args);

  getTags({ ...options, silent: false })
    .then((result) => {
      // Output JSON to stdout for AI to parse
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    })
    .catch((error) => {
      console.error(chalk.red(`Fatal error: ${error.message}`));
      process.exit(1);
    });
}

export default getTags;

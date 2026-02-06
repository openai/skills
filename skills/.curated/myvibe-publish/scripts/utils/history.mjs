import { readFile, writeFile, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join, dirname } from "node:path";
import yaml from "js-yaml";

const HISTORY_DIR = join(homedir(), ".myvibe");
const HISTORY_FILE = join(HISTORY_DIR, "published.yaml");

/**
 * Ensure the history directory exists
 */
async function ensureHistoryDir() {
  if (!existsSync(HISTORY_DIR)) {
    await mkdir(HISTORY_DIR, { recursive: true });
  }
}

/**
 * Load publish history from file
 * @returns {Promise<Object>} History data with mappings
 */
async function loadHistory() {
  try {
    if (!existsSync(HISTORY_FILE)) {
      return { mappings: {} };
    }
    const content = await readFile(HISTORY_FILE, "utf-8");
    const data = yaml.load(content);
    return data || { mappings: {} };
  } catch {
    return { mappings: {} };
  }
}

/**
 * Save publish history to file
 * @param {Object} history - History data to save
 */
async function saveHistory(history) {
  await ensureHistoryDir();
  const content = yaml.dump(history, { indent: 2, lineWidth: -1 });
  await writeFile(HISTORY_FILE, content, "utf-8");
}

/**
 * Get publish history for a source path and hub
 * @param {string} sourcePath - Absolute path to source (file or directory)
 * @param {string} hubUrl - MyVibe hub URL
 * @returns {Promise<{did: string, lastPublished: string, title: string} | null>}
 */
export async function getPublishHistory(sourcePath, hubUrl) {
  const history = await loadHistory();
  const { origin } = new URL(hubUrl);

  const pathMappings = history.mappings[sourcePath];
  if (!pathMappings) {
    return null;
  }

  const hubMapping = pathMappings[origin];
  if (!hubMapping) {
    return null;
  }

  return hubMapping;
}

/**
 * Save publish history for a source path and hub
 * @param {string} sourcePath - Absolute path to source (file or directory)
 * @param {string} hubUrl - MyVibe hub URL
 * @param {string} did - Vibe DID
 * @param {string} title - Vibe title (optional)
 */
export async function savePublishHistory(sourcePath, hubUrl, did, title = "") {
  const history = await loadHistory();
  const { origin } = new URL(hubUrl);

  if (!history.mappings[sourcePath]) {
    history.mappings[sourcePath] = {};
  }

  history.mappings[sourcePath][origin] = {
    did,
    lastPublished: new Date().toISOString(),
    ...(title && { title }),
  };

  await saveHistory(history);
}

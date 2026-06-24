import { access, rm } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import createSecretStore, { FileStore } from "@aigne/secrets";

const CONFIG_FILENAME = "myvibe-connected.yaml";
const SERVICE_NAME = "myvibe-publish";

/**
 * Create a secret store for storing access tokens
 * Uses system keyring when available, falls back to file storage
 */
export async function createStore() {
  const filepath = join(homedir(), ".aigne", CONFIG_FILENAME);
  const secretStore = await createSecretStore({
    filepath,
    serviceName: SERVICE_NAME,
  });

  /**
   * Migrate from file store to keyring if needed
   */
  async function migrate() {
    // System doesn't support keyring
    if (secretStore instanceof FileStore) {
      return true;
    }
    // Check if file exists (needs migration)
    try {
      await access(filepath);
    } catch {
      // File doesn't exist, no migration needed
      return true;
    }

    // Migrate from file to keyring
    const fileStore = new FileStore({ filepath });
    const map = await fileStore.listMap();
    for (const [key, value] of Object.entries(map)) {
      await secretStore.setItem(key, value);
    }
    // Remove old file after migration
    await rm(filepath);
  }

  /**
   * Clear all stored tokens
   */
  async function clear() {
    const map = await secretStore.listMap();
    for (const key of Object.keys(map)) {
      await secretStore.deleteItem(key);
    }
  }

  /**
   * Clear token for a specific hostname
   */
  async function clearHost(hostname) {
    try {
      await secretStore.deleteItem(hostname);
    } catch {
      // Ignore if item doesn't exist
    }
  }

  await migrate();

  // Add custom methods
  secretStore.clear = clear;
  secretStore.clearHost = clearHost;

  return secretStore;
}

import chalk from "chalk";
import open from "open";
import { joinURL } from "ufo";
import { createConnect } from "@aigne/cli/utils/aigne-hub/credential.js";

import { createStore } from "./store.mjs";
import {
  WELLKNOWN_SERVICE_PATH,
  AUTH_RETRY_COUNT,
  AUTH_FETCH_INTERVAL,
} from "./constants.mjs";

const TOKEN_KEY = "VIBE_HUB_ACCESS_TOKEN";

/**
 * Get cached access token for a given hub URL
 * @param {string} hubUrl - The MyVibe URL
 * @returns {Promise<string|null>} - The cached access token or null
 */
export async function getCachedAccessToken(hubUrl) {
  const { hostname } = new URL(hubUrl);
  const store = await createStore();

  // Check environment variable first
  let accessToken = process.env.VIBE_HUB_ACCESS_TOKEN;

  // Check stored token
  if (!accessToken) {
    try {
      const storeItem = await store.getItem(hostname);
      accessToken = storeItem?.[TOKEN_KEY];
    } catch (error) {
      console.warn("Could not read stored token:", error.message);
    }
  }

  return accessToken || null;
}

/**
 * Save access token for a given hub URL
 * @param {string} hubUrl - The MyVibe URL
 * @param {string} token - The access token to save
 */
async function saveAccessToken(hubUrl, token) {
  const { hostname } = new URL(hubUrl);
  const store = await createStore();

  try {
    await store.setItem(hostname, { [TOKEN_KEY]: token });
  } catch (error) {
    console.warn("Could not save token:", error.message);
  }
}

/**
 * Clear access token for a given hub URL
 * @param {string} hubUrl - The MyVibe URL
 */
export async function clearAccessToken(hubUrl) {
  const { hostname } = new URL(hubUrl);
  const store = await createStore();

  try {
    await store.clearHost(hostname);
    console.log(chalk.yellow(`Cleared authorization for ${hostname}`));
  } catch (error) {
    console.warn("Could not clear token:", error.message);
  }
}

/**
 * Get access token, prompting for authorization if needed
 * @param {string} hubUrl - The MyVibe URL
 * @param {string} [locale='en'] - User locale
 * @returns {Promise<string>} - The access token
 */
export async function getAccessToken(hubUrl, locale = "en") {
  const { hostname, origin } = new URL(hubUrl);

  // Check for cached token first
  let accessToken = await getCachedAccessToken(hubUrl);
  if (accessToken) {
    return accessToken;
  }

  // Need to get new token via authorization
  const connectUrl = joinURL(origin, WELLKNOWN_SERVICE_PATH);

  console.log(chalk.cyan("\nAuthorization required for MyVibe..."));

  try {
    const result = await createConnect({
      connectUrl,
      connectAction: "gen-simple-access-key",
      source: "MyVibe Publish Skill",
      closeOnSuccess: true,
      appName: "MyVibe",
      appLogo:
        "https://www.myvibe.so/image-bin/uploads/bd15c582471327539b56896cde77ad55.svg",
      retry: AUTH_RETRY_COUNT,
      fetchInterval: AUTH_FETCH_INTERVAL,
      openPage: async (pageUrl) => {
        const url = new URL(pageUrl);
        url.searchParams.set("locale", locale);
        const tipsTitleApp = getAgentName();
        if (tipsTitleApp) {
          url.searchParams.set("tipsTitleApp", tipsTitleApp);
        }

        const connectUrl = url.toString();
        open(connectUrl);

        console.log(
          chalk.cyan(
            "\n🔗 Please open the following URL in your browser to authorize:",
          ),
          chalk.underline(connectUrl),
          "\n",
        );
      },
    });

    accessToken = result.accessKeySecret;

    // Save token for future use
    await saveAccessToken(hubUrl, accessToken);

    console.log(chalk.green("✅ Authorization successful!\n"));

    return accessToken;
  } catch (error) {
    throw new Error(
      `${chalk.red("Authorization failed.")}\n\n` +
        `${chalk.bold("Possible causes:")}\n` +
        `  • Network issue\n` +
        `  • Authorization timeout (5 minutes)\n` +
        `  • User cancelled authorization\n\n` +
        `${chalk.bold("Solution:")} Please try again.`,
    );
  }
}

/**
 * Handle authorization error (401/403)
 * Clears the token so next request will re-authorize
 * @param {string} hubUrl - The MyVibe URL
 * @param {number} statusCode - HTTP status code
 */
export async function handleAuthError(hubUrl, statusCode) {
  if (statusCode === 401 || statusCode === 403) {
    console.log(
      chalk.yellow(
        `\n⚠️ Authorization error (${statusCode}). Clearing saved token...`,
      ),
    );
    await clearAccessToken(hubUrl);
    console.log(
      chalk.cyan("Please run the publish command again to re-authorize.\n"),
    );
  }
}


function getAgentName() {
  if (process.env.CODEX) {
    return 'Codex';
  }
  if (process.env.CLAUDECODE) {
    return 'Claude Code';
  }
  if (process.env.GEMINI_CLI) {
    return 'Gemini CLI';
  }
  if (process.env.OPENCODE) {
    return 'OpenCode';
  }
}
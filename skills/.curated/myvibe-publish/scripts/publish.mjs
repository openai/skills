#!/usr/bin/env node

import { existsSync, readFileSync, unlinkSync } from "node:fs";
import { stat } from "node:fs/promises";
import { resolve } from "node:path";
import chalk from "chalk";
import { joinURL } from "ufo";
import yaml from "js-yaml";

import { VIBE_HUB_URL_DEFAULT, API_PATHS, getScreenshotResultPath, isMainModule } from "./utils/constants.mjs";
import { getAccessToken } from "./utils/auth.mjs";
import { apiPatch, apiGet, subscribeToSSE, pollConversionStatus } from "./utils/http.mjs";
import { zipDirectory, getFileInfo } from "./utils/zip.mjs";
import { uploadFile, createVibeFromUrl } from "./utils/upload.mjs";
import { getPublishHistory, savePublishHistory } from "./utils/history.mjs";

/**
 * Try to read screenshot result from file with retries
 * @param {string} sourcePath - The source path (dir or file) for hash calculation
 * @param {number} maxRetries - Maximum number of retries (default: 3)
 * @param {number} retryDelay - Delay between retries in ms (default: 3000)
 * @returns {Promise<{success: boolean, url?: string, resultPath?: string}>}
 */
async function readScreenshotResult(sourcePath, maxRetries = 3, retryDelay = 3000) {
  const resultPath = getScreenshotResultPath(sourcePath);

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      if (existsSync(resultPath)) {
        const content = readFileSync(resultPath, "utf-8");
        const result = JSON.parse(content);

        if (result.success && result.url) {
          console.log(chalk.green(`✓ Screenshot ready: ${result.url}`));
          return { ...result, resultPath };
        } else {
          // Screenshot failed, don't retry
          console.log(chalk.yellow(`Screenshot generation failed: ${result.error || "Unknown error"}`));
          return { success: false, resultPath };
        }
      }
    } catch (error) {
      // JSON parse error or other issues
      console.log(chalk.yellow(`Failed to read screenshot result: ${error.message}`));
    }

    // File not found, wait and retry (except on last attempt)
    if (attempt < maxRetries) {
      console.log(chalk.gray(`Screenshot not ready, waiting ${retryDelay / 1000}s... (attempt ${attempt}/${maxRetries})`));
      await new Promise((resolve) => setTimeout(resolve, retryDelay));
    }
  }

  console.log(chalk.yellow("Screenshot not available, proceeding without cover image"));
  return { success: false, resultPath };
}

/**
 * Main publish function
 */
async function publish(options) {
  const {
    file,
    dir,
    url,
    hub = VIBE_HUB_URL_DEFAULT,
    title,
    desc,
    visibility = "public",
    // Extended metadata fields from config
    coverImage,
    githubRepo,
    platformTags,
    techStackTags,
    categoryTags,
    modelTags,
    // Config file path (for cleanup after publish)
    configPath,
    // Version control options
    did: explicitDid,
    newVibe = false,
  } = options;

  let cleanup = null;

  try {
    // Validate input
    const inputCount = [file, dir, url].filter(Boolean).length;
    if (inputCount === 0) {
      throw new Error("Please provide one of: --file, --dir, or --url");
    }
    if (inputCount > 1) {
      throw new Error("Please provide only one of: --file, --dir, or --url");
    }

    console.log(chalk.bold("\n🚀 MyVibe Publish\n"));
    console.log(chalk.gray(`Hub: ${hub}`));

    // Get authorization
    const accessToken = await getAccessToken(hub);

    // Resolve source path for history lookup
    let sourcePath = null;
    if (dir) {
      sourcePath = resolve(dir);
    } else if (file) {
      sourcePath = resolve(file);
    } else if (url) {
      sourcePath = url;
    }

    // Determine DID for version update
    let existingDid = null;
    if (!newVibe) {
      if (explicitDid) {
        existingDid = explicitDid;
      } else if (sourcePath) {
        const history = await getPublishHistory(sourcePath, hub);
        if (history) {
          existingDid = history.did;
        }
      }
    }

    let did;
    let needsConversion = false;
    let versionHistoryEnabled;

    if (url) {
      // URL import mode
      const result = await createVibeFromUrl(url, hub, accessToken, {
        title,
        description: desc,
        visibility,
      });
      did = result.did;
      // URL imports don't need conversion
      needsConversion = false;
    } else {
      // File or directory upload mode
      let filePath;

      if (dir) {
        // Compress directory first
        const dirPath = resolve(dir);
        if (!existsSync(dirPath)) {
          throw new Error(`Directory not found: ${dirPath}`);
        }
        const dirStat = await stat(dirPath);
        if (!dirStat.isDirectory()) {
          throw new Error(`Not a directory: ${dirPath}`);
        }

        const zipResult = await zipDirectory(dirPath);
        filePath = zipResult.zipPath;
        cleanup = zipResult.cleanup;
      } else {
        // Use provided file
        filePath = resolve(file);
        if (!existsSync(filePath)) {
          throw new Error(`File not found: ${filePath}`);
        }

        const fileInfo = await getFileInfo(filePath);
        if (fileInfo.type !== "application/zip" && fileInfo.type !== "text/html") {
          throw new Error(`Unsupported file type: ${fileInfo.type}. Only ZIP and HTML files are supported.`);
        }
      }

      // Upload file with optional existing DID for version update
      const uploadResult = await uploadFile(filePath, hub, accessToken, { did: existingDid });
      did = uploadResult.did;
      needsConversion = uploadResult.status === "PENDING";
      versionHistoryEnabled = uploadResult.versionHistoryEnabled;
    }

    // Wait for conversion if needed
    if (needsConversion) {
      console.log(chalk.cyan("\nWaiting for conversion..."));

      const { origin } = new URL(hub);
      const streamUrl = joinURL(origin, API_PATHS.CONVERT_STREAM(did));
      const statusUrl = joinURL(origin, API_PATHS.CONVERSION_STATUS(did));

      try {
        // Try SSE stream first
        await subscribeToSSE(streamUrl, accessToken, hub, {
          onMessage: (message) => {
            console.log(chalk.gray(`  ${message}`));
          },
          onProgress: (data) => {
            if (data.message) {
              console.log(chalk.gray(`  ${data.message}`));
            }
          },
          onCompleted: (data) => {
            console.log(chalk.green("\n✅ Conversion completed!"));
          },
          onError: (error) => {
            console.log(chalk.red(`\n❌ Conversion error: ${error}`));
          },
        });
      } catch (sseError) {
        // Fallback to polling if SSE fails
        console.log(chalk.yellow("SSE connection failed, using polling..."));
        await pollConversionStatus(statusUrl, accessToken, hub, {
          onProgress: (status) => {
            console.log(chalk.gray(`  Status: ${status.status}`));
          },
          onCompleted: (status) => {
            console.log(chalk.green("\n✅ Conversion completed!"));
          },
          onError: (error) => {
            console.log(chalk.red(`\n❌ Conversion error: ${error}`));
          },
        });
      }
    }

    // Try to read screenshot result from file (if not already provided)
    // Only for dir/file mode, not URL import
    let finalCoverImage = coverImage;
    let screenshotResultPath = null;
    if (!finalCoverImage && sourcePath && !url) {
      console.log(chalk.cyan("\nChecking for screenshot..."));
      const screenshotResult = await readScreenshotResult(sourcePath);
      screenshotResultPath = screenshotResult.resultPath;
      if (screenshotResult.success && screenshotResult.url) {
        finalCoverImage = screenshotResult.url;
      }
    }

    // Execute publish action
    console.log(chalk.cyan("\nPublishing..."));

    const { origin } = new URL(hub);
    const actionUrl = joinURL(origin, API_PATHS.VIBE_ACTION(did));

    const actionData = {
      action: "publish",
    };

    if (title) actionData.title = title;
    if (desc) actionData.description = desc;
    if (visibility) actionData.visibility = visibility;
    // Extended metadata fields
    if (finalCoverImage) actionData.coverImage = finalCoverImage;
    if (githubRepo) actionData.githubRepo = githubRepo;
    if (platformTags && platformTags.length > 0) actionData.platformTags = platformTags;
    if (techStackTags && techStackTags.length > 0) actionData.techStackTags = techStackTags;
    if (categoryTags && categoryTags.length > 0) actionData.categoryTags = categoryTags;
    if (modelTags && modelTags.length > 0) actionData.modelTags = modelTags;

    const actionResult = await apiPatch(actionUrl, actionData, accessToken, hub);

    if (actionResult.success) {
      console.log(chalk.green.bold("\n✅ Published successfully!\n"));

      // Fetch vibe details to get userDid and preview URL
      const vibeInfoUrl = joinURL(origin, API_PATHS.VIBE_INFO(did));
      const vibeInfo = await apiGet(vibeInfoUrl, accessToken, hub);

      // Build vibe URL: /{userDid}/{did}
      const vibeUrl = joinURL(hub, vibeInfo.userDid, did);
      console.log(chalk.cyan(`🔗 ${vibeUrl}\n`));

      // Upgrade prompt: updating existing project + version history not enabled
      if (existingDid && versionHistoryEnabled === false) {
        const pricingUrl = joinURL(hub, "pricing");
        console.log(chalk.yellow("📦 Previous version overwritten. Want to keep version history?"));
        console.log(chalk.yellow(`   Upgrade to Creator → ${pricingUrl}\n`));
      }

      // Save publish history for future version updates
      if (sourcePath) {
        try {
          await savePublishHistory(sourcePath, hub, did, title || "");
        } catch (e) {
          // Ignore history save errors
        }
      }

      // Delete config file after successful publish
      if (configPath && existsSync(configPath)) {
        try {
          unlinkSync(configPath);
          console.log(chalk.gray(`Cleaned up config file: ${configPath}`));
        } catch (e) {
          // Ignore cleanup errors
        }
      }

      // Delete screenshot result file after successful publish
      if (screenshotResultPath && existsSync(screenshotResultPath)) {
        try {
          unlinkSync(screenshotResultPath);
          console.log(chalk.gray(`Cleaned up screenshot result: ${screenshotResultPath}`));
        } catch (e) {
          // Ignore cleanup errors
        }
      }

      return {
        success: true,
        did,
        url: vibeUrl,
      };
    } else {
      throw new Error(actionResult.error || "Publish action failed");
    }
  } catch (error) {
    console.error(chalk.red(`\n❌ Error: ${error.message}\n`));
    return {
      success: false,
      error: error.message,
    };
  } finally {
    // Cleanup temp files
    if (cleanup) {
      await cleanup();
    }
  }
}

/**
 * Parse config object (shared by file and stdin loaders)
 * @param {Object} config - Parsed config object
 * @returns {Object} - Options object
 */
function parseConfig(config) {
  const options = {};

  // Parse source
  if (config.source) {
    if (config.source.type === "dir") {
      options.dir = config.source.path;
    } else if (config.source.type === "file") {
      options.file = config.source.path;
    } else if (config.source.type === "url") {
      options.url = config.source.path;
    }
    // Optional explicit DID for version update
    if (config.source.did) {
      options.did = config.source.did;
    }
  }

  // Parse metadata
  if (config.metadata) {
    if (config.metadata.title) options.title = config.metadata.title;
    if (config.metadata.description) options.desc = config.metadata.description;
    if (config.metadata.visibility) options.visibility = config.metadata.visibility;
    if (config.metadata.coverImage) options.coverImage = config.metadata.coverImage;
    if (config.metadata.githubRepo) options.githubRepo = config.metadata.githubRepo;
    if (config.metadata.platformTags) options.platformTags = config.metadata.platformTags;
    if (config.metadata.techStackTags) options.techStackTags = config.metadata.techStackTags;
    if (config.metadata.categoryTags) options.categoryTags = config.metadata.categoryTags;
    if (config.metadata.modelTags) options.modelTags = config.metadata.modelTags;
  }

  // Parse hub URL (can be at root level)
  if (config.hub) options.hub = config.hub;

  return options;
}

/**
 * Load options from stdin (JSON format)
 * @returns {Promise<Object>} - Parsed options
 */
async function loadConfigFromStdin() {
  return new Promise((resolve, reject) => {
    let data = "";

    // Set encoding
    process.stdin.setEncoding("utf8");

    // Check if stdin has data (not a TTY)
    if (process.stdin.isTTY) {
      reject(new Error("No data provided via stdin. Use: echo '{...}' | node publish.mjs --config-stdin"));
      return;
    }

    process.stdin.on("data", (chunk) => {
      data += chunk;
    });

    process.stdin.on("end", () => {
      try {
        const config = JSON.parse(data);
        resolve(parseConfig(config));
      } catch (e) {
        reject(new Error(`Failed to parse JSON from stdin: ${e.message}`));
      }
    });

    process.stdin.on("error", (err) => {
      reject(new Error(`Failed to read from stdin: ${err.message}`));
    });

    // Timeout after 5 seconds if no data
    setTimeout(() => {
      if (!data) {
        reject(new Error("Timeout waiting for stdin data"));
      }
    }, 5000);
  });
}

/**
 * Load options from config file (YAML format)
 * @param {string} configPath - Path to config YAML file
 * @returns {Object} - Parsed options
 */
function loadConfigFile(configPath) {
  const absolutePath = resolve(configPath);
  if (!existsSync(absolutePath)) {
    throw new Error(`Config file not found: ${absolutePath}`);
  }

  const content = readFileSync(absolutePath, "utf-8");
  const config = yaml.load(content);

  const options = parseConfig(config);
  options.configPath = absolutePath; // Store for cleanup after publish

  return options;
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
      case "--config":
      case "-c":
        // Load options from config file
        const configOptions = loadConfigFile(nextArg);
        Object.assign(options, configOptions);
        i++;
        break;
      case "--file":
      case "-f":
        options.file = nextArg;
        i++;
        break;
      case "--dir":
      case "-d":
        options.dir = nextArg;
        i++;
        break;
      case "--url":
      case "-u":
        options.url = nextArg;
        i++;
        break;
      case "--hub":
      case "-h":
        options.hub = nextArg;
        i++;
        break;
      case "--title":
      case "-t":
        options.title = nextArg;
        i++;
        break;
      case "--desc":
        options.desc = nextArg;
        i++;
        break;
      case "--visibility":
      case "-v":
        options.visibility = nextArg;
        i++;
        break;
      case "--did":
        options.did = nextArg;
        i++;
        break;
      case "--new":
        options.newVibe = true;
        break;
      case "--config-stdin":
        options.configStdin = true;
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
${chalk.bold("MyVibe Publish")}

Publish web content to MyVibe.

${chalk.bold("Usage:")}
  node publish.mjs [options]

${chalk.bold("Options:")}
  --config, -c <path>     Load options from YAML config file
  --config-stdin          Load options from stdin (JSON format)
  --file, -f <path>       Path to HTML file or ZIP archive
  --dir, -d <path>        Directory to compress and publish
  --url, -u <url>         URL to import and publish
  --hub, -h <url>         MyVibe URL (default: ${VIBE_HUB_URL_DEFAULT})
  --title, -t <title>     Project title
  --desc <desc>           Project description
  --visibility, -v <vis>  Visibility: public or private (default: public)
  --did <did>             Vibe DID for version update (overrides auto-detection)
  --new                   Force create new Vibe, ignore publish history
  --help                  Show this help message

${chalk.bold("Config File Format (YAML):")}
  source:
    type: dir
    path: ./dist
    did: z2qaXXXX  # Optional: explicit DID for version update
  hub: https://www.myvibe.so
  metadata:
    title: My App
    description: A cool app
    visibility: public
    coverImage: https://...
    githubRepo: https://github.com/...
    platformTags: [1, 2]
    techStackTags: [3, 4]
    categoryTags: [5]
    modelTags: [6]

${chalk.bold("Examples:")}
  # Publish using config file
  node publish.mjs --config ./publish-config.yaml

  # Publish using stdin (no file needed)
  echo '{"source":{"type":"dir","path":"./dist"},"metadata":{"title":"My App"}}' | node publish.mjs --config-stdin

  # Publish a ZIP file
  node publish.mjs --file ./dist.zip --title "My App"

  # Publish a directory
  node publish.mjs --dir ./dist --title "My App" --desc "A cool app"

  # Import from URL
  node publish.mjs --url https://example.com/app
`);
}

// CLI entry point
if (isMainModule(import.meta.url)) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    printHelp();
    process.exit(1);
  }

  const options = parseArgs(args);

  // Handle --config-stdin asynchronously
  (async () => {
    try {
      if (options.configStdin) {
        const stdinOptions = await loadConfigFromStdin();
        Object.assign(options, stdinOptions);
        delete options.configStdin;
      }

      const result = await publish(options);
      process.exit(result.success ? 0 : 1);
    } catch (error) {
      console.error(chalk.red(`Fatal error: ${error.message}`));
      process.exit(1);
    }
  })();
}

export default publish;

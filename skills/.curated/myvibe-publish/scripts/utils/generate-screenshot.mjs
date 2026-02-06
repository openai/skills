#!/usr/bin/env node

import { existsSync, unlinkSync, mkdirSync, copyFileSync, rmSync, writeFileSync } from "node:fs";
import { spawn, execSync } from "node:child_process";
import path from "node:path";
import chalk from "chalk";

import { VIBE_HUB_URL_DEFAULT, getScreenshotResultPath, isMainModule } from "./constants.mjs";
import { uploadImage } from "./upload-image.mjs";

const DEFAULT_PORT = 3456;
const SERVER_STARTUP_TIMEOUT = 10000;
const SCREENSHOT_PATH = "/tmp/myvibe-screenshot.png";

/**
 * Save screenshot result to file for publish.mjs to read
 * @param {string} sourcePath - The source path (dir or file) for hash calculation
 * @param {Object} result - The result object to save
 */
function saveResultToFile(sourcePath, result) {
  try {
    const resultPath = getScreenshotResultPath(sourcePath);
    writeFileSync(resultPath, JSON.stringify(result, null, 2));
    console.log(chalk.gray(`Result saved to ${resultPath}`));
  } catch (error) {
    console.error(chalk.yellow(`Warning: Failed to save result to file: ${error.message}`));
  }
}

/**
 * Clear previous screenshot result file
 * @param {string} sourcePath - The source path (dir or file) for hash calculation
 */
function clearResultFile(sourcePath) {
  try {
    const resultPath = getScreenshotResultPath(sourcePath);
    if (existsSync(resultPath)) {
      unlinkSync(resultPath);
    }
  } catch {
    // Ignore errors
  }
}

/**
 * Generate screenshot of a local directory or file and upload to MyVibe
 * @param {Object} options
 * @param {string} [options.dir] - Directory to serve and screenshot
 * @param {string} [options.file] - Single HTML file to screenshot
 * @param {string} [options.hub] - MyVibe hub URL
 * @param {number} [options.port] - Port for local server (default: 3456)
 * @returns {Promise<{success: boolean, url?: string, error?: string, suggestion?: string}>}
 */
export async function generateScreenshot(options) {
  const {
    hub = VIBE_HUB_URL_DEFAULT,
    port = DEFAULT_PORT,
  } = options;

  // Determine source path for hash calculation (original path, not temp dir)
  // Fallback to "unknown" for edge case when neither is provided (will fail validation)
  const sourcePath = options.file || options.dir || "unknown";

  let serverProcess = null;
  let tempDir = null;
  let dir = options.dir;

  // Clear previous result file at the start
  clearResultFile(sourcePath);

  try {
    // Handle --file: copy to temp directory
    if (options.file) {
      const filePath = path.resolve(options.file);
      if (!existsSync(filePath)) {
        const result = {
          success: false,
          error: `File not found: ${filePath}`,
          suggestion: "Check that the file path is correct",
        };
        saveResultToFile(sourcePath, result);
        return result;
      }

      // Create temp directory and copy file as index.html
      tempDir = `/tmp/myvibe-screenshot-${Date.now()}`;
      mkdirSync(tempDir, { recursive: true });
      copyFileSync(filePath, path.join(tempDir, "index.html"));
      dir = tempDir;
    }

    // Validate that we have a directory to serve
    if (!dir) {
      const result = {
        success: false,
        error: "--dir or --file is required",
        suggestion: "Provide either --dir <directory> or --file <html-file>",
      };
      saveResultToFile(sourcePath, result);
      return result;
    }

    // Step 1: Validate directory
    const dirPath = path.resolve(dir);
    if (!existsSync(dirPath)) {
      const result = {
        success: false,
        error: `Directory not found: ${dirPath}`,
        suggestion: "Check that the directory path is correct",
      };
      saveResultToFile(sourcePath, result);
      return result;
    }

    console.log(chalk.cyan(`\n📸 Generating screenshot for: ${dirPath}\n`));

    // Step 2: Check agent-browser
    console.log(chalk.gray(`Checking agent-browser...`));
    const agentBrowserCheck = checkAgentBrowser();
    if (!agentBrowserCheck.installed) {
      saveResultToFile(sourcePath, agentBrowserCheck);
      return agentBrowserCheck;
    }
    console.log(chalk.green(`✓ agent-browser ready`));

    // Step 3: Find available port and start server
    let actualPort = port;
    if (!(await isPortAvailable(port))) {
      console.log(chalk.yellow(`Port ${port} is in use, finding available port...`));
      actualPort = await findAvailablePort(port);
    }
    console.log(chalk.gray(`Starting local server on port ${actualPort}...`));
    serverProcess = await startServer(dirPath, actualPort);

    // Step 4: Wait for server ready
    await waitForServer(actualPort);
    console.log(chalk.green(`✓ Server ready on port ${actualPort}`));

    // Step 5: Take screenshot with agent-browser
    console.log(chalk.gray(`Taking screenshot...`));
    await takeScreenshot(`http://localhost:${actualPort}`, SCREENSHOT_PATH);
    console.log(chalk.green(`✓ Screenshot saved`));

    // Step 6: Upload to MyVibe
    console.log(chalk.gray(`Uploading to MyVibe...`));
    const uploadResult = await uploadImage({ file: SCREENSHOT_PATH, hub });

    if (!uploadResult.success) {
      const result = {
        success: false,
        error: uploadResult.error,
        suggestion: "Check your network connection and MyVibe authorization",
      };
      // Save error result to file for publish.mjs to read
      saveResultToFile(sourcePath, result);
      return result;
    }

    console.log(chalk.green.bold(`\n✅ Screenshot uploaded successfully!\n`));
    console.log(chalk.cyan(`🔗 ${uploadResult.url}\n`));

    const result = {
      success: true,
      url: uploadResult.url,
      screenshotPath: SCREENSHOT_PATH,
    };

    // Save result to file for publish.mjs to read
    saveResultToFile(sourcePath, result);

    return result;
  } catch (error) {
    const result = handleError(error);
    // Save error result to file for publish.mjs to read
    saveResultToFile(sourcePath, result);
    return result;
  } finally {
    // Cleanup: stop server
    if (serverProcess) {
      serverProcess.kill();
      console.log(chalk.gray(`Server stopped`));
    }
    // Cleanup: close agent-browser (in case it's still open)
    try {
      execSync("agent-browser close 2>/dev/null", { stdio: "ignore" });
    } catch {
      // Ignore errors
    }
    // Cleanup: remove temp directory if created
    if (tempDir && existsSync(tempDir)) {
      try {
        rmSync(tempDir, { recursive: true, force: true });
      } catch {
        // Ignore cleanup errors
      }
    }
  }
}

/**
 * Check if agent-browser is installed and has Chromium
 * @returns {{installed: boolean, error?: string, suggestion?: string}}
 */
function checkAgentBrowser() {
  // Check if agent-browser command exists
  try {
    execSync("which agent-browser", { stdio: "ignore" });
  } catch {
    return {
      installed: false,
      success: false,
      error: "agent-browser is not installed",
      suggestion: "Run: npm install -g agent-browser && agent-browser install",
    };
  }

  // Check if Chromium is installed by running a simple command
  try {
    execSync("agent-browser close 2>/dev/null || true", { stdio: "ignore" });
    return { installed: true };
  } catch {
    return {
      installed: false,
      success: false,
      error: "agent-browser Chromium is not installed",
      suggestion: "Run: agent-browser install",
    };
  }
}

/**
 * Check if a port is available
 * @param {number} port
 * @returns {Promise<boolean>}
 */
async function isPortAvailable(port) {
  try {
    await fetch(`http://localhost:${port}`, {
      method: "HEAD",
      signal: AbortSignal.timeout(1000),
    });
    return false; // Port is in use (got response)
  } catch (error) {
    // ECONNREFUSED means port is available
    if (error.cause?.code === "ECONNREFUSED") {
      return true;
    }
    // Timeout or other errors - assume available
    return true;
  }
}

/**
 * Find an available port starting from the given port
 * @param {number} startPort
 * @param {number} maxAttempts
 * @returns {Promise<number>}
 */
async function findAvailablePort(startPort, maxAttempts = 10) {
  for (let i = 0; i < maxAttempts; i++) {
    const port = startPort + i;
    if (await isPortAvailable(port)) {
      return port;
    }
  }
  throw new Error(`No available port found in range ${startPort}-${startPort + maxAttempts - 1}`);
}

/**
 * Start a local HTTP server
 * @param {string} dir - Directory to serve
 * @param {number} port - Port number
 * @returns {Promise<ChildProcess>} Server process
 */
async function startServer(dir, port) {
  return new Promise((resolve, reject) => {
    const serverProcess = spawn("npx", ["-y", "http-server", dir, "-p", port.toString(), "-c-1", "--silent"], {
      stdio: ["ignore", "pipe", "pipe"],
      detached: false,
    });

    serverProcess.on("error", (err) => {
      reject(new Error(`Failed to start server: ${err.message}`));
    });

    // Give it a moment to start
    setTimeout(() => {
      if (serverProcess.killed) {
        reject(new Error("Server process terminated unexpectedly"));
      } else {
        resolve(serverProcess);
      }
    }, 500);
  });
}

/**
 * Wait for server to be ready
 * @param {number} port - Port number
 * @param {number} timeout - Timeout in milliseconds
 */
async function waitForServer(port, timeout = SERVER_STARTUP_TIMEOUT) {
  const startTime = Date.now();
  const url = `http://localhost:${port}`;

  while (Date.now() - startTime < timeout) {
    try {
      const response = await fetch(url, { method: "HEAD" });
      if (response.ok || response.status === 404) {
        // 404 is ok - server is running, just maybe no index
        return;
      }
    } catch {
      // Server not ready yet, wait and retry
    }
    await new Promise((resolve) => setTimeout(resolve, 200));
  }

  throw new Error(`Server did not start within ${timeout / 1000} seconds`);
}

/**
 * Take screenshot using agent-browser
 * @param {string} url - URL to screenshot
 * @param {string} outputPath - Path to save screenshot
 */
async function takeScreenshot(url, outputPath) {
  // Remove old screenshot if exists
  try {
    unlinkSync(outputPath);
  } catch {
    // Ignore if doesn't exist
  }

  // Open URL in agent-browser
  try {
    execSync(`agent-browser open "${url}"`, {
      stdio: "inherit",
      timeout: 30000,
    });
  } catch (error) {
    throw new Error(`Failed to open URL in agent-browser: ${error.message}`);
  }

  // Wait for page to load
  await new Promise((resolve) => setTimeout(resolve, 2000));

  // Take screenshot
  try {
    execSync(`agent-browser screenshot "${outputPath}"`, {
      stdio: "inherit",
      timeout: 30000,
    });
  } catch (error) {
    throw new Error(`Failed to take screenshot: ${error.message}`);
  }

  // Close browser
  try {
    execSync("agent-browser close", {
      stdio: "inherit",
      timeout: 10000,
    });
  } catch {
    // Ignore close errors
  }

  // Verify screenshot was created
  if (!existsSync(outputPath)) {
    throw new Error("Screenshot file was not created");
  }
}

/**
 * Handle errors and return structured response with suggestions
 * @param {Error} error
 * @returns {{success: false, error: string, suggestion: string}}
 */
function handleError(error) {
  const message = error.message || String(error);

  // agent-browser not installed
  if (message.includes("agent-browser") && message.includes("not found")) {
    return {
      success: false,
      error: "agent-browser is not installed",
      suggestion: "Run: npm install -g agent-browser && agent-browser install",
    };
  }

  // Chromium not installed
  if (message.includes("Chromium") || message.includes("browser") && message.includes("install")) {
    return {
      success: false,
      error: "Chromium browser not installed for agent-browser",
      suggestion: "Run: agent-browser install",
    };
  }

  // Port already in use
  if (message.includes("EADDRINUSE") || message.includes("address already in use")) {
    return {
      success: false,
      error: "Port is already in use",
      suggestion: "Try a different port with --port <number>, or kill the process using the port",
    };
  }

  // No available port
  if (message.includes("No available port")) {
    return {
      success: false,
      error: message,
      suggestion: "Kill processes using ports 3456-3465, or specify a different port range",
    };
  }

  // Server timeout
  if (message.includes("Server did not start")) {
    return {
      success: false,
      error: "Local server failed to start",
      suggestion: "Check if npx and http-server are working correctly",
    };
  }

  // Screenshot timeout or failure
  if (message.includes("screenshot") || message.includes("Screenshot")) {
    return {
      success: false,
      error: message,
      suggestion: "Try running manually: agent-browser open <url> && agent-browser screenshot /tmp/test.png",
    };
  }

  // Authorization errors
  if (message.includes("401") || message.includes("403") || message.includes("Unauthorized")) {
    return {
      success: false,
      error: "Authorization failed",
      suggestion: "Your MyVibe token may have expired. Re-run the publish command to re-authorize",
    };
  }

  // Directory not found
  if (message.includes("ENOENT") || message.includes("not found") || message.includes("Directory not found")) {
    return {
      success: false,
      error: message,
      suggestion: "Check that the path exists and is accessible",
    };
  }

  // Generic fallback
  return {
    success: false,
    error: message,
    suggestion: "Check the error message above. If the problem persists, try running screenshot steps manually",
  };
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
      case "--dir":
      case "-d":
        options.dir = nextArg;
        i++;
        break;
      case "--file":
      case "-f":
        options.file = nextArg;
        i++;
        break;
      case "--hub":
      case "-h":
        options.hub = nextArg;
        i++;
        break;
      case "--port":
      case "-p":
        options.port = parseInt(nextArg, 10);
        i++;
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
${chalk.bold("MyVibe Screenshot Generator")}

Generate a screenshot of a local directory or HTML file and upload to MyVibe.

${chalk.bold("Usage:")}
  node generate-screenshot.mjs --dir <path> [options]
  node generate-screenshot.mjs --file <path> [options]

${chalk.bold("Options:")}
  --dir, -d <path>    Directory to serve and screenshot
  --file, -f <path>   Single HTML file to screenshot
  --hub, -h <url>     MyVibe URL (default: ${VIBE_HUB_URL_DEFAULT})
  --port, -p <port>   Local server port (default: ${DEFAULT_PORT})
  --help              Show this help message

${chalk.bold("Examples:")}
  # Generate screenshot from directory
  node generate-screenshot.mjs --dir ./dist

  # Generate screenshot from single HTML file
  node generate-screenshot.mjs --file ./index.html

  # Use specific port
  node generate-screenshot.mjs --dir ./dist --port 8080
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

  if (!options.dir && !options.file) {
    console.error(chalk.red("Error: --dir or --file is required"));
    process.exit(1);
  }

  generateScreenshot(options)
    .then((result) => {
      // Output JSON for script consumption
      console.log(JSON.stringify(result, null, 2));
      process.exit(result.success ? 0 : 1);
    })
    .catch((error) => {
      console.error(chalk.red(`Fatal error: ${error.message}`));
      process.exit(1);
    });
}

export default generateScreenshot;

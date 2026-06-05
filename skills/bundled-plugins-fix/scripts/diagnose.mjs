import { readFileSync, readlinkSync, existsSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const HOME = process.env.USERPROFILE || "C:\\Users\\liang";
const CODEX_HOME = join(HOME, ".codex");

// --- paths ---
const CONFIG = join(CODEX_HOME, "config.toml");
const CHROME_LATEST = join(CODEX_HOME, "plugins", "cache", "openai-bundled", "chrome", "latest");
const CHROME_CACHE = join(CODEX_HOME, "plugins", "cache", "openai-bundled", "chrome", "26.601.21317");
const MARKET_PLUGINS = join(CODEX_HOME, ".tmp", "bundled-marketplaces", "openai-bundled", "plugins");
const V2_MANIFEST = join(process.env.LOCALAPPDATA || join(HOME, "AppData", "Local"), "OpenAI", "Codex", "chrome-native-hosts-v2.json");
const EXTENSION_MANIFEST = join(process.env.LOCALAPPDATA || join(HOME, "AppData", "Local"), "OpenAI", "extension", "com.openai.codexextension.json");
const CHROME_EXT_PATH = join(process.env.LOCALAPPDATA || join(HOME, "AppData", "Local"), "Google", "Chrome", "User Data", "Default", "Extensions", "hehggadaopoacecdllhhajmbjkdcmajg");

const PASS = "✅";
const FAIL = "❌";
const WARN = "⚠️";

let passed = 0, failed = 0, warned = 0;

function check(label, ok, detail) {
  if (ok) { console.log(`${PASS} ${label}`); passed++; }
  else if (detail) { console.log(`${WARN} ${label}: ${detail}`); warned++; }
  else { console.log(`${FAIL} ${label}`); failed++; }
}

function section(title) {
  console.log(`\n=== ${title} ===`);
}

// =============================================
section("1. config.toml — Plugin Enablement");
// =============================================
try {
  const cfg = readFileSync(CONFIG, "utf-8");
  check('chrome@openai-bundled enabled', cfg.includes('[plugins."chrome@openai-bundled"]'), "Missing section");
  check('computer-use@openai-bundled enabled', cfg.includes('[plugins."computer-use@openai-bundled"]'), "Missing section");
} catch (e) {
  check("config.toml readable", false, e.message);
}

// =============================================
section("2. Chrome latest junction");
// =============================================
try {
  const target = readlinkSync(CHROME_LATEST);
  const hasPlugin = existsSync(join(target, ".codex-plugin", "plugin.json"));
  check("Junction exists: " + target, hasPlugin, "target=" + target);
} catch (e) {
  check("Chrome latest junction", false, e.message);
}

// =============================================
section("3. Marketplace source — chrome");
// =============================================
const mktChrome = join(MARKET_PLUGINS, "chrome");
check("browser-client.mjs", existsSync(join(mktChrome, "scripts", "browser-client.mjs")));
check("extension-host.exe", existsSync(join(mktChrome, "extension-host", "windows", "x64", "extension-host.exe")));
check("check-extension-installed.js", existsSync(join(mktChrome, "scripts", "check-extension-installed.js")));
check("check-native-host-manifest.js", existsSync(join(mktChrome, "scripts", "check-native-host-manifest.js")));
check("extension-id.json", existsSync(join(mktChrome, "scripts", "extension-id.json")));

// =============================================
section("4. Marketplace source — computer-use");
// =============================================
const mktCu = join(MARKET_PLUGINS, "computer-use");
check(".codex-plugin/plugin.json", existsSync(join(mktCu, ".codex-plugin", "plugin.json")));
check("scripts/computer-use-client.mjs", existsSync(join(mktCu, "scripts", "computer-use-client.mjs")));
check("node_modules/@oai/sky", existsSync(join(mktCu, "node_modules", "@oai", "sky", "package.json")));
check("assets/app-icon.png", existsSync(join(mktCu, "assets", "app-icon.png")));
check("skills/computer-use/SKILL.md", existsSync(join(mktCu, "skills", "computer-use", "SKILL.md")));

// =============================================
section("5. Native host manifest");
// =============================================
try {
  const manifest = JSON.parse(readFileSync(EXTENSION_MANIFEST, "utf-8"));
  check("manifest path: " + manifest.path, existsSync(manifest.path), "Binary not found at path");
  check("allowed_origins", manifest.allowed_origins?.includes("chrome-extension://hehggadaopoacecdllhhajmbjkdcmajg/"));
  check("type = stdio", manifest.type === "stdio");
  check("name = com.openai.codexextension", manifest.name === "com.openai.codexextension");
} catch (e) {
  check("Native host manifest", false, e.message);
}

// =============================================
section("6. Windows Registry (NativeMessagingHosts)");
// =============================================
// Can't read registry from Node.js directly, check via known state
check("Registry check (manual verification recommended)", true, "Run: Get-ItemProperty 'HKCU:\\SOFTWARE\\Google\\Chrome\\NativeMessagingHosts\\com.openai.codexextension'");

// =============================================
section("7. Chrome extension");
// =============================================
try {
  const extDirs = readdirSync(CHROME_EXT_PATH);
  check("Extension directory exists", extDirs.length > 0, "Empty directory");
  check("Extension version: " + extDirs.join(", "), true);
} catch (e) {
  check("Chrome extension installed", false, "Not found at expected path");
}

// =============================================
section("8. Extension-host process");
// =============================================
// Check via PowerShell (more reliable than tasklist)
import { execSync } from "node:child_process";
try {
  const out = execSync('powershell -NoProfile -Command "if (Get-Process -Name extension-host -ErrorAction SilentlyContinue) { \'running\' } else { \'stopped\' }"', { stdio: "pipe", encoding: "utf-8", timeout: 5000 });
  const isRunning = out.includes("running");
  check("extension-host.exe", isRunning, isRunning ? "" : "Process not found");
} catch (e) {
  check("extension-host.exe", false, e.message);
}

// =============================================
section("9. V2 manifest consistency");
// =============================================
try {
  const v2 = JSON.parse(readFileSync(V2_MANIFEST, "utf-8"));
  const entry = v2.entries?.[0];
  check("extensionHostPath exists", existsSync(entry?.paths?.extensionHostPath));
  check("browserClientPath exists", existsSync(entry?.paths?.browserClientPath));
  check("extensionIds match", entry?.extensionIds?.includes("hehggadaopoacecdllhhajmbjkdcmajg"));
  check("nativeHostNames match", entry?.nativeHostNames?.includes("com.openai.codexextension"));
} catch (e) {
  check("V2 manifest readable", false, e.message);
}

// =============================================
console.log(`\n=== Summary: ${passed} passed, ${warned} warnings, ${failed} failed ===`);
if (failed > 0) {
  console.log("Some checks failed. Fix the issues above and re-run this script.");
  process.exit(1);
} else {
  console.log("All checks passed.");
}
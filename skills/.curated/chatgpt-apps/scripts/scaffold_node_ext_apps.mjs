#!/usr/bin/env node

import { mkdirSync, writeFileSync, existsSync, readdirSync, lstatSync } from "node:fs";
import path from "node:path";

function toSlug(value) {
  const normalized = value.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return normalized || "example-chatgpt-app";
}

function toToolName(value) {
  const normalized = value.trim().toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/_+/g, "_").replace(/^_+|_+$/g, "");
  return normalized || "show_example";
}

function toTitle(value) {
  const parts = value.split(/[-_]+/).filter(Boolean);
  return parts.map((part) => part[0].toUpperCase() + part.slice(1)).join(" ") || "Example";
}

function fillTemplate(template, mapping) {
  let result = template;
  for (const [key, value] of Object.entries(mapping)) {
    result = result.replaceAll(key, value);
  }
  return result;
}

function writeFile(filePath, content) {
  mkdirSync(path.dirname(filePath), { recursive: true });
  writeFileSync(filePath, content, "utf8");
}

function ensureTargetDir(targetPath, force) {
  if (existsSync(targetPath)) {
    if (!lstatSync(targetPath).isDirectory()) {
      throw new Error(`Output path exists and is not a directory: ${targetPath}`);
    }
    if (readdirSync(targetPath).length > 0 && !force) {
      throw new Error(
        `Refusing to write into non-empty directory: ${targetPath}\nRe-run with --force to overwrite generated files.`
      );
    }
  }

  mkdirSync(targetPath, { recursive: true });
}

function buildPackageJson(appSlug) {
  const packageJson = {
    name: appSlug,
    private: true,
    type: "module",
    scripts: {
      dev: "tsx watch src/server.ts",
      start: "tsx src/server.ts",
      check: "tsc --noEmit",
    },
    dependencies: {
      "@modelcontextprotocol/ext-apps": "^1.0.1",
      "@modelcontextprotocol/sdk": "^1.20.2",
      zod: "^3.25.76",
    },
    devDependencies: {
      "@types/node": "^24.3.0",
      tsx: "^4.19.4",
      typescript: "^5.9.2",
    },
  };

  return `${JSON.stringify(packageJson, null, 2)}\n`;
}

function buildTsconfig() {
  return `{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "types": ["node"],
    "outDir": "dist"
  },
  "include": ["src/**/*.ts"]
}
`;
}

const WIDGET_TEMPLATE = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>__APP_TITLE__</title>
    <style>
      :root {
        color: #0b0f19;
        font-family: "Inter", system-ui, sans-serif;
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        min-height: 100vh;
        padding: 16px;
        background:
          radial-gradient(circle at top right, #d8f3ff 0, transparent 40%),
          linear-gradient(180deg, #f7fbff 0%, #edf3fb 100%);
      }

      main {
        width: 100%;
        max-width: 420px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(11, 15, 25, 0.08);
        box-shadow: 0 14px 32px rgba(11, 15, 25, 0.08);
      }

      .eyebrow {
        margin: 0 0 8px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #4f5d75;
      }

      h1 {
        margin: 0 0 10px;
        font-size: 24px;
        line-height: 1.15;
      }

      p {
        margin: 0;
        line-height: 1.5;
      }

      .stack {
        display: grid;
        gap: 12px;
      }

      button {
        border: 0;
        border-radius: 999px;
        padding: 10px 14px;
        font: inherit;
        font-weight: 600;
        color: white;
        background: #0f62fe;
        cursor: pointer;
      }

      button[hidden] {
        display: none;
      }

      button.secondary {
        background: #0b0f19;
      }

      .meta {
        padding: 12px;
        border-radius: 14px;
        background: #f5f8fc;
        color: #4f5d75;
        font-size: 13px;
      }
    </style>
  </head>
  <body>
    <main class="stack">
      <p class="eyebrow">__APP_TITLE__ starter</p>
      <h1 id="headline">Waiting for tool output</h1>
      <p id="message">Call the __TOOL_NAME__ tool to hydrate this widget.</p>
      <button id="tool-button" type="button">Call __TOOL_NAME__ from the widget</button>
      <button id="follow-up-button" class="secondary" type="button">
        Ask the host to explain this app
      </button>
      <div class="meta" id="meta">
        This widget uses the MCP Apps bridge by default.
      </div>
    </main>

    <script type="module">
      const headlineEl = document.querySelector("#headline");
      const messageEl = document.querySelector("#message");
      const metaEl = document.querySelector("#meta");
      const toolButtonEl = document.querySelector("#tool-button");
      const followUpButtonEl = document.querySelector("#follow-up-button");

      let toolOutput = null;
      let rpcId = 0;
      const pendingRequests = new Map();

      const render = () => {
        const headline = toolOutput?.headline ?? "__APP_TITLE__";
        const message =
          toolOutput?.message ??
          "Call the __TOOL_NAME__ tool to hydrate this widget.";

        headlineEl.textContent = headline;
        messageEl.textContent = message;

        const theme = window.openai?.theme ?? "bridge-only";
        metaEl.textContent =
          "Runtime: " +
          (window.openai ? "MCP Apps bridge + optional window.openai" : "MCP Apps bridge only") +
          " | Theme: " +
          theme;
      };

      const rpcNotify = (method, params) => {
        window.parent.postMessage({ jsonrpc: "2.0", method, params }, "*");
      };

      const rpcRequest = (method, params) =>
        new Promise((resolve, reject) => {
          const id = ++rpcId;
          pendingRequests.set(id, { resolve, reject });
          window.parent.postMessage({ jsonrpc: "2.0", id, method, params }, "*");
        });

      window.addEventListener(
        "message",
        (event) => {
          if (event.source !== window.parent) {
            return;
          }

          const message = event.data;
          if (!message || message.jsonrpc !== "2.0") {
            return;
          }

          if (typeof message.id === "number") {
            const pending = pendingRequests.get(message.id);
            if (!pending) {
              return;
            }

            pendingRequests.delete(message.id);
            if (message.error) {
              pending.reject(message.error);
              return;
            }

            pending.resolve(message.result);
            return;
          }

          if (message.method === "ui/notifications/tool-result") {
            toolOutput = message.params?.structuredContent ?? null;
            render();
          }
        },
        { passive: true }
      );

      const initializeBridge = async () => {
        await rpcRequest("ui/initialize", {
          appInfo: { name: "__APP_SLUG__-widget", version: "0.1.0" },
          appCapabilities: {},
          protocolVersion: "2026-01-26",
        });
        rpcNotify("ui/notifications/initialized", {});
      };

      const bridgeReady = initializeBridge();

      toolButtonEl.addEventListener("click", async () => {
        await bridgeReady;

        const response = await rpcRequest("tools/call", {
          name: "__TOOL_NAME__",
          arguments: {
            message: "Tool call triggered from the widget.",
          },
        });

        toolOutput = response?.structuredContent ?? toolOutput;
        render();
      });

      followUpButtonEl.addEventListener("click", async () => {
        await bridgeReady;

        rpcNotify("ui/message", {
          role: "user",
          content: [
            {
              type: "text",
              text: "Explain how the __TOOL_NAME__ widget works.",
            },
          ],
        });
      });

      render();
    </script>
  </body>
</html>
`;

const SERVER_TEMPLATE = `import { createServer } from "node:http";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  registerAppResource,
  registerAppTool,
  RESOURCE_MIME_TYPE,
} from "@modelcontextprotocol/ext-apps/server";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.resolve(__dirname, "..");
const WIDGET_URI = "__WIDGET_URI__";
const WIDGET_HTML = readFileSync(
  path.join(ROOT_DIR, "public", "widget.html"),
  "utf8"
);

function createAppServer(): McpServer {
  const server = new McpServer({
    name: "__APP_SLUG__",
    version: "0.1.0",
  });

  registerAppResource(
    server,
    "main-widget",
    WIDGET_URI,
    {},
    async () => ({
      contents: [
        {
          uri: WIDGET_URI,
          mimeType: RESOURCE_MIME_TYPE,
          text: WIDGET_HTML,
          _meta: {
            ui: {
              prefersBorder: true,
              csp: {
                connectDomains: [],
                resourceDomains: [],
              },
            },
            "openai/widgetDescription":
              "__APP_TITLE__ starter widget rendered by the MCP server.",
          },
        },
      ],
    })
  );

  registerAppTool(
    server,
    "__TOOL_NAME__",
    {
      title: "__APP_TITLE__",
      description:
        "Use this when the user wants to render the __APP_TITLE__ starter widget or inspect a minimal Apps SDK tool result.",
      inputSchema: {
        message: z
          .string()
          .optional()
          .describe("Optional message to show inside the widget."),
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        openWorldHint: false,
        idempotentHint: true,
      },
      _meta: {
        ui: { resourceUri: WIDGET_URI },
        "openai/toolInvocation/invoking": "Loading __APP_TITLE__",
        "openai/toolInvocation/invoked": "__APP_TITLE__ ready",
      },
    },
    async ({ message }) => {
      const resolvedMessage =
        message?.trim() ||
        "This starter uses the MCP Apps bridge first, keeps follow-up messaging on ui/message, and limits window.openai to optional host signals.";

      return {
        content: [
          {
            type: "text" as const,
            text: "Rendered the __APP_TITLE__ starter widget.",
          },
        ],
        structuredContent: {
          headline: "__APP_TITLE__",
          message: resolvedMessage,
          source: "__TOOL_NAME__",
          themeHint:
            "Read window.openai.theme in the widget if you need ChatGPT theme information.",
        },
        _meta: {
          "openai/outputTemplate": WIDGET_URI,
        },
      };
    }
  );

  return server;
}

const port = Number(process.env.PORT ?? "__PORT__");
const MCP_PATH = "/mcp";

createServer(async (req, res) => {
  if (!req.url) {
    res.writeHead(400).end("Missing URL");
    return;
  }

  const url = new URL(req.url, "http://" + (req.headers.host ?? "localhost"));
  const isMcpRoute = url.pathname === MCP_PATH || url.pathname.startsWith(MCP_PATH + "/");

  if (req.method === "OPTIONS" && isMcpRoute) {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, GET, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "content-type, mcp-session-id",
      "Access-Control-Expose-Headers": "Mcp-Session-Id",
    });
    res.end();
    return;
  }

  if (req.method === "GET" && url.pathname === "/") {
    res.writeHead(200, { "content-type": "text/plain" }).end("__APP_TITLE__ MCP server");
    return;
  }

  const transportMethods = new Set(["GET", "POST", "DELETE"]);
  if (isMcpRoute && req.method && transportMethods.has(req.method)) {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Expose-Headers", "Mcp-Session-Id");

    const server = createAppServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true,
    });

    res.on("close", () => {
      transport.close();
      server.close();
    });

    try {
      await server.connect(transport);
      await transport.handleRequest(req, res);
    } catch (error) {
      console.error("Failed to handle MCP request:", error);
      if (!res.headersSent) {
        res.writeHead(500).end("Internal server error");
      }
    }
    return;
  }

  res.writeHead(404).end("Not Found");
}).listen(port, () => {
  console.log("__APP_TITLE__ MCP server listening on http://localhost:" + port + MCP_PATH);
});
`;

function buildWidgetHtml(appSlug, appTitle, toolName) {
  return fillTemplate(WIDGET_TEMPLATE, {
    "__APP_SLUG__": appSlug,
    "__APP_TITLE__": appTitle,
    "__TOOL_NAME__": toolName,
  });
}

function buildServerTs(appSlug, appTitle, toolName, widgetUri, port) {
  return fillTemplate(SERVER_TEMPLATE, {
    "__APP_SLUG__": appSlug,
    "__APP_TITLE__": appTitle,
    "__TOOL_NAME__": toolName,
    "__WIDGET_URI__": widgetUri,
    "__PORT__": String(port),
  });
}

function usage() {
  return [
    "Generate a minimal Node + @modelcontextprotocol/ext-apps starter with a vanilla widget that uses the MCP Apps bridge by default.",
    "Prefer upstream examples first; use this scaffold as the fallback.",
    "",
    "Usage:",
    "  ./scripts/scaffold_node_ext_apps.mjs <output_dir> [--app-name <name>] [--tool-name <name>] [--port <number>] [--force]",
    "",
    "If the executable bit is unavailable, run:",
    "  node scripts/scaffold_node_ext_apps.mjs <output_dir> [--app-name <name>] [--tool-name <name>] [--port <number>] [--force]",
  ].join("\\n");
}

function parseArgs(argv) {
  const args = {
    outputDir: null,
    appName: "example-chatgpt-app",
    toolName: null,
    port: 8787,
    force: false,
  };

  const tokens = [...argv];
  while (tokens.length > 0) {
    const token = tokens.shift();

    if (!args.outputDir && !token.startsWith("--")) {
      args.outputDir = token;
      continue;
    }

    if (token === "--app-name") {
      args.appName = tokens.shift() ?? "";
      continue;
    }

    if (token === "--tool-name") {
      args.toolName = tokens.shift() ?? "";
      continue;
    }

    if (token === "--port") {
      const value = Number(tokens.shift());
      if (!Number.isInteger(value) || value <= 0) {
        throw new Error("Expected a positive integer after --port");
      }
      args.port = value;
      continue;
    }

    if (token === "--force") {
      args.force = true;
      continue;
    }

    if (token === "--help" || token === "-h") {
      console.log(usage());
      process.exit(0);
    }

    throw new Error(`Unknown argument: ${token}`);
  }

  if (!args.outputDir) {
    throw new Error(`Missing required output directory.\\n\\n${usage()}`);
  }

  return args;
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  const appSlug = toSlug(args.appName);
  const toolName = toToolName(args.toolName || appSlug);
  const appTitle = toTitle(appSlug);
  const widgetUri = "ui://widget/main-v1.html";

  const outputDir = path.resolve(args.outputDir);
  ensureTargetDir(outputDir, args.force);

  const files = new Map([
    [path.join(outputDir, "package.json"), buildPackageJson(appSlug)],
    [path.join(outputDir, "tsconfig.json"), buildTsconfig()],
    [path.join(outputDir, "public", "widget.html"), buildWidgetHtml(appSlug, appTitle, toolName)],
    [path.join(outputDir, "src", "server.ts"), buildServerTs(appSlug, appTitle, toolName, widgetUri, args.port)],
  ]);

  for (const [filePath, content] of files) {
    writeFile(filePath, content);
  }

  console.log("Generated starter scaffold:");
  for (const filePath of files.keys()) {
    console.log(" -", path.relative(outputDir, filePath));
  }
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}

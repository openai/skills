# Openai-bundled Plugin Architecture

## Overview

The openai-bundled plugins work through these interconnected components:

```
Chrome Extension 1.1.5  ←→  extension-host.exe  ←→  Codex Desktop App
        ↕                          ↕
  Native Messaging            node_repl MCP Server
        ↕                          ↕
  Native Messaging         browser-client.mjs / computer-use-client.mjs
  Host Manifest
        ↕
  Windows Registry
```

## Component Details

### 1. config.toml (`~/.codex/config.toml`)

Plugin enablement switch. Each plugin needs a separate `[plugins."<name>@<marketplace>"]` section with `enabled = true`.

```toml
[plugins."chrome@openai-bundled"]
enabled = true

[plugins."computer-use@openai-bundled"]
enabled = true
```

`browser@openai-bundled` is a legacy alias; the current plugin name is `chrome`.

### 2. Plugin Cache (`~/.codex/plugins/cache/openai-bundled/`)

Stores downloaded plugin files organized by `name/version/`:

```
chrome/26.601.21317/
├── .codex-plugin/plugin.json       # plugin metadata
├── scripts/                        # browser control JS
│   ├── browser-client.mjs          # Chrome control core
│   ├── check-*.js                  # environment checks
│   ├── extension-id.json           # EXT ID: hehggadaopoacecdllhhajmbjkdcmajg
│   ├── open-chrome-window.js       # open Chrome
│   └── installManifest.mjs         # native host manifest installer
├── extension-host/                 # native messaging host binary
│   └── windows/x64/extension-host.exe
├── skills/                         # skill definitions
├── assets/                         # icons, etc.
└── docs/
```

```
computer-use/26.601.21317/
├── .codex-plugin/plugin.json
├── scripts/computer-use-client.mjs  # desktop control core (depends on @oai/sky)
├── node_modules/@oai/sky/           # Computer Use runtime
├── skills/computer-use/SKILL.md
└── assets/app-icon.png
```

### 3. `latest` Junction

`plugins/cache/openai-bundled/chrome/latest` is an NTFS junction pointing to the versioned plugin directory:
- **Correct**: → `.../cache/openai-bundled/chrome/26.601.21317` (full plugin)
- **Wrong**: → `.../.tmp/bundled-marketplaces/.../chrome` (extension-host only)

This path is referenced by:
- `chrome-native-hosts-v2.json` → `browserClientPath` and `extensionHostPath`
- `com.openai.codexextension.json` → `path`

### 4. Marketplace Source (`~/.codex/.tmp/bundled-marketplaces/openai-bundled/plugins/`)

Codex desktop scans this directory to discover available plugins. Each plugin needs its own subdirectory with required files.

**Note**: The `CodexSandboxUsers` group has only RX permissions here. Sandboxed processes cannot write to this directory — operations require escalation.

### 5. Native Host Manifest

- **Registry**: `HKCU:\SOFTWARE\Google\Chrome\NativeMessagingHosts\com.openai.codexextension`
- **Manifest file**: `%LOCALAPPDATA%\OpenAI\extension\com.openai.codexextension.json`
- **Purpose**: Defines the communication channel between the Chrome extension and extension-host.exe

### 6. Chrome Extension (Codex 1.1.5)

- **Install path**: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions\hehggadaopoacecdllhhajmbjkdcmajg\1.1.5_0`
- **Extension ID**: `hehggadaopoacecdllhhajmbjkdcmajg`
- **Native Host Name**: `com.openai.codexextension`
- **Permissions**: nativeMessaging, debugger, tabs, scripting, alarms, etc.

### 7. V2 Native Host Manifest (`%LOCALAPPDATA%\OpenAI\Codex\chrome-native-hosts-v2.json`)

Records runtime environment paths. Key fields:
- `browserClientPath`: path to browser-client.mjs
- `extensionHostPath`: path to extension-host.exe
- `extensionIds`: Chrome extension ID list
- `nativeHostNames`: native messaging host name

### 8. node_repl MCP Server

Launched from `node_repl.exe`, handles plugin script loading and execution. Environment variables configured in `config.toml` under `[mcp_servers.node_repl.env]`:
- `BROWSER_USE_AVAILABLE_BACKENDS`: "chrome,iab" — enables Chrome and in-app browser
- `NODE_REPL_TRUSTED_BROWSER_CLIENT_SHA256S`: trusted SHA256 hashes for browser-client.mjs

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---|---|---|
| Chrome plugin unresponsive | `latest` junction points to marketplace source | Recreate junction pointing to cache or copy full plugin structure to marketplace |
| computer-use not appearing | Marketplace source missing computer-use directory | Copy complete plugin structure from cache |
| @chrome/@computer-use not triggered | config.toml missing plugin entries | Add `[plugins."..."] enabled = true` |
| extension-host not starting | Native host manifest path wrong or Chrome extension not installed | Reinstall extension or update manifest |
| browser-client load failure | `latest` junction wrong location, browser-client.mjs not at target | Fix junction target |
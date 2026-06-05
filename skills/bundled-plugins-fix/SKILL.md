---
name: bundled-plugins-fix
description: Diagnose and fix issues with openai-bundled plugins (chrome@openai-bundled, computer-use@openai-bundled) in the Codex desktop app on Windows. Use when the user reports that bundled plugins are not working, not loading, not responding, or showing errors. Covers checking: marketplace source structure for missing computer-use entries, plugin cache integrity, chrome latest junction/symlink targets, native host manifests, Chrome extension status, Windows registry for NativeMessagingHosts, and config.toml plugin enablement. Does NOT cover: non-openai-bundled plugins, macOS/Linux-specific issues, or general Codex CLI setup.
---

# Openai-bundled Plugins Diagnostics & Repair

Diagnose and repair common issues with `chrome@openai-bundled` and `computer-use@openai-bundled` plugins in the Codex desktop app for Windows.

## When to use

Users reporting these symptoms may have broken bundled plugins:
- "chrome plugin not working" / "computer use plugin doesn't respond"
- "@chrome doesn't do anything" / "computer use has no effect"
- "Plugins not showing in the list"
- "Chrome control is unresponsive"
- "Desktop control unavailable"

## Diagnostic steps

### 1. Check config.toml for plugin enablement

**File**: `~/.codex/config.toml`

Required entries:
```toml
[plugins."chrome@openai-bundled"]
enabled = true

[plugins."computer-use@openai-bundled"]
enabled = true
```

**Common issue**: Only the legacy `[plugins."browser@openai-bundled"]` exists; `chrome` and `computer-use` sections are missing.

**Fix**: Add the two sections above.

### 2. Check the chrome latest junction

**Path**: `~/.codex/plugins/cache/openai-bundled/chrome/latest`

This NTFS junction must point to the versioned plugin cache directory (e.g. `.../chrome/26.601.21317`), **not** to the marketplace source directory (`.tmp/bundled-marketplaces/...`).

**Verify** (PowerShell):
```powershell
(Get-Item "...\chrome\latest").Target
Test-Path "$target\.codex-plugin\plugin.json"
```

**Fix**: If the junction points to the marketplace source:
```powershell
# Stop extension-host to release the junction
Stop-Process -Name extension-host -Force

# Remove and recreate
cmd /c "rmdir `"...\chrome\latest`""
cmd /c "mklink /J `"...\chrome\latest`" `"...\chrome\26.601.21317`""
```

Alternatively, copy the full plugin structure into the marketplace source:
```powershell
Copy-Item "...\chrome\26.601.21317" "...\.tmp\bundled-marketplaces\openai-bundled\plugins\chrome\" -Recurse -Force
```

### 3. Check marketplace source completeness

**Path**: `~/.codex/.tmp/bundled-marketplaces/openai-bundled/plugins/`

Required structure:
```
plugins/
├── chrome/
│   ├── .codex-plugin/plugin.json
│   ├── extension-host/windows/x64/extension-host.exe
│   ├── scripts/browser-client.mjs
│   └── skills/control-chrome/SKILL.md
└── computer-use/
    ├── .codex-plugin/plugin.json
    ├── scripts/computer-use-client.mjs
    ├── node_modules/@oai/sky/package.json
    ├── assets/app-icon.png
    └── skills/computer-use/SKILL.md
```

**Fix**: Copy missing files from the plugin cache at `plugins/cache/openai-bundled/`:
```powershell
Copy-Item "...\cache\openai-bundled\chrome\26.601.21317\scripts" "...\.tmp\...\plugins\chrome\" -Recurse -Force
Copy-Item "...\cache\openai-bundled\computer-use\26.601.21317" "...\.tmp\...\plugins\computer-use\" -Recurse -Force
```

### 4. Check native host registration

**Registry**: `HKCU:\SOFTWARE\Google\Chrome\NativeMessagingHosts\com.openai.codexextension`

The `(default)` value should point to:
```
%LOCALAPPDATA%\OpenAI\extension\com.openai.codexextension.json
```

**Manifest file** content:
```json
{
  "name": "com.openai.codexextension",
  "description": "Codex chrome native messaging host",
  "path": "C:\\Users\\<user>\\.codex\\plugins\\cache\\openai-bundled\\chrome\\latest\\extension-host\\windows\\x64\\extension-host.exe",
  "type": "stdio",
  "allowed_origins": ["chrome-extension://hehggadaopoacecdllhhajmbjkdcmajg/"]
}
```

### 5. Check Chrome extension

- **Extension ID**: `hehggadaopoacecdllhhajmbjkdcmajg`
- **Install path**: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions\hehggadaopoacecdllhhajmbjkdcmajg\1.1.5_0`
- **Native host name**: `com.openai.codexextension`

Verify the extension is installed in Chrome by navigating to `chrome://extensions/` and looking for "Codex".

### 6. Check extension-host process

A running `extension-host.exe` confirms the native messaging channel is active:
```powershell
Get-Process -Name extension-host
```

If the process is stopped, restart Codex desktop or trigger a Chrome plugin action to auto-launch it.

## Using the diagnostic script

```bash
node ~/.codex/skills/bundled-plugins-fix/scripts/diagnose.mjs
```

Run before and after repairs to confirm all 25 checks pass. The script checks everything listed above in one pass.

## Architecture reference

See `references/architecture.md` for a detailed component map of how openai-bundled plugins connect.
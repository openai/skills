---
name: myvibe-publish
description: Deploy web projects to MyVibe. Use when the user asks to publish, deploy, or host web content (HTML, ZIP, directory, or URL) on MyVibe.
---

# MyVibe Publish

Deploy any web project to [MyVibe](https://www.myvibe.so) instantly. Supports HTML files, ZIP archives, directories, and URL imports with automatic project type detection.

## Prerequisites

- Node.js 18 or later
- When sandboxing blocks deployment network calls, rerun with `sandbox_permissions=require_escalated`.
- The deployment and screenshot generation may take a few minutes. Use a 10-minute (600000ms) timeout for publish commands.

## Quick Start

**Just run this (with a 10-minute timeout):**
```bash
node scripts/publish.mjs --dir ./dist
```

If dependencies are missing, install them first:
```bash
cd scripts && npm install && cd ..
```

## Options

| Option | Alias | Description |
|--------|-------|-------------|
| `--file <path>` | `-f` | Path to HTML file or ZIP archive |
| `--dir <path>` | `-d` | Directory to compress and publish |
| `--url <url>` | `-u` | URL to import and publish |
| `--hub <url>` | `-h` | MyVibe URL (default: https://www.myvibe.so/) |
| `--title <title>` | `-t` | Project title |
| `--desc <desc>` | | Project description |
| `--visibility <vis>` | `-v` | Visibility: public or private (default: public) |
| `--did <did>` | | Vibe DID for version update (overrides auto-detection) |
| `--new` | | Force create new Vibe, ignore publish history |

## Workflow Overview

1. **Detect Project Type** - if no build needed, start screenshot in background
2. **Build** (if needed) - then start screenshot in background
3. **Metadata Analysis** - extract title, description, tags
4. **Confirm Publish** - show metadata, get user confirmation
5. **Execute Publish** - script auto-reads screenshot result
6. **Return Result** - show publish URL

**Before proceeding, gather the following information:**
- Read the source file or main files in the directory
- Run: `git remote get-url origin 2>/dev/null || echo "Not a git repo"`
- Run: `node scripts/utils/fetch-tags.mjs --hub {hub}`

---

## Step 1: Detect Project Type

| Check | Project Type | Next Step |
|-------|-------------|-----------|
| `--file` with HTML/ZIP | **Single File** | Start screenshot, then Step 3 |
| Has `dist/`, `build/`, or `out/` with index.html | **Pre-built** | Step 2 (confirm rebuild) |
| Has `package.json` with build script, no output | **Buildable** | Step 2 (build first) |
| Multiple `package.json` or workspace config | **Monorepo** | Step 2 (select app) |
| Has `index.html` at root, no `package.json` | **Static** | Start screenshot, then Step 3 |

**Start screenshot for non-build projects** (run in the background):

For directory source (`--dir`):
```bash
node scripts/utils/generate-screenshot.mjs --dir {publish_target} --hub {hub}
```

For single file source (`--file`):
```bash
node scripts/utils/generate-screenshot.mjs --file {publish_target} --hub {hub}
```

IMPORTANT: Use `--file` when the source is a single HTML file, and `--dir` when it is a directory. The flag must match the `source.type` in the publish config so that both scripts calculate the same hash for the screenshot result file.

---

## Step 2: Build (if needed)

Detect package manager from lock files, build command from package.json scripts.

Ask the user to confirm:
- **Pre-built**: "Rebuild or use existing output?"
- **Buildable**: "Build before publishing?"
- **Monorepo**: "Which app to publish?"

After build completes, start screenshot in the background, then proceed to Step 3.

---

## Step 3: Metadata Analysis

### Extract title
Priority: `<title>` → `og:title` → package.json name → first `<h1>`

### Generate description (50-150 words, story-style)

Cover: **Why** (motivation) → **What** (functionality) → **Journey** (optional)

Sources: conversation history, README.md, source code, package.json, git log

Guidelines:
- Natural, conversational tone
- Focus on value and story, not technical specs
- Avoid generic "A web app built with React"

### Extract githubRepo
From git remote or package.json repository field. Convert SSH to HTTPS format.

### Match tags

Fetch tags: `node scripts/utils/fetch-tags.mjs --hub {hub}`

| Tag Type | Match Method |
|----------|--------------|
| **techStackTags** | Match package.json dependencies against tag slug |
| **platformTags** | From conversation context (Codex, Claude Code, Cursor, etc.) |
| **modelTags** | From conversation context (GPT-4, Claude 3.5, etc.) |
| **categoryTags** | Infer from project (game libs → game, charts → viz) |

---

## Step 4: Confirm Publish

Display metadata and ask the user for confirmation:

```
Publishing to MyVibe:
──────────────────────
Title: [value]

Description:
[50-150 word story]

GitHub: [URL or "Not detected"]
Cover Image: [Will be included if ready]

Tags: Tech Stack: [...] | Platform: [...] | Category: [...] | Model: [...]
```

Options: "Publish" / "Edit details"

---

## Step 5: Execute Publish

**Check dependencies**: If `scripts/node_modules` missing, run `npm install` first.
**No need to check screenshot background task result** - the publish script automatically waits for and reads the screenshot result. Execute publish directly:

Pass config via stdin:

```bash
node scripts/publish.mjs --config-stdin <<'EOF'
{
  "source": { "type": "dir", "path": "./dist", "did": "z2qaXXXX" },
  "hub": "https://www.myvibe.so",
  "metadata": {
    "title": "My App",
    "description": "Story description here",
    "visibility": "public",
    "githubRepo": "https://github.com/user/repo",
    "platformTags": [1, 2],
    "techStackTags": [3, 4],
    "categoryTags": [5],
    "modelTags": [6]
  }
}
EOF
```

- `did` optional - for explicit version updates
- `coverImage` auto-read from `/tmp/myvibe-screenshot-{hash}.json`
- Screenshot result file cleaned up after publish

---

## Step 6: Return Result

After publish script completes, **check the script output** for these messages:

### Success Message
Always include the Vibe URL in your response:
```
Published successfully!
[URL]
```

### Upgrade Prompt (Important)
The script prints an upgrade prompt when updating an existing Vibe without version history enabled:
```
Previous version overwritten. Want to keep version history?
Upgrade to Creator at {hub}/pricing
```

**You MUST include this upgrade information in your response to the user if the script output contains it.** This helps free-tier users discover the version history feature.

---

## Error Handling

| Error | Action |
|-------|--------|
| Dependencies missing | Run `npm install` in scripts directory |
| 401/403 Auth error | Token auto-cleared, re-run to authorize |
| Build failed | Analyze error, offer fix, or publish source as-is |
| Screenshot failed | Skip coverImage, proceed without it |
| agent-browser missing | Run `npm install -g agent-browser && agent-browser install` |
| Private mode error | See "Private Mode Error Handling" below |

### Private Mode Error Handling

When publishing with `visibility: private` fails with "Private mode is only available for Creator and Studio users", ask the user how they would like to proceed:

**Question:** "Private publishing requires a Creator or Studio subscription. How would you like to proceed?"

| Option | Label | Description |
|--------|-------|-------------|
| 1 | Publish as Public | Your Vibe will be visible to everyone. You can change this later after upgrading. |
| 2 | View Upgrade Options | Open the pricing page to explore subscription plans with private publishing. |

**Actions based on selection:**
- **Option 1**: Re-run publish with `visibility: "public"`, inform user the Vibe is now public
- **Option 2**: Display the pricing URL `{hub}/pricing` and stop the publish flow

## Notes

- Always analyze content for meaningful title/description - never use directory names
- Confirm with user before publishing
- Default hub: https://www.myvibe.so/
- Tags cached 7 days locally
- Publish history in `~/.myvibe/published.yaml` for auto version updates
- Use `--new` to force new Vibe instead of updating

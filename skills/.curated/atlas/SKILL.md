---
name: "atlas"
description: "macOS-only AppleScript control for the ChatGPT Atlas desktop app. Use only when the user explicitly asks to control Atlas tabs/bookmarks/history on macOS and the \"ChatGPT Atlas\" app is installed; do not trigger for general browser tasks or non-macOS environments."
---


# Atlas Control (macOS)

Use the bundled CLI to control Atlas and inspect local browser data.

## Quick Start

Set a stable path to the CLI:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export ATLAS_CLI="$CODEX_HOME/skills/atlas/scripts/atlas_cli.py"
```

User-scoped skills install under `$CODEX_HOME/skills` (default: `~/.codex/skills`).

Then run:

```bash
uv run --python 3.12 python "$ATLAS_CLI" app-name
uv run --python 3.12 python "$ATLAS_CLI" tabs --json
```

The CLI requires the Atlas app bundle in `/Applications` or `~/Applications`:

- `ChatGPT Atlas`

If AppleScript fails with a permissions error, grant Automation permission in System Settings > Privacy & Security > Automation, allowing your terminal to control ChatGPT Atlas.

## Tabs Workflow

1. List tabs to get `window_id` and `tab_index`:

```bash
uv run --python 3.12 python "$ATLAS_CLI" tabs
```

2. Focus a tab using the `window_id` and `tab_index` from the listing:

```bash
uv run --python 3.12 python "$ATLAS_CLI" focus-tab <window_id> <tab_index>
```

3. Open a new tab:

```bash
uv run --python 3.12 python "$ATLAS_CLI" open-tab "https://chatgpt.com/"
```

Optional maintenance commands:

```bash
uv run --python 3.12 python "$ATLAS_CLI" reload-tab <window_id> <tab_index>
uv run --python 3.12 python "$ATLAS_CLI" close-tab <window_id> <tab_index>
```

## Bookmarks and History

Atlas stores Chromium-style profile data under `~/Library/Application Support/com.openai.atlas/browser-data/host/`.

List bookmarks:

```bash
uv run --python 3.12 python "$ATLAS_CLI" bookmarks --limit 100
```

Search bookmarks:

```bash
uv run --python 3.12 python "$ATLAS_CLI" bookmarks --search "docs"
```

Search history:

```bash
uv run --python 3.12 python "$ATLAS_CLI" history --search "openai docs" --limit 50
```

History for today (local time):

```bash
uv run --python 3.12 python "$ATLAS_CLI" history --today --limit 200 --json
```

The history command copies the SQLite database to a temporary location to avoid lock errors.

If history looks stale or empty, ask the user which Atlas install they are using, then check both Atlas data roots and inspect the one with the most recent `History` file:

- `~/Library/Application Support/com.openai.atlas/browser-data/host/`
- `~/Library/Application Support/com.openai.atlas.beta/browser-data/host/`

## References

Read `references/atlas-data.md` in the skill folder (for example, `$CODEX_HOME/skills/atlas/references/atlas-data.md`) when adjusting data paths or timestamps.

---
name: "codex-wrapped"
description: "Generate a Codex Wrapped usage recap from local Codex logs, including last 30 days, last 7 days, and an all-time focus-hours callout. Use when the user asks for a usage summary, activity recap, or Codex Wrapped report."
---


# Codex Wrapped

Use this skill whenever the user wants a Codex Wrapped report or usage insights. Render text-only output (no image generation).

The report must be year-agnostic and should highlight last 30 days and last 7 days, while still calling out all-time focus hours.

## Quick Commands (run in order)

1) **Compute stats**
```bash
python3 .codex/skills/codex-wrapped/scripts/get_codex_stats.py \
  --output /tmp/wrapped_stats.json
```
(Defaults to the system timezone; override `--timezone` only if the user requests it.)

2) **Render text report**
```bash
.codex/skills/codex-wrapped/scripts/report.sh \
  --stats-file /tmp/wrapped_stats.json
```
This prints the report directly to stdout.

## Files
- `scripts/get_codex_stats.py` -- computes rolling-window stats to `/tmp/wrapped_stats.json`.
- `scripts/report.sh` -- text report renderer.

## Responding to the user
- Paste the report text exactly as printed, wrapped in triple backticks (```), to preserve spacing/box drawing.
- If something fails, state what you ran and the error.

## Notes
- Keep `/tmp/wrapped_stats.json` unless sensitive; rerun stats if outdated.
- The report adapts to terminal width. Set `WRAPPED_WIDTH=120` (or similar) to force a wider layout.
- Layout options: default is `columns` (two-column). Use `--layout table` (or `WRAPPED_LAYOUT=table`) to switch back to the compact grid.

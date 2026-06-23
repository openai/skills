---
name: token-usage-report
description: >-
  Summarize Codex token usage from local rollout logs across all projects and
  sessions for a target date. Trigger when user asks for token totals/usages in
  Chinese or English, e.g. "统计 token", "今天总共用了多少 token", "所有项目所有
  session 的 token", "token usage today", "how many tokens did I use today",
  "all projects all sessions token usage", or per-project token breakdown.
---

# Token Usage Report

## Overview

Use this skill to compute token usage totals from local Codex rollout logs:
`~/.codex/sessions/**/rollout-*.jsonl`.

This skill is designed for accurate day-level summaries across all projects and
sessions, including sessions created on previous days but used on the target day.

## Workflow

1. Resolve date and timezone.
- If user says "today", use current local date.
- Prefer explicit `YYYY-MM-DD` when user gives relative dates.

2. Run the bundled script.
- Text summary:
  - `bun ~/.codex/skills/token-usage-report/scripts/report-token-usage.mjs --date YYYY-MM-DD --timezone Asia/Shanghai`
- JSON output:
  - `bun ~/.codex/skills/token-usage-report/scripts/report-token-usage.mjs --date YYYY-MM-DD --timezone Asia/Shanghai --json`

3. Return concise results.
- Always include: total tokens, sessions count, per-project totals.
- Include top sessions when helpful.

## Script Options

- `--date YYYY-MM-DD`: target date (default: today in selected timezone)
- `--timezone IANA_TZ`: timezone, e.g. `Asia/Shanghai`
- `--sessions-root PATH`: custom sessions root (default `~/.codex/sessions`)
- `--limit N`: top session rows in text mode (default `20`)
- `--json`: print machine-readable JSON

## Notes

- The script merges token events across rollout files by `sessionId` before counting.
- Day usage is computed from cumulative totals using monotonic increments to avoid
  double counting in resumed sessions.

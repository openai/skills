---
name: rlhf-feedback-loop
description: Capture thumbs up/down feedback, block repeated mistakes, recall past learnings, and export DPO training pairs. Activate when the user says thumbs up, thumbs down, that worked, that failed, or asks to recall past feedback.
---

# RLHF Feedback Loop

Persistent feedback capture and recall for AI coding agents. This skill gives Codex memory of what worked and what failed across sessions.

## How to Use

### Capture Feedback

When the user gives explicit positive or negative feedback:

```bash
npx -y rlhf-feedback-loop capture --feedback=up --context="description of what worked" --tags="relevant,tags"
npx -y rlhf-feedback-loop capture --feedback=down --context="description of failure" --what-went-wrong="root cause" --what-to-change="fix" --tags="relevant,tags"
```

### Recall Past Feedback

Before starting any non-trivial task, check for relevant past feedback:

```bash
npx -y rlhf-feedback-loop stats
```

### Generate Prevention Rules

After accumulating negative feedback, generate guardrails:

```bash
npx -y rlhf-feedback-loop rules
```

### Export DPO Training Pairs

Export preference pairs for model fine-tuning:

```bash
npx -y rlhf-feedback-loop export-dpo
```

## MCP Server (Recommended)

For real-time in-session recall, use the MCP server:

```bash
codex mcp add rlhf -- npx -y rlhf-feedback-loop serve
```

This exposes 11 tools including `recall`, `capture_feedback`, `prevention_rules`, and `export_dpo_pairs`.

## Rules

1. ALWAYS capture feedback when the user says "thumbs up", "thumbs down", "that worked", "that failed", or similar.
2. ALWAYS include context describing what happened and relevant tags.
3. For negative feedback, ALWAYS include `--what-went-wrong` and `--what-to-change`.
4. Before starting complex tasks, check `stats` for patterns of past failures.
5. All data stays local in JSONL files. Nothing is sent to external services.

## References

- `references/architecture.md` — system architecture and data flow

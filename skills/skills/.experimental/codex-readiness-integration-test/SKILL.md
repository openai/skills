---
name: codex-readiness-integration-test
description: Run the Codex Readiness integration test. Use when you need an end-to-end agentic loop with build/test scoring.
metadata:
  short-description: Run Codex Readiness integration test
---

# LLM Codex Readiness Integration Test

This skill runs a multi-stage integration test to validate agentic execution quality. It always runs in execute mode (no read-only mode).

## Outputs

Each run writes to `.codex-readiness-integration-test/<timestamp>/` and updates `.codex-readiness-integration-test/latest.json`.

New outputs per run:
- `agentic_summary.json` and `logs/agentic.log` (agentic loop execution)
- `llm_results.json` (automatic LLM evaluation)
- `summary.txt` (human-readable summary)

## Pre-conditions (Required)

- Authenticate with the Codex CLI using the repo-local HOME before running the test.
  Run these in your own terminal (not via the integration test):
  HOME=$PWD/.codex-home XDG_CACHE_HOME=$PWD/.codex-home/.cache codex login
  HOME=$PWD/.codex-home XDG_CACHE_HOME=$PWD/.codex-home/.cache codex login status
- The integration test creates {repo_root}/.codex-home and {repo_root}/.codex-home/.cache/codex as its first step.

## Workflow

0) Ask the user how to source the task.
   - Offer two explicit options: (a) user provides a custom task/prompt, or (b) auto-generate a task.
   - Do not run the entry point until the user chooses one option.
1) Generate or load `{out_dir}/prompt.pending.json`.
   - Use the integration test's expected prompt path, not `prompt.json` at the repo root.
   - With the default out dir, this path is `.codex-readiness-integration-test/prompt.pending.json`.
   - If `--seed-task` is provided, it is used as the starting task.
   - If not provided, generate a task with `skills/codex-readiness-integration-test/references/generate_prompt.md` and save the JSON to `{out_dir}/prompt.pending.json`.
   - The user must approve the prompt before execution (no auto-approve mode). Make sure to output a summary of the prompt when asking the user to approve.
2) Execute the agentic loop via Codex CLI (uses `AGENTS.md` and `change_prompt`).
3) Run build/test commands from the prompt plan via `skills/codex-readiness-integration-test/scripts/run_plan.py`.
4) Collect evidence (`evidence.json`), deterministic checks, and run automatic LLM evals via Codex CLI.
5) Score and write the report + summary output.

## Configuration

Optional fields in `{out_dir}/prompt.pending.json`:
- `agentic_loop`: configure Codex CLI invocation for the agentic loop.
- `llm_eval`: configure Codex CLI invocation for automatic evals.

If these fields are omitted, defaults are used.

## Requirements

- The LLM evaluator must fail if evidence mentions the phrase `Context compaction enabled`.
- Use qualitative context-usage evaluation (no strict thresholds).


## What this test covers well

- Runs Codex CLI against the real repo root, producing real filesystem edits and git diffs.
- Executes the approved change prompt and then runs the build/test plan in-repo.
- Captures evidence, deterministic checks, and LLM eval artifacts for review.

## What this test does not represent

- The agentic loop may use non-default flags (e.g., bypass approvals/sandbox), so interactive guardrails differ.
- Uses a dedicated HOME (`.codex-home`), which can change auth/config/cache vs normal CLI use.
- Auto-generated prompts and one-shot execution do not simulate interactive guidance.
- MCP servers/tools are not exercised unless explicitly configured.

## Notes

- The prompts in `skills/codex-readiness-integration-test/references/` expect strict JSON.
- Use `skills/codex-readiness-integration-test/references/json_fix.md` to repair invalid JSON output.
- This skill calls the `codex` CLI. Ensure it is installed and available on PATH, or override the command in `{out_dir}/prompt.pending.json`.
- If the agentic loop detects sandbox-blocked tool access, it now writes `requires_escalation: true` to `{run_dir}/agentic_summary.json` and exits with code `3`. Re-run the integration test with escalated permissions in that case.

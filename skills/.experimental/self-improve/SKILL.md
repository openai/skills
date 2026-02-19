---
name: self-improve
description: Run a minimal self-improvement loop with one bounded change per iteration, smoke+regression acceptance gates, and durable decision logging through auto-memory. Use when users ask for iterative improvement of prompts, workflows, or code quality over time.
---

# Self Improve

Use this skill to run deterministic, test-gated improvement iterations.
This skill is standalone first, with optional integrations for `auto-memory` and `ralph-wiggum-loop`.

## Setup

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export SELF_IMPROVE_DIR="$CODEX_HOME/skills/self-improve"
export AUTO_MEMORY_DIR="$CODEX_HOME/skills/auto-memory"
```

## Standalone Workflow

1. Define objective + two required gates:
   - `smoke_command` (required)
   - `regression_command` (required)
2. Produce exactly one bounded change plan using `references/prompt-contract.md`.
3. Execute exactly one change-set.
4. Run exactly one verification pass for each gate.
5. Decision rule:
   - Accept only if both gates pass.
   - Reject if either gate fails.
6. Persist iteration outcome:
   - Preferred: save with optional auto-memory integration (below).
   - Fallback: write local note in `.self-improve/memory/` (contract below).

## Local Fallback Memory Contract

When auto-memory is unavailable, create:
- directory: `.self-improve/memory/`
- file name: `<timestamp>-iteration.md` (for example `20260218-182500-iteration.md`)
- required sections:
  - `Summary`
  - `Context`
  - `Decision`
  - `Rationale`
  - `Implementation`
  - `Verification`
  - `Follow-ups`
  - `Changelog`

Include:
- objective
- planned change (one change-set only)
- smoke/regression command + exit code evidence
- accept/reject decision reason tied to gate outcomes

## Optional Auto-memory Integration

Load prior memory before proposing changes:

```bash
python3 "$AUTO_MEMORY_DIR/scripts/load_memory.py" \
  --project "<project>" \
  --query "<objective> decisions regressions known-good commands" \
  --limit 8
```

Persist durable outcome:

```bash
python3 "$AUTO_MEMORY_DIR/scripts/save_memory.py" \
  --project "<project>" \
  --title "<repo>: self-improve iteration <id>" \
  --strict-sections \
  --body "<memory note body>" \
  --tags "self-improve,decision,eval"
```

Compaction handoff (optional integration):

```bash
python3 "$AUTO_MEMORY_DIR/scripts/compaction_handoff.py" \
  --project "<project>" \
  --mode pre \
  --objective "<objective>" \
  --summary "<state and blockers>"
```

```bash
python3 "$AUTO_MEMORY_DIR/scripts/compaction_handoff.py" \
  --project "<project>" \
  --mode post \
  --objective "<objective>"
```

Use returned `reinjection_prompt` as first payload after compaction.

## Optional Ralph Integration

Use Ralph as the change executor while keeping this skill as the decision policy:
- run Ralph with `max_iterations=1`
- allow edits only in approved paths
- apply self-improve gates after each Ralph run
- accept/reject using the same two-gate rule

## Secret Safety

Never store secret values in markdown memory notes.
When secret persistence is required:

```bash
python3 "$AUTO_MEMORY_DIR/scripts/store_secret_env.py" \
  --project "<project>" \
  --var "<ENV_NAME>" \
  --value-file /path/to/secret.txt
```

## References

- `references/prompt-contract.md`
- `references/eval-criteria.md`
- `references/auto-memory-integration.md`

## Agent Team Protocol Review Adapter (2026-02-19)

When used with `/Users/maleick/.codex/skills/agent-team-protocol`, `self-improve` is the acceptance gate owner.

- Enforce reviewer separation (no self-approval).
- Keep existing smoke+regression dual-gate decision contract.
- On conflicting review outcomes, escalate and stop instead of retrying in-loop.

Reference: `references/agent-team-review-gate.md`

Optional policy CLI:

```bash
python3 "$SELF_IMPROVE_DIR/scripts/agent_team_review_gate.py" \
  --decision accept \
  --smoke-status pass \
  --regression-status fail \
  --author-id builder-01 \
  --final-reviewer-id reviewer-01 \
  --enforce-reviewer-separation \
  --reviewer-decision reviewer-01:accept \
  --reviewer-decision reviewer-02:reject
```

---
name: relicta-release-governance
description: Operate Relicta release workflows end-to-end with governance and safety checks. Use when working in repositories that use `relicta` and `.relicta.yaml` for version planning, bumping, notes generation, approval, publishing, plugin setup, MCP usage, policy checks, dashboard operations, and release troubleshooting.
---

# Relicta Release Governance

## Overview
Drive Relicta from intent to published release with predictable command order, explicit guardrails, and fast recovery for common failure modes.

## Quick Start
Run these commands in repository root:

```bash
relicta init
relicta plan
relicta bump
relicta notes
relicta approve
relicta publish
```

Use one-command mode when appropriate:

```bash
relicta release
```

Use dry-run for safe previews:

```bash
relicta release --dry-run
```

## Workflow
1. Validate environment.
2. Establish or confirm config.
3. Plan and inspect risk.
4. Version and generate notes.
5. Approve and publish.
6. Verify outputs and recover if needed.

## Step 1: Validate Environment
Run:

```bash
relicta version
relicta health
git status --short
```

Expect:
- `relicta` available and healthy.
- Repository is correct.
- Working tree state is understood before release actions.

## Step 2: Confirm Configuration
Use `.relicta.yaml` as the canonical config file name.

If missing:

```bash
relicta init
```

Confirm critical sections:
- `versioning`
- `workflow`
- `plugins`
- `governance`
- `dashboard` (if serving UI)

## Step 3: Plan and Risk Review
Run:

```bash
relicta plan --analyze
relicta status
```

Focus on:
- Current and next version.
- Commit count and release type.
- Governance/risk signals before bump/publish.

If no changes are detected, stop release flow.

## Step 4: Version and Notes
Run:

```bash
relicta bump
relicta notes
```

Optional AI notes:

```bash
relicta notes --ai
```

If bump type must be overridden:

```bash
relicta bump --level patch
```

## Step 5: Approval and Publish
Interactive/human-in-the-loop:

```bash
relicta approve
relicta publish
```

CI/non-interactive:

```bash
relicta release --yes --ci
```

If you must create artifacts locally without pushing:

```bash
relicta publish --skip-push
```

## Step 6: Verify and Recover
Run:

```bash
relicta status
relicta history
```

Recovery commands:

```bash
relicta cancel
relicta reset
relicta clean
```

Use these when state is failed/canceled/stale.

## Plugins
Discover and install:

```bash
relicta plugin list --available
relicta plugin install <name>
relicta plugin enable <name>
relicta plugin configure <name>
```

Confirm plugin status:

```bash
relicta plugin list
relicta plugin info <name>
```

## Governance and Policy
Policy lifecycle:

```bash
relicta policy list
relicta policy validate
```

Use `plan --analyze` before approval to surface governance signals.

## MCP and Dashboard
MCP server:

```bash
relicta mcp serve
```

Dashboard server:

```bash
relicta serve
```

Security rule:
- Treat dashboard auth mode `none` as local-development only.
- For shared environments, configure `dashboard.auth.mode: api_key` in `.relicta.yaml`.

## Troubleshooting Playbook
- Error: configuration not found.
  Action: create or point to `.relicta.yaml` via `--config`.
- Error: workflow state mismatch across commands.
  Action: inspect `relicta status`; then `relicta reset` or `relicta clean` and rerun flow.
- Error: plugin not executing.
  Action: verify install (`plugin list`), enable/configure, then retry publish.
- Error: publish blocked by governance.
  Action: inspect `plan --analyze`, adjust policy or perform required approval.

## Output Standards
When assisting users with Relicta tasks:
- Report exact commands run.
- Summarize state transitions and version/tag outcomes.
- Call out whether run was dry-run, local-only, or published.
- Prefer deterministic, auditable steps over speculative advice.

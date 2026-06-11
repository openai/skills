---
name: ariadne-loop
description: Use when a user wants to turn a GitHub issue, release plan, refactor, bugfix, PR follow-up, or long coding-agent handoff into a verifiable Loop Engineering contract with inspect/act/verify/decide steps, evidence gates, rollback rules, human approvals, and JSON agent reports.
metadata:
  short-description: Write verifiable loop specs for coding agents
---

# Ariadne Loop

Use this skill when the user wants a coding agent to work from a bounded loop
contract instead of a loose prompt. The loop contract should make state,
allowed actions, verifiers, stop rules, rollback behavior, and report shape
explicit.

## Good Fits

- turning a GitHub issue into a repair loop,
- preparing a release with verification gates,
- breaking a risky refactor into small verifiable turns,
- following up on PR review comments or failing checks,
- handing a long Codex or Claude Code thread to a fresh agent.

## Workflow

1. Identify the source:
   - issue title and body,
   - release/refactor/bugfix request,
   - PR comments and failing checks,
   - long-thread handoff notes.
2. Write or request a snapshot with:
   - `title`,
   - `goal`,
   - `current_state`,
   - `recent_progress`,
   - `constraints`,
   - `verifiers`,
   - `external_effects`,
   - `risk`.
3. Generate an agent packet that includes:
   - inspect -> act -> verify -> decide,
   - concrete verifiers,
   - stop rules,
   - rollback behavior,
   - human gates for external effects,
   - JSON-only report contract.
4. If the user wants a first-run demo and the Ariadne Loop CLI is installed:

   ```bash
   ariadne-loop quickstart --output .ariadne/quickstart
   ```

   This creates a snapshot, loop JSON, agent packet, sample reports, and a
   supervision decision.

5. For real work, prefer:

   ```bash
   ariadne-loop init --preset bugfix --output loop-snapshot.json
   ariadne-loop make --input loop-snapshot.json --output loop.json --format json
   ariadne-loop make --input loop-snapshot.json --output agent-packet.md --format markdown
   ariadne-loop check --input loop.json
   ```

6. If work starts from an issue body, prefer:

   ```bash
   ariadne-loop from-issue \
     --title "Issue title" \
     --body-file issue.md \
     --output issue-loop.json
   ```

7. If the user has JSONL agent reports, supervise them:

   ```bash
   ariadne-loop supervise \
     --loop loop.json \
     --reports reports.jsonl \
     --output decision.json
   ```

## If the CLI Is Not Installed

Do not block. Produce the snapshot JSON and the agent packet directly. You can
also point the user to the browser builder:

```text
https://zhangzeyu99-web.github.io/ariadne-loop/playground.html
```

Use this report contract:

```json
{
  "action_id": "inspect|act|verify|decide",
  "status": "continue|stop|needs_human|rollback",
  "evidence": ["specific evidence observed in this turn"],
  "next_step": "the next concrete action",
  "passed_verifiers": ["gate ids that passed in this turn"],
  "failed_verifiers": ["gate ids that failed in this turn"]
}
```

## Human Gates

Require human confirmation before:

- commit,
- push,
- tag or release creation,
- package publish,
- deploy,
- deletion,
- sending external messages,
- payment or billing actions.

After any approved external effect, read back the real target before reporting
success.

## Project

Source and examples:
<https://github.com/zhangzeyu99-web/ariadne-loop>

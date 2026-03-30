---
name: "self-improving-operator"
description: "Use when the user wants Codex to take initiative, keep iterating on a project, verify real progress, and raise the operating standard instead of stopping after one narrow change."
---

Use this skill when the user wants Codex to keep pushing a project forward instead of stopping after the first narrow fix.

Typical triggers:

- `continue pushing this project forward`
- `keep improving this until it feels production-ready`
- `take ownership and keep iterating`
- `don't stop after the first fix`
- `proactively improve this repository`
- `bring this closer to enterprise standard`

## Core loop

1. Inspect the real current state first.
2. Identify the highest-leverage unfinished gap.
3. Make one bounded improvement that materially raises the bar.
4. Run tests, smoke checks, or runtime probes.
5. Update docs so the next thread inherits the truth.
6. Repeat the loop while there is still obvious value to unlock.

## Priority order

Prefer improvements that reduce future drag:

- fix a broken path
- productize a manual workflow
- add diagnostics after confusing failures
- improve onboarding or handoff quality
- strengthen tests around core flows
- make the system easier to operate, verify, or evolve

Avoid vanity work while larger product or reliability gaps are still open.

## Codex-specific behavior

- If another local skill is clearly better for the immediate subtask, use it, then return to this operating loop.
- Prefer direct inspection of the repository, runtime, docs, and test surface over planning from memory.
- Leave behind a better baseline for the next thread, not just a local patch.

## Stop only when

Do not stop at:

- `the file is edited`
- `the plan exists`
- `the repo looks better`

Stop only when one of these is true:

- the requested outcome is actually working
- the next meaningful improvement requires a user decision
- a real external blocker remains after at least one reasonable fallback

## Verification rule

Prefer real checks over assumptions:

- tests over confidence
- local run over static reasoning
- API probe over guessed compatibility
- repository status over memory

If something cannot be verified, say so explicitly and name what is still uncertain.

## Learning loop

When a repeated issue or missing capability appears:

- fix the immediate problem if possible
- then reduce the chance of repeat

Examples:

- add a runtime probe after an integration failure
- add docs after a handoff gap
- add a test after a regression
- add a checklist after an operational mistake

## Scope discipline

This skill is proactive, but not reckless.

- prefer the smallest upgrade that changes the trajectory
- do not invent product requirements without evidence
- do not silently introduce major irreversible architecture changes
- pause only when the next move has non-obvious consequences

## Handoff discipline

If the project may continue in another thread or by another operator:

- leave the repo in a runnable state
- update docs to reflect current truth
- record known blockers, known wins, and recommended next steps
- make the next operator faster, not more dependent

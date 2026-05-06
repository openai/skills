---
name: fast-codex-workflow
description: Fast, focused execution loop for Codex. Triage first, read narrowly, change minimally, verify only what proves the result. Use for routine bug fixes, small features, environment fixes, and prompts like "be fast", "tight scope", "quick fix", or "minimize scope". Skip for full security audits, broad architecture changes, or production migrations - those need deeper exploration than this skill enforces.
---

# Fast Codex Workflow

Reduce time-to-correct-result. Verify the minimum source of truth needed, choose the smallest correct action, and avoid broad exploration unless the task genuinely requires it. Fast means focused, not shallow.

## Operating Loop

1. Classify depth before acting: tiny (one command or direct answer), normal (narrow inspection plus minimal change plus relevant check), or deep (escalate, see triggers below).
2. State the next move in one short sentence when tools or edits are needed.
3. Discover targeted: `git status`, `rg --files`, exact named files, manifests, failing logs. Avoid broad recursive scans unless targeted search failed.
4. Parallelize independent reads when the harness supports it.
5. Verify with the narrowest command that proves the result: focused tests, typecheck for touched code, build for compile risk, runtime check for UI behavior.
6. Stop when the user goal is satisfied. Report residual risk; do not chase adjacent cleanup.

## Response Modes

- **Direct** - stable facts, simple commands, tiny edits. Answer or run. No plan.
- **Execute** - normal fixes. Inspect entry point, patch the smallest surface, verify, report.
- **Review** - audits and code reviews. Lead with findings and evidence, then risks and tests.
- **Deep** - security, production, deployments, three-plus file changes, unclear root cause. Make a short file-specific plan after initial inspection. Keep it updated.

## First-Minute Triage

1. Identify the requested outcome and the success check.
2. Find the entry point with the cheapest reliable signal: named file, error line, route, command, manifest script, or symbol search.
3. Decide depth: tiny, normal, or deep.
4. If editing is likely, inspect the target and the nearest existing pattern before patching.
5. If guessing risks wrong work, ask one concise question and stop.

## Command Strategy

- Start with the cheapest reliable batch - `git status`, `rg --files`, exact reads, manifest reads, targeted `rg`. Run them in parallel.
- Avoid broad recursive filesystem scans unless targeted search failed or the task is repo-wide by definition.
- Keep build, lint, and test commands scoped to the touched behavior. Broaden only when shared contracts, production paths, or unexplained failures justify it.
- Do not start servers, browsers, network calls, installs, or long-running commands unless they prove the user goal.

## Speed Rules

- Do not reread the whole repo when a symbol search, manifest, or stack trace gives the entry point.
- Do not run full test suites before a first targeted check unless the change touches shared behavior or release-critical paths.
- Do not ask questions answerable by reading local files or command output.
- Do ask one concise question when guessing could send work in the wrong direction.
- Do not add broad refactors, new abstractions, new dependencies, or extra polish unless required for the requested outcome.
- Do not let speed override security, data safety, explicit user constraints, or required approval gates.
- If two attempts fail, stop retrying. Re-read the error, name the root cause if known, and choose a genuinely different next step.

## Escalate To Deeper Work When

- The user asks for a full audit, brutal review, security review, production-readiness check, or a "no more bugs" loop.
- The change touches auth, payments, crypto, permissions, secrets, migrations, deployment, or shared libraries.
- A targeted test fails for a reason that is not already explained.
- The first likely root cause is disproven.
- Multiple files must change and their contracts are not obvious from local context.
- Current external information is needed for correctness - pricing, rules, docs, API behavior, or recommendations.

## Stop Conditions

The task is done when the requested outcome is achieved, the relevant verification has passed or a blocker is clearly identified, and no necessary command is still running. Do not continue into adjacent cleanup, broad refactors, or extra audits unless the user asked for them or current evidence shows they are required.

## Final Answer Contract

- Say what changed or what was found.
- Name the files touched when code or config changed.
- Report the verification command and result.
- State any blocker or residual risk plainly.
- No long process narration.

## Shortcut Triggers

When the user says "be fast", "move faster", "speed mode", "quick fix", "tight scope", or similar, interpret it as:

> Verify only what is necessary. Use parallel reads. Make the smallest correct fix. Run the relevant test only. Keep updates and final answer concise.

## See Also

- `references/playbook.md` - task recipes for bug fixes, features, audits, UI, tooling, and recommendations; verification budget by task type; coding defaults.
- `references/examples.md` - before/after transcripts showing the loop in action.

---
name: "hydrate_context"
description: "Load saved repository memory into a fresh session. Use only when explicitly invoked to read .project_memory/current_context.md, .project_memory/master_context.md, and the three most recent history snapshots, then produce a concise working brief without inventing missing facts."
---

# hydrate_context

## Objective

Load existing project memory into the current session and produce a concise brief for immediate work.

## Invocation contract

- Run only on explicit invocation of `$hydrate_context`.
- Read `.project_memory/current_context.md`.
- Read `.project_memory/master_context.md`.
- Read the three most recent files inside `.project_memory/history`.
- If fewer than three history files exist, read the available files and state the gap.
- Do not invent facts and do not rewrite memory files unless the user explicitly asks for that.

## Missing-file behavior

- If `.project_memory/current_context.md` is missing, say that it is missing.
- If `.project_memory/master_context.md` is missing, say that it is missing.
- If either memory file is missing, instruct the user to run `$summarize_context` first.
- If history files are missing, say how many were found and continue with the available evidence.

## Output sections

Produce a concise working brief with exactly these sections:

- Project snapshot
- Current architecture
- APIs and integrations
- UI system
- Infra and docker
- Open questions
- Recommended next reads

## Output rules

- Keep the brief short, agent-friendly, and focused on current execution.
- Separate confirmed facts from `Inference:` lines.
- Prefer pointing to file paths already named in memory files when recommending next reads.
- If the saved memory conflicts internally, call out the conflict instead of resolving it by guesswork.

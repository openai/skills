---
name: "multi-turn-consistency-check"
description: "Run a deliberate consistency pass over long, correction-heavy conversations to reduce factual drift, unsupported carry-over, and context confusion. Use when a thread spans multiple turns with changing requirements, ambiguous callbacks to earlier context, conflicting dates, names, IDs, paths, or any answer must separate verified facts from inference before concluding. Prefer explicit invocation for targeted checks. Do not trigger for short self-contained requests or purely creative tasks."
---

# Multi Turn Consistency Check

## Overview

Keep long conversations anchored to the latest confirmed state. Rebuild the active facts from the most recent user instructions, tool outputs, files, and external sources before answering; do not inherit earlier assistant claims as truth.

This skill is single-mode by default: perform an internal consistency pass at answer time. Do not create or maintain a persistent conversation log unless the user explicitly asks for one, or the task is clearly a handoff that benefits from a durable summary.

## Quick Start

1. Rebuild the current state from the latest user turns and fresh evidence.
2. Create a compact internal fact ledger. Always load `references/fact-ledger.md`.
3. Scan for conflicts. Load `references/conflict-signals.md` when the thread is long, corrected, or scope-shifting.
4. Verify unstable claims before concluding.
5. Answer from the ledger and mark assumptions explicitly.

## Rebuild The Current State

- Prefer the latest explicit user instruction over earlier assistant assumptions or plans.
- Treat prior assistant messages as unverified unless they are backed by a file read, command output, cited source, or explicit user statement.
- Re-resolve pronouns and relative references such as "that change", "same as before", "the second option", "today", and "latest" against the current turn.
- When time is involved, anchor the answer to exact dates instead of relying on relative words alone.
- When the request depends on code, reread the relevant files before claiming current behavior or status.

## Build A Fact Ledger

Create a short internal ledger before the final answer. Use the categories from `references/fact-ledger.md`:

- user-stated facts
- verified local facts
- verified external facts
- bounded inferences
- unresolved items

Keep each claim atomic and attach the source mentally or explicitly in the answer when useful. Never silently upgrade an inference into a verified fact.

Do not write this ledger to a markdown file by default. Keep it internal unless the user explicitly requests a written handoff, status record, or persistent working note.

## Check For Conflict Patterns

Use `references/conflict-signals.md` to detect and resolve:

- later user turns that reverse earlier requirements
- mismatched names, IDs, branches, paths, dates, or numbers
- stale plans that survived after scope changed
- assistant claims that were never grounded in evidence
- references to "current", "latest", or "today" that require verification
- entity swaps where the thread changes subject but keeps inherited assumptions

When a conflict exists, say so plainly. Either resolve it from evidence or ask one short blocking question if the answer would otherwise be risky.

## Verify Unstable Or High-Risk Claims

Verify before answering when:

- the user asks for "latest", "current", "today", "recent", prices, schedules, laws, versions, or leadership
- the codebase may have changed since the last read
- the thread contains corrections, retries, or previous failed attempts
- the claim would materially change the recommendation, fix, or plan
- the answer is high-stakes or would spend real time or money

If verification is not possible, say that it is unverified. Do not fill the gap with a confident guess.

## Write The Final Answer

- Lead with the conclusion only after grounding it.
- Distinguish verified statements from inferences in the wording.
- Mention the conflict you resolved when it materially affects the result.
- Keep assumptions short and explicit.
- Cite files, command results, or sources when they are the basis of the answer.
- If the user appears confused about dates, include the exact date in the response.
- Do not repeat a prior assistant error just because it is in the context window.

## Use A Short Correction Pattern

When prior context is wrong or stale:

1. State the conflict.
2. State the current grounded version.
3. State what remains uncertain, if anything.
4. Continue with the answer or next step.

Example phrasing:

- "The thread contains two conflicting branch names. The current repo state shows `release/2026-03`, so I am using that."
- "Earlier in the conversation `X` was treated as completed, but the file still contains the unfinished marker. I am treating it as unfinished."
- "I can answer the rest, but the dependency version is still unverified."

## Stay Proportional

- Use full grounding when stale context could cause a wrong answer, bad edit, or incorrect recommendation.
- Use lighter grounding for short, self-contained, or obviously creative tasks.
- If a single unresolved point blocks a safe answer, ask one short question instead of forcing a complete response.
- Avoid adding process overhead when a quick reread of the relevant context is enough.

## Persistent Notes Are Optional

- Do not create `conversation-ledger.md`, `working-state.md`, or similar files by default.
- Write a persistent note only when the user asks for one, the task requires a handoff, or the thread is long enough that a durable record clearly reduces risk.
- If you do write one, keep it short, factual, and easy to refresh from current evidence.

## Avoid These Failure Modes

- Propagating a prior assistant mistake because it was said confidently.
- Treating plans, examples, or hypothetical options as completed work.
- Assuming the latest user request inherits all earlier constraints when the user has changed direction.
- Answering relative-date questions without converting to exact dates.
- Claiming repo state from memory instead of rereading the relevant files.
- Merging contradictory facts into a single blended answer.

## Reference Map

- `references/fact-ledger.md` -> Use for the minimal ledger format and evidence labels.
- `references/conflict-signals.md` -> Load when the thread is long, corrected, or scope-shifting.

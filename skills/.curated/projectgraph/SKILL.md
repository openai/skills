---
name: projectgraph
description: Use when a user wants to initialize, seed, maintain, review, validate, auto-capture, or multi-view a ProjectGraph for a Codex Project; supports trace-first graph maintenance, Codex JSONL locators, hidden provenance, Markmap viewer setup, perspective views, and drift checks.
---

# ProjectGraph

ProjectGraph is a file-based, human-facing structure map for a Codex Project. Use this skill when a user asks to create a ProjectGraph, migrate an existing Project into ProjectGraph, maintain Graph after a meaningful boundary, review Graph drift, or package ProjectGraph behavior for another Project.

## Core Rules

- Visible Graph records only conclusions, facts, problem structure, route tradeoffs, and logic chains.
- Process details stay hidden in trace files and `TRACE_INDEX.json`.
- Every visible node must trace back to at least one source reference.
- Use the target project's existing language, or the user's requested language, while preserving necessary technical terms.
- Do not add `confidence`, `status`, `RawTrace`, `LiveMindMap`, or `StableMap`.
- Treat ProjectGraph as a record layer, not as an execution authority.
- Automatic capture may write locator traces, but it must not silently rewrite the visible Graph.
- Multiple views are display projections over the same canonical Graph, not separate truth sources.

## Workflows

### Initialize A Project

1. Inspect the target Project in read-only mode first.
2. Run `scripts/bootstrap_projectgraph.py --target <project_root> --project-name <name>`.
3. If the Project already has `AGENTS.md`, append the ProjectGraph section only when the user wants it; do not overwrite existing project rules.
4. Run `scripts/validate_projectgraph.py --root <project_root>`.
5. Tell the user this is only a bootstrap structure; historical seed still requires a read-only exploration pass.

### Generate A Seed Graph

1. Read available history, repo docs, task records, reports, and accessible Codex transcripts.
2. Write seed traces that state coverage limits and locators.
3. Build `PROJECT_GRAPH.json`, `PROJECT_GRAPH.md`, and `TRACE_INDEX.json` from conclusions, facts, problem structure, route tradeoffs, and logic chains.
4. Ask the user to review the seed before treating it as the future baseline.
5. Run validation and fix drift before finishing.

### Maintain After A Meaningful Boundary

Meaningful boundaries include task completion, design decision, route exclusion, conflict correction, important risk confirmation, and `/compact` before or after context compression.

1. Create a short trace with locator fields.
2. Update `PROJECT_GRAPH.json`, `PROJECT_GRAPH.md`, and `TRACE_INDEX.json`.
3. Add sibling nodes for new independent topics.
4. Add child nodes for additions or refinements to old topics.
5. Record conflicting conclusions side by side or as later correction nodes; do not silently overwrite old conclusions.
6. Run validation.

### Capture Codex JSONL Locators

Use this when the user wants ProjectGraph enabled for ongoing Codex work, including ordinary windows, `/side` task windows, `/fork`, `/compact`, and agent task execution.

1. Prefer Codex hook payload fields when available: `session_id`, `turn_id`, and `transcript_path`.
2. Run `scripts/capture_codex_trace.py --root <project_root>` from a Stop hook or with `--transcript-path <jsonl>` when operating manually. The script reads hook JSON from stdin when available.
3. Let the script write a trace keyframe containing the absolute transcript path, selected JSONL line numbers, tool-call lines, and `sha256_16` hashes.
4. Treat `/side` and `/fork` windows as independent Codex sessions: capture their own transcript path instead of merging them into the parent trace.
5. Promote the captured trace into `PROJECT_GRAPH.json`, `PROJECT_GRAPH.md`, and `TRACE_INDEX.json` only at a meaningful boundary.
6. Repeated automatic captures should remain idempotent enough for daily use: if a trace title collides, the script appends a time/turn suffix instead of overwriting old evidence.
7. Keep capture lightweight; do not add a daemon, task board, hidden status model, or automatic judgment loop.

### Add Or Review Perspective Views

Use this when the same ProjectGraph needs different mind-map displays for different readers.

1. Keep `PROJECT_GRAPH.json` as the only canonical graph.
2. Add display projections under `display.views` with either a `root_id` or a short `node_refs` list.
3. Use views to reorganize what is shown, not to create new facts.
4. Recommended first views are:
   - `global`: project logic and full record.
   - `technical`: route choices, implementation details, tests, and key conclusions.
   - `project`: delivery surface, blockers, sequencing, and remaining work.
   - `product`: user problem, intended behavior, implementation drift, and requirement changes.
5. Run validation after adding views so every `root_id` and `node_refs` target exists.

## Locator Minimum

Each trace should include:

- `project`
- `cwd`
- `date`
- `timezone`
- `session_id` or `codex_thread_id`
- `turn_id`, or `null` with a reason
- `transcript_path`, or `null` with a reason
- `field_availability_note`
- `boundary_type`
- `user_quote`
- `assistant_action`

When an original Codex JSONL transcript is discoverable, include the absolute `transcript_path` and useful line numbers in the trace or source locator.

For hook-generated traces, also include a short hash for every cited JSONL line. The trace is a locator and summary, not a copy of the original transcript.

## Bundled Resources

- `scripts/bootstrap_projectgraph.py`: creates the initial `.projectgraph/` structure, local viewer runtime, bootstrap trace, and validator in a target Project.
- `scripts/capture_codex_trace.py`: writes trace keyframes that point back to Codex JSONL transcripts and selected tool-call lines.
- `scripts/validate_projectgraph.py`: checks Graph, TraceIndex, trace files, forbidden keys, and viewer references.
- `scripts/check_release.py`: runs skill-source release hygiene checks before packaging or publishing.
- `templates/`: reusable target Project templates for AGENTS, trace locator, seed trace, Graph JSON, TraceIndex JSON, and Markdown outline.
- `assets/`: local Markmap viewer runtime copied into target Projects by bootstrap.

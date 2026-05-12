# ProjectGraph

- Use `.projectgraph/` as a background structured record layer.
- The visible Graph records only conclusions, facts, problem structure, route tradeoffs, and core logic chains.
- Keep process details hidden by default, but every visible node must trace back to a trace or source reference through `TRACE_INDEX.json`.
- Create a short trace at meaningful boundaries: task completion, design decisions, route tradeoffs, conflict correction, important risk confirmation, and before or after `/compact`.
- Every trace must include a `locator`; when fields are unavailable, set them to `null` and state why.
- Use `python3 tools/projectgraph/capture_codex_trace.py --root . --transcript-path <Codex JSONL>` to create a locator trace that points back to a real Codex JSONL transcript. This script does not rewrite the visible Graph automatically.
- After creating a trace, synchronize `PROJECT_GRAPH.json`, `PROJECT_GRAPH.md`, and `TRACE_INDEX.json`.
- Multiple display views belong in `display.views` inside `PROJECT_GRAPH.json`; they are projections over one canonical graph, not separate fact graphs.
- After each update, run `python3 tools/projectgraph/validate_projectgraph.py`.
- Do not add `confidence`, `status`, `RawTrace`, `LiveMindMap`, or `StableMap` layers.
- Treat ProjectGraph as a human-facing record layer, not an execution authority.

# Trace: <title>

## locator

```json
{
  "project": "<Project name>",
  "cwd": "<absolute path>",
  "date": "YYYY-MM-DD",
  "timezone": "<IANA timezone>",
  "codex_thread_id": null,
  "session_id": null,
  "turn_id": null,
  "transcript_path": null,
  "field_availability_note": "State which fields came from a Codex hook, environment variable, history record, or were unavailable.",
  "boundary_type": "<task completion|design decision|route tradeoff|conflict correction|important risk confirmation|compact boundary|other>",
  "user_quote": "<one or two short source quotes at most>",
  "assistant_action": "<what this trace and Graph update did>",
  "transcript_lines": {
    "session_meta": null,
    "task_started": null,
    "message:user": null,
    "message:assistant": null
  },
  "tool_call_lines": []
}
```

## Summary

Use one or two short paragraphs to explain why this boundary is worth recording.

## Extracted Conclusions

- Record only conclusions, facts, problem structure, route tradeoffs, and logic chains.
- Do not paste a full raw conversation.

## Graph Impact

- State which nodes were added, corrected, or preserved.
- When conclusions conflict, record both or add a later correction; do not silently overwrite the older node.

## Raw JSONL Location

- If this trace came from a Codex hook or `capture_codex_trace.py`, list the selected JSONL line numbers and `sha256_16` values.
- A Stop hook may call `python3 tools/projectgraph/capture_codex_trace.py --root .`; the script reads hook payload JSON from stdin.
- Do not paste the full raw transcript; the trace stores locators and a keyframe summary.

# Memory-Agent Response Template

The historical file name `response-schema.md` is retained for compatibility.
The current canonical memory-agent response is no longer a strict JSON object.

## Goal

The memory-management agent should do only two things:
- remove memory blocks that are unrelated to the current task context,
- append a short summary at the end.

## Canonical Response Shape

The response should be plain text in this form:

```text
<zero or more complete original memory blocks kept exactly as provided>

[SUMMARY] <summary no longer than 500 characters>
```

## Response Rules

- The retained memory blocks must stay in their complete original format.
- The agent must not rewrite memory lines, log-file prefixes, IDs, timestamps,
  related-resource lines, URLs, or file paths.
- The agent must not return JSON, field labels, bullet lists, or explanatory
  prose.
- The final non-empty line should start with `[SUMMARY]`.
- The summary must describe only the retained task-relevant memories.
- If no memory remains relevant after filtering, the response should contain
  only the summary line.

## Validation Guidance

Runtime implementations should keep validation lightweight.

Recommended behavior:
- accept any non-empty plain-text response,
- strip one surrounding code fence if the entire response is fenced,
- normalize the final summary line to `[SUMMARY] ...`,
- avoid strict field-level or schema-level rejection.

The scripts should still fall back to raw output when the provider fails, the
response is empty, or the transport/runtime path errors out.

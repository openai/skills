# Script Output Template

This file defines the canonical final output contract for `easy-memory`
scripts when the optional memory-management agent succeeds.

## Scope

This contract applies to:
- `scripts/read_today_log.py`
- `scripts/search_memory.py`

It does not replace raw fallback output. If the scripts do not return the
plain-text success shape described here, callers must treat the result as raw
fallback output.

## Canonical Success Shape

When the memory-management agent succeeds, the scripts should print the agent's
filtered plain-text result directly:

```text
<zero or more complete original memory blocks kept exactly as provided>

[SUMMARY] <summary no longer than 500 characters>
```

## Output Rules

- Each retained memory block should remain in its original display format.
- For `read_today_log.py`, that means the raw memory line plus any readable
  related-resource lines.
- For `search_memory.py`, that means the `log_file: raw_line` form plus any
  readable related-resource lines.
- The final non-empty line should start with `[SUMMARY]`.
- The summary should describe only the retained task-relevant memories.
- If the agent kept no memory blocks, the script may still return only the
  summary line.

## Fallback Rule

If any of the following is true, callers must not assume the success shape is
present:
- the memory-management agent is disabled,
- the local config is missing or invalid,
- the provider call fails,
- the agent returns empty output,
- the runtime raises an unexpected error.

In those cases, callers must parse the script output as raw fallback output.

## Canonical Example

The canonical example file for this output shape should live at:
- `assets/examples/script-output.example.txt`

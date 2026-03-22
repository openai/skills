# Conflict Signals

Load this file when the thread is longer than a few substantive turns, contains corrections, or refers back to earlier work.

## Common Signals

- A later message reverses a prior yes or no decision.
- Names, IDs, branches, file paths, dates, or numbers differ across turns.
- The user says "same as before" after the topic or scope has changed.
- A plan created earlier is being reused after the codebase or requirements changed.
- An assistant claim is being carried forward without tool evidence.
- Relative time words such as "today", "tomorrow", or "latest" appear in a thread that already has date confusion.

## Resolution Order

1. Latest explicit user instruction
2. Fresh local evidence from files, commands, and tools
3. Fresh external evidence from authoritative sources
4. Older user context
5. Earlier assistant text
6. Model inference

## Action Pattern

- Restate the conflict in one sentence.
- Resolve it from current evidence when possible.
- If it cannot be resolved safely, ask one short blocking question.
- Remove the stale assumption from the next answer instead of blending both versions.
- Replace relative time words with exact dates when time is part of the conflict.

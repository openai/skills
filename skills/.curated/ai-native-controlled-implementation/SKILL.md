---
name: ai-native-controlled-implementation
description: "Use when implementing from docs/implementation-plan.md in small validated batches with progress tracking, pause discipline, and MVP boundaries."
---

# AI Native Controlled Implementation

Use this skill to implement a planned project without allowing scope drift or uncontrolled generation.

## Workflow

1. Re-anchor before editing.
   - Read `docs/implementation-plan.md`.
   - Read `docs/progress.md` if it exists.
   - Inspect the repo state before changing files.
   - Identify the smallest coherent batch that moves the MVP toward its first testable state.

2. Enforce MVP scope.
   - Implement only tasks needed for the current MVP batch.
   - Do not add future-phase features, polish, or speculative abstractions.
   - Preserve architectural boundaries defined in the plan.

3. Maintain `docs/progress.md`.
   - Create the file when missing.
   - Derive tasks from `docs/implementation-plan.md`.
   - Update the `Last updated` date whenever modifying the file.
   - Do not turn progress into an implementation log.

4. Implement one logical batch.
   - Keep changes closely scoped.
   - Run appropriate verification for the changed surface.
   - Work through local failures before reporting completion.

5. Pause at a batch boundary unless the user explicitly asked for continued multi-batch execution.
   - Summarize what changed.
   - State what is now testable.
   - List known limitations and remaining MVP work.
   - Do not continue beyond the first testable MVP state without explicit instruction.

## Progress File Structure

`docs/progress.md` must follow this structure:

```markdown
# <Project Name> Implementation Progress

Last updated: YYYY-MM-DD

## Summary

- High-level bullet summary of the current implementation state.

## Milestones Checklist

### Phase X - <Phase Name>

- [ ] Task description
- [x] Completed task
- [ ] Blocked task (Blocked: reason)
- [ ] Deferred task (Deferred)
```

Use only `[ ]` and `[x]` as task statuses.

See `references/implementation-rules.md` for the full kickoff prompt and boundary rules.

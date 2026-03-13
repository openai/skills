# Memory Routing

Use this reference to route tasks to the correct project and anchor clarifications in current codebase reality.

## Discovery Priority

Run this order unless user provides explicit `project_hint`.

1. User-provided path, repo name, or branch in current prompt.
2. Existing project memory files in candidate repos:
   - `memory.md`
   - `.codex/memory.md`
   - `docs/architecture.md`
   - `docs/context.md`
3. Agent memory locations if available in current environment:
   - workspace-level memory files
   - codex-managed memory files
4. Repository signals when memory files are missing:
   - top-level README
   - package/service manifests
   - main entrypoints and module maps

## Startup Project Memory (Small)

If memory discovery is missing or insufficient, create a compact startup memory block in-session (do not require immediate file writes).

Template:

```markdown
## Startup Project Memory (Provisional)
- Project candidate: <name/path>
- Primary goal area: <domain capability>
- Probable entrypoints: <files/modules>
- Core dependencies: <libraries/services>
- Naming style clues: <snake/camel/prefix conventions>
- Open unknowns: <top 3 unknowns>
- Confidence: inferred
```

Rules:

1. Keep to 5-8 bullets.
2. Label as provisional until confirmed.
3. Use it to guide the next clarification round.

## Routing Decision

Score each candidate project on:

1. Prompt match to domain terms.
2. Memory confidence and freshness.
3. Existence of expected entrypoints.
4. Ownership or boundary fit.

Select highest-confidence candidate and output:

```markdown
## Project Route
- Selected project: <name/path>
- Why selected: <top evidence>
- Memory source: <existing memory | startup provisional memory>
- Routing confidence: <high|medium|low>
```

If routing confidence is low, ask confirmation before deep implementation planning.

## Codebase-Aware Clarification Rules

After route selection, ensure clarifications are anchored to the selected codebase.

1. Ask where in the current project the change should land.
2. Ask which existing contracts and tests must remain valid.
3. Ask which naming conventions are already present in that project.
4. Ask for boundaries: what adjacent modules must not be touched.
5. Ask for acceptance criteria tied to current behavior, not generic outcomes.

## Memory Reuse for All Tasks

For each new task chunk:

1. Reuse the latest confirmed memory for that project.
2. Re-score confidence after new evidence.
3. Refresh startup memory if contradictions appear.
4. Re-route only if strong conflicting evidence appears.

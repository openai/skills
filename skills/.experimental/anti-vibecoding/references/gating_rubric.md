# Gating Rubric

Use this rubric to decide whether implementation can start and how strict pre-green behavior should be.

## Dimensions and Scoring

Score each dimension `0`, `1`, or `2`.

1. Requirements and Scope
2. Project Route and Memory Confidence
3. Current Codebase Context
4. Constraints and Non-Goals
5. Naming Conventions (Micro)
6. Naming Conventions (Macro)
7. Acceptance Criteria and Verification

Score meanings:

- `0`: Missing or contradictory.
- `1`: Partial, still ambiguous.
- `2`: Clear, specific, and testable.

Total score range: `0-14`.

## Gate Colors

- `RED`: `0-7`
- `YELLOW`: `8-11`
- `GREEN`: `12-14`

Additional gate condition:

- `GREEN` is valid only if Requirements, Project Route and Memory, Current Codebase Context, and Acceptance Criteria are all at least `1`.

## Pre-Green Tool Budget Rules

Default by mode:

- `strict`: `0`
- `balanced`: `3` read-only calls
- `light`: `8` read-only calls
- `auto`: derived by risk profile

If `pre_green_tool_budget` is explicitly provided by user, use it as override.

Budget consumption rules:

1. Count one budget unit per tool call.
2. Allow only read-only inspection before green.
3. Treat memory discovery and routing checks as budgeted pre-green calls.
4. Deny mutating actions before green regardless of remaining budget.

## Auto Mode Selection

Use ambiguity and risk to pick effective mode.

Inputs:

1. Number of dimensions scored `0`.
2. Presence of conflicting requirements.
3. Presence of unknown integration points.
4. Project routing confidence.
5. User tolerance for assumptions.

Heuristic:

- Choose `strict` if two or more dimensions are `0`, if requirements conflict, or if routing confidence is low.
- Choose `balanced` if most dimensions are `1` and no hard conflicts exist.
- Choose `light` if at least five dimensions are `2` and only low-risk unknowns remain.

## Round Completion Logic

After each clarification round:

1. Rescore all seven dimensions.
2. Publish missing items required for green.
3. If not green, generate next targeted question batch.
4. If green, explicitly announce gate pass before any implementation work.

## Assumption Handling

If user declines to answer a question:

1. Record assumption explicitly.
2. Mark confidence as inferred.
3. Reflect risk in coaching report.
4. Continue only if gate can still reach green without violating hard constraints.

---
name: swift-concurrency
description: Proposal-backed workflow for implementing and reviewing Swift structured concurrency with async/await, Task and TaskGroup, actors, AsyncSequence, Sendable, isolation, and executor behavior. Use when writing, refactoring, debugging, or testing Swift code that coordinates concurrent work, handles cancellation/timeouts, migrates to strict concurrency, bridges callback APIs, or needs Swift Evolution-grounded implementation guidance.
---

# Swift Concurrency

Apply this workflow in order.

## Workflow

1. Load proposal-backed references before coding.
- Load `references/structured-concurrency-playbook.md` for implementation rules.
- Load `references/implemented-proposals.md` when you need proposal citations or historical compatibility checks.
- Load `references/patterns.md` for copy-paste templates.

2. Classify the problem shape.
- Choose `async` functions for one operation with awaited dependencies.
- Choose `async let` for small fixed-width parallelism.
- Choose task groups for dynamic fan-out or result aggregation.
- Choose actors for shared mutable state.
- Choose `AsyncSequence` for streamed events.
- Choose `@MainActor` for UI-facing mutation.

3. Choose the narrowest concurrency primitive.
- Prefer structured concurrency over detached tasks.
- Use `Task.detached` only for explicit lifetime and isolation boundaries.
- Keep work in child tasks scoped to the caller whenever possible.

4. Design cancellation and timeout behavior up front.
- Check cancellation in long-running loops.
- Call `Task.checkCancellation()` before expensive work units.
- Propagate cancellation unless product requirements demand fallback behavior.

5. Declare isolation explicitly.
- Annotate UI entry points with `@MainActor`.
- Move race-prone mutable state into actors.
- Conform cross-task value types to `Sendable` where diagnostics require it.
- Use `sending` ownership transfer intentionally when available.

6. Verify behavior with async tests.
- Write `async` XCTest methods and await expectations directly.
- Test cancellation, timeout, and partial-failure paths.
- Enable strict concurrency checks for the target when possible.

7. Enforce review gates.
- Reject fire-and-forget tasks where structured alternatives exist.
- Reject continuation wrappers that can double-resume or never resume.
- Reject mutable shared state outside actor/global-actor boundaries without proof.
- Reject migration plans that skip strict-concurrency settings for globals/statics.

## Decision Guide

- Need 2-4 known parallel calls: use `async let`.
- Need dynamic child task counts: use `with(Throwing)TaskGroup`.
- Need serialized mutable state: use `actor`.
- Need callback/delegate bridging: use `withChecked(Throwing)Continuation`.
- Need producer-consumer streaming: use `AsyncStream` or `AsyncThrowingStream`.

## Implementation Rules

- Bound task lifetimes to lexical scope.
- Avoid fire-and-forget except at explicit app boundaries.
- Preserve task priority unless an override is intentional.
- Prefer domain errors over erasing into untyped `Error`.
- Use `nonisolated` only when thread safety is proven.
- Treat distributed actors as opt-in architecture, not a default.

## References

Load [`references/structured-concurrency-playbook.md`](references/structured-concurrency-playbook.md) for proposal-backed implementation and review rules.

Load [`references/implemented-proposals.md`](references/implemented-proposals.md) for the complete list of relevant merged `Implemented` Swift Evolution proposals.

Load [`references/patterns.md`](references/patterns.md) for copy-paste templates:
- Timeout wrapper using task groups
- Actor-backed cache with deduplication
- Bounded parallel map with `TaskGroup`
- Callback-to-`async` continuation wrapper
- `AsyncThrowingStream` bridge for delegate-style APIs

## Maintenance

Regenerate the proposal index when Swift Evolution changes:

```bash
curl -sS https://download.swift.org/swift-evolution/v1/evolution.json > /tmp/swift-evolution.json
python3 scripts/build_implemented_proposals_index.py \
  --source /tmp/swift-evolution.json \
  --output references/implemented-proposals.md
```

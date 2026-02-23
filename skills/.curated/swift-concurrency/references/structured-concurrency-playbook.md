# Structured Concurrency Playbook (Proposal-Backed)

Use this playbook when implementing or reviewing Swift structured concurrency code.

## 1) Build a Task Tree First

- Prefer structured concurrency as the default model (`SE-0304`).
- Use `async let` for fixed-width parallelism known at compile time (`SE-0317`).
- Use `with(Throwing)TaskGroup` for dynamic fan-out/fan-in (`SE-0304`, `SE-0381`, `SE-0442`).
- Start child tasks synchronously from caller context when setup invariants matter (`SE-0472`).
- Name long-lived or externally observed tasks to improve diagnostics (`SE-0469`).

## 2) Define Cancellation, Deadlines, and Timeouts

- Treat cancellation as cooperative and explicit (`SE-0304`).
- Check cancellation in loops and before expensive units.
- Model deadlines and sleeping via `Clock` APIs (`SE-0329`, `SE-0374`, `SE-0473`).
- Keep timeout wrappers in structured scopes (task groups) so unfinished work is canceled predictably (`SE-0304`, `SE-0329`).

## 3) Apply Isolation Deliberately

- Put shared mutable state behind actors (`SE-0306`).
- Use global actors for domain-wide serialization (for example UI on `MainActor`) (`SE-0316`).
- Avoid assuming property wrappers imply actor isolation (`SE-0401`).
- Use actor-aware initialization and lifecycle rules (`SE-0327`, `SE-0371`, `SE-0411`).
- Model inheritance and conformance isolation explicitly in class/protocol hierarchies (`SE-0420`, `SE-0470`).
- Use `nonisolated` intentionally, and account for caller-actor execution behavior of nonisolated async functions (`SE-0449`, `SE-0461`).
- Control default actor-isolation inference when module policies demand it (`SE-0466`).
- Use dynamic enforcement only as compatibility glue while migrating non-strict code (`SE-0423`).

## 4) Move Data Across Tasks Safely

- Enforce `Sendable` for cross-concurrency boundaries (`SE-0302`).
- Do not rely on unsafe pointer `Sendable` behavior (`SE-0331`).
- Use `sending` for ownership-safe transfer semantics where available (`SE-0430`).
- Understand newer inference rules for `Sendable` methods and key path literals (`SE-0418`).
- For Objective-C imported completion handlers, account for `@Sendable` annotations (`SE-0463`).

## 5) Bridge Legacy and Streaming APIs Correctly

- Bridge callback APIs with checked continuations and resume exactly once (`SE-0300`).
- Use `AsyncSequence`/`AsyncIteratorProtocol` and stream factories for producer-consumer workflows (`SE-0298`, `SE-0314`, `SE-0388`, `SE-0421`, `SE-0468`).
- Use ObjC concurrency interop rules when wrapping Cocoa APIs (`SE-0297`).
- Mark APIs unavailable from async contexts when blocking semantics are unsafe (`SE-0340`).

## 6) Choose Executors and Scheduling Semantics Intentionally

- Use custom actor executors only with clear scheduling/perf motivation (`SE-0392`).
- Set task executor preference deliberately for locality/performance-sensitive paths (`SE-0417`).
- Implement proper serial-executor isolation checks (`SE-0424`, `SE-0471`).
- Use task-priority escalation APIs where service-level objectives require it (`SE-0462`).

## 7) Enforce Strict Concurrency in Stages

- Use incremental migration strategy and tighten checks progressively (`SE-0337`).
- Enforce strict concurrency for global/static state (`SE-0412`).
- Rely on clarified non-actor-isolated async execution rules when auditing race risks (`SE-0338`, `SE-0461`).
- Keep memory-model assumptions aligned with Swift guarantees (`SE-0282`).

## 8) Handle Entry Points and Top-Level Behavior

- Ensure async entry behavior matches asynchronous main semantics (`SE-0323`).
- Understand top-level concurrency behavior in scripts/tooling contexts (`SE-0343`).
- Use effectful read-only properties (`get async` / `get throws`) where it improves API clarity (`SE-0310`).

## 9) Distributed Actors (Only When Needed)

- Treat distributed actors as an explicit architectural commitment, not a default (`SE-0336`, `SE-0344`, `SE-0428`).

## Review Gate (Fail Review If Any Item Is True)

- Unstructured fire-and-forget tasks are used where parent-scoped tasks are possible.
- Cancellation is ignored in long-running operations.
- Shared mutable state is outside actor/global-actor protection without proof of safety.
- Cross-task data movement lacks `Sendable`/`sending` correctness.
- Continuations can be resumed multiple times or not resumed at all.
- Actor-isolation defaults are relied on implicitly in mixed strict/non-strict modules.
- Global/static mutable state remains outside strict concurrency policy.

## Proposal Index

For the complete proposal list (all relevant and implemented), load `implemented-proposals.md`.

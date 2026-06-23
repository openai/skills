# Implemented Concurrency-Relevant Swift Evolution Proposals

Snapshot source: `https://download.swift.org/swift-evolution/v1/evolution.json`
- `creationDate`: `2026-02-23T17:35:59Z`
- `commit`: `a3e4924a36d9e695e65b736e952ce7c5bec2438d`
- `selected proposals`: `55`

Selection rules:
- Include only proposals where `status.state == implemented`.
- Include proposals whose `link` filename matches concurrency keywords (`async`, `actor`, `task`, `sendable`, `isolat`, `executor`, `stream`, `clock`, `continuation`, `distributed`, `concurr`).
- Also include manual IDs: `SE-0282`, `SE-0310`, `SE-0430`.

| Proposal | Implemented | Title | Link |
|---|---:|---|---|
| `SE-0282` | `5.3` | Clarify the Swift memory consistency model ⚛︎ | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0282-atomics.md) |
| `SE-0296` | `5.5` | Async/await | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0296-async-await.md) |
| `SE-0297` | `5.5` | Concurrency Interoperability with Objective-C | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0297-concurrency-objc.md) |
| `SE-0298` | `5.5` | Async/Await: Sequences | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0298-asyncsequence.md) |
| `SE-0300` | `5.5` | Continuations for interfacing async tasks with synchronous code | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0300-continuation.md) |
| `SE-0302` | `5.7` | `Sendable` and `@Sendable` closures | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0302-concurrent-value-and-concurrent-closures.md) |
| `SE-0304` | `5.5` | Structured concurrency | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0304-structured-concurrency.md) |
| `SE-0306` | `5.5` | Actors | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0306-actors.md) |
| `SE-0310` | `5.5` | Effectful Read-only Properties | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0310-effectful-readonly-properties.md) |
| `SE-0311` | `5.5` | Task Local Values | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0311-task-locals.md) |
| `SE-0313` | `5.5` | Improved control over actor isolation | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0313-actor-isolation-control.md) |
| `SE-0314` | `5.5` | `AsyncStream` and `AsyncThrowingStream` | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0314-async-stream.md) |
| `SE-0316` | `5.5` | Global actors | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0316-global-actors.md) |
| `SE-0317` | `5.5` | `async let` bindings | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0317-async-let.md) |
| `SE-0323` | `5.5.2` | Asynchronous Main Semantics | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0323-async-main-semantics.md) |
| `SE-0327` | `5.10` | On Actors and Initialization | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0327-actor-initializers.md) |
| `SE-0329` | `5.7` | Clock, Instant, and Duration | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0329-clock-instant-duration.md) |
| `SE-0331` | `5.6` | Remove Sendable conformance from unsafe pointer types | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0331-remove-sendable-from-unsafepointer.md) |
| `SE-0336` | `5.7` | Distributed Actor Isolation | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0336-distributed-actor-isolation.md) |
| `SE-0337` | `5.6` | Incremental migration to concurrency checking | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0337-support-incremental-migration-to-concurrency-checking.md) |
| `SE-0338` | `5.7` | Clarify the Execution of Non-Actor-Isolated Async Functions | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0338-clarify-execution-non-actor-async.md) |
| `SE-0340` | `5.7` | Unavailable From Async Attribute | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0340-swift-noasync.md) |
| `SE-0343` | `5.7` | Concurrency in Top-level Code | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0343-top-level-concurrency.md) |
| `SE-0344` | `5.7` | Distributed Actor Runtime | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0344-distributed-actor-runtime.md) |
| `SE-0371` | `6.2` | Isolated synchronous deinit | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0371-isolated-synchronous-deinit.md) |
| `SE-0374` | `5.9` | Add sleep(for:) to Clock | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0374-clock-sleep-for.md) |
| `SE-0381` | `5.9` | DiscardingTaskGroups | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0381-task-group-discard-results.md) |
| `SE-0388` | `5.9` | Convenience Async[Throwing]Stream.makeStream methods | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0388-async-stream-factory.md) |
| `SE-0392` | `5.9` | Custom Actor Executors | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0392-custom-actor-executors.md) |
| `SE-0401` | `5.9` | Remove Actor Isolation Inference caused by Property Wrappers | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0401-remove-property-wrapper-isolation.md) |
| `SE-0411` | `5.10` | Isolated default value expressions | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0411-isolated-default-values.md) |
| `SE-0412` | `5.10` | Strict concurrency for global variables | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0412-strict-concurrency-for-global-variables.md) |
| `SE-0414` | `6.0` | Region based Isolation | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0414-region-based-isolation.md) |
| `SE-0417` | `6.0` | Task Executor Preference | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0417-task-executor-preference.md) |
| `SE-0418` | `6.0` | Inferring `Sendable` for methods and key path literals | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0418-inferring-sendable-for-methods.md) |
| `SE-0420` | `6.0` | Inheritance of actor isolation | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0420-inheritance-of-actor-isolation.md) |
| `SE-0421` | `6.0` | Generalize effect polymorphism for `AsyncSequence` and `AsyncIteratorProtocol` | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0421-generalize-async-sequence.md) |
| `SE-0423` | `6.0` | Dynamic actor isolation enforcement from non-strict-concurrency contexts | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0423-dynamic-actor-isolation.md) |
| `SE-0424` | `6.0` | Custom isolation checking for SerialExecutor | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0424-custom-isolation-checking-for-serialexecutor.md) |
| `SE-0428` | `6.0` | Resolve DistributedActor protocols | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0428-resolve-distributed-actor-protocols.md) |
| `SE-0430` | `6.0` | `sending` parameter and result values | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0430-transferring-parameters-and-results.md) |
| `SE-0431` | `6.0` | `@isolated(any)` Function Types | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0431-isolated-any-functions.md) |
| `SE-0434` | `6.0` | Usability of global-actor-isolated types | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0434-global-actor-isolated-types-usability.md) |
| `SE-0442` | `6.1` | Allow TaskGroup's ChildTaskResult Type To Be Inferred | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0442-allow-taskgroup-childtaskresult-type-to-be-inferred.md) |
| `SE-0449` | `6.1` | Allow `nonisolated` to prevent global actor inference | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0449-nonisolated-for-global-actor-cutoff.md) |
| `SE-0461` | `6.2` | Run nonisolated async functions on the caller's actor by default | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md) |
| `SE-0462` | `6.2` | Task Priority Escalation APIs | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0462-task-priority-escalation-apis.md) |
| `SE-0463` | `6.2` | Import Objective-C completion handler parameters as `@Sendable` | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0463-sendable-completion-handlers.md) |
| `SE-0466` | `6.2` | Control default actor isolation inference | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0466-control-default-actor-isolation.md) |
| `SE-0468` | `6.2` | `Hashable` conformance for `Async(Throwing)Stream.Continuation` | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0468-async-stream-continuation-hashable-conformance.md) |
| `SE-0469` | `6.2` | Task Naming | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0469-task-names.md) |
| `SE-0470` | `6.2` | Global-actor isolated conformances | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0470-isolated-conformances.md) |
| `SE-0471` | `6.2` | Improved Custom SerialExecutor isolation checking for Concurrency Runtime | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0471-SerialExecutor-isIsolated.md) |
| `SE-0472` | `6.2` | Starting tasks synchronously from caller context | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0472-task-start-synchronously-on-caller-context.md) |
| `SE-0473` | `6.3` | Clock Epochs | [view](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0473-clock-epochs.md) |

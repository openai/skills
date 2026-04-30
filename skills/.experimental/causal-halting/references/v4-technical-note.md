# Causal Halting V4 Technical Note

V4.0 turns the project from separate scripts into a runnable package and CLI.

The core invariant remains:

```text
prediction_about(E) -> result -> control(E)
```

When that modeled path exists before the observed execution ends, the artifact is classified as `causal_paradox`.

When no modeled path is found, the artifact may be `valid_acyclic`, but only within this scope:

```text
no modeled prediction-feedback cycle was detected
```

This is not a proof of termination, safety, correctness, or classical halting decidability.

Natural language is not classified by deterministic scripts. Prose must first become explicit structured IR:

```text
natural language -> LLM-authored DesignIR -> deterministic analyzer
```

The CLI, adapters, reports, viewer, and evaluation corpus all operate on structured artifacts.

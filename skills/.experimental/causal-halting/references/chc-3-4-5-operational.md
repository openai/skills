# CHC-3/4/5 Operational Notes

CHC-3, CHC-4, and CHC-5 are structured-artifact analyzers. They do not parse prose.
In v4.0 they emit `validity_scope`, `identity_resolution`, `formal_status`, and
`theorem_coverage` metadata.

## CHC-3: ProcessIR

Use `scripts/chc_process_check.py` for process/session artifacts.

It tracks:

- process identity;
- execution identity;
- session identity;
- result identity;
- control channel identity.

It rejects a result routed back into the observed execution before that execution ends,
including multi-hop paths through named channels/controllers when those routes are
present in `ProcessIR`.

## CHC-4: Temporal Trace

Use `scripts/chc_temporal_check.py` for JSONL traces with temporal metadata.

It preserves:

- `timestamp`;
- `logical_clock`;
- `span_id`;
- `parent_id`;
- `trace_id`;
- `happens_before`.

It builds a happens-before closure from explicit `happens_before`, span parent links,
logical clocks, and safe timestamp order. If temporal order is insufficient and no
paradox is directly visible, it returns `insufficient_info`.

## CHC-5: PredictionIR

Use `scripts/chc_prediction_check.py` for probabilistic or scored predictions.

The rule is structural:

```text
prediction_about(E) -> PredictionResult -> control(E)
```

The confidence value is not used for classification. `prediction_scope` must be
explicit; bounded local progress metrics are accepted only when scoped as local
metrics rather than predictions about the current execution's outcome.

## Boundary

These analyzers do not prove arbitrary termination and do not solve the classical Halting Problem. They only detect modeled prediction-feedback structure. `valid_acyclic` means only `no_modeled_prediction_feedback_only`.


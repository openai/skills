# Quick Start

V4.0 is designed around one runnable path:

```powershell
python -m pip install -e .
chc version
chc demo --output .tmp/demo
```

Open `.tmp/demo/report.md` after the demo runs.

## Minimal Checks

```powershell
chc check examples/diagonal.graph --format json
chc trace examples/self-prediction.trace.jsonl --format json
chc trace examples/future-run.trace.jsonl --format json
```

Expected shape:

- `diagonal.graph` -> `causal_paradox`
- `self-prediction.trace.jsonl` -> `causal_paradox`
- `future-run.trace.jsonl` -> `valid_acyclic`

`valid_acyclic` only means no modeled prediction-feedback cycle was found. It does not prove termination, safety, correctness, or absence of unmodeled feedback.

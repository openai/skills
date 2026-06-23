# CHC-1 And CHC-2 Operational Notes

V2.0 extends the executable checker beyond CHC-0.

This does not make CHC a halting oracle. The checker still analyzes only causal prediction-feedback structure.

## CHC-1

CHC-1 supports recursive CHC functions through finite causal effect summaries:

```text
Eff(f) = fixed-point summary of body_effect(f)
```

If summaries converge, the checker analyzes the run against the converged graph. If summaries do not converge within the configured limit, the result is conservative `insufficient_info`.

Example:

```text
Rec(y) = let r = H(Rec,y) in if r then Rec(y) else halt
run Rec(Task)
```

Expected:

```text
classification: causal_paradox
chc_level: CHC-1
fixed_point_status: converged
```

## CHC-2

CHC-2 supports higher-order function parameters only when effects are explicit:

```text
Cb(x) = halt
Apply(cb!Clean,x) = cb(x)
run Apply(Cb,Task)
```

Missing effect annotations return `insufficient_info`. `HaltResult` cannot be passed into callbacks.

Expected fields:

```text
chc_level
effect_summaries
fixed_point_status
higher_order_effects
effect_composition_status
```

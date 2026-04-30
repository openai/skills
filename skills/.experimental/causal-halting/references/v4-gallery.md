# Gallery

Small visual patterns for design review.

## Unsafe Same-Run Prediction Feedback

```text
AgentRun -> Predictor observes AgentRun -> Prediction controls AgentRun before it ends
```

Classification: `causal_paradox`

## Safer External Orchestrator

```text
AgentRun -> Supervisor observes AgentRun -> Orchestrator consumes result -> NextAgentRun
```

Classification: `valid_acyclic`

## Post-Run Audit

```text
AgentRun ends -> Evaluator scores AgentRun -> Audit record is written
```

Classification: `valid_acyclic`

## Ordinary Local Loop

```text
AgentRun increments local progress counter -> AgentRun continues until bounded budget expires
```

Classification: `valid_acyclic` when no modeled prediction about the whole current execution is consumed.

## Ambiguous Identity

```text
Supervisor produces r-1 -> somebody consumes r-1
```

Classification: `insufficient_info`

Question to answer: who consumes `r-1`, and does that consumer control the observed execution before it ends?

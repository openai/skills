# Causal Halting Report

**Classification:** `causal_paradox`
**Validity scope:** `no_modeled_prediction_feedback_only`

**Human summary:** A modeled prediction or observation result can control the execution it observes.

CHC does not solve classical halting. `valid_acyclic` only means no modeled prediction-feedback cycle was detected; it does not prove termination, general safety, correctness, or absence of unmodeled feedback.
**Identity resolution:** resolved=2, ambiguous=0, missing=0, conflicts=0

A prediction or observation result controls the same execution it observes.

## Causal Graph

```mermaid
flowchart LR
  n_E_AgentRun_task_["E(AgentRun,task)"] -- "" --> n_R_AgentRun_task_["R(AgentRun,task)"]
  n_R_AgentRun_task_["R(AgentRun,task)"] -- "" --> n_E_AgentRun_task_["E(AgentRun,task)"]
```

## Proof Obligations
- `prediction_result_not_consumed_by_observed_execution`

## Recommendations
- Move the prediction result to an external orchestrator or controller.
- Make the result affect a future execution, not the execution being observed.
- Convert current-run self-prediction into post-run audit when possible.
- Replace self-halting prediction with bounded local progress metrics.
- Keep monitor and controller roles separate.

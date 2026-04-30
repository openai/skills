---
name: causal-halting
description: This skill should be used when the user asks to analyze halting-problem variants, Turing diagonalization, self-reference, prediction-feedback loops, AI agent termination, workflow self-evaluation, systems that ask whether their own current execution will halt, Causal Halting Calculus (CHC-0), causal paradox vs semantic unprovability, halting predictors, or designs that separate observation, execution, and feedback.
---

# Causal Halting

Use this skill to apply the Causal Halting Calculus (CHC-0/1/2/3/4/5) as an analysis method. CHC does not solve the classical Halting Problem. It separates two failure modes: structural prediction-feedback cycles (`causal_paradox`) and ordinary semantic undecidability (`unproved`).

This skill is self-contained for publication through `openai/skills` and `npx skills`. It includes the formal reference, runnable checker, examples, and license inside this directory.

When this skill is packaged as the `causal-halting` plugin, a background prompt guard may put CHC-0 hygiene into context automatically. Treat that guard as a routing signal, not as a proof result: apply the workflow below only when structurally relevant, keep the distinction sharp, and do not overclaim.

To use the CHC-0 lens for every relevant question in the current session, the user can run `/causal-halting on` or say `use causal-halting for this session`. To turn it off, the user can run `/causal-halting off` or say `causal-halting session off`.

## Workflow

1. State the exact claim being analyzed.
   - Distinguish "decide all halting" from "detect prediction-feedback loops."
   - Do not claim CHC-0 removes undecidability.

2. Identify the CHC roles.
   - `Code`: inert program description.
   - `Exec`: live execution event.
   - `H`: halting observation operator.
   - `HaltResult`: causal token produced by `H`, not ordinary data.

3. Enforce CHC-0 restrictions before reasoning.
   - No `eval`.
   - No runtime code generation.
   - No higher-order code.
   - No recursion in CHC-defined code.
   - CHC calls are fully inlined over an acyclic call graph.
   - L0 programs are opaque, H-free, and may be Turing-complete.
   - `HaltResult` is not `Val`.
   - `HaltResult` cannot enter L0 or cross CHC function boundaries.
   - `HaltResult` can only be discarded or eliminated by `H-BRANCH`.

4. Build the symbolic causal graph.
   - Observation `H(p,a)` adds `E(p,a) -> R(p,a)`.
   - Branching on `HaltResult(p,a)` inside current execution `e` adds `R(p,a) -> e`.
   - Branching on ordinary `Bool` adds no causal edge.
   - L0 calls add no causal edge.
   - CHC calls inline their body and accumulate edges.
   - For natural-language designs, the LLM must interpret semantic roles into `DesignIR`, then classify deterministically from that IR.
   - Never classify prose directly. Never use keyword presence as evidence.
   - Use `design_ir_version: "1.0"` and include `semantic_evidence` for auditability.
   - Valid DesignIR control timing values are `during_observed_execution`, `after_observed_execution`, `future_execution`, `external_controller`, and `unknown`.
   - For JSONL traces, use event identity (`exec_id`, `result_id`) rather than prose inference.

5. Check `acyclic_unif`.
   - Look for a nonempty path `E(s,t) ->+ E(u,v)`.
   - If `(s,t)` and `(u,v)` unify under first-order unification, classify as `causal_paradox`.
   - Use unification, not enumeration of concrete substitutions.

6. Classify the result.
   - `causal_paradox`: a unifiable prediction-feedback cycle exists.
   - `unproved`: no causal paradox, but termination/divergence is not proven.
   - `proved_halts` or `proved_diverges`: only if an explicit proof, restricted analysis, or trusted verifier establishes it.

7. Explain the boundary.
   - `causal_paradox` is type-system intrinsic and stable across proof systems.
   - `unproved` is proof-system relative and can shrink under stronger sound provers.

8. For Mini-CHC v2, account for higher layers.
   - CHC-1 recursion uses fixed-point causal effect summaries.
   - If summaries do not converge, classify conservatively as `insufficient_info`.
   - CHC-2 higher-order calls require explicit effect annotations, such as `cb!Clean`.
   - Missing or incomplete higher-order effects are `insufficient_info`, not `valid_acyclic`.
   - `HaltResult` still cannot be passed into callbacks.

9. For V3 structured analyzers, use the correct artifact.
   - CHC-3: `ProcessIR` for process/session non-interference.
   - CHC-4: temporal JSONL traces with happens-before/span metadata.
   - CHC-5: `PredictionIR` for probabilistic/scored predictions.
   - If identity, timing, or effect data is missing, return `insufficient_info`.
   - `valid_acyclic` never means the system terminates or is safe in general.
   - Treat `validity_scope: no_modeled_prediction_feedback_only` as mandatory: `valid_acyclic` only means no modeled prediction-feedback path was detected.
   - Check `identity_resolution`; missing, ambiguous, or conflicting production identity should be `insufficient_info`.

10. When a `causal_paradox` is found in an agent/workflow design, suggest a causal refactoring.
   - Move prediction results to an external orchestrator or controller.
   - Make results affect future executions, not the observed execution.
   - Convert current-run self-prediction into post-run audit when possible.
   - State the proof obligation: the observed execution must not consume its own prediction result before it ends.

## Canonical Examples

Diagonal program:

```text
D(y) =
  let r = H(y,y) in
  if r then loop else halt
```

Graph:

```text
E(y,y) -> R(y,y) -> E(D,y)
```

The path `E(y,y) ->+ E(D,y)` becomes a cycle under unifier `y |-> D`. Therefore `D(D)` is a `causal_paradox`.

Semantic hard case:

```text
Q_e() =
  simulate e(e)
  if e(e) halts, halt
  else diverge
```

`Q_e` is H-free L0 code, so it generates no causal graph edges. It is causally valid, but deciding it for all `e` would decide the classical Halting Problem. Therefore it belongs to `unproved` in general.

## Output Pattern

When responding, prefer this structure:

```text
Core claim:
CHC roles:
Causal graph:
acyclic_unif result:
Classification:
Limits:
```

Keep the distinction sharp:

```text
CHC-0 rejects diagonal prediction feedback.
CHC-0 does not decide all halting questions.
```

## Bundled Checker

Use `scripts/chc_check.py` for explicit graph DSL or Mini-CHC v2 artifacts. The checker uses Python standard library only and supports CHC-0/1/2 operational analysis.

Use `scripts/chc_design_analyze.py` for explicit `DesignIR`, `scripts/chc_trace_check.py` for JSONL traces, `scripts/chc_process_check.py` for CHC-3 ProcessIR, `scripts/chc_temporal_check.py` for CHC-4 temporal traces, `scripts/chc_prediction_check.py` for CHC-5 PredictionIR, `scripts/chc_identity_check.py` for identity-resolution metadata, `scripts/chc_theory_coverage.py` for Lean/theory coverage, `scripts/chc_workflow_adapter.py` for generic workflow JSON, `scripts/chc_otel_adapter.py` for explicitly annotated OpenTelemetry JSON, `scripts/chc_langgraph_adapter.py` for structured LangGraph-style JSON, `scripts/chc_temporal_airflow_adapter.py` for structured Temporal/Airflow-style JSON, `scripts/chc_eval_design_ir.py` and `scripts/chc_eval_suite.py` for corpus fixture evaluation, `scripts/chc_repair.py` for causal repair reports, `scripts/chc_verify_repair.py` and `scripts/chc_certificate.py` for before/after trace verification and certificates, and `scripts/chc_report.py` for Markdown/Mermaid reports.

Run from the skill root:

```powershell
python scripts/chc_check.py examples/diagonal.graph
python scripts/chc_check.py --format json examples/diagonal.chc
python scripts/chc_check.py examples/qe-valid-acyclic.chc
python scripts/chc_design_analyze.py examples/self-prediction.design-ir.json
python scripts/chc_trace_check.py examples/self-prediction.trace.jsonl
python scripts/chc_repair.py examples/self-prediction.analysis.json
python scripts/chc_workflow_adapter.py examples/generic-workflow.json
python scripts/chc_otel_adapter.py examples/otel-self-prediction.json
python scripts/chc_langgraph_adapter.py examples/langgraph-future-run.json
python scripts/chc_temporal_airflow_adapter.py examples/temporal-airflow-indirect-feedback.json
python scripts/chc_verify_repair.py examples/self-prediction.trace.jsonl examples/future-run.trace.jsonl
python scripts/chc_report.py examples/self-prediction.analysis.json
python scripts/chc_eval_design_ir.py examples/design-ir-corpus
python scripts/chc_eval_suite.py examples/design-ir-corpus
python scripts/chc_process_check.py examples/process-self-feedback.process-ir.json
python scripts/chc_temporal_check.py examples/temporal-self-feedback.trace.jsonl
python scripts/chc_prediction_check.py examples/prediction-self-risk.prediction-ir.json
python scripts/chc_certificate.py examples/self-prediction.trace.jsonl examples/future-run.trace.jsonl --repair examples/self-prediction.analysis.json
```

Classify checker output as follows:

```text
causal_paradox    unifiable E ->+ E prediction-feedback path found
valid_acyclic     no CHC causal paradox detected
insufficient_info conservative rejection for incomplete summaries/effects
parse_error       unsupported or invalid checker input
unproved        semantic status only; arbitrary halting remains undecidable
```

## Bundled Examples

Use the files in `examples/` when demonstrating or testing the skill:

```text
examples/diagonal.chc          mini-CHC diagonal program
examples/diagonal.graph        explicit diagonal causal graph
examples/chc1-recursive-feedback.chc recursive CHC-1 feedback
examples/chc2-higher-order-safe.chc safe CHC-2 higher-order effect
examples/qe-valid-acyclic.chc  H-free semantic hard case
examples/safe-supervisor.graph supervisor observes separate worker
examples/self-prediction.trace.jsonl same-run feedback trace
examples/future-run.trace.jsonl safe future-run trace
examples/post-end-audit.trace.jsonl safe post-run audit trace
examples/generic-workflow.json generic workflow adapter input
examples/otel-self-prediction.json annotated OpenTelemetry adapter input
examples/langgraph-future-run.json structured LangGraph-style adapter input
examples/temporal-airflow-indirect-feedback.json structured Temporal/Airflow-style adapter input
examples/process-self-feedback.process-ir.json CHC-3 process/session feedback
examples/temporal-self-feedback.trace.jsonl CHC-4 temporal feedback trace
examples/prediction-self-risk.prediction-ir.json CHC-5 probabilistic feedback
examples/self-prediction.design-ir.json explicit DesignIR input
examples/self-prediction.analysis.json repair input
examples/design-ir-corpus/ multilingual DesignIR extraction fixtures
```

## References

For formal rules, theorem statements, and the current paper draft, read:

```text
references/causal-halting-calculus.md
```

For LLM interpretation of prose into DesignIR, read:

```text
references/design-ir-extraction.md
```

For operational CHC-1/CHC-2 checker behavior, read:

```text
references/chc-1-2-operational.md
```

For standalone publication notes and installation commands, read:

```text
README.md
```

# Causal Halting Skill

A self-contained Agent Skill for analyzing prediction-feedback loops in halting-style reasoning.

This package is the portable skill distribution for `causal-halting`. It is suitable for installation through `openai/skills`, direct GitHub skill install, and `npx skills`.

## What It Does

The skill applies Causal Halting Calculus (CHC-0/1/2/3/4/5) as an analysis method.

It separates two failure modes:

```text
causal_paradox  structural prediction-feedback cycle
unproved        causally valid behavior whose halting status is not proven
```

It does not solve the classical Halting Problem. It detects the narrower pattern where a prediction or observation about an execution can control that same execution:

```text
Exec(P, X) -> HaltResult(P, X) -> Exec(P, X)
```

## Contents

```text
causal-halting/
  SKILL.md
  README.md
  LICENSE.txt
  agents/
    openai.yaml
  references/
    causal-halting-calculus.md
    chc-1-2-operational.md
    chc-3-4-5-operational.md
    design-ir-extraction.md
  scripts/
    chc_check.py
    chc_design_analyze.py
    chc_design_schema.py
    chc_trace_check.py
    chc_repair.py
    chc_report.py
    chc_eval_design_ir.py
    chc_workflow_adapter.py
    chc_otel_adapter.py
    chc_langgraph_adapter.py
    chc_temporal_airflow_adapter.py
    chc_verify_repair.py
    chc_certificate.py
    chc_process_check.py
    chc_temporal_check.py
    chc_prediction_check.py
    chc_eval_suite.py
    sync_skill_package.py
  schemas/
    design-ir.schema.json
    effect-summary.schema.json
    effect-annotation.schema.json
    process-ir.schema.json
    temporal-trace.schema.json
    prediction-result.schema.json
    repair-certificate.schema.json
  examples/
    diagonal.chc
    diagonal.graph
    chc1-recursive-feedback.chc
    chc2-higher-order-safe.chc
    future-run.trace.jsonl
    generic-workflow.json
    langgraph-future-run.json
    otel-self-prediction.json
    temporal-airflow-indirect-feedback.json
    post-end-audit.trace.jsonl
    qe-valid-acyclic.chc
    safe-supervisor.graph
    self-prediction.analysis.json
    self-prediction.design-ir.json
    self-prediction.trace.jsonl
    design-ir-corpus/
```

## Install

### Codex Skill Installer

```text
$skill-installer install https://github.com/chrystyan96/causal-halting/tree/master/skills/causal-halting
```

Restart Codex after installing a new skill.

### npx skills

```powershell
npx skills add https://github.com/chrystyan96/causal-halting/tree/master/skills/causal-halting -a codex -g
```

For local testing from the repository root:

```powershell
npx skills add .\skills\causal-halting -a codex -g
```

## Use

Ask the agent to analyze designs involving halting, self-reference, prediction feedback, or AI agent loops:

```text
Use causal-halting to analyze this agent design:
The agent asks a monitor whether the current run will halt,
then decides whether to continue based on the monitor result.
```

Expected response shape:

```text
Core claim:
CHC roles:
Causal graph:
acyclic_unif result:
Classification:
Limits:
```

## Checker

The bundled checker uses Python standard library only.

Run from this skill directory:

```powershell
python scripts/chc_check.py examples/diagonal.graph
python scripts/chc_check.py --format json examples/diagonal.chc
python scripts/chc_check.py examples/qe-valid-acyclic.chc
python scripts/chc_check.py examples/safe-supervisor.graph
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
python scripts/chc_certificate.py examples/self-prediction.trace.jsonl examples/future-run.trace.jsonl --repair examples/self-prediction.analysis.json
python scripts/chc_process_check.py examples/process-self-feedback.process-ir.json
python scripts/chc_temporal_check.py examples/temporal-self-feedback.trace.jsonl
python scripts/chc_prediction_check.py examples/prediction-self-risk.prediction-ir.json
```

Checker classifications:

```text
causal_paradox  unifiable prediction-feedback cycle found
valid_acyclic   no CHC causal paradox detected
insufficient_info conservative rejection for incomplete recursion/effect information
parse_error     unsupported or invalid checker input
```

`semantic_status` may be:

```text
unproved        causally valid, but arbitrary halting remains undecidable
not_analyzed    semantic halting status was not analyzed
```

## Examples

### Diagonal

```text
D(y) = if H(y,y) then loop else halt
run D(D)
```

Expected:

```text
classification: causal_paradox
```

The program asks for a halting observation about its own current execution and then branches on that result.

### Q_e

```text
Q_e() = simulate e(e); if e(e) halts then halt else diverge
run Q_e()
```

Expected:

```text
classification: valid_acyclic
semantic_status: unproved
```

`Q_e` is H-free, so it has no CHC-0 causal paradox. It remains semantically hard because deciding it for all `e` would decide classical halting.

### Safe Supervisor

```text
E(TaskA,input) -> R(TaskA,input)
R(TaskA,input) -> E(Supervisor,input)
```

Expected:

```text
classification: valid_acyclic
```

The supervisor observes a separate worker. The result does not feed back into the observed worker execution.

## Design, Trace, And Repair Workflows

The portable skill also includes the v3.1 analysis scripts:

```text
chc_design_analyze.py  analyze explicit DesignIR JSON
chc_design_schema.py   validate design-analysis JSON
chc_trace_check.py     deterministically analyze JSONL execution traces
chc_repair.py          generate repair reports and proof obligations
chc_report.py          render Markdown/Mermaid reports
chc_eval_design_ir.py  evaluate DesignIR corpus fixtures without parsing prose
chc_workflow_adapter.py convert generic workflow JSON to CHC trace JSONL
chc_otel_adapter.py    convert explicitly annotated OpenTelemetry JSON to CHC trace JSONL
chc_langgraph_adapter.py convert structured LangGraph-style JSON to CHC trace JSONL
chc_temporal_airflow_adapter.py convert structured Temporal/Airflow-style JSON to CHC trace JSONL
chc_verify_repair.py   verify before/after trace repair
chc_certificate.py     emit machine-readable repair certificates
chc_process_check.py   analyze CHC-3 ProcessIR
chc_temporal_check.py  analyze CHC-4 temporal trace JSONL
chc_prediction_check.py analyze CHC-5 PredictionIR
chc_identity_check.py  validate identity-resolution metadata
chc_theory_coverage.py summarize Lean/theorem coverage
chc_eval_suite.py      summarize corpus coverage and deterministic checks
sync_skill_package.py  compare/copy portable skill package
```

Every analyzer output carries `validity_scope: no_modeled_prediction_feedback_only`.
That scope means only that no modeled prediction-feedback cycle was detected;
it does not prove termination, general safety, correctness, or trace completeness.

Trace schema:

```json
{"type":"exec_start","exec_id":"run-1","program":"AgentRun","input":"task-a"}
{"type":"observe","observer":"Supervisor","target_exec_id":"run-1","result_id":"r-1"}
{"type":"consume","result_id":"r-1","consumer_exec_id":"run-1","purpose":"strategy_change"}
{"type":"exec_end","exec_id":"run-1","status":"halted"}
```

Repair reports move same-run prediction feedback to a separate orchestrator/future-run boundary and emit proof obligations. `chc_verify_repair.py` checks that the after trace removes same-run pre-end consumption and, when supplied with repair JSON, satisfies the listed obligations.

`valid_acyclic` does not mean the program terminates, the system is safe, or the agent is correct. It only means no modeled prediction-feedback cycle was detected.

## No Lexical Analysis

Natural language is interpreted by the LLM into `DesignIR`. The bundled scripts do not classify prose and do not use keyword lists, regex patterns, or language-specific phrases for design understanding.

If prose is passed directly to `chc_design_analyze.py`, it returns `needs_design_ir`.

See `references/design-ir-extraction.md` for the semantic extraction contract.

DesignIR v1.0 requires `design_ir_version`, stable IDs, explicit observation results, explicit control timing, `semantic_evidence`, and `uncertain` entries when the consumer is unclear.

The `examples/design-ir-corpus/` fixtures separate natural-language descriptions from expected `DesignIR`. `chc_eval_design_ir.py` validates the expected JSON artifacts and expected classifications only; it does not classify prose.

## Limits

- Does not solve the classical Halting Problem.
- Does not prove arbitrary termination or divergence.
- Checks explicit graph DSL and Mini-CHC v2 artifacts only.
- Natural-language designs must be interpreted into `DesignIR` by the LLM before script analysis.
- Deterministically checks traces only when they follow the documented JSONL schema.
- Converts only documented structured formats. OpenTelemetry requires explicit `chc.*` attributes, and LangGraph/Temporal/Airflow-style input requires explicit causal fields.
- Produces causal refactoring guidance, not arbitrary code patches.
- Treats semantic undecidability as `unproved`, not as `causal_paradox`.
- CHC-1 recursion is checked through conservative finite effect summaries.
- CHC-2 higher-order calls require explicit effect annotations.
- Does not include the full Codex plugin hook or `/causal-halting` slash command. Those live in the full plugin repository.

## License

Apache-2.0. See `LICENSE.txt`.

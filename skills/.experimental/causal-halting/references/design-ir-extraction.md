# DesignIR Extraction Contract

Natural language is never classified directly by Causal Halting scripts.

The LLM must interpret prose into `DesignIR`. Deterministic scripts then validate
and classify the `DesignIR`.

## Rule

Do not look for specific words. Ask:

```text
what execution exists?
what execution is observed or predicted?
what result is produced?
what execution consumes that result?
```

Words like `halt`, `loop`, `supervisor`, `monitor`, `prediction`, or `execucao`
are not evidence by themselves. Only structured causal roles in `DesignIR` are
analyzed.

## Schema

```json
{
  "design_ir_version": "1.0",
  "executions": [
    {"id": "run-1", "program": "AgentRun", "input": "task"}
  ],
  "observations": [
    {"id": "obs-1", "observer": "Supervisor", "target_exec": "run-1", "result": "r-1"}
  ],
  "controls": [
    {
      "id": "ctrl-1",
      "result": "r-1",
      "target_exec": "run-1",
      "timing": "during_observed_execution",
      "action": "change_strategy"
    }
  ],
  "semantic_evidence": [
    {"source": "user description", "claim": "The result changes the same active run."}
  ],
  "uncertain": []
}
```

Required timing values:

```text
during_observed_execution
after_observed_execution
future_execution
external_controller
unknown
```

Classification is deterministic from DesignIR. The LLM may write
`semantic_evidence`, but it must not write the final classification as evidence.

## Ambiguity

If the consumer of an observation result is unclear, do not guess:

```json
{
  "design_ir_version": "1.0",
  "executions": [
    {"id": "run-1", "program": "AgentRun", "input": "task"}
  ],
  "observations": [
    {"id": "obs-1", "observer": "Evaluator", "target_exec": "run-1", "result": "r-1"}
  ],
  "controls": [],
  "semantic_evidence": [
    {
      "source": "user description",
      "claim": "The consumer of the observation result is unclear."
    }
  ],
  "uncertain": [
    {
      "field": "controls.target_exec",
      "reason": "The prose says the result is used, but not which execution consumes it."
    }
  ]
}
```

## Multilingual Examples

English:

```text
The active worker receives an evaluator's forecast and revises its own route.
```

DesignIR:

```json
{
  "design_ir_version": "1.0",
  "executions": [
    {"id": "run-1", "program": "Worker", "input": "task"}
  ],
  "observations": [
    {"id": "obs-1", "observer": "Evaluator", "target_exec": "run-1", "result": "r-1"}
  ],
  "controls": [
    {
      "id": "ctrl-1",
      "result": "r-1",
      "target_exec": "run-1",
      "timing": "during_observed_execution",
      "action": "revise_route"
    }
  ],
  "semantic_evidence": [
    {"source": "English example", "claim": "The active worker consumes the assessment result."}
  ],
  "uncertain": []
}
```

Portuguese:

```text
O agente em execucao recebe uma avaliacao sobre sua propria rodada e muda o plano.
```

DesignIR:

```json
{
  "design_ir_version": "1.0",
  "executions": [
    {"id": "run-1", "program": "AgentRun", "input": "task"}
  ],
  "observations": [
    {"id": "obs-1", "observer": "Evaluator", "target_exec": "run-1", "result": "r-1"}
  ],
  "controls": [
    {
      "id": "ctrl-1",
      "result": "r-1",
      "target_exec": "run-1",
      "timing": "during_observed_execution",
      "action": "change_plan"
    }
  ],
  "semantic_evidence": [
    {"source": "Portuguese example", "claim": "A mesma rodada muda o plano."}
  ],
  "uncertain": []
}
```

Spanish:

```text
El proceso activo recibe una evaluacion de esa misma ejecucion y cambia su ruta.
```

DesignIR:

```json
{
  "design_ir_version": "1.0",
  "executions": [
    {"id": "run-1", "program": "ActiveProcess", "input": "task"}
  ],
  "observations": [
    {"id": "obs-1", "observer": "Evaluator", "target_exec": "run-1", "result": "r-1"}
  ],
  "controls": [
    {
      "id": "ctrl-1",
      "result": "r-1",
      "target_exec": "run-1",
      "timing": "during_observed_execution",
      "action": "change_route"
    }
  ],
  "semantic_evidence": [
    {"source": "Spanish example", "claim": "La misma ejecucion consume la evaluacion."}
  ],
  "uncertain": []
}
```

## Non-Goal

This contract does not expose hidden chain-of-thought. It asks the LLM for an
auditable structured interpretation.

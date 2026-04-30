# Adapters

Adapters convert structured runtime or workflow artifacts into CHC trace events.

They do not infer intent from names, labels, prose, or keywords.

## OpenTelemetry

Use explicit `chc.*` attributes:

```text
chc.event.type        exec_start | observe | consume | exec_end | control_exec
chc.exec.id           stable execution ID
chc.target_exec.id    observed execution ID
chc.result.id         observation or prediction result ID
chc.consumer_exec.id  execution consuming the result
chc.trace.id          trace ID
chc.span.id           span ID
chc.parent.id         parent span ID
chc.service.name      service name
```

Run:

```powershell
python scripts/chc_otel_adapter.py examples/otel-self-prediction.json --format jsonl
```

## LangGraph-Style JSON

Use explicit `runs`, `observations`, and `controls`.

```powershell
python scripts/chc_langgraph_adapter.py examples/langgraph-future-run.json --format jsonl
```

## Temporal/Airflow-Style JSON

Use explicit workflow/task run IDs and causal control fields.

```powershell
python scripts/chc_temporal_airflow_adapter.py examples/temporal-airflow-future-run.json --format jsonl
```

If stable execution/result/control identity is missing, the analyzer must return `insufficient_info`, not `valid_acyclic`.

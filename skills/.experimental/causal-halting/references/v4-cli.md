# CLI

Install locally:

```powershell
python -m pip install -e .
```

Unified entrypoint:

```powershell
chc <command> [args...]
```

Commands:

```text
chc check <graph-or-chc-file>
chc design <design-ir-json>
chc trace <trace-jsonl>
chc process <process-ir-json>
chc temporal <trace-jsonl-or-json>
chc prediction <prediction-ir-json>
chc repair <analysis-json>
chc verify-repair <before> <after> --repair <repair-json>
chc report <analysis-json> --format markdown|json|mermaid
chc demo
chc eval
chc version
```

Most analyzer commands support `--format json` and `--explain-like-human`.

The original `scripts/*.py` entrypoints remain available for compatibility.

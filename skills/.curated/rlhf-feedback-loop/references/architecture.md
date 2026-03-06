# RLHF Feedback Loop Architecture

## Data Flow

```
Thumbs up/down → Capture (JSONL log) → Rubric engine → Memory promotion
                                                          |
                                                    +-----+-----+
                                                    |           |
                                                  Learn      Prevent
                                                    |           |
                                                LanceDB    Prevention
                                                vectors      rules
                                                    |
                                                DPO export → fine-tune
```

## Storage

- **Feedback log**: `.rlhf/feedback-log.jsonl` — raw signals
- **Memory log**: `.rlhf/memory-log.jsonl` — promoted memories
- **Prevention rules**: `.rlhf/prevention-rules.md` — auto-generated guardrails
- **LanceDB**: `.claude/memory/feedback/lancedb/` — vector embeddings

## MCP Tools (11 total)

| Tool | Purpose |
|------|---------|
| `recall` | Search past feedback for current task context |
| `capture_feedback` | Record thumbs up/down with structured metadata |
| `feedback_stats` | Analytics: counts, ratios, domain breakdown |
| `feedback_summary` | Human-readable summary of recent feedback |
| `prevention_rules` | Generate/retrieve prevention guardrails |
| `export_dpo_pairs` | Export DPO training pairs (prompt/chosen/rejected) |
| `construct_context_pack` | Build bounded context from memories |
| `evaluate_context_pack` | Record pack outcome for improvement |
| `context_provenance` | Audit trail of context decisions |
| `list_intents` | Available action plans |
| `plan_intent` | Generate execution plan with checkpoints |

## Links

- GitHub: https://github.com/IgorGanapolsky/rlhf-feedback-loop
- npm: https://www.npmjs.com/package/rlhf-feedback-loop
- MCP Registry: io.github.IgorGanapolsky/rlhf-feedback-loop

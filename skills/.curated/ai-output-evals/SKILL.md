# AI Output Evals

## Description

Use this skill when the user wants to evaluate, compare, or regression-test AI, LLM, RAG, or agent outputs.

## Workflow

1. Identify the behavior under test: the user input, expected output, actual output, and any retrieved sources or tool calls.
2. Choose the smallest reliable checks before suggesting model-based judging:
   - exact match for deterministic strings
   - substring checks for required facts
   - regular expressions for structured patterns
   - JSON validity and JSON-path checks for structured output
   - citation coverage for grounded RAG answers
   - token F1 or overlap for short natural-language answers
3. Separate required checks from advisory checks so a useful response is not rejected for harmless wording differences.
4. Report failures as actionable regressions with the case id, failed check, observed output, and expected evidence.
5. Recommend adding the eval to CI when the case protects product behavior, safety policy, retrieval quality, or a previously fixed bug.

## Output Shape

When creating an eval, prefer a compact table:

| case | check | pass/fail | note |
| --- | --- | --- | --- |

When writing a fixture, prefer JSON or JSONL records with:

```json
{
  "id": "refund-policy",
  "input": "Can I refund after 45 days?",
  "expected": "Refunds are available within 30 days.",
  "actual": "Refunds are only available within 30 days.",
  "checks": [
    { "type": "contains", "value": "30 days" },
    { "type": "token_f1", "min": 0.6 }
  ]
}
```

## Guidance

- Do not overfit evals to one exact phrasing unless the product contract requires it.
- For RAG, score retrieval and answer generation separately when possible.
- For agents, include tool-call assertions for important side effects.
- For safety behavior, include both refusal and allowed-helpfulness cases.
- Keep eval datasets small at first; expand them when regressions reveal missing coverage.


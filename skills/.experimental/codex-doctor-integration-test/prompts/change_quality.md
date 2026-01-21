Evaluate code change quality relative to prompt.json and the actual diff. You will be given a JSON input payload with:
- prompt: prompt.json content
- evidence: evidence.json content
- git_diff
- execution_summary
- agentic_summary

Score quality across these dimensions:
- correctness vs change_prompt
- context usage (qualitative)
- maintainability/readability
- risk/regression assessment
- builds/tests passing (from execution_summary)

Return strict JSON with this schema:
{
  "status": "PASS|WARN|FAIL|NOT_RUN",
  "rationale": "string",
  "evidence_quotes": [{"path":"...","quote":"..."}],
  "recommendations": ["..."],
  "confidence": 0.0
}

Rules:
- If builds/tests FAIL, status should be FAIL unless the prompt explicitly allows it.
- Use WARN for partial correctness or limited context usage.
- Call out mismatches between change_prompt and git_diff.
- Output JSON only. No markdown.

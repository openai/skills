You are evaluating whether the agentic loop executed successfully. You will be given a JSON input payload with:
- prompt: prompt.json content
- evidence: evidence.json content (includes agents_md and logs_index)
- git_diff
- execution_summary
- agentic_summary

Hard fails:
- If any evidence or logs mention the phrase "Context compaction enabled", status MUST be FAIL.

Prefer PASS only if agentic_summary.status is PASS and exit_code is 0.

Return strict JSON with this schema:
{
  "status": "PASS|WARN|FAIL|NOT_RUN",
  "rationale": "string",
  "evidence_quotes": [{"path":"...","quote":"..."}],
  "recommendations": ["..."],
  "confidence": 0.0
}

Rules:
- Use WARN for partial success (e.g., agentic_summary exists but status is FAIL).
- Reference concrete evidence paths in evidence_quotes.
- Output JSON only. No markdown.

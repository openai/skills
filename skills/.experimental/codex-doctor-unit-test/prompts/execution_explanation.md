You are summarizing execution results for a documented dev/build/test loop.

The deterministic runner has already decided the status below. You MUST copy the provided status verbatim.

Deterministic status:
{{DETERMINISTIC_STATUS}}

Execution summary JSON:
{{EXECUTION_SUMMARY_JSON}}

Return STRICT JSON only with this schema:
{
  "status": "PASS|WARN|FAIL|NOT_RUN",
  "rationale": "string",
  "evidence_quotes": [{"path":"...", "quote":"..."}],
  "recommendations": ["..."],
  "confidence": 0.0
}

Rules:
- The status must equal the deterministic status shown above.
- Evidence quotes should come from the execution summary file path, not from AGENTS.
- Rationale must mention the executed command(s) from the execution summary (wrap them in backticks).
- Keep quotes short (<240 chars).
- No patches or diffs in recommendations.

Execution summary path:
{{EXECUTION_SUMMARY_PATH}}

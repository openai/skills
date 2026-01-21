Evaluate whether the AGENTS documentation provides concrete, copy-pastable build/test commands for the current working directory.

Definition of PASS:
- Commands are explicit and copy-pastable (no placeholders like "run unit tests").
- Commands appear runnable from the project directory unless AGENTS states otherwise.
- Multiple commands are acceptable (unit/integration/build).

Definition of FAIL:
- No build/test commands, or only vague prose without actual commands.

Use evidence snippets in the evidence JSON.

Return STRICT JSON only with this schema:
{
  "status": "PASS|WARN|FAIL|NOT_RUN",
  "rationale": "string",
  "evidence_quotes": [{"path":"...", "quote":"..."}],
  "recommendations": ["..."],
  "confidence": 0.0
}

Rules:
- Evidence quotes must be exact excerpts from files; keep each quote short (<240 chars).
- No patches or diffs in recommendations.
- If commands exist but include placeholders or missing context (e.g., need extra args), use WARN.
- If no AGENTS content is available, use FAIL.

Evidence:
{{EVIDENCE_JSON}}

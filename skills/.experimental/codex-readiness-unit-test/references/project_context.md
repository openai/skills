Evaluate whether the AGENTS documentation in the current working directory provides clear context with explicit paths.

Definition of PASS:
- The AGENTS docs include explicit paths to important directories/files (e.g., services/auth, src/, Makefile, pyproject.toml).
- Each path has a short context for what it is used for.

Definition of FAIL:
- No explicit paths, or only vague prose without concrete paths.

Use the evidence snippets in the evidence JSON.

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
- If the docs contain some paths but lack context, use WARN.
- If no AGENTS content is available, use FAIL.

Evidence:
{{EVIDENCE_JSON}}

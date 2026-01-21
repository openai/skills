Evaluate whether the AGENTS documentation describes the dev/build/test loop(s) for the current working directory.

Definition of PASS:
- Documentation includes ordering (what to run first, next, last).
- It specifies when to run the loop (e.g., after each change, before PR).
- It defines success criteria (what output indicates success).
- Multiple loops are acceptable (fast vs full).

Definition of FAIL:
- No loop guidance, or only vague statements with no ordering/criteria.

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
- If ordering exists but missing when-to-run or success criteria, use WARN.
- If no AGENTS content is available, use FAIL.

Evidence:
{{EVIDENCE_JSON}}

You are evaluating repository onboarding quality based on provided evidence.

Return STRICT JSON only with this schema:
{
  "status": "PASS|WARN|FAIL|NOT_RUN",
  "rationale": "string",
  "evidence_quotes": [{"path":"...", "quote":"..."}],
  "recommendations": ["..."],
  "confidence": 0.0
}

Rules:
- Use only evidence provided (AGENTS/PLANS snippets and summaries).
- Evidence quotes must be exact excerpts from files; keep each quote short (<240 chars).
- No patches or diffs in recommendations.
- If evidence is missing, use WARN or FAIL and explain why.

Evidence:
{{EVIDENCE_JSON}}

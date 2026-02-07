You are fixing invalid JSON from a prior evaluator.

Return ONLY valid JSON that matches this schema exactly:
{
  "status": "PASS|WARN|FAIL|NOT_RUN",
  "rationale": "string",
  "evidence_quotes": [{"path":"...", "quote":"..."}],
  "recommendations": ["..."],
  "confidence": 0.0
}

Rules:
- Do not include any extra keys.
- Do not include markdown, commentary, or code fences.
- If the original content lacks evidence, keep evidence_quotes empty.

Invalid output to fix:
{{RAW_OUTPUT}}

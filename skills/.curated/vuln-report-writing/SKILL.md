---
name: vuln-report-writing
description: Create professional offensive-security report content for bug bounty findings or full penetration-test reports. Use when asked to write a vulnerability finding (asset, description, impact, remediation, references, PoC steps) or to assemble a pentest report with executive summary, scope, methodology, findings, and recommendations.
---

# Vuln Report Writing

## Overview
Create clear, reproducible, no-hype vulnerability reports for bug bounty submissions or pentest deliverables using strict, triage-friendly structure.

## Workflow Decision Tree
1. Identify mode: **Bug bounty finding** or **Pentest report**.
2. Collect inputs: asset, vuln type, affected components, evidence/PoC, impact, remediation, references.
3. Draft using the required structure; keep language factual and concise.
4. Validate for clarity and reproducibility; add assumptions if data is missing.

## Mode A: Bug Bounty Finding
Use the exact fields and order below:
1. Affected asset
2. Description (2–3 sentences)
3. Impact (1–2 sentences)
4. Remediation (1–2 sentences)
5. References (prefer OWASP; otherwise high-quality vendor/standards)
6. Evidence/PoC (1–4 short steps; mention Burp where appropriate)

Template: see `references/bugbounty-finding.md`.

## Mode B: Pentest Report
Include standard report sections plus findings in the Mode A format.
Required sections:
- Executive summary (short, non-technical)
- Scope (in-scope assets only)
- Methodology (high level, non-sensitive)
- Findings (each in Mode A format)
- Risk overview (aggregate themes, not hype)
- Recommendations (prioritized, pragmatic)
- Appendix (optional: tooling list, test accounts, evidence index)

Template: see `references/pentest-report.md`.

## Quality Rules (apply to both modes)
- Keep claims factual; avoid exaggeration or speculative impact.
- Make reproduction easy; write steps as short, testable actions.
- State assumptions when required inputs are missing.
- Show impact clearly and directly; avoid buzzwords.
- Prefer OWASP references; otherwise use vendor/standards docs.

## Resources
- `references/bugbounty-finding.md` for the finding template and phrasing guidance.
- `references/pentest-report.md` for the full report structure.
- `references/owasp-refs.md` for commonly used OWASP references.

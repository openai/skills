---
name: "postman-validate"
description: "Use when running Postman cloud collection tests, creating Postman mock servers, or auditing an API or collection for security issues."
metadata:
  short-description: "Test, mock, and audit Postman APIs"
---

# Postman Validate

Use this skill for Postman validation workflows: cloud test runs, mock-server creation, and security audits.

If Postman MCP is unavailable, switch to [postman](../postman/SKILL.md) for setup first.

## Workflow

1. Resolve the relevant workspace and collection or spec.
2. If the user wants tests, run the collection through Postman, summarize the results, and inspect failing requests and responses.
3. If the user wants a mock, check for example responses, reuse an existing mock when possible, or create a new one and return the mock URL.
4. If the user wants a security audit, inspect auth, transport security, validation, error handling, rate limiting, and exposed secrets.
5. Present concrete next actions, and re-run the relevant validation after fixes when appropriate.

## Important rules

- Use collection UIDs in `OWNER_ID-UUID` format for cloud runs.
- Mocks depend on saved example responses.
- Include impacted endpoints or configuration in every security finding.
- Prefer direct explanation of failures and risks over raw output dumps.

## Error handling

- MCP unavailable: use [postman](../postman/SKILL.md) for setup.
- Timeout: retry once and narrow the workflow if needed.
- Plan limitations: surface them clearly for mocks, large runs, or other restricted operations.

---
name: "postman-docs"
description: "Use when generating, improving, syncing, or publishing API documentation from Postman collections or OpenAPI specs."
metadata:
  short-description: "Generate and publish Postman docs"
---

# Postman Docs

Analyze documentation coverage for a collection or spec, fill in gaps, and publish or unpublish Postman docs when appropriate.

If Postman MCP is unavailable, switch to [postman](../postman/SKILL.md) for setup first.

## Workflow

1. Resolve the source of truth: local spec, Postman spec, or Postman collection.
2. Assess documentation completeness for descriptions, examples, auth, errors, and rate limits.
3. Generate or improve missing documentation content.
4. Apply updates to the chosen source and publish docs if the user wants a public URL.
5. If both a spec and collection exist, keep the source-of-truth decision explicit before syncing.

## Important rules

- Local markdown generation can still work without MCP, but publishing requires MCP.
- Direct collection sync only supports OpenAPI 3.0.
- Prefer concise coverage summaries before proposing large documentation rewrites.

## Error handling

- MCP unavailable: use [postman](../postman/SKILL.md) for setup or continue locally when publishing is not required.
- Invalid spec: surface parse and validation issues first.
- Too many matching APIs: ask the user to choose a collection or spec.

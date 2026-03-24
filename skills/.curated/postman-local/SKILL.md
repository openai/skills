---
name: "postman-local"
description: "Use when sending one-off HTTP requests with the Postman CLI, running local git-synced Postman collections, or generating and linting an OpenAPI spec from code."
metadata:
  short-description: "Use Postman CLI and local Postman files"
---

# Postman Local

Use this skill for local Postman CLI workflows: one-off requests, local collection runs, and spec generation or linting from code.

## Prerequisites

- Verify `postman --version`.
- Verify authentication with `postman whoami`.
- For local collection runs, confirm the repo has `postman/collections/` and `.postman/resources.yaml`.

## Workflow

1. Determine whether the user needs a direct request, a local collection run, or spec generation.
2. For direct requests, build the exact `postman request` command with only the needed headers, body, auth, and environment settings.
3. For local collection runs, resolve the collection’s cloud ID mapping, add an environment only when required, and run `postman collection run`.
4. For spec generation, scan the codebase for route definitions, update or create an OpenAPI 3.0.3 YAML spec, and lint it with `postman spec lint`.
5. Summarize the command run, output shape, failures, and next steps.

## Important rules

- Show the exact CLI command before running it.
- Never print secrets or raw tokens in output.
- Run collections by cloud ID, not local path.
- Generate OpenAPI 3.0.3 in YAML and keep linting until errors and warnings are resolved.

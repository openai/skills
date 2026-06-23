---
name: "api"
description: "Generate or refresh docs/api.md from repository evidence. Use only when explicitly invoked to inspect routes, handlers, API specs, schemas, and service calls, then document the API surface grouped by service without inventing contracts."
---

# api

## Objective

Create or update `docs/api.md` so another agent can understand the repository's API surface and service boundaries.

## Invocation contract

- Run only on explicit invocation of `$api`.
- If `docs/` does not exist in the target repository, create it before writing `docs/api.md`.
- Read the existing `docs/api.md` before changing it.
- Inspect controllers, routes, handlers, OpenAPI files, Postman collections, gRPC definitions, GraphQL schemas, gateway configs, and frontend service calls when they provide missing API evidence.
- Infer from code only when no formal API spec exists, and state that clearly.
- Preserve useful existing content that still matches the repository.
- Use `Unknown` for missing request, response, auth, or error details.

## Required sections

Create or update `docs/api.md` with these sections:

- API inventory grouped by service
- Event contracts if present
- Webhook contracts if present
- Inter service APIs if present
- Shared DTOs or schemas if present
- API handoff summary

## Per-service requirements

For each service, include:

- Base path
- Auth requirements
- Endpoints
- Method
- Request shape
- Response shape
- Error responses
- Dependencies
- Notes
- Known gaps

## Documentation rules

- Prefer endpoint tables for dense inventories and short bullets for supporting notes.
- Cite the files used to infer each service inventory.
- When DTOs or schemas are defined in code, reflect the real field names and note omitted details as `Unknown`.
- Distinguish confirmed behavior from `Inference:` lines.
- Avoid copying full specs verbatim when a concise summary is sufficient.

## Suggested scan targets

- HTTP: `controllers/`, `routes/`, `handlers/`, middleware, server bootstrap files
- Specs: `openapi.*`, `swagger.*`, `postman*`, `insomnia*`
- RPC and schemas: `proto/`, `graphql/`, shared DTO or schema folders
- Frontend callers: `services/`, `api/`, `lib/api*`, data-fetching hooks

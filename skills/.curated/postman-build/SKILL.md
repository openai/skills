---
name: "postman-build"
description: "Use when searching Postman workspaces for APIs, syncing collections with specs, pushing API changes to Postman, or generating typed client code from a Postman collection."
metadata:
  short-description: "Search, sync, and generate from Postman"
---

# Postman Build

Use this skill for remote Postman build workflows: finding APIs, syncing specs and collections, and generating client code from a collection.

If Postman MCP is unavailable, switch to [postman](../postman/SKILL.md) for setup first.

## Workflow

1. Resolve the relevant workspace and collection or spec.
2. If the user is exploring APIs or endpoints, inspect workspace collections first and use public Postman search only as a fallback.
3. If the user is syncing, determine whether the flow is spec-to-collection, collection-to-spec, or targeted collection updates.
4. If the user wants generated code, inspect requests, responses, auth, environments, and any linked spec, then detect the target project language.
5. Summarize the resulting API matches, sync changes, or generated code artifacts.

## Important rules

- `searchPostmanElements` searches the public Postman network, not private workspace content.
- `syncCollectionWithSpec` is async and supports OpenAPI 3.0 only.
- For Swagger 2.0 or OpenAPI 3.1, regenerate the collection instead of forcing direct sync.
- Use the current project’s existing HTTP library and style when generating code.

## Error handling

- MCP unavailable: use [postman](../postman/SKILL.md) for setup.
- Invalid spec: surface parse errors before syncing.
- Empty or incomplete collections: redirect within the workflow to search or sync rather than guessing.

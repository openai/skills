---
name: postman-json
description: Generate and maintain Postman collection JSON files from Express source code. Use when new API endpoints are added, existing endpoints are changed, or multiple routes must be synced into a single up-to-date collection that mirrors route/module structure and request requirements.
---

# Postman JSON

## Overview

Generate or update a Postman collection by reading an Express server entry file and discovered route modules. Mirror route-file structure into Postman folders and infer request requirements such as bearer auth, JSON body fields, multipart file fields, and verification tokens.

## Run This Workflow

1. Detect mounted routers from `app.use("/prefix", router)` in the Express server entry file.
2. Parse each router file and discover `router.<method>(...)` endpoints.
3. Infer request requirements from route handlers and middleware usage:
- Bearer auth when auth middleware is present.
- JSON body fields from `req.body` access.
- Multipart form-data and file fields when upload middleware is present.
- Additional body fields from imported middleware (for example `turnstileToken`).
4. Sync a Postman collection JSON:
- Keep non-generated top-level items.
- Replace the generated root tree so added endpoints appear and removed ones disappear.
- Keep the Postman folder hierarchy aligned with route file paths in the codebase.

## Use The Script

Run:

```bash
python3 skills/postman-json/scripts/sync_postman_collection.py \
  --project-root . \
  --server-file ./src/server.js \
  --output ./postman/my-api.postman_collection.json \
  --collection-name "My API" \
  --base-url "http://localhost:3000"
```

Default behavior when options are omitted:

- Auto-detect the server file (`server.js`, `app.js`, `src/server.js`, `src/app.js`, `backend/server.js`, `backend/app.js`, then fallback scan).
- Write to `./postman/<project-name>.postman_collection.json`.
- Use collection name `<Project Name> API`.
- Set `baseUrl` variable to `http://localhost:3000`.

## Validate The Output

After syncing, verify:

1. New endpoints appear in the expected source-structure folder.
2. Auth-protected endpoints include bearer auth (`{{shopToken}}`).
3. Multipart endpoints include file field placeholders and required text fields.
4. JSON endpoints include request body templates matching required fields.

## References

- See [`references/request-inference-rules.md`](references/request-inference-rules.md) for route parsing and request-template inference rules.
- Use [`scripts/sync_postman_collection.py`](scripts/sync_postman_collection.py) for deterministic collection generation and update.

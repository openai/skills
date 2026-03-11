---
name: "postman-json"
description: "Use when the user needs to generate or update Postman collection JSON from Express or Node route source code, especially after endpoint or middleware changes; discover mounted routers from app.use(...) aliases (ESM imports and CommonJS require), parse router methods, infer auth/body/upload requirements, and sync a deterministic generated subtree."
---

# Postman JSON

Generate or refresh a Postman collection from Express source files. Keep the generated Postman tree aligned with code structure and request requirements inferred from handlers and middleware.

## Quick start

- Run `scripts/sync_postman_collection.py` with explicit `--project-root` and `--server-file` when the repo has multiple server entry points.
- Re-run after route or middleware edits so the generated subtree stays accurate.
- Treat the script output as source-of-truth for generated Postman endpoints.

## Workflow

1. Discover mounted routers from `app.use("/prefix", routerAlias)` in the server file.
2. Resolve `routerAlias` to route modules from both ESM imports and CommonJS `require(...)` aliases.
3. Parse each route module for `router.<method>(path, ...middleware, handler)` calls.
4. Infer request requirements from middleware/handler context and imported middleware source:
- Bearer auth when auth middleware is detected.
- Multipart mode with file fields when upload middleware or `req.file`/`req.files` usage is detected.
- Body fields from `req.body` access.
5. Sync collection JSON:
- Preserve non-generated top-level items.
- Replace only the generated root subtree.
- Keep folder hierarchy aligned with route file paths.

## Use the script

```bash
python3 skills/.curated/postman-json/scripts/sync_postman_collection.py \
  --project-root . \
  --server-file ./src/server.js \
  --output ./postman/my-api.postman_collection.json \
  --collection-name "My API" \
  --base-url "http://localhost:3000"
```

When flags are omitted, defaults are:

- Server auto-discovery from common entry paths (`server.js`, `app.js`, `src/server.js`, `src/app.js`, `backend/server.js`, `backend/app.js`) then fallback scan.
- Output at `./postman/<project-name>.postman_collection.json`.
- Collection name `<Project Name> API`.
- `baseUrl` variable `http://localhost:3000`.

## Validation checklist

1. Endpoints appear in the expected source-structure folder path.
2. Auth-protected endpoints include bearer auth with `{{token}}`.
3. Multipart endpoints include file fields and required text fields.
4. JSON endpoints include expected body templates.
5. Removed routes no longer appear in the generated subtree.

## Reference map

Read only what you need:

- `references/request-inference-rules.md` -> route parsing and request-template inference details.
- `scripts/sync_postman_collection.py` -> deterministic sync behavior and parser implementation.

## Quality rules

- Keep inference deterministic and route-scoped; avoid file-wide leakage between endpoints.
- Prefer parser updates over hand-editing generated Postman request bodies.
- Preserve non-generated collection content when syncing.

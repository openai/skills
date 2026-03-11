# Request Inference Rules

Use these rules when generating or updating Postman requests from Express route code.

## Route Discovery

1. Read mounted routers from `app.use("/prefix", routerVariable)` in the server entry file.
2. Resolve `routerVariable` to its imported route file.
3. Parse `router.<method>(path, ...middleware, handler)` calls in each route file.
4. Build full endpoint path as `<mount-prefix> + <route-path>`.

## Folder Structure

Mirror route file paths in Postman folders:

- `src/routes/users.js` -> `src / routes / users`
- `backend/routes/admin/users.js` -> `backend / routes / admin / users`

## Request Requirements

Infer requirements in this order:

1. Use middleware names and imported middleware source code for auth/body clues.
2. Use handler code (`req.body`, `req.file`, `req.files`) for payload fields.
3. Apply safe defaults when requirements are ambiguous.

### Auth

- If middleware name contains `auth`, set bearer auth with `{{token}}`.
- If middleware source reads `req.headers.authorization`, set bearer auth.

### Body Mode

- If route needs file upload (`req.file`/`req.files` or upload middleware), use `form-data`.
- Else if body fields are detected, use raw JSON.
- Else send no body.

### Body Fields

- Extract from `req.body.<field>` and `req.body?.<field>`.
- Include destructured fields from patterns like `const { fieldA } = req.body`.

## Update Strategy

On each sync:

1. Keep existing top-level collection items that are not generated.
2. Replace the generated root subtree entirely with fresh route output.
3. Keep collection variables and ensure defaults exist:
- `baseUrl`
- `token`

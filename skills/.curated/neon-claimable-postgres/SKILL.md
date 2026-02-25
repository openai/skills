---
name: neon-claimable-postgres
description: >-
  Provision instant temporary Postgres databases via Neon Claimable Postgres
  (pg.new) with no login, signup, or credit card. Use when users ask for a
  quick Postgres environment, a throwaway DATABASE_URL for prototyping/tests,
  or "just give me a DB now". Triggers include: "quick postgres", "temporary
  postgres", "no signup database", "no credit card database", "instant
  DATABASE_URL".
---

# Neon Claimable Postgres

Create an instant Postgres database with Neon Claimable Postgres (`pg.new`) for fast local development, demos, prototyping, and test environments.

Databases are temporary by default (typically 72 hours) and can be claimed later to a Neon account for permanent use.

## Quick Start

```bash
npx get-db@latest -y
```

By default, this writes the following environment variables to `.env`:

```
DATABASE_URL=<pooled connection string>
DATABASE_URL_DIRECT=<direct connection string>
# Claimable DB expires at: <expiration date>
# Claim it now to your account using the link below:
PUBLIC_POSTGRES_CLAIM_URL=<claim URL>
```

`PUBLIC_` is the default prefix used by `get-db` (including `-y` and default prompts). If a custom prefix is configured via `-p, --prefix`, this becomes `{prefix}POSTGRES_CLAIM_URL`.

And returns a DATABASE_URL connection string in the console ready to use.

## When to Use Which Method

### CLI (`npx get-db`)

Use this by default for most users who want a fast setup in an existing project.

```bash
npx get-db@latest
```

Common flags:

- `-y, --yes`: skip prompts
- `-e, --env <path>`: choose env file path
- `-k, --key <name>`: customize env var key (default `DATABASE_URL`)
- `-s, --seed <path>`: run SQL seed file
- `-L, --logical-replication`: enable logical replication
- `-r, --ref <id>`: set source/referrer id

Full CLI reference: [references/get-db.md](./references/get-db.md)

### SDK (`get-db/sdk`)

Use this for scripts and programmatic provisioning flows.

```typescript
import { instantPostgres } from "get-db/sdk";

const db = await instantPostgres();
console.log(db.connectionString);
```

### REST API

Use this for non-Node environments or custom integrations.

```bash
curl -X POST https://pg.new/api/v1/database \
  -H "Content-Type: application/json" \
  -d '{"ref":"my-app"}'
```

Full API reference: [references/api.md](./references/api.md)

### Vite Plugin

Use this for Vite projects that need automatic database setup on `vite dev`.

```typescript
import { defineConfig } from "vite";
import { postgres } from "vite-plugin-db";

export default defineConfig({
  plugins: [postgres()],
});
```

Full Vite plugin reference: [references/vite-plugin.md](./references/vite-plugin.md)

## Agent Workflow

1. Confirm user wants a temporary, no-signup database.
2. Pick CLI, SDK, or API (default to CLI).
3. If CLI, run `npx get-db@latest` in the project root.
4. Verify `DATABASE_URL` was added to the intended env file.
5. Offer a quick connection test (`SELECT 1`) in their stack.
6. Explain expiry and how to keep it via claim URL.

## Output to Provide to the User

Always return:

- where the connection string was written (for example `.env`)
- which variable key was used (`DATABASE_URL` or custom key)
- whether a `{prefix}POSTGRES_CLAIM_URL` is present (default: `PUBLIC_POSTGRES_CLAIM_URL`)
- a reminder that unclaimed DBs are temporary

## Claiming Your Database

Databases are temporary by default (typically 72 hours) and can be claimed later to a Neon account for permanent use - using the `{prefix}POSTGRES_CLAIM_URL` link (default: `PUBLIC_POSTGRES_CLAIM_URL`).

This is a web page, not an API endpoint. Users visit this URL in a browser to:

1. Sign in to their Neon account (or create one)
2. Transfer ownership of the database to their account
3. Once claimed, the database no longer expires

## Safety and UX Notes

- Do not overwrite existing env files; update in place.
- Ask before destructive seed SQL (`DROP`, `TRUNCATE`, mass `DELETE`).
- For production workloads, recommend standard Neon provisioning instead of temporary claimable DBs.
- If users need long-term persistence, instruct them to open the claim URL immediately.

---
name: claimable-postgres
description: >-
  Provision instant temporary Postgres databases via Claimable Postgres by Neon
  (pg.new) with no login, signup, or credit card. Use when users ask for a
  quick Postgres environment, a throwaway DATABASE_URL for prototyping/tests,
  or "just give me a DB now". Triggers include: "quick postgres", "temporary
  postgres", "no signup database", "no credit card database", "instant
  DATABASE_URL".
---

# Claimable Postgres

Create an instant Postgres database with Claimable Postgres by Neon (`pg.new`) for fast local development, demos, prototyping, and test environments.

Databases are temporary by default (typically 72 hours) and can be claimed later to a Neon account for permanent use.

## Quick Start

```bash
npx get-db
```

This creates a database and writes `DATABASE_URL` to `.env`.

## When to Use Which Method

### CLI (`npx get-db`)

Use this by default for most users who want a fast setup in an existing project.

```bash
npx get-db
```

Common flags:
- `-y, --yes`: skip prompts
- `-e, --env <path>`: choose env file path
- `-k, --key <name>`: customize env var key (default `DATABASE_URL`)
- `-s, --seed <path>`: run SQL seed file
- `-L, --logical-replication`: enable logical replication
- `-r, --ref <id>`: set source/referrer id

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

## Agent Workflow

1. Confirm user wants a temporary, no-signup database.
2. Ask whether they want CLI, SDK, or API (default to CLI).
3. If CLI, run `npx get-db` in the project root.
4. Verify `DATABASE_URL` was added to the intended env file.
5. Offer a quick connection test (`SELECT 1`) in their stack.
6. Explain expiry and how to keep it via claim URL.

## Output to Provide to the User

Always return:

- where the connection string was written (for example `.env`)
- which variable key was used (`DATABASE_URL` or custom key)
- whether a `PUBLIC_CLAIM_URL` is present
- a reminder that unclaimed DBs are temporary

## Safety and UX Notes

- Do not overwrite existing env files; update in place.
- Ask before destructive seed SQL (`DROP`, `TRUNCATE`, mass `DELETE`).
- For production workloads, recommend standard Neon provisioning instead of temporary claimable DBs.
- If users need long-term persistence, instruct them to open the claim URL immediately.

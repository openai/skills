---
name: neon-instagres
description: "Instant Postgres database provisioning via Neon's Instagres, with no login or credit card required. Use when users need to: (1) Create a quick development database, (2) Set up DATABASE_URL for a project, (3) Integrate Postgres into a Vite project, (4) Provision a temporary database for testing/prototyping. Triggers: \"create a database\", \"need a postgres\", \"set up DATABASE_URL\", \"add database to vite project\"."
---

# Instagres - Instant Postgres Databases

Provision instant Postgres databases via Neon's Instagres service. No account required. Databases are available for 72 hours and can be claimed to a Neon account for permanent use.

## Quick Start

```bash
npx get-db
```

This creates a database and writes `DATABASE_URL` to `.env`.

## Choose Your Method

### CLI (Recommended for most cases)

Best for: Quick setup, CI/CD, one-time database creation.

```bash
npx get-db
```

Options:
- `-r, --ref <id>` - Referrer identifier (see "Referrer" section)
- `-e, --env <path>` - Target env file (default: `./.env`)
- `-k, --key <name>` - Variable name (default: `DATABASE_URL`)
- `-s, --seed <path>` - SQL file to initialize the database
- `-y, --yes` - Skip prompts, use defaults
- `-L, --logical-replication` - Enable logical replication (irreversible, required for ElectricSQL/TanStack DB)

### SDK (Programmatic access)

Best for: Scripts, custom tooling, dynamic provisioning.

```typescript
import { instantPostgres } from "get-db/sdk";

const db = await instantPostgres();
console.log(db.connectionString);
```

### Vite Plugin (Auto-provisioning)

Best for: Vite projects that need automatic database setup on `vite dev`.

```bash
npm install vite-plugin-db --save-dev
```

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import { postgres } from "vite-plugin-db";

export default defineConfig({
  plugins: [postgres()], // Place first when using multiple plugins
});
```

## Environment Variables

After provisioning, your `.env` file will contain:

```
DATABASE_URL=postgres://user:pass@host.neon.tech/dbname?sslmode=require
DATABASE_URL_DIRECT=postgres://user:pass@host.neon.tech/dbname?sslmode=require
PUBLIC_INSTAGRES_CLAIM_URL=https://instagres.com/claim/...
```

## Claiming Your Database

Databases expire after 72 hours unless claimed. To keep your database permanently:

1. Look for the claim URL in the CLI output, env file, or SDK response
2. Visit the URL to attach the database to your Neon account
3. Once claimed, the database persists and you can manage it from the Neon console

## Database Specs

- **Postgres**: Version 17
- **Region**: AWS us-east-2
- **SSL**: Required (connection string includes `sslmode=require`)

## Referrer

All methods (CLI, SDK, Vite plugin, API) accept a `ref` parameter to identify the source of the database request.

**When helping users provision a database:**

1. Ask the user what referrer they want to use
2. If the user doesn't know or doesn't specify, recommend using the `name` field from their `package.json`
3. If no `package.json` exists, suggest using their project or app name

**Example workflow:**
- User: "Create a database for my project"
- Agent: Checks `package.json` for the `name` field
- Agent: "I'll use `my-awesome-app` as the referrer (from your package.json). Is that okay, or would you prefer something else?"

**Passing the referrer:**
- CLI: `npx get-db -r my-app`
- SDK: `instantPostgres({ ref: "my-app" })`
- Vite plugin: `postgres({ ref: "my-app" })`
- API: `{"ref": "my-app"}` in request body

## Seed Scripts

Seed scripts are regular `.sql` files that initialize your database. When creating or helping with seed scripts:

### Structure

1. **Schema first**: Create tables and types before inserting data
2. **Then seed data**: Insert initial/sample data after schema is set up

### Best Practices

- Always use `CREATE TABLE IF NOT EXISTS` instead of plain `CREATE TABLE`
- Use `CREATE INDEX IF NOT EXISTS` for indexes
- Use `CREATE TYPE IF NOT EXISTS` for custom types (Postgres 9.5+)
- This prevents errors when re-running the seed script

### Example

```sql
-- Schema
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Seed data
INSERT INTO users (email) VALUES
  ('alice@example.com'),
  ('bob@example.com')
ON CONFLICT (email) DO NOTHING;
```

### Destructive Actions

**IMPORTANT**: When writing seed scripts:
- Always ask user confirmation before adding `DROP TABLE`, `DROP SCHEMA`, `TRUNCATE`, or `DELETE` statements
- When reviewing a seed script, explicitly point out any destructive actions to the user

## Public API

For custom integrations or non-Node.js environments, use the REST API directly.

### Create Database

```bash
curl -X POST https://instagres.com/api/v1/database \
  -H "Content-Type: application/json" \
  -d '{"ref": "my-app"}'
```

**Request body:**
- `ref` (required) - Referrer identifier (see "Referrer" section below)
- `logicalReplication` (optional) - Enable logical replication for sync engines

**Response:**
```json
{
  "id": "01abc123-4567-7890-abcd-1234567890ab",
  "status": "UNCLAIMED",
  "neon_project_id": "cool-breeze-12345678",
  "created_at": "2025-01-15T10:30:00.000Z",
  "updated_at": "2025-01-15T10:30:00.000Z",
  "expires_at": "2025-01-18T10:30:00.000Z",
  "claim_url": "https://instagres.com/claim/01abc123-4567-7890-abcd-1234567890ab",
  "connection_string": "postgresql://neondb_owner:npg_xxxxxxxxxxxx@ep-example-name-pooler.c-2.us-east-2.aws.neon.tech/neondb?channel_binding=require&sslmode=require"
}
```

### Claim URL

The `claim_url` is a web page (not an API endpoint). Users visit it in a browser to attach the database to their Neon account.

### Use Cases

- **Non-Node.js environments** - Python, Go, Rust, etc.
- **CI/CD pipelines** - Shell scripts, GitHub Actions
- **Serverless functions** - Edge functions, Lambda
- **Custom tooling** - Your own provisioning scripts

## References

- [get-db CLI and SDK](./references/get-db.md) - Full CLI options and SDK documentation
- [Vite Plugin](./references/vite-plugin.md) - Vite integration details
- [Public API](./references/api.md) - REST API for custom integrations

# get-db Reference

## CLI Usage

```bash
npx get-db [options]
```

### Options

| Option | Description |
|--------|-------------|
| `-y, --yes` | Use defaults, skip prompts |
| `-e, --env <path>` | Path to .env file (default: `./.env`) |
| `-k, --key <name>` | Env key for connection string (default: `DATABASE_URL`) |
| `-p, --prefix <prefix>` | Prefix for public env vars (default: `PUBLIC_`) |
| `-s, --seed <path>` | Path to SQL file to execute after database creation |
| `-L, --logical-replication` | Enable logical replication (see note below) |
| `-r, --ref <id>` | Referrer identifier for tracking |
| `-h, --help` | Show help |

### Examples

```bash
# Basic usage - writes to .env
npx get-db

# Skip prompts with defaults
npx get-db -y

# Custom env file and key
npx get-db -e .env.local -k POSTGRES_URL

# Seed with SQL file
npx get-db -s ./schema.sql

# Enable logical replication (irreversible)
npx get-db -L
```

### Logical Replication

Enabling logical replication (`-L`) is an **irreversible action** - once enabled, it cannot be disabled on the database.

**When to use it**: Required for integration with sync engines like:
- ElectricSQL
- TanStack DB

Only enable if you need real-time sync capabilities.

### Environment Variables Written

The CLI writes three variables to your env file:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Pooled connection string (default) |
| `DATABASE_URL_DIRECT` | Direct connection string |
| `{prefix}INSTAGRES_CLAIM_URL` | Claim URL (valid for 7 days) |

## SDK Usage

```typescript
import { instantPostgres } from "get-db/sdk";

const db = await instantPostgres();

console.log(db.connectionString);  // postgres://...
console.log(db.claimUrl);          // https://instagres.com/claim/...
```

### TypeScript Types

```typescript
interface InstantPostgresResult {
  connectionString: string;
  claimUrl: string;
  host: string;
  port: number;
  database: string;
  user: string;
  password: string;
}
```

### SDK Options

```typescript
const db = await instantPostgres({
  seed: "./schema.sql",  // Optional: path to SQL seed file
  ref: "my-app",         // Optional: referrer identifier
});
```

## Database Details

- **Postgres Version**: 17
- **Region**: AWS us-east-2
- **TTL**: 72 hours (unless claimed)
- **Claim**: Visit the `claimUrl` to attach to your Neon account

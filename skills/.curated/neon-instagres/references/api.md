# Instagres Public API Reference

## Create Database

**Endpoint:** `POST https://instagres.com/api/v1/database`

**Content-Type:** `application/json`

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ref` | string | Yes | Referrer identifier (e.g., your app name) |
| `logicalReplication` | boolean | No | Enable logical replication (irreversible) |

### Response

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

### Response Fields

| Field | Description |
|-------|-------------|
| `id` | Unique database identifier (UUID) |
| `status` | `UNCLAIMED` or `CLAIMED` |
| `neon_project_id` | Underlying Neon project ID |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |
| `expires_at` | Expiration timestamp (72 hours from creation) |
| `claim_url` | URL to claim the database to a Neon account |
| `connection_string` | PostgreSQL connection string (pooled, includes `channel_binding=require&sslmode=require`) |

### Error Responses

**400 Bad Request** - Missing referrer:
```json
{
  "status": 400,
  "message": "Missing referrer",
  "hint": "Pass a `ref` to the request body to identify the source of the request."
}
```

**500 Internal Server Error** - Creation failed:
```json
{
  "status": 500,
  "message": "Failed to create the database."
}
```

## Claim Database

**URL:** `https://instagres.com/claim/{database_id}`

This is a web page, not an API endpoint. Users visit this URL in a browser to:
1. Sign in to their Neon account (or create one)
2. Transfer ownership of the database to their account
3. Once claimed, the database no longer expires

### Claim URL Validity

- Claim URLs are valid for 7 days from database creation
- After claiming, the database is managed through the [Neon Console](https://console.neon.tech)

## Example Usage

### cURL

```bash
# Create a database
curl -X POST https://instagres.com/api/v1/database \
  -H "Content-Type: application/json" \
  -d '{"ref": "my-app"}'

# Create with logical replication enabled
curl -X POST https://instagres.com/api/v1/database \
  -H "Content-Type: application/json" \
  -d '{"ref": "my-app", "logicalReplication": true}'
```

### JavaScript/TypeScript

```typescript
const response = await fetch("https://instagres.com/api/v1/database", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ ref: "my-app" }),
});

const db = await response.json();
console.log(db.connection_string);
```

### Python

```python
import requests

response = requests.post(
    "https://instagres.com/api/v1/database",
    json={"ref": "my-app"}
)

db = response.json()
print(db["connection_string"])
```

## Use Cases for Direct API Access

The CLI and SDK handle most use cases, but direct API access is useful for:

- **Custom tooling** - Integrating into your own scripts or CI/CD pipelines
- **Non-Node.js environments** - Using from Python, Go, Rust, etc.
- **Serverless functions** - Provisioning databases from edge functions
- **Automation** - Creating databases programmatically in any language

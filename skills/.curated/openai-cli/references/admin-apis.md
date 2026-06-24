# Admin APIs

Use Admin APIs when the task is to create a project and machine credentials for an app or agent. The CLI reads `OPENAI_ADMIN_KEY`; use `--admin-api-key` only for one-off overrides.

```bash
# Create the project that will own this app or agent and save the response.
openai admin:organization:projects create \
  --name "automation project" \
  --format json > project.json
PROJECT_ID="$(jq -r '.id' project.json)"

# Create a service account inside the project and save the full response.
openai admin:organization:projects:service-accounts create \
  --project-id "$PROJECT_ID" \
  --name "automation bot" \
  --format json > service-account.json

# Extract the returned API key into an env file for the workload to use.
jq -r '.api_key.value | "OPENAI_API_KEY=\(.)"' \
  service-account.json > .env
```

## Agent Rules

- The core provisioning flow is project -> service account -> API key.
- Treat the generated project JSON, service-account JSON, and `.env` as secrets; add them to `.gitignore` before using this pattern in a repository.
- Use project and service-account writes only when the user explicitly asks for them.
- Do not invent or create admin credentials. If the user asks for an Admin API workflow but no admin key is configured, explain that the CLI expects `OPENAI_ADMIN_KEY`.

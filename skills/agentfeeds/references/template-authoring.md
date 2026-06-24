# Template Authoring

Use local templates when no built-in template fits a private file, dashboard, API, or approved read-only command.

Built-in templates are sourced from the standalone catalog repository:

```text
https://github.com/verkyyi/agentfeeds-catalog
```

The skill bundle includes a frozen catalog snapshot for offline first-run discovery. Updated catalog files are cached under `~/.agentfeeds/catalog-cache/` by the refresh worker. User-local templates live under `~/.agentfeeds/templates/` and are merged into discovery at runtime.

Start by checking built-ins:

```bash
python3 scripts/agentfeeds.py templates find <topic>
python3 scripts/agentfeeds.py templates show <template-id>
```

List supported adapter kinds:

```bash
python3 scripts/agentfeeds.py admin templates adapters
```

Scaffold a draft:

```bash
python3 scripts/agentfeeds.py admin templates scaffold <adapter-kind> <template-id>
```

The scaffold command prints the generated file paths. Edit the template YAML, then validate and dry-run it:

```bash
python3 scripts/agentfeeds.py admin templates validate
python3 scripts/agentfeeds.py admin templates test <template-id> key=value
```

Local templates live under the Agent Feeds runtime root:

```text
~/.agentfeeds/templates/streams/
~/.agentfeeds/templates/schemas/event-types/
```

Use `local_command` only for explicitly approved read-only commands. Commands must be argv arrays, not shell strings. Avoid commands that mutate files, cloud resources, accounts, or external services. New command templates are written with `pending: true` and cannot run until the operator approves them.

Local command templates require an interactive command digest approval before they can run:

```bash
python3 scripts/agentfeeds.py admin templates approve-command <template-id> [key=value ...]
```

Tell the user to run approval themselves in a terminal. Do not approve on the user's behalf. If the command, parameters, or template YAML change, approve the new digest before testing, subscribing, or refreshing.

For templates that need secrets, store only references in YAML:

```yaml
headers:
  Authorization: "Bearer {{secret:github_token}}"
```

Tell the user to set the value with:

```bash
python3 scripts/agentfeeds.py admin secrets set github_token
```

On macOS this uses Keychain when available; other platforms fall back to a local 0600 secret file under the Agent Feeds root.

macOS personal sources are built-in catalog templates under `mac/*`. Prefer those before creating operator-local templates.

---
name: remote-bridge
description: Deploy code and manage remote servers over SSH. Use when the user wants to deploy, sync files, run a remote command, restart a service, or check logs on a server they manage.
---

# remote-bridge

Deploy and manage remote servers directly from Codex — sync files, run commands, restart services, and tail logs over SSH.

> **Requires the remote-bridge MCP server installed separately.**
> This skill does not ship the server. Install it first, then add it to your MCP config.

## Prerequisites

### 1. Install the MCP server

```bash
npm install -g remote-bridge-cli
```

### 2. Add to Codex MCP config

```json
{
  "mcpServers": {
    "remote-bridge": {
      "command": "remote-bridge",
      "args": ["mcp"]
    }
  }
}
```

### 3. Create `remotebridge.yaml` in your project root

```yaml
project_name: "my-app"
targets:
  staging:
    host: "your-server.com"
    user: "ubuntu"
    remote_path: "/var/www/app"
    ssh_key: "~/.ssh/id_rsa"
    restart_cmd: "pm2 restart app"
    logs:
      - "/var/www/app/logs/error.log"
  production:
    host: "prod.example.com"
    user: "ubuntu"
    remote_path: "/var/www/app"
    ssh_key: "~/.ssh/id_rsa"
    restart_cmd: "pm2 restart app"
    require_confirmation: true
    logs:
      - "/var/www/app/logs/error.log"
```

## Tools

| Tool | Description |
|---|---|
| `sync_to_remote` | Sync a local directory to the remote server |
| `run_remote_command` | Run a shell command on the remote server |
| `preflight_check` | Check remote OS and available runtimes |
| `fetch_logs` | Tail recent lines from configured log files |
| `restart_service` | Restart the remote service |
| `deploy` | Full pipeline: sync → restart → tail logs on failure |

## Safety

- `delete` is **off by default** on `sync_to_remote`. Pass `delete=true` only for intentional full-mirror syncs.
- Set `require_confirmation: true` on production targets — sync returns a dry-run preview and requires `confirm=true` before executing.
- Always pass `local_path` explicitly on `sync_to_remote`.

## Workflow

**Deploy:** Call `deploy` — it syncs, restarts, and tails logs on failure automatically.

**Sync only:** Run with `dry_run=true` first, show the preview, then re-run to execute.

**Logs:** Call `fetch_logs` with a `lines` count (default 50).

## Example prompts

- "Deploy the current project to staging"
- "Show me what would change if I synced to production"
- "Run `npm install` on the staging server"
- "Show me the last 100 lines of logs"
- "Restart the production service"

## Source

- GitHub: https://github.com/varaprasadreddy9676/remote-bridge
- npm: `remote-bridge-cli`
- License: MIT

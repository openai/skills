---
name: remote-bridge
description: Sync files, run commands, tail logs, and deploy to remote servers over SSH and rsync. Use when the user wants to deploy code, sync a directory, run a remote command, or check logs on a Linux server they manage.
---

# remote-bridge

Deploy and manage remote Linux servers directly from Codex — sync files via rsync, run shell commands, tail logs, restart services, and run full deploy pipelines over SSH.

## Prerequisites

Install the remote-bridge CLI (Rust binary, ships as an npm package):

```bash
npm install -g remote-bridge-cli
```

Create a `remotebridge.yaml` in your project root:

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

Add to Codex MCP config:

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

## Tools

| Tool | Description |
|---|---|
| `sync_to_remote` | Sync a local directory to the remote server via rsync |
| `run_remote_command` | Run a shell command on the remote server |
| `preflight_check` | Check remote OS, Node.js, Python, Rust, Docker versions |
| `fetch_logs` | Tail recent lines from configured remote log files |
| `restart_service` | Restart the remote service via `restart_cmd` |
| `deploy` | Full pipeline: sync → restart → tail logs on failure |

## Safety

- `delete` is **off by default** on `sync_to_remote`. Only pass `delete=true` for intentional full-mirror syncs.
- Set `require_confirmation: true` on production targets. A dry-run preview is returned and `confirm=true` is required before syncing.
- Always pass `local_path` explicitly on `sync_to_remote`. Never assume `.` is the right directory.
- For production syncs, always run `dry_run=true` first and show the preview before executing.

## Workflow

### Deploy
1. Run `preflight_check` on first deploy or when server state is unknown.
2. Call `deploy` — it runs sync, restart, and tails logs automatically on failure.

### Sync only
1. Confirm `local_path` with the user.
2. Run `sync_to_remote` with `dry_run=true` and show the preview.
3. Get user confirmation, then re-run without `dry_run`.

### Logs
Call `fetch_logs` with a `lines` count appropriate to the situation (default 50, more when debugging).

## Example prompts

- "Deploy the current project to staging"
- "Sync the ./dist folder to production"
- "Show me a dry run of what would sync to production"
- "Run `npm install` on the staging server"
- "Show me the last 100 lines of error logs on staging"
- "Restart the production service"

## Source

- GitHub: https://github.com/varaprasadreddy9676/remote-bridge
- npm: `remote-bridge-cli`
- License: MIT

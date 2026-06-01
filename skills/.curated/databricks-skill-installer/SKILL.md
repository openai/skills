---
name: databricks-skill-installer
description: Run `databricks aitools install --global` to install or refresh Databricks skills for Codex and other supported coding agents. Use when Codex needs to bootstrap Databricks skills with the Databricks CLI or install a specific Databricks skill such as `databricks-apps` or `databricks-jobs`.
---

# Databricks Skill Installer

First check:

```bash
databricks -v
```

If the command is missing, follow the upstream Databricks CLI install guide and treat it as the source of truth. In a sandboxed agent session, show the user the appropriate install command from that guide and ask them to run it in their own terminal.

[databricks-cli-install.md](https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks/databricks-cli-install.md)

Run:

```bash
databricks aitools install --global --agents codex
```

Install one skill with:

```bash
databricks aitools install --global --agents codex --skills databricks-apps
```

After installation, restart Codex so the newly installed skills are discovered. Until you restart, the current session can only inspect the installed files under `${CODEX_HOME:-~/.codex}/skills` — the new skills won't be invokable. Once Codex restarts, open the installed Databricks skill and follow its upstream `SKILL.md`.

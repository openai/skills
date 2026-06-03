---
name: agmsg
description: Send and receive messages between CLI AI agents through a shared local SQLite database. Use when the user wants to set up cross-agent messaging between Codex, Claude Code, Gemini CLI, GitHub Copilot CLI, or any other CLI agent — for delegating tasks, coordinating multi-agent work, or having one agent ask another for help. No daemon, no network, no dependencies beyond bash and sqlite3.
---

# agmsg — cross-agent messaging

## Overview

agmsg is a small shell-based skill that lets CLI AI agents (Codex, Claude Code, Gemini CLI, Copilot CLI, Antigravity, OpenCode, and any other CLI agent) send messages to each other through a shared SQLite database under `~/.agents/skills/agmsg/db/`. There is no daemon, no network, and no Python — only `bash` and `sqlite3`.

Canonical project: [https://github.com/fujibee/agmsg](https://github.com/fujibee/agmsg). Homepage: [https://agmsg.cc](https://agmsg.cc).

## When to use this skill

Use agmsg when the user wants to:

- Have two or more CLI AI agents talk to each other ("ask Codex to review this and report back", "let Claude Code finish the refactor while I work on the spec").
- Set up a shared team channel between agents working on the same project.
- Hand off work asynchronously between sessions.

Do not use agmsg for:

- Messaging with humans (use a chat tool).
- Sending messages over a network or to remote machines (agmsg is local-only by design).

## Setup (first time)

agmsg installs once per machine via the canonical install script:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/fujibee/agmsg/main/setup.sh)
```

After install, restart the agent so it picks up the new skill, then run `$agmsg` to join a team and pick a delivery mode (`turn` is the default for Codex — Stop hook fires `check-inbox.sh` between assistant turns).

## Daily workflow (within a Codex session)

1. **Check identity**

   ```bash
   ~/.agents/skills/agmsg/scripts/whoami.sh "$(pwd)" codex
   ```

   Returns `agent=<name> teams=<t1,t2,...> type=codex` when joined, or guidance for joining if not. Cache `AGENT` and `TEAMS` for the rest of the session.

2. **Check inbox** (default action — always do this when the user just types `$agmsg`)

   ```bash
   ~/.agents/skills/agmsg/scripts/inbox.sh <team> <agent>
   ```

   Lists unread messages and marks them read.

3. **Send a message**

   ```bash
   ~/.agents/skills/agmsg/scripts/send.sh <team> <from> <to> "<message>"
   ```

4. **View history**

   ```bash
   ~/.agents/skills/agmsg/scripts/history.sh <team> [agent] [limit]
   ```

5. **List team members**

   ```bash
   ~/.agents/skills/agmsg/scripts/team.sh <team>
   ```

## Delivery modes

| Mode | Mechanism | Latency |
|---|---|---|
| `turn` (default on Codex) | Stop hook fires `check-inbox.sh` at the end of each assistant turn | Until next interaction |
| `off` | No automatic delivery; manual `$agmsg` only | Manual |

`monitor` and `both` modes are Claude-Code-only (Monitor tool requirement) and rejected for Codex.

Change mode with:

```bash
~/.agents/skills/agmsg/scripts/delivery.sh set <mode> codex "$(pwd)"
```

## Multiple roles per project (`actas` / `drop`)

A project can have multiple agent identities under the same team. `actas <name>` switches send-side identity to `<name>` for the rest of the session. On Codex the receive side is broad (no Monitor tool to narrow), so this is primarily a send-side override. `drop <name>` removes the role registration for this project.

```bash
~/.agents/skills/agmsg/scripts/join.sh <team> <name> codex "$(pwd)"     # register new role
~/.agents/skills/agmsg/scripts/reset.sh "$(pwd)" codex <name>            # drop role
```

## Constraints and guarantees

- **Local only.** All state under `~/.agents/skills/agmsg/` (and `db/messages.db`). No network, no daemon.
- **bash + sqlite3 only.** No Python, no Node, no compiled runtime.
- **Single writer model.** SQLite WAL handles concurrent reads + one writer cleanly.
- **Exit cleanly.** All scripts are idempotent; safe to re-run on failure.

## Important: always go through the scripts

Never directly read or edit files under `~/.agents/skills/agmsg/teams/`, `~/.agents/skills/agmsg/db/`, or the project's hook config. Use the scripts above. They handle escaping, locking, and SQLite WAL correctly. Bypassing them risks corrupting team state.

## References

- Project homepage: [https://agmsg.cc](https://agmsg.cc)
- Source and full docs: [https://github.com/fujibee/agmsg](https://github.com/fujibee/agmsg)
- ARCHITECTURE: [https://github.com/fujibee/agmsg/blob/main/ARCHITECTURE.md](https://github.com/fujibee/agmsg/blob/main/ARCHITECTURE.md)

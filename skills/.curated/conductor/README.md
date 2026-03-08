<p align="center">
  <img src="assets/conductor.png" alt="Conductor" width="120">
</p>

<h1 align="center">Conductor Skills</h1>

<p align="center">
  Teach your AI coding agent to create, run, monitor, and manage
  <a href="https://github.com/conductor-oss/conductor">Conductor</a> workflow orchestrations.
</p>

<p align="center">
  <a href="https://github.com/conductor-oss/conductor-skills/blob/main/LICENSE.txt">
    <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License">
  </a>
</p>

---

## What You Get

Once installed, your AI agent can:

- **Create** workflow definitions with any task type (HTTP, SWITCH, FORK, WAIT, etc.)
- **Run** workflows synchronously or asynchronously
- **Monitor** executions and search by status, time, or correlation ID
- **Manage** workflows — pause, resume, terminate, retry, restart
- **Signal** WAIT and HUMAN tasks for human-in-the-loop patterns
- **Write workers** in Python, JavaScript, Java, Go, C#, Ruby, or Rust
- **Visualize** workflows as Mermaid diagrams
- **Manage** schedules, secrets, and webhooks (Orkes enterprise)

---

## Quick Install

### 1. Pick your agent &nbsp;&nbsp; 2. Run one command &nbsp;&nbsp; 3. Set your server URL

<br>

> **All you need is a terminal with `curl`.** No git, no cloning, no dev tools.

<br>

### Claude Code

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent claude
```

### Codex CLI (OpenAI)

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent codex --project-dir .
```

### Gemini CLI

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent gemini --project-dir .
```

### Cursor

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent cursor --project-dir .
```

### Windsurf

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent windsurf --project-dir .
```

### Cline

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent cline --project-dir .
```

### GitHub Copilot

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent copilot --project-dir .
```

### Aider

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent aider --project-dir .
```

### Amazon Q Developer

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent amazonq --project-dir .
```

### Roo Code

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent roo --project-dir .
```

### Amp

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent amp --project-dir .
```

### OpenCode

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent opencode --project-dir .
```

<br>

### Step 3: Set your server URL

```bash
export CONDUCTOR_SERVER_URL=http://localhost:8080/api

# Optional: if your server requires authentication
export CONDUCTOR_AUTH_TOKEN=your-token-here
```

That's it. Ask your agent: *"Create a workflow that fetches weather data and sends a notification."*

---

## Supported Agents

| Agent | Flag | What gets installed |
|-------|------|-------------------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `claude` | Native skill (via `claude skill add`) |
| [Codex CLI](https://github.com/openai/codex) | `codex` | `AGENTS.md` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `gemini` | `GEMINI.md` |
| [Cursor](https://cursor.com) | `cursor` | `.cursor/rules/conductor.mdc` |
| [Windsurf](https://codeium.com/windsurf) | `windsurf` | `.windsurfrules` |
| [Cline](https://github.com/cline/cline) | `cline` | `.clinerules` |
| [GitHub Copilot](https://github.com/features/copilot) | `copilot` | `.github/copilot-instructions.md` |
| [Aider](https://aider.chat) | `aider` | `.conductor-skills/` + `.aider.conf.yml` |
| [Amazon Q](https://aws.amazon.com/q/developer/) | `amazonq` | `.amazonq/rules/conductor.md` |
| [Roo Code](https://github.com/RooVetGit/Roo-Code) | `roo` | `.roo/rules/conductor.md` |
| [Amp](https://ampcode.com) | `amp` | `.amp/instructions.md` |
| [OpenCode](https://github.com/opencode-ai/opencode) | `opencode` | `AGENTS.md` |

---

## Uninstall

```bash
curl -sSL https://raw.githubusercontent.com/conductor-oss/conductor-skills/main/install.sh | bash -s -- --agent <name> --project-dir . --uninstall
```

---

## Examples

| Example | Description |
|---------|-------------|
| [Create and Run a Workflow](examples/create-and-run-workflow.md) | Define a workflow, register it, and execute it end-to-end |
| [Monitor and Retry](examples/monitor-and-retry.md) | Search executions, diagnose failures, and batch-retry |
| [Signal a Wait Task](examples/signal-wait-task.md) | Human-in-the-loop with WAIT tasks and external signals |

## References

| Reference | Description |
|-----------|-------------|
| [Workflow Definition Schema](references/workflow-definition.md) | Full JSON schema, all task types, input expressions |
| [Writing Workers](references/workers.md) | SDK examples in Python, JavaScript, Java, Go, and more |
| [API Reference](references/api-reference.md) | REST endpoints for direct API access |

## Evaluations

The `evaluations/` directory contains automated test scenarios to validate the skill works correctly with your agent. See [evaluations/README.md](evaluations/README.md) for details.

```bash
python3 scripts/run_evals.py --verbose
```

---

## License

Apache 2.0 — see [LICENSE.txt](LICENSE.txt).

Built for [Conductor OSS](https://github.com/conductor-oss/conductor). Enterprise features powered by [Orkes](https://orkes.io).

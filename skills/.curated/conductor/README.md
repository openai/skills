<p align="center">
  <img src="assets/conductor.png" alt="Conductor" width="120">
</p>

<h1 align="center">Conductor Skills</h1>

<p align="center">
  Teach your AI coding agent to create, run, monitor, and manage
  <a href="https://github.com/conductor-oss/conductor">Conductor</a> workflow orchestrations.
</p>

<p align="center">
  <a href="https://github.com/conductor-oss/conductor">
    <img src="https://img.shields.io/github/stars/conductor-oss/conductor?style=social" alt="Star Conductor">
  </a>
  &nbsp;&middot;&nbsp;
  <a href="https://join.slack.com/t/orkes-conductor/shared_invite/zt-3dpcskdyd-W895bJDm8psAV7viYG3jFA">
    <img src="https://img.shields.io/badge/Slack-Join%20Community-4A154B?logo=slack" alt="Join Slack">
  </a>
  &nbsp;&middot;&nbsp;
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

### Install for all detected agents

One command to auto-detect every supported agent on your system and install globally where possible. Re-run anytime — it only installs for newly detected agents.

**macOS / Linux**
```bash
curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh | bash -s -- --all
```

**Windows (PowerShell)**
```powershell
irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -All
```

**Windows (cmd)**
```cmd
powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -All"
```

### Install for a specific agent

You can also install for a single agent. Agents marked with <sup>*</sup> require per-project install — run the command from your project directory.

 
<details>
<summary><strong>macOS / Linux</strong></summary>

| Agent | Command |
|-------|---------|
| [Cline](https://github.com/cline/cline) <sup>*</sup> | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent cline` |
| [GitHub Copilot](https://github.com/features/copilot) <sup>*</sup> | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent copilot` |
| [Amazon Q](https://aws.amazon.com/q/developer/) <sup>*</sup> | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent amazonq` |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent claude` |
| [Codex CLI](https://github.com/openai/codex) | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent codex --global` |
| [Cursor](https://cursor.com) | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent cursor --global` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent gemini --global` |
| [Windsurf](https://codeium.com/windsurf) | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent windsurf --global` |
| [Aider](https://aider.chat) | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent aider --global` |
| [Roo Code](https://github.com/RooVetGit/Roo-Code) | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent roo --global` |
| [Amp](https://ampcode.com) | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent amp --global` |
| [OpenCode](https://opencode.ai) | `curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh \| bash -s -- --agent opencode --global` |
</details>


<details>
<summary><strong>Windows PowerShell</strong></summary>

| Agent | Command |
|-------|---------|
| [Cline](https://github.com/cline/cline) <sup>*</sup> | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent cline` |
| [GitHub Copilot](https://github.com/features/copilot) <sup>*</sup> | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent copilot` |
| [Amazon Q](https://aws.amazon.com/q/developer/) <sup>*</sup> | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent amazonq` |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent claude` |
| [Codex CLI](https://github.com/openai/codex) | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent codex -Global` |
| [Cursor](https://cursor.com) | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent cursor -Global` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent gemini -Global` |
| [Windsurf](https://codeium.com/windsurf) | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent windsurf -Global` |
| [Aider](https://aider.chat) | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent aider -Global` |
| [Roo Code](https://github.com/RooVetGit/Roo-Code) | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent roo -Global` |
| [Amp](https://ampcode.com) | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent amp -Global` |
| [OpenCode](https://opencode.ai) | `irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent opencode -Global` |

</details>

<details>
<summary><strong>Windows Command Prompt (cmd)</strong></summary>

| Agent | Command |
|-------|---------|
| [Cline](https://github.com/cline/cline) <sup>*</sup> | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent cline"` |
| [GitHub Copilot](https://github.com/features/copilot) <sup>*</sup> | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent copilot"` |
| [Amazon Q](https://aws.amazon.com/q/developer/) <sup>*</sup> | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent amazonq"` |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent claude"` |
| [Codex CLI](https://github.com/openai/codex) | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent codex -Global"` |
| [Cursor](https://cursor.com) | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent cursor -Global"` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent gemini -Global"` |
| [Windsurf](https://codeium.com/windsurf) | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent windsurf -Global"` |
| [Aider](https://aider.chat) | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent aider -Global"` |
| [Roo Code](https://github.com/RooVetGit/Roo-Code) | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent roo -Global"` |
| [Amp](https://ampcode.com) | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent amp -Global"` |
| [OpenCode](https://opencode.ai) | `powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent opencode -Global"` |

</details>

> <sup>*</sup> Global install not supported — run from your project directory. You can also omit `--global` / `-Global` for any agent to do a project-level install instead.

That's it — ask your agent to connect to your server (see [Try It](#try-it) below).

---

## Supported Agents

| Agent | Flag | Global install | Project install |
|-------|------|---------------|-----------------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `claude` | Native skill (via `claude skill add`) | — |
| [Codex CLI](https://github.com/openai/codex) | `codex` | `~/.codex/AGENTS.md` | `AGENTS.md` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `gemini` | `~/.gemini/GEMINI.md` | `GEMINI.md` |
| [Cursor](https://cursor.com) | `cursor` | `~/.cursor/skills/conductor/SKILL.md` | `.cursor/rules/conductor.mdc` |
| [Windsurf](https://codeium.com/windsurf) | `windsurf` | `~/.codeium/windsurf/memories/global_rules.md` | `.windsurfrules` |
| [Cline](https://github.com/cline/cline) | `cline` | — | `.clinerules` |
| [GitHub Copilot](https://github.com/features/copilot) | `copilot` | — | `.github/copilot-instructions.md` |
| [Aider](https://aider.chat) | `aider` | `~/.conductor-skills/` + `~/.aider.conf.yml` | `.conductor-skills/` + `.aider.conf.yml` |
| [Amazon Q](https://aws.amazon.com/q/developer/) | `amazonq` | — | `.amazonq/rules/conductor.md` |
| [Roo Code](https://github.com/RooVetGit/Roo-Code) | `roo` | `~/.roo/rules/conductor.md` | `.roo/rules/conductor.md` |
| [Amp](https://ampcode.com) | `amp` | `~/.config/AGENTS.md` | `.amp/instructions.md` |
| [OpenCode](https://opencode.ai) | `opencode` | `~/.config/opencode/skills/conductor/SKILL.md` | `AGENTS.md` |

---

## Try It

After installing, try these prompts with your agent:

**Configure**
- *"Connect to my Conductor server at https://play.orkes.io/api"*
- *"Save my Conductor server config as a profile called production"*
- *"Switch to my staging Conductor profile"*

**Create & Run**
- *"Create a workflow that calls the GitHub API to get open issues and sends a Slack notification"*
- *"Run the my-workflow workflow with input {\"userId\": 123}"*

**Monitor**
- *"Show me all failed workflow executions from the last hour"*
- *"What's the status of execution abc-123?"*

**Manage**
- *"Retry all failed executions of my-workflow"*
- *"Pause the running execution xyz-456"*

**Human-in-the-Loop**
- *"Signal the wait task in execution abc-123 with approval: true"*

**Modify**
- *"Add an error-handling branch to the order-processing workflow"*
- *"Add a WAIT task before the payment step in my checkout workflow"*

**Workers**
- *"Write a Python worker that processes image thumbnails"*
- *"Write a JavaScript worker that validates email addresses"*
- *"Generate a Go worker that fetches data from a REST API and transforms the response"*

**Visualize**
- *"Show me a diagram of the order-processing workflow"*

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

## Upgrade

Check for a newer version and upgrade all installed agents:

**macOS / Linux**
```bash
curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh | bash -s -- --all --upgrade
```

**Windows**
```powershell
irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -All -Upgrade
```

Or upgrade a single agent: `--agent <name> --upgrade`

---

## Uninstall

**macOS / Linux**
```bash
# Remove a global install
curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh | bash -s -- --agent <name> --global --uninstall

# Remove a project-level install
curl -sSL https://conductor-oss.github.io/conductor-skills/install.sh | bash -s -- --agent <name> --uninstall
```

**Windows (PowerShell)**
```powershell
# Remove a global install
irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent <name> -Global -Uninstall

# Remove a project-level install
irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent <name> -Uninstall
```

**Windows (cmd)**
```cmd
powershell -c "irm https://conductor-oss.github.io/conductor-skills/install.ps1 -OutFile install.ps1; .\install.ps1 -Agent <name> -Global -Uninstall"
```

---

## License

Apache 2.0 — see [LICENSE.txt](LICENSE.txt).

Built for [Conductor OSS](https://github.com/conductor-oss/conductor). Enterprise features powered by [Orkes](https://orkes.io).

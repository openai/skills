# Migration Differences

## Summary

This reference covers Claude Code to Codex migration only. It lists migration differences, partial mappings, and unsupported Claude Code behavior. Direct 1:1 mappings are intentionally omitted. When the converter preserves Claude-only semantics as prompt guidance, it also emits a `manual_fix_required` report row and writes a `## MANUAL MIGRATION REQUIRED` block into the generated file.

Docs last checked: 2026-04-20. If today's date is later, re-open the official Codex docs below and the Claude Code docs map before trusting these mappings.

## Instructions

| Source | Codex | Migration behavior | Caveat |
| --- | --- | --- | --- |
| `.claude/CLAUDE.md`, `CLAUDE.md`, or `claude.md` | `AGENTS.md` symlink | Linked automatically when content looks provider-neutral | This keeps one shared instruction body instead of duplicating docs. |
| Root `AGENTS.md` | Root `AGENTS.md` | Reported as active | The converter does not overwrite or symlink the target file to itself. |
| Instruction content with `/hooks`, `.claude/agents/`, settings paths, subagent language, or permission-mode assumptions | Generated `AGENTS.md` copy | Manual rewrite pass | The converter intentionally breaks the symlink when obvious Claude-only semantics need a Codex-specific edit. |

## Commands

| Source | Codex | Migration behavior | Caveat |
| --- | --- | --- | --- |
| `.claude/commands/*.md` | `.agents/skills/source-command-<name>/SKILL.md` | Converted to one-file Codex skills | Slash-command invocation, `argument-hint`, `allowed-tools`, `$ARGUMENTS`, shell-output interpolation, and file-reference expansion are preserved as manual-review text. |
| Command files with runtime expansion | One-file Codex skills plus `manual_fix_required` rows | Preserved as prompt text | Argument placeholders, shell-output interpolation, automatic file expansion, model/agent routing, and executable hook behavior have different runtime behavior and must be checked manually. |

## Skills

| Source | Codex | Migration behavior | Caveat |
| --- | --- | --- | --- |
| `.claude/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` | Converted; selected support directories are copied | Skill-local `scripts/`, `references/`, and `assets/` are copied when they are real files under the source skill root. |
| `.claude/skills/<name>.md` | `.agents/skills/<name>/SKILL.md` | Converted as a single-file skill | No sibling support directories are copied for this legacy shape. |
| `--skill <name>` | Selected `.agents/skills/<name>/SKILL.md` | Converts only matching Claude skill folders or single-file skills | `--skill` may be passed multiple times, implies `--skills`, skips slash-command conversion, and cannot be combined with `--replace`. |
| `allowed-tools` | No strict skill allowlist | Preserved as prompt guidance in `SKILL.md` | `agents/openai.yaml` can declare tool dependencies, but that is not a permission boundary. |
| `user-invocable` | `policy.allow_implicit_invocation` | Manual review only | Similar intent, not equivalent semantics. |
| `model` / `effort` | No skill-level model pin | Unsupported | Codex model selection is session/agent scoped in this converter. |
| `disable-model-invocation` | No direct equivalent | Unsupported | Requires a manual rewrite if the source skill depends on this behavior. |
| `argument-hint` / `context` / `agent` / `hooks` / `paths` / `shell` | No direct equivalent | Unsupported | Keep only if the behavior can be rewritten into prompt guidance or config. |

## MCP and config

| Source | Codex | Migration behavior | Caveat |
| --- | --- | --- | --- |
| `.mcp.json` or `.claude.json` `mcpServers` | `.codex/config.toml` `[mcp_servers.<name>]` | Converted | Project `.mcp.json` and global `.claude.json` use the same source shape for this migrator. Codex supports additional MCP server fields such as `cwd`, `enabled_tools`, `disabled_tools`, and timeout settings, but this converter only writes fields that map clearly from Claude source config. |
| Claude Code model/sandbox settings or MCP config | `personality = "friendly"` | Written when the migrator generates `.codex/config.toml` | Codex supports `none`, `friendly`, and `pragmatic`; Claude Code migrations default to friendly to preserve a warm assistant style. |
| `type: sse` | No SSE support | Unsupported | Codex supports stdio and streamable HTTP in current docs. |
| `headers.Authorization: Bearer ${VAR}` | `bearer_token_env_var` | Direct auth rewrite | Only the bearer-token shape is rewritten this way; `${VAR:-default}` fallbacks are not preserved. |
| `headers` with `${VAR}` | `env_http_headers` | Partial mapping | Static headers map to `http_headers`; `${VAR:-default}` fallbacks are not preserved. |
| `env` with `${VAR}` | `env_vars` | Partial mapping | Literal values stay in `env`; self-references become `env_vars`, and `${VAR:-default}` fallbacks are not preserved. |
| `oauth.callbackPort` | `mcp_oauth_callback_port` | Manual review only | `oauth.clientId`, `oauth.authServerMetadataUrl`, and `headersHelper` are unsupported. |
| `enabledMcpjsonServers` / `disabledMcpjsonServers` | Per-server `enabled` | Partial mapping | `enableAllProjectMcpServers` has no direct equivalent in this converter. |
| `allowedMcpServers` / `deniedMcpServers` | `requirements.toml` | Manual policy mapping | Not written by this converter. |
| `.claude/settings.local.json` | No local-only Codex equivalent | Unsupported | Codex project config is tied to trusted project behavior. |

## Subagents

| Source | Codex | Migration behavior | Caveat |
| --- | --- | --- | --- |
| `.claude/agents/*.md` | `.codex/agents/*.toml` | Converted | Missing `name` or `description` is inferred and reported for review. |
| `tools` / `disallowedTools` | No source-style fine-grained agent permissions | Preserved as prompt guidance in `developer_instructions` | Use `sandbox_mode`, `[permissions]`, MCP tool filters, or app tool filters manually when intent is clear. |
| `skills` | No spawn-time preload equivalent | Preserved as prompt guidance in `developer_instructions` | `skills.config` is enable/disable config, not preload behavior. |
| `mcpServers` | Codex custom-agent `mcp_servers` or shared Codex MCP config | Manual review only | Codex custom-agent files can include MCP config, but this converter does not automatically map Claude subagent `mcpServers`. Use shared Codex MCP config or manually add agent-local `mcp_servers` when the source intent is clear. |
| `permissionMode` | `sandbox_mode` | Partial mapping | Only `acceptEdits` and `readOnly` are mapped; `default`, `dontAsk`, `bypassPermissions`, and `plan` are preserved as manual-review prompt guidance. |
| `model` + `effort` | `model` + `model_reasoning_effort` | Partial mapping by model family | Sonnet-family effort is biased one tier higher for coding-agent behavior; source `max` maps to Codex `xhigh`. |
| `hooks` / `memory` / `background` / `isolation` / `maxTurns` | No direct equivalent | Unsupported | Foreground/background and resume behavior do not map cleanly to Codex custom-agent files. |
| `initialPrompt` | No direct equivalent | Unsupported | Only applies when the agent runs as the main Claude session agent. |
| Auto-delegation by `description` | Automatic or explicit Codex sub-agent spawning | Behavior change | Not a 1:1 match; verify generated agent descriptions manually. |
| Independent agent permissions | Parent sandbox inheritance + runtime overrides | Behavior change | Codex custom-agent files set defaults, not hard isolation from the parent turn. |

## Plugin Marketplaces

| Source | Codex | Migration behavior | Caveat |
| --- | --- | --- | --- |
| `.claude/plugins/` | Codex plugins / skills / MCP servers / apps | Reported as `manual_fix_required` only | Codex plugins can bundle skills, MCP servers, and apps, but the migrator does not copy plugin trees. Migrate the plugin, bundled skills, commands, agents, hooks, and MCP config by hand. |
| `.claude/plugin-marketplaces.json` | Codex plugin install or local plugin path | Reported as `manual_fix_required` only | Marketplace entries can point to local or remote plugin sources; the migrator does not fetch or install them. Codex marketplace metadata lives under `.agents/plugins/marketplace.json` or `~/.agents/plugins/marketplace.json`. |
| `.claude-plugin/marketplace.json` | Codex plugin install or local plugin path | Reported as `manual_fix_required` only | Treat it as marketplace source material. Do not copy it into Codex as a legacy marketplace; adapt it to the Codex plugin marketplace layout if you keep it local. |
| `metadata.pluginRoot` | No direct equivalent | Unsupported | Shorthand plugin sources that depend on `metadata.pluginRoot` need manual layout. |
| Marketplace or `plugin.json` custom `skills` / `agents` paths | Codex plugin manifest and bundled skill paths | Manual review only | Codex plugins can declare bundled skills, MCP servers, and apps. Custom Claude plugin paths still need manual layout review; no automated scan. |
| Plugin `commands/` | `.agents/skills/<name>/SKILL.md` | Manual | Treat like any other command migration if you copy files by hand. |
| `strict`, `hooks`, `mcpServers`, `lspServers`, `outputStyles` | No direct equivalent | Unsupported | No automatic plugin config import. |

## Hooks

| Source | Codex | Migration behavior | Caveat |
| --- | --- | --- | --- |
| `hooks` in `~/.claude/settings.json`, `.claude/settings.json`, or `.claude/settings.local.json` | `.codex/hooks.json` + `[features].codex_hooks = true` | Partial conversion | Review behavior before relying on migrated hooks; Claude and Codex hook runtimes are not 1:1. |
| `Notification` | `notify` | Manual rewrite only | `notify` is a turn-complete notification command, not a general lifecycle hook or approval-prompt hook. |
| `PreToolUse` | `PreToolUse` in `.codex/hooks.json` | Partial conversion | Codex currently runs PreToolUse for shell commands only and blocks only `permissionDecision: "deny"`, legacy `decision: "block"`, or exit code `2`. |
| `PostToolUse` | `PostToolUse` in `.codex/hooks.json` | Partial conversion | Codex currently runs PostToolUse for shell commands only; `decision: "block"` becomes model feedback, and `continue: false` stops execution. Formatting or fixups that Claude tied to `Edit`/`Write` should move to a `Stop` hook, because only Bash is matched for `PostToolUse`. |
| `UserPromptSubmit` | `UserPromptSubmit` in `.codex/hooks.json` | Partial conversion | Codex can inject context or block a prompt, but it ignores `matcher` for this event and does not support source `if` filters. |
| `SessionStart` | `SessionStart` in `.codex/hooks.json` | Partial conversion | Codex matches `startup` and `resume`; Claude may also expose other session flows. |
| `Stop` | `Stop` in `.codex/hooks.json` | Partial conversion | Codex ignores `matcher` for Stop, can request a continuation prompt, and does not expose every source subagent/teammate stop lifecycle. |
| `PermissionRequest` / `SubagentStart` / `SubagentStop` / `TaskCreated` / `TaskCompleted` / `StopFailure` / `PreCompact` / `PostCompact` / `SessionEnd` | No direct equivalent | Unsupported | Keep as manual follow-up items; Codex does not expose matching lifecycle coverage today. |
| `type: "command"` | `type: "command"` | Partial conversion | `command`, `timeout` / `timeoutSec`, and `statusMessage` map. Empty commands are skipped by Codex. |
| `type: "prompt"` / `type: "agent"` / `type: "http"` / `async: true` | No direct equivalent | Unsupported | Codex parses `prompt` / `agent` but skips them, and async hooks are skipped. HTTP hooks need a wrapper command. |
| Hook `matcher` + `if` filters | Regex `matcher` only | Partial conversion | Codex keeps regex `matcher` for `PreToolUse`, `PostToolUse`, and `SessionStart` only. Source `if` filters do not map. |
| Hooks in skills, agents, and plugins | No direct equivalent | Unsupported | Codex discovers hooks from config layers, not from skill or subagent manifests. |

## Planning and validation

| Command | Behavior | Caveat |
| --- | --- | --- |
| `--plan` | Prints staged migration output and generated artifact paths without writing files | Still depends on the selected source, target, and component flags. |
| `--doctor` | Prints readiness, risk counts, and manual-review items without writing files | Static guidance only; it does not prove the migrated setup works. |
| `--validate-target` | Validates an already migrated Codex target | Checks TOML parseability, skill frontmatter, custom-agent TOML fields, AGENTS.md size, and MCP command availability. |

## Minimal examples

Source skill metadata becomes prompt guidance:

```md
allowed-tools:
  - Read
  - Bash
```

```md
## MANUAL MIGRATION REQUIRED

Claude `allowed-tools` was preserved as prompt guidance, not a Codex permission boundary.

You're allowed to use these tools:

- Read
- Bash
```

Source subagent metadata becomes TOML plus prompt guidance:

```md
skills:
  - release-notes
tools:
  - Read
disallowedTools:
  - Bash
```

```toml
sandbox_mode = "workspace-write"
developer_instructions = """
## Skills
- $release-notes

## Tools
You're allowed to use these tools:
- Read

Don't use these tools:
- Bash
"""
```

## Sources

- https://docs.claude.com/en/docs/claude-code/claude_code_docs_map
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/mcp
- https://developers.openai.com/codex/plugins/
- https://developers.openai.com/codex/plugins/build/
- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/hooks
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/hooks-guide
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/plugin-marketplaces

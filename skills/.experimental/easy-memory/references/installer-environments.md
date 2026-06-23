# Installer Environment Adapters

This reference defines how automated installers may adapt `easy-memory` to different host environments while keeping the canonical skill package compatible with the upstream `openai/skills` repository.

## Canonical Source Of Truth

The tracked skill package must keep the upstream OpenAI skill structure as its source of truth:

```text
easy-memory/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
├── references/
└── assets/
```

The canonical source tree must not require host-specific directories such as Codex-only or Claude Code-only layout additions in order to be considered valid.

## What Installers May Do

An automated installer may inspect the target environment and generate local adapter artifacts for that environment. Examples include:
- creating host-specific wrapper files that point back to the canonical skill contents,
- translating the canonical system prompt or metadata into a host-specific agent definition,
- wiring command entry points or local registration files required by the host,
- prompting the user to provide local runtime configuration such as API base URL, model ID, API key, and agent enablement flags.
- creating or updating a local project-scoped config file such as `./easy-memory/agent-config.json`.

These installer-generated artifacts must be treated as local derived files, not as canonical source files for the upstream skill package.

## What Installers Must Not Do

Installers must not:
- require the upstream package to commit host-specific adapter directories as part of the canonical source tree,
- store user secrets or machine-specific credentials in tracked repository files,
- rewrite core memory semantics in `scripts/` without the user explicitly choosing a different runtime mode,
- make Codex, Claude Code, or any other environment-specific adapter the only supported execution path.

## Configuration Placement

For future memory-management agent support, use this split:
- Canonical source package:
  - `SKILL.md` for workflow rules,
  - `agents/openai.yaml` for Codex/OpenAI UI metadata,
  - `references/` for API contracts, prompt sources, and response schema documentation,
  - `assets/` for sample request/response fixtures and templates,
  - `scripts/` for deterministic execution logic.
- Local installer or user environment:
- API key,
- local config file path,
- base URL,
- selected model ID,
  - environment-specific enablement toggles,
  - generated host adapter files.

## Host Mapping Guidance

If the installer targets Codex:
- keep `agents/openai.yaml` as the canonical metadata file inside the skill package,
- avoid inventing additional required Codex-only directories beyond the upstream package layout unless the host explicitly requires local generated artifacts.
- prefer a generated local config that uses `api_style: "codex_exec"` instead of adding an HTTP provider by default.
- when generating a default Codex local config, prefer:
  - `model: "gpt-5.3-codex-spark"`
  - `codex_service_tier: "fast"`
  - `codex_reasoning_effort: "medium"`
  - no API key or base URL fields unless the user explicitly selects an external provider.

If the installer targets Claude Code:
- prefer generating local adapter artifacts from the canonical prompt and metadata sources rather than making Claude-specific files the source of truth,
- keep generated Claude-oriented files installer-managed and replaceable.

If the installer targets another host:
- map from the canonical package into that host's local registration mechanism,
- keep the mapping reversible and avoid embedding secrets into the installed skill package.

## Recommended Local Config File

For project-scoped installation flows, prefer a local config file at:
- `./easy-memory/agent-config.json`

The installer may populate this file with non-secret defaults and prompt the user for secret values or defer those to environment variables.

Environment variables should override the local config file so that host-specific launchers can supply temporary or machine-specific values without rewriting project-local state.

## Packaging Rule

If a skill is intended for one-click installation from GitHub or another installer-supported source, the repository copy should remain self-contained and portable without requiring post-clone source edits. Environment-specific supplementation should happen as a local install step, not as a divergence from the upstream-compatible source package.

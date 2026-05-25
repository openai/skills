# documents

Audit, create, and update project documentation. Documentation is code - stale docs are worse than no docs.

## Rules

1. **Never invent technical details** - only document what actually exists in the codebase
2. **ASCII-only characters** and Unix LF line endings
3. **Current over complete** - a smaller, accurate doc beats a comprehensive stale one
4. **One source of truth** - don't duplicate information; link instead
5. **README naming** - only root gets `README.md`; subdirectories use `README_<dirname>.md`
6. **One command runs everything** - document it prominently in root README

## Steps

### 1. Get Project State (REQUIRED FIRST STEP)

Run the analysis script to understand current project progress:

```bash
# Check for local scripts first, fall back to plugin
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

The JSON output includes:
- `current_phase` - Current phase number
- `completed_sessions` - List of completed session IDs
- `monorepo` - true/false/null from state.json
- `packages` - Array of registered packages (empty if not monorepo)
- `active_package` - Resolved package context (null if not applicable)

Also read:
- `.spec_system/state.json` - Project state and phase/session progress
- `.spec_system/PRD/PRD.md` - Product requirements for context

### 2. Determine Audit Scope (Phase-Focused vs Full)

Check if a phase was recently completed:

1. **Identify recently completed phase**: Look at `completed_sessions` in state.json - if all sessions for a phase are complete but the next phase hasn't started, that phase was "just completed"
2. **Collect phase artifacts**: For the completed phase, read all `implementation-notes.md` files from `.spec_system/specs/phaseNN-session*/`
3. **Extract change manifest**: Build a list of files/directories created or modified during that phase

**Phase-Focused Mode** (when a phase was just completed):
- Prioritize documenting changes from the completed phase
- Focus README updates on newly added packages/services
- Update ARCHITECTURE.md with new components added in the phase
- Still verify all standard files exist, but deep-audit only changed areas
- **Monorepo**: Check which packages had sessions in the completed phase. Focus per-package README updates on packages that changed.

**Full Audit Mode** (initial setup, major milestones, or explicit request):
- Audit all documentation comprehensively
- Use when: first run, after multiple phases, or user requests full audit
- **Monorepo**: Verify all packages have README files and that root documentation covers workspace structure

Report the audit mode to the user before proceeding.

### 3. Audit Existing Documentation

Check for the presence and quality of standard documentation files.

> **Naming Convention**: `README.md` is reserved for project root only. All other README files use `README_<directory-name>.md` (e.g., `apps/web/README_web.md`).

#### Root Level (Required)

| File | Purpose | Check |
|------|---------|-------|
| `README.md` | What this is, repo map, one-command quickstart | Exists? Current? |
| `CONTRIBUTING.md` | Branch conventions, PR rules, commit style | Exists? Current? |
| `LICENSE` | Legal clarity | Exists? |

#### /docs/ Directory

```
docs/
|-- ARCHITECTURE.md        # System diagram, service relationships, tech stack
|-- CODEOWNERS             # Who owns what
|-- onboarding.md          # Zero-to-hero checklist
|-- development.md         # Local environment, dev scripts
|-- environments.md        # Dev/staging/prod differences
|-- deployment.md          # CI/CD pipelines, release process
|-- adr/                   # Architecture Decision Records
|   \-- NNNN-title.md
|-- runbooks/              # "If X breaks, do Y"
|   \-- incident-response.md
\-- api/                   # API contracts, OpenAPI links
```

#### Per-Package/Service READMEs

Check for `README_<dirname>.md` in each significant directory. Pattern: `[parent]/[dirname]/README_[dirname].md`

**Monorepo**: Use the `packages` array from state.json as the authoritative list of packages needing READMEs.

### 4. Generate Audit Report

Create a mental checklist of:
- Missing files (need to create)
- Stale files (need to update)
- Redundant content (need to consolidate)
- Wordy sections (need to trim)

Report findings to the user before proceeding.

### 5. Create Missing Documentation

For each missing required file:

1. **Check for local override**: `.spec_system/doc-templates/<filename>`
2. **If exists**: Use local template
3. **Otherwise**: Use default templates below

> **Local templates take precedence** - same pattern as scripts.

#### README.md Template

```markdown
# [PROJECT_NAME]

[One-line description of what this project does]

## Quick Start

```bash
# One command to run everything
[COMMAND]
```

## Repository Structure

```
.
|-- [dir1]/          # [Purpose]
|-- [dir2]/          # [Purpose]
\-- [dir3]/          # [Purpose]
```

## Documentation

- [Getting Started](docs/onboarding.md)
- [Development Guide](docs/development.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md)

## Tech Stack

- [Technology 1] - [Why]

[MONOREPO ONLY]
## Packages

| Package | Path | Description | Stack |
|---------|------|-------------|-------|
| [name] | [path] | [Purpose] | [Stack] |
[END MONOREPO ONLY]

## Project Status

See [PRD](.spec_system/PRD/PRD.md) for current progress and roadmap.
```

#### CONTRIBUTING.md Template

```markdown
# Contributing

## Branch Conventions

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - New features
- `fix/*` - Bug fixes

## Commit Style

Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`

## Pull Request Process

1. Create feature branch from `develop`
2. Make changes with clear commits
3. Write/update tests and documentation
4. Open PR with description
5. Address review feedback, squash and merge
```

#### docs/ARCHITECTURE.md Template

```markdown
# Architecture

## System Overview

[High-level description of the system]

## Dependency Graph

```
[Service A] --> [Service B] --> [Database]
```

## Components

### [Component 1]
- **Purpose**: [What it does]
- **Tech**: [Technology used]
- **Location**: `[path/]`

## Tech Stack Rationale

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| [Tech 1] | [Purpose] | [Rationale] |

## Data Layer

- **Database**: [Type, hosting, extensions]
- **Migration Tool**: [Name, location, naming convention]

## Data Flow

[Describe how data moves through the system]

[MONOREPO ONLY]
## Package Dependencies

| Package | Depends On | Depended By |
|---------|-----------|-------------|
| [name] | [list] | [list] |
[END MONOREPO ONLY]

## Key Decisions

See [Architecture Decision Records](docs/adr/) for detailed decision history.
```

#### docs/onboarding.md Template

```markdown
# Onboarding

## Prerequisites

- [ ] [Tool 1] installed
- [ ] [Tool 2] installed
- [ ] Access to [System/Service]

## Setup Steps

1. Clone: `git clone [repo-url] && cd [project-name]`
2. Install: `[install command]`
3. Configure: `cp .env.example .env` (edit with your values)
4. Start: `[start command]`

## Required Secrets

| Variable | Where to Get | Description |
|----------|--------------|-------------|
| `API_KEY` | [Location] | [Purpose] |

## Verify Setup

- [ ] App runs at `http://localhost:[port]`
- [ ] Tests pass: `[test command]`
```

#### docs/development.md Template

```markdown
# Development Guide

## Required Tools

- [Tool 1] v[version]+
- [Tool 2] v[version]+

## Port Mappings

| Service | Port | URL |
|---------|------|-----|
| [Service 1] | [port] | http://localhost:[port] |

## Dev Scripts

| Command | Purpose |
|---------|---------|
| `[cmd]` | [Description] |

## Database

1. Start: `[start command]`
2. Migrate: `[migration command]`
3. Seed: `[seed command]`
4. Reset: `[reset command]`

## Testing

```bash
[test command]          # Run all tests
[coverage command]      # Run with coverage
```
```

#### docs/environments.md Template

```markdown
# Environments

| Environment | URL | Purpose |
|-------------|-----|---------|
| Development | localhost | Local development |
| Staging | [url] | Pre-production testing |
| Production | [url] | Live system |

## Configuration Differences

| Config | Dev | Staging | Prod |
|--------|-----|---------|------|
| [Setting 1] | [value] | [value] | [value] |

## Required Environment Variables

- `[VAR_1]`: [Description]
```

#### docs/deployment.md Template

```markdown
# Deployment

## Local Dev

```bash
[one-command start]     # Start everything
curl localhost:[port]/health  # Verify
[stop command]          # Stop
```

## CI/CD Pipeline

```
Push --> Build --> Test --> [Staging] --> [Production]
```

## Release Process

1. Merge to `main`
2. CI runs tests and builds artifacts
3. Deploy to staging, run smoke tests
4. Deploy to production, verify health

## Rollback

```bash
[rollback command]
```

**When to rollback**: Health check fails post-deploy, error rate spikes, or critical bug reported.
```

#### docs/adr/0000-template.md (ADR Template)

```markdown
# [Number]. [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD

## Context
What prompted this decision?

## Options Considered
1. [Option A] - [pros/cons]
2. [Option B] - [pros/cons]

## Decision
What we chose and why.

## Consequences
Trade-offs, what this enables, what it prevents.
```

#### docs/runbooks/incident-response.md Template

```markdown
# Incident Response

| Level | Description | Response Time |
|-------|-------------|---------------|
| P0 | Complete outage | Immediate |
| P1 | Major feature broken | < 1 hour |
| P2 | Minor feature broken | < 4 hours |
| P3 | Cosmetic/minor | Next business day |

## Common Incidents

### [Incident Type]
**Symptoms**: [What you'll see]
**Resolution**: [Steps to fix]
```

#### README_[dirname].md Template (Per-Package/Service)

```markdown
# [PACKAGE_NAME]

[One-line description]

## Usage

```bash
[import/install command]
```

## Run Commands

| Command | Purpose |
|---------|---------|
| `[cmd]` | [Description] |

## Key Dependencies

- [Dependency 1] - [Why]
```

### 6. Update Existing Documentation

For each existing documentation file:

1. Read current content
2. Compare against project state from `.spec_system/`
3. Identify discrepancies: features documented but not implemented, features implemented but not documented, outdated instructions, broken links
4. Update to reflect current state
5. Remove redundancy and wordiness

### 7. Sync with Spec System Progress

Cross-reference documentation with completed sessions, current phase objectives, technical stack decisions, and architecture choices made in specs. Ensure README and ARCHITECTURE reflect actual implemented state, not planned future state.

#### Phase-Focused Sync (when applicable)

When in Phase-Focused Mode, use implementation-notes.md files as the primary source:

1. Read all implementation notes for the completed phase
2. Extract structured changes: files created, files modified, dependencies added, APIs changed
3. Prioritize documentation updates based on change type:

| Change Type | Documentation Action |
|-------------|---------------------|
| New package/service | Create README_<name>.md |
| New API endpoints | Update docs/api/ |
| New dependencies | Update tech stack in README, ARCHITECTURE |
| Config changes | Update onboarding.md, environments.md |
| New scripts | Update development.md |

4. Skip deep-audit for unchanged areas - verify file exists, don't rewrite content

### 8. Quality Checks

For all documentation files:

- **Accuracy**: All commands work, all paths exist, all links valid, version numbers current
- **Conciseness**: No redundant sections, no verbose explanations where a command suffices
- **Completeness**: All required files present, all sections filled in (no TODO placeholders left)

### 9. Generate Documentation Report

Create `.spec_system/docs-audit.md` with: audit date, project name, audit mode, a summary table (root files, /docs/ files, ADRs, package READMEs -- each with required/found/status counts), sections for files created, files updated, files verified as current, and any remaining documentation gaps requiring human input.

### 10. Report to User

Show files created/updated, documentation coverage, and gaps requiring human input.

## Output

Report: audit mode used, files created/updated, documentation coverage, gaps requiring human input, and link to `.spec_system/docs-audit.md`. If all documents are satisfactory, recommend phasebuild for the next phase.

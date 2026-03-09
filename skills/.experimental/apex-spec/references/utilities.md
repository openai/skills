# Utility Commands

Standalone helpers that operate **outside the session workflow**.
These can be run at any time -- they do not read or modify session state (`state.json`), specs, or task checklists.

## When to Use

Use utility commands for ad-hoc operations that support your workflow but are not part of the plan-implement-validate cycle. They are safe to run at any point -- mid-session, between sessions, or before initialization.

## Command Reference

| Command | Purpose |
|---------|---------|
| `sculpt-ui` | Guide AI-led creation of distinctive, production-grade frontend interfaces |
| `copush` | Pull, version-bump, commit all changes, and push to origin |
| `dockcleanbuild` | Clean Docker environment and rebuild all images and containers from scratch |
| `dockbuild` | Quick Docker Compose build and start with full output |
| `up2imp` | Audit upstream changes and curate an optimally ordered implementation list |
| `pullndoc` | Git pull an upstream repo and document every imported change |
| `qimpl` | Context-aware autonomous implementation session driven by a work file |
| `qfrontdev` | Autonomous frontend implementation session with designer-level quality standards |
| `qbackenddev` | Autonomous backend/infrastructure development session driven by a work file |

## Adding a New Utility Command

### 1. Create the reference file

Create `references/<name>.md` with this structure (no frontmatter):

```markdown
# <name>

<Purpose paragraph>

## Rules

- <constraints and guardrails>

## Steps

1. <step>
2. <step>
...
```

Keep utility commands focused -- they should do one thing well and require minimal context.

### 2. Document it here

Add a row to the Command Reference table above, then add a section below with:

```markdown
## <name>

**Purpose**: What it does in one sentence.

**Usage**:

<name> [arguments if any]

**Behavior**: What happens when you run it.
```

### 3. Update README.md

Add the command to the Utility Commands table in README.md.

---

## Conventions

- Utility commands **must not** modify `state.json`, session specs, or task checklists
- Utility commands **may** read `.spec_system/` files for context
- Utility commands **may** modify project source files, configs, or non-session spec system files
- Frontmatter must include `category: utility`
- Command names should be short, verb-first when possible (e.g., `check-ascii`, `reset-hooks`)

---

## copush

**Purpose**: Pull latest from origin, increment the project version, commit all non-gitignored changes, and push.

**Usage**:
```
copush
```

**Behavior**: Pulls from origin (never upstream) and halts if the merge is not clean.
Increments the patch version in all project version files (README.md, plugin.json, etc.),
preserving any pre-release tag. Stages and commits ALL non-gitignored changes -- including
work outside the current session -- with no co-author or attribution lines. Pushes to origin
and halts if rejected. Reports every step's outcome.

---

## dockcleanbuild

**Purpose**: Full Docker cleanup and from-scratch rebuild cycle, preserving volumes/data.

**Usage**:
```
dockcleanbuild
```

**Behavior**: Clears Docker build cache and stale images, then stops and removes the
project's containers (preserving volumes). Builds the project source if applicable, then
rebuilds all Docker images with `--no-cache` -- primary Dockerfile first, then any
secondary Dockerfiles (Dockerfile.local, etc.). Brings containers back up and runs a
final cleanup of dangling images. All docker commands use `sudo`. Reports ALL output
including warnings, errors, deprecation notices, and update notices regardless of severity.

---

## dockbuild

**Purpose**: Quick Docker Compose build-and-start with full output reporting.

**Usage**:
```
dockbuild
```

**Behavior**: Runs `sudo docker compose up -d --build 2>&1 | tee dev/stderr` to build
and start containers with full output capture. Verifies container status afterwards.
Reports every warning, error, deprecation notice, update notice, and informational
message found in the output, no matter how minor.

---

## up2imp

**Purpose**: Audit a raw upstream changes list and rewrite it as a curated, optimally ordered implementation list for a hardened fork.

**Usage**:
```
up2imp <changes-file> [upstream-dir]
```

**Behavior**: Reads the specified changes file (raw upstream updates since last comparison)
and the upstream codebase directory (defaults to `.001_ORIGINAL/`). Classifies each change
as include or exclude based on whether it objectively improves the fork (bug fixes,
performance, security, stability, meaningful refactors). Excludes stripped features,
unused components, cosmetic changes, and anything conflicting with the fork's direction.
Rewrites the changes file in place with only actionable items in optimal implementation
order, preserving enough detail for efficient engineering.

---

## qimpl

**Purpose**: Run an autonomous, context-window-disciplined implementation session guided by a work file.

**Usage**:
```
qimpl <work-file>
```

**Behavior**: Reads the work file for session goals and prior context, verifies details
against the actual codebase, then implements methodically with senior-engineer rigor.
Stops after approximately 30 tool executions or when the session feels overloaded to
maintain output quality. Updates the work file on exit with progress, remaining work,
and notes for session continuity. Never assumes or guesses -- looks up uncertain details.

---

## qbackenddev

**Purpose**: Run an autonomous backend, infrastructure, or general engineering session guided by a work file.

**Usage**:
```
qbackenddev <work-file>
```

**Behavior**: Reads the work file for session goals (implement, audit, plan, refactor,
document, convert, or review partner work) covering backend code, infrastructure, DevOps,
CLI commands, APIs, and databases. Analyzes existing codebase patterns before making
changes. Verifies all work file details against actual code. Works autonomously through
all tasks without asking permission. Supports merging multiple draft plans, validating a
partner engineer's audit, and converting between formats. Stops after approximately 30
tool executions or when the session feels overloaded and updates the work file for
session continuity.

---

## qfrontdev

**Purpose**: Run an autonomous frontend development session with senior-engineer rigor and designer-level quality standards, guided by a work file.

**Usage**:
```
qfrontdev <work-file>
```

**Behavior**: Reads the work file for session goals (implement, audit, plan, fix, document,
or refactor) with a designer's eye for quality. Verifies all referenced details against
the actual codebase before writing code. Works autonomously through all tasks in the work
file, applying a quality gate (responsive, accessible, consistent, complete, performant)
to every change. Targets Linear/Vercel/Stripe-level polish as the minimum standard.
Stops after approximately 30 tool executions or when the session feels overloaded and
updates the work file for session continuity.

---

## pullndoc

**Purpose**: Pull an upstream/original repo and generate a comprehensive changelog documenting every imported change.

**Usage**:
```
pullndoc <upstream-dir>
```

**Behavior**: Snapshots the current HEAD of the upstream directory, runs `git pull`, then
analyzes every commit and file diff between the old and new HEAD. Generates a markdown file
at `<upstream-dir>/docs/upstream-pull-<YYYY-MM-DD>.md` with a full summary, commit log,
per-file change descriptions (with intent, not just line counts), and a breaking changes
section. Never omits any changed file. Stops early if already up to date.

---

## sculpt-ui

**Purpose**: Guide AI-led creation of distinctive, production-grade frontend interfaces with high design quality.

**Usage**:
```
sculpt-ui
```

**Behavior**: Walks through a four-phase design process before and during frontend implementation.
Phase 1 builds a Design Brief (emotional targets, aesthetic identity, signature moment).
Phase 2 establishes a micro design system (type scale, color architecture, spacing, depth).
Phase 3 covers implementation craft (layout composition, section transitions, motion choreography, advanced CSS/SVG techniques).
Phase 4 enforces quality standards (60fps performance, WCAG AA accessibility, responsive adaptive design).
Also includes an anti-pattern checklist to avoid generic AI output.
Read-only on the spec system -- never modifies state.json, specs, or task checklists.

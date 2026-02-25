# local_project_memory

`memory_cli.py` provides structured memory in SQLite with two scopes:
- `project` (default): local, per-project memory in `.memory/memory.db`
- `global`: namespaced shared memory (for cross-project or user-global knowledge)

Project context auto-resolves from the nearest `.memory/` directory or Git repo root when using project scope.

## Requirements

- Python 3.10+ (standard library only)

## Quick Start

```bash
python3 skills/local_project_memory/scripts/memory_cli.py init
python3 skills/local_project_memory/scripts/memory_cli.py upsert skills/local_project_memory/examples/example_mu.json
python3 skills/local_project_memory/scripts/memory_cli.py search "workflow"
python3 skills/local_project_memory/scripts/memory_cli.py stats
```

Global (namespaced) example:

```bash
python3 skills/local_project_memory/scripts/memory_cli.py init --scope global --namespace user:git
python3 skills/local_project_memory/scripts/memory_cli.py search "commit style" --scope global --namespace user:git
```

## Project Resolution

Resolution order:

1. `.memory/` in current directory
2. nearest parent `.memory/`
3. Git repository root folder name
4. error: `No project context found. Run 'scripts/memory_cli.py init' in your project root.`

`init` behavior:

- create `.memory/` in current directory
- create DB at `.memory/memory.db` in the project root directory

## Global Scope & Namespaces

Use `--scope global --namespace <name>` to store/retrieve durable knowledge outside a single repo.

Recommended namespaces:

- `project:<repo-or-domain>` for cross-project technical knowledge
- `user:git` for commit conventions/preferences
- `user:workflow` for personal working habits
- `team:<org-or-squad>` for shared team standards

Global database location:

- Default: `~/.local/share/local_project_memory/global/`
- Override with `LOCAL_PROJECT_MEMORY_GLOBAL_DIR=/path/to/dir`

Global scope uses one shared SQLite DB file: `memory.db`.
Namespaces are isolated within that database.

## Commands

```bash
python3 scripts/memory_cli.py init [--scope project|global] [--namespace NAME]
python3 scripts/memory_cli.py search "<query>" [--scope project|global] [--namespace NAME] [--k 8] [--type TYPE] [--tag substring] [--include-deprecated] [--view tiny|compact|full] [--select path1,path2,...]
python3 scripts/memory_cli.py get <mu_id> [--scope project|global] [--namespace NAME] [--view tiny|compact|full] [--select path1,path2,...]
python3 scripts/memory_cli.py upsert [--scope project|global] [--namespace NAME] <file_or_dash>
python3 scripts/memory_cli.py deprecate [--scope project|global] [--namespace NAME] <mu_id> --replaced-by <new_id>
python3 scripts/memory_cli.py vacuum [--scope project|global] [--namespace NAME] [--dry-run]
python3 scripts/memory_cli.py stats [--scope project|global] [--namespace NAME]
```

Notes:

- `--scope` defaults to `project`
- `--namespace` is required when `--scope global`

## Projection

Views:

- `tiny`: `id,type,title,validity.status,updated_at`
- `compact`: tiny + `summary,tags`
- `full`: full MU

`--select` overrides view and always includes `schema` and `schema_version`.

Examples:

```bash
python3 scripts/memory_cli.py get arch-routing-v2 --select id,type,content.decision,validity.status
python3 scripts/memory_cli.py search "routing" --select id,title,summary
```

## Validation Rules

- `id` must be slug-like and contain no spaces
- `type` must be one of: `ARCH_DECISION`, `CONSTRAINTS`, `GLOSSARY`, `INTERFACE_SPEC`, `KNOWN_ISSUE`, `TASK_CONTEXT`, `WORKFLOW`
- `content` must be a JSON object
- reject if `summary + content_json` exceeds 50k chars
- reject obvious secrets (`API_KEY`, `PRIVATE_KEY`, `SECRET_KEY`, `BEARER`, `-----BEGIN`)
- if deprecated, `validity.replaced_by` is required

## Output Rules

- success JSON only to stdout
- errors to stderr
- exit code 0 on success
- object-based success responses (for example `init`, `stats`, `upsert`) include storage metadata (`scope`, `target`, `namespace`, `project`) to make automation explicit

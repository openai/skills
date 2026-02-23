# local_project_memory

`memory_cli.py` provides local, per-project structured memory in SQLite.
Project context auto-resolves from the nearest `.memory/` directory or Git repo root.

## Requirements

- Python 3.10+ (standard library only)

## Quick Start

```bash
python3 skills/local_project_memory/scripts/memory_cli.py init
python3 skills/local_project_memory/scripts/memory_cli.py upsert skills/local_project_memory/examples/example_mu.json
python3 skills/local_project_memory/scripts/memory_cli.py search "workflow"
python3 skills/local_project_memory/scripts/memory_cli.py stats
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

## Commands

```bash
python3 scripts/memory_cli.py init
python3 scripts/memory_cli.py search "<query>" [--k 8] [--type TYPE] [--tag substring] [--include-deprecated] [--view tiny|compact|full] [--select path1,path2,...]
python3 scripts/memory_cli.py get <mu_id> [--view tiny|compact|full] [--select path1,path2,...]
python3 scripts/memory_cli.py upsert <file_or_dash>
python3 scripts/memory_cli.py deprecate <mu_id> --replaced-by <new_id>
python3 scripts/memory_cli.py vacuum [--dry-run]
python3 scripts/memory_cli.py stats
```

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

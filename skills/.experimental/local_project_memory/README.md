# local_project_memory

`memory_cli.py` provides structured memory in SQLite with two scopes:
- `project` (default): local, per-project memory in `.memory/memory.db`
- `global`: namespaced shared memory (for cross-project or user-global knowledge)

Project context auto-resolves from the nearest `.memory/` directory or Git repo root when using project scope.

The CLI also maintains a lightweight similarity graph between memory units. New or updated memories are linked to similar items, `search` can return a query-aware memory neighborhood for each hit, and maintenance commands can help inspect duplicates and merge candidates.

## Requirements

- Python 3.10+ (standard library only)

## Quick Start

```bash
python3 skills/local_project_memory/scripts/memory_cli.py init
python3 skills/local_project_memory/scripts/memory_cli.py upsert skills/local_project_memory/examples/example_mu.json
python3 skills/local_project_memory/scripts/memory_cli.py search "workflow"
python3 skills/local_project_memory/scripts/memory_cli.py related workflow-memory-maintenance
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
python3 scripts/memory_cli.py search "<query>" [--scope project|global] [--namespace NAME] [--k 8] [--type TYPE] [--tag substring] [--include-deprecated] [--view tiny|compact|full] [--select path1,path2,...] [--include-neighborhood|--no-include-neighborhood] [--neighbors-k 3]
python3 scripts/memory_cli.py get <mu_id> [--scope project|global] [--namespace NAME] [--view tiny|compact|full] [--select path1,path2,...]
python3 scripts/memory_cli.py upsert [--scope project|global] [--namespace NAME] <file_or_dash>
python3 scripts/memory_cli.py deprecate [--scope project|global] [--namespace NAME] <mu_id> --replaced-by <new_id>
python3 scripts/memory_cli.py related [--scope project|global] [--namespace NAME] <mu_id> [--k 8] [--link-type TYPE] [--include-deprecated]
python3 scripts/memory_cli.py dedupe [--scope project|global] [--namespace NAME] [--k 8] [--include-deprecated]
python3 scripts/memory_cli.py relink [--scope project|global] [--namespace NAME] <mu_id>
python3 scripts/memory_cli.py relink [--scope project|global] [--namespace NAME] --all
python3 scripts/memory_cli.py merge-suggest [--scope project|global] [--namespace NAME] <mu_id> [--include-deprecated]
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

`--select` overrides the main MU projection and always includes `schema` and `schema_version`.

Neighborhood defaults for `search`:

- `tiny`: no neighborhood by default
- `compact`: includes `neighborhood` by default
- `full`: includes `neighborhood` by default

You can always override this with `--include-neighborhood` or `--no-include-neighborhood`.

Each neighborhood entry is returned in a compact shape and is ordered by coherence to the current search query, using a combination of direct query relevance and stored similarity score.

Examples:

```bash
python3 scripts/memory_cli.py get arch-routing-v2 --select id,type,content.decision,validity.status
python3 scripts/memory_cli.py search "routing" --select id,title,summary
python3 scripts/memory_cli.py search "authentication" --neighbors-k 5
python3 scripts/memory_cli.py search "authentication" --view tiny --include-neighborhood
```

## Similarity Graph

On each `upsert`, the CLI computes candidate neighbors using FTS and stores the strongest relationships in `memory_links`.

Current link types:

- `duplicate_candidate`: very high similarity, likely merge/deprecate candidate
- `similar`: related memory with meaningful overlap

Similarity scoring is deterministic and standard-library-only. It uses a weighted combination of:

- title and summary token overlap
- tag overlap
- retrieval hint overlap
- same-type bonus
- content key overlap

This keeps the feature explainable and cheap to maintain while still being useful for cleanup workflows.

## Relationship Commands

Examples:

```bash
python3 scripts/memory_cli.py related auth-jwt-v2
python3 scripts/memory_cli.py related auth-jwt-v2 --link-type duplicate_candidate
python3 scripts/memory_cli.py dedupe
python3 scripts/memory_cli.py relink auth-jwt-v2
python3 scripts/memory_cli.py relink --all
python3 scripts/memory_cli.py merge-suggest auth-jwt-v2
```

Behavior:

- `related` shows stored links for one memory unit
- `dedupe` lists likely duplicate pairs once
- `relink` recomputes similarity links after edits or bulk changes
- `merge-suggest` recommends a canonical memory unit without mutating data

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
- `search` returns a JSON array of result objects
- `related` and `dedupe` return JSON arrays
- `stats` now includes a `links` section with relationship counts and orphan-memory summaries

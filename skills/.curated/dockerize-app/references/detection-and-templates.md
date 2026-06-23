# Detection And Templates

This reference describes how `scripts/dockerize_app.py` decides what to generate.

## Stack detection order

When multiple signals exist, the script chooses the first stack from this priority:

1. `node`
2. `python`
3. `go`
4. `rust`

Example: If a repo has both `package.json` and `go.mod`, Node wins unless the script is changed.

## Stack signals

- Node:
  - `package.json` is required for Node detection.
  - Package manager detection order:
    - `packageManager` field in `package.json`
    - `pnpm-lock.yaml`
    - `yarn.lock`
    - default `npm`
- Python:
  - `requirements.txt` or `pyproject.toml`
  - install mode:
    - Poetry if `poetry.lock` or `[tool.poetry]`
    - pyproject install if only `pyproject.toml` exists
    - requirements-based otherwise
- Go:
  - `go.mod`
- Rust:
  - `Cargo.toml`

## Framework mapping

- Node:
  - `next` -> `nextjs`, default port `3000`
  - `vite` -> `vite`, default port `5173`
  - `@nestjs/core` or `@nestjs/common` -> `nest`, default port `3000`
  - `express` -> `express`, default port `3000`
- Python:
  - `fastapi` in requirements/pyproject -> `fastapi`, default port `8000`
  - `django` in requirements/pyproject -> `django`, default port `8000`

## Generated files and intent

- `Dockerfile`:
  - Production-leaning default image with stack-specific install/build/start.
- `.dockerignore`:
  - Common exclusions plus stack-specific ignores.
- `docker-compose.yml`:
  - Local-dev oriented, maps `${PORT:-<default>}` and runs the detected dev command.
- `.env.example` (optional flag):
  - Basic starter vars.
- `compose.override.yml` (optional flag):
  - Dev-only volume mounts.

## Safe write behavior

- Existing files are not overwritten unless `--force` is used.
- `--dry-run` previews content without writing.

## Practical workflow

1. Run dry-run first:
   - `python3 scripts/dockerize_app.py --repo . --dry-run --with-env-example --with-compose-override`
2. Review commands/ports.
3. Run again without dry-run.
4. If needed, rerun with `--force` after manual review.

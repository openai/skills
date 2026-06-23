---
name: dockerize-app
description: Inspect a repository and generate Docker artifacts for common app stacks. Use when a user asks to dockerize a project, containerize an app, create Dockerfile/.dockerignore, produce docker-compose.yml for local development, or detect frameworks like Next.js, Vite, FastAPI, Django, Express, Nest, Go, or Rust and scaffold container configs.
---

# Dockerize App

Generate Docker setup files by inspecting repository signals.

## Quick start

1. Run the bundled script from the target repository root:

```bash
python3 "$CODEX_HOME/skills/dockerize-app/scripts/dockerize_app.py" --repo .
```

2. To also create optional files when missing:

```bash
python3 "$CODEX_HOME/skills/dockerize-app/scripts/dockerize_app.py" \
  --repo . \
  --with-env-example \
  --with-compose-override
```

3. Review generated files and adjust ports, commands, and env values for project specifics.

## What the script detects

- Node signals:
  - `package.json`
  - `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`
  - Framework markers in dependencies: `next`, `vite`, `express`, `@nestjs/core`
- Python signals:
  - `requirements.txt`, `pyproject.toml`, `poetry.lock`
  - Framework markers: `fastapi`, `django`
- Go signal:
  - `go.mod`
- Rust signal:
  - `Cargo.toml`

## Generated files

- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml` (local dev oriented)
- `.env.example` (optional, only if missing and `--with-env-example` is set)
- `compose.override.yml` (optional, only if missing and `--with-compose-override` is set)

## Behavior

- Prefer not to overwrite existing files unless `--force` is provided.
- Print detected stack/framework/package manager and written/skipped files.
- Use deterministic templates and conservative defaults.

## References

- For deeper behavior details (stack priority, framework mapping, port defaults, and template output expectations), read:
  - `references/detection-and-templates.md`

## Command reference

```bash
python3 scripts/dockerize_app.py --repo <path> [--force] [--dry-run] [--with-env-example] [--with-compose-override]
```

- `--repo`: target repository path (default `.`)
- `--force`: overwrite existing generated files
- `--dry-run`: print outputs without writing
- `--with-env-example`: create `.env.example` if missing
- `--with-compose-override`: create `compose.override.yml` if missing

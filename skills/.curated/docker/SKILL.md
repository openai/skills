---
name: "docker"
description: "Create or refresh repository Docker assets from real project evidence. Use only when explicitly invoked to inspect the detected stack, then create or update Dockerfile, docker-compose.yml, docs/docker.md, and .dockerignore without inventing unsupported services."
---

# docker

## Objective

Create concrete Docker assets that match the real repository and document the container strategy clearly for later agents.

## Invocation contract

- Run only on explicit invocation of `$docker`.
- Inspect the repository before editing any Docker asset.
- If `docs/` does not exist in the target repository, create it before writing `docs/docker.md`.
- Create or update these files at the repository root: `Dockerfile`, `docker-compose.yml`, `docs/docker.md`, and `.dockerignore`.
- Read any existing Docker assets first and preserve useful content that still matches the detected stack.
- Support frontend and backend together when both exist.
- Include database, cache, worker, reverse proxy, or migrations only when repository evidence shows they are real parts of the stack.
- Do not create fantasy services.

## Required documentation

Create or update `docs/docker.md` with these sections:

- What was detected
- Container strategy
- Build details
- Run details
- Environment variable expectations
- Volumes
- Ports
- Networks
- Dev workflow
- Prod notes
- Known assumptions
- Docker handoff summary

## Implementation rules

- Derive build and run commands from actual project files such as `package.json`, solution files, manifests, lockfiles, framework configs, and existing scripts.
- If the repository already has service-specific Dockerfiles or Compose files, adapt and consolidate them rather than duplicating them blindly.
- If one root `Dockerfile` cannot represent every deployable unit cleanly, make the root `docker-compose.yml` the source of truth and document the role of the root `Dockerfile` explicitly in `docs/docker.md`.
- Keep assumptions minimal, evidence-backed, and listed under `Known assumptions`.
- Use `Unknown` when required runtime details cannot be proven from the repository.

## Suggested scan targets

- App runtimes: `package.json`, `pnpm-workspace.yaml`, `requirements*.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `*.csproj`, `pom.xml`, `build.gradle*`
- Existing container assets: `Dockerfile*`, `docker-compose*.yml`, `.dockerignore`
- Infra and ops: `.env*`, CI workflows, deploy scripts, reverse proxy configs, migration scripts, seed scripts

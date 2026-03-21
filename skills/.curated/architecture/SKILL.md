---
name: "architecture"
description: "Generate or refresh docs/architecture.md from repository evidence. Use only when explicitly invoked to inspect real modules, services, configs, infra, and runtime wiring, then document the architecture without inventing missing details."
---

# architecture

## Objective

Create or update `docs/architecture.md` from the actual repository so another agent can understand the system shape quickly.

## Invocation contract

- Run only on explicit invocation of `$architecture`.
- If `docs/` does not exist in the target repository, create it before writing `docs/architecture.md`.
- Read the existing `docs/architecture.md` before changing it.
- Inspect source code first, then configs and env examples, then docs and operational files.
- Update the existing file in place when it exists and preserve useful content that still matches current evidence.
- Write `Unknown` for missing or ambiguous details instead of guessing.

## Required sections

Create or update `docs/architecture.md` with these sections:

- System overview
- Bounded contexts or modules
- Service catalog
- Responsibilities of each service
- Runtime communication paths
- Authentication and authorization flow
- Data flow
- Storage systems
- Caching systems
- Background jobs or queues if present
- External integrations
- Config and environment structure
- Deployment topology
- Operational concerns
- Known bottlenecks and risks
- Recommended diagrams in Mermaid
- Architecture handoff summary
- Repository evidence

## Documentation rules

- Use repository evidence for every major claim and record that evidence in the `Repository evidence` section.
- When diagram recommendations are supported by the repository, include short Mermaid snippets for the most useful views, such as module context, runtime flow, or deployment topology.
- If a Mermaid diagram would require guesswork, mark the missing edges or nodes as `Unknown` instead of fabricating them.
- Distinguish confirmed behavior from `Inference:` lines.
- Prefer concise tables and bullets over long prose.

## Suggested scan targets

- Modules and services: `src/`, `services/`, `apps/`, `packages/`
- Runtime and auth: entrypoints, middleware, route registration, auth handlers, gateway configs
- Data and storage: ORM models, migrations, schema files, repositories, cache adapters
- Ops and deployment: `Dockerfile*`, `docker-compose*.yml`, `k8s/`, `helm/`, `terraform/`, `.github/workflows/`

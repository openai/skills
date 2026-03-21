---
name: "summarize_context"
description: "Create or refresh durable project memory for a repository. Use only when explicitly invoked to scan real code, configs, env examples, API specs, Docker assets, and infra files, then update .project_memory/master_context.md, .project_memory/current_context.md, and a timestamped history snapshot."
---

# summarize_context

## Objective

Capture durable repository memory and save it into the project memory files used by later chats.

## Invocation contract

- Run only on explicit invocation of `$summarize_context`.
- If `.project_memory/` or `.project_memory/history/` do not exist in the target repository, create them before writing outputs.
- Inspect the repository in this order: source code and entrypoints, configuration and env examples, infrastructure and container assets, then docs and API specs.
- Extract facts only from repository evidence. Never guess.
- If information is missing, write `Unknown` and name the gap and the folder or file area that was checked.
- If output files already exist, update them in place and preserve useful stable content.

## Required outputs

- Update `.project_memory/master_context.md` as the long-lived merged context.
- Update `.project_memory/current_context.md` as the concise working context for the next agent.
- Create or update `.project_memory/history/YYYYMMDD_HHMMSS.md` as the timestamped snapshot for the current run.

## Required sections

Write all three outputs in clean markdown and include these sections:

- Project name
- Product purpose
- Business goals
- Core user flows
- Main modules and services
- Data model summary
- API surface summary
- UI system summary
- Infra and deployment summary
- Docker related findings
- Environment variables and config files
- Build, run, test commands
- External integrations
- Known risks
- Open questions
- Recent decisions if they can be inferred from docs or code comments
- Important file map
- Glossary of project specific terms
- Next agent starting point

## Update policy

- Keep `master_context.md` broader and more stable than `current_context.md`.
- Keep `current_context.md` concise and immediately actionable for the next session.
- Keep history snapshots time-stamped and representative of what was known at that moment.
- Never delete a stable fact unless current repository evidence clearly contradicts it.
- Prefer bullets, short tables, and file references over long prose.
- Mark inferred conclusions with `Inference:` and support them with file evidence.

## Evidence expectations

- Cite the concrete files or folders used to infer major claims.
- Treat lockfiles, generated output, and vendor directories as secondary evidence.
- Prefer primary sources such as application entrypoints, route definitions, schema files, Docker assets, CI workflows, infrastructure code, and env examples.

## Suggested scan targets

- Application code: `src/`, `app/`, `server/`, `client/`, `frontend/`, `backend/`
- Config and environment: `.env*`, `appsettings*.json`, `package.json`, `pyproject.toml`, `requirements*.txt`, `pom.xml`, `build.gradle*`, `Cargo.toml`
- Infra and delivery: `Dockerfile*`, `docker-compose*.yml`, `.github/workflows/`, `infra/`, `terraform/`, `k8s/`, `helm/`
- API evidence: `openapi.*`, `swagger.*`, `postman*`, `controllers/`, `routes/`, `graphql/`, `proto/`
- UI evidence: `components/`, `pages/`, `layouts/`, `styles/`, `tailwind.config.*`, `theme.*`

## Completion standard

- End each generated markdown file with a section named `Next agent starting point`.
- Make the outputs directly useful to another agent that has never seen the repository before.

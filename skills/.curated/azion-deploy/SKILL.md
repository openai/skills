---
name: azion-deploy
description: Deploy applications, static sites, and edge functions to Azion using Azion CLI and Azion Build workflows. Use when the user asks to deploy, publish, host, or configure a project on Azion, including local deploys, CI/CD deploys, framework builds, and project linking/authentication issues.
---

# Azion Deploy

Use this skill to deploy projects to Azion with predictable steps and minimal prompts.

## Prerequisites

1. Confirm `azion` CLI is installed and available.
2. Confirm authentication before deploy.
3. Confirm project is initialized/linked when needed.

Quick checks:

```bash
azion --version
azion whoami
```

If CLI is missing, install using `references/azion-cli.md`.
If auth fails, run `azion login` (interactive) or use `--token` for non-interactive runs.

For token-based runs with `.env`:

```bash
set -a
source .env
set +a
```

## Auth Wizard (Run Before Deploy)

1. Check current auth state:

```bash
azion whoami
```

2. If `whoami` fails, choose one:
- Interactive local auth:

```bash
azion login
azion whoami
```

- Token auth with `.env`:

```bash
set -a
source .env
set +a
azion whoami --token "$AZION_TOKEN"
```

3. Only continue to `link/build/deploy` after `whoami` succeeds.

## Stable Quickstart (Recommended)

Prefer this flow for new projects and first deploys:

```bash
azion link --auto --name <project-name> --preset static --token "$AZION_TOKEN"
azion build --token "$AZION_TOKEN"
azion deploy --local --skip-build --auto --token "$AZION_TOKEN"
```

Why this flow:
- Avoid remote pipeline failures during first tests.
- Ensure `.edge/manifest.json` is generated before deploy.
- Keep deploy non-interactive and reproducible.

## Post-Deploy Verification (Required)

After every deploy, validate both root and health:

```bash
curl -i https://<domain>/
curl -i https://<domain>/health
```

Expected:
- Root returns your app content (or your custom response).
- Health returns your edge-function response when implemented.

If response is Azion fallback page (`404` with "There's nothing here yet"), continue with troubleshooting.

## API Version Awareness (v3 vs v4)

Azion CLI commands in this skill (`edge-application`, `origin`, `rules-engine`, `domain`) are v3-style resources.

If the account is migrated to API v4, a successful v3 deploy can still end in fallback page if Workloads/Connectors are not configured in the v4 model.

When this happens:
- Treat CLI deploy success as partial.
- Validate account migration state in Azion documentation and Console.
- Complete v4-side mapping (Workload/Connector/Domain) before expecting traffic on the map domain.

## Account Model Gate (Do First)

Before running deployment commands, identify account model:

1. Open Azion Console > Products.
2. If menu shows `Workloads`, `Connectors`, or `Custom Pages`, account is migrated to API v4.
3. If not, account is in legacy v3 model.

If account is API v4:
- Do not rely only on legacy `Domains/Origins` automation paths.
- Ensure Workload + Deployment Settings are correctly configured, with Application selected.
- Ensure Workload domain access is enabled (`Workload Domain Allow Access`) when testing with `*.map.azionedge.net`.

## Workflow

Important execution rule:
- Never run `azion link`, `azion build`, and `azion deploy` in parallel.
- Always run them sequentially and wait for each command to finish successfully before starting the next one.

1. Detect current state:
- Is there already an Azion app/project config in this repo?
- Is it linked to the target Azion application?
- Is this an interactive local deploy, local automated deploy, or CI/CD deploy?

2. Prepare project:
- If project is not configured, prefer `azion link --preset static` for minimal setup.
- Use `azion init` only when interactive template selection is desired.
- If existing app should be used, run `azion link`.
- If framework build is needed, run `azion build`.

3. Deploy:
- Local deterministic deploy: `azion deploy --local --skip-build --auto`
- CI/non-interactive deploy: `azion deploy --yes --token "$AZION_TOKEN"`
- Deploy prebuilt assets: `azion deploy --skip-build`

4. Validate result:
- Capture deployment output URL/app info.
- If available, run a quick HTTP check against returned URL.

## Command Patterns

Interactive local flow:

```bash
azion login
azion init
azion build
azion deploy
```

Link existing Azion app then deploy:

```bash
azion login
azion link
azion build
azion deploy
```

CI/CD flow (non-interactive):

```bash
azion deploy --yes --token "$AZION_TOKEN"
```

Deploy from a specific folder:

```bash
azion deploy --folder dist --yes --token "$AZION_TOKEN"
```

## Required Build Artifacts Checks

Before `deploy --local --skip-build`, confirm:

```bash
test -f .edge/manifest.json
test -f .edge/worker.js
```

For `javascript` preset, ensure `handler.js` exists before `azion build`.

## Recommended Defaults

- Prefer `azion link --preset static` + `azion build` + `azion deploy --local --skip-build`.
- Use `--yes` in CI to avoid prompts.
- Use `--skip-build` only when `.edge/manifest.json` already exists.
- Use `--debug` when troubleshooting CLI failures.

## Troubleshooting

- Authentication errors: verify token scope or rerun `azion login`.
- Missing token in `.env`: set `AZION_TOKEN=<value>` and rerun auth checks.
- Build error with missing `handler.js`: create `handler.js` or set the correct build entry.
- Build error from `npx` cache (`~/.npm/_npx/.../package.json`): clear `_npx` cache and rerun build.
- Deploy error `open .edge/worker.js` or `open .edge/manifest.json`: run `azion build` first and verify files.
- Remote deploy failure with `rclone` and API version/auth errors: prefer local deploy path (`--local --skip-build`).
- If deploy output says `.edge/storage` is missing, static files were not uploaded.
- If fallback page persists after successful deploy:
  - Check domain URL with `curl -i`.
  - Check origins for the app. `azion link/deploy` may auto-create `single_origin` pointing to `api.azion.com`.
  - Check rules engine and function instance are active.
  - If account is API v4, verify Workload Deployment settings in Console:
    - Application is selected (mandatory).
    - Domain is attached to workload.
    - Workload domain access is enabled for map domain tests.
  - Retry full local deploy: `azion deploy --local --auto --debug`.
  - If still failing on a clean app, assume v3/v4 model mismatch or platform-side issue:
    - collect `x-azion-request-id` from response headers
    - verify API v4 migration/workload configuration in docs and console
    - open Azion support ticket with app/domain IDs and request IDs.
- Origin/Rules name conflicts on retries: use a unique project name and relink.
- Wrong project/app target: rerun `azion link` and redeploy.
- Non-interactive failures: ensure `--yes` and `--token` are set.

For flags, install commands, and framework behavior, read:
- `references/azion-cli.md`
- `references/azion-build-frameworks.md`

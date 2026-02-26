# Azion CLI Reference

Source documentation:
- https://www.azion.com/pt-br/documentacao/produtos/azion-cli/visao-geral/
- https://www.azion.com/pt-br/documentacao/produtos/azion-cli/comandos/deploy/
- https://www.azion.com/pt-br/documentacao/produtos/guias/verifique-a-migracao-da-sua-conta-para-api-v4/
- https://www.azion.com/en/documentation/products/build/workload/workload-main-settings/
- https://www.azion.com/en/documentation/products/build/workload/deployments/

## Install

macOS / Linux:

```bash
curl -fsSL https://downloads.azion.com/cli/install.sh | sh
```

Windows (PowerShell):

```powershell
irm https://downloads.azion.com/cli/install.ps1 | iex
```

Verify:

```bash
azion --version
```

## Authentication

Interactive:

```bash
azion login
azion whoami
```

Auth wizard:

```bash
azion whoami
```

If it fails:

```bash
azion login
azion whoami
```

Or token-based:

```bash
set -a
source .env
set +a
azion whoami --token "$AZION_TOKEN"
```

Token-based (non-interactive):
- Use global flag `--token` / `-t`
- Example:

```bash
set -a
source .env
set +a
azion deploy --yes --token "$AZION_TOKEN"
```

## Core Commands

Initialize project:

```bash
azion init
```

Link local directory to an existing Azion application:

```bash
azion link
```

Build project:

```bash
azion build
```

Deploy project:

```bash
azion deploy
```

Execution order rule:
- Run `azion link` -> `azion build` -> `azion deploy` sequentially.
- Do not run these commands in parallel; it can cause configuration race conditions.

Recommended stable local flow:

```bash
azion link --auto --name <project-name> --preset static --token "$AZION_TOKEN"
azion build --token "$AZION_TOKEN"
azion deploy --local --skip-build --auto --token "$AZION_TOKEN"
```

Mandatory post-deploy check:

```bash
curl -i https://<domain>/
curl -i https://<domain>/health
```

If domain returns fallback page after deploy success, do not stop at CLI output.
Validate account model/migration and resource mapping in Azion docs/console.

## API v4 Migration Check

Per Azion migration guide:
- If Products menu contains `Workloads`, `Connectors`, or `Custom Pages`, account is in API v4 model.
- In API v4, legacy v3 resources can appear configured while traffic is still unresolved without workload/deployment mapping.

Minimum v4 checks in Console:
- Workload exists and is active.
- Workload Deployment has an Application selected (mandatory per docs).
- Domain is attached to that workload/deployment.
- `Workload Domain Allow Access` enabled for `*.map.azionedge.net` tests.

## Deploy Options

Main options from `azion deploy` docs:
- `--auto`, `-a`: use default values in prompts
- `--yes`, `-y`: answer yes to all prompts
- `--skip-build`, `-s`: skip build step
- `--folder`, `-f`: deploy a specific folder
- `--name`, `-n`: specify project name

Global options frequently used:
- `--token`, `-t`: authenticate with token
- `--config`, `-c`: use custom config path
- `--debug`, `-d`: verbose debug output

## Practical CI Pattern

```bash
azion deploy --yes --skip-build --token "$AZION_TOKEN"
```

Use `--skip-build` only when artifacts are already built.

## Common Failure Patterns

- `open .edge/manifest.json` or `open .edge/worker.js`: run `azion build` first.
- `Missing default entry point .../handler.js`: create `handler.js` for `javascript` preset.
- `~/.npm/_npx/.../package.json` ENOENT during build: clear `~/.npm/_npx` and rerun.
- Remote deploy logs failing with `rclone` auth/API version errors: use local deploy (`--local --skip-build`).
- Deploy says `.edge/storage` is missing: no static files were uploaded.
- Domain returns `404` fallback page "There's nothing here yet" after successful deploy:
  - inspect origins with `azion list origin --application-id <id> --details`
  - verify if auto-created origin points to `api.azion.com`
  - if clean app also reproduces, check API v4 migration state and workload/connector mapping
  - gather `x-azion-request-id` header and escalate to Azion support.

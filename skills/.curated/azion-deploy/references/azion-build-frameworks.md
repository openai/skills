# Azion Build and Frameworks

Source documentation:
- https://www.azion.com/pt-br/documentacao/produtos/build/develop-with-azion/frameworks-specific/visao-geral/
- https://www.azion.com/pt-br/documentacao/produtos/guias/build/criar-uma-aplicacao/

## Purpose

Azion Build enables framework-aware builds for modern frontend/fullstack projects and packages outputs for Azion deploy workflows.

## How to Use in Practice

1. Initialize/link project first (`azion init` or `azion link`).
2. Run build:

```bash
azion build
```

3. Deploy:

```bash
azion deploy
```

Stable automated variant:

```bash
azion link --auto --name <project-name> --preset static --token "$AZION_TOKEN"
azion build --token "$AZION_TOKEN"
azion deploy --local --skip-build --auto --token "$AZION_TOKEN"
```

## Operational Guidance

- Prefer the default framework integration when the framework is recognized.
- For first deploy tests, prefer local deploy mode to reduce remote pipeline failure points.
- If project already has build artifacts (for example in `dist/`), deploy with:

```bash
azion deploy --folder dist --skip-build
```

- If framework behavior differs from expected output, rebuild and inspect logs using `--debug` on deploy.
- For `javascript` preset, ensure `handler.js` exists before build.
- Ensure `.edge/manifest.json` exists before using `--skip-build`.
- Always verify final domain with `curl -i` after deploy; CLI success alone is not enough.
- If domain still returns Azion fallback page on a clean app, treat as platform-side issue and escalate with request IDs.

## Create Application Guide Alignment

When following the "Criar uma aplicação" guide:
- Prefer starting from a minimal preset and validate request routing first.
- Confirm the deployment model used by the account (legacy resources or Workloads/API v4).
- In API v4 environments, finish workload/deployment configuration in Console to make domain traffic resolve correctly.

## Expected Result

A successful flow should produce deployed static assets and configured edge behavior consistent with the project build output.

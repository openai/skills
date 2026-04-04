---
name: "openai-model-upgrader"
description: "Use when a repo, monorepo, demo app, SDK, promptfoo suite, eval harness, or docs site contains OpenAI model references that may be stale and the user wants a careful upgrade to current OpenAI models in one pass. This skill inventories model usage first, checks official OpenAI docs and deprecations before each replacement, analyzes endpoint/modality/cost/latency/test constraints, performs a dependency/reference sweep for docs and guides linked to changed examples, applies only justified model updates unless a stop condition is hit, and then reports what changed plus intentionally unchanged legacy mentions."
---

# OpenAI Model Upgrader

Upgrade OpenAI model references deliberately. Do not do blind search-and-replace.

For each usage site, decide whether to change the model, what to replace it with, and which collateral files must change too.

## Default behavior

Default flow: inventory model usage, build a migration matrix, apply the safe upgrades, validate the patch, then summarize the result.

Do not pause after the matrix unless a stop condition is hit or the user explicitly asks for a plan-only review.

## Workflow

### 1. Inventory model usage first

Before consulting docs or editing files, inspect the repo and build a model inventory.

Search broadly across source, tests, fixtures, eval configs, promptfoo configs, docs, notebooks, examples, package defaults, CI scripts, and env templates.

Start with patterns like:

```bash
rg -n -S 'gpt-|o[134]|whisper-|tts-|text-embedding-|omni-moderation-|dall-e-|computer-use-preview'
```

For each hit, record:

- exact model string
- file path
- code, config, docs, test, fixture, or historical text
- API surface or endpoint
- purpose: text generation, reasoning, transcription, TTS, realtime, embeddings, moderation, image, evals, fine-tuning
- whether this is active runtime behavior or a legacy/historical example

If model selection is indirect, inspect constants, wrappers, provider adapters, env defaults, and generated config.

### 2. Infer repo intent before choosing replacements

Read nearby code and docs and infer why each model is used there.

Look for constraints such as:

- low latency or low cost
- highest quality or strongest reasoning
- realtime voice vs chained speech architecture
- transcription vs text generation vs TTS
- pinned dated models for deterministic tests or benchmark stability
- snapshots, eval thresholds, or promptfoo assertions sensitive to model behavior
- comments documenting compatibility or rollout constraints
- fallback chains and provider abstraction boundaries

Preserve intent. Do not replace a mini/nano or low-latency model with a frontier model unless that tradeoff is clearly intended for that usage site.

### 3. Check current official OpenAI docs before each migration decision

Use official OpenAI docs as the source of truth for model recommendations, endpoint support, and deprecations.

Prefer:

- `mcp__openaiDeveloperDocs__search_openai_docs`
- `mcp__openaiDeveloperDocs__fetch_openai_doc`
- `mcp__openaiDeveloperDocs__get_openapi_spec` when endpoint schema or supported fields matter

For every model family actually used in the repo, answer:

- Is this model current, previous-generation, deprecated, preview-only, or still acceptable?
- What is the recommended modern replacement for this exact workload?
- Is the replacement valid for the same endpoint and modality?
- Does the replacement change request fields, response shape, reasoning settings, prompting guidance, or pricing/latency assumptions?
- Are there release dates, deprecation dates, or migration docs that affect the decision?

Use absolute dates for deprecations and rollout timing.

If docs are ambiguous or unavailable, stop and present options instead of guessing.

### 4. Build a migration matrix, then edit

Create a concise matrix that groups all active model usages by purpose and endpoint:

```text
old model -> proposed model
where used
why this replacement
expected behavior/cost/latency change
required collateral edits
confidence
```

Also list model references you will intentionally leave unchanged, with reasons.

Do not edit until this matrix exists, but once it exists, continue directly to applying the justified updates unless a stop condition applies.

### 5. Run a dependency sweep

Before editing, find collateral files that reference each planned change, especially guides, docs, snippets, and generated outputs tied to updated examples.

For each file, symbol, docs slug, and example path in the migration matrix:

- search for references to the file path, basename, exported symbol names, section titles, and example IDs
- inspect docs pages, guides, README sections, sidebars/nav metadata, and tutorial snippets that link to or quote the changed example
- inspect tests, fixtures, and snapshots that consume the changed example or assert its model output
- inspect generated-doc sources, docs frontmatter, and markdown links if the repo has a docs site
- update model names and surrounding prose so linked guides and examples stay consistent

Use targeted searches such as:

```bash
rg -n -S 'examples/foo|foo.ts|FooExample|old-model-name|docs-slug'
```

If a planned update touches an `examples/` file, search for the example path and example name across `docs/`, `site/`, `guides/`, `README*`, and package docs before finishing the edit pass.

### 6. Apply only justified updates

Update model strings and the surrounding code/config/docs together.

Common collateral to inspect and update:

- model constants and helper wrappers
- docs, READMEs, snippets, screenshots, and UI labels
- env examples and defaults
- promptfoo configs, eval suites, and model matrices
- snapshots, expected outputs, and golden files
- tool-specific defaults in SDK adapters or provider layers
- comments that now describe stale model behavior

Preserve historical references in changelogs, migration notes, archived examples, and tests that intentionally document legacy behavior.

## Replacement rules

### Text and reasoning models

- Upgrade previous-generation models to the latest model that matches the workload and repo intent.
- Preserve model tier where intent is explicit. A cheap fast path should usually stay a cheap fast path.
- Preserve reasoning-vs-general family unless docs clearly recommend switching for that use case.
- Preserve dated-pin style if the repo intentionally uses dated pins for determinism.

### User-facing model pickers and allowlists

- If a file defines a model dropdown, selector, registry, or allowlist that intentionally exposes multiple OpenAI model generations to end users, do not collapse that list to only the newest model.
- Preserve existing selectable models unless a model is explicitly deprecated, unsupported by that endpoint/modality, or clearly broken.
- Prefer appending newer recommended models to broad model catalogs, while updating a singleton default model separately only when repo intent indicates the default should move.
- If a model list mixes OpenAI models with model IDs from other providers, and it is not clear which entries this skill should manage, stop and ask before editing.

### Transcription

- Replace STT models only with transcription models supported by the current endpoint.
- Do not swap a transcription model to a general text model.
- Distinguish plain audio transcription from realtime transcription.

### Text to speech

- Replace TTS models only with models supported by the speech endpoint and the repo's voice architecture.
- Preserve whether the usage optimizes for latency, quality, or voice steerability.

### Realtime speech

- Check realtime model docs and deprecations carefully.
- Do not convert chained STT -> LLM -> TTS apps into realtime apps, or vice versa, unless the user explicitly asks for an architecture migration.
- Preserve WebRTC, WebSocket, and SIP assumptions unless the upgrade requires a documented API migration.

### Embeddings, moderation, image, and fine-tuning

- Upgrade within the correct model family and endpoint constraints only.
- Verify supported request/response fields before changing code.

## Validation

After edits:

- rerun model-reference searches and explain what changed and what was intentionally left alone
- rerun reverse-reference searches for changed example paths, filenames, symbols, and old model names to catch stale docs or guides that still point at updated examples
- verify each replacement is valid for its endpoint
- run the narrowest relevant tests, evals, or promptfoo suites if available
- call out expected prompt drift, output-shape drift, latency/cost changes, and snapshot churn

If validation cannot run, say exactly what remains unchecked.

## Required output

After edits and validation, report in this order:

1. Inventory of active OpenAI model usages grouped by purpose and endpoint
2. Migration matrix with `old -> new`, rationale, and confidence
3. Intentionally unchanged references and why
4. Files changed and collateral touched
5. Validation performed and residual risks

## Stop conditions

Stop and ask before editing if:

- a model reference appears intentionally pinned for a benchmark, fixture, or historical migration doc
- the right replacement is unclear from official docs
- the change would require an architecture migration, not just a model upgrade
- the repo mixes OpenAI and non-OpenAI model IDs, and it is unclear which entries this skill should manage
- tests/evals are likely to shift materially and the user has not asked you to rebaseline them

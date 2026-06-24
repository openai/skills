---
name: repo-skill-miner
description: Crawl, index, analyze, and export reusable skill candidates from source repositories using repo-skills-miner. Use when the user wants to mine a codebase for OpenAI/Codex skills, build a repository skill dataset, find skill-worthy workflows in one or many repos, generate skill cards, compare mined skills against an existing skill catalog, or prepare candidate SKILL.md pull requests.
---

# Repo Skill Miner

Use this skill to turn source repositories into reviewed skill candidates. The goal is not to blindly convert every function into a skill; it is to extract evidence, rank useful workflows, and draft small OpenAI-compatible `SKILL.md` folders for the highest-value capabilities.

## Validated Version Evidence

This guidance was checked against `https://github.com/peytontolbert/repository-skill-miner` at commit `98ef6f8b75dc351f01c7ab71c4651f177c82846d`. The miner's dependency file lists `transformers`, `torch`, and `pyarrow`, but the actual annotation/export behavior depends on model, Parquet, and CLI versions.

Capture the active miner and data stack before comparing results across runs:

```bash
git -C repository-skill-miner rev-parse HEAD
python - <<'PY'
from importlib.metadata import PackageNotFoundError, version
for package in ["transformers", "torch", "pyarrow", "pandas", "typer", "rich"]:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "not installed")
PY
```

## What This Skill Delivers

Use this skill to take a user from "I have repositories" to a ranked set of skill candidates with evidence. A complete run produces:

- A miner checkout or a clear install blocker.
- A database/store containing the ingested target repo revisions.
- Search results or cards showing candidate workflows.
- A ranked table of recommended skills with source evidence, overlap, risk, and PR scope.
- Draft `SKILL.md` folders only for candidates that are broad, safe, and distinct from existing skills.

Do not assume the user knows the miner. If it is not present, introduce it as the repository skill miner project and set it up from source.

## Install or Locate the Miner

If the user provides an existing checkout, use it after recording its remote and commit:

```bash
git -C repository-skill-miner remote -v
git -C repository-skill-miner rev-parse HEAD
```

If no checkout exists, clone the GitHub repository and pin the validated commit before running commands:

```bash
git clone https://github.com/peytontolbert/repository-skill-miner.git
cd repository-skill-miner
git checkout 98ef6f8b75dc351f01c7ab71c4651f177c82846d
```

Install with the package manager the repo provides. If there is no pinned environment, use an isolated virtualenv:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

If installation fails, stop with the failing package and Python version; do not continue with guessed commands.

## Reusable Workflow Value

The miner is useful only when it turns repository evidence into reusable agent procedures. Do not summarize a library. For each candidate, extract:

- The repeated workflow a user wants completed.
- The files, commands, or APIs that prove the workflow exists.
- The version or commit where that workflow was observed.
- The portable instructions an agent can follow in another repo.
- The validation command or artifact proving completion.
- The risks: secrets, license, private infra, huge artifacts, or duplicate OpenAI skills.

Score candidates before drafting:

| score | question |
|---|---|
| 0-3 | How many users/repos would benefit? |
| 0-3 | Is this a repeatable workflow rather than a concept summary? |
| 0-2 | Is there concrete source evidence and validation? |
| 0-2 | Is it safe and license-clean to describe? |

Only draft skills with a total score of 7 or higher unless the user explicitly wants exploratory drafts.

## References

Open `references/workflows.md` for detailed install checks, ingestion manifests, evidence review, candidate scoring, dataset export, OpenAI skill drafting, and review artifacts.

Open `references/mastery.md` when deciding what counts as a skill-worthy workflow, how to avoid dataset-to-PR mistakes, how to audit evidence, and how to turn mined candidates into complete reusable skills.

Open `references/source-evidence.md` when checking whether this skill covers workflows observed in the repository-skill-miner source and mined dataset evidence.

## First Steps

1. Locate or clone `https://github.com/peytontolbert/repository-skill-miner`; do not assume it is installed globally.
2. Confirm the target repositories to mine and whether they are public, private, or sensitive.
3. Create a dedicated output directory for the run, preferably outside the source repo being mined.
4. Do not publish mined outputs until secrets, licenses, and source provenance have been reviewed.
5. Write a run manifest with miner commit, target repo remotes/commits, excludes, annotation model, output directory, and timestamp.

## Safety Rules

- Treat repository crawling as data extraction. It may copy source snippets, docs, config, and generated artifacts into SQLite, CAS blobs, JSONL, or Parquet.
- Before mining private repos, ask whether secrets/config files should be excluded.
- Exclude or redact `.env`, private keys, credentials, local caches, build outputs, dependency directories, and user data.
- Do not include large artifacts, mined datasets, or source snippets in an OpenAI skills PR unless the user explicitly asks and licensing allows it.
- Prefer generated skill instructions and provenance summaries over copied code.

Useful excludes:

```bash
--exclude ".git,node_modules,.venv,venv,env,dist,build,__pycache__,.pytest_cache,.mypy_cache,.env,.secrets"
```

## Mine One Repository

From the miner checkout:

```bash
python -m skill_engine --db skill_engine.db --store skill_engine_store init

python -m skill_engine --db skill_engine.db --store skill_engine_store ingest \
  --repo "$TARGET_REPO" \
  --workers 4 \
  --exclude ".git,node_modules,.venv,venv,env,dist,build,__pycache__,.pytest_cache,.mypy_cache,.env,.secrets"
```

Capture the `revision_id` from the `ingest_repo_ok` JSON log. Most follow-up commands use it.

Expected result: a SQLite DB, a content-addressed store directory, and an `ingest_repo_ok` log line containing the target repo path and `revision_id`. If ingest emits secret-like files, stop and tighten excludes before building cards.

Record the run in a small manifest:

```json
{
  "miner_repo": "https://github.com/peytontolbert/repository-skill-miner",
  "miner_commit": "98ef6f8b75dc351f01c7ab71c4651f177c82846d",
  "target_repo": "<git remote, checkout, or archive source>",
  "target_commit": "<commit sha>",
  "revision_id": "<miner revision id>",
  "excludes": [".git", "node_modules", ".env"],
  "outputs": ["skill_engine.db", "skill_engine_store"]
}
```

## Inspect Mined Skills

Search by capability, framework, file type, or workflow:

```bash
python -m skill_engine --db skill_engine.db --store skill_engine_store agent-search \
  --query "mcp OR fastmcp OR tools OR resources" \
  --topk 20 \
  --include-annotation
```

Fetch evidence for a candidate:

```bash
python -m skill_engine --db skill_engine.db --store skill_engine_store agent-get \
  --skill-id <SKILL_ID> \
  --include-doc \
  --include-snippet \
  --include-annotation
```

Emit skill cards for review:

```bash
python -m skill_engine --db skill_engine.db --store skill_engine_store cards \
  --revision-id <REVISION_ID> \
  --limit 2000 \
  > skill_cards.jsonl
```

Expected result: `skill_cards.jsonl` where each line is a candidate with source path, evidence text, and metadata. If the file is empty, inspect whether the repo was ingested, whether excludes were too broad, and whether the query is too narrow.

## Optional Annotation

Annotation is expensive and may require local model setup. Use it only when deterministic metadata and source evidence are not enough.

```bash
python -m skill_engine --db skill_engine.db --store skill_engine_store annotate \
  --revision-id <REVISION_ID> \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --cache-dir "$MODEL_CACHE" \
  --offline \
  --temperature 0
```

If the model is not already available, do not download large model weights without confirming cost, time, and disk use. Prefer deterministic metadata and search before adding LLM annotation.

## Build a Dataset

For HF-style Parquet datasets, use the repository's dataset builder only after card and annotation locations are known:

```bash
python scripts/build_hf_skills_dataset.py \
  --source "label|$CARDS_PARQUET|$SOURCE_REPO|$ANNOTATION_DIR" \
  --out-dir artifacts/hf_label_skills \
  --max-excerpt-chars 12000
```

Review `dataset_summary.json` before treating the export as canonical.

## Rank Candidates for OpenAI Skills

Prefer candidates that are:

- Broadly useful across many repositories or users.
- Workflow-oriented, not single-function wrappers.
- Safe to describe without copying sensitive implementation details.
- Backed by enough source evidence to write reliable instructions.
- Distinct from skills already present in `openai/skills`.
- Small enough to review as one focused PR.

Before proposing top candidates, compare against the existing skills catalog:

```bash
find "$OPENAI_SKILLS_REPO/skills/.curated" -maxdepth 2 -name SKILL.md -print \
  | sort \
  | sed 's#/SKILL.md$##'
```

Report ranked candidates in a table with `candidate`, `source repo(s)`, `evidence path or skill id`, `existing-skill overlap`, `risk`, and `recommended PR scope`.

Minimum ranking output:

| candidate | source repo(s) | evidence | overlap | risk | PR scope |
|---|---|---|---|---|---|
| short skill name | repo and revision | skill id/path/card line | existing skill names or none | secrets/license/version concerns | one focused skill folder |

Each recommendation must explain reusable workflow value in one sentence:

```text
This is worth a skill because it lets an agent repeatedly <do workflow> across <repo/user class>, with validation via <command/artifact>.
```

Avoid candidates that are:

- Repo-specific maintenance procedures.
- Thin wrappers around a private CLI or local-only service.
- Mostly copied code or huge reference dumps.
- Dependent on secrets, private infrastructure, or unreviewed user data.
- Already covered by an existing OpenAI skill.

## Draft OpenAI Skill PRs

For each selected candidate:

1. Create one branch per skill.
2. Add `skills/.curated/<skill-name>/SKILL.md`.
3. Add `skills/.curated/<skill-name>/LICENSE.txt`.
4. Add `skills/.curated/<skill-name>/agents/openai.yaml` when appropriate.
5. Keep the skill concise; move large details into references only if they are necessary.
6. Validate with the local skill validator if available.
7. For review-first workflows, keep branches local until the user approves pushing.

The draft must stand alone for someone who has never seen the mined repo. Include install or prerequisite checks, version capture, a happy-path command loop, failure modes, and done criteria. Do not ship only a topic overview.

## Review Checklist

- The source repos and dataset paths are recorded.
- License and provenance are acceptable.
- Secret-bearing files were excluded or redacted.
- The candidate is not a duplicate of an existing skill.
- The ranking explains why this skill provides reusable workflow value beyond a library summary.
- The `description` frontmatter clearly states when the skill should trigger.
- The body describes an actionable workflow with validation and failure modes.
- The PR contains one logical skill, not a dataset dump.

# Source Evidence

Use this file as the evidence anchor for the workflow coverage in this skill. This skill must make repository-skill-miner useful to a user who has never seen the project before.

## Retrieved Sources

- `https://github.com/peytontolbert/repository-skill-miner` at commit `98ef6f8b75dc351f01c7ab71c4651f177c82846d`.
- Source modules for ingestion, storage, skill cards, semantic search, evidence scheduling, pattern distillation, server routes, and Parquet/card export.
- Mined datasets containing source repository, source revision, source path, excerpt, annotations, and workflow-card style records.

## Workflows Reflected In The Skill

### Reproducible Mining Run

The source stores repository revisions and source metadata, so the skill requires a run manifest with:

- miner repository URL and commit;
- target repository remote and commit;
- excludes and permission assumptions;
- annotation model and confidence threshold;
- output dataset location;
- timestamp and validation commands.

The skill must never depend on a user-specific local checkout path.

### Evidence And Card Review

The source exposes revision-scoped skills, cards, evidence runs, signals, repository fingerprints, and pattern cards. The skill therefore teaches agents to inspect candidate skills against evidence:

- source repo/revision/path;
- excerpt and symbol context;
- side effects and permissions;
- verification artifacts where available;
- transferability beyond one repository.

### Search And Retrieval

The source includes semantic search and server routes for searching skills/cards/signals. The skill requires agents to search candidates, cluster them by workflow value, and retrieve supporting evidence before drafting a skill.

### Dataset Export

Tests and CLI paths cover writing card outputs, including Parquet. The skill requires schema inspection and sample-row review before using exported datasets for PRs.

### OpenAI Skill Drafting

The mined output is not itself an OpenAI skill. The skill therefore requires a transformation step: select a real reusable workflow, write complete instructions, add validation and done criteria, and cite evidence by repository/commit rather than local paths.

## Review Standard

Reject repo-skill-miner outputs that are only lists of libraries or symbols. A useful workflow must produce a reproducible manifest, evidence-backed candidates, a transferability argument, and complete OpenAI skill content that a fresh agent can run without knowing the miner author's local environment.

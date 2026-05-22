# Repository Skill Miner Workflows

Use this reference to run repeatable repository-mining projects and produce skill candidates with evidence.

## Contents

- [Source Setup](#source-setup)
- [Run Manifest](#run-manifest)
- [Ingestion Workflow](#ingestion-workflow)
- [Evidence Review](#evidence-review)
- [Candidate Scoring](#candidate-scoring)
- [Dataset Export Review](#dataset-export-review)
- [Skill Drafting](#skill-drafting)
- [Review Artifact](#review-artifact)

## Source Setup

Use the GitHub source:

```bash
git clone https://github.com/peytontolbert/repository-skill-miner.git
cd repository-skill-miner
git checkout 98ef6f8b75dc351f01c7ab71c4651f177c82846d
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Record the actual commit even if the user chooses a newer revision.

## Run Manifest

Create a manifest before mining:

```json
{
  "miner_repo": "https://github.com/peytontolbert/repository-skill-miner",
  "miner_commit": "98ef6f8b75dc351f01c7ab71c4651f177c82846d",
  "targets": [
    {
      "repo": "<remote or source>",
      "commit": "<sha>",
      "sensitivity": "public|private|sensitive"
    }
  ],
  "excludes": [".git", "node_modules", ".env"],
  "annotation": {
    "enabled": false,
    "model": null
  },
  "outputs": {}
}
```

## Ingestion Workflow

1. Initialize DB/store.
2. Ingest with excludes.
3. Capture `revision_id`.
4. Spot-check stored docs/snippets for secrets.
5. Only then build cards or annotations.

Expected outputs:

```text
skill_engine.db
skill_engine_store/
ingest log with revision_id
manifest updated with revision_id
```

## Evidence Review

For each candidate, collect:

- source repo and commit
- file paths or skill IDs
- doc evidence
- code snippet evidence
- observed commands or APIs
- version constraints
- safety/license concerns

Reject candidates that require private credentials, copied source code, or undocumented local infrastructure.

## Candidate Scoring

Score 0-10:

```text
breadth:
workflow specificity:
source evidence:
validation path:
safety/license:
overlap with existing skills:
```

Recommended threshold: 7+ for PR drafts.

## Dataset Export Review

Before treating a dataset as canonical:

- Open `dataset_summary.json`.
- Check row counts.
- Check missing annotations.
- Check source labels and paths.
- Sample records from the Parquet file.
- Verify excerpts do not contain secrets or huge copied code.

## Skill Drafting

A mined candidate becomes a real skill only after adding:

- trigger-specific frontmatter description
- setup/prerequisite checks
- version evidence
- happy-path workflow
- troubleshooting
- validation artifacts
- done criteria
- references for deeper workflows when needed

Do not submit topic summaries.

## Review Artifact

Final mining report should include:

```text
miner repo/commit:
target repos/commits:
outputs:
top candidates:
rejected candidates:
existing-skill overlap:
license/safety notes:
recommended PR branches:
```

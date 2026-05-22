# Repository Skill Miner Mastery Notes

This reference explains how to use repository mining to produce useful skills, not just data.

## Contents

- [What Counts as Skill-Worthy](#what-counts-as-skill-worthy)
- [Evidence Quality](#evidence-quality)
- [Mining Strategy](#mining-strategy)
- [Candidate Clustering](#candidate-clustering)
- [Existing Skill Overlap](#existing-skill-overlap)
- [Skill Drafting Standard](#skill-drafting-standard)
- [Safety and Licensing](#safety-and-licensing)
- [Review Report Template](#review-report-template)
- [Common Mistakes](#common-mistakes)

## What Counts as Skill-Worthy

A mined candidate is worth turning into a skill when it helps an agent repeatedly complete a workflow that appears across projects or users.

Good candidates:

- have a clear user goal
- require procedural domain knowledge
- have source evidence from real repositories
- can be validated with commands or artifacts
- are safe to describe without copying proprietary implementation
- are distinct from existing skills

Weak candidates:

- describe a library at a high level
- wrap one function
- only apply to one private repo
- require hidden credentials or infrastructure
- depend on copying large code snippets
- duplicate an accepted OpenAI skill

## Evidence Quality

Rank evidence by strength:

1. working scripts, tests, CLIs, or configs
2. docs that match working code
3. repeated patterns across repos
4. comments or README notes
5. inferred behavior from isolated snippets

Do not draft a skill from weak evidence unless the user explicitly asks for exploratory work.

## Mining Strategy

For one repo:

1. Ingest with safe excludes.
2. Search broad framework/workflow terms.
3. Fetch candidate evidence.
4. Cluster related candidates manually.
5. Score candidates.
6. Draft only the top workflows.

For many repos:

1. Normalize target repo names and commits.
2. Build per-repo cards.
3. Group by workflow class.
4. Rank by breadth and validation strength.
5. Check against existing skills.
6. Draft one PR per skill.

## Candidate Clustering

Merge candidates when they serve one workflow:

- setup + validation + troubleshooting for one tool
- file format authoring + validation for one output class
- model training + export for one framework

Split candidates when they require different users, tools, or success criteria.

## Existing Skill Overlap

Before drafting, compare:

- frontmatter descriptions
- skill titles
- reference topics
- scripts/assets
- accepted workflows

If overlap exists, propose an update to the existing skill instead of a new skill unless the new workflow is clearly distinct.

## Skill Drafting Standard

Every drafted skill should answer:

```text
When should this trigger?
What concrete outcome should the agent produce?
What must be checked before work starts?
What is the happy path?
What are the main branches/variants?
How is success validated?
What can go wrong?
What version or source evidence supports it?
What deeper references should be loaded only when needed?
```

## Safety and Licensing

Repository mining may copy data into intermediate artifacts. Always treat outputs as sensitive until reviewed.

Reject or redact:

- secrets
- API keys
- private URLs
- credentials
- personal data
- large copied code blocks
- license-incompatible content

Prefer paraphrased workflows and provenance summaries over copied implementation.

## Review Report Template

```text
miner source:
miner commit:
target repos:
target commits:
dataset outputs:
candidate count:
top 10 candidates:
accepted candidates:
rejected candidates:
existing skill overlap:
license/safety notes:
recommended PRs:
```

## Common Mistakes

- Treating frequency as value. A common pattern is not automatically a good skill.
- Drafting a skill before checking existing accepted skills.
- Copying too much source evidence into the PR.
- Ignoring versions and commits.
- Writing a library summary instead of a workflow.
- Skipping validation commands.
- Combining unrelated workflows into one broad skill.

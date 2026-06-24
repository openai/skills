---
name: meta-skill
description: Design, create, audit, and refine Agent Skills with careful evaluation, competitive research, a concise design brief, and a distinctive skill identity. Use when an agent needs to make a new skill folder, update an existing skill, write SKILL.md instructions, decide what scripts/references/assets belong in a skill, validate skill metadata, compare similar skills or tools, improve a skill using meta-skill principles, or turn a repeated workflow into a reusable agent capability with a clear point of view.
---

# Meta Skill

Use this skill to turn a repeated workflow, domain practice, or tool integration into a compact Agent Skill that another agent can use without extra explanation. Treat each skill as a small product: evaluate whether it deserves to exist, study what already solves the problem, write a crisp design brief, then give it a distinct working style and purpose.

## Workflow

1. Evaluate whether a skill is warranted. Prefer creating a skill only when it captures reusable judgment, a repeated workflow, fragile tool knowledge, domain-specific context, or assets/scripts that reduce future work. If the request is better served by a one-off answer, prompt, script, or ordinary documentation, say so and offer the smallest useful alternative.
2. Clarify the target behavior with concrete prompts the skill should handle. Ask only for missing details that change the skill's scope, destination, or safety profile.
3. Research nearby solutions before naming or writing. Inspect existing local skills, related plugins, repository conventions, and public or user-provided competitors when available. Identify what they do well, what they omit, and how this skill should differ instead of duplicating them.
4. Write a short design brief using `references/design-brief.md`. Keep it internal unless the user asks to see it, but let it drive the implementation.
5. Define the skill's soul: one sentence naming its unique promise, judgment style, and user experience. Use this as a design constraint for scope, examples, tone, resources, and validation.
6. Choose a lowercase hyphenated skill name under 64 characters. Name the folder exactly after the skill name.
7. Decide the smallest useful file set:
   - `SKILL.md` for trigger metadata and essential workflow instructions.
   - `references/` for longer docs that should be loaded only when relevant.
   - `scripts/` for deterministic or repeated operations that should not be rewritten each time.
   - `assets/` for templates, fonts, icons, examples, or other files used in final outputs.
8. Initialize or create the folder using the best helper available in the current agent environment. If no initializer exists, create the folder manually with a required `SKILL.md` and only the resource directories the skill truly needs. Pass UI metadata such as display name, short description, and default prompt only when the host agent or marketplace supports it.

9. Replace all placeholders. Keep frontmatter to only `name` and `description`; put all trigger conditions in `description`, because the body loads only after the skill triggers.
10. Write the body as instructions for another agent instance. Use imperative language, compact examples, and explicit references to bundled files only when those files should be read.
11. Validate the folder before delivery using the relevant platform validator, schema checker, or install test. If no validator exists, inspect frontmatter, resource paths, trigger boundaries, and example prompts manually.

12. For complex skills, forward-test with realistic prompts and revise based on what the skill failed to make obvious.

## Evaluation Principles

- Be conservative about creating new skills. A skill should remove future ambiguity, encode hard-won context, or make a repeated workflow safer and faster.
- Avoid thin wrappers around common reasoning. If a general instruction is enough, improve the prompt or documentation instead of creating a skill.
- Separate evaluation from implementation. Decide the user's job, risks, alternatives, and success criteria before editing files.
- Name risks early: stale external docs, hidden credentials, destructive actions, expensive calls, privacy boundaries, or workflows that require human approval.
- Prefer narrow excellence over broad vagueness. A memorable small skill is more useful than a generic one that triggers everywhere.

## Competitive Research

- Search available local skills and plugins first. Compare names, descriptions, resource structure, and trigger boundaries.
- When external research is appropriate and available, inspect comparable tools, repos, docs, marketplace entries, or examples before finalizing scope.
- Treat the host platform's skill creation guide or validator as the baseline for mechanics. This skill should add product judgment, differentiation, and design coherence on top of that baseline.
- Capture only the useful delta in the skill itself: what this skill does differently, what it intentionally avoids, and what neighboring skill should be used instead.
- Do not clone a competitor's structure blindly. Borrow proven patterns, then adapt them to the user's actual workflow and the host agent's progressive disclosure model.

## Design Brief

Before creating or substantially updating a skill, sketch the brief from `references/design-brief.md`. Use it to make tradeoffs explicit: whether to build, what to research, what to exclude, and how to know the skill improved.

If updating this skill itself, apply the same brief recursively: compare it to the closest skill-creation baseline, identify the missing meta-level behavior, then revise only the parts that make future skill creation more discerning, researched, or distinctive.

## Distinctive Soul

Before implementation, write an internal one-sentence identity for the skill:

```text
This skill helps <user> accomplish <job> by being <distinctive judgment/style>, unlike <nearby alternative> which <limitation or different focus>.
```

Use the identity to decide what belongs in the skill and what should be excluded. The finished skill does not need to include the sentence verbatim, but its description, workflow, resources, and examples should make the identity legible.

## Delivery Standard

- Explain what changed and why it improves the skill's judgment, usability, or distinctiveness.
- Mention the closest alternative or competitor considered and how the final skill differs.
- Keep the final skill usable without reading the design brief, while keeping the brief available for audits and major revisions.

## Authoring Rules

- Keep `SKILL.md` concise. Move optional detail into one-level reference files and name when to open them.
- Let the skill's unique promise shape every section; remove content that could belong unchanged in any other skill.
- Prefer resources only when they reduce future work or prevent fragile recreation.
- Avoid extra documentation such as `README.md`, install guides, changelogs, or process notes unless the user explicitly asks.
- Use existing local conventions from nearby skills when updating an existing skill.
- Test every added script by running it at least once, or clearly state why it was not run.
- Preserve user edits in existing skill folders; patch around them rather than replacing whole files blindly.

## Quality Review

Before finishing, read `references/quality-checklist.md` and apply the checklist. Fix any failure that would stop the skill from triggering, loading, validating, or being useful to a future agent.

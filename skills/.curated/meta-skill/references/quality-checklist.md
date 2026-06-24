# Skill Quality Checklist

Use this checklist before delivering a created or updated skill.

## Strategic Fit

- The skill is justified by reusable judgment, fragile workflow knowledge, domain context, scripts, references, or assets.
- A simpler one-off answer, prompt, README, or local script would not serve the user better.
- A concise design brief exists mentally or explicitly for substantial work, covering the build decision, alternatives, soul, scope, and validation.
- Important risks are named and handled: stale docs, credentials, destructive actions, privacy, cost, permissions, or required human approval.
- The skill has a narrow enough scope to be excellent instead of generically helpful.

## Competitive Research

- Existing local skills and relevant plugins have been checked for overlap.
- Comparable external tools, docs, repos, marketplace entries, or user-provided references have been reviewed when available and useful.
- The new or updated skill has a clear delta from nearby alternatives.
- The skill says when to use a neighboring skill or tool instead, if that boundary matters.

## Distinctive Soul

- The skill has a one-sentence identity: who it helps, what job it performs, and what judgment or style makes it different.
- The frontmatter description, workflow, examples, and resources all reinforce that identity.
- The skill's closest baseline or competitor is clear enough that the difference is not hand-wavy.
- Generic advice that could appear unchanged in any other skill has been removed or made specific.
- The skill feels like a purposeful capability, not a template with a new name.

## Trigger Metadata

- `SKILL.md` frontmatter contains only `name` and `description`.
- `name` matches the folder name and uses lowercase letters, digits, and hyphens only.
- `description` says what the skill does and exactly when to use it.
- Trigger conditions are not hidden only in the body.

## Body

- The first paragraph explains what the skill enables.
- Instructions are actionable and written for another agent instance.
- The workflow is shorter than the task it replaces.
- Examples are concrete, minimal, and directly reusable.
- Long optional detail lives in `references/`, not inline.

## Resources

- Each resource directory has a clear purpose.
- Scripts are executable, deterministic, and tested.
- Reference files are linked directly from `SKILL.md` with guidance on when to read them.
- Assets are files to copy or use, not documents the model must read.
- Placeholder example files have been removed.

## Validation

- Run the relevant platform validator, schema checker, or install test against the final skill folder.
- Inspect platform-specific UI metadata if present; any `default_prompt` should mention `$skill-name` literally.
- Check for leftover TODO markers or template prose.
- The final response can say why the skill is better after the update.
- If the skill changes a risky or complex workflow, forward-test it with a realistic user request.

# Ivan Human UI

Human-polish skill for Codex that helps teams remove "AI-looking" UI output and ship clearer, intentional product pages.

## What This Skill Solves

- Removes common template-like AI artifacts in web/slides UI.
- Enforces concrete visual constraints (not vague advice).
- Adds a repeatable evaluation loop with scoring and evidence.
- Includes deterministic checks for testimonial/media visibility issues.

## Best For

- Landing pages
- Dashboard marketing pages
- Presentation-like web sections
- "Two images not showing" style UI bug + polish tasks

## Quick Start

1. Trigger the skill in Codex.
2. Run one prompt from `references/eval-prompts.md`.
3. Follow `references/minimal-eval-workflow.md`.
4. Score with `references/eval-rubric.md`.
5. Append the result in `references/eval-results.md`.

### Install In Codex

Use the GitHub folder URL directly with `$skill-installer`:

`$skill-installer install https://github.com/openai/skills/tree/main/skills/.experimental/ivan-human-ui`

## Included Resources

- `SKILL.md`: Core workflow and guardrails.
- `references/human-ui-constraints.md`: Hard design constraints.
- `references/style-directions.md`: Show-don't-tell direction exploration.
- `references/image-visibility-checks.md`: Track/file visibility checklist.
- `references/eval-prompts.md`: Regression prompts.
- `references/eval-rubric.md`: Scoring rubric and ship bar.
- `references/evals/`: Real evaluation reports.
- `scripts/verify_testimonial_tracks.mjs`: Deterministic track verification.

## Contributor Notes

- Keep guidance concrete (class/token/value level).
- Avoid adding fuzzy style language.
- For each new capability, include:
  - at least one eval prompt
  - a scoring expectation
  - an evidence artifact under `references/evals/`

## 中文说明

这个 skill 用于“去 AI 味”UI 打磨，强调可执行约束和可复现评测。

- 适用场景：落地页、Dashboard 营销页、演示风格页面。
- 交付要求：必须输出具体改动（类名/变量/数值），不能只给抽象建议。
- 评测闭环：按 `minimal-eval-workflow.md` 执行，评分写入 `eval-results.md`。

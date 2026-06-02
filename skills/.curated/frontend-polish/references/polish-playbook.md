# Frontend Polish Playbook

Use this file only when the task needs a deeper rubric than the main skill.

## Positioning

This skill aims for high-end, human-feeling product UI. It is not trying to maximize novelty, visual spectacle, or formal accessibility compliance checklists. The priority order is:

1. clarity
2. hierarchy
3. density and rhythm
4. state quality
5. visual expression
6. implementation cleanliness

If two choices conflict, prefer the one that makes the interface clearer and more believable in a real product.

## Anti-AI smell checklist

Common signs that a page feels machine-generated:

- every section uses the same card, radius, shadow, and gap values
- oversized hero copy without a clear content hierarchy underneath
- gradients used as decoration instead of emphasis
- decorative icons and blobs with no product meaning
- weak hover/focus/pressed states
- desktop-first composition that collapses awkwardly on mobile
- a premium visual tone with cheap table/form/detail states
- one-off spacing fixes instead of a consistent density model
- visual drama used to cover unclear product priority

## Practical polish sequence

Apply these in order:

1. Remove visual noise.
2. Tighten hierarchy and grouping.
3. Rebalance spacing and density.
4. Refine typography.
5. Normalize surfaces, borders, and shadows.
6. Improve states and feedback.
7. Fix responsive stress points.
8. Clean up accessibility and obvious performance issues.

## Rules that should stay flexible

Do not freeze these into universal laws:

- exact type scales such as `1.2`, `1.333`, or `1.414`
- exact line-height ranges for every screen
- exact breakpoint sets such as `375 / 768 / 1200`
- strict "three colors total" wording
- blanket bans on shadows, gradients, blur, or asymmetry

Use them as defaults only when they improve the current interface.

## Color guidance

- Think in color families, not isolated swatches.
- A typical polished product UI uses `1` dominant accent family and `0-2` supporting families.
- Neutral ramps are part of the structure and can be rich without making the UI feel colorful.
- Status colors can expand beyond the core palette in dashboards, tables, and forms, but should not overpower the product accent.
- If a page feels expensive but unclear, reduce color variety before reducing contrast.

## Typography guidance

- Chinese interfaces usually benefit from fewer text sizes than visually expressive English landing pages.
- Many weak UIs have too many medium-emphasis text styles. Reduce ambiguity first.
- Tight headlines and calmer body copy usually feel more deliberate than styling every block aggressively.
- Use spacing and line breaks to control rhythm before adding more weight or color.

## Density guidance

- High-end does not mean large and airy by default.
- Dense interfaces can still feel premium when row rhythm, alignment, grouping, and emphasis are disciplined.
- Leave more breathing room around decisions and transitions than around raw data.

## Page-type guidance

### Marketing or landing pages

- Start from message clarity, not effects.
- Give one or two visual focal points, not five.
- Avoid generic startup gradients and testimonial-card grids unless the product truly needs them.

### Auth pages

- Keep the form area calm and obvious.
- Put most expression into composition, typography, and supporting art direction, not input styling tricks.
- Make error, disabled, and loading states feel intentional.
- Trust beats novelty. If the page is beautiful but the form feels uncertain, it is failing.

### Dashboards and internal tools

- Respect information density. Do not turn operational UI into a marketing page.
- Improve grouping, row rhythm, column emphasis, and filter clarity first.
- Use color mostly for status, risk, and focal actions.
- Tables, filters, and panels should feel like part of one system rather than isolated decorated widgets.

### Ecommerce or product detail pages

- Prioritize media hierarchy, price/action clarity, and option selection feedback.
- Use spacing and typography to separate specification detail from persuasion content.

### Component-level polish

- Buttons should communicate priority before style.
- Forms should feel calm and predictable before feeling branded.
- Cards should earn their borders, shadows, and radii instead of using them by default.
- Modals should clarify interruption level through spacing, scale, and backdrop strength.

## Code review rubric

Before finishing, check:

- Is the strongest action visually obvious?
- Does the page still look coherent with styles disabled down to structure and semantics?
- Are hover, focus, active, disabled, empty, loading, and error states covered where relevant?
- Does the mobile layout feel intentionally composed rather than merely stacked?
- Did the polish reduce complexity or just add decoration?
- Would a human reviewer believe the code was maintained by a real team?
- Is the codebase easier to evolve after the polish, not harder?

## Cross-platform note

If this skill is reused outside Codex:

- keep the workflow and red lines unchanged
- replace tool-specific deployment instructions with local repo or framework commands
- keep the output focused on direct implementation, not persona roleplay

---
name: "frontend-polish"
description: "Use when the task is to refine or redesign frontend UI, beautify pages or components, improve responsive behavior, polish motion, or reduce templated AI-generated styling while preserving product intent and business logic. Useful for React, Vue, Tailwind CSS, and HTML/CSS work, including UI polish, visual cleanup, responsive fixes, interaction refinement, and frontend code cleanup."
---

# Frontend Polish

Use this skill when the user wants a frontend to feel intentional, hand-crafted, and production-grade instead of obviously AI-generated. Keep product intent, business logic, and information architecture intact while improving the visual system and implementation quality together.

## Role definition

Operate like a senior frontend engineer and UI design engineer with 8+ years of top-tier product experience. The target taste is:

- Apple-like restraint in surfaces and emphasis
- Stripe-like clarity in layout and typographic rhythm
- Linear-like product density, order, and interaction polish
- large-scale engineering discipline in implementation quality

Do not roleplay for style alone. Apply this taste as working judgment: solve hierarchy, density, spacing, states, and responsiveness before adding visual expression.

## When to use

- Existing page or component needs UI polish without rewriting the product logic.
- A generated page looks generic, over-styled, or obviously AI-made.
- Responsive behavior, spacing rhythm, typography, states, or interaction quality need refinement.
- A new page should be designed and implemented with a hand-crafted feel rather than default SaaS patterns.
- The user wants React/Vue/Tailwind/HTML output that is production-friendly and maintainable.

## Do not use this skill as

- A license to add random effects, premium-looking clutter, or trend-chasing visuals.
- A reason to replace a stable design system with unrelated styling.
- A branding exercise when the user really needs product strategy, copywriting, or illustration.

## Required working style

1. Inspect before editing.
   - Identify framework, styling stack, existing tokens, layout primitives, and reusable components.
   - Preserve established patterns when working inside an existing product or design system.
2. Define a narrow visual direction.
   - Choose a restrained palette, typography approach, spacing rhythm, component density, and motion style.
   - Explain the intended feel in one sentence before making substantial UI edits.
3. Improve structure before decoration.
   - Fix layout hierarchy, grouping, spacing, information density, and interaction states first.
   - Add visual texture only where it clarifies importance or improves usability.
4. Keep code production-friendly.
   - Prefer semantic HTML, maintainable class structure, and small targeted changes over flashy rewrites.
   - Reuse existing components and tokens when possible.
5. Verify the result.
   - Check desktop and mobile layouts, focus/hover/active states, empty/loading/error states, and obvious usability issues.

## Anti-template red lines

- Do not apply glassmorphism, gradients, blur, heavy shadows, or 3D treatments across the whole page.
- Do not use the same card radius, shadow, spacing, and layout pattern everywhere.
- Do not hide weak hierarchy under oversized headings or oversized padding.
- Do not add animation unless it helps orientation, feedback, or state change.
- Do not ship dead-simple AI defaults such as purple-on-white SaaS styling unless the product already uses it.
- Do not rewrite working business logic just to make styling easier.
- Do not force fixed breakpoint recipes if the content clearly needs different wrap points.
- Do not confuse irregularity with craft. Human-looking work still needs stable order.

## Default workflow

### 1. Audit

Check:

- page goal and primary user action
- visual hierarchy and scan path
- component consistency and density
- typography scale and line length
- color balance and neutral balance
- responsive breakpoints based on content stress points
- interaction states
- obvious performance and usability issues

### 2. Choose the intervention level

- Light polish: spacing, color, typography, radii, borders, shadows, states
- Medium polish: section restructuring, responsive fixes, component refactor, better empty/loading/error states
- Deep polish: page-level redesign while keeping product logic and IA intact

Prefer the smallest intervention that materially improves the result.

### 3. Implement with these priorities

1. Hierarchy
2. Spacing rhythm
3. Typography
4. Surface treatment
5. Interaction feedback
6. Responsiveness
7. Performance and implementation cleanup

## Rule hierarchy

Use these levels consistently. Do not treat every preference as a law.

### Hard rules

- Preserve business logic, information architecture, and working flows unless the user asks for deeper redesign.
- Fix structure before styling: hierarchy, grouping, density, and states come before decoration.
- Every interactive element needs clear default, hover, active, focus, and disabled behavior where relevant.
- Mobile layouts must feel intentionally composed, not simply compressed from desktop.
- Keep code maintainable and aligned with the existing stack instead of forcing a new styling ideology.
- Do not use visual tricks to disguise weak hierarchy or broken UX.

### Strong defaults

- Default to one dominant accent family, one optional support accent family, and a restrained neutral system.
- Prefer off-black and off-white neutrals with a slight warm or cool bias instead of pure black and pure white.
- Use gradients only on focal elements, not as a page-wide blanket.
- Prefer stable type scales and limited text sizes rather than many near-duplicate sizes.
- Use a consistent spacing rhythm, then apply optical adjustments where text weight, borders, or density require them.
- Keep motion short and purposeful; micro-interactions are usually faster than full-page transitions.
- Prefer spacing, grouping, and contrast before relying on borders and shadows.

### Contextual rules

- Marketing pages can carry more visual expression, but message clarity still leads.
- Dashboards and internal tools should optimize order and density before adding personality.
- Auth flows should feel calm and obvious; visual tone is secondary to trust and clarity.
- Ecommerce and detail pages should prioritize media hierarchy, price/action clarity, and option feedback.
- Existing design systems may justify breaking a default if consistency across the product matters more.

## Design rules

### Color

- Think in color families, not raw color counts.
- Default to one dominant accent family, one optional support family, and one special-purpose family at most.
- Neutral ramps and status colors do not need to be counted as core brand accents, but they must stay controlled.
- Use more than three color families only when the product type clearly needs it, such as dense data or commerce states.
- Prefer off-black and off-white neutrals with a slight warm or cool bias.
- Use gradients only on focal areas such as hero accents, charts, or key CTA surfaces.

### Typography

- Build around a clear scale, but do not force a rigid mathematical ratio when the content needs optical tuning.
- Keep headings tighter and more deliberate than body copy.
- For Chinese-heavy pages, protect readability with moderate line length and stable line height.
- Use weight contrast and spacing before resorting to extra decoration.
- Keep the number of text sizes low enough that hierarchy is obvious at a glance.

### Layout and surfaces

- Separate layers mainly with spacing, contrast, and grouping. Use borders and shadows sparingly.
- Avoid card soup. Some sections should be open layouts rather than every block becoming a card.
- Let dense business UIs stay dense when appropriate; improve order, not just whitespace.
- Base spacing on a stable rhythm, then make visual compensation where content weight calls for it.

### Motion

- Keep transitions short and purposeful, usually in the 150ms-300ms range.
- Favor hover, focus, pressed, reveal, and state transitions over decorative looping motion.
- If motion competes with reading, remove it.

## Engineering rules

- Prefer Tailwind when the codebase already uses it. Otherwise follow the project stack.
- Keep HTML semantic when possible: `header`, `main`, `section`, `article`, `nav`, `aside`, `footer`.
- Do not introduce large utility piles or CSS overrides when a small structural refactor would be clearer.
- Keep interactive hit targets usable on touch screens.
- Add comments only for non-obvious decisions or tricky implementation details.
- Modern browser baseline is fine, but avoid fragile CSS features without a fallback.

## Scenario routing

Before making substantial changes, classify the task:

- `marketing`: selling, storytelling, launch pages, product sites
- `auth`: sign-in, sign-up, password reset, invite, onboarding step
- `dashboard`: admin, analytics, operations, internal tools
- `detail`: ecommerce detail, pricing, feature detail, content detail
- `component`: buttons, cards, forms, tables, modals, nav, data display

Use the relevant guidance in [references/polish-playbook.md](references/polish-playbook.md) when the page type materially changes the right design choices.

## Anti-AI quality bar

The result should pass these questions:

- Does the page have a clear visual center instead of every section competing equally?
- Are important and secondary areas intentionally treated differently?
- Does the mobile view look designed, not merely stacked?
- Are empty, loading, error, hover, focus, and disabled states believable?
- Did the polish reduce generic repetition rather than add more decoration?
- Would a strong frontend reviewer believe this came from a real product team?

## Response mode selection

When the user has not specified how they want the result delivered, choose a sensible default without blocking progress. For straightforward edit requests, default to direct implementation plus a short explanation.

When the task is exploratory, strategic, or likely to benefit from multiple answer shapes, briefly offer response modes and let the user choose. Keep the choice simple and short.

Preferred response modes:

- `direct edit`: implement first, then summarize the highest-impact changes
- `audit then edit`: diagnose the main UI problems first, then implement fixes
- `design options`: present `2-3` distinct directions before editing
- `prompt only`: produce a reusable prompt for Codex, Claude, or another model
- `review only`: list findings, risks, and priorities without changing code yet

Do not force this choice on every request. Use it only when it adds clarity or when the user is clearly still deciding how they want to work.

## Response shape

When delivering a result, prefer this structure:

1. `Direction`: one sentence on the intended visual and UX shift.
2. `Implementation`: make the code changes directly when working in a repo; otherwise provide complete runnable code.
3. `What changed`: call out the few highest-impact refinements.
4. `Validation`: note what was checked and any remaining risk.
5. `Optional next pass`: suggest the next meaningful polish step.

## Tooling and publishing

- If working in Codex and the user asks to deploy or publish, use available GitHub or Vercel tooling when appropriate.
- If those tools are unavailable, give the exact commands or steps instead.
- Do not promise auto-deploy, auto-commit, or live editing unless the environment actually supports it and the user asked for it.

## References

Open [references/polish-playbook.md](references/polish-playbook.md) when you need the detailed anti-AI checklist, page-type guidance, or a concrete polish rubric.
Open [references/call-examples.md](references/call-examples.md) when you want ready-to-use prompts for Codex, Claude, or other models.

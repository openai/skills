---
name: "ui"
description: "Generate or refresh docs/ui.md from repository evidence. Use only when explicitly invoked to inspect frontend code, styles, theme tokens, component libraries, and responsive patterns, then document transferable UI implementation details for other agents."
---

# ui

## Objective

Create or update `docs/ui.md` so another agent can reproduce the repository's UI system and styling conventions accurately.

## Invocation contract

- Run only on explicit invocation of `$ui`.
- If `docs/` does not exist in the target repository, create it before writing `docs/ui.md`.
- Read the existing `docs/ui.md` before changing it.
- Inspect frontend code, CSS, SCSS, Tailwind config, theme tokens, component libraries, layouts, shared components, form and validation patterns, icon usage, responsive rules, dark mode logic, and asset conventions.
- Update the existing file in place when it exists and preserve useful content that still matches the repository.
- If the repository has little or no UI evidence, write `Unknown` and cite the missing areas checked.

## Required sections

Create or update `docs/ui.md` with these sections:

- UI stack
- Page inventory
- Theme tokens
- Color palette
- Typography
- Spacing scale
- Radius scale
- Shadow rules
- Grid and layout rules
- Breakpoints
- Component patterns
- State styles
- Form styles
- Table styles
- Modal and drawer styles
- Navigation patterns
- Feedback patterns
- Animation rules
- Accessibility rules
- Exact CSS or token level details where available
- Tailwind mappings if applicable
- Important reusable components
- Abstract page renders
- UI file map
- UI handoff summary

## Documentation rules

- Make the file directly useful to another coding agent that needs to reproduce the same style.
- Record exact token names, CSS custom properties, Tailwind theme entries, spacing values, breakpoints, and reusable component paths when they exist.
- For each significant page or route, include an abstract pure-render HTML sketch that captures structure and hierarchy without framework logic, data fetching, event handlers, or implementation-specific state wiring.
- Keep each abstract page render at the layout level: sections, landmarks, major components, repeated blocks, and content hierarchy.
- Label each abstract render with the source page or route it was inferred from and mark missing structure as `Unknown`.
- Use semantic HTML where possible in the abstract renders, such as `header`, `nav`, `main`, `section`, `aside`, `form`, `table`, and `footer`.
- Distinguish confirmed behavior from `Inference:` lines.
- Prefer concise tables and path lists over long prose.
- Preserve user edits and useful prior notes that still match the codebase.

## Abstract page render format

For the `Abstract page renders` section, add one subsection per important page, screen, or route and include:

- Page or route name
- Source files used
- Purpose of the page
- Main regions and reusable blocks
- A fenced `html` code block showing the pure-render abstract layout

The HTML should:

- Show only static structure and hierarchy.
- Use placeholder content only when the real content is dynamic.
- Omit JavaScript behavior, framework directives, and styling implementation details.
- Be concise enough to scan quickly while still being useful for reconstruction.

## Suggested scan targets

- Frontend app: `app/`, `src/`, `pages/`, `components/`, `layouts/`
- Styling: `styles/`, `*.css`, `*.scss`, `tailwind.config.*`, `postcss.config.*`, theme files
- UI primitives: design system folders, shared components, icon registries, utility class maps
- Interaction patterns: form components, validators, table helpers, modal or drawer components, toast or alert systems

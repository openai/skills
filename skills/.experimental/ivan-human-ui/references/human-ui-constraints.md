# Ivan Human UI Constraints

Use this file as the hard constraint pack when redesigning marketing pages or dashboards.

## 1) Layout And Hierarchy

- Replace "center everything" defaults with intentional asymmetry.
- Prefer hero split layouts when content is dense: headline block `3/5`, support block `2/5`.
- Align the top of support copy with the top of the headline when using split hero layout.
- Keep screenshot blocks full-width inside container when zigzag layouts feel noisy.
- Use consistent container rhythm; common gap baseline: `8px`.

## 2) Typography

- Use Inter Variable when available; enable display/text axis where supported.
- Use precise weights between defaults when needed (example: `550` between `500` and `600`).
- Tighten headline tracking slightly at large sizes.
- Keep eyebrow labels mono, uppercase, with wider tracking.
- Use character-based measure (`ch`) for readable line length where suitable.

## 3) Color Direction

- Avoid default AI palette bias (especially generic purple/indigo gradients).
- Use neutral grays as baseline unless brand color is explicit.
- Match gray family across screenshot and UI surface (avoid slate/neutral mismatch).
- Remove decorative color for its own sake; color must carry hierarchy or brand meaning.

## 4) Borders, Rings, Shadows

- Avoid muddy solid border + shadow combos.
- Prefer subtle outer ring (`gray-950` with low opacity) plus clean shadow.
- Keep ring outside where possible for sharper separation.
- Ensure concentric radii between container and nested screenshot.

## 5) Buttons And Navigation

- Remove unnecessary icons in secondary actions if they add clutter.
- Use consistent button heights by padding strategy, not fixed height.
- Keep visual heights equal when mixing solid and outlined buttons.
- Keep navbar action less dominant than hero primary CTA.

## 6) Imagery And Screenshots

- Prefer real product screenshots over generated fake UI.
- Crop screenshots to highlight one feature at a time.
- Keep screenshot framing intentional (inset wells, clear edge definition).
- Add subtle overlay ring on top of screenshot when edge definition is weak.

## 7) Section Styling

- Keep logo cloud simple; avoid washed opacity if logos lose identity.
- For feature headings, allow inline title + supporting sentence treatment.
- Simplify stats blocks; avoid unnecessary dark slabs unless brand requires it.
- Use section dividers and canvas-grid borders only when they improve structure clarity.

## 8) Forbidden Output Style

- Do not output fuzzy advice like:
  - "optimize it a bit"
  - "add some premium logic"
  - "use some XX logic"
- Do output explicit, editable instructions:
  - token/class/value changes
  - spacing/radius/weight numbers
  - exact component placement changes

# PowerPoint and Excel Authoring Mastery Notes

## Mental Model

Office artifacts are structured documents, not screenshots. A good generated deck or workbook remains editable, auditable, and traceable after the agent finishes.

## PowerPoint Principles

- Reuse slide masters and layouts.
- Keep titles, labels, tables, and notes as editable objects.
- Preserve speaker notes when updating decks.
- Avoid rasterizing data unless the user asks for an image.
- Validate visual layout after structural validation.

## Excel Principles

- Preserve formulas when auditability matters.
- Separate inputs, calculations, and outputs.
- Use named ranges for key assumptions.
- Avoid overwriting formulas with values.
- Treat `data_only=True` carefully because it reads cached values.

## Model-Backed Decks

Deck numbers should trace to workbook cells or source rows. The workbook is the source of truth; regenerate slides after workbook changes instead of manually patching derived numbers.

## Common Risks

- formulas broken by row/column insertions
- chart references not updated
- merged cells hiding data
- missing fonts changing layout
- text overflow in placeholders
- stale cached formula values

## Review Standard

A complete Office artifact change proves:

- output files open structurally
- key text/formulas/named ranges are present
- generated numbers are traceable
- visual preview is checked when layout matters
- assumptions and live data sources are documented

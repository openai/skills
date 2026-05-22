# PowerPoint and Excel Authoring Workflows

Use this reference to produce Office files that are editable, auditable, and validated.

## PowerPoint Workflow

1. Inspect template slide layouts and placeholders.
2. Reuse slide masters when possible.
3. Keep text as editable text.
4. Avoid rasterizing tables or key numbers.
5. Validate slide count, text, notes, images, and chart objects.
6. Render or preview when layout fidelity matters.

Inspect:

```python
from pptx import Presentation
prs = Presentation("deck.pptx")
for i, slide in enumerate(prs.slides, 1):
    print(i, [shape.text for shape in slide.shapes if hasattr(shape, "text") and shape.text.strip()])
```

## Excel Workflow

1. Inspect sheets, named ranges, formulas, charts, merged cells, and workbook links.
2. Preserve formulas unless the user asks for values.
3. Keep inputs, calculations, and outputs distinct.
4. Use named ranges for important assumptions.
5. Validate formulas with `data_only=False`; inspect calculated values with `data_only=True` only if Excel or another engine has recalculated.

Inspect formulas:

```python
from openpyxl import load_workbook
wb = load_workbook("model.xlsx", data_only=False)
for ws in wb.worksheets:
    formulas = [cell.coordinate for row in ws.iter_rows() for cell in row if isinstance(cell.value, str) and cell.value.startswith("=")]
    print(ws.title, formulas[:20])
```

## Model-Backed Decks

Build order:

1. Update workbook assumptions and formulas.
2. Validate workbook checks.
3. Extract slide-ready tables/numbers.
4. Generate deck from workbook outputs.
5. Reopen deck and verify every generated number.

Trace every visible number:

```text
slide:
shape/table:
visible value:
workbook sheet/cell:
source:
timestamp:
```

## Layout Validation

Check:

- text overflow or clipping
- overlapping shapes
- missing fonts
- chart label collisions
- wide table fit
- speaker notes preservation

Use LibreOffice, PowerPoint, or another renderer when visual fidelity matters.

## Final Artifact

Final notes should include:

```text
input/template files:
output files:
library versions:
validation commands:
formula/named-range checks:
visual preview status:
assumptions or manual edits:
```

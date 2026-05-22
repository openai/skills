---
name: powerpoint-excel-authoring
description: Create, edit, inspect, validate, or automate PowerPoint decks and Excel workbooks. Use when working with .pptx or .xlsx files, python-pptx, openpyxl, financial models, charts, tables, slide templates, speaker notes, workbook formulas, named ranges, or model-backed presentation outputs.
---

# PowerPoint and Excel Authoring

Use this skill for generated or edited Office artifacts. Treat decks and workbooks as inspectable files with structure, not screenshots; validate the actual document after writing it.

## Validated Version Evidence

This guidance was checked against mined environments using `python-pptx` 1.0.2 and `openpyxl` 3.1.5. Office file rendering still varies by viewer, fonts, and chart support, so capture library versions before debugging generated files:

```bash
python - <<'PY'
from importlib.metadata import PackageNotFoundError, version
for package in ["python-pptx", "openpyxl", "xlsxwriter", "pandas"]:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "not installed")
PY
```

If the project has no package manager or the required Office libraries are missing, install only the packages needed for the requested artifact:

```bash
python -m pip install python-pptx openpyxl
```

Add `xlsxwriter` or `pandas` only when the workbook workflow needs charts, styled report generation, or dataframe export.

## What This Skill Delivers

Use this skill to create or modify Office files that remain editable and auditable. A complete run produces:

- The source template/input files and library versions.
- A deterministic script or notebook cell that writes the output artifact.
- A structural validation of slides/sheets/text/formulas/named ranges.
- A visual or rendered check when layout matters.
- A final note listing assumptions, live data, manual edits, and any formulas intentionally overwritten.

## Standalone Quick Start

If there is no existing template, create a minimal editable deck:

```python
from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Status Update"
slide.placeholders[1].text = "Generated with python-pptx"
prs.save("output.pptx")
```

Create a minimal workbook with formulas preserved:

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Model"
ws["A1"] = "Revenue"
ws["B1"] = 100
ws["A2"] = "Growth"
ws["B2"] = 0.10
ws["A3"] = "Next"
ws["B3"] = "=B1*(1+B2)"
wb.save("output.xlsx")
```

Immediately prove the files reopen and preserve editable content:

```python
from pptx import Presentation
from openpyxl import load_workbook

prs = Presentation("output.pptx")
assert len(prs.slides) >= 1
assert prs.slides[0].shapes.title.text

wb = load_workbook("output.xlsx", data_only=False)
assert wb["Model"]["B3"].value == "=B1*(1+B2)"
```

For user work, prefer editing their template instead of starting from blank files.

## Workflow

1. Identify the artifact: presentation, workbook, or model-backed deck.
2. Inspect existing files before editing:
   - For `.pptx`, inspect slide count, layouts, placeholders, notes, images, and charts.
   - For `.xlsx`, inspect sheet names, dimensions, formulas, named ranges, merged cells, and charts.
3. Preserve templates, styles, and formulas unless the user asks to redesign.
4. Make deterministic edits with `python-pptx`, `openpyxl`, or the repo's existing tooling.
5. Reopen the output and verify structure, text, formulas, and key visual elements.

## PowerPoint

- Use existing slide masters and layouts when available.
- Keep titles, labels, and notes editable as text.
- Avoid placing important content only in raster images.
- Check that text fits in its shape and does not overlap other elements.
- Use speaker notes for narration, assumptions, or source detail when appropriate.
- For charts, preserve data provenance or include the source workbook when possible.

## Excel

- Prefer formulas over hardcoded outputs when a workbook is meant to be auditable.
- Use named ranges for key assumptions and outputs.
- Keep inputs, calculations, and outputs visually distinct.
- Validate workbook links, formulas, and sheet references after edits.
- Avoid overwriting formulas with values unless explicitly requested.
- For financial models, include balance checks, sensitivity tables, and clear assumptions when in scope.

## Model-Backed Decks

- Build or update the workbook first, then populate slides from workbook outputs.
- Keep every deck number traceable to a workbook cell, table, or source.
- Add a concise source or timestamp note when using live or unstable data.
- Re-run deck generation after workbook changes instead of manually patching derived numbers.

## References

Open `references/workflows.md` for detailed PowerPoint template editing, layout checks, Excel formulas/named ranges/charts, model-backed decks, validation, and review artifacts.

Open `references/mastery.md` for Office artifact mental models, editability/auditability rules, formula and chart risks, model-backed deck design, and review standards.

Open `references/source-evidence.md` when checking whether this skill covers workflows observed in mined/source repository evidence.

Traceability contract for generated numbers:

```text
slide:
visible number:
workbook sheet/cell or source row:
formula or transformation:
timestamp/source:
```

## Validation

Useful checks include:

```bash
python - <<'PY'
from pathlib import Path
print(Path("output.pptx").stat().st_size)
print(Path("output.xlsx").stat().st_size)
PY
```

Reopen PowerPoint outputs and inspect editable structure:

```bash
python - <<'PY'
from pptx import Presentation

prs = Presentation("output.pptx")
print("slides", len(prs.slides))
for i, slide in enumerate(prs.slides, 1):
    texts = [shape.text for shape in slide.shapes if hasattr(shape, "text") and shape.text.strip()]
    print(i, texts[:3])
PY
```

Reopen Excel outputs with formulas preserved:

```bash
python - <<'PY'
from openpyxl import load_workbook

wb = load_workbook("output.xlsx", data_only=False)
print(wb.sheetnames)
for ws in wb.worksheets:
    formulas = [cell.coordinate for row in ws.iter_rows() for cell in row if isinstance(cell.value, str) and cell.value.startswith("=")]
    print(ws.title, ws.max_row, ws.max_column, formulas[:10])
PY
```

If visual fidelity matters, render or preview the document and check for clipping, overlap, missing fonts, and chart sizing.

## Done Criteria

- The file opens with the expected slide/sheet structure.
- Key text, formulas, charts, and generated numbers are verified.
- Any assumptions, live data sources, or manual edits are called out.
- The final notes include output paths and the validation commands used.

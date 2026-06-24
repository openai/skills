# Source Evidence

Use this file as the evidence anchor for the workflow coverage in this skill. Office automation must produce editable, inspectable artifacts rather than screenshots or brittle one-off files.

## Retrieved Sources

- `deepset-ai/haystack`: `PPTXToDocument`, `XLSXToDocument`, multi-file conversion docs, and dependencies on `python-pptx`, `openpyxl`, `pandas`, and `tabulate`.
- `OpenHands/OpenHands`: lock evidence for `openpyxl` 3.1.5 and `python-pptx` 1.0.2.
- `letta-ai/letta`: lock evidence for `python-pptx` 1.0.2.
- `MetaGPT`: `.xlsx` document-store fixtures and spreadsheet-backed retrieval examples.

## Workflows Reflected In The Skill

### Editable Office Artifacts

Haystack converter evidence treats `.pptx` and `.xlsx` as structured files with extractable document content. The skill therefore requires agents to preserve editability:

- use real PowerPoint shapes, placeholders, notes, and layouts instead of flat images;
- use workbook cells, formulas, named ranges, tables, and charts instead of static screenshots;
- keep source data and generated outputs auditable.

### Template-Preserving PowerPoint Work

PowerPoint workflows must respect slide masters, existing layouts, brand fonts/colors, and placeholders. The skill covers template inspection, slide generation, notes/speaker context, and validation by reopening the file.

### Excel Modeling And Reporting

Spreadsheet workflows must preserve formulas and workbook semantics. The skill requires:

- formula and named-range checks;
- chart source-range validation;
- table formatting and sheet protection when relevant;
- recalculation/openability notes when generated outside Excel.

### Document Conversion And Retrieval Use Cases

Haystack and MetaGPT evidence shows Office files used as inputs to document pipelines and retrieval stores. The skill therefore covers both authoring and extraction-oriented checks: generated files should be readable by common libraries and retain meaningful text/table content.

## Review Standard

Reject Office automation that only creates visually plausible files. A useful workflow must prove the artifact opens, content remains editable, formulas and chart ranges are inspectable, and extraction/reload checks pass for the target use case.

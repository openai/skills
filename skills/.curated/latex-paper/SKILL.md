---
name: "latex-paper"
description: "End-to-end LaTeX paper authoring and editing for research-grade manuscripts. Use when tasks require creating, restructuring, or updating formatted .tex projects, managing citations/figures/tables, enforcing section conventions, and running deterministic compile/lint/troubleshooting workflows."
---

# LaTeX Paper Skill

## Overview

Use this skill to create and maintain publication-ready LaTeX projects with predictable structure, formatting consistency, and reproducible compile diagnostics.

## Workflow Decision Tree

1. Identify intent:
- If the user asks to start a paper, scaffold with `scripts/new_paper.sh`.
- If the user asks to edit an existing paper, preserve class/template choices and patch minimally.
- If the user asks to convert a `.tex` file directly into PDF, run `scripts/tex_to_pdf.sh`.
- If the user reports build failures, run `scripts/compile.sh` first to capture deterministic diagnostics.
- If the user reports citation/reference issues, run `scripts/fixrefs.sh` and then patch affected `.tex`/`.bib` entries.

2. Choose template only when creating a new project:
- Use `article` for general manuscripts, drafts, and arXiv-style preprints.
- Use `ieeetran` for IEEE conference/journal flows.
- Use `acmart` for ACM conference/journal flows.
- Load [template_matrix.md](references/template_matrix.md) for selection details.

3. Apply editing conventions:
- Keep one idea per paragraph in methods/results-heavy sections.
- Keep labels stable; never rename labels/cite keys unless all references are updated atomically.
- Prefer explicit section names over vague titles.
- Ensure every figure/table has caption + label + in-text reference.

4. Verify before completion:
- Run `scripts/compile.sh <project-dir>`.
- Run `scripts/lint.sh <project-dir>`.
- Run `scripts/fixrefs.sh <project-dir>`.
- Return the concrete file changes and remaining warnings.

## Commands

### New paper scaffold

```bash
scripts/new_paper.sh /path/to/paper --template article --title "Paper Title" --author "Author Name"
```

### Compile with deterministic logs

```bash
scripts/compile.sh /path/to/paper --main main.tex --engine pdflatex
```

### Convert a single TeX file to PDF

```bash
scripts/tex_to_pdf.sh /path/to/main.tex --engine pdflatex
```

### Lint and style checks

```bash
scripts/lint.sh /path/to/paper --main main.tex
```

### Missing refs/citations diagnostics

```bash
scripts/fixrefs.sh /path/to/paper
```

## Project Editing Rules

- Preserve existing class and package choices unless the user asks to migrate templates.
- Avoid broad rewrites; patch the smallest viable region.
- Keep bibliography keys stable and human-readable (`lastnameYYYYtopic`).
- Add comments only where logic is non-obvious (for example, custom macros or float constraints).

## Reference Loading (Progressive)

Load only what is needed:

- Structure and section logic: [structure.md](references/structure.md)
- Citations and bibliography workflows: [citations.md](references/citations.md)
- Figure/table conventions: [figures_tables.md](references/figures_tables.md)
- Template choice and tradeoffs: [template_matrix.md](references/template_matrix.md)

## Done Criteria

Complete the task only after these checks:

- Project compiles or has explicit blocking diagnostics with file/line pointers.
- No unresolved `\\ref`/`\\cite` issues from `scripts/fixrefs.sh`.
- Requested formatting changes are reflected in source, not only in generated output.

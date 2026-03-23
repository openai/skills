---
name: ascii-codebase-diagrams
description: Scan a repository and produce aligned text-based architecture diagrams with Unicode box-drawing characters. Use when the task is to diagram a codebase, map module relationships, show request or data flow, visualize directory structure, or create text-only architecture documentation grounded in source files.
---

# ASCII Codebase Diagrams

## Overview

Use this skill to turn repository structure and runtime behavior into clean text diagrams that are easy to review in chat, markdown, or plain-text files. Keep every box, connector, and label grounded in what the codebase actually does.

## Workflow

1. Scan the repository before drawing anything. Start with the README and runtime manifests, then inspect entrypoints, key config, and the most important directories with fast file searches.
2. Separate runtime architecture from build tooling, CI, examples, and tests unless those are part of the requested diagram.
3. Pick the smallest set of diagrams that explains the system clearly. Usually 3-6 diagrams is enough.
4. Load `references/glyph-palette.md` before drawing so spacing, alignment, and glyph choices stay consistent.
5. Draft the diagrams, then lint them manually using the self-check rules in the reference.
6. Deliver diagrams inline by default. If the user asks for files, write them to the requested path or to `output/ascii-diagrams/`.

## What To Diagram

Always consider these:

- High-level request or workflow pipeline
- Module or service interconnection map
- Directory or file layout tree

Add these when they help:

- Data flow or transformation path
- External integration map
- API route map
- State machine or lifecycle view
- Deployment topology

## Output Rules

- Use Unicode box-drawing characters, not Mermaid, PlantUML, screenshots, or image files.
- Keep lines under 100 characters when practical; aim for 80 when the diagram stays readable.
- Use ALL CAPS titles with an underline of matching width.
- Keep labels short and literal.
- Add a short legend only when the diagram would otherwise be ambiguous.
- State assumptions explicitly whenever the repo evidence is incomplete.

## File Output Convention

When the user wants files, use:

```text
output/ascii-diagrams/
├── 00_overview.txt
├── 01_pipeline.txt
├── 02_module-map.txt
└── ...
```

- `00_overview.txt` should summarize what each numbered file covers.
- Use lowercase kebab-case names after the numeric prefix.
- Keep each file self-contained so it can be opened independently.

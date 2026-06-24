---
name: research-paper-translation
description: Translate research paper PDFs into faithful Chinese with exact version locking, paragraph alignment, and fact-preserving review. Use when the user wants a Chinese close-reading translation of a paper PDF, needs to verify a translation against the source, or wants version-aware paragraph-by-paragraph rendering instead of a summary.
---

# Research Paper Translation

Translate against the exact paper PDF the user provides. Do not mix arXiv versions, conference versions, camera-ready variants, or later revisions unless the user explicitly asks for comparison.

## Trigger Conditions

Use this skill when the user asks for any of the following:

- paragraph-by-paragraph Chinese translation of a research paper PDF
- Chinese close reading of a paper without skipping sentences
- verification that an existing translation matches the source paper
- version-aware translation where PDF wording may differ across releases

Do not use this skill for generic document translation unless the document is clearly a research paper or preprint.

## Workflow

### 1. Lock the exact source artifact

- Read the local PDF first.
- Identify visible version evidence when possible:
  - `arXiv:...v1`, `v2`, etc.
  - conference footer
  - page headers
  - wording or statistics that reveal a version difference
- If there is a version-mismatch risk, state the detected version in working notes or the output.
- If the user already has a translation from a different paper version, warn and rebuild from the actual PDF they provided.

### 2. Extract text before translating

- Prefer the bundled script at `scripts/extract_pdf_text.py` when available.
- If using tools directly, prefer this order:
  - `PyMuPDF`
  - `pdftotext`
  - `pdfplumber`
- Save extracted text to a temp file when the paper is long, so section-by-section review is stable and not limited by terminal truncation.
- Prefer real text extraction over OCR-like guessing.

For extraction details and fallback guidance, read `references/pdf-extraction.md`.

### 3. Clean extraction artifacts

- Repair hyphenated line breaks such as `dia-\nlogues`.
- Merge wrapped lines back into sentences when they clearly belong together.
- Ignore repeated headers, footer metadata, and page numbers unless the user asked for them.
- Keep section order aligned with the paper.
- Treat figure captions, table captions, footnotes, and appendices as separate units when they materially affect understanding.

### 4. Translate by paragraph, not by summary

- Preserve paragraph order from the paper.
- If extraction merged two paper paragraphs into one block, split them before translating.
- Preserve technical terms when needed, especially:
  - benchmark names
  - task names
  - model names
  - dataset names
  - metric names

For serious study, the default output format is:

- `原文定位句`
  - Use only a short opening phrase or sentence fragment for locating the paragraph.
  - Do not paste long stretches of original text.
- `翻译`
  - Translate the full paragraph content into Chinese.
  - Do not skip sentences.

### 5. Preserve facts exactly

- Keep all numbers, percentages, counts, model names, metric names, table references, and section references aligned with the source.
- Be especially careful with:
  - dataset size
  - average turns, sessions, or tokens
  - reported gains or drops
  - task definitions
  - error taxonomies
- Keep parenthetical citations concise rather than naturalizing them away.

### 6. Handle paper structure explicitly

- Translate these separately when present:
  - abstract
  - main sections
  - subsections
  - conclusion
  - limitations
  - broader impacts
- Include appendices when the user wants deep reading.
- For dense tables, summarize table meaning in prose unless the user explicitly asks for row-by-row translation.

### 7. Perform a strict review pass

Before finalizing:

- Check section titles against the extracted text.
- Check that each translated paragraph has a matching source paragraph.
- Recheck the first paragraph of every section because version mismatch often shows up there first.
- Recheck every important number against the PDF.
- If the user reports that a translation does not match the paper, assume one of these first:
  - version mismatch
  - extraction drift
  - summary-style rewriting instead of translation

## Output Modes

### Default: close reading

Use when the user wants faithful study output:

- `原文定位句`
- `翻译`

### Fast reading

Use only when the user explicitly wants speed over strict alignment:

- section heading
- concise Chinese translation
- optional short takeaway

## Red Flags

Stop and correct the workflow if any of these appear:

- numbers in the translation do not match the PDF
- the quoted English source text is paraphrased rather than extracted
- arXiv and conference versions are being mixed
- a "full translation" reads like a summary

## Example Requests

Use this skill for prompts like:

- `帮我逐段翻译这篇论文`
- `我要精读，别漏句子`
- `按原文定位句 + 翻译来做`
- `检查这版翻译是不是和原论文对得上`
- `Use $research-paper-translation to read this paper PDF and produce a paragraph-aligned Chinese translation.`

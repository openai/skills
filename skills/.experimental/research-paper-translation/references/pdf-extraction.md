# PDF Extraction Notes

Use this reference only when you need extraction guidance beyond the core workflow in `SKILL.md`.

## Extraction order

Prefer these in order:

1. `PyMuPDF` (`fitz`)
2. `pdftotext`
3. `pdfplumber`

Why:

- `PyMuPDF` usually gives the best balance of speed and structural fidelity for born-digital papers.
- `pdftotext` is a strong fallback when Python PDF libraries are unavailable.
- `pdfplumber` can recover text when layout handling differs, but often needs more cleanup.

## Bundled script

If `scripts/extract_pdf_text.py` exists, use it first instead of rebuilding the extraction logic inline.

The script:

- tries extraction engines in the preferred order
- writes text to `--output` if provided
- otherwise writes to a temp `.txt` file
- prints the chosen engine and output path

## Cleanup expectations

After extraction, still review for:

- hyphenated line breaks
- wrapped lines that should be merged into sentences
- repeated headers or footers
- broken paragraph boundaries
- caption spillover into body text

## Failure handling

If one extractor succeeds but the text quality is poor:

- switch to the next available extractor before translating
- compare the first paragraph of each section against the PDF
- confirm that section headings, key numbers, and table references still align

If none of the preferred tools are available:

- explain the limitation clearly
- avoid pretending that guessed or paraphrased English is extracted source text
- do not continue with a "faithful translation" claim unless the source text is trustworthy

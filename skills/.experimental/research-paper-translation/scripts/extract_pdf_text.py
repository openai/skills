#!/usr/bin/env python3
"""Extract text from a PDF with deterministic fallbacks."""

from __future__ import annotations

import argparse
import importlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF using PyMuPDF, pdftotext, or pdfplumber."
    )
    parser.add_argument("pdf", help="Path to the input PDF file.")
    parser.add_argument(
        "--output",
        help="Path to the output text file. Defaults to a temp file when omitted.",
    )
    return parser.parse_args()


def ensure_pdf(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\f", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip() + "\n"


def extract_with_pymupdf(pdf_path: Path) -> str:
    fitz = importlib.import_module("fitz")
    document = fitz.open(pdf_path)
    try:
        pages = [page.get_text() for page in document]
    finally:
        document.close()
    return "\n\n".join(pages)


def extract_with_pdftotext(pdf_path: Path) -> str:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext is not installed")
    result = subprocess.run(
        [pdftotext, "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
    )
    return result.stdout.decode("utf-8", errors="replace")


def extract_with_pdfplumber(pdf_path: Path) -> str:
    pdfplumber = importlib.import_module("pdfplumber")
    pages: list[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n\n".join(pages)


def temp_output_path(pdf_path: Path) -> Path:
    stem = pdf_path.stem.replace(" ", "_")
    handle, path = tempfile.mkstemp(prefix=f"{stem}-", suffix=".txt")
    Path(path).unlink(missing_ok=True)
    return Path(path)


def write_output(text: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(normalize_text(text), encoding="utf-8")


def main() -> int:
    args = parse_args()
    pdf_path = Path(args.pdf).expanduser().resolve()
    ensure_pdf(pdf_path)

    extractors = [
        ("pymupdf", extract_with_pymupdf),
        ("pdftotext", extract_with_pdftotext),
        ("pdfplumber", extract_with_pdfplumber),
    ]
    errors: list[str] = []

    for name, extractor in extractors:
        try:
            text = extractor(pdf_path)
            if text.strip():
                output_path = (
                    Path(args.output).expanduser().resolve()
                    if args.output
                    else temp_output_path(pdf_path)
                )
                write_output(text, output_path)
                print(f"engine={name}")
                print(f"output={output_path}")
                return 0
            errors.append(f"{name}: extracted empty text")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {exc}")

    print("Failed to extract text from the PDF.", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Build a lightweight JSONL index from BaZi reference PDFs.

Example:
  python3 scripts/build_pdf_index.py \
    --source-dir "/Users/ivan/Desktop/电子书/ddddddd/" \
    --out references/pdf-index.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


KEYWORDS = {
    "三命通会": ["三命通会"],
    "穷通宝鉴": ["穷通宝鉴"],
    "滴天髓_子平真诠": ["滴天髓", "子平真詮", "子平真诠"],
    "八字提要": ["八字提要", "韦千里"],
    "周易译注": ["周易译注"],
}


def iter_pdfs(source_dir: Path) -> Iterable[Path]:
    for p in sorted(source_dir.iterdir()):
        if p.is_file() and p.suffix.lower() == ".pdf":
            yield p


def detect_tags(file_name: str) -> list[str]:
    tags: list[str] = []
    for canonical, kws in KEYWORDS.items():
        if any(kw in file_name for kw in kws):
            tags.append(canonical)
    return tags


def read_pdf_sample(pdf_path: Path, max_pages: int, max_chars: int) -> tuple[int, str]:
    try:
        from pypdf import PdfReader
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "pypdf is required. Install with: python3 -m pip install pypdf"
        ) from exc

    reader = PdfReader(str(pdf_path))
    text_parts: list[str] = []
    page_total = len(reader.pages)
    limit = min(max_pages, page_total)
    for i in range(limit):
        txt = reader.pages[i].extract_text() or ""
        if txt:
            text_parts.append(txt.strip())
    sample = "\n".join(text_parts).strip()
    if len(sample) > max_chars:
        sample = sample[:max_chars]
    return page_total, sample


def main() -> int:
    parser = argparse.ArgumentParser(description="Build PDF metadata index JSONL")
    parser.add_argument("--source-dir", required=True, help="Directory with source PDFs")
    parser.add_argument(
        "--out",
        default="references/pdf-index.jsonl",
        help="Output JSONL path (default: references/pdf-index.jsonl)",
    )
    parser.add_argument("--max-pages", type=int, default=6, help="Pages to sample per file")
    parser.add_argument("--max-chars", type=int, default=6000, help="Max chars per sample")
    args = parser.parse_args()

    source_dir = Path(args.source_dir).expanduser().resolve()
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not source_dir.exists() or not source_dir.is_dir():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    indexed = 0
    with out_path.open("w", encoding="utf-8") as fout:
        for pdf in iter_pdfs(source_dir):
            page_count, sample = read_pdf_sample(pdf, args.max_pages, args.max_chars)
            row = {
                "file_name": pdf.name,
                "file_path": str(pdf),
                "page_count": page_count,
                "tags": detect_tags(pdf.name),
                "sample_text": sample,
            }
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")
            indexed += 1

    summary_path = out_path.with_suffix(".summary.json")
    summary = {
        "source_dir": str(source_dir),
        "indexed_files": indexed,
        "index_path": str(out_path),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Indexed {indexed} PDFs -> {out_path}")
    print(f"Summary -> {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

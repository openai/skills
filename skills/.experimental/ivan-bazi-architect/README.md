# Ivan Bazi Architect

Codex skill for BaZi-oriented decision diagnostics with indexed classical references.

## Resource Setup

Configure your local PDF source directory in a local `config.json` (copy from `config.example.json`):

```json
{
  "source_dir": "/path/to/your/bazi-pdfs",
  "output_format": "audit_memo",
  "citation_mode": "book_file_snippet"
}
```

You can also pass `--source-dir` directly to the index script.

## Core References

- 三命通会（基础术语与多维意象）
- 穷通宝鉴（调候准则，SW-1）
- 滴天髓 / 子平真诠（能量流通与格局判定，SW-2）
- 八字提要（实战回退与执行指南）
- 周易译注（边界与可证伪框架）

## Quick Start

1. Build index:
   - `python3 scripts/build_pdf_index.py --source-dir "/path/to/your/bazi-pdfs" --out references/pdf-index.jsonl`
   - Or use config fallback: `python3 scripts/build_pdf_index.py --config config.json --out references/pdf-index.jsonl`
2. Invoke skill in Codex and request SW-1/SW-2/SW-3 diagnosis.
3. Ask for output in publish format (X thread / short brief / audit memo).

## Install In Codex

`$skill-installer install https://github.com/openai/skills/tree/main/skills/.experimental/ivan-bazi-architect`

## Boundary

This skill is for reflective strategy support with citations and uncertainty notes. It is not a deterministic guarantee engine.

## Contributor Notes

- Keep personal absolute paths out of committed files.
- Store local source directories in uncommitted `config.json`.
- Add new failure patterns to `references/gotchas.md` when you see repeat model mistakes.

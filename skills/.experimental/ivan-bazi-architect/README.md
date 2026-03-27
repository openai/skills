# Ivan Bazi Architect

Codex skill for BaZi-oriented decision diagnostics with indexed classical references.

## Resource Path

Default source directory:

`/Users/ivan/Desktop/电子书/ddddddd/`

## Core References

- 三命通会（基础术语与多维意象）
- 穷通宝鉴（调候准则，SW-1）
- 滴天髓 / 子平真诠（能量流通与格局判定，SW-2）
- 八字提要（实战回退与执行指南）
- 周易译注（边界与可证伪框架）

## Quick Start

1. Build index:
   - `python3 scripts/build_pdf_index.py --source-dir "/Users/ivan/Desktop/电子书/ddddddd/" --out references/pdf-index.jsonl`
2. Invoke skill in Codex and request SW-1/SW-2/SW-3 diagnosis.
3. Ask for output in publish format (X thread / short brief / audit memo).

## Install In Codex

`$skill-installer install https://github.com/openai/skills/tree/main/skills/.experimental/ivan-bazi-architect`

## Boundary

This skill is for reflective strategy support with citations and uncertainty notes. It is not a deterministic guarantee engine.

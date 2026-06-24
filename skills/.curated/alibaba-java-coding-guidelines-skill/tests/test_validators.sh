#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

missing=0
for validator in \
  scripts/validate_skill.py \
  scripts/validate_skill.mjs \
  scripts/validate_skill.go
do
  if [[ ! -f "$validator" ]]; then
    echo "缺少校验入口：$validator"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

python3 scripts/validate_skill.py
node scripts/validate_skill.mjs
go run scripts/validate_skill.go

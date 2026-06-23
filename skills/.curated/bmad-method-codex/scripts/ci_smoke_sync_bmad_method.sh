#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
TMP_OUTPUT="$(mktemp)"
trap 'rm -f "$TMP_OUTPUT"' EXIT

python3 scripts/sync_bmad_method.py check --json --max-retries 3 --retry-delay 1.0 > "$TMP_OUTPUT"
python3 - <<'PY' "$TMP_OUTPUT"
import json
import sys

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as handle:
    data = json.load(handle)

required = ["latest_release", "health", "action", "is_optimal"]
for key in required:
    if key not in data:
        raise SystemExit(f"Missing key in sync report: {key}")

if not isinstance(data["latest_release"].get("tag"), str):
    raise SystemExit("Release tag is missing")

print("OK sync smoke")
PY

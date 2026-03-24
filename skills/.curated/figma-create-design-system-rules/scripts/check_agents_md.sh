#!/usr/bin/env bash
# Draft helper: report whether AGENTS.md exists at repo root.
set -euo pipefail

if [[ -f AGENTS.md ]]; then
  echo "AGENTS.md found"
else
  echo "AGENTS.md not found"
fi

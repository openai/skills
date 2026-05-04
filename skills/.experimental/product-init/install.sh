#!/usr/bin/env bash
# product-init — one-line install, works on Claude Code, Codex CLI, OpenClaw
# curl -sSL https://raw.githubusercontent.com/mturac/product-init/main/install.sh | bash
set -euo pipefail

REPO="https://github.com/mturac/product-init"
INSTALLED=0

clone_to() {
  local dest="$1"
  if [ -d "$dest" ]; then
    echo "  already installed at $dest, pulling latest..."
    git -C "$dest" pull -q
  else
    echo "→ Installing to $dest ..."
    mkdir -p "$(dirname "$dest")"
    git clone -q "$REPO" "$dest"
  fi
  make_venv "$dest"
  INSTALLED=$((INSTALLED + 1))
}

make_venv() {
  local dir="$1"
  if [ ! -f "$dir/.venv/bin/python" ]; then
    echo "  → creating venv..."
    python3 -m venv "$dir/.venv"
    "$dir/.venv/bin/pip" install -q -r "$dir/scripts/requirements.txt"
  fi
}

# Auto-detect installed runtimes and install there
[ -d "$HOME/.claude" ]    && clone_to "$HOME/.claude/skills/product-init"
[ -d "$HOME/.codex" ]     && clone_to "$HOME/.codex/skills/product-init"
[ -d "$HOME/.openclaw" ]  && clone_to "$HOME/.openclaw/skills/product-init"

# Fallback: nothing detected → install for Claude Code (most common)
if [ "$INSTALLED" -eq 0 ]; then
  echo "No runtime detected — installing for Claude Code (default)"
  clone_to "$HOME/.claude/skills/product-init"
fi

echo ""
echo "product-init ready. Type /product-init in your AI tool to start."

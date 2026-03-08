#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# Conductor Skills Installer
# Installs Conductor workflow orchestration skills for your AI coding agent.
# https://github.com/conductor-oss/conductor-skills
# ─────────────────────────────────────────────────────────────────────────────

VERSION="1.0.0"
REPO_BASE="https://raw.githubusercontent.com/conductor-oss/conductor-skills/main"

# Files to download
SKILL_FILES=(
  "SKILL.md"
  "references/workflow-definition.md"
  "references/workers.md"
  "references/api-reference.md"
  "examples/create-and-run-workflow.md"
  "examples/monitor-and-retry.md"
  "examples/signal-wait-task.md"
)

# Colors (if terminal supports them)
if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BLUE='\033[0;34m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' BLUE='' BOLD='' NC=''
fi

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

info()  { echo -e "${BLUE}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC} $*"; }
error() { echo -e "${RED}[error]${NC} $*" >&2; }

usage() {
  cat <<EOF
${BOLD}Conductor Skills Installer v${VERSION}${NC}

Usage:
  install.sh --agent <name> [--project-dir <path>] [--force] [--uninstall]

Options:
  --agent <name>        AI coding agent to install for (required)
  --project-dir <path>  Target project directory (default: current directory)
  --force               Overwrite existing files without prompting
  --uninstall           Remove installed skill files
  --help                Show this help message

Supported agents:
  claude      Claude Code (Anthropic)
  codex       Codex CLI (OpenAI)
  gemini      Gemini CLI (Google)
  cursor      Cursor
  windsurf    Windsurf (Codeium)
  cline       Cline
  aider       Aider
  copilot     GitHub Copilot
  amazonq     Amazon Q Developer
  opencode    OpenCode
  roo         Roo Code
  amp         Amp

Examples:
  # Install for Claude Code
  install.sh --agent claude

  # Install for Cursor in a specific project
  install.sh --agent cursor --project-dir ~/my-project

  # Uninstall from a project
  install.sh --agent cursor --project-dir ~/my-project --uninstall

EOF
  exit 0
}

# ─────────────────────────────────────────────────────────────────────────────
# Download & assembly
# ─────────────────────────────────────────────────────────────────────────────

download_files() {
  local tmp_dir="$1"

  info "Downloading skill files..."
  for file in "${SKILL_FILES[@]}"; do
    local dir
    dir=$(dirname "$file")
    mkdir -p "$tmp_dir/$dir"
    if ! curl -sSfL "$REPO_BASE/$file" -o "$tmp_dir/$file" 2>/dev/null; then
      error "Failed to download $file"
      error "Check your internet connection and try again."
      rm -rf "$tmp_dir"
      exit 1
    fi
  done
  ok "Downloaded ${#SKILL_FILES[@]} files"
}

assemble_content() {
  local tmp_dir="$1"
  local output="$2"

  {
    cat "$tmp_dir/SKILL.md"
    echo ""
    echo "---"
    echo ""
    echo "# References"
    echo ""
    for f in "$tmp_dir"/references/*.md; do
      cat "$f"
      echo ""
      echo "---"
      echo ""
    done
    echo "# Examples"
    echo ""
    for f in "$tmp_dir"/examples/*.md; do
      cat "$f"
      echo ""
      echo "---"
      echo ""
    done
  } > "$output"
}

# ─────────────────────────────────────────────────────────────────────────────
# Safe file writing (respects --force)
# ─────────────────────────────────────────────────────────────────────────────

safe_write() {
  local target="$1"
  local source="$2"
  local force="$3"

  if [ -f "$target" ] && [ "$force" != "true" ]; then
    warn "File already exists: $target"
    printf "  Overwrite? [y/N] "
    read -r answer
    if [[ ! "$answer" =~ ^[Yy] ]]; then
      info "Skipped. Use --force to overwrite."
      return 1
    fi
  fi

  local dir
  dir=$(dirname "$target")
  mkdir -p "$dir"
  cp "$source" "$target"
  ok "Installed: $target"
}

# ─────────────────────────────────────────────────────────────────────────────
# Agent-specific installers
# ─────────────────────────────────────────────────────────────────────────────

install_claude() {
  local project_dir="$1"

  if ! command -v claude &>/dev/null; then
    error "'claude' CLI not found. Install it first: npm install -g @anthropic-ai/claude-code"
    exit 1
  fi

  info "Installing skill via Claude Code CLI..."
  claude skill add --from "https://github.com/conductor-oss/conductor-skills"
  ok "Conductor skill added to Claude Code"
}

install_to_file() {
  local target="$1"
  local assembled="$2"
  local force="$3"
  local prefix="${4:-}"

  if [ -n "$prefix" ]; then
    local tmp_with_prefix
    tmp_with_prefix=$(mktemp)
    {
      echo "$prefix"
      cat "$assembled"
    } > "$tmp_with_prefix"
    safe_write "$target" "$tmp_with_prefix" "$force"
    rm -f "$tmp_with_prefix"
  else
    safe_write "$target" "$assembled" "$force"
  fi
}

install_aider() {
  local project_dir="$1"
  local tmp_dir="$2"
  local force="$3"

  local skill_dir="$project_dir/.conductor-skills"
  mkdir -p "$skill_dir/references" "$skill_dir/examples"

  info "Copying skill files to $skill_dir ..."
  cp "$tmp_dir/SKILL.md" "$skill_dir/"
  for f in "$tmp_dir"/references/*.md; do
    cp "$f" "$skill_dir/references/"
  done
  for f in "$tmp_dir"/examples/*.md; do
    cp "$f" "$skill_dir/examples/"
  done
  ok "Files copied to $skill_dir"

  local config="$project_dir/.aider.conf.yml"
  if [ -f "$config" ] && grep -q "conductor-skills" "$config" 2>/dev/null; then
    info "Aider config already references conductor-skills, skipping."
  else
    info "Adding read entries to $config ..."
    {
      echo ""
      echo "# Conductor Skills"
      echo "read:"
      for file in "${SKILL_FILES[@]}"; do
        echo "  - .conductor-skills/$file"
      done
    } >> "$config"
    ok "Updated: $config"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Uninstall
# ─────────────────────────────────────────────────────────────────────────────

get_target_path() {
  local agent="$1"
  local project_dir="$2"

  case "$agent" in
    claude)   echo "__claude__" ;;
    codex)    echo "$project_dir/AGENTS.md" ;;
    gemini)   echo "$project_dir/GEMINI.md" ;;
    cursor)   echo "$project_dir/.cursor/rules/conductor.mdc" ;;
    windsurf) echo "$project_dir/.windsurfrules" ;;
    cline)    echo "$project_dir/.clinerules" ;;
    aider)    echo "$project_dir/.conductor-skills" ;;
    copilot)  echo "$project_dir/.github/copilot-instructions.md" ;;
    amazonq)  echo "$project_dir/.amazonq/rules/conductor.md" ;;
    opencode) echo "$project_dir/AGENTS.md" ;;
    roo)      echo "$project_dir/.roo/rules/conductor.md" ;;
    amp)      echo "$project_dir/.amp/instructions.md" ;;
  esac
}

do_uninstall() {
  local agent="$1"
  local project_dir="$2"

  if [ "$agent" = "claude" ]; then
    info "To remove the Conductor skill from Claude Code, run:"
    echo "  claude skill remove conductor"
    return
  fi

  local target
  target=$(get_target_path "$agent" "$project_dir")

  if [ "$agent" = "aider" ]; then
    if [ -d "$target" ]; then
      rm -rf "$target"
      ok "Removed: $target"
      info "Note: You may also want to remove the 'read:' entries from .aider.conf.yml"
    else
      warn "Nothing to uninstall: $target not found"
    fi
    return
  fi

  if [ -f "$target" ]; then
    rm -f "$target"
    ok "Removed: $target"
  else
    warn "Nothing to uninstall: $target not found"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

main() {
  local agent=""
  local project_dir="."
  local force="false"
  local uninstall="false"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --agent)      agent="$2"; shift 2 ;;
      --project-dir) project_dir="$2"; shift 2 ;;
      --force)      force="true"; shift ;;
      --uninstall)  uninstall="true"; shift ;;
      --help|-h)    usage ;;
      *)            error "Unknown option: $1"; usage ;;
    esac
  done

  if [ -z "$agent" ]; then
    error "Missing required --agent flag"
    echo ""
    usage
  fi

  # Normalize agent name
  agent=$(echo "$agent" | tr '[:upper:]' '[:lower:]')

  # Validate agent
  case "$agent" in
    claude|codex|gemini|cursor|windsurf|cline|aider|copilot|amazonq|opencode|roo|amp) ;;
    *) error "Unknown agent: $agent"; echo ""; usage ;;
  esac

  # Resolve project dir to absolute path
  project_dir=$(cd "$project_dir" && pwd)

  echo ""
  echo -e "${BOLD}Conductor Skills Installer v${VERSION}${NC}"
  echo ""

  # Handle uninstall
  if [ "$uninstall" = "true" ]; then
    do_uninstall "$agent" "$project_dir"
    echo ""
    ok "Done!"
    return
  fi

  # Claude Code has its own install path
  if [ "$agent" = "claude" ]; then
    install_claude "$project_dir"
    echo ""
    print_next_steps
    return
  fi

  # Download files to temp dir
  local tmp_dir
  tmp_dir=$(mktemp -d)
  trap 'rm -rf "$tmp_dir"' EXIT

  download_files "$tmp_dir"

  # Assemble into single file
  local assembled="$tmp_dir/_assembled.md"
  assemble_content "$tmp_dir" "$assembled"
  ok "Assembled skill content ($(wc -c < "$assembled" | tr -d ' ') bytes)"

  # Install based on agent
  echo ""
  info "Installing for ${BOLD}${agent}${NC} in ${project_dir} ..."
  echo ""

  case "$agent" in
    codex)
      install_to_file "$project_dir/AGENTS.md" "$assembled" "$force"
      ;;
    gemini)
      install_to_file "$project_dir/GEMINI.md" "$assembled" "$force"
      ;;
    cursor)
      local frontmatter
      frontmatter=$(cat <<'FRONT'
---
description: Conductor workflow orchestration - create, run, monitor, and manage workflows
globs: "**/*"
alwaysApply: true
---

FRONT
)
      install_to_file "$project_dir/.cursor/rules/conductor.mdc" "$assembled" "$force" "$frontmatter"
      ;;
    windsurf)
      install_to_file "$project_dir/.windsurfrules" "$assembled" "$force"
      ;;
    cline)
      install_to_file "$project_dir/.clinerules" "$assembled" "$force"
      ;;
    aider)
      install_aider "$project_dir" "$tmp_dir" "$force"
      ;;
    copilot)
      install_to_file "$project_dir/.github/copilot-instructions.md" "$assembled" "$force"
      ;;
    amazonq)
      install_to_file "$project_dir/.amazonq/rules/conductor.md" "$assembled" "$force"
      ;;
    opencode)
      install_to_file "$project_dir/AGENTS.md" "$assembled" "$force"
      ;;
    roo)
      install_to_file "$project_dir/.roo/rules/conductor.md" "$assembled" "$force"
      ;;
    amp)
      install_to_file "$project_dir/.amp/instructions.md" "$assembled" "$force"
      ;;
  esac

  echo ""
  print_next_steps
}

print_next_steps() {
  echo -e "${GREEN}${BOLD}Installation complete!${NC}"
  echo ""
  echo "Next steps:"
  echo "  1. Set your Conductor server URL:"
  echo ""
  echo "     export CONDUCTOR_SERVER_URL=http://localhost:8080/api"
  echo ""
  echo "  2. (Optional) Set auth token if your server requires it:"
  echo ""
  echo "     export CONDUCTOR_AUTH_TOKEN=your-token-here"
  echo ""
  echo "  3. Start using it! Ask your agent:"
  echo ""
  echo '     "Create a workflow that fetches weather data and sends a notification"'
  echo ""
  echo -e "  Docs: ${BLUE}https://github.com/conductor-oss/conductor-skills${NC}"
  echo ""
}

main "$@"

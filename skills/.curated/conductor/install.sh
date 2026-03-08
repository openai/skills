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
  install.sh [--agent <name> | --all] [--global] [--project-dir <path>]
             [--upgrade] [--check] [--force] [--uninstall]

Options:
  --agent <name>        Install for a specific agent
  --all                 Auto-detect all agents and install for each
  --global              Install globally (available in all projects)
  --project-dir <path>  Target project directory (default: current directory)
  --upgrade             Check for newer version and upgrade installed agents
  --check               Dry run — show what would be installed, no changes
  --force               Overwrite existing files without prompting
  --uninstall           Remove installed skill files
  --version             Print version and exit
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
  # Auto-detect and install for all agents
  install.sh --all

  # Install globally for Codex CLI
  install.sh --agent codex --global

  # Check what would be installed
  install.sh --all --check

  # Upgrade all installed agents to latest
  install.sh --all --upgrade

  # Uninstall from all agents
  install.sh --all --uninstall

EOF
  exit 0
}

# ─────────────────────────────────────────────────────────────────────────────
# Agent detection
# ─────────────────────────────────────────────────────────────────────────────

detect_agents() {
  local detected=()

  command -v claude &>/dev/null && detected+=(claude)
  { command -v codex &>/dev/null || [ -d "$HOME/.codex" ]; } && detected+=(codex)
  { command -v gemini &>/dev/null || [ -d "$HOME/.gemini" ]; } && detected+=(gemini)
  [ -d "$HOME/.cursor" ] && detected+=(cursor)
  [ -d "$HOME/.codeium" ] && detected+=(windsurf)
  [ -d "$HOME/.cline" ] && detected+=(cline)
  command -v aider &>/dev/null && detected+=(aider)
  [ -d "$HOME/.config/github-copilot" ] && detected+=(copilot)
  { command -v q &>/dev/null || [ -d "$HOME/.amazonq" ]; } && detected+=(amazonq)
  command -v opencode &>/dev/null && detected+=(opencode)
  [ -d "$HOME/.roo" ] && detected+=(roo)
  { command -v amp &>/dev/null || [ -d "$HOME/.config/amp" ]; } && detected+=(amp)

  echo "${detected[@]}"
}

# ─────────────────────────────────────────────────────────────────────────────
# Manifest tracking
# ─────────────────────────────────────────────────────────────────────────────

GLOBAL_MANIFEST="$HOME/.conductor-skills/manifest.json"

get_manifest_path() {
  local is_global="$1"
  local project_dir="${2:-.}"
  if [ "$is_global" = "true" ]; then
    echo "$GLOBAL_MANIFEST"
  else
    echo "$project_dir/.conductor-skills/manifest.json"
  fi
}

ensure_manifest() {
  local manifest="$1"
  local dir
  dir=$(dirname "$manifest")
  mkdir -p "$dir"
  if [ ! -f "$manifest" ]; then
    echo '{"schema_version":1,"installations":{}}' > "$manifest"
  fi
}

read_manifest_version() {
  local manifest="$1"
  local agent="$2"

  if [ ! -f "$manifest" ]; then
    echo ""
    return
  fi

  python3 -c "
import json, sys
try:
    m = json.load(open('$manifest'))
    print(m.get('installations',{}).get('$agent',{}).get('version',''))
except: pass
" 2>/dev/null || echo ""
}

write_manifest_entry() {
  local manifest="$1"
  local agent="$2"
  local ver="$3"
  local mode="$4"
  local target_path="$5"

  ensure_manifest "$manifest"

  python3 -c "
import json, datetime
m = json.load(open('$manifest'))
now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
entry = m.setdefault('installations',{}).get('$agent',{})
m['installations']['$agent'] = {
    'version': '$ver',
    'installed_at': entry.get('installed_at', now),
    'updated_at': now,
    'mode': '$mode',
    'target_path': '$target_path'
}
json.dump(m, open('$manifest','w'), indent=2)
" 2>/dev/null
}

remove_manifest_entry() {
  local manifest="$1"
  local agent="$2"

  if [ ! -f "$manifest" ]; then
    return
  fi

  python3 -c "
import json
m = json.load(open('$manifest'))
m.get('installations',{}).pop('$agent', None)
json.dump(m, open('$manifest','w'), indent=2)
" 2>/dev/null
}

list_manifest_agents() {
  local manifest="$1"

  if [ ! -f "$manifest" ]; then
    echo ""
    return
  fi

  python3 -c "
import json
try:
    m = json.load(open('$manifest'))
    agents = list(m.get('installations',{}).keys())
    print(' '.join(agents))
except: pass
" 2>/dev/null || echo ""
}

# ─────────────────────────────────────────────────────────────────────────────
# Remote version check
# ─────────────────────────────────────────────────────────────────────────────

fetch_remote_version() {
  local remote_ver
  remote_ver=$(curl -sSfL "$REPO_BASE/VERSION" 2>/dev/null | tr -d '[:space:]') || true
  echo "$remote_ver"
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
# Global install paths
# ─────────────────────────────────────────────────────────────────────────────

supports_global() {
  local agent="$1"
  case "$agent" in
    claude|codex|gemini|cursor|windsurf|roo|amp|aider|opencode) return 0 ;;
    *) return 1 ;;
  esac
}

get_global_path() {
  local agent="$1"
  case "$agent" in
    claude)   echo "__claude__" ;;
    codex)    echo "${CODEX_HOME:-$HOME/.codex}/AGENTS.md" ;;
    cursor)   echo "$HOME/.cursor/skills/conductor/SKILL.md" ;;
    gemini)   echo "$HOME/.gemini/GEMINI.md" ;;
    windsurf) echo "$HOME/.codeium/windsurf/memories/global_rules.md" ;;
    roo)      echo "$HOME/.roo/rules/conductor.md" ;;
    amp)      echo "$HOME/.config/AGENTS.md" ;;
    aider)    echo "$HOME/.aider.conf.yml" ;;
    opencode) echo "$HOME/.config/opencode/skills/conductor/SKILL.md" ;;
  esac
}

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

# ─────────────────────────────────────────────────────────────────────────────
# Per-agent install logic
# ─────────────────────────────────────────────────────────────────────────────

install_claude() {
  if ! command -v claude &>/dev/null; then
    error "'claude' CLI not found. Install it first: npm install -g @anthropic-ai/claude-code"
    return 1
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

install_aider_to_dir() {
  local skill_dir="$1"
  local tmp_dir="$2"
  local config="$3"
  local read_prefix="$4"

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

  if [ -f "$config" ] && grep -q "conductor-skills" "$config" 2>/dev/null; then
    info "Aider config already references conductor-skills, skipping."
  else
    info "Adding read entries to $config ..."
    {
      echo ""
      echo "# Conductor Skills"
      echo "read:"
      for file in "${SKILL_FILES[@]}"; do
        echo "  - ${read_prefix}${file}"
      done
    } >> "$config"
    ok "Updated: $config"
  fi
}

# Install a single agent. Returns 0 on success, 1 on skip/failure.
install_for_agent() {
  local agent="$1"
  local project_dir="$2"
  local is_global="$3"
  local force="$4"
  local tmp_dir="$5"
  local assembled="$6"

  # Claude has its own install path
  if [ "$agent" = "claude" ]; then
    install_claude
    return $?
  fi

  if [ "$is_global" = "true" ]; then
    local target_path
    target_path=$(get_global_path "$agent")

    if [ "$agent" = "aider" ]; then
      install_aider_to_dir "$HOME/.conductor-skills" "$tmp_dir" "$HOME/.aider.conf.yml" "$HOME/.conductor-skills/"
    else
      install_to_file "$target_path" "$assembled" "$force"
    fi
  else
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
        install_aider_to_dir "$project_dir/.conductor-skills" "$tmp_dir" "$project_dir/.aider.conf.yml" ".conductor-skills/"
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
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Uninstall
# ─────────────────────────────────────────────────────────────────────────────

uninstall_agent() {
  local agent="$1"
  local project_dir="$2"
  local is_global="$3"

  if [ "$agent" = "claude" ]; then
    info "To remove the Conductor skill from Claude Code, run:"
    echo "  claude skill remove conductor"
    return
  fi

  local target
  if [ "$is_global" = "true" ]; then
    if [ "$agent" = "aider" ]; then
      local skill_dir="$HOME/.conductor-skills"
      if [ -d "$skill_dir" ]; then
        rm -rf "$skill_dir"
        ok "Removed: $skill_dir"
        info "Note: You may also want to remove the 'read:' entries from ~/.aider.conf.yml"
      else
        warn "Nothing to uninstall: $skill_dir not found"
      fi
      return
    fi
    target=$(get_global_path "$agent")
  else
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
  fi

  if [ -f "$target" ]; then
    rm -f "$target"
    ok "Removed: $target"
  else
    warn "Nothing to uninstall: $target not found"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Check mode (dry run)
# ─────────────────────────────────────────────────────────────────────────────

do_check() {
  local agents=("$@")

  local manifest
  manifest=$(get_manifest_path "true" "")

  echo ""
  echo -e "${BOLD}Detected agents:${NC}"
  if [ ${#agents[@]} -eq 0 ]; then
    warn "No AI coding agents detected on this system."
    return
  fi

  for agent in "${agents[@]}"; do
    local installed_ver
    installed_ver=$(read_manifest_version "$manifest" "$agent")
    local global_support="yes"
    supports_global "$agent" || global_support="no"

    if [ -n "$installed_ver" ]; then
      if [ "$installed_ver" = "$VERSION" ]; then
        echo -e "  ${GREEN}●${NC} $agent  v${installed_ver} (up to date)"
      else
        echo -e "  ${YELLOW}●${NC} $agent  v${installed_ver} → v${VERSION} (upgrade available)"
      fi
    else
      echo -e "  ${BLUE}●${NC} $agent  (not installed)  global: $global_support"
    fi
  done
  echo ""
}

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

main() {
  local agent=""
  local project_dir="."
  local force="false"
  local uninstall="false"
  local global="false"
  local all="false"
  local upgrade="false"
  local check="false"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --agent)       agent="$2"; shift 2 ;;
      --project-dir) project_dir="$2"; shift 2 ;;
      --global)      global="true"; shift ;;
      --all)         all="true"; shift ;;
      --upgrade)     upgrade="true"; shift ;;
      --check)       check="true"; shift ;;
      --force)       force="true"; shift ;;
      --uninstall)   uninstall="true"; shift ;;
      --version)     echo "v${VERSION}"; exit 0 ;;
      --help|-h)     usage ;;
      *)             error "Unknown option: $1"; usage ;;
    esac
  done

  # Require --agent or --all
  if [ -z "$agent" ] && [ "$all" != "true" ]; then
    error "Missing required --agent flag (or use --all)"
    echo ""
    usage
  fi

  # Resolve project dir to absolute path
  project_dir=$(cd "$project_dir" && pwd)

  echo ""
  echo -e "${BOLD}Conductor Skills Installer v${VERSION}${NC}"
  echo ""

  # Build agent list
  local agents=()
  if [ "$all" = "true" ]; then
    local detected
    detected=$(detect_agents)
    if [ -z "$detected" ]; then
      warn "No AI coding agents detected on this system."
      echo ""
      info "Supported agents: claude, codex, gemini, cursor, windsurf, cline,"
      info "  aider, copilot, amazonq, opencode, roo, amp"
      echo ""
      info "Install one of the above, then re-run this command."
      exit 0
    fi
    # shellcheck disable=SC2206
    agents=($detected)
    info "Detected agents: ${agents[*]}"
    echo ""
  else
    agent=$(echo "$agent" | tr '[:upper:]' '[:lower:]')
    case "$agent" in
      claude|codex|gemini|cursor|windsurf|cline|aider|copilot|amazonq|opencode|roo|amp) ;;
      *) error "Unknown agent: $agent"; echo ""; usage ;;
    esac
    agents=("$agent")
  fi

  # Check mode — dry run
  if [ "$check" = "true" ]; then
    do_check "${agents[@]}"
    exit 0
  fi

  # Determine manifest path
  local manifest
  if [ "$global" = "true" ] || [ "$all" = "true" ]; then
    manifest=$(get_manifest_path "true" "")
  else
    manifest=$(get_manifest_path "false" "$project_dir")
  fi

  # Handle uninstall
  if [ "$uninstall" = "true" ]; then
    for a in "${agents[@]}"; do
      local use_global="$global"
      if [ "$all" = "true" ] && supports_global "$a"; then
        use_global="true"
      fi
      info "Uninstalling ${BOLD}${a}${NC} ..."
      uninstall_agent "$a" "$project_dir" "$use_global"
      remove_manifest_entry "$manifest" "$a"
    done
    echo ""
    ok "Done!"
    return
  fi

  # Check for upgrade
  local target_version="$VERSION"
  if [ "$upgrade" = "true" ]; then
    info "Checking for updates..."
    local remote_ver
    remote_ver=$(fetch_remote_version)
    if [ -z "$remote_ver" ]; then
      warn "Could not check for updates (offline?). Using bundled v${VERSION}."
    elif [ "$remote_ver" != "$VERSION" ]; then
      info "Update available: v${VERSION} → v${remote_ver}"
      target_version="$remote_ver"
    else
      info "Already at latest version (v${VERSION})."
    fi
    echo ""
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

  # Install for each agent
  local installed_count=0
  local skipped_count=0

  for a in "${agents[@]}"; do
    echo ""

    # Determine if global for this agent
    local use_global="$global"
    if [ "$all" = "true" ]; then
      if supports_global "$a"; then
        use_global="true"
      else
        info "${BOLD}${a}${NC}: skipped (project-only install). Use --project-dir <path> to include."
        skipped_count=$((skipped_count + 1))
        continue
      fi
    fi

    # Validate global support for single-agent mode
    if [ "$use_global" = "true" ] && ! supports_global "$a"; then
      error "Global install is not supported for $a. Run from your project directory instead."
      continue
    fi

    # Idempotency check
    local installed_ver
    installed_ver=$(read_manifest_version "$manifest" "$a")
    if [ -n "$installed_ver" ] && [ "$installed_ver" = "$target_version" ] && [ "$force" != "true" ] && [ "$upgrade" != "true" ]; then
      ok "${a} already at v${installed_ver}, skipping."
      skipped_count=$((skipped_count + 1))
      continue
    fi

    if [ -n "$installed_ver" ] && [ "$installed_ver" != "$target_version" ]; then
      info "Upgrading ${BOLD}${a}${NC} from v${installed_ver} to v${target_version} ..."
    else
      info "Installing for ${BOLD}${a}${NC} ..."
    fi

    # Perform install
    if install_for_agent "$a" "$project_dir" "$use_global" "$force" "$tmp_dir" "$assembled"; then
      # Determine target path for manifest
      local target_path
      if [ "$use_global" = "true" ]; then
        target_path=$(get_global_path "$a")
      else
        target_path=$(get_target_path "$a" "$project_dir")
      fi
      local mode
      if [ "$use_global" = "true" ]; then mode="global"; else mode="project"; fi
      write_manifest_entry "$manifest" "$a" "$target_version" "$mode" "$target_path"
      installed_count=$((installed_count + 1))
    fi
  done

  echo ""
  echo -e "${GREEN}${BOLD}Done!${NC} Installed: ${installed_count}, Skipped: ${skipped_count}"
  echo ""
  echo "Next steps:"
  echo "  Ask your agent to connect to your Conductor server, e.g.:"
  echo ""
  echo '     "Connect to my Conductor server at http://localhost:8080/api"'
  echo ""
  echo -e "  Docs: ${BLUE}https://github.com/conductor-oss/conductor-skills${NC}"
  echo ""
}

main "$@"

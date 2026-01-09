#!/usr/bin/env bash
set -euo pipefail

die() {
  echo "project-notify: $1" >&2
  exit 2
}

trim() {
  local s="${1:-}"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf "%s" "$s"
}

to_lower() {
  printf "%s" "$1" | tr '[:upper:]' '[:lower:]'
}

usage() {
  cat >&2 <<'EOF'
Usage:
  project-notify.sh <message> [--level <info|success|warn|error>]
  project-notify.sh --message <message> [--level <info|success|warn|error>]

Behavior:
  - Derives title from PROJECT_PATH basename (preferred), else git root, else PWD basename.
  - Delegates to scripts/desktop-notify.sh.

Environment:
  PROJECT_PATH                  Used to derive the title (preferred)
  CODEX_DESKTOP_NOTIFY=0        Disable notifications (default: enabled)
  CODEX_DESKTOP_NOTIFY_HINTS=1  Print install hints when backend missing (default: disabled)
EOF
}

message=""
level="success"

while [[ $# -gt 0 ]]; do
  case "${1:-}" in
    --message)
      message="${2:-}"
      [[ -n "$message" ]] || die "Missing value for --message"
      shift 2
      ;;
    --level)
      level="$(to_lower "$(trim "${2:-}")")"
      [[ -n "$level" ]] || die "Missing value for --level"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      if [[ -z "$message" ]]; then
        message="$1"
        shift
      else
        die "Unexpected argument: $1"
      fi
      ;;
  esac
done

if [[ -z "$message" && $# -gt 0 ]]; then
  message="$1"
  shift || true
fi

message="$(trim "$message")"
[[ -n "$message" ]] || die "Missing message"

case "$level" in
  info|success|warn|warning|error)
    ;;
  *)
    die "Invalid --level: $level (expected info|success|warn|error)"
    ;;
esac

self_path="${BASH_SOURCE[0]:-$0}"
self_dir="$(cd "$(dirname "$self_path")" >/dev/null 2>&1 && pwd -P || true)"
[[ -n "$self_dir" ]] || die "Unable to resolve script directory"

desktop_notify_abs=""
declare -a desktop_notify_candidates=()

desktop_notify_candidates+=("${self_dir%/}/desktop-notify.sh")

if [[ -n "${CODEX_HOME:-}" ]]; then
  desktop_notify_candidates+=("${CODEX_HOME%/}/skills/desktop-notify/scripts/desktop-notify.sh")
  desktop_notify_candidates+=("${CODEX_HOME%/}/scripts/desktop-notify.sh")
fi

for candidate in "${desktop_notify_candidates[@]}"; do
  if [[ -f "$candidate" ]]; then
    desktop_notify_abs="$candidate"
    break
  fi
done

[[ -n "$desktop_notify_abs" ]] || die "Missing desktop notifier (expected next to project-notify.sh)"

resolve_project_path_for_title() {
  local candidate
  candidate="$(trim "${PROJECT_PATH:-}")"
  if [[ -n "$candidate" ]]; then
    printf "%s" "$candidate"
    return 0
  fi

  if command -v git >/dev/null 2>&1; then
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      git rev-parse --show-toplevel 2>/dev/null || true
      return 0
    fi
  fi

  printf "%s" "${PWD:-.}"
}

project_path="$(resolve_project_path_for_title)"
title="$(basename "$project_path")"
title="$(trim "$title")"
if [[ -z "$title" || "$title" == "/" || "$title" == "." ]]; then
  title="project"
fi

if [[ -x "$desktop_notify_abs" ]]; then
  "$desktop_notify_abs" --title "$title" --message "$message" --level "$level" >/dev/null || true
else
  bash "$desktop_notify_abs" --title "$title" --message "$message" --level "$level" >/dev/null || true
fi

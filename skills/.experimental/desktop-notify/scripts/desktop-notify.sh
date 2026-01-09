#!/usr/bin/env bash
set -euo pipefail

die() {
  echo "desktop-notify: $1" >&2
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
  desktop-notify.sh --title <title> --message <message> [--level <info|success|warn|error>]

Behavior:
  - macOS: uses terminal-notifier (if installed)
  - Linux: uses notify-send (libnotify) (if installed)
  - Missing backend: no-op (optional one-line install hint to stderr)

Environment:
  CODEX_DESKTOP_NOTIFY=0   Disable notifications (default: enabled)
  CODEX_DESKTOP_NOTIFY_HINTS=1  Print install hints when backend missing (default: disabled)

Install hints:
  - macOS: brew install terminal-notifier
  - Linux (Debian/Ubuntu): sudo apt-get install libnotify-bin
  - Linux (Fedora): sudo dnf install libnotify
EOF
}

is_disabled_by_env() {
  local v
  v="$(to_lower "$(trim "${CODEX_DESKTOP_NOTIFY:-1}")")"
  case "$v" in
    0|false|no|off)
      return 0
      ;;
  esac
  return 1
}

are_hints_enabled() {
  local v
  v="$(to_lower "$(trim "${CODEX_DESKTOP_NOTIFY_HINTS:-0}")")"
  case "$v" in
    1|true|yes|on)
      return 0
      ;;
  esac
  return 1
}

title=""
message=""
level="info"

while [[ $# -gt 0 ]]; do
  case "${1:-}" in
    --title)
      title="${2:-}"
      [[ -n "$title" ]] || die "Missing value for --title"
      shift 2
      ;;
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
    *)
      die "Unknown argument: ${1}"
      ;;
  esac
done

[[ -n "$title" ]] || die "Missing --title"
[[ -n "$message" ]] || die "Missing --message"

case "$level" in
  info|success|warn|warning|error)
    ;;
  *)
    die "Invalid --level: $level (expected info|success|warn|error)"
    ;;
esac

if is_disabled_by_env; then
  exit 0
fi

os="$(uname -s 2>/dev/null || true)"

if [[ "$os" == "Darwin" ]]; then
  if command -v terminal-notifier >/dev/null 2>&1; then
    if terminal-notifier -title "$title" -message "$message" >/dev/null 2>&1; then
      exit 0
    fi
    exit 0
  fi

  if are_hints_enabled; then
    echo "desktop-notify: terminal-notifier not found (install: brew install terminal-notifier)" >&2
  fi
  exit 0
fi

if [[ "$os" == "Linux" ]]; then
  if command -v notify-send >/dev/null 2>&1; then
    urgency="normal"
    case "$level" in
      error)
        urgency="critical"
        ;;
      warn|warning)
        urgency="normal"
        ;;
    esac

    if notify-send -u "$urgency" "$title" "$message" >/dev/null 2>&1; then
      exit 0
    fi
    exit 0
  fi

  if are_hints_enabled; then
    echo "desktop-notify: notify-send not found (install: libnotify; e.g. apt-get install libnotify-bin)" >&2
  fi
  exit 0
fi

exit 0

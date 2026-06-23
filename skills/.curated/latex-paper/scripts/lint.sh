#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") <project-dir> [--main main.tex]

Examples:
  $(basename "$0") ./paper
  $(basename "$0") ./paper --main manuscript.tex
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

project_dir="$1"
shift
main_tex="main.tex"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --main)
      main_tex="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ ! -d "$project_dir" ]]; then
  echo "Project directory not found: $project_dir" >&2
  exit 1
fi

if [[ ! -f "$project_dir/$main_tex" ]]; then
  echo "Main TeX file not found: $project_dir/$main_tex" >&2
  exit 1
fi

status=0
mkdir -p "$project_dir/build"

if command -v chktex >/dev/null 2>&1; then
  echo "Running chktex..."
  set +e
  chktex -q -f'%f:%l:%c:%k:%n:%m\n' "$project_dir/$main_tex" | tee "$project_dir/build/chktex.log"
  chktex_status=${PIPESTATUS[0]}
  set -e
  if [[ $chktex_status -ne 0 ]]; then
    status=1
  fi
else
  echo "chktex not found. Skipping chktex pass."
fi

echo "Checking duplicate labels..."
dup_labels="$(
  rg -No -h --glob '*.tex' '\\label\\{[^}]+\\}' "$project_dir" 2>/dev/null \
    | sed -E 's/^\\\\label[{]([^}]+)[}]$/\\1/' \
    | sort \
    | uniq -d \
    || true
)"
if [[ -n "$dup_labels" ]]; then
  echo "Duplicate labels detected:"
  echo "$dup_labels"
  status=1
fi

echo "Checking TODO/FIXME markers..."
if rg -n --glob '*.tex' 'TODO|FIXME' "$project_dir" >/dev/null 2>&1; then
  rg -n --glob '*.tex' 'TODO|FIXME' "$project_dir"
fi

if [[ $status -eq 0 ]]; then
  echo "Lint checks passed."
else
  echo "Lint checks found issues."
fi

exit "$status"

#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") <project-dir> [--main main.tex] [--engine pdflatex|xelatex|lualatex]

Examples:
  $(basename "$0") ./paper
  $(basename "$0") ./paper --main manuscript.tex --engine xelatex
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

project_dir="$1"
shift

main_tex="main.tex"
engine="pdflatex"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --main)
      main_tex="${2:-}"
      shift 2
      ;;
    --engine)
      engine="${2:-}"
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

if ! command -v latexmk >/dev/null 2>&1; then
  echo "latexmk is required but not installed." >&2
  echo "Install TeX Live or MacTeX and ensure latexmk is in PATH." >&2
  exit 1
fi

engine_flag="-pdf"
case "$engine" in
  pdflatex)
    engine_flag="-pdf"
    ;;
  xelatex)
    engine_flag="-xelatex"
    ;;
  lualatex)
    engine_flag="-lualatex"
    ;;
  *)
    echo "Unsupported engine: $engine" >&2
    exit 1
    ;;
esac

mkdir -p "$project_dir/build"
log_file="$project_dir/build/compile.log"

set +e
(
  cd "$project_dir"
  latexmk "$engine_flag" -interaction=nonstopmode -file-line-error -halt-on-error -outdir=build "$main_tex"
) 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
set -e

if [[ $status -ne 0 ]]; then
  echo
  echo "Compile failed. Key diagnostics:"
  grep -E '^!|^[^:]+:[0-9]+:|LaTeX Warning:|Package .* Warning:' "$log_file" | head -n 40 || true
  echo
  echo "Full log: $log_file"
  exit "$status"
fi

pdf_name="${main_tex%.tex}.pdf"
echo "Compile succeeded: $project_dir/build/$pdf_name"
echo "Log file: $log_file"

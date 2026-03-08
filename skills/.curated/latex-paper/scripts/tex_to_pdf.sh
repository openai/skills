#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") <file.tex> [--engine pdflatex|xelatex|lualatex] [--output-dir DIR] [--clean]

Examples:
  $(basename "$0") ./paper/main.tex
  $(basename "$0") ./paper/main.tex --engine xelatex --output-dir ./paper/dist
USAGE
}

if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

input_tex="$1"
shift

engine="pdflatex"
output_dir=""
clean_aux="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --engine)
      engine="${2:-}"
      shift 2
      ;;
    --output-dir)
      output_dir="${2:-}"
      shift 2
      ;;
    --clean)
      clean_aux="true"
      shift
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

if [[ ! -f "$input_tex" ]]; then
  echo "TeX file not found: $input_tex" >&2
  exit 1
fi

if [[ "${input_tex##*.}" != "tex" ]]; then
  echo "Input must be a .tex file: $input_tex" >&2
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

input_abs="$(cd "$(dirname "$input_tex")" && pwd)/$(basename "$input_tex")"
project_dir="$(dirname "$input_abs")"
main_tex="$(basename "$input_abs")"

if [[ -z "$output_dir" ]]; then
  output_dir="$project_dir/build"
fi
mkdir -p "$output_dir"
output_abs="$(cd "$output_dir" && pwd)"

log_file="$output_abs/tex_to_pdf.log"

set +e
(
  cd "$project_dir"
  latexmk "$engine_flag" -interaction=nonstopmode -file-line-error -halt-on-error -outdir="$output_abs" "$main_tex"
) 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
set -e

if [[ $status -ne 0 ]]; then
  echo
  echo "Conversion failed. Key diagnostics:"
  grep -E '^!|^[^:]+:[0-9]+:|LaTeX Warning:|Package .* Warning:' "$log_file" | head -n 40 || true
  echo
  echo "Full log: $log_file"
  exit "$status"
fi

if [[ "$clean_aux" == "true" ]]; then
  (
    cd "$project_dir"
    latexmk -c -outdir="$output_abs" "$main_tex" >/dev/null 2>&1 || true
  )
fi

pdf_name="${main_tex%.tex}.pdf"
pdf_path="$output_abs/$pdf_name"

if [[ ! -f "$pdf_path" ]]; then
  echo "Conversion reported success, but PDF not found: $pdf_path" >&2
  exit 1
fi

echo "PDF generated: $pdf_path"
echo "Log file: $log_file"

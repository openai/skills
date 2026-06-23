#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") <output-dir> [--template article|ieeetran|acmart] [--title TITLE] [--author AUTHOR] [--date DATE]

Examples:
  $(basename "$0") /tmp/my-paper
  $(basename "$0") /tmp/my-paper --template ieeetran --title "My Paper" --author "A. Researcher"
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

output_dir="$1"
shift

template="article"
title="Untitled Paper"
author="Anonymous"
date_value="\\today"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --template)
      template="${2:-}"
      shift 2
      ;;
    --title)
      title="${2:-}"
      shift 2
      ;;
    --author)
      author="${2:-}"
      shift 2
      ;;
    --date)
      date_value="${2:-}"
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

case "$template" in
  article|ieeetran|acmart)
    ;;
  *)
    echo "Unsupported template: $template" >&2
    exit 1
    ;;
esac

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "${script_dir}/.." && pwd)"
template_dir="${skill_dir}/assets/templates/${template}"

if [[ ! -d "$template_dir" ]]; then
  echo "Template directory not found: $template_dir" >&2
  exit 1
fi

if [[ -e "$output_dir" && -n "$(ls -A "$output_dir" 2>/dev/null || true)" ]]; then
  echo "Output directory exists and is not empty: $output_dir" >&2
  exit 1
fi

mkdir -p "$output_dir"
cp -R "$template_dir/." "$output_dir/"

main_tex="${output_dir}/main.tex"
if [[ -f "$main_tex" ]]; then
  escape_sed() {
    printf '%s' "$1" | sed -e 's/[\\/&]/\\&/g'
  }

  title_escaped="$(escape_sed "$title")"
  author_escaped="$(escape_sed "$author")"
  date_escaped="$(escape_sed "$date_value")"

  sed -i \
    -e "s/__TITLE__/${title_escaped}/g" \
    -e "s/__AUTHOR__/${author_escaped}/g" \
    -e "s/__DATE__/${date_escaped}/g" \
    "$main_tex"
fi

echo "Created LaTeX project: $output_dir"
echo "Template: $template"

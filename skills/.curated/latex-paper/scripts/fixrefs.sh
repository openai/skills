#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage:
  $(basename "$0") <project-dir>

Checks:
  - unresolved label references (\\ref, \\eqref, \\autoref, \\cref, \\Cref, \\pageref)
  - missing bibliography keys for \\cite* commands
USAGE
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

project_dir="$1"
if [[ ! -d "$project_dir" ]]; then
  echo "Project directory not found: $project_dir" >&2
  exit 1
fi

if ! command -v rg >/dev/null 2>&1; then
  echo "ripgrep (rg) is required." >&2
  exit 1
fi

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

labels_file="$tmp_dir/labels.txt"
ref_targets_file="$tmp_dir/ref_targets.txt"
missing_labels_file="$tmp_dir/missing_labels.txt"

cite_targets_file="$tmp_dir/cite_targets.txt"
bib_keys_file="$tmp_dir/bib_keys.txt"
missing_cites_file="$tmp_dir/missing_cites.txt"

rg -No --glob '*.tex' '\\label\{[^}]+\}' "$project_dir" \
  | sed -E 's/.*\\label\{([^}]+)\}.*/\1/' \
  | sort -u > "$labels_file" || true

rg -No --glob '*.tex' '\\(ref|eqref|autoref|cref|Cref|pageref)\{[^}]+\}' "$project_dir" \
  | sed -E 's/.*\{([^}]+)\}.*/\1/' \
  | sort -u > "$ref_targets_file" || true

comm -23 "$ref_targets_file" "$labels_file" > "$missing_labels_file" || true

rg -No --glob '*.tex' '\\cite[a-zA-Z*]*\{[^}]+\}' "$project_dir" \
  | sed -E 's/.*\{([^}]+)\}.*/\1/' \
  | tr ',' '\n' \
  | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' \
  | rg -v '^$' \
  | sort -u > "$cite_targets_file" || true

: > "$bib_keys_file"
while IFS= read -r bib_file; do
  rg -No '^@[a-zA-Z]+\{[^,]+' "$bib_file" \
    | sed -E 's/^@[a-zA-Z]+\{([^,]+).*/\1/' \
    | sort -u >> "$bib_keys_file" || true
done < <(rg --files "$project_dir" -g '*.bib' || true)
sort -u -o "$bib_keys_file" "$bib_keys_file"

comm -23 "$cite_targets_file" "$bib_keys_file" > "$missing_cites_file" || true

status=0

if [[ -s "$missing_labels_file" ]]; then
  echo "Missing label definitions for these references:"
  cat "$missing_labels_file"
  status=1
fi

if [[ -s "$missing_cites_file" ]]; then
  echo "Missing bibliography entries for these citation keys:"
  cat "$missing_cites_file"
  status=1
fi

if [[ $status -eq 0 ]]; then
  echo "No missing label/citation keys found."
fi

exit "$status"

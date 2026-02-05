#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Collect GitHub repository candidates from multiple search queries in parallel.

Usage:
  collect_github_repos.sh --queries-file <path> --output <path> [options]

Required:
  --queries-file <path>   Text file with one search query per line
  --output <path>         Output JSON file (array of repo objects)

Options:
  --per-query <n>         Max results per query (default: 30)
  --parallel <n>          Parallel workers (default: 6)
  --max-candidates <n>    Max deduped repos to hydrate (default: 100)
  --sort <field>          Search sort field (default: stars)
  --order <asc|desc>      Search sort order (default: desc)
  --no-hydrate            Skip per-repo details lookup
  --help                  Show this message

Notes:
  - Requires: gh, jq
  - Supports comments and blank lines in query file
EOF
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
}

hash_line() {
  if command -v shasum >/dev/null 2>&1; then
    printf '%s' "$1" | shasum -a 256 | awk '{print $1}'
  else
    printf '%s' "$1" | md5sum | awk '{print $1}'
  fi
}

if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

QUERIES_FILE=""
OUTPUT=""
PER_QUERY=30
PARALLEL=6
MAX_CANDIDATES=100
SORT="stars"
ORDER="desc"
HYDRATE=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --queries-file)
      QUERIES_FILE="${2:-}"
      shift 2
      ;;
    --output)
      OUTPUT="${2:-}"
      shift 2
      ;;
    --per-query)
      PER_QUERY="${2:-}"
      shift 2
      ;;
    --parallel)
      PARALLEL="${2:-}"
      shift 2
      ;;
    --max-candidates)
      MAX_CANDIDATES="${2:-}"
      shift 2
      ;;
    --sort)
      SORT="${2:-}"
      shift 2
      ;;
    --order)
      ORDER="${2:-}"
      shift 2
      ;;
    --no-hydrate)
      HYDRATE=0
      shift
      ;;
    --help|-h)
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

if [[ -z "$QUERIES_FILE" || -z "$OUTPUT" ]]; then
  echo "Both --queries-file and --output are required." >&2
  usage
  exit 1
fi

if [[ ! -f "$QUERIES_FILE" ]]; then
  echo "Queries file not found: $QUERIES_FILE" >&2
  exit 1
fi

require_cmd gh
require_cmd jq

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

SEARCH_DIR="$TMP_DIR/search"
DETAIL_DIR="$TMP_DIR/details"
mkdir -p "$SEARCH_DIR" "$DETAIL_DIR"

readarray -t QUERIES < <(grep -vE '^\s*($|#)' "$QUERIES_FILE")

if [[ "${#QUERIES[@]}" -eq 0 ]]; then
  echo "No valid queries found in: $QUERIES_FILE" >&2
  exit 1
fi

search_one() {
  local query="$1"
  local key
  key="$(hash_line "$query")"
  gh api -X GET search/repositories \
    -f q="$query" \
    -f per_page="$PER_QUERY" \
    -f page=1 \
    -f sort="$SORT" \
    -f order="$ORDER" \
    > "$SEARCH_DIR/$key.json"
}

export -f search_one hash_line
export SEARCH_DIR PER_QUERY SORT ORDER

printf '%s\0' "${QUERIES[@]}" \
  | xargs -0 -P "$PARALLEL" -I{} bash -c 'search_one "$1"' _ "{}"

MERGED_FILE="$TMP_DIR/merged.json"
jq -s '
  [ .[] | .items[]? ]
  | unique_by(.full_name)
  | sort_by(-(.stargazers_count // 0), -(.forks_count // 0))
' "$SEARCH_DIR"/*.json > "$MERGED_FILE"

if [[ "$HYDRATE" -eq 0 ]]; then
  mkdir -p "$(dirname "$OUTPUT")"
  cp "$MERGED_FILE" "$OUTPUT"
  echo "Wrote candidates to $OUTPUT"
  exit 0
fi

REPOS_FILE="$TMP_DIR/repos.txt"
jq -r '.[].full_name' "$MERGED_FILE" | head -n "$MAX_CANDIDATES" > "$REPOS_FILE"

if [[ ! -s "$REPOS_FILE" ]]; then
  echo "No repositories returned from search." >&2
  exit 1
fi

hydrate_one() {
  local full_name="$1"
  local safe_name
  safe_name="$(printf '%s' "$full_name" | tr '/:' '__')"
  gh api "repos/$full_name" > "$DETAIL_DIR/$safe_name.json"
}

export -f hydrate_one
export DETAIL_DIR

tr '\n' '\0' < "$REPOS_FILE" \
  | xargs -0 -P "$PARALLEL" -I{} bash -c 'hydrate_one "$1"' _ "{}"

mkdir -p "$(dirname "$OUTPUT")"
jq -s '[ .[] ]' "$DETAIL_DIR"/*.json > "$OUTPUT"

echo "Wrote $(jq 'length' "$OUTPUT") hydrated repositories to $OUTPUT"

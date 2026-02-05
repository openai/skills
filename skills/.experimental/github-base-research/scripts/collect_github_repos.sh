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
  --parallel <n>          Parallel workers (default: 4)
  --max-candidates <n>    Max deduped repos to hydrate (default: 100)
  --min-stars <n>         Minimum stars for candidates (default: 50)
  --include-forks         Include forked repositories (default: false)
  --safe-mode             Use conservative API settings (parallel=1, per-query<=25)
  --retries <n>           Retries for API calls (default: 4)
  --initial-backoff <n>   Initial retry delay in seconds (default: 2)
  --trim-description <n>  Max description chars in final output (default: 600)
  --sort <field>          Search sort field (default: stars)
  --order <asc|desc>      Search sort order (default: desc)
  --no-hydrate            Skip per-repo details lookup
  --help                  Show this message

Notes:
  - Requires: gh, jq
  - Supports comments and blank lines in query file
  - Compatible with macOS default Bash (3.2)
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

log() {
  printf '[collect] %s\n' "$*" >&2
}

if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

QUERIES_FILE=""
OUTPUT=""
PER_QUERY=30
PARALLEL=4
MAX_CANDIDATES=100
MIN_STARS=50
INCLUDE_FORKS=0
SAFE_MODE=0
RETRIES=4
INITIAL_BACKOFF=2
TRIM_DESCRIPTION=600
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
    --min-stars)
      MIN_STARS="${2:-}"
      shift 2
      ;;
    --include-forks)
      INCLUDE_FORKS=1
      shift
      ;;
    --safe-mode)
      SAFE_MODE=1
      shift
      ;;
    --retries)
      RETRIES="${2:-}"
      shift 2
      ;;
    --initial-backoff)
      INITIAL_BACKOFF="${2:-}"
      shift 2
      ;;
    --trim-description)
      TRIM_DESCRIPTION="${2:-}"
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

if [[ "$SAFE_MODE" -eq 1 ]]; then
  PARALLEL=1
  if [[ "$PER_QUERY" -gt 25 ]]; then
    PER_QUERY=25
  fi
  log "Safe mode enabled: parallel=${PARALLEL}, per-query=${PER_QUERY}"
fi

if [[ "$PARALLEL" -lt 1 ]]; then
  echo "--parallel must be >= 1" >&2
  exit 1
fi

if [[ "$RETRIES" -lt 1 ]]; then
  echo "--retries must be >= 1" >&2
  exit 1
fi

QUERIES=()
while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line%$'\r'}"
  if [[ "$line" =~ ^[[:space:]]*$ ]]; then
    continue
  fi
  if [[ "$line" =~ ^[[:space:]]*# ]]; then
    continue
  fi
  QUERIES+=("$line")
done < "$QUERIES_FILE"

if [[ "${#QUERIES[@]}" -eq 0 ]]; then
  echo "No valid queries found in: $QUERIES_FILE" >&2
  exit 1
fi

gh_api_retry() {
  local outfile="$1"
  shift

  local attempt=1
  local delay="$INITIAL_BACKOFF"
  local err_file="$TMP_DIR/gh-api-error.log"

  while true; do
    if gh api -H "Accept: application/vnd.github+json" "$@" > "$outfile" 2> "$err_file"; then
      return 0
    fi

    if [[ "$attempt" -ge "$RETRIES" ]]; then
      log "API request failed after ${attempt} attempts: gh api $*"
      cat "$err_file" >&2 || true
      return 1
    fi

    if grep -Eqi 'secondary rate limit|rate limit exceeded|abuse detection|Please wait a few minutes' "$err_file"; then
      log "Rate limit on attempt ${attempt}/${RETRIES}. Sleeping ${delay}s before retry."
    else
      log "API error on attempt ${attempt}/${RETRIES}. Sleeping ${delay}s before retry."
    fi

    sleep "$delay"
    delay=$((delay * 2))
    attempt=$((attempt + 1))
  done
}

search_one() {
  local query="$1"
  local key
  key="$(hash_line "$query")"
  gh_api_retry "$SEARCH_DIR/$key.json" \
    -X GET search/repositories \
    -f q="$query" \
    -f per_page="$PER_QUERY" \
    -f page=1 \
    -f sort="$SORT" \
    -f order="$ORDER"
}

hydrate_one() {
  local full_name="$1"
  local safe_name
  safe_name="$(printf '%s' "$full_name" | tr '/:' '__')"
  gh_api_retry "$DETAIL_DIR/$safe_name.json" "repos/$full_name"
}

export -f search_one hydrate_one hash_line gh_api_retry log
export SEARCH_DIR DETAIL_DIR TMP_DIR PER_QUERY SORT ORDER RETRIES INITIAL_BACKOFF

log "Running ${#QUERIES[@]} search queries with parallel=${PARALLEL}"
if ! printf '%s\0' "${QUERIES[@]}" \
  | xargs -0 -P "$PARALLEL" -I{} bash -c 'search_one "$1"' _ "{}"; then
  if [[ "$PARALLEL" -gt 1 ]]; then
    log "Parallel search run failed. Retrying search serially to avoid burst limits."
    for query in "${QUERIES[@]}"; do
      search_one "$query"
    done
  else
    exit 1
  fi
fi

MERGED_FILE="$TMP_DIR/merged.json"
jq -s --argjson min_stars "$MIN_STARS" --argjson include_forks "$INCLUDE_FORKS" '
  [ .[] | .items[]? ]
  | map(select((.archived // false) | not))
  | map(select((.stargazers_count // 0) >= $min_stars))
  | if $include_forks == 1 then . else map(select((.fork // false) | not)) end
  | unique_by(.full_name)
  | sort_by(
      -(.stargazers_count // 0),
      -(.forks_count // 0),
      -((.updated_at // "") | fromdateiso8601? // 0)
    )
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

repo_count="$(wc -l < "$REPOS_FILE" | tr -d ' ')"
log "Hydrating ${repo_count} repositories with parallel=${PARALLEL}"
if ! tr '\n' '\0' < "$REPOS_FILE" \
  | xargs -0 -P "$PARALLEL" -I{} bash -c 'hydrate_one "$1"' _ "{}"; then
  if [[ "$PARALLEL" -gt 1 ]]; then
    log "Parallel hydration run failed. Retrying hydration serially."
    while IFS= read -r full_name || [[ -n "$full_name" ]]; do
      [[ -z "$full_name" ]] && continue
      hydrate_one "$full_name"
    done < "$REPOS_FILE"
  else
    exit 1
  fi
fi

mkdir -p "$(dirname "$OUTPUT")"
jq -s --argjson desc_max "$TRIM_DESCRIPTION" '
[
  .[] | {
    full_name,
    name,
    html_url,
    description: (((.description // "") | tostring)[0:$desc_max]),
    language,
    topics: (.topics // []),
    stargazers_count: (.stargazers_count // 0),
    forks_count: (.forks_count // 0),
    watchers_count: (.watchers_count // 0),
    subscribers_count: (.subscribers_count // 0),
    open_issues_count: (.open_issues_count // 0),
    pushed_at,
    updated_at,
    created_at,
    default_branch,
    license,
    archived: (.archived // false),
    disabled: (.disabled // false),
    has_issues: (.has_issues // false),
    has_wiki: (.has_wiki // false),
    fork: (.fork // false)
  }
]
' "$DETAIL_DIR"/*.json > "$OUTPUT"

echo "Wrote $(jq 'length' "$OUTPUT") hydrated repositories to $OUTPUT"

#!/usr/bin/env bash
# =============================================================================
# common.sh - Shared utilities for the Apex Spec System
# =============================================================================
# Source this file in other scripts: source "$(dirname "$0")/common.sh"
# =============================================================================
# CREDIT NOTE: The 1st version of this file was taken directly from Github's Spec Kit
# =============================================================================

set -euo pipefail

# =============================================================================
# CONFIGURATION
# =============================================================================

SPEC_SYSTEM_DIR="${SPEC_SYSTEM_DIR:-.spec_system}"
STATE_FILE="${SPEC_SYSTEM_DIR}/state.json"
SPECS_DIR="${SPECS_DIR:-${SPEC_SYSTEM_DIR}/specs}"

# =============================================================================
# COLORS AND LOGGING
# =============================================================================

# Colors (only if terminal supports it)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    NC=''
fi

log_info() {
    # Use printf for portability and to avoid echo option edge-cases (e.g. "-n").
    printf '%b\n' "${BLUE}[INFO]${NC} $*"
}

log_success() {
    printf '%b\n' "${GREEN}[SUCCESS]${NC} $*"
}

log_warning() {
    printf '%b\n' "${YELLOW}[WARNING]${NC} $*"
}

log_error() {
    printf '%b\n' "${RED}[ERROR]${NC} $*" >&2
}

log_debug() {
    if [[ "${DEBUG:-0}" == "1" ]]; then
        printf '%b\n' "${CYAN}[DEBUG]${NC} $*"
    fi
}

# =============================================================================
# STRING HELPERS
# =============================================================================

trim() {
    local s="${1:-}"
    # Remove leading whitespace
    s="${s#"${s%%[![:space:]]*}"}"
    # Remove trailing whitespace
    s="${s%"${s##*[![:space:]]}"}"
    printf '%s' "$s"
}

# =============================================================================
# JSON OPERATIONS (requires jq)
# =============================================================================

check_jq() {
    if ! command -v jq &>/dev/null; then
        log_error "jq is required but not installed. Install with: apt install jq"
        return 1
    fi
}

json_get() {
    local file="$1"
    local path="$2"

    check_jq || return 1

    if [[ ! -f "$file" ]]; then
        log_error "File not found: $file"
        return 1
    fi

    jq -r "$path" -- "$file"
}

json_set() {
    local file="$1"
    local path="$2"
    local value="$3"

    check_jq || return 1

    if [[ ! -f "$file" ]]; then
        log_error "File not found: $file"
        return 1
    fi

    local tmp_file
    tmp_file=$(mktemp)

    if jq "$path = $value" -- "$file" >"$tmp_file"; then
        if mv -- "$tmp_file" "$file"; then
            return 0
        fi
        local rc=$?
        rm -f -- "$tmp_file"
        return $rc
    fi

    local rc=$?
    rm -f -- "$tmp_file"
    return $rc
}

json_append_array() {
    local file="$1"
    local path="$2"
    local value="$3"

    check_jq || return 1

    local tmp_file
    tmp_file=$(mktemp)

    if jq "$path += [$value]" -- "$file" >"$tmp_file"; then
        if mv -- "$tmp_file" "$file"; then
            return 0
        fi
        local rc=$?
        rm -f -- "$tmp_file"
        return $rc
    fi

    local rc=$?
    rm -f -- "$tmp_file"
    return $rc
}

validate_json() {
    local file="$1"

    check_jq || return 1

    if jq empty -- "$file" 2>/dev/null; then
        return 0
    else
        log_error "Invalid JSON in $file"
        return 1
    fi
}

# =============================================================================
# SESSION ID PARSING
# =============================================================================
# Session ID format: phaseNN-sessionNN[x]-name
# Examples:
#   phase00-session01-project-setup
#   phase01-session08b-refinements

is_valid_identifier() {
    local name="${1:-}"
    # Valid bash identifier: [a-zA-Z_][a-zA-Z0-9_]*
    # Use glob matching (not regex) to avoid clobbering BASH_REMATCH.
    [[ -n "$name" ]] || return 1
    [[ "$name" == [a-zA-Z_]* ]] || return 1
    [[ "$name" != *[!a-zA-Z0-9_]* ]] || return 1
    return 0
}

parse_session_id() {
    local session_id="$1"
    local phase_var="${2:-}"
    local session_var="${3:-}"
    local suffix_var="${4:-}"
    local name_var="${5:-}"

    # Regex: phase([0-9]{2})-session([0-9]{2})([a-z])?-(.+)
    if [[ "$session_id" =~ ^phase([0-9]{2})-session([0-9]{2})([a-z])?-(.+)$ ]]; then
        # Capture values immediately so helper calls below can't clobber BASH_REMATCH.
        local phase_val="${BASH_REMATCH[1]}"
        local session_val="${BASH_REMATCH[2]}"
        local suffix_val="${BASH_REMATCH[3]}"
        local name_val="${BASH_REMATCH[4]}"

        if [[ -n "$phase_var" ]]; then
            is_valid_identifier "$phase_var" || {
                log_error "Invalid variable name: $phase_var"
                return 1
            }
            printf -v "$phase_var" '%s' "$phase_val"
        fi
        if [[ -n "$session_var" ]]; then
            is_valid_identifier "$session_var" || {
                log_error "Invalid variable name: $session_var"
                return 1
            }
            printf -v "$session_var" '%s' "$session_val"
        fi
        if [[ -n "$suffix_var" ]]; then
            is_valid_identifier "$suffix_var" || {
                log_error "Invalid variable name: $suffix_var"
                return 1
            }
            printf -v "$suffix_var" '%s' "$suffix_val"
        fi
        if [[ -n "$name_var" ]]; then
            is_valid_identifier "$name_var" || {
                log_error "Invalid variable name: $name_var"
                return 1
            }
            printf -v "$name_var" '%s' "$name_val"
        fi
        return 0
    else
        log_error "Invalid session ID format: $session_id"
        return 1
    fi
}

get_phase_from_session_id() {
    local session_id="$1"
    local phase
    parse_session_id "$session_id" phase && echo "$phase"
}

get_session_number_from_id() {
    local session_id="$1"
    local session
    parse_session_id "$session_id" "" session && echo "$session"
}

get_session_suffix_from_id() {
    local session_id="$1"
    local suffix
    parse_session_id "$session_id" "" "" suffix && echo "$suffix"
}

get_session_name_from_id() {
    local session_id="$1"
    local name
    parse_session_id "$session_id" "" "" "" name && echo "$name"
}

build_session_id() {
    local phase="$1"
    local session="$2"
    local name="$3"
    local suffix="${4:-}"

    # Zero-pad phase and session
    printf "phase%02d-session%02d%s-%s" "$phase" "$session" "$suffix" "$name"
}

# Build session reference (e.g., S0103 for Phase 01, Session 03)
build_session_ref() {
    local phase="$1"
    local session="$2"

    printf "S%02d%02d" "$phase" "$session"
}

# =============================================================================
# STATE QUERIES
# =============================================================================

get_current_phase() {
    json_get "$STATE_FILE" '.current_phase'
}

get_current_session() {
    json_get "$STATE_FILE" '.current_session'
}

get_project_name() {
    json_get "$STATE_FILE" '.project_name'
}

get_completed_sessions() {
    # Handle both string entries ("phase00-session01-name") and
    # object entries ({"id": "phase00-session01-name", "package": "apps/web"}).
    # Always returns normalized session IDs, one per line.
    check_jq || return 1
    jq -r '.completed_sessions[] |
        if type == "object" then .id else . end' -- "$STATE_FILE" 2>/dev/null || true
}

get_completed_sessions_count() {
    json_get "$STATE_FILE" '.completed_sessions | length'
}

is_session_completed() {
    local session_id="$1"
    local completed
    completed=$(get_completed_sessions)

    if grep -Fxq -- "$session_id" <<<"$completed"; then
        return 0
    else
        return 1
    fi
}

# Check if session number is completed (handles suffixes like session08b)
is_session_number_completed() {
    local session_num="$1"
    local phase="${2:-$(get_current_phase)}"
    local completed
    completed=$(get_completed_sessions)

    # Match any session with this number (with or without suffix)
    local pattern
    pattern=$(printf "phase%02d-session%02d" "$phase" "$session_num")

    if grep -q "^${pattern}" <<<"$completed"; then
        return 0
    else
        return 1
    fi
}

get_phase_status() {
    local phase="$1"
    json_get "$STATE_FILE" ".phases[\"$phase\"].status"
}

get_phase_name() {
    local phase="$1"
    json_get "$STATE_FILE" ".phases[\"$phase\"].name"
}

get_phase_session_count() {
    local phase="$1"
    json_get "$STATE_FILE" ".phases[\"$phase\"].session_count"
}

# =============================================================================
# STATE UPDATES
# =============================================================================

set_current_session() {
    local session_id="$1"
    json_set "$STATE_FILE" '.current_session' "\"$session_id\""
}

clear_current_session() {
    json_set "$STATE_FILE" '.current_session' 'null'
}

add_completed_session() {
    local session_id="$1"
    local package_path="${2:-}"

    local monorepo_flag
    monorepo_flag=$(get_monorepo_flag)

    if [[ "$monorepo_flag" == "true" ]]; then
        # Object form: { "id": "...", "package": "..." | null }
        local entry
        if [[ -n "$package_path" && "$package_path" != "null" ]]; then
            entry=$(jq -n --arg id "$session_id" --arg pkg "$package_path" \
                '{"id": $id, "package": $pkg}')
        else
            entry=$(jq -n --arg id "$session_id" '{"id": $id, "package": null}')
        fi
        json_append_array "$STATE_FILE" '.completed_sessions' "$entry"
    else
        # String form (classic single-repo behavior)
        json_append_array "$STATE_FILE" '.completed_sessions' "\"$session_id\""
    fi
}

set_phase_status() {
    local phase="$1"
    local status="$2"
    json_set "$STATE_FILE" ".phases[\"$phase\"].status" "\"$status\""
}

# =============================================================================
# MONOREPO STATE QUERIES
# =============================================================================

# Returns "true", "false", or "null" (unknown/absent).
get_monorepo_flag() {
    check_jq || return 1
    local val
    val=$(jq -r 'if .monorepo == true then "true"
                 elif .monorepo == false then "false"
                 else "null" end' -- "$STATE_FILE" 2>/dev/null)
    echo "${val:-null}"
}

# Returns the packages array as compact JSON. Empty array if absent.
get_packages() {
    check_jq || return 1
    jq -c '.packages // []' -- "$STATE_FILE" 2>/dev/null || echo "[]"
}

# Given a package name, return its path (e.g., "apps/web").
get_package_path() {
    local name="$1"
    check_jq || return 1
    jq -r --arg name "$name" \
        '(.packages // []) | map(select(.name == $name)) | .[0].path // empty' \
        -- "$STATE_FILE" 2>/dev/null
}

# Given a relative path, return the full package JSON object.
get_package_by_path() {
    local path="$1"
    check_jq || return 1
    jq -c --arg path "$path" \
        '(.packages // []) | map(select(.path == $path)) | .[0] // empty' \
        -- "$STATE_FILE" 2>/dev/null
}

# Return completed session IDs for a specific package (or cross-cutting if empty/null).
get_sessions_for_package() {
    local package_path="${1:-}"
    check_jq || return 1

    if [[ -z "$package_path" || "$package_path" == "null" ]]; then
        # Cross-cutting sessions: objects with null package, or plain strings
        jq -r '.completed_sessions[] |
            if type == "object" then
                (if .package == null then .id else empty end)
            else . end' -- "$STATE_FILE" 2>/dev/null || true
    else
        # Sessions scoped to a specific package
        jq -r --arg pkg "$package_path" '.completed_sessions[] |
            if type == "object" then
                (if .package == $pkg then .id else empty end)
            else empty end' -- "$STATE_FILE" 2>/dev/null || true
    fi
}

# =============================================================================
# MONOREPO DETECTION
# =============================================================================

# Check if the project is a monorepo by looking for workspace indicators.
# Returns JSON: { "detected": bool, "indicator": string|null, "packages": [...] }
detect_monorepo() {
    check_jq || return 1

    local detected="false"
    local indicator=""

    # Check workspace indicators in priority order
    if [[ -f "pnpm-workspace.yaml" ]]; then
        detected="true"
        indicator="pnpm-workspace.yaml"
    elif [[ -f "package.json" ]] && jq -e '.workspaces' -- "package.json" &>/dev/null; then
        detected="true"
        indicator="package.json workspaces"
    elif [[ -f "turbo.json" ]]; then
        detected="true"
        indicator="turbo.json"
    elif [[ -f "nx.json" ]]; then
        detected="true"
        indicator="nx.json"
    elif [[ -f "Cargo.toml" ]] && grep -q '^\[workspace\]' "Cargo.toml" 2>/dev/null; then
        detected="true"
        indicator="Cargo.toml workspace"
    elif [[ -f "go.work" ]]; then
        detected="true"
        indicator="go.work"
    elif [[ -f "lerna.json" ]]; then
        detected="true"
        indicator="lerna.json"
    fi

    if [[ "$detected" == "true" ]]; then
        local pkgs
        pkgs=$(detect_packages)
        jq -n --arg indicator "$indicator" --argjson packages "$pkgs" \
            '{"detected": true, "indicator": $indicator, "packages": $packages}'
    else
        jq -n '{"detected": false, "indicator": null, "packages": []}'
    fi
}

# Enumerate packages in a monorepo.
# Returns JSON array of { name, path, stack_hint }.
detect_packages() {
    check_jq || return 1

    local packages="[]"
    local -a pkg_globs=()
    local require_manifest=false

    # Extract workspace globs from config files
    if [[ -f "pnpm-workspace.yaml" ]]; then
        while IFS= read -r g; do
            [[ -n "$g" ]] && pkg_globs+=("$g")
        done < <(_extract_pnpm_globs)
    elif [[ -f "package.json" ]] && jq -e '.workspaces' -- "package.json" &>/dev/null; then
        while IFS= read -r g; do
            [[ -n "$g" ]] && pkg_globs+=("$g")
        done < <(_extract_npm_globs)
    elif [[ -f "Cargo.toml" ]] && grep -q '^\[workspace\]' "Cargo.toml" 2>/dev/null; then
        while IFS= read -r g; do
            [[ -n "$g" ]] && pkg_globs+=("$g")
        done < <(_extract_cargo_members)
    elif [[ -f "go.work" ]]; then
        while IFS= read -r g; do
            [[ -n "$g" ]] && pkg_globs+=("$g")
        done < <(_extract_go_dirs)
    fi

    # Fallback: scan common monorepo directories (require manifest evidence)
    if [[ ${#pkg_globs[@]} -eq 0 ]]; then
        pkg_globs=("apps/*" "packages/*" "libs/*" "services/*" "modules/*")
        require_manifest=true
    fi

    # Expand globs and build package list
    local prev_nullglob
    prev_nullglob=$(shopt -p nullglob 2>/dev/null || echo "shopt -u nullglob")
    shopt -s nullglob

    for glob in "${pkg_globs[@]}"; do
        for dir in $glob; do
            [[ -d "$dir" ]] || continue
            if [[ "$require_manifest" == true ]]; then
                _has_package_manifest "$dir" || continue
            fi

            local name
            name=$(basename "$dir")
            local stack
            stack=$(_detect_stack_hint "$dir")

            packages=$(echo "$packages" | jq \
                --arg name "$name" \
                --arg path "$dir" \
                --arg stack "$stack" \
                '. += [{"name": $name, "path": $path, "stack_hint": $stack}]')
        done
    done

    eval "$prev_nullglob"
    echo "$packages"
}

# Resolve which package is active based on explicit flag or CWD inference.
# Returns: compact JSON package object, or "null".
resolve_package_context() {
    local explicit_package="${1:-}"
    check_jq || return 1

    local monorepo_flag
    monorepo_flag=$(get_monorepo_flag)

    # Not a monorepo -- no package context
    if [[ "$monorepo_flag" != "true" ]]; then
        echo "null"
        return 0
    fi

    # Priority 1: Explicit --package argument
    if [[ -n "$explicit_package" && "$explicit_package" != "null" ]]; then
        local pkg
        pkg=$(get_package_by_path "$explicit_package")
        if [[ -n "$pkg" ]]; then
            echo "$pkg"
        else
            # Path not in packages array; return minimal info
            jq -n --arg path "$explicit_package" \
                '{"name": ($path | split("/") | last), "path": $path,
                  "type": "unknown", "stack": "unknown"}'
        fi
        return 0
    fi

    # Priority 2: CWD inference
    local cwd repo_root rel_cwd
    cwd=$(pwd)
    repo_root=$(cd "$(dirname "$STATE_FILE")/.." 2>/dev/null && pwd)
    rel_cwd="${cwd#"${repo_root}"/}"

    # CWD is repo root (prefix not stripped) -- ambiguous
    if [[ "$rel_cwd" == "$cwd" || -z "$rel_cwd" ]]; then
        echo "null"
        return 0
    fi

    # Find the longest matching package path
    local packages_json
    packages_json=$(get_packages)
    echo "$packages_json" | jq -c --arg cwd "$rel_cwd" \
        '[.[] | select(($cwd == .path) or ($cwd | startswith(.path + "/")))]
         | sort_by(.path | length) | reverse | .[0] // null'
}

# --- Internal helpers for monorepo detection ---

_has_package_manifest() {
    local dir="$1"
    [[ -f "$dir/package.json" ]] \
        || [[ -f "$dir/Cargo.toml" ]] \
        || [[ -f "$dir/go.mod" ]] \
        || [[ -f "$dir/pyproject.toml" ]] \
        || [[ -f "$dir/setup.py" ]]
}

_detect_stack_hint() {
    local dir="$1"
    if [[ -f "$dir/tsconfig.json" ]] || compgen -G "$dir/tsconfig.*.json" >/dev/null 2>&1; then
        echo "TypeScript"
    elif [[ -f "$dir/package.json" ]]; then
        echo "JavaScript"
    elif [[ -f "$dir/Cargo.toml" ]]; then
        echo "Rust"
    elif [[ -f "$dir/go.mod" ]]; then
        echo "Go"
    elif [[ -f "$dir/pyproject.toml" ]] || [[ -f "$dir/setup.py" ]] || [[ -f "$dir/requirements.txt" ]]; then
        echo "Python"
    elif [[ -f "$dir/Gemfile" ]]; then
        echo "Ruby"
    elif [[ -f "$dir/pom.xml" ]] || [[ -f "$dir/build.gradle" ]] || [[ -f "$dir/build.gradle.kts" ]]; then
        echo "Java"
    else
        echo "unknown"
    fi
}

# Parse package globs from pnpm-workspace.yaml
_extract_pnpm_globs() {
    local in_packages=false
    while IFS= read -r line; do
        local trimmed
        trimmed=$(trim "$line")
        if [[ "$trimmed" == "packages:" ]]; then
            in_packages=true
            continue
        fi
        if [[ "$in_packages" == true ]]; then
            # End of list: non-list, non-empty line
            if [[ -n "$trimmed" && "$trimmed" != -* ]]; then
                break
            fi
            if [[ "$trimmed" == "- "* ]]; then
                local val="${trimmed#- }"
                val=$(trim "$val")
                # Remove surrounding quotes
                val="${val%\"}"
                val="${val#\"}"
                val="${val%\'}"
                val="${val#\'}"
                [[ -n "$val" ]] && printf '%s\n' "$val"
            fi
        fi
    done <"pnpm-workspace.yaml"
}

# Parse workspace globs from package.json (npm/yarn format)
_extract_npm_globs() {
    jq -r '.workspaces |
        if type == "array" then .[]
        elif type == "object" then (.packages // [])[]
        else empty end' -- "package.json" 2>/dev/null
}

# Parse workspace members from Cargo.toml
_extract_cargo_members() {
    sed -n '/^\[workspace\]/,/^\[/{
        /members/,/\]/{
            s/.*"\([^"]*\)".*/\1/p
        }
    }' "Cargo.toml" 2>/dev/null
}

# Parse use directives from go.work
_extract_go_dirs() {
    local in_use=false
    while IFS= read -r line; do
        local trimmed
        trimmed=$(trim "$line")
        if [[ "$trimmed" == "use ("* ]]; then
            in_use=true
            continue
        fi
        if [[ "$in_use" == true ]]; then
            [[ "$trimmed" == ")" ]] && {
                in_use=false
                continue
            }
            trimmed="${trimmed#./}"
            [[ -n "$trimmed" ]] && printf '%s\n' "$trimmed"
        elif [[ "$trimmed" == use\ ./* ]]; then
            local dir="${trimmed#use ./}"
            dir=$(trim "$dir")
            [[ -n "$dir" ]] && printf '%s\n' "$dir"
        fi
    done <"go.work" 2>/dev/null
}

# =============================================================================
# FILE VALIDATION
# =============================================================================

validate_ascii() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        log_error "File not found: $file"
        return 1
    fi

    # Check for non-ASCII characters (bytes > 127) using POSIX-compatible grep
    # LC_ALL=C ensures byte-by-byte comparison; [^[:print:][:space:]] catches
    # non-printable/non-whitespace chars including non-ASCII
    if LC_ALL=C grep -q '[^[:print:][:space:]]' -- "$file" 2>/dev/null; then
        log_error "Non-ASCII characters found in: $file"
        return 1
    fi

    # Check for CRLF line endings (carriage return)
    if grep -q "$(printf '\r')" -- "$file" 2>/dev/null; then
        log_error "CRLF line endings found in: $file"
        return 1
    fi

    return 0
}

find_non_ascii() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        log_error "File not found: $file"
        return 1
    fi

    # Show non-ASCII characters with line numbers using POSIX-compatible grep
    LC_ALL=C grep -n '[^[:print:][:space:]]' -- "$file" 2>/dev/null || true
}

validate_all_files() {
    local dir="${1:-.}"
    local errors=0

    while IFS= read -r -d '' file; do
        if ! validate_ascii "$file"; then
            ((errors++)) || true
        fi
    done < <(find "$dir" -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.json" -o -name "*.sh" \) -print0)

    if [[ $errors -gt 0 ]]; then
        log_error "Found $errors files with encoding issues"
        return 1
    fi

    log_success "All files pass ASCII validation"
    return 0
}

# =============================================================================
# DIRECTORY OPERATIONS
# =============================================================================

ensure_dir() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        mkdir -p -- "$dir"
        log_info "Created directory: $dir"
    fi
}

get_session_dir() {
    local session_id="$1"
    echo "${SPECS_DIR}/${session_id}"
}

session_dir_exists() {
    local session_id="$1"
    [[ -d "$(get_session_dir "$session_id")" ]]
}

# =============================================================================
# DATE/TIME UTILITIES
# =============================================================================

get_date() {
    date '+%Y-%m-%d'
}

get_datetime() {
    date '+%Y-%m-%d %H:%M:%S'
}

get_timestamp() {
    date '+%Y%m%d_%H%M%S'
}

# =============================================================================
# INITIALIZATION CHECK
# =============================================================================

check_spec_system() {
    if [[ ! -d "$SPEC_SYSTEM_DIR" ]]; then
        log_error "Spec system not found. Expected: $SPEC_SYSTEM_DIR/"
        return 1
    fi

    if [[ ! -f "$STATE_FILE" ]]; then
        log_error "State file not found: $STATE_FILE"
        return 1
    fi

    if ! validate_json "$STATE_FILE"; then
        return 1
    fi

    return 0
}

# =============================================================================
# HELP
# =============================================================================

show_common_help() {
    cat <<'EOF'
Apex Spec System - Common Utilities

Functions available after sourcing common.sh:

LOGGING:
  log_info <msg>      - Blue info message
  log_success <msg>   - Green success message
  log_warning <msg>   - Yellow warning message
  log_error <msg>     - Red error message

JSON (requires jq):
  json_get <file> <path>           - Read JSON value
  json_set <file> <path> <value>   - Write JSON value
  validate_json <file>             - Validate JSON syntax

SESSION ID:
  parse_session_id <id> [vars...]  - Parse session ID components
  get_phase_from_session_id <id>   - Extract phase number
  build_session_id <p> <s> <name>  - Construct session ID
  build_session_ref <p> <s>        - Build ref like S0103

STATE:
  get_current_phase                - Current phase number
  get_current_session              - Current session ID
  get_completed_sessions           - List completed sessions
  is_session_completed <id>        - Check if completed
  set_current_session <id>         - Update current session
  add_completed_session <id> [pkg] - Mark session complete

MONOREPO:
  get_monorepo_flag                - "true", "false", or "null"
  get_packages                     - JSON array of packages
  get_package_path <name>          - Package path by name
  get_package_by_path <path>       - Package object by path
  get_sessions_for_package [path]  - Sessions for a package
  detect_monorepo                  - Detect monorepo (JSON)
  detect_packages                  - Enumerate packages (JSON)
  resolve_package_context [path]   - Active package (JSON)

VALIDATION:
  validate_ascii <file>            - Check ASCII encoding
  find_non_ascii <file>            - List non-ASCII chars
  check_spec_system                - Verify setup

UTILITIES:
  get_date                         - YYYY-MM-DD
  get_datetime                     - YYYY-MM-DD HH:MM:SS
  ensure_dir <dir>                 - Create if not exists
  get_session_dir <id>             - Get specs/session path
EOF
}

# Show help if script run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    show_common_help
fi

# CREDIT NOTE: The 1st version of this file was taken directly from Github's Spec Kit

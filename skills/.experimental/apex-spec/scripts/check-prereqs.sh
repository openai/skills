#!/usr/bin/env bash
# =============================================================================
# check-prereqs.sh - Validate session prerequisites
# =============================================================================
# Usage:
#   ./check-prereqs.sh --env                    # Check environment only
#   ./check-prereqs.sh --tools "node,npm"       # Check specific tools
#   ./check-prereqs.sh --json --env             # JSON output for Claude
# =============================================================================
# NOTE: The 1st version of this file was taken directly from Github's Spec Kit
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "${SCRIPT_DIR}/common.sh"

# =============================================================================
# OUTPUT MODE
# =============================================================================

OUTPUT_MODE="human"
JSON_RESULT=""
PACKAGE_FILTER=""

# =============================================================================
# JSON BUILDING HELPERS
# =============================================================================

init_json() {
    JSON_RESULT=$(jq -n --arg generated_at "$(get_datetime)" '{
        "generated_at": $generated_at,
        "overall": "pass",
        "environment": {},
        "package": {},
        "workspace": {},
        "tools": {},
        "sessions": {},
        "files": {},
        "database": {},
        "issues": []
    }')
}

add_json_issue() {
    local type="$1"
    local name="$2"
    local message="$3"
    JSON_RESULT=$(echo "$JSON_RESULT" | jq \
        --arg type "$type" \
        --arg name "$name" \
        --arg msg "$message" \
        '.issues += [{"type": $type, "name": $name, "message": $msg}]')
    JSON_RESULT=$(echo "$JSON_RESULT" | jq '.overall = "fail"')
}

set_check_result() {
    local category="$1"
    local name="$2"
    local status="$3"
    local extra="${4:-}"

    if [[ -n "$extra" ]]; then
        JSON_RESULT=$(echo "$JSON_RESULT" | jq \
            --arg cat "$category" \
            --arg name "$name" \
            --arg status "$status" \
            --arg extra "$extra" \
            '.[$cat][$name] = {"status": $status, "info": $extra}')
    else
        JSON_RESULT=$(echo "$JSON_RESULT" | jq \
            --arg cat "$category" \
            --arg name "$name" \
            --arg status "$status" \
            '.[$cat][$name] = {"status": $status}')
    fi
}

# =============================================================================
# SMALL STRING/LIST HELPERS
# =============================================================================

trim() {
    local s="${1:-}"
    # Remove leading whitespace
    s="${s#"${s%%[![:space:]]*}"}"
    # Remove trailing whitespace
    s="${s%"${s##*[![:space:]]}"}"
    printf '%s' "$s"
}

# Print a comma-separated list as trimmed, non-empty, newline-delimited items.
# This avoids word-splitting issues and preserves spaces inside individual items.
split_csv() {
    local input="${1:-}"
    local item=""
    local -a parts=()

    input="$(trim "$input")"
    [[ -z "$input" ]] && return 0

    local IFS=','
    read -r -a parts <<<"$input" || true

    for item in "${parts[@]}"; do
        item="$(trim "$item")"
        [[ -z "$item" ]] && continue
        printf '%s\n' "$item"
    done
}

# =============================================================================
# CHECK FUNCTIONS
# =============================================================================

check_required_sessions() {
    local prereqs="${1:-}"

    if [[ "$OUTPUT_MODE" == "human" ]]; then
        log_info "Checking required sessions..."
    fi

    if [[ -z "$(trim "$prereqs")" ]]; then
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_info "No prerequisite sessions specified"
        fi
        return 0
    fi

    local failed=0

    local prereq=""
    while IFS= read -r prereq; do
        [[ -z "$prereq" ]] && continue

        if is_session_completed "$prereq"; then
            if [[ "$OUTPUT_MODE" == "human" ]]; then
                log_success "Prerequisite met: $prereq"
            else
                set_check_result "sessions" "$prereq" "pass" "completed"
            fi
        else
            if [[ "$OUTPUT_MODE" == "human" ]]; then
                log_error "Prerequisite NOT met: $prereq"
            else
                set_check_result "sessions" "$prereq" "fail" "not completed"
                add_json_issue "session" "$prereq" "prerequisite session not completed"
            fi
            ((failed++)) || true
        fi
    done < <(split_csv "$prereqs")

    return $failed
}

check_required_tools() {
    local tools="${1:-}"

    if [[ "$OUTPUT_MODE" == "human" ]]; then
        log_info "Checking required tools..."
    fi

    if [[ -z "$(trim "$tools")" ]]; then
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_info "No specific tools required"
        fi
        return 0
    fi

    local failed=0

    local tool=""
    while IFS= read -r tool; do
        [[ -z "$tool" ]] && continue

        if command -v "$tool" &>/dev/null; then
            local version=""
            # Try to get version for common tools
            case "$tool" in
                node) version=$(node --version 2>&1 | head -1 || echo "unknown") ;;
                npm) version=$(npm --version 2>&1 | head -1 || echo "unknown") ;;
                python | python3) version=$("$tool" --version 2>&1 | head -1 || echo "unknown") ;;
                docker) version=$(docker --version 2>&1 | head -1 || echo "unknown") ;;
                git) version=$(git --version 2>&1 | head -1 || echo "unknown") ;;
                go) version=$(go version 2>&1 | head -1 || echo "unknown") ;;
                cargo) version=$(cargo --version 2>&1 | head -1 || echo "unknown") ;;
                *) version=$("$tool" --version 2>&1 | head -1 || echo "available") ;;
            esac
            [[ -z "$version" ]] && version="available"

            if [[ "$OUTPUT_MODE" == "human" ]]; then
                log_success "Tool available: $tool ($version)"
            else
                set_check_result "tools" "$tool" "pass" "$version"
            fi
        else
            if [[ "$OUTPUT_MODE" == "human" ]]; then
                log_error "Tool NOT available: $tool"
            else
                set_check_result "tools" "$tool" "fail" "not installed"
                add_json_issue "tool" "$tool" "required tool not installed"
            fi
            ((failed++)) || true
        fi
    done < <(split_csv "$tools")

    return $failed
}

check_required_files() {
    local files="${1:-}"

    if [[ "$OUTPUT_MODE" == "human" ]]; then
        log_info "Checking required files..."
    fi

    if [[ -z "$(trim "$files")" ]]; then
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_info "No specific files required"
        fi
        return 0
    fi

    local failed=0

    local file=""
    while IFS= read -r file; do
        [[ -z "$file" ]] && continue

        if [[ -f "$file" ]]; then
            if [[ "$OUTPUT_MODE" == "human" ]]; then
                log_success "File exists: $file"
            else
                set_check_result "files" "$file" "pass" "exists"
            fi
        else
            if [[ "$OUTPUT_MODE" == "human" ]]; then
                log_error "File NOT found: $file"
            else
                set_check_result "files" "$file" "fail" "not found"
                add_json_issue "file" "$file" "required file not found"
            fi
            ((failed++)) || true
        fi
    done < <(split_csv "$files")

    return $failed
}

check_database() {
    # Only runs when database signals are detected
    local has_db=false

    # Check for common DB signals
    local db_signals=(
        "docker-compose.yml" "docker-compose.yaml" "compose.yml" "compose.yaml"
        "prisma/schema.prisma" "drizzle.config.ts" "drizzle.config.js"
        "alembic.ini" "knexfile.js" "knexfile.ts"
        "diesel.toml" "sqlc.yaml" "sqlc.yml"
    )

    for signal in "${db_signals[@]}"; do
        if [[ -f "$signal" ]]; then
            has_db=true
            break
        fi
    done

    # Check .env for DATABASE_URL
    if [[ -f ".env" ]] && grep -q "DATABASE_URL\|DB_HOST\|DB_PORT" .env 2>/dev/null; then
        has_db=true
    fi

    [[ "$has_db" == false ]] && return 0

    # Detect DB type
    local db_type="unknown"
    if [[ -f ".env" ]]; then
        if grep -q "postgresql://" .env 2>/dev/null; then
            db_type="PostgreSQL"
        elif grep -q "mysql://" .env 2>/dev/null; then
            db_type="MySQL"
        elif grep -q "mongodb://" .env 2>/dev/null; then
            db_type="MongoDB"
        fi
    fi
    set_check_result "database" "type" "pass" "$db_type"

    # Detect migration tool
    local migration_tool="none"
    if [[ -f "prisma/schema.prisma" ]]; then
        migration_tool="prisma"
    elif [[ -f "drizzle.config.ts" || -f "drizzle.config.js" ]]; then
        migration_tool="drizzle"
    elif [[ -f "alembic.ini" ]]; then
        migration_tool="alembic"
    elif [[ -f "knexfile.js" || -f "knexfile.ts" ]]; then
        migration_tool="knex"
    elif [[ -f "diesel.toml" ]]; then
        migration_tool="diesel"
    elif [[ -f "sqlc.yaml" || -f "sqlc.yml" ]]; then
        migration_tool="sqlc"
    fi

    if [[ "$migration_tool" != "none" ]]; then
        set_check_result "database" "migration_tool" "pass" "$migration_tool"
    else
        set_check_result "database" "migration_tool" "warn" "no migration tool detected"
    fi

    # Check if migration tool CLI is available
    if [[ "$migration_tool" != "none" && "$migration_tool" != "sqlc" ]]; then
        local tool_cmd=""
        case "$migration_tool" in
            prisma) tool_cmd="npx prisma" ;;
            drizzle) tool_cmd="npx drizzle-kit" ;;
            alembic) tool_cmd="alembic" ;;
            knex) tool_cmd="npx knex" ;;
            diesel) tool_cmd="diesel" ;;
        esac
        if [[ -n "$tool_cmd" ]] && command -v "$(echo "$tool_cmd" | awk '{print $1}')" &>/dev/null; then
            set_check_result "database" "tool_available" "pass" "$tool_cmd"
        else
            set_check_result "database" "tool_available" "warn" "$tool_cmd not in PATH"
        fi
    fi

    # Check for seed script
    local seed_found=false
    local seed_files=("scripts/seed.ts" "scripts/seed.js" "scripts/seed.py" "prisma/seed.ts" "prisma/seed.js" "cmd/seed/main.go")
    for sf in "${seed_files[@]}"; do
        if [[ -f "$sf" ]]; then
            set_check_result "database" "seed_script" "pass" "$sf"
            seed_found=true
            break
        fi
    done
    if [[ "$seed_found" == false ]]; then
        set_check_result "database" "seed_script" "warn" "no seed script found"
    fi
}

check_environment() {
    if [[ "$OUTPUT_MODE" == "human" ]]; then
        log_info "Checking environment..."
    fi

    local failed=0
    local has_jq=false
    if command -v jq &>/dev/null; then
        has_jq=true
    fi

    # Check spec system
    if [[ -d "$SPEC_SYSTEM_DIR" && -f "$STATE_FILE" ]]; then
        if [[ "$has_jq" == true ]]; then
            if validate_json "$STATE_FILE" 2>/dev/null; then
                if [[ "$OUTPUT_MODE" == "human" ]]; then
                    log_success "Spec system: OK"
                else
                    set_check_result "environment" "spec_system" "pass" "$SPEC_SYSTEM_DIR"
                fi
            else
                if [[ "$OUTPUT_MODE" == "human" ]]; then
                    log_error "Spec system: Invalid state.json"
                else
                    set_check_result "environment" "spec_system" "fail" "invalid state.json"
                    add_json_issue "environment" "spec_system" "state.json is not valid JSON"
                fi
                ((failed++)) || true
            fi
        else
            if [[ "$OUTPUT_MODE" == "human" ]]; then
                log_error "Spec system: Found but jq missing (cannot validate state.json)"
            else
                set_check_result "environment" "spec_system" "fail" "jq not installed (cannot validate state.json)"
                add_json_issue "environment" "spec_system" "jq is required to validate state.json"
            fi
            ((failed++)) || true
        fi
    else
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_error "Spec system: NOT found"
        else
            set_check_result "environment" "spec_system" "fail" "not found"
            add_json_issue "environment" "spec_system" ".spec_system directory or state.json not found"
        fi
        ((failed++)) || true
    fi

    # Check jq
    if [[ "$has_jq" == true ]]; then
        local jq_version
        jq_version=$(jq --version 2>/dev/null || echo "unknown")
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_success "jq: OK ($jq_version)"
        else
            set_check_result "environment" "jq" "pass" "$jq_version"
        fi
    else
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_error "jq: NOT installed (required for scripts)"
        else
            set_check_result "environment" "jq" "fail" "not installed"
            add_json_issue "environment" "jq" "jq is required but not installed"
        fi
        ((failed++)) || true
    fi

    # Check git (optional but noted)
    if command -v git &>/dev/null; then
        local git_version
        git_version=$(git --version 2>/dev/null | head -1 || echo "unknown")
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_success "git: OK ($git_version)"
        else
            set_check_result "environment" "git" "pass" "$git_version"
        fi
    else
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_info "git: NOT installed (optional)"
        else
            set_check_result "environment" "git" "skip" "not installed (optional)"
        fi
    fi

    return $failed
}

# =============================================================================
# MONOREPO: PACKAGE & WORKSPACE CHECKS
# =============================================================================

# Verify a specific package exists in state.json and on disk.
# Requires: PACKAGE_FILTER set, jq available, state.json valid.
check_package() {
    local pkg_path="$1"

    if [[ "$OUTPUT_MODE" == "human" ]]; then
        log_info "Checking package: $pkg_path ..."
    fi

    local failed=0

    # Check package exists in state.json packages array
    local pkg_entry=""
    pkg_entry=$(get_package_by_path "$pkg_path" 2>/dev/null) || true

    if [[ -z "$pkg_entry" || "$pkg_entry" == "null" ]]; then
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_error "Package not registered in state.json: $pkg_path"
        else
            set_check_result "package" "registered" "fail" "$pkg_path not in state.json packages"
            add_json_issue "package" "$pkg_path" "package not registered in state.json"
        fi
        ((failed++)) || true
    else
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_success "Package registered: $pkg_path"
        else
            set_check_result "package" "registered" "pass" "$pkg_path"
        fi
    fi

    # Check package directory exists on disk
    if [[ -d "$pkg_path" ]]; then
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_success "Package directory exists: $pkg_path"
        else
            set_check_result "package" "directory" "pass" "$pkg_path"
        fi
    else
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_error "Package directory NOT found: $pkg_path"
        else
            set_check_result "package" "directory" "fail" "$pkg_path not found"
            add_json_issue "package" "$pkg_path" "package directory does not exist"
        fi
        ((failed++)) || true
    fi

    # Check for a package manifest (package.json, Cargo.toml, etc.)
    if [[ -d "$pkg_path" ]]; then
        local has_manifest=false
        for manifest in package.json Cargo.toml go.mod pyproject.toml setup.py; do
            if [[ -f "$pkg_path/$manifest" ]]; then
                has_manifest=true
                if [[ "$OUTPUT_MODE" == "human" ]]; then
                    log_success "Package manifest: $pkg_path/$manifest"
                else
                    set_check_result "package" "manifest" "pass" "$manifest"
                fi
                break
            fi
        done
        if [[ "$has_manifest" == false ]]; then
            if [[ "$OUTPUT_MODE" == "human" ]]; then
                log_info "No package manifest found in $pkg_path (optional)"
            else
                set_check_result "package" "manifest" "skip" "no manifest found (optional)"
            fi
        fi
    fi

    # Include package stack hint from state.json if available
    if [[ -n "$pkg_entry" && "$pkg_entry" != "null" ]]; then
        local stack=""
        stack=$(echo "$pkg_entry" | jq -r '.stack // empty' 2>/dev/null) || true
        if [[ -n "$stack" ]]; then
            if [[ "$OUTPUT_MODE" == "human" ]]; then
                log_info "Package stack: $stack"
            else
                set_check_result "package" "stack" "pass" "$stack"
            fi
        fi
    fi

    return $failed
}

# Verify monorepo workspace tooling when monorepo: true.
# Checks for workspace manager, config, and optional task runner.
check_workspace_tools() {
    if [[ "$OUTPUT_MODE" == "human" ]]; then
        log_info "Checking workspace tools..."
    fi

    local monorepo_flag=""
    monorepo_flag=$(get_monorepo_flag 2>/dev/null) || true

    if [[ "$monorepo_flag" != "true" ]]; then
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_info "Not a monorepo -- skipping workspace tool checks"
        else
            set_check_result "workspace" "status" "skip" "not a monorepo"
        fi
        return 0
    fi

    local failed=0

    # Detect workspace manager
    local manager=""
    local manager_version=""
    if [[ -f "pnpm-workspace.yaml" ]]; then
        manager="pnpm"
        manager_version=$(pnpm --version 2>/dev/null || echo "not installed")
    elif [[ -f "package.json" ]] && jq -e '.workspaces' package.json &>/dev/null; then
        # npm or yarn workspaces
        if command -v yarn &>/dev/null; then
            manager="yarn"
            manager_version=$(yarn --version 2>/dev/null || echo "unknown")
        else
            manager="npm"
            manager_version=$(npm --version 2>/dev/null || echo "unknown")
        fi
    elif [[ -f "Cargo.toml" ]] && grep -q '^\[workspace\]' Cargo.toml 2>/dev/null; then
        manager="cargo"
        manager_version=$(cargo --version 2>/dev/null | head -1 || echo "unknown")
    elif [[ -f "go.work" ]]; then
        manager="go"
        manager_version=$(go version 2>/dev/null | head -1 || echo "unknown")
    elif [[ -f "lerna.json" ]]; then
        manager="lerna"
        manager_version=$(npx lerna --version 2>/dev/null || echo "unknown")
    fi

    if [[ -n "$manager" ]]; then
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_success "Workspace manager: $manager ($manager_version)"
        else
            set_check_result "workspace" "manager" "pass" "$manager $manager_version"
        fi
    else
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_error "No workspace manager detected (monorepo: true in state.json)"
        else
            set_check_result "workspace" "manager" "fail" "no workspace config found"
            add_json_issue "workspace" "manager" "monorepo is true but no workspace manager detected"
        fi
        ((failed++)) || true
    fi

    # Check for task runner (turbo, nx -- optional but noted)
    local runner=""
    local runner_version=""
    if [[ -f "turbo.json" ]]; then
        runner="turbo"
        runner_version=$(npx turbo --version 2>/dev/null || echo "config found")
    elif [[ -f "nx.json" ]]; then
        runner="nx"
        runner_version=$(npx nx --version 2>/dev/null || echo "config found")
    fi

    if [[ -n "$runner" ]]; then
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_success "Task runner: $runner ($runner_version)"
        else
            set_check_result "workspace" "runner" "pass" "$runner $runner_version"
        fi
    else
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            log_info "No task runner detected (turbo/nx -- optional)"
        else
            set_check_result "workspace" "runner" "skip" "none detected (optional)"
        fi
    fi

    return $failed
}

# =============================================================================
# USAGE
# =============================================================================

show_usage() {
    cat <<'EOF'
Usage: check-prereqs.sh [OPTIONS]

Check prerequisites for a session.

OPTIONS:
  -t, --tools LIST     Comma-separated list of required tools
  -f, --files LIST     Comma-separated list of required files
  -p, --prereqs LIST   Comma-separated list of prerequisite sessions
  -e, --env            Check environment only
  --package PATH       Check package-specific prerequisites (monorepo)
  --json               Output results as JSON (for Claude integration)
  -h, --help           Show this help message

OUTPUT MODES:
  Default (no --json): Human-readable output with colors
  --json: Structured JSON for programmatic use

MONOREPO SUPPORT:
  When --package is specified:
  - Verifies the package is registered in state.json
  - Checks the package directory exists on disk
  - Checks for a package manifest (package.json, Cargo.toml, etc.)
  - Reports the package stack from state.json

  When monorepo: true in state.json (automatic with --env):
  - Detects workspace manager (pnpm, npm/yarn, cargo, go, lerna)
  - Detects task runner (turbo, nx) if present

JSON OUTPUT STRUCTURE:
  {
    "generated_at": "2024-01-15 10:30:00",
    "overall": "pass" | "fail",
    "environment": {
      "spec_system": {"status": "pass", "info": ".spec_system"},
      "jq": {"status": "pass", "info": "jq-1.7"}
    },
    "package": {
      "registered": {"status": "pass", "info": "apps/web"},
      "directory": {"status": "pass", "info": "apps/web"},
      "manifest": {"status": "pass", "info": "package.json"},
      "stack": {"status": "pass", "info": "TypeScript + React"}
    },
    "workspace": {
      "manager": {"status": "pass", "info": "pnpm 8.15.0"},
      "runner": {"status": "pass", "info": "turbo 1.12.0"}
    },
    "tools": {
      "node": {"status": "pass", "info": "v20.10.0"},
      "docker": {"status": "fail", "info": "not installed"}
    },
    "sessions": {
      "phase00-session01": {"status": "pass", "info": "completed"}
    },
    "files": {
      "package.json": {"status": "pass", "info": "exists"}
    },
    "issues": [
      {"type": "tool", "name": "docker", "message": "required tool not installed"}
    ]
  }

    "database": {
      "type": {"status": "pass", "info": "PostgreSQL"},
      "migration_tool": {"status": "pass", "info": "prisma"},
      "tool_available": {"status": "pass", "info": "npx prisma"},
      "seed_script": {"status": "warn", "info": "no seed script found"}
    },

  Notes:
  - "package" section only present when --package is used
  - "workspace" section only present when monorepo: true in state.json
  - "database" section only present when DB signals detected in project
  - Both "package" and "workspace" sections empty ({}) when not applicable

EXAMPLES:
  ./check-prereqs.sh --env                              # Check environment
  ./check-prereqs.sh --tools "node,npm,docker"          # Check tools
  ./check-prereqs.sh --json --env                       # JSON output
  ./check-prereqs.sh --json --env --tools "node,npm"
  ./check-prereqs.sh --json --env --package apps/web    # Monorepo package check
EOF
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    local tools=""
    local files=""
    local prereqs=""
    local env_only=false
    local run_any=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --json)
                OUTPUT_MODE="json"
                check_jq || exit 1
                init_json
                shift
                ;;
            --tools=*)
                tools="${1#*=}"
                run_any=true
                shift
                ;;
            -t | --tools)
                if [[ $# -lt 2 ]]; then
                    log_error "Missing value for $1"
                    show_usage
                    exit 1
                fi
                tools="$2"
                run_any=true
                shift 2
                ;;
            --files=*)
                files="${1#*=}"
                run_any=true
                shift
                ;;
            -f | --files)
                if [[ $# -lt 2 ]]; then
                    log_error "Missing value for $1"
                    show_usage
                    exit 1
                fi
                files="$2"
                run_any=true
                shift 2
                ;;
            --prereqs=*)
                prereqs="${1#*=}"
                run_any=true
                shift
                ;;
            -p | --prereqs)
                if [[ $# -lt 2 ]]; then
                    log_error "Missing value for $1"
                    show_usage
                    exit 1
                fi
                prereqs="$2"
                run_any=true
                shift 2
                ;;
            -e | --env)
                env_only=true
                run_any=true
                shift
                ;;
            --package)
                if [[ -z "${2:-}" ]]; then
                    log_error "--package requires a PATH argument"
                    exit 1
                fi
                PACKAGE_FILTER="$2"
                run_any=true
                shift 2
                ;;
            -h | --help)
                show_usage
                exit 0
                ;;
            --)
                shift
                break
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    # Default to env check if nothing specified
    if [[ "$run_any" == false ]]; then
        env_only=true
    fi

    if [[ "$OUTPUT_MODE" != "json" ]]; then
        echo "=============================================="
        echo "PREREQUISITE CHECK"
        echo "=============================================="
        echo ""
    fi

    local total_failed=0
    local rc=0

    # Always check environment first
    rc=0
    check_environment || rc=$?
    total_failed=$((total_failed + rc))

    # Check workspace tools when monorepo (automatic with --env)
    if [[ "$env_only" == true || -n "$PACKAGE_FILTER" ]]; then
        rc=0
        check_workspace_tools || rc=$?
        total_failed=$((total_failed + rc))
    fi

    # Check database (automatic with --env, only when DB signals detected)
    if [[ "$env_only" == true && "$OUTPUT_MODE" == "json" ]]; then
        check_database
    fi

    # Check package if --package was specified
    if [[ -n "$PACKAGE_FILTER" ]]; then
        [[ "$OUTPUT_MODE" == "human" ]] && echo ""
        rc=0
        check_package "$PACKAGE_FILTER" || rc=$?
        total_failed=$((total_failed + rc))
    fi

    if [[ "$env_only" == true && -z "$tools" && -z "$files" && -z "$prereqs" && -z "$PACKAGE_FILTER" ]]; then
        # Just environment check (and workspace/package if applicable)
        :
    else
        if [[ "$OUTPUT_MODE" == "human" ]]; then
            echo ""
        fi

        # Check session prerequisites
        if [[ -n "$(trim "$prereqs")" ]]; then
            rc=0
            check_required_sessions "$prereqs" || rc=$?
            total_failed=$((total_failed + rc))
            [[ "$OUTPUT_MODE" == "human" ]] && echo ""
        fi

        # Check tools
        if [[ -n "$(trim "$tools")" ]]; then
            rc=0
            check_required_tools "$tools" || rc=$?
            total_failed=$((total_failed + rc))
            [[ "$OUTPUT_MODE" == "human" ]] && echo ""
        fi

        # Check files
        if [[ -n "$(trim "$files")" ]]; then
            rc=0
            check_required_files "$files" || rc=$?
            total_failed=$((total_failed + rc))
            [[ "$OUTPUT_MODE" == "human" ]] && echo ""
        fi
    fi

    # Output results
    if [[ "$OUTPUT_MODE" == "json" ]]; then
        echo "$JSON_RESULT" | jq .
    else
        echo "=============================================="
        if [[ $total_failed -eq 0 ]]; then
            log_success "All prerequisites met!"
        else
            log_error "Some prerequisites not met ($total_failed issues)"
        fi
    fi

    # Exit with appropriate code
    if [[ "$OUTPUT_MODE" == "json" ]]; then
        local overall
        overall=$(echo "$JSON_RESULT" | jq -r '.overall')
        [[ "$overall" == "pass" ]] && exit 0 || exit 1
    else
        [[ $total_failed -eq 0 ]] && exit 0 || exit 1
    fi
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

# CREDIT NOTE: The 1st version of this file was taken directly from Github's Spec Kit

#!/usr/bin/env bash
# =============================================================================
# analyze-project.sh - Analyze project state for session recommendations
# =============================================================================
# Usage:
#   ./analyze-project.sh           # Human-readable output
#   ./analyze-project.sh --json    # JSON output for Claude integration
# =============================================================================
# CREDIT NOTE: The 1st version of this file was taken directly from Github's Spec Kit
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "${SCRIPT_DIR}/common.sh"

# =============================================================================
# OUTPUT MODE
# =============================================================================

OUTPUT_MODE="human"
PACKAGE_FILTER=""

# =============================================================================
# JSON OUTPUT FUNCTIONS
# =============================================================================

output_json() {
    check_jq || exit 1

    local project_name current_phase current_session completed_count
    project_name=$(get_project_name)
    current_phase=$(get_current_phase)
    current_session=$(get_current_session)
    completed_count=$(get_completed_sessions_count)

    # Monorepo state
    local monorepo_flag packages_json active_package monorepo_detection
    monorepo_flag=$(get_monorepo_flag)
    packages_json=$(get_packages)
    active_package=$(resolve_package_context "$PACKAGE_FILTER")

    # Auto-detect monorepo when state is unknown (null)
    if [[ "$monorepo_flag" == "null" ]]; then
        monorepo_detection=$(detect_monorepo)
    else
        monorepo_detection="null"
    fi

    # Build phases array
    local phases_json="[]"
    local phases
    phases=$(json_get "$STATE_FILE" '.phases | keys[]' 2>/dev/null || echo "")

    for phase in $phases; do
        local name status count
        name=$(get_phase_name "$phase")
        status=$(get_phase_status "$phase")
        count=$(get_phase_session_count "$phase")

        phases_json=$(echo "$phases_json" | jq \
            --arg num "$phase" \
            --arg name "$name" \
            --arg status "$status" \
            --argjson count "$count" \
            '. += [{"number": ($num | tonumber), "name": $name, "status": $status, "session_count": $count}]')
    done

    # Build completed sessions array
    local completed_json="[]"
    while IFS= read -r session; do
        [[ -n "$session" ]] && completed_json=$(echo "$completed_json" | jq --arg s "$session" '. += [$s]')
    done < <(get_completed_sessions)

    # Build candidate sessions array
    local candidates_json="[]"
    local prd_dir
    prd_dir="${SPEC_SYSTEM_DIR}/PRD/phase_$(printf '%02d' "$current_phase")"

    if [[ -d "$prd_dir" ]]; then
        while IFS= read -r file; do
            [[ -z "$file" ]] && continue
            local filename
            filename=$(basename "$file" .md)

            # Extract session number from filename (session_NN_name)
            if [[ "$filename" =~ ^session_([0-9]+)_(.+)$ ]]; then
                local session_num_raw="${BASH_REMATCH[1]}"
                local session_num
                session_num=$((10#$session_num_raw))
                local session_name="${BASH_REMATCH[2]}"
                local is_completed="false"

                if is_session_number_completed "$session_num" "$current_phase"; then
                    is_completed="true"
                fi

                # Parse Package: annotation from first 10 lines of stub
                local pkg_annotation=""
                pkg_annotation=$(head -10 "$file" | sed -n 's/^[*]*Package[*]*:[[:space:]]*\(.*\)/\1/p' | head -1)
                pkg_annotation=$(trim "$pkg_annotation")

                candidates_json=$(echo "$candidates_json" | jq \
                    --arg file "$filename" \
                    --arg path "$file" \
                    --argjson num "$session_num" \
                    --arg name "$session_name" \
                    --argjson completed "$is_completed" \
                    --arg pkg "$pkg_annotation" \
                    '. += [{"file": $file, "path": $path, "session_number": $num, "name": $name, "completed": $completed, "package": (if $pkg == "" then null else $pkg end)}]')
            fi
        done < <(find "$prd_dir" -name "session_*.md" -type f 2>/dev/null | sort)
    fi

    # Filter candidates by package if --package was specified
    if [[ -n "$PACKAGE_FILTER" ]]; then
        candidates_json=$(echo "$candidates_json" | jq --arg pkg "$PACKAGE_FILTER" \
            '[.[] | select(.package == $pkg or .package == null)]')
    fi

    # Get current session directory status
    local session_dir_exists="false"
    local session_files="[]"
    if [[ "$current_session" != "null" && -n "$current_session" ]]; then
        local session_dir
        session_dir=$(get_session_dir "$current_session")
        if [[ -d "$session_dir" ]]; then
            session_dir_exists="true"
            while IFS= read -r f; do
                [[ -n "$f" ]] && session_files=$(echo "$session_files" | jq --arg f "$(basename "$f")" '. += [$f]')
            done < <(find "$session_dir" -type f -name "*.md" 2>/dev/null | sort)
        fi
    fi

    # Convert monorepo_flag string to proper JSON value
    local monorepo_json
    case "$monorepo_flag" in
        true) monorepo_json="true" ;;
        false) monorepo_json="false" ;;
        *) monorepo_json="null" ;;
    esac

    # Build final JSON output
    jq -n \
        --arg project "$project_name" \
        --arg state_file "$STATE_FILE" \
        --argjson current_phase "$current_phase" \
        --arg current_session "$current_session" \
        --argjson session_dir_exists "$session_dir_exists" \
        --argjson session_files "$session_files" \
        --argjson completed_count "$completed_count" \
        --argjson phases "$phases_json" \
        --argjson completed_sessions "$completed_json" \
        --argjson candidates "$candidates_json" \
        --argjson monorepo "$monorepo_json" \
        --argjson packages "$packages_json" \
        --argjson active_package "$active_package" \
        --argjson monorepo_detection "$monorepo_detection" \
        --arg generated_at "$(get_datetime)" \
        '{
            "project": $project,
            "state_file": $state_file,
            "generated_at": $generated_at,
            "current_phase": $current_phase,
            "current_session": (if $current_session == "null" then null else $current_session end),
            "current_session_dir_exists": $session_dir_exists,
            "current_session_files": $session_files,
            "completed_sessions_count": $completed_count,
            "monorepo": $monorepo,
            "packages": $packages,
            "active_package": $active_package,
            "monorepo_detection": $monorepo_detection,
            "phases": $phases,
            "completed_sessions": $completed_sessions,
            "candidate_sessions": $candidates
        }'
}

# =============================================================================
# HUMAN-READABLE OUTPUT FUNCTIONS
# =============================================================================

analyze_phases() {
    log_info "Analyzing phases..."

    local current_phase
    current_phase=$(get_current_phase)

    echo "Current Phase: $current_phase"
    echo ""
    echo "Phase Status:"
    echo "-------------"

    # Get all phase numbers from state
    local phases
    phases=$(json_get "$STATE_FILE" '.phases | keys[]' 2>/dev/null || echo "")

    for phase in $phases; do
        local name status count
        name=$(get_phase_name "$phase")
        status=$(get_phase_status "$phase")
        count=$(get_phase_session_count "$phase")
        printf "  Phase %02d: %-25s [%s] (%d sessions)\n" "$phase" "$name" "$status" "$count"
    done
}

analyze_sessions() {
    log_info "Analyzing completed sessions..."

    local count
    count=$(get_completed_sessions_count)

    echo ""
    echo "Completed Sessions: $count"
    echo "-------------------"

    get_completed_sessions | while read -r session; do
        [[ -n "$session" ]] && echo "  - $session"
    done
}

analyze_current() {
    log_info "Analyzing current state..."

    local current
    current=$(get_current_session)

    echo ""
    echo "Current Session: ${current:-"(none)"}"

    if [[ "$current" != "null" && -n "$current" ]]; then
        local session_dir
        session_dir=$(get_session_dir "$current")

        echo "Session Directory: $session_dir"

        if [[ -d "$session_dir" ]]; then
            echo "Files:"
            find "$session_dir" -maxdepth 1 -type f -printf '  %f\n' 2>/dev/null | sort
        else
            echo "  (directory not created yet)"
        fi
    fi
}

analyze_next_candidates() {
    log_info "Finding next session candidates..."

    local current_phase
    current_phase=$(get_current_phase)

    local prd_dir
    prd_dir="${SPEC_SYSTEM_DIR}/PRD/phase_$(printf '%02d' "$current_phase")"

    echo ""
    echo "Next Session Candidates (Phase $current_phase):"
    echo "----------------------------------------------"

    if [[ -d "$prd_dir" ]]; then
        # List session files that aren't completed
        while IFS= read -r file; do
            local filename
            filename=$(basename "$file" .md)

            # Extract session number from filename (session_NN_name)
            if [[ "$filename" =~ ^session_([0-9]+)_ ]]; then
                local session_num_raw="${BASH_REMATCH[1]}"
                local session_num
                session_num=$((10#$session_num_raw))

                if ! is_session_number_completed "$session_num" "$current_phase"; then
                    echo "  - $filename (not completed)"
                else
                    echo "  - $filename (completed)"
                fi
            fi
        done < <(find "$prd_dir" -name "session_*.md" -type f | sort)
    else
        echo "  (no phase directory found: $prd_dir)"
    fi
}

show_summary() {
    echo ""
    echo "=============================================="
    echo "PROJECT ANALYSIS SUMMARY"
    echo "=============================================="

    local project_name
    project_name=$(get_project_name)

    echo "Project: $project_name"
    echo "State File: $STATE_FILE"

    # Show monorepo status if applicable
    local monorepo_flag
    monorepo_flag=$(get_monorepo_flag)
    if [[ "$monorepo_flag" == "true" ]]; then
        echo "Monorepo: Yes"
        local packages
        packages=$(get_packages)
        local pkg_count
        pkg_count=$(echo "$packages" | jq 'length')
        echo "Packages: $pkg_count"
        echo "$packages" | jq -r '.[] | "  - \(.name) (\(.path))"' 2>/dev/null
    elif [[ "$monorepo_flag" == "null" ]]; then
        echo "Monorepo: Unknown (not yet determined)"
    fi
    echo ""

    analyze_phases
    analyze_sessions
    analyze_current
    analyze_next_candidates

    echo ""
    echo "=============================================="
}

# =============================================================================
# USAGE
# =============================================================================

show_usage() {
    cat <<'EOF'
Usage: analyze-project.sh [OPTIONS]

Analyze project state for session recommendations.

OPTIONS:
  --json              Output analysis as JSON (for Claude integration)
  --package PATH      Filter candidates by package path (monorepo only)
  --help              Show this help message

OUTPUT MODES:
  Default (no flags): Human-readable summary with colors
  --json: Structured JSON for programmatic use

JSON OUTPUT STRUCTURE:
  {
    "project": "project-name",
    "state_file": ".spec_system/state.json",
    "generated_at": "2024-01-15 10:30:00",
    "current_phase": 1,
    "current_session": "phase01-session02-feature" | null,
    "current_session_dir_exists": true | false,
    "current_session_files": ["spec.md", "tasks.md"],
    "completed_sessions_count": 5,
    "monorepo": true | false | null,
    "packages": [{"name": "web", "path": "apps/web", "stack_hint": "TypeScript"}],
    "active_package": {"name": "web", "path": "apps/web", ...} | null,
    "monorepo_detection": {"detected": true, "indicator": "...", "packages": [...]} | null,
    "phases": [
      {"number": 0, "name": "Foundation", "status": "completed", "session_count": 3}
    ],
    "completed_sessions": ["phase00-session01-setup", ...],
    "candidate_sessions": [
      {"file": "session_01_auth", "path": "...", "session_number": 1, "name": "auth", "completed": false, "package": "apps/web" | null}
    ]
  }

MONOREPO FIELDS:
  monorepo             true/false/null from state.json
  packages             Array of registered packages (empty if not monorepo)
  active_package       Resolved package context from --package flag or CWD
  monorepo_detection   Auto-detection result (only when monorepo is null)
  candidate.package    Package annotation parsed from session stub header

EXAMPLES:
  ./analyze-project.sh                          # View human-readable summary
  ./analyze-project.sh --json                   # Get JSON for Claude
  ./analyze-project.sh --json | jq              # Pretty-print JSON
  ./analyze-project.sh --json --package apps/web  # Filter by package
EOF
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --json)
                OUTPUT_MODE="json"
                shift
                ;;
            --package)
                if [[ -z "${2:-}" ]]; then
                    log_error "--package requires a PATH argument"
                    exit 1
                fi
                PACKAGE_FILTER="$2"
                shift 2
                ;;
            --help | -h)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    check_spec_system || exit 1

    if [[ "$OUTPUT_MODE" == "json" ]]; then
        output_json
    else
        show_summary
    fi
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

# CREDIT NOTE: The 1st version of this file was taken directly from Github's Spec Kit

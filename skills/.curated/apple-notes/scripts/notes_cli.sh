#!/usr/bin/env bash
set -euo pipefail

die() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

ensure_osascript() {
  command -v osascript >/dev/null 2>&1 || die "osascript not found. This script requires macOS."
}

is_positive_int() {
  [[ "${1:-}" =~ ^[1-9][0-9]*$ ]]
}

usage() {
  cat <<'EOF'
Usage:
  notes_cli.sh create --body "<html>" [--folder "Notes"] [--account-index 1]
  notes_cli.sh create --body-file /absolute/path/body.html [--folder "Notes"] [--account-index 1]
  notes_cli.sh list-latest [--limit 20] [--folder "Notes"] [--account-index 1]
  notes_cli.sh search-title --query "zagreb" [--limit 20] [--folder "Notes"] [--account-index 1]
  notes_cli.sh search-any --query "zagreb" [--limit 20] [--folder "Notes"] [--account-index 1]
  notes_cli.sh update --title "Exact Title" --body "<html>" [--folder "Notes"] [--account-index 1]
  notes_cli.sh update --title "Exact Title" --body-file /absolute/path/body.html [--folder "Notes"] [--account-index 1]
  notes_cli.sh delete --title "Exact Title" [--folder "Notes"] [--account-index 1]
  notes_cli.sh count [--folder "Notes"] [--account-index 1]
  notes_cli.sh help
EOF
}

require_value() {
  local option="${1:-}"
  local value="${2:-}"
  [[ -n "$value" ]] || die "${option} requires a value."
}

cmd_create() {
  local folder="Notes"
  local account_index="1"
  local body=""
  local body_file=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --body)
        require_value "$1" "${2:-}"
        body="$2"
        shift 2
        ;;
      --body-file)
        require_value "$1" "${2:-}"
        body_file="$2"
        shift 2
        ;;
      --folder)
        require_value "$1" "${2:-}"
        folder="$2"
        shift 2
        ;;
      --account-index)
        require_value "$1" "${2:-}"
        account_index="$2"
        shift 2
        ;;
      *)
        die "Unknown option for create: $1"
        ;;
    esac
  done

  if [[ -z "$body" && -z "$body_file" ]]; then
    die "create requires either --body or --body-file."
  fi
  if [[ -n "$body" && -n "$body_file" ]]; then
    die "Use only one of --body or --body-file."
  fi
  is_positive_int "$account_index" || die "--account-index must be a positive integer."

  if [[ -n "$body_file" ]]; then
    [[ -f "$body_file" ]] || die "Body file does not exist: $body_file"
    body="$(cat "$body_file")"
  fi

  osascript - "$account_index" "$folder" "$body" <<'APPLESCRIPT'
on run argv
  set accountIndex to (item 1 of argv) as integer
  set folderName to item 2 of argv
  set newBody to item 3 of argv

  tell application "Notes"
    set targetFolder to folder folderName of account accountIndex
    set newNote to make new note at targetFolder with properties {body:newBody}
    return "Created: " & (name of newNote)
  end tell
end run
APPLESCRIPT
}

cmd_list_latest() {
  local folder="Notes"
  local account_index="1"
  local limit="20"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --limit)
        require_value "$1" "${2:-}"
        limit="$2"
        shift 2
        ;;
      --folder)
        require_value "$1" "${2:-}"
        folder="$2"
        shift 2
        ;;
      --account-index)
        require_value "$1" "${2:-}"
        account_index="$2"
        shift 2
        ;;
      *)
        die "Unknown option for list-latest: $1"
        ;;
    esac
  done

  is_positive_int "$limit" || die "--limit must be a positive integer."
  is_positive_int "$account_index" || die "--account-index must be a positive integer."

  osascript - "$account_index" "$folder" "$limit" <<'APPLESCRIPT'
on run argv
  set accountIndex to (item 1 of argv) as integer
  set folderName to item 2 of argv
  set takeCount to (item 3 of argv) as integer

  tell application "Notes"
    tell folder folderName of account accountIndex
      set totalCount to count of notes
      if totalCount < takeCount then set takeCount to totalCount

      set output to "Total notes: " & totalCount & linefeed & "Showing latest: " & takeCount & linefeed
      repeat with i from 1 to takeCount
        set n to item i of notes
        set output to output & (name of n) & " | " & ((modification date of n) as text) & linefeed
      end repeat
      return output
    end tell
  end tell
end run
APPLESCRIPT
}

cmd_search_title() {
  local folder="Notes"
  local account_index="1"
  local limit="20"
  local query=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --query)
        require_value "$1" "${2:-}"
        query="$2"
        shift 2
        ;;
      --limit)
        require_value "$1" "${2:-}"
        limit="$2"
        shift 2
        ;;
      --folder)
        require_value "$1" "${2:-}"
        folder="$2"
        shift 2
        ;;
      --account-index)
        require_value "$1" "${2:-}"
        account_index="$2"
        shift 2
        ;;
      *)
        die "Unknown option for search-title: $1"
        ;;
    esac
  done

  [[ -n "$query" ]] || die "search-title requires --query."
  is_positive_int "$limit" || die "--limit must be a positive integer."
  is_positive_int "$account_index" || die "--account-index must be a positive integer."

  osascript - "$account_index" "$folder" "$query" "$limit" <<'APPLESCRIPT'
on run argv
  set accountIndex to (item 1 of argv) as integer
  set folderName to item 2 of argv
  set queryText to item 3 of argv
  set takeCount to (item 4 of argv) as integer

  tell application "Notes"
    set matches to every note of folder folderName of account accountIndex whose name contains queryText
    set totalCount to count of matches
    if totalCount is 0 then return "No matches"

    if totalCount < takeCount then set takeCount to totalCount
    set output to "Total matches: " & totalCount & linefeed & "Showing up to " & takeCount & ":" & linefeed
    repeat with i from 1 to takeCount
      set n to item i of matches
      set output to output & (name of n) & " | " & ((modification date of n) as text) & linefeed
    end repeat
    return output
  end tell
end run
APPLESCRIPT
}

cmd_search_any() {
  local folder="Notes"
  local account_index="1"
  local limit="20"
  local query=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --query)
        require_value "$1" "${2:-}"
        query="$2"
        shift 2
        ;;
      --limit)
        require_value "$1" "${2:-}"
        limit="$2"
        shift 2
        ;;
      --folder)
        require_value "$1" "${2:-}"
        folder="$2"
        shift 2
        ;;
      --account-index)
        require_value "$1" "${2:-}"
        account_index="$2"
        shift 2
        ;;
      *)
        die "Unknown option for search-any: $1"
        ;;
    esac
  done

  [[ -n "$query" ]] || die "search-any requires --query."
  is_positive_int "$limit" || die "--limit must be a positive integer."
  is_positive_int "$account_index" || die "--account-index must be a positive integer."

  osascript - "$account_index" "$folder" "$query" "$limit" <<'APPLESCRIPT'
on run argv
  set accountIndex to (item 1 of argv) as integer
  set folderName to item 2 of argv
  set queryText to item 3 of argv
  set takeCount to (item 4 of argv) as integer

  tell application "Notes"
    set matches to every note of folder folderName of account accountIndex whose name contains queryText or body contains queryText
    set totalCount to count of matches
    if totalCount is 0 then return "No matches"

    if totalCount < takeCount then set takeCount to totalCount
    set output to "Total matches: " & totalCount & linefeed & "Showing up to " & takeCount & ":" & linefeed
    repeat with i from 1 to takeCount
      set n to item i of matches
      set output to output & (name of n) & " | " & ((modification date of n) as text) & linefeed
    end repeat
    return output
  end tell
end run
APPLESCRIPT
}

cmd_update() {
  local folder="Notes"
  local account_index="1"
  local title=""
  local body=""
  local body_file=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --title)
        require_value "$1" "${2:-}"
        title="$2"
        shift 2
        ;;
      --body)
        require_value "$1" "${2:-}"
        body="$2"
        shift 2
        ;;
      --body-file)
        require_value "$1" "${2:-}"
        body_file="$2"
        shift 2
        ;;
      --folder)
        require_value "$1" "${2:-}"
        folder="$2"
        shift 2
        ;;
      --account-index)
        require_value "$1" "${2:-}"
        account_index="$2"
        shift 2
        ;;
      *)
        die "Unknown option for update: $1"
        ;;
    esac
  done

  [[ -n "$title" ]] || die "update requires --title."
  if [[ -z "$body" && -z "$body_file" ]]; then
    die "update requires either --body or --body-file."
  fi
  if [[ -n "$body" && -n "$body_file" ]]; then
    die "Use only one of --body or --body-file."
  fi
  is_positive_int "$account_index" || die "--account-index must be a positive integer."

  if [[ -n "$body_file" ]]; then
    [[ -f "$body_file" ]] || die "Body file does not exist: $body_file"
    body="$(cat "$body_file")"
  fi

  osascript - "$account_index" "$folder" "$title" "$body" <<'APPLESCRIPT'
on run argv
  set accountIndex to (item 1 of argv) as integer
  set folderName to item 2 of argv
  set exactName to item 3 of argv
  set newBody to item 4 of argv

  tell application "Notes"
    set matches to every note of folder folderName of account accountIndex whose name is exactName
    if matches is {} then error "Note not found"

    if (count of matches) > 1 then
      set output to "More than one note has this title. Please choose by date:" & linefeed
      repeat with n in matches
        set output to output & (name of n) & " | " & ((modification date of n) as text) & linefeed
      end repeat
      return output
    end if

    set theNote to item 1 of matches
    set body of theNote to newBody
    return "Updated: " & (name of theNote)
  end tell
end run
APPLESCRIPT
}

cmd_delete() {
  local folder="Notes"
  local account_index="1"
  local title=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --title)
        require_value "$1" "${2:-}"
        title="$2"
        shift 2
        ;;
      --folder)
        require_value "$1" "${2:-}"
        folder="$2"
        shift 2
        ;;
      --account-index)
        require_value "$1" "${2:-}"
        account_index="$2"
        shift 2
        ;;
      *)
        die "Unknown option for delete: $1"
        ;;
    esac
  done

  [[ -n "$title" ]] || die "delete requires --title."
  is_positive_int "$account_index" || die "--account-index must be a positive integer."

  osascript - "$account_index" "$folder" "$title" <<'APPLESCRIPT'
on run argv
  set accountIndex to (item 1 of argv) as integer
  set folderName to item 2 of argv
  set exactName to item 3 of argv

  tell application "Notes"
    set matches to every note of folder folderName of account accountIndex whose name is exactName
    if matches is {} then error "Note not found"

    if (count of matches) > 1 then
      set output to "More than one note has this title. Please choose by date:" & linefeed
      repeat with n in matches
        set output to output & (name of n) & " | " & ((modification date of n) as text) & linefeed
      end repeat
      return output
    end if

    delete item 1 of matches
    return "Deleted"
  end tell
end run
APPLESCRIPT
}

cmd_count() {
  local folder="Notes"
  local account_index="1"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --folder)
        require_value "$1" "${2:-}"
        folder="$2"
        shift 2
        ;;
      --account-index)
        require_value "$1" "${2:-}"
        account_index="$2"
        shift 2
        ;;
      *)
        die "Unknown option for count: $1"
        ;;
    esac
  done

  is_positive_int "$account_index" || die "--account-index must be a positive integer."

  osascript - "$account_index" "$folder" <<'APPLESCRIPT'
on run argv
  set accountIndex to (item 1 of argv) as integer
  set folderName to item 2 of argv

  tell application "Notes"
    tell folder folderName of account accountIndex
      return "Total notes: " & (count of notes)
    end tell
  end tell
end run
APPLESCRIPT
}

main() {
  ensure_osascript

  local cmd="${1:-help}"
  if [[ $# -gt 0 ]]; then
    shift
  fi

  case "$cmd" in
    create)
      cmd_create "$@"
      ;;
    list-latest)
      cmd_list_latest "$@"
      ;;
    search-title)
      cmd_search_title "$@"
      ;;
    search-any)
      cmd_search_any "$@"
      ;;
    update)
      cmd_update "$@"
      ;;
    delete)
      cmd_delete "$@"
      ;;
    count)
      cmd_count "$@"
      ;;
    help|-h|--help)
      usage
      ;;
    *)
      die "Unknown command: $cmd"
      ;;
  esac
}

main "$@"

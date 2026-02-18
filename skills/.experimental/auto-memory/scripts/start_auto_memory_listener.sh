#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LISTENER_SCRIPT="$SCRIPT_DIR/app_server_compaction_listener.py"

DEFAULT_PROJECT_RAW="$(basename "$PWD")"
DEFAULT_PROJECT="$(printf '%s' "$DEFAULT_PROJECT_RAW" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-*//;s/-*$//')"
DEFAULT_PROJECT="${DEFAULT_PROJECT:-workspace}"

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

PROJECT="${AUTO_MEMORY_PROJECT:-$DEFAULT_PROJECT}"
OBJECTIVE="${AUTO_MEMORY_OBJECTIVE:-Continue the active task using preserved context after compaction.}"
LIMIT="${AUTO_MEMORY_LIMIT:-8}"
OUTPUT_FRAMING="${AUTO_MEMORY_OUTPUT_FRAMING:-jsonl}"
REQUEST_ID_PREFIX="${AUTO_MEMORY_REQUEST_ID_PREFIX:-auto-memory}"
MODE="${AUTO_MEMORY_MODE:-compaction}"
PROMPT_OUT="${AUTO_MEMORY_PROMPT_OUT:-$CODEX_HOME/tmp/auto-memory-reinjection.txt}"
JSONL_LOG="${AUTO_MEMORY_LOG:-$CODEX_HOME/tmp/auto-memory-listener.log}"
REINJECTION_MAX_CHARS="${AUTO_MEMORY_REINJECTION_MAX_CHARS:-12000}"
REINJECTION_MAX_ESTIMATED_TOKENS="${AUTO_MEMORY_REINJECTION_MAX_ESTIMATED_TOKENS:-3000}"
OVERSIZE_ACTION="${AUTO_MEMORY_OVERSIZE_ACTION:-skip}"
QUERY="${AUTO_MEMORY_QUERY:-}"
INPUT_FILE="${AUTO_MEMORY_INPUT_FILE:-}"
QUIET="${AUTO_MEMORY_QUIET:-1}"
VISUAL_STATUS="${AUTO_MEMORY_VISUAL_STATUS:-1}"
AUTO_SAVE_EVENTS="${AUTO_MEMORY_AUTO_SAVE_EVENTS:-turn/complete,turn/completed}"
AUTO_SAVE_TITLE_PREFIX="${AUTO_MEMORY_AUTO_SAVE_TITLE_PREFIX:-Auto memory}"
AUTO_SAVE_TAGS="${AUTO_MEMORY_AUTO_SAVE_TAGS:-auto-memory,auto-save}"
AUTO_SAVE_PROJECT_FIELD="${AUTO_MEMORY_AUTO_SAVE_PROJECT_FIELD:-project}"
AUTO_SAVE_SUMMARY_FIELDS="${AUTO_MEMORY_AUTO_SAVE_SUMMARY_FIELDS:-summary,objective,next_step,result,status}"
SAVE_COMPACTION_ALERTS="${AUTO_MEMORY_SAVE_COMPACTION_ALERTS:-0}"
COMPACTION_ALERT_TITLE_PREFIX="${AUTO_MEMORY_COMPACTION_ALERT_TITLE_PREFIX:-Auto memory compaction}"
COMPACTION_ALERT_TAGS="${AUTO_MEMORY_COMPACTION_ALERT_TAGS:-auto-memory,compaction,failure}"
INJECT_TURN_START="${AUTO_MEMORY_INJECT_TURN_START:-}"

if [[ -z "$INJECT_TURN_START" ]]; then
  if [[ "$MODE" == "autosave" ]]; then
    INJECT_TURN_START="0"
  else
    INJECT_TURN_START="1"
  fi
fi

mkdir -p "$(dirname "$PROMPT_OUT")" "$(dirname "$JSONL_LOG")"

CMD=(
  python3 "$LISTENER_SCRIPT"
  --project "$PROJECT"
  --objective "$OBJECTIVE"
  --limit "$LIMIT"
  --output-framing "$OUTPUT_FRAMING"
  --request-id-prefix "$REQUEST_ID_PREFIX"
  --prompt-out "$PROMPT_OUT"
  --jsonl-log "$JSONL_LOG"
  --reinjection-max-chars "$REINJECTION_MAX_CHARS"
  --reinjection-max-estimated-tokens "$REINJECTION_MAX_ESTIMATED_TOKENS"
  --oversize-action "$OVERSIZE_ACTION"
)

case "$MODE" in
  compaction)
    ;;
  autosave)
    CMD+=(--disable-compaction)
    if [[ -n "$AUTO_SAVE_EVENTS" ]]; then
      CMD+=(--auto-save-events "$AUTO_SAVE_EVENTS")
    fi
    ;;
  both)
    if [[ -n "$AUTO_SAVE_EVENTS" ]]; then
      CMD+=(--auto-save-events "$AUTO_SAVE_EVENTS")
    fi
    ;;
  *)
    echo "Unsupported AUTO_MEMORY_MODE: $MODE (expected compaction|autosave|both)" >&2
    exit 2
    ;;
esac

if [[ "$MODE" == "autosave" || "$MODE" == "both" ]]; then
  CMD+=(
    --auto-save-title-prefix "$AUTO_SAVE_TITLE_PREFIX"
    --auto-save-tags "$AUTO_SAVE_TAGS"
    --auto-save-project-field "$AUTO_SAVE_PROJECT_FIELD"
    --auto-save-summary-fields "$AUTO_SAVE_SUMMARY_FIELDS"
  )
fi

if [[ "$INJECT_TURN_START" == "1" ]]; then
  CMD+=(--inject-turn-start)
fi

if [[ -n "$QUERY" ]]; then
  CMD+=(--query "$QUERY")
fi

if [[ -n "$INPUT_FILE" ]]; then
  CMD+=(--input-file "$INPUT_FILE")
fi

if [[ "$QUIET" == "1" ]]; then
  CMD+=(--quiet)
fi

if [[ "$VISUAL_STATUS" == "1" ]]; then
  CMD+=(--visual-status)
fi

if [[ "$SAVE_COMPACTION_ALERTS" == "1" ]]; then
  CMD+=(--save-compaction-alerts)
  CMD+=(--compaction-alert-title-prefix "$COMPACTION_ALERT_TITLE_PREFIX")
  CMD+=(--compaction-alert-tags "$COMPACTION_ALERT_TAGS")
fi

CMD+=("$@")

echo "Starting auto-memory listener" >&2
echo "project=$PROJECT" >&2
echo "objective=$OBJECTIVE" >&2
echo "mode=$MODE" >&2
echo "visual_status=$VISUAL_STATUS" >&2
echo "save_compaction_alerts=$SAVE_COMPACTION_ALERTS" >&2
echo "prompt_out=$PROMPT_OUT" >&2
echo "log=$JSONL_LOG" >&2

exec "${CMD[@]}"

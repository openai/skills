#!/usr/bin/env bash

# Config knobs
LABEL_MIN=5
LABEL_MAX=15
MIN_PANEL_WIDTH=80
DEFAULT_PANEL_WIDTH=96
FRAME_BUFFER=7

detect_term_width() {
  local cols=""
  if [[ -t 1 ]]; then
    if [[ -n "${COLUMNS:-}" ]]; then
      cols="$COLUMNS"
    fi
    if command -v tput >/dev/null 2>&1; then
      local tcols
      tcols=$(tput cols 2>/dev/null || true)
      if [[ "$tcols" =~ ^[0-9]+$ ]]; then
        cols="$tcols"
      fi
    fi
  fi
  if [[ "$cols" =~ ^[0-9]+$ && "$cols" -gt 0 ]]; then
    echo "$cols"
  fi
}

TERM_WIDTH=$(detect_term_width)
if [[ -n "${WRAPPED_WIDTH:-}" && "${WRAPPED_WIDTH}" =~ ^[0-9]+$ ]]; then
  TERM_WIDTH="$WRAPPED_WIDTH"
fi
if [[ -z "$TERM_WIDTH" ]]; then
  TERM_WIDTH=$DEFAULT_PANEL_WIDTH
fi
DATA_LIMIT=$((TERM_WIDTH - 2))
if (( DATA_LIMIT < MIN_PANEL_WIDTH )); then
  DATA_LIMIT=$MIN_PANEL_WIDTH
fi

DECOR_CHUNK=".:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:."
TITLE="OpenAI Codex Wrapped"
SUBTITLE=""

# Defaults (overwritten by stats JSON)
joined_line="Member since unknown"
timezone_line="Local time: unknown"
table_rows=()
hero_line=""
highlight_lines=()
activity_lines=()
column_rows=()
column_head_left="Last 30 days"
column_head_right="Last 7 days"

die() { echo "$*" >&2; exit 1; }

show_help() {
  cat <<'EOF'
Usage: report.sh --stats-file <path> [--layout table|columns]

  --stats-file   Path to the metrics JSON produced by get_codex_stats.py.
  --layout       Layout style (table or columns). Default: columns.
  -h, --help     Show this message and exit.
EOF
}

strip_ansi_len() {
  local raw="$1"
  local clean
  clean=$(printf '%s' "$raw" | perl -pe 's/\e\[[0-9;]*[a-zA-Z]//g')
  printf '%s' "${#clean}"
}

calc_panel_width() {
  local max_seen=0
  for entry in "$@"; do
    local span
    span=$(strip_ansi_len "$entry")
    (( span > max_seen )) && max_seen=$span
  done
  max_seen=$((max_seen + FRAME_BUFFER))
  if (( max_seen < MIN_PANEL_WIDTH )); then
    max_seen=$MIN_PANEL_WIDTH
  fi
  if (( max_seen > DATA_LIMIT )); then
    max_seen=$DATA_LIMIT
  fi
  echo "$max_seen"
}

center_line() {
  local text="$1"
  local width="$2"
  local text_len
  text_len=$(strip_ansi_len "$text")
  local left_pad=$(( (width - text_len) / 2 ))
  local right_pad=$(( width - text_len - left_pad ))
  printf "│%*s%s%*s│\n" "$left_pad" "" "$text" "$right_pad" ""
}

divider_line() {
  local width="$1"
  local left="$2"
  local mid="$3"
  local right="$4"
  local bar="$left"
  for ((i=0; i<width; i++)); do bar+="─"; done
  bar+="$right"
  printf '%s\n' "$bar"
}

split_row() {
  local label="$1"
  local value="$2"
  local l_width="$3"
  local r_width="$4"

  if [[ -z "$label" ]]; then
    label=$(printf "%-${l_width}s" "")
  elif (( ${#label} < LABEL_MIN )); then
    label=$(printf "%-${LABEL_MIN}s" "$label")
  elif (( ${#label} > l_width )); then
    label=$(echo "$label" | cut -c1-$((l_width-3)))...
  else
    label=$(printf "%-${l_width}s" "$label")
  fi

  if (( ${#value} > r_width )); then
    value=$(echo "$value" | cut -c1-$((r_width-3)))...
  else
    value=$(printf "%-${r_width}s" "$value")
  fi

  printf "│ %s │ %s │\n" "$label" "$value"
}

left_line() {
  local text="$1"
  local width="$2"
  local content=" $text"
  content=$(fit_cell "$content" "$width")
  printf "│%s│\n" "$content"
}

fit_cell() {
  local text="$1"
  local width="$2"
  local len
  len=$(strip_ansi_len "$text")
  if (( len > width )); then
    if (( width > 3 )); then
      text=$(echo "$text" | cut -c1-$((width-3)))...
    else
      text=$(echo "$text" | cut -c1-"$width")
    fi
  fi
  printf "%-${width}s" "$text"
}

center_cell() {
  local text="$1"
  local width="$2"
  local text_len
  text_len=$(strip_ansi_len "$text")
  if (( text_len >= width )); then
    printf "%s" "$(fit_cell "$text" "$width")"
    return
  fi
  local left_pad=$(( (width - text_len) / 2 ))
  local right_pad=$(( width - text_len - left_pad ))
  printf "%*s%s%*s" "$left_pad" "" "$text" "$right_pad" ""
}

trim_ws() {
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf "%s" "$s"
}

load_stats() {
  local src="$1"
  [[ -r "$src" ]] || die "Unable to read stats file: $src"
  local tsv
  tsv=$(python3 - "$src" <<'PY'
import json, sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text())
windows = data.get("windows", {})
all_time = windows.get("all_time", {})
last_30 = windows.get("last_30_days", {})
last_7 = windows.get("last_7_days", {})

def triple(key, default="unknown"):
    return (
        all_time.get(key, default),
        last_30.get(key, default),
        last_7.get(key, default),
    )

def compress_time(value: str) -> str:
    if not isinstance(value, str):
        return str(value)
    value = value.replace(" hours", "h").replace(" hour", "h")
    value = value.replace(" minutes", "m").replace(" minute", "m")
    return value

def compress_days(value: str) -> str:
    if not isinstance(value, str):
        return str(value)
    return value.replace(" days", "d").replace(" day", "d")

def compress_peak(value: str) -> str:
    if not isinstance(value, str):
        return str(value)
    return (
        value.replace(" bird", " b")
        .replace(" owl", " o")
        .replace(" day", " d")
        .replace(" eve", " e")
    )

def double_str(key, default="unknown", compress=None, collapse=False):
    _, m, w = triple(key, default)
    if compress:
        m = compress(m)
        w = compress(w)
    if collapse and m == w:
        return str(m)
    return f"30d {m} | 7d {w}"

rows = [
    ("Window", "Last 30 days | Last 7 days"),
    ("Sessions", double_str("sessions_display", "0")),
    ("Assistant messages", double_str("assistant_messages_display", "0")),
    ("Tokens", double_str("total_tokens_display", "0")),
    ("Usage time", double_str("usage_hours_display", "0")),
    ("Biggest day", double_str("biggest_day_display", "unknown")),
    ("Top repo", double_str("top_repo_display", "unknown", collapse=True)),
    ("Longest turn", double_str("longest_turn_display", "unknown")),
]

column_metrics = [
    ("Sessions", "sessions_display"),
    ("Prompts", "user_messages_display"),
    ("Tokens", "total_tokens_display"),
    ("Usage time", "usage_hours_display"),
    ("Biggest day", "biggest_day_display"),
]
stack_sections = [
    ("Last 30 days", "last_30_days"),
    ("Last 7 days", "last_7_days"),
]

joined_display = data.get("joined_display", "unknown")
timezone = data.get("timezone_abbrev") or data.get("timezone", "unknown")
def compress_focus(value: str) -> str:
    return str(value)

print(f"joined_line\tMember since {joined_display}")
print(f"timezone_line\tLocal time: {timezone}")
for label, value in rows:
    print(f"row\t{label}\t{value}")

def format_stack(stat_key: str, value: str) -> str:
    return str(value)

def bar(active: int, total: int, width: int = 10) -> str:
    if total <= 0:
        return "." * width
    ratio = max(0.0, min(1.0, active / total))
    filled = int(round(ratio * width))
    return "#" * filled + "." * (width - filled)

def percent(active: int, total: int) -> str:
    if total <= 0:
        return "0%"
    return f"{int(round(active / total * 100))}%"

all_time = windows.get("all_time", {})
last_30 = windows.get("last_30_days", {})
last_7 = windows.get("last_7_days", {})

high_30_prompts = last_30.get("user_messages_display", "0")
high_30_active = last_30.get("active_days_display", "0")
high_peak = last_30.get("peak_hour_slot", "unknown")
high_streak = last_30.get("usage_streak_display", "unknown")
high_focus = all_time.get("usage_hours_display", "unknown")

print(f"hero_line\t{high_30_prompts} prompts in 30d — peak {high_peak}")
print(f"highlight_line\t{joined_display} | {timezone}")
print(f"highlight_line\tActive days: {high_30_active} in 30d | Streak: {high_streak}")
print(f"highlight_line\tAll-time focus: {high_focus}")

act_30 = last_30.get("active_days", 0)
act_7 = last_7.get("active_days", 0)
bar_30 = bar(int(act_30), 30)
bar_7 = bar(int(act_7), 7)
print(f"activity_line\t30d activity: {bar_30} ({int(act_30)}/30)")
print(f"activity_line\t7d activity:  {bar_7} ({int(act_7)}/7)")

print("column_head\tLast 30 days\tLast 7 days")
for label, stat_key in column_metrics:
    left = format_stack(stat_key, last_30.get(stat_key, "unknown"))
    right = format_stack(stat_key, last_7.get(stat_key, "unknown"))
    print(f"column_row\t{label}\t{left}\t{right}")
for line in data.get("contrib_lines", []):
    print(f"contrib_line\t{line}")
PY
  ) || die "Failed to parse stats JSON: $src"

  while IFS=$'\t' read -r key label value extra; do
    case "$key" in
      joined_line) joined_line="$label" ;;
      timezone_line) timezone_line="$label" ;;
      focus_line) ;;
      row) table_rows+=("${label}"$'\t'"${value}") ;;
      stack_section) stack_rows+=("SECTION"$'\t'"${label}") ;;
      stack_item) stack_rows+=("ITEM"$'\t'"${label}"$'\t'"${value}") ;;
      stack_blank) stack_rows+=("BLANK") ;;
      hero_line) hero_line="$label" ;;
      highlight_line) highlight_lines+=("$label") ;;
      activity_line) activity_lines+=("$label") ;;
      column_head)
        column_head_left="$label"
        column_head_right="$value"
        ;;
      column_row)
        column_rows+=("${label}"$'\t'"${value}"$'\t'"${extra}") ;;
    esac
  done <<<"$tsv"
}

render() {
  local stats_path="$1"
  local layout_override="${2:-}"
  load_stats "$stats_path"
  if ((${#contrib_lines[@]} == 0)); then
    contrib_lines=("Sun  " "Mon  " "Tue  " "Wed  " "Thu  " "Fri  " "Sat  ")
  fi

  holiday_lines=()

  local layout="${WRAPPED_LAYOUT:-columns}"
  if [[ -n "$layout_override" ]]; then
    layout="$layout_override"
  elif [[ -n "${REPORT_LAYOUT:-}" ]]; then
    layout="${REPORT_LAYOUT}"
  fi

  local width_input=("$DECOR_CHUNK" "$TITLE" "$SUBTITLE" "$hero_line")
  width_input+=("${highlight_lines[@]}")
  width_input+=("${activity_lines[@]}")
  if [[ "$layout" == "table" ]]; then
    for row in "${table_rows[@]}"; do
      IFS=$'\t' read -r label value <<<"$row"
      width_input+=("$label" "$value")
    done
  else
    width_input+=("$column_head_left" "$column_head_right")
    for row in "${column_rows[@]}"; do
      IFS=$'\t' read -r label value_left value_right <<<"$row"
      width_input+=("$label" "$value_left" "$value_right")
    done
  fi
  PANEL_WIDTH=$(calc_panel_width "${width_input[@]}")

  local max_label=0
  for row in "${table_rows[@]}"; do
    IFS=$'\t' read -r label value <<<"$row"
    local span
    span=$(strip_ansi_len "$label")
    (( span > max_label )) && max_label=$span
  done
  local left_span=$max_label
  (( left_span < LABEL_MIN )) && left_span=$LABEL_MIN
  (( left_span > LABEL_MAX )) && left_span=$LABEL_MAX
  local right_span=$((PANEL_WIDTH - 5 - left_span))
  if (( right_span < 20 )); then
    right_span=20
    left_span=$((PANEL_WIDTH - 5 - right_span))
    (( left_span < LABEL_MIN )) && left_span=$LABEL_MIN
  fi
  local stack_rows_mode=0
  if (( right_span < 40 )); then
    stack_rows_mode=1
  fi

  divider_line "$((PANEL_WIDTH))" "┌" "─" "┐"
  local deco_line="$DECOR_CHUNK"
  while (( $(strip_ansi_len "$deco_line") < PANEL_WIDTH )); do
    deco_line+="$DECOR_CHUNK"
  done
  deco_line=${deco_line:0:PANEL_WIDTH}
  printf "│%s│\n" "$deco_line"
  center_line "$TITLE" "$PANEL_WIDTH"
  if [[ -n "$SUBTITLE" ]]; then
    center_line "$SUBTITLE" "$PANEL_WIDTH"
  fi
  if [[ -n "$hero_line" ]]; then
    center_line "$hero_line" "$PANEL_WIDTH"
  fi
  printf "│%s│\n" "$deco_line"

  divider_line "$((PANEL_WIDTH))" "├" "─" "┤"
  center_line "Highlights" "$PANEL_WIDTH"
  for ln in "${highlight_lines[@]}"; do
    left_line "$ln" "$PANEL_WIDTH"
  done
  for ln in "${activity_lines[@]}"; do
    left_line "$ln" "$PANEL_WIDTH"
  done
  center_line "" "$PANEL_WIDTH"

  if [[ "$layout" == "table" ]]; then
    local horiz_left="├"; local horiz_mid="┬"; local horiz_right="┤"
    local lbar; printf -v lbar '%*s' $((left_span + 2)) ""; lbar=${lbar// /─}
    local rbar; printf -v rbar '%*s' $((right_span + 2)) ""; rbar=${rbar// /─}
    printf "%s%s%s%s%s\n" "$horiz_left" "$lbar" "$horiz_mid" "$rbar" "$horiz_right"

    for row in "${table_rows[@]}"; do
      IFS=$'\t' read -r label value <<<"$row"
      if (( stack_rows_mode == 1 )) && [[ "$label" == "Window" ]]; then
        continue
      fi
      if (( stack_rows_mode == 1 )) && [[ "$value" == *"|"* ]]; then
        IFS='|' read -r part_a part_b part_c <<<"$value"
        part_a=$(trim_ws "$part_a")
        part_b=$(trim_ws "$part_b")
        part_c=$(trim_ws "$part_c")
        split_row "$label" "$part_a" "$left_span" "$right_span"
        if [[ -n "$part_b" ]]; then
          split_row "" "$part_b" "$left_span" "$right_span"
        fi
        if [[ -n "$part_c" ]]; then
          split_row "" "$part_c" "$left_span" "$right_span"
        fi
      else
        split_row "$label" "$value" "$left_span" "$right_span"
      fi
    done

    local tail_left="└"; local tail_mid="┴"; local tail_right="┘"
    printf "%s%s%s%s%s\n" "$tail_left" "$lbar" "$tail_mid" "$rbar" "$tail_right"
  else
    divider_line "$((PANEL_WIDTH))" "├" "─" "┤"
    local inner_width=$((PANEL_WIDTH))
    local gap=" │ "
    local gap_len=3
    local left_width=$(( (inner_width - gap_len) / 2 ))
    local right_width=$(( inner_width - gap_len - left_width ))
    local head_left
    local head_right
    head_left=$(center_cell "$column_head_left" "$left_width")
    head_right=$(center_cell "$column_head_right" "$right_width")
    printf "│%s%s%s│\n" "$head_left" "$gap" "$head_right"

    for row in "${column_rows[@]}"; do
      IFS=$'\t' read -r label value_left value_right <<<"$row"
      local ltext=" ${label}: ${value_left}"
      local rtext=" ${label}: ${value_right}"
      ltext=$(fit_cell "$ltext" "$left_width")
      rtext=$(fit_cell "$rtext" "$right_width")
      printf "│%s%s%s│\n" "$ltext" "$gap" "$rtext"
    done

    divider_line "$((PANEL_WIDTH))" "└" "─" "┘"
  fi
}

main() {
  local stats_path=""
  local layout_arg=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --stats-file) stats_path="$2"; shift 2 ;;
      --layout) layout_arg="$2"; shift 2 ;;
      -h|--help) show_help; exit 0 ;;
      *) show_help; exit 1 ;;
    esac
  done
  [[ -n "$stats_path" ]] || die "--stats-file is required."
  render "$stats_path" "$layout_arg"
}

main "$@"

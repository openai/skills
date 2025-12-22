---
name: easy-memory
description: Project-local memory logging for history/notes stored as YYYY-MM-DD.log files in the easy-memory directory. Use when you must read today's memory, search memory by English keywords, append structured English log entries with IDs, or update/delete entries by ID. Do not install or run this skill from CODEX_HOME; keep it in the current project directory.
---

# Easy Memory

## Overview

Maintain project-local memory logs inside the easy-memory directory. Each day uses one log file named `YYYY-MM-DD.log`.

## Mandatory workflow (must follow)

1. Before any task, run `scripts/read_today_log.py` to load the full log for today.
2. Before any task, run `scripts/search_memory.py` with English keywords for the task. Choose `--max-results` based on task complexity (this is the memory search depth).
3. Before finishing or submitting any task, append a new entry with `scripts/write_memory.py` following the log rules below.
4. Every log entry must be written in English.

## Log entry format

Each entry is a single line and must end with a timestamp:

```
[ID:<unique-id>] [REF:<ref-level>] [FACT:<true|false>] <content> [TIME:YYYY-MM-DD:HH:MM]
```

Rules:
- Log file name must be `YYYY-MM-DD.log` and use the current date only.
- If today's log file does not exist, create it; otherwise append to the end.
- Each entry must be written in English.
- The timestamp must be the final token of the line and must be accurate to minutes.
- Each entry must include a unique ID, a reference level, and a factual flag.

## Scripts

### Read today's log

```
python3 scripts/read_today_log.py
```

Reads the full log for the current date.

### Search memory

```
python3 scripts/search_memory.py <keyword1> <keyword2> --max-results 5
```

Searches all `.log` files in the easy-memory directory. Keywords must be English. Default `--max-results` is 5.
Results are prioritized in this order:
- Factual entries (`FACT:true`) first
- Higher reference level first (`REF:critical` > `high` > `medium` > `low`, or higher numeric values)
- Newer timestamps first

### Write memory

```
python3 scripts/write_memory.py --content "..." --factual true --ref-level medium
```

Appends a new entry to today's log. Content must be English and single-line. The script generates the unique ID and timestamp.

### Update memory

```
python3 scripts/update_memory.py --id <entry-id> --content "..." --ref-level high --factual false
```

Updates the entry matching the ID across all logs. The timestamp is refreshed to the current time.

Use update when:
- New factual findings contradict older memory entries (especially results from recent searches).
- The latest task outcomes refine or correct existing memory.

### Delete memory

```
python3 scripts/delete_memory.py --id <entry-id>
```

Deletes the entry matching the ID across all logs.

Use delete when:
- Older memory entries are no longer valuable or are misleading.
- A memory entry conflicts with verified facts and should be removed instead of updated.

## Local installation rule

Do not install this skill under `~/.codex/skills` or any global Codex directory. Keep it in the current project directory so logs remain local to the project.

## Reminder to repeat each time

- Every log entry must be written in English.
- Before any task, run `scripts/read_today_log.py` and `scripts/search_memory.py` with English keywords; adjust `--max-results` based on task complexity.
- Before finishing or submitting any task, write a log entry using `scripts/write_memory.py` following the rules above.

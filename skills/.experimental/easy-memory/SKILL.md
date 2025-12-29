---
name: easy-memory
description: Project-local memory logging for history/notes stored as YYYY-MM-DD.log files in ./easy-memory relative to the current working directory. Use when you must read today's memory, search memory by keywords (English preferred), append structured log entries with IDs (English preferred; UTF-8 accepted), or update/delete entries by ID. Logs always go to the working directory even if the skill is installed globally.
---

# Easy Memory

## Overview

Maintain project-local memory logs inside the ./easy-memory directory under the current working directory. Each day uses one log file named `YYYY-MM-DD.log`.

## Initialization (must follow)

Run initialization once per project before any other scripts when:
- `./easy-memory` does not exist, or
- `./easy-memory/init.log` is missing.

Run:

```
python3 scripts/init_memory.py
```

Initialization behavior:
- Create `./easy-memory` if needed.
- Locate `AGENTS.MD` in the project root (current working directory). If missing, create it.
- If `AGENTS.MD` exists, append a rules block to the end:
  ```
  ## easy-memory rules
  - At the start of the current session (before the first task), use the `easy-memory` skill and follow all rules and constraints in its `SKILL.md`.
  - Only re-run memory read/search when necessary for the task.
  ```
- Create `./easy-memory/init.log` containing the same rules block and a `Date: YYYY-MM-DD` line at the end.
- If `init.log` already exists, initialization is skipped and `AGENTS.MD` is not modified.

If you need the absolute usage path for easy-memory scripts, use the directory
containing this `SKILL.md` (the `scripts/` folder sits alongside it). Avoid
persisting absolute paths in project `AGENTS.MD` because different environments
may maintain the same project.

All other scripts require `init.log` to exist and will exit if initialization has not been run.

## Mandatory workflow (must follow)

1. At the start of the current session (before the first task), run `scripts/read_today_log.py` to load the full log for today.
2. At the start of the current session (before the first task), run `scripts/search_memory.py` with English-preferred keywords for the session/task. Only repeat steps 1-2 when necessary for the task. Choose `--max-results` based on task complexity (this is the memory search depth).
3. Before finishing or submitting any task, append a new entry with `scripts/write_memory.py` following the log rules below.
4. Log entries should be written in English when possible; UTF-8 is accepted.

## Log entry format

Each entry is a single line and must end with a timestamp:

```
[ID:<unique-id>] [REF:<ref-level>] [FACT:<true|false>] <content> [TIME:YYYY-MM-DD:HH:MM]
```

Rules:
- Log file name must be `YYYY-MM-DD.log` and use the current date only.
- If today's log file does not exist, create it; otherwise append to the end.
- Entries should be written in English when possible; UTF-8 is accepted.
- The timestamp must be the final token of the line and must be accurate to minutes.
- Each entry must include a unique ID, a reference level, and a factual flag.

## Scripts

### Initialize memory

```
python3 scripts/init_memory.py
```

Runs one-time initialization to create `AGENTS.MD` rules and `./easy-memory/init.log`.

### Read today's log

```
python3 scripts/read_today_log.py
```

Reads the full log for the current date.

### Search memory

```
python3 scripts/search_memory.py <keyword1> <keyword2> --max-results 5
```

Searches all `.log` files in the ./easy-memory directory under the current working directory. Keywords should be English; UTF-8 is accepted. Default `--max-results` is 5.
Results are prioritized in this order:
- Factual entries (`FACT:true`) first
- Higher reference level first (`REF:critical` > `high` > `medium` > `low`, or higher numeric values)
- Newer timestamps first

### Write memory

```
python3 scripts/write_memory.py --content "..." --factual true --ref-level medium
```

Appends a new entry to today's log. Content should be English and single-line; UTF-8 is accepted. The script generates the unique ID and timestamp.

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

## Log location rule

Logs are always stored under `./easy-memory` relative to the directory where you run the scripts. The skill can be installed globally; logs never go to the install directory.

## Reminder to repeat each session

- Log entries should be written in English when possible; UTF-8 is accepted.
- At the start of the current session (before the first task), run `scripts/read_today_log.py` and `scripts/search_memory.py` with English-preferred keywords; adjust `--max-results` based on task complexity. Only repeat when necessary.
- Before finishing or submitting any task, write a log entry using `scripts/write_memory.py` following the rules above.

#!/usr/bin/env python3
"""Read incomplete macOS Reminders as Agent Feeds local_command JSON."""

from __future__ import annotations

import json
import platform
import subprocess
import sys


SCRIPT = r'''
set rows to {}
tell application "Reminders"
  repeat with listRef in lists
    set listName to name of listRef
    set matches to every reminder of listRef whose completed is false
    repeat with remRef in matches
      set bodyText to ""
      set dueText to ""
      try
        set bodyText to body of remRef
      end try
      try
        set dueText to (due date of remRef) as string
      end try
      set end of rows to (id of remRef) & tab & (name of remRef) & tab & bodyText & tab & dueText & tab & listName
    end repeat
  end repeat
end tell
set AppleScript's text item delimiters to linefeed
return rows as text
'''


def main() -> int:
    if platform.system() != "Darwin":
        print(json.dumps({"items": []}))
        return 0
    result = subprocess.run(["osascript", "-e", SCRIPT], check=False, text=True, capture_output=True, timeout=25)
    if result.returncode:
        print(json.dumps({"items": []}))
        print(result.stderr.strip(), file=sys.stderr)
        return 0
    items = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        reminder_id, title, body, due_at, list_name = parts[:5]
        items.append(
            {
                "id": reminder_id or f"{list_name}:{title}:{due_at}",
                "title": title or "(untitled reminder)",
                "content": body or None,
                "source": list_name,
                "starts_at": due_at or None,
                "updated_at": due_at or None,
            }
        )
    print(json.dumps({"items": items}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

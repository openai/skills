#!/usr/bin/env python3
"""Read today's macOS Calendar events as Agent Feeds local_command JSON."""

from __future__ import annotations

import json
import platform
import subprocess
import sys


SCRIPT = r'''
set startDate to current date
set hours of startDate to 0
set minutes of startDate to 0
set seconds of startDate to 0
set endDate to startDate + (1 * days)
set rows to {}
tell application "Calendar"
  repeat with cal in calendars
    set calName to name of cal
    set matches to every event of cal whose start date is greater than or equal to startDate and start date is less than endDate
    repeat with ev in matches
      set evLocation to ""
      try
        set evLocation to location of ev
      end try
      set end of rows to (uid of ev) & tab & (summary of ev) & tab & ((start date of ev) as string) & tab & ((end date of ev) as string) & tab & evLocation & tab & calName
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
        if len(parts) < 6:
            continue
        uid, title, starts_at, ends_at, location, calendar_name = parts[:6]
        items.append(
            {
                "id": uid or f"{calendar_name}:{starts_at}:{title}",
                "title": title or "(untitled event)",
                "content": location or None,
                "source": calendar_name,
                "starts_at": starts_at,
                "ends_at": ends_at,
                "updated_at": starts_at,
            }
        )
    print(json.dumps({"items": items}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

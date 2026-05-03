#!/usr/bin/env python3
"""Read recent macOS Mail inbox messages as Agent Feeds local_command JSON."""

from __future__ import annotations

import json
import platform
import subprocess
import sys


SCRIPT = r'''
set rows to {}
tell application "Mail"
  set messageCount to count of messages of inbox
  set maxItems to 20
  if messageCount < maxItems then set maxItems to messageCount
  repeat with i from 1 to maxItems
    set msg to message i of inbox
    set senderText to ""
    set subjectText to ""
    set dateText to ""
    set previewText to ""
    try
      set senderText to sender of msg
    end try
    try
      set subjectText to subject of msg
    end try
    try
      set dateText to (date received of msg) as string
    end try
    try
      set previewText to content of msg
      if length of previewText > 500 then set previewText to text 1 thru 500 of previewText
    end try
    set end of rows to (message id of msg) & tab & subjectText & tab & senderText & tab & dateText & tab & previewText
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
        message_id, subject, sender, received_at, preview = parts[:5]
        items.append(
            {
                "id": message_id or f"{sender}:{received_at}:{subject}",
                "title": subject or "(no subject)",
                "content": preview or None,
                "source": "Mail Inbox",
                "sender": sender or None,
                "updated_at": received_at or None,
            }
        )
    print(json.dumps({"items": items}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

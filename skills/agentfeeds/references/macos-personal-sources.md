# macOS Personal Sources

Use this reference when the user wants local personal context from macOS apps such as Calendar, Reminders, Notes, Mail, Messages, Safari, Finder, or local folders.

The public catalog includes built-in `mac/*` templates. Prefer these before creating operator-local templates.

## Discover

Find available Mac templates:

```bash
python3 scripts/agentfeeds.py templates find mac
```

Useful built-ins include:

- `mac/calendar-today`: today's Calendar.app agenda
- `mac/calendar-upcoming`: next 7 days of Calendar.app events
- `mac/reminders-pending`: pending Reminders.app items
- `mac/notes-recent`: recently modified Notes.app notes
- `mac/mail-unread`: unread Mail.app messages
- `mac/imessage-unread`: unread iMessage conversations
- `mac/safari-reading-list`: Safari Reading List items
- `mac/finder-recent-downloads`: recent items in Downloads

## Subscribe

Subscribe only the sources the user asks for:

```bash
python3 scripts/agentfeeds.py subscribe mac/calendar-today
python3 scripts/agentfeeds.py subscribe mac/reminders-pending
python3 scripts/agentfeeds.py subscribe mac/mail-unread
```

Then check health:

```bash
python3 scripts/agentfeeds.py streams health --json
```

## Permissions

Mac templates are read-only, but the host process may need user-granted macOS permissions:

- Calendar templates may require Calendar permission.
- Reminders templates may require Reminders permission.
- Notes and Mail templates may require Automation permission for the relevant app.
- iMessage reads `~/Library/Messages/chat.db` and may require Full Disk Access.
- Safari Reading List reads `~/Library/Safari/Bookmarks.plist`.
- Finder Downloads reads `~/Downloads`.

If a source fails with a macOS permission error, tell the user which permission is needed, then refresh that one stream:

```bash
python3 scripts/agentfeeds.py refresh --stream <subscription-id>
```

## Answering

For questions like "what is on my calendar today?", "what reminders are still open?", or "what recent mail needs attention?", search local state first:

```bash
python3 scripts/agentfeeds.py search <topic> --json
```

Read the matching stream before answering:

```bash
python3 scripts/agentfeeds.py streams read <subscription-id> --limit 20 --json
```

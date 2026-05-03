# macOS Personal Sources

Use this reference when the user wants local personal context from macOS apps such as Calendar, Reminders, or Mail.

These sources are local `local_command` templates. They read from macOS apps through AppleScript, may trigger macOS Automation or app-data permission prompts on first refresh, and are pending until the operator approves each command.

## Install Templates

Install the local templates:

```bash
python3 scripts/agentfeeds.py admin macos install-templates --json
```

This creates:

- `macos/calendar-today`: today's local Calendar events
- `macos/reminders-open`: incomplete Reminders items
- `macos/mail-inbox-recent`: recent Mail inbox messages

## Approval

For each source the user wants, tell the user to run the approval command in an interactive terminal:

```bash
python3 scripts/agentfeeds.py admin templates approve-command macos/calendar-today
python3 scripts/agentfeeds.py admin templates approve-command macos/reminders-open
python3 scripts/agentfeeds.py admin templates approve-command macos/mail-inbox-recent
```

Do not approve on the user's behalf. Approval prints the exact command and requires typing `APPROVE`.

## Subscribe

After approval, subscribe only the sources the user chose:

```bash
python3 scripts/agentfeeds.py subscribe macos/calendar-today --title "Calendar today"
python3 scripts/agentfeeds.py subscribe macos/reminders-open --title "Open reminders"
python3 scripts/agentfeeds.py subscribe macos/mail-inbox-recent --title "Recent inbox mail"
```

Then check health:

```bash
python3 scripts/agentfeeds.py streams health --json
```

If a source fails with a macOS permission error, tell the user to grant the requested Automation/app permission in System Settings, then refresh that one stream:

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

---
name: desktop-notify
description: Send desktop notifications on macOS/Linux (terminal-notifier / notify-send) with an optional project-title wrapper.
metadata:
  short-description: Desktop notifications (macOS/Linux)
---

# Desktop Notify

Send a short status update to the user via a desktop notification.

This skill bundles two scripts:

- `scripts/desktop-notify.sh`: Send a notification with an explicit title.
- `scripts/project-notify.sh`: Derive a project title (basename) then send a notification.

## Quick start

Project-title wrapper (recommended):

```bash
bash "<path-to-skill>/scripts/project-notify.sh" "Done" --level success
```

Custom title:

```bash
bash "<path-to-skill>/scripts/desktop-notify.sh" \
  --title "my-project" \
  --message "Done" \
  --level info
```

## Behavior

- macOS: uses `terminal-notifier` when installed.
- Linux: uses `notify-send` (libnotify) when installed.
- Missing backend: silent no-op by default.
- Unsupported OS: silent no-op.

## Environment

- `CODEX_DESKTOP_NOTIFY=0`: disable notifications (default: enabled)
- `CODEX_DESKTOP_NOTIFY_HINTS=1`: print a one-line install hint when backend is missing (default: disabled)
- `PROJECT_PATH`: used by `scripts/project-notify.sh` to derive the project title (fallback: git root, then `$PWD`)

## Install hints

- macOS: `brew install terminal-notifier`
- Linux (Debian/Ubuntu): `sudo apt-get install libnotify-bin`
- Linux (Fedora): `sudo dnf install libnotify`

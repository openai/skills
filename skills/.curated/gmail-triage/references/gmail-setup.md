# Gmail Setup

1) Enable IMAP access
- Gmail > Settings > See all settings > Forwarding and POP/IMAP
- Turn IMAP access ON

2) Use an App Password
- Enable 2-Step Verification on your Google account
- Create an App Password for Mail
- Export `GMAIL_APP_PASSWORD` with that value

3) Optional: avoid interactive credentials in logs
- Store values in `~/.config/env/global.env`:

```bash
GMAIL_USERNAME=you@example.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx
GMAIL_IMAP_SERVER=imap.gmail.com
GMAIL_IMAP_PORT=993
```

Then run:

```bash
python3 scripts/triage.py --since-days 2 --max 20
```

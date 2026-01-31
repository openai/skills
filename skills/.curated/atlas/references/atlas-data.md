# Atlas Data Paths (macOS)

Atlas stores Chromium-style profile data under:

- `~/Library/Application Support/com.openai.atlas/browser-data/host/Local State`
- Profiles under: `~/Library/Application Support/com.openai.atlas/browser-data/host/<profile>`

Key files in the active profile:

- `History` (SQLite DB, table `urls`)
- `Bookmarks` (JSON)

The active profile is derived from `profile.last_used` in `Local State`, with a fallback to `Default`.

## AppleScript Assumptions

Atlas appears to expose a Safari-style AppleScript dictionary with:

- `every window`
- `every tab of w`
- `active tab index`
- `make new tab with properties {URL:"..."}`
- `close tab <n>`
- `reload tab <n>`

Treat Atlas as a single app with one AppleScript target.

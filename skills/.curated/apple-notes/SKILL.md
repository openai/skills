---
name: apple-notes
description: Create, list, update, search, delete, and count Apple Notes on macOS. Use when automating Notes tasks like finding notes, updating note content, deleting by exact title, and checking note totals.
---

# Apple Notes

Manage Apple Notes using the local bash CLI backed by `osascript`.

## Operating rules

1. `create` and `update` use HTML body payload (`--body` or `--body-file`).
2. `update` and `delete` locate notes by exact title (`--title`).
3. If multiple notes share the same title, disambiguate by modification date.
4. Default scope is `folder "Notes"` in `account 1`.

## Requirements

- macOS with Apple Notes.
- `osascript` available on PATH.
- Terminal automation permission for Notes in macOS Settings.

## Run

```bash
bash scripts/notes_cli.sh help
```

## Commands

Prefer `--body-file` as default path. Use inline `--body` only for short one-line HTML because shell quoting/newlines can break payloads.

Create from file (recommended):

```bash
bash scripts/notes_cli.sh create --body-file /tmp/note.html
```

Create with inline body (simple cases only):

```bash
bash scripts/notes_cli.sh create --body "<div>Short text</div>"
```

List latest notes:

```bash
bash scripts/notes_cli.sh list-latest --limit 20
```

Search by title:

```bash
bash scripts/notes_cli.sh search-title --query "zagreb" --limit 20
```

Search by title or body:

```bash
bash scripts/notes_cli.sh search-any --query "zagreb" --limit 20
```

Update body by exact title:

```bash
bash scripts/notes_cli.sh update --title "Title" --body-file /tmp/new-body.html
```

Delete flow:

1. Run `search-title` or `search-any`.
2. If output shows multiple same titles, ask user to choose by modification date.
3. Run delete on the chosen exact title.

```bash
bash scripts/notes_cli.sh delete --title "Title"
```

Count notes:

```bash
bash scripts/notes_cli.sh count
```

Optional scope override for any command:

```bash
--folder "Notes" --account-index 1
```

## Writing good notes

### What makes a note good

A good note in Apple Notes is easy to understand fast and useful later. It captures one idea, stays readable, and is structured so you can scan it. You should be able to quickly answer: what is the idea, why it matters, and when to use it. If it still makes sense months later without extra context, it is a good note.

### Title rules

Write the title as a clear statement, not a category. Keep it short but specific so it works in search and still makes sense later. Include the key concept words you would search for, and remove filler words like `notes`, `summary`, `chapter`, or `thoughts`.

Useful title patterns:

- `X causes Y`
- `X is better than Y for Z`
- `If X then Y`
- `X fails when ...`
- `Why X matters`
- `How X works`

### Body formatting rules

- After the note title, leave one empty line.
- Start with one short sentence that states the main idea or takeaway.
- Leave another empty line, then use short paragraphs or short bullet lists.
- Keep paragraphs to 1 to 3 lines.
- Use one blank line between blocks.
- If you add a list, keep it small (usually 3 to 6 items).
- Put examples on their own lines so they are easy to spot.

### What to avoid

- Do not mix many unrelated ideas in one note; split them.
- Avoid label prefixes like `Description:`, `Chapter:`, `Topic:`, `Summary:`.
- Avoid vague filler like `interesting` or `important` without saying what changed, what to do, or what to watch for.
- Avoid long unstructured blocks; if it is hard to scan, it is hard to reuse.

### Examples

Example 1

```
Active recall beats rereading

Trying to remember shows what you do not know and makes learning stick.

* Close the text and write 5 points from memory
* Then reopen and fix the gaps
* Repeat later with a shorter test
```

Example 2

```
Clear constraints make decisions easier

Decisions get faster and calmer when you set must haves first.

Must haves

* Under 1.5 kg
* Battery 8 hours
* Quiet fan

Then compare options only against these constraints.
```

When creating or updating note content, compose it using these writing rules first, then pass it with `--body-file`.

## Base template

Use this default body skeleton for structured notes:

```html
<div><h1>{{TITLE}}</h1></div>
<div><br/></div>
<div>{{ONE_SENTENCE_TAKEAWAY}}</div>
<div><br/></div>
<div>{{BODY_BLOCK_OR_LIST}}</div>
```

## HTML formatting support

Supported elements: `h1`...`h6`, `p`, `br`, `strong`, `em`, `code`, `blockquote`, `ul`, `ol`, nested lists, `pre` + `code`, `a`, `img`, `table`, `thead`, `tbody`, `hr`.

Compact multi-format example:

```bash
cat >/tmp/notes_format_example.html <<'HTML'
<html><head><meta charset="utf-8"></head><body>
<h1>Title</h1><p><strong>Bold</strong> <em>Italic</em> <code>code</code></p>
<blockquote><p>Quote</p></blockquote><ul><li>One</li><li>Two</li></ul>
<pre><code>print("hello")</code></pre><p><a href="https://example.com">link</a></p>
<p><img src="https://example.com/image.png" alt="img"></p>
<table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td>2</td></tr></table><hr>
</body></html>
HTML

bash scripts/notes_cli.sh create --body-file /tmp/notes_format_example.html
```

## Command outputs

- `create`: `Created: <name>`
- `list-latest`: starts with `Total notes:` and `Showing latest:`
- `search-title` and `search-any`: `No matches` or starts with `Total matches:`
- `update`: `Updated: <name>`; duplicate title returns list starting with `More than one note has this title.`
- `delete`: `Deleted`; duplicate title returns list starting with `More than one note has this title.`
- `count`: `Total notes: <number>`
- `update` and `delete` missing title target: AppleScript error contains `Note not found`

## Troubleshooting

- `Not authorized to send Apple events to Notes`: grant Terminal automation access to Notes.
- `Folder ... not found`: pass valid `--folder` or use defaults.
- `Note not found`: run search first and confirm exact title.

## Resources

- `scripts/notes_cli.sh`
- `agents/openai.yaml`

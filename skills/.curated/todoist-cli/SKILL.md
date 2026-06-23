---
name: todoist-cli
description: Manage Todoist tasks, projects, labels, sections, and comments using the `td` CLI; use for listing, adding, updating, completing, and filtering Todoist items.
---

# Todoist CLI (td)

## Prerequisites

- Ensure `td` is installed and authenticated.
- Check auth with `td auth status`.
- If not authenticated, run `td auth login` or set `TODOIST_API_TOKEN`.

## Quick Reference

- `td today` - Tasks due today and overdue
- `td inbox` - Inbox tasks
- `td add "task text"` - Quick add with natural language
- `td task list` - List tasks with filters
- `td task complete <ref>` - Complete a task
- `td project list` - List projects
- `td label list` - List labels

## Output Formats

All list commands support:
- `--json` - JSON output (essential fields)
- `--ndjson` - Newline-delimited JSON (streaming)
- `--full` - Include all fields in JSON
- `--raw` - Disable markdown rendering

## Task References

Tasks can be referenced by:
- Name (fuzzy matched within context)
- `id:xxx` - Explicit task ID

## Commands

### Quick Add

```bash
td add "Buy milk tomorrow p1 #Shopping"
td add "Meeting with John at 3pm" --assignee "john@example.com"
```

### Today & Inbox

```bash
td today                    # Due today + overdue
td today --json             # JSON output
td inbox                    # Inbox tasks
```

### Task Management

```bash
td task list --project "Work"
td task list --label "urgent" --priority p1
td task list --due today
td task list --filter "today | overdue"
td task view "task name"
td task complete "task name"
td task complete id:123456
td task complete "task name" --forever  # Stop recurrence
td task add --content "New task" --due "tomorrow" --priority p2
td task update "task name" --due "next week"
td task move "task name" --project "Personal"
td task delete "task name" --yes
```

### Projects

```bash
td project list
td project view "Project Name"
td project create --name "New Project" --color "blue"
td project update "Project Name" --favorite
td project archive "Project Name"
td project delete "Project Name" --yes
```

### Labels

```bash
td label list
td label create --name "urgent" --color "red"
td label update "urgent" --color "orange"
td label delete "urgent" --yes
```

### Comments

```bash
td comment list --task "task name"
td comment add --task "task name" --content "Comment text"
```

### Sections

```bash
td section list --project "Work"
td section create --project "Work" --name "In Progress"
```

## Priority Mapping

- p1 = Highest priority (API value 4)
- p2 = High priority (API value 3)
- p3 = Medium priority (API value 2)
- p4 = Lowest priority (API value 1, default)

## Examples

### Daily workflow

```bash
td today --json | jq '.results | length'  # Count today's tasks
td inbox --limit 5                          # Quick inbox check
```

### Filter by multiple criteria

```bash
td task list --project "Work" --label "urgent" --priority p1
td task list --filter "today & #Work"
```

### Complete tasks efficiently

```bash
td task complete "Review PR"
td task complete id:123456789
```

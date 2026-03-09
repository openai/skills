---
name: "gh-manage-issues"
description: "Use when a user asks to create, list, update, close, or manage GitHub issues; use `gh` to interact with issues, add labels, assign users, and manage issue workflows."
---

# GitHub Issues Management

## Overview

Use GitHub CLI (`gh`) to manage issues - create, list, update, close, add labels, assign users, and more. This skill provides a comprehensive workflow for GitHub issue management.

Prereq: authenticate with the standard GitHub CLI once (run `gh auth login`), then confirm with `gh auth status` (repo scope required).

## Inputs

- `repo`: path to the repository (default `.`)
- `action`: create, list, view, update, close, add-label, remove-label, assign, unassign
- `issue_number`: issue number (for view, update, close, label operations)
- `title`: issue title (for create)
- `body`: issue body/description (for create)
- `labels`: comma-separated labels (for create or add-label)
- `assignee`: username to assign (for assign)

## Quick Start

### List issues
```bash
gh issue list --repo "owner/repo"
gh issue list --repo "owner/repo" --state all --limit 20
```

### Create issue
```bash
gh issue create --repo "owner/repo" --title "Bug: Login fails" --body "Description here"
gh issue create --repo "owner/repo" --title "Feature Request" --label "enhancement"
```

### View issue
```bash
gh issue view 123 --repo "owner/repo"
gh issue view 123 --repo "owner/repo" --comments
```

### Update issue
```bash
gh issue edit 123 --repo "owner/repo" --title "New Title"
gh issue edit 123 --repo "owner/repo" --add-label "bug"
gh issue edit 123 --repo "owner/repo" --add-assignee "username"
```

### Close issue
```bash
gh issue close 123 --repo "owner/repo"
```

## Workflow

1. Verify gh authentication
   - Run `gh auth status` in the repo
   - If unauthenticated, ask user to run `gh auth login`

2. Determine the action
   - Create: Create a new issue
   - List: List issues with optional filters
   - View: View issue details and comments
   - Update: Edit issue title, body, labels
   - Add-label/remove-label: Manage labels
   - Assign/unassign: Manage assignees
   - Close: Close an issue

3. Execute the action
   - Use appropriate `gh issue` command
   - Use `--json` flag for machine-friendly output when needed

4. Report results
   - Show issue URL for created/updated issues
   - List relevant issues with their numbers and titles

## Examples

### Create a bug report with labels
```bash
gh issue create --title "Bug: Cannot upload files" --body "Steps to reproduce..." --label "bug,high-priority"
```

### List all open issues assigned to you
```bash
gh issue list --assignee "@me" --state open
```

### Add a label to multiple issues
```bash
# First list issues, then add label
gh issue list --label "needs-triage" --json number | jq -r '.[].number' | xargs -I {} gh issue edit {} --add-label "in-progress"
```

### Create issue from template
```bash
gh issue create --title "Issue Title" --body-file /path/to/template.md
```

## Tips

- Use `--jq` flag to filter JSON output: `gh issue list --json title,state,labels`
- Use `--search` flag for complex queries: `gh issue list --search "is:issue is:open label:bug"`
- Use `gh issue develop` to create a branch from an issue
- Use `gh issue comment` to add comments to issues
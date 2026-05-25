# pullndoc

Perform a git pull on an upstream/original codebase directory and generate a comprehensive
markdown document cataloging every change that was pulled in. Designed for teams
maintaining forks that need a detailed record of upstream evolution.

## Usage

```
pullndoc <upstream-dir>
```

- `<upstream-dir>` -- Path to the upstream/original repo directory
  (e.g., `.001_ORIGINAL`)

## Rules

1. **Document everything** -- Every changed file must appear in the output document;
   never omit, skip, or summarize away any file from the diff
2. **Read full diffs** -- Read complete file diffs, not just stat summaries; if the
   diff is very large, paginate through it completely before writing the doc
3. **Explain intent** -- Describe the functional purpose of changes (bug fix, new
   feature, refactor, config change), not just "lines added/removed"
4. **Stop if current** -- If the pull brings no new commits, report "Already up to
   date" and stop
5. **Read-only on spec system** -- Never modify state.json, session specs, or task
   checklists
6. **ASCII only** -- Output file uses characters 0-127 only

## Steps

### 1. Snapshot current state before pulling

Change into the upstream directory provided by the user.

Record the current HEAD commit hash:
```bash
git rev-parse HEAD
```
Save this as `$BEFORE_SHA`.

Record the current branch name.

### 2. Execute the pull

Run `git pull`.

Record the new HEAD commit hash as `$AFTER_SHA`.

If `$BEFORE_SHA == $AFTER_SHA`, report "Already up to date" and HALT -- do not
continue to subsequent steps.

### 3. Analyze ALL changes between $BEFORE_SHA and $AFTER_SHA

Run all three of these to build a complete picture:

```bash
git log --oneline $BEFORE_SHA..$AFTER_SHA
```
List every commit pulled in.

```bash
git diff --stat $BEFORE_SHA..$AFTER_SHA
```
Get the full file-level change summary.

```bash
git diff $BEFORE_SHA..$AFTER_SHA
```
Read the **complete diff** for every changed file. Do not skip or summarize any
file. If the diff is very large, paginate through it completely.

### 4. Generate the documentation

Create a markdown file at:
```
<upstream-dir>/docs/upstream-pull-<YYYY-MM-DD>.md
```

Create the `docs/` directory inside the upstream dir if it does not exist.

Structure the document as follows:

```
# Upstream Pull -- <date>

## Summary
- Branch: <branch name>
- Previous HEAD: <short sha + commit message>
- New HEAD: <short sha + commit message>
- Total commits pulled: N
- Files changed: N | Insertions: N | Deletions: N

## Commit Log
(List each commit: sha, author, date, message)

## Changes by File
For EVERY changed file, document:
- File path and change type (added / modified / deleted / renamed)
- What changed and why -- describe the functional purpose of the diff:
  new features, bug fixes, refactors, config changes, dependency updates, etc.
- Key code changes -- quote or paraphrase the most significant hunks

## Breaking Changes & Migration Notes
(Flag anything that could affect downstream code: renamed exports, changed
function signatures, removed features, dependency version bumps, schema changes,
altered env vars, etc. State "None detected" if applicable.)
```

## Output

The generated markdown file path is reported to the user along with a brief summary:
- Number of commits pulled
- Number of files changed
- Whether any breaking changes were detected
- The full path to the documentation file

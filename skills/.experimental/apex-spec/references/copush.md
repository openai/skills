# copush

Pull the latest from origin, increment the project version, commit all non-gitignored
changes, and push to origin. Designed as a single command to bundle routine
commit-and-push workflows without manual version tracking.

## Rules

1. **Origin only** - Pull and push to `origin` remote only; never touch `upstream`
2. **Clean merge or halt** - If the pull results in conflicts or a non-fast-forward situation that cannot be cleanly auto-merged, stop immediately and explain the situation to the user
3. **No attributions** - Do NOT add co-author lines, signed-off-by, or any attribution metadata to the commit
4. **Commit everything** - Stage and commit ALL non-gitignored changes in the repo, not just files you touched in the current session
5. **Read-only on spec system** - Never modify state.json, session specs, or task checklists (version files are fine)
6. **ASCII only** - Commit messages use characters 0-127 only

## Steps

### 1. Pull from origin

Run `git pull origin <current-branch>` to fetch and merge the latest changes.

If the merge is clean (fast-forward or auto-merge with no conflicts), proceed.

If there are merge conflicts or the merge cannot complete cleanly:
- Abort the merge with `git merge --abort`
- Report the conflict details to the user
- HALT -- do not continue to subsequent steps

### 2. Increment the project version

Look for version strings in the project. Common locations include:
- `README.md` (e.g., `**Version: X.Y.Z**`)
- `package.json` (`"version": "X.Y.Z"`)
- `plugin.json` / `marketplace.json`
- `SKILL.md`
- Any files listed in project instructions under version update instructions

Increment the **patch** version (e.g., `1.0.3` becomes `1.0.4`). If the version
contains a pre-release tag (e.g., `1.0.3-beta`), increment the patch but preserve
the tag (e.g., `1.0.4-beta`).

If no version string can be found anywhere in the project, initialize versioning
at `0.1.0` in all standard locations appropriate for the project type:
- **Node/JS/TS projects**: `package.json` (`"version": "0.1.0"`)
- **Python projects**: `pyproject.toml` or `setup.py`
- **Rust projects**: `Cargo.toml`
- **Go projects**: Add a `VERSION` file (Go lacks a manifest version field)
- **Ruby projects**: `Gemfile` or `.gemspec`
- **Java projects**: `pom.xml` or `build.gradle`
- **Always**: `README.md` (add a `**Version: 0.1.0**` line near the top)
- **Plugin projects**: `plugin.json`, `marketplace.json`, `SKILL.md` if they exist

Only add to locations that already exist or are standard for the detected stack.
Do not create manifest files that the project does not already have.
Note the initialization in the commit message.

### 3. Stage all changes

Before staging, review `git status` output for files that should NOT be committed.
Watch for and exclude:

- **Secrets/credentials**: `.env`, `*.pem`, `*.key`, credentials files, API keys
- **Build artifacts**: `__pycache__/`, `*.pyc`, `node_modules/`, `dist/`, `build/`
- **OS/editor junk**: `.DS_Store`, `Thumbs.db`, `.vscode/settings.json`, `*.swp`
- **Large binaries**: database files, media assets, compiled binaries

If any of these are present and not already covered by `.gitignore`, add the
appropriate entries to `.gitignore` BEFORE staging. Then run `git add -A` to stage
every non-gitignored file in the repository. This includes work from outside the
current session that the user may have pending.

After staging, run `git diff --cached --stat` and scan the file list one more time
to confirm nothing sensitive or unintended slipped through.

### 4. Commit

Create a single commit with a concise, descriptive message summarizing the changes.
Do NOT include any co-author, signed-off-by, or attribution lines.

### 5. Push to origin

Run `git push origin <current-branch>`.

If the push is rejected (e.g., remote has new commits since the pull), report the
situation and HALT. Do not force-push.

## Output

Report:
- Whether the pull was clean
- Which files had the version bumped (and from/to values)
- The commit hash and message
- Whether the push succeeded
- Any warnings, errors, or issues encountered at any step

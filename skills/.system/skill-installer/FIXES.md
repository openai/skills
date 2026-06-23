# Fix Records

## Root path git installs

Date: 2026-06-23

### Problem

Installing a skill from the repository root with the git fallback path could copy only
top-level files and omit nested directories such as `assets/`, `agents/`, or
`scripts/`.

This affected commands like:

```bash
scripts/install-skill-from-github.py --repo owner/repo --path . --method git
```

### Cause

The git fallback always used sparse checkout. Passing `.` to
`git sparse-checkout set` checked out only files at the repository root instead
of the full tree needed for a root-level skill.

### Fix

The installer now treats `.` as a repository-root skill path and uses a full
shallow checkout instead of sparse checkout for that case. Non-root skill paths
continue to use sparse checkout.

When installing `--path .` without `--name`, the default destination skill name
is now derived from the repository name.

### Verification

- Ran `python3 -m py_compile` against the installer script.
- Installed `zenbordercom/agent-team-skill` with `--method git --path .`.
- Verified nested files under `assets/`, `agents/`, and `scripts/` were present
  in the installed skill directory.

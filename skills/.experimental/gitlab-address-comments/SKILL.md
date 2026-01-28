---
name: gitlab-address-comments
description: Help address review/issue comments on the open GitLab MR for the current branch using glab CLI. Use when the user wants help addressing review/issue comments on an open GitLab MR
metadata:
  short-description: Address comments in a GitLab MR review
---

# MR Comment Handler

Find the open MR for the current branch and address its review threads using `glab`. Run all `glab` commands with elevated network access.

## Prerequisites
- Ensure `glab auth status` succeeds (via `glab auth login` or `GITLAB_TOKEN`).
- Ensure `glab` is at least v1.80.4.
- When sandboxing blocks network calls, rerun with `sandbox_permissions=require_escalated`.
- Sanity check auth up front:
```bash
glab auth status
```

## 1) Resolve the MR for the current branch
Do a quick check so we know which MR we are about to operate on:
```bash
branch="$(git rev-parse --abbrev-ref HEAD)"
glab mr view "$branch" --output json
```
If this fails, the fetch script below will still try to locate the MR by `source_branch`.

## 2) Fetch unresolved discussions to `/tmp`
Use the local script to fetch MR discussions via `glab api`. This filters out bot/system-only threads and returns unresolved discussions when `--open-comments` is set.
```bash
skill_dir="<path-to-skill>"
branch="$(git rev-parse --abbrev-ref HEAD)"
safe_branch="${branch//\//_}"
out="/tmp/${safe_branch}_mr_open_discussions.json"
python "$skill_dir/scripts/fetch_comments.py" --open-comments --output "$out"
```
If you want the full payload (including resolved discussions), drop `--open-comments`.

## 3) Summarize, triage, and ask once
- Load the JSON and number each unresolved discussion.
- Start with a compact summary list instead of dumping full threads.
- Sort by: unresolved first (already filtered), then most recently updated.
- When possible, group or label by file path to reduce context switching.
- In the summary list, show: number, discussion id, author, file:line (if present), and a one-line summary.
- Ask for a batch selection in one shot. Accept: `1,3,5-7`, `all`, `none`, or `top N`.
- If the user does not choose, suggest a small default set (for example `top 3`) with a short rationale.
- Only after selection, show the full thread and code context for the selected numbers.
- When showing code context, include 3 lines before and after and clearly mark the referenced line(s).

## 4) Implement fixes for the selected discussions
- Apply focused fixes that address the selected threads.
- Run the most relevant tests or checks you can in-repo.
- Report back with: what changed, which discussion numbers were addressed, and any follow-ups.

Notes:
- If `glab` hits auth or rate issues, prompt the user to run `glab auth login` or re-export `GITLAB_TOKEN`, then retry.
- If no open MR is found for the branch, say so clearly and ask for the MR URL or IID.
- Do not prompt “address or skip?” one comment at a time unless the user explicitly asks for that mode.

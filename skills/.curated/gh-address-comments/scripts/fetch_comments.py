#!/usr/bin/env python3
"""
Fetch all PR conversation comments + reviews + review threads (inline threads)
for the PR associated with the current git branch, by shelling out to:

  gh api graphql

Requires:
  - `gh auth login` already set up
  - current branch has an associated (open) PR, or --pr is supplied

Usage:
  python fetch_comments.py --repo "."
  python fetch_comments.py --repo "." --pr 123
  python fetch_comments.py --repo "." --pr "https://github.com/org/repo/pull/456" --json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

QUERY = """\
query(
  $owner: String!,
  $repo: String!,
  $number: Int!,
  $commentsCursor: String,
  $reviewsCursor: String,
  $threadsCursor: String
) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number
      url
      title
      state

      # Top-level "Conversation" comments (issue comments on the PR)
      comments(first: 100, after: $commentsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          body
          createdAt
          updatedAt
          author { login }
        }
      }

      # Review submissions (Approve / Request changes / Comment), with body if present
      reviews(first: 100, after: $reviewsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          state
          body
          submittedAt
          author { login }
        }
      }

      # Inline review threads (grouped), includes resolved state
      reviewThreads(first: 100, after: $threadsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          diffSide
          startLine
          startDiffSide
          originalLine
          originalStartLine
          resolvedBy { login }
          comments(first: 100) {
            nodes {
              id
              body
              createdAt
              updatedAt
              author { login }
            }
          }
        }
      }
    }
  }
}
"""


def _run(cmd: list[str], stdin: str | None = None, cwd: Path | None = None) -> str:
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, cwd=cwd)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr}")
    return p.stdout


def _run_json(cmd: list[str], stdin: str | None = None, cwd: Path | None = None) -> dict[str, Any]:
    out = _run(cmd, stdin=stdin, cwd=cwd)
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON from command output: {e}\nRaw:\n{out}") from e


def _ensure_gh_authenticated(cwd: Path | None = None) -> None:
    try:
        _run(["gh", "auth", "status"], cwd=cwd)
    except RuntimeError:
        print("run `gh auth login` to authenticate the GitHub CLI", file=sys.stderr)
        raise RuntimeError(
            "gh auth status failed; run `gh auth login` to authenticate the GitHub CLI"
        ) from None


def _find_git_root(start: Path) -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def gh_pr_view_json(fields: str, cwd: Path | None = None) -> dict[str, Any]:
    return _run_json(["gh", "pr", "view", "--json", fields], cwd=cwd)


def get_current_pr_ref(cwd: Path | None = None) -> tuple[str, str, int]:
    """
    Resolve the PR for the current branch (whatever gh considers associated).
    Works for cross-repo PRs too, by reading head repository owner/name.
    """
    pr = gh_pr_view_json("number,headRepositoryOwner,headRepository", cwd=cwd)
    owner = pr["headRepositoryOwner"]["login"]
    repo = pr["headRepository"]["name"]
    number = int(pr["number"])
    return owner, repo, number


def get_pr_ref_from_value(
    pr_value: str, cwd: Path | None = None
) -> tuple[str, str, int]:
    """
    Resolve owner, repo, and number from an explicit PR number or URL.

    If ``pr_value`` is a URL we parse it directly.  If it is a bare number we
    ask ``gh pr view`` to resolve it against the current repo.
    """
    if pr_value.startswith("http://") or pr_value.startswith("https://"):
        parts = [p for p in pr_value.split("/") if p]
        # https: / / github.com / owner / repo / pull / number
        try:
            idx = parts.index("pull")
            owner = parts[idx - 2]
            repo = parts[idx - 1]
            number = int(parts[idx + 1])
            return owner, repo, number
        except (ValueError, IndexError):
            pass

    # Treat it as a number and let gh resolve the rest
    pr = _run_json(
        ["gh", "pr", "view", pr_value, "--json", "number,headRepositoryOwner,headRepository"],
        cwd=cwd,
    )
    owner = pr["headRepositoryOwner"]["login"]
    repo = pr["headRepository"]["name"]
    number = int(pr["number"])
    return owner, repo, number


def gh_api_graphql(
    owner: str,
    repo: str,
    number: int,
    comments_cursor: str | None = None,
    reviews_cursor: str | None = None,
    threads_cursor: str | None = None,
    cwd: Path | None = None,
) -> dict[str, Any]:
    """
    Call `gh api graphql` using -F variables, avoiding JSON blobs with nulls.
    Query is passed via stdin using query=@- to avoid shell newline/quoting issues.
    """
    cmd = [
        "gh",
        "api",
        "graphql",
        "-F",
        "query=@-",
        "-F",
        f"owner={owner}",
        "-F",
        f"repo={repo}",
        "-F",
        f"number={number}",
    ]
    if comments_cursor:
        cmd += ["-F", f"commentsCursor={comments_cursor}"]
    if reviews_cursor:
        cmd += ["-F", f"reviewsCursor={reviews_cursor}"]
    if threads_cursor:
        cmd += ["-F", f"threadsCursor={threads_cursor}"]

    return _run_json(cmd, stdin=QUERY, cwd=cwd)


def fetch_all(owner: str, repo: str, number: int, cwd: Path | None = None) -> dict[str, Any]:
    conversation_comments: list[dict[str, Any]] = []
    reviews: list[dict[str, Any]] = []
    review_threads: list[dict[str, Any]] = []

    comments_cursor: str | None = None
    reviews_cursor: str | None = None
    threads_cursor: str | None = None

    pr_meta: dict[str, Any] | None = None

    while True:
        payload = gh_api_graphql(
            owner=owner,
            repo=repo,
            number=number,
            comments_cursor=comments_cursor,
            reviews_cursor=reviews_cursor,
            threads_cursor=threads_cursor,
            cwd=cwd,
        )

        if "errors" in payload and payload["errors"]:
            raise RuntimeError(f"GitHub GraphQL errors:\n{json.dumps(payload['errors'], indent=2)}")

        pr = payload["data"]["repository"]["pullRequest"]
        if pr_meta is None:
            pr_meta = {
                "number": pr["number"],
                "url": pr["url"],
                "title": pr["title"],
                "state": pr["state"],
                "owner": owner,
                "repo": repo,
            }

        c = pr["comments"]
        r = pr["reviews"]
        t = pr["reviewThreads"]

        conversation_comments.extend(c.get("nodes") or [])
        reviews.extend(r.get("nodes") or [])
        review_threads.extend(t.get("nodes") or [])

        comments_cursor = c["pageInfo"]["endCursor"] if c["pageInfo"]["hasNextPage"] else None
        reviews_cursor = r["pageInfo"]["endCursor"] if r["pageInfo"]["hasNextPage"] else None
        threads_cursor = t["pageInfo"]["endCursor"] if t["pageInfo"]["hasNextPage"] else None

        if not (comments_cursor or reviews_cursor or threads_cursor):
            break

    assert pr_meta is not None
    return {
        "pull_request": pr_meta,
        "conversation_comments": conversation_comments,
        "reviews": reviews,
        "review_threads": review_threads,
    }


def render_text(data: dict[str, Any]) -> None:
    """Print a human-readable summary of the fetched PR data."""
    pr = data["pull_request"]
    print(f"PR #{pr['number']}: {pr['title']} ({pr['state']})")
    print(f"URL: {pr['url']}")
    print()

    comments = data.get("conversation_comments") or []
    if comments:
        print(f"--- Conversation comments ({len(comments)}) ---")
        for c in comments:
            author = (c.get("author") or {}).get("login", "unknown")
            print(f"\n[{author}] ({c.get('createdAt', '')}):")
            print(c.get("body", ""))
    else:
        print("--- No conversation comments ---")
    print()

    review_list = data.get("reviews") or []
    if review_list:
        print(f"--- Reviews ({len(review_list)}) ---")
        for r in review_list:
            author = (r.get("author") or {}).get("login", "unknown")
            state = r.get("state", "")
            print(f"\n[{author}] {state} ({r.get('submittedAt', '')}):")
            body = r.get("body", "")
            if body:
                print(body)
    else:
        print("--- No reviews ---")
    print()

    threads = data.get("review_threads") or []
    if threads:
        print(f"--- Review threads ({len(threads)}) ---")
        for idx, t in enumerate(threads, start=1):
            resolved = "RESOLVED" if t.get("isResolved") else "OPEN"
            outdated = " (outdated)" if t.get("isOutdated") else ""
            path = t.get("path", "")
            line = t.get("line", "")
            print(f"\nThread #{idx}: {path}:{line} [{resolved}{outdated}]")
            for tc in (t.get("comments", {}).get("nodes") or []):
                author = (tc.get("author") or {}).get("login", "unknown")
                print(f"  [{author}] ({tc.get('createdAt', '')}):")
                print(f"  {tc.get('body', '')}")
    else:
        print("--- No review threads ---")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch PR comments, reviews, and review threads via GitHub GraphQL.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path inside the target Git repository.",
    )
    parser.add_argument(
        "--pr",
        default=None,
        help="PR number or URL (defaults to current branch PR).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit JSON instead of human-readable text output.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_path = Path(args.repo).resolve()
    git_root = _find_git_root(repo_path)
    if git_root is None:
        print("Error: not inside a Git repository.", file=sys.stderr)
        return 1

    try:
        _ensure_gh_authenticated(cwd=git_root)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        if args.pr:
            owner, repo, number = get_pr_ref_from_value(args.pr, cwd=git_root)
        else:
            owner, repo, number = get_current_pr_ref(cwd=git_root)
    except RuntimeError as exc:
        print(f"Error resolving PR: {exc}", file=sys.stderr)
        return 1

    try:
        result = fetch_all(owner, repo, number, cwd=git_root)
    except RuntimeError as exc:
        print(f"Error fetching comments: {exc}", file=sys.stderr)
        return 1

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        render_text(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

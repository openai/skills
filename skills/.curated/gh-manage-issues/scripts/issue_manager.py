#!/usr/bin/env python3
"""GitHub Issues Manager - Bulk operations helper."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_gh(args: list[str]) -> subprocess.CompletedProcess:
    """Run gh command and return result."""
    result = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)
    return result


def list_issues(repo: str, state: str = "open", labels: str = None, assignee: str = None):
    """List issues with optional filters."""
    args = ["issue", "list", "--repo", repo, "--state", state, "--json", "number,title,labels,assignees,state"]
    if labels:
        args.extend(["--label", labels])
    if assignee:
        args.extend(["--assignee", assignee])
    
    result = run_gh(args)
    issues = json.loads(result.stdout)
    
    if not issues:
        print("No issues found")
        return
    
    for issue in issues:
        labels_str = ", ".join([l["name"] for l in issue.get("labels", [])]) or "no labels"
        assignees_str = ", ".join(issue.get("assignees", [])) or "unassigned"
        print(f"#{issue['number']}: {issue['title']}")
        print(f"   Labels: {labels_str} | Assignees: {assignees_str} | State: {issue['state']}")
        print()


def create_issue(repo: str, title: str, body: str = None, labels: str = None, assignee: str = None):
    """Create a new issue."""
    args = ["issue", "create", "--repo", repo, "--title", title]
    
    if body:
        args.extend(["--body", body])
    if labels:
        for label in labels.split(","):
            args.extend(["--label", label.strip()])
    if assignee:
        args.extend(["--assignee", assignee])
    
    result = run_gh(args)
    print(f"Issue created: {result.stdout.strip()}")


def add_labels(repo: str, issue_num: int, labels: str):
    """Add labels to an issue."""
    args = ["issue", "edit", f"{repo}", "--issue-number", str(issue_num), "--add-label"]
    
    for label in labels.split(","):
        args.append(label.strip())
    
    run_gh(args)
    print(f"Labels added to issue #{issue_num}")


def main():
    parser = argparse.ArgumentParser(description="GitHub Issues Manager")
    parser.add_argument("--repo", required=True, help="Repository (owner/repo)")
    parser.add_argument("--action", choices=["list", "create", "add-labels"], required=True)
    parser.add_argument("--state", default="open", help="Issue state (open/closed/all)")
    parser.add_argument("--labels", help="Filter by labels (comma-separated)")
    parser.add_argument("--assignee", help="Filter by assignee")
    parser.add_argument("--title", help="Issue title (for create)")
    parser.add_argument("--body", help="Issue body (for create)")
    parser.add_argument("--issue", type=int, help="Issue number (for add-labels)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    if args.action == "list":
        list_issues(args.repo, args.state, args.labels, args.assignee)
    elif args.action == "create":
        if not args.title:
            print("Error: --title required for create action", file=sys.stderr)
            sys.exit(1)
        create_issue(args.repo, args.title, args.body, args.labels, args.assignee)
    elif args.action == "add-labels":
        if not args.issue or not args.labels:
            print("Error: --issue and --labels required for add-labels action", file=sys.stderr)
            sys.exit(1)
        add_labels(args.repo, args.issue, args.labels)


if __name__ == "__main__":
    main()
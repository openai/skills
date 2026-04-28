---
name: address-pr-comments
description: Fetch unresolved GitHub pull request review comments with gh, make local code changes to address them, run relevant QA checks, reply to review comments, and resolve all but the final review thread. Use when asked to address unresolved PR comments, review feedback, requested changes, or inline GitHub PR comments from the current branch. Do not commit or push.
---

# Address Unresolved PR Comments

Use the `gh` CLI to inspect and update GitHub pull request review threads. Make local code changes only; never commit or push.

## Workflow

1. Identify the current PR and repository.
2. Fetch unresolved review threads.
3. Read the relevant code for each comment.
4. Make local changes that follow the repository's conventions.
5. Run focused QA checks for the changed code.
6. React and reply to each actionable comment.
7. Resolve all review threads except the last one.
8. Stop and summarize the local changes.

## Fetch Unresolved Comments

Get the current PR number and repository:

```bash
PR_NUMBER=$(gh pr view --json number --jq .number)
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
```

Fetch unresolved review threads:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 10) {
            nodes {
              databaseId
              author { login }
              path
              body
              line
            }
          }
        }
      }
    }
  }
}' -f owner="${REPO%%/*}" -f repo="${REPO##*/}" -F pr=$PR_NUMBER \
  --jq '.data.repository.pullRequest.reviewThreads.nodes[]
    | select(.isResolved == false)
    | {threadId: .id, comments: [.comments.nodes[] | {id: .databaseId, author: .author.login, path: .path, line: .line, body: .body}]}'
```

This query fetches at most 100 review threads and 10 comments per thread. For large PRs, rerun with adjusted pagination or cursor-based paging before concluding there are no more unresolved threads.

## Address Comments

For every unresolved thread:

1. Read the referenced file and nearby code before editing.
2. Decide whether the comment is actionable.
3. If actionable, make the smallest appropriate local code change.
4. If not actionable or no longer applicable, skip the code change and record the reason for the final summary.
5. Run targeted tests, linters, type checks, or format checks that are appropriate for the touched files. Use repository instructions when present. If a check cannot run, record why.

React to each review comment that was handled or intentionally skipped:

```bash
gh api repos/${REPO}/pulls/comments/${COMMENT_ID}/reactions -f content=eyes
```

Reply to each review comment with a concise explanation. Always prefix the reply with `AI: `:

```bash
gh api "repos/${REPO}/pulls/${PR_NUMBER}/comments/${COMMENT_ID}/replies" -f body="AI: <response>"
```

Resolve all review threads except the last unresolved thread. Leave the last thread unresolved so the reviewer receives a notification and can verify the changes:

```bash
gh api graphql -f query='mutation($threadId: ID!) { resolveReviewThread(input: {threadId: $threadId}) { thread { id isResolved } } }' -f threadId="${THREAD_ID}"
```

## Stop Condition

After handling comments, replying, and resolving all but the last thread:

- Do not commit.
- Do not push.
- Do not perform additional GitHub actions.
- Present a summary of code changes, skipped comments, unresolved final thread, and QA results so the human can review.

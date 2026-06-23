---
name: git-commit-helper
description: Generate a commit message based on staged changes. Use when a user asks for a commit message proposal.
metadata:
  short-description: Generate commit message
---

# Git Commit Helper

## Goal

Generate a clear, conventional commit message based on the current staged changes in the repository.

## Workflow

1.  **Read Staged Changes**
    - Executing `git diff --cached` is the primary way to see what will be committed.
    - If there is no output, inform the user that no changes are staged.

2.  **Analyze Changes**
    - Identify the scope of changes (e.g., component, docs, build system).
    - Determine the type of change (feat, fix, docs, style, refactor, test, chore).

3.  **Generate Commit Message**
    - Create a commit message following the [Conventional Commits](https://www.conventionalcommits.org/) specification.
    - **Format**:

      ```
      <type>(<scope>): <description>

      [optional body]

      [optional footer(s)]
      ```

    - Keep the subject line under 50 characters if possible.
    - Use the imperative mood in the subject line (e.g., "Add feature" not "Added feature").

4.  **Present to User**
    - Output the proposed commit message in a code block.
    - Ask the user if they would like to run the commit command or edit the message.

## Examples

**Input:**
`git diff --cached` shows changes to `README.md` adding a new section.

**Output:**

```
docs(readme): add contribution guidelines section
```

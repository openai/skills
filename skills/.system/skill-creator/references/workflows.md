# Workflow Design Patterns for Skills

This guide covers best practices for designing multi-step sequential workflows and conditional logic in skills.

## Overview

Skills often involve multi-step processes with decision points, loops, and conditional branches. This document provides proven patterns for organizing these workflows so Codex can execute them reliably.

## Basic Sequential Workflow

For straightforward linear processes, use a numbered list with clear inputs and outputs:

```markdown
## Process Overview

This workflow accomplishes [specific goal] through these steps:

1. **Step One**
   - Input: [what's needed]
   - Action: [what to do]
   - Output: [what results]

2. **Step Two**
   - Input: [what's needed from previous step]
   - Action: [what to do]
   - Output: [what results]

3. **Step Three**
   - Input: [what's needed]
   - Action: [what to do]
   - Output: [final result]
```

### Example: GitHub PR Comment Handler

```markdown
## Workflow: Address PR Comments

1. **List all comments**
   - Input: Current Git branch with associated PR
   - Action: Run `gh pr view` to find PR number, then fetch comments
   - Output: Numbered list of comments grouped by type (review comments, issue comments, thread comments)

2. **Present options to user**
   - Input: Comment list
   - Action: Ask user which comments to address
   - Output: Selected comment IDs

3. **Apply fixes**
   - Input: Selected comments and current code
   - Action: For each comment, modify code and push commits
   - Output: Updated PR with fixes applied
```

## Conditional Workflows

When a workflow has decision points, use explicit branching:

```markdown
## Workflow: Deploy to [Service]

1. **Validate input**
   - Input: Deployment configuration
   - Action: Check for required fields
   - Output: Valid config or error message

2. **Choose deployment path**
   - If staging environment: Go to step 3a
   - If production environment: Go to step 3b
   - Otherwise: Return error

3a. **Deploy to staging**
   - Input: Code and staging config
   - Action: [specific steps]
   - Output: Deployment confirmation

3b. **Deploy to production**
   - Input: Code and production config
   - Action: [specific steps with extra safety checks]
   - Output: Deployment confirmation

4. **Verify deployment**
   - Input: Deployed service URL
   - Action: Run health checks
   - Output: Success or rollback
```

## Loop Workflows

For repetitive tasks on collections, show the loop structure clearly:

```markdown
## Workflow: Process Multiple Files

1. **Get input**
   - Input: Directory path
   - Action: List all files matching pattern
   - Output: File list

2. **For each file** (loop):
   - Input: Current file path
   - Action: [process the file]
   - Output: Processed file
   - Error handling: [what to do if processing fails]

3. **Aggregate results**
   - Input: All processed files
   - Action: Combine results
   - Output: Final summary
```

## Error Handling and Recovery

Make error paths explicit:

```markdown
## Workflow: Fetch Data with Retry Logic

1. **Attempt fetch**
   - Input: API endpoint
   - Action: Call API with timeout
   - Output: Data or timeout error

2. **Handle errors**
   - If timeout: Wait and retry (max 3 times)
   - If auth error: Prompt user to re-authenticate with `gh auth login`
   - If rate limit: Suggest waiting and retrying later
   - Otherwise: Return error to user

3. **Success path**
   - Input: Successfully fetched data
   - Action: Parse and validate
   - Output: Structured data
```

## Sub-workflows

For complex workflows, break into named sub-procedures:

```markdown
## Main Workflow: Build and Deploy

1. **[Prepare environment]**: See section "Prepare Environment Sub-workflow" below
2. **[Build application]**: See section "Build Application Sub-workflow" below
3. **[Run tests]**: See section "Test Application Sub-workflow" below
4. **[Deploy application]**: See section "Deploy Application Sub-workflow" below

### Prepare Environment Sub-workflow

1. Check dependencies
2. Configure build system
3. Validate configuration

### Build Application Sub-workflow

1. Compile code
2. Bundle assets
3. Create build artifact

[Additional sub-workflows...]
```

## State Management

When workflow state matters, make it explicit:

```markdown
## Workflow: State-Dependent Process

**State variables:**
- `currentPhase`: One of [start, processing, validating, complete]
- `errorCount`: Number of retries attempted
- `results`: Accumulated results from each step

1. **Initialize**
   - Set `currentPhase = "start"`
   - Load previous state if resuming
   - Output: Ready to proceed

2. **Process**
   - While `currentPhase != "complete"` and `errorCount < 3`:
     - Execute step
     - Update `results`
     - If error: increment `errorCount`, retry
     - If success: advance `currentPhase`
   - Output: Final state

3. **Handle completion**
   - Save state (for resumable workflows)
   - Return results
```

## Testing Workflows

When describing workflows, consider these validation questions:

- **Can Codex understand the input requirements?** Are all prerequisites explicitly listed?
- **Is each step deterministic?** Does the step have a single clear outcome?
- **Are error cases handled?** What should happen if a step fails?
- **Can the workflow be resumed?** If a step fails, can the workflow restart from that point?
- **Are decision criteria clear?** If there's branching, are the conditions explicit?

## Best Practices

1. **Keep steps atomic**: Each step should be a single logical unit of work
2. **Explicit transition criteria**: State clearly how Codex knows when to move to the next step
3. **Named branch conditions**: Use `if [condition]: go to step X` rather than implicit branching
4. **Error messages are instructions**: Tell Codex exactly what to do when something fails
5. **Avoid nested conditionals**: Use separate numbered steps instead of deep `if/else` blocks
6. **Include recovery paths**: Every error should have a clear recovery action

## When to Use Scripts Instead

Some workflows should be implemented as executable scripts rather than markdown instructions:

- **Deterministic, fragile operations**: Parsing complex file formats, database queries
- **Operations that repeatedly rewrite the same code**: Boilerplate generation, file manipulation
- **Performance-critical paths**: Operations that would be slow or unreliable if left to Codex
- **External API integrations**: Fetching data reliably from APIs with retries and error handling

For these cases, include a `scripts/` folder and reference the script from the workflow instructions.

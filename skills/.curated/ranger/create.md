# Creating a New Feature Review

Create a feature review when starting new work that doesn't have an existing feature review to resume.

## Basic Command

```bash
ranger create "<feature review name>" \
  --description "<description>" \
  -c "<scenario 1>" \
  -c "<scenario 2>"
```

Use multiple `-c` flags for multiple scenarios. Each scenario can contain commas.

## What Gets Captured Automatically

When you create a feature review, the CLI automatically captures:
- **Git repo URL** - From `git remote get-url origin`
- **Git branch** - From current branch name
- **Created timestamp**
- **Your organization** - From API token

This enables `ranger list` to filter feature reviews by git context later.

## Writing Good Scenarios

**CRITICAL: Scenarios are E2E test flows, NOT a TODO list.**

Ranger verifies scenarios by running them in a real browser. Each scenario must describe a **complete user journey** that can be tested through the UI.

### Key Principles

**Brevity is paramount.** Testing takes developer time. Your job is to identify only the most critical user flows—not to exhaustively cover every scenario.

1. **Start minimal** - Propose **1 scenario** for most features, **2 scenarios max** for large features. You can always add more later if needed.
2. **High-level flows only** - Describe the key user journey at a high level. Don't get granular unless explicitly asked.
3. **E2E flows only** - Each scenario is a test a QA engineer would run in the browser
4. **Must be UI-testable** - No backend-only work, no code changes, no infrastructure tasks
5. **Happy path focus** - Describe the successful user journey, not edge cases

The goal is to quickly validate that the core functionality works—not to build a comprehensive test suite.

### What Scenarios Are NOT

❌ **NOT a TODO list** - Don't list implementation tasks
```
Bad: "Add validation to form"
Bad: "Write unit tests"
Bad: "Refactor auth module"
```

❌ **NOT backend features** - Must be verifiable through UI
```
Bad: "API returns correct response"
Bad: "Database migration runs"
Bad: "Caching layer works"
```

❌ **NOT granular UI checks** - Don't check individual elements
```
Bad: "Button is visible"
Bad: "Form has 3 fields"
Bad: "Error message is red"
```

### What Scenarios ARE

✅ **Complete E2E user flows** that a QA tester would execute:

```
Good: "User can log in with valid credentials and see the dashboard"
Good: "User can add item to cart, proceed to checkout, and complete purchase"
Good: "User can create a new project, invite a team member, and see them in the members list"
```

### Examples

**Bad - implementation tasks:**
```
1. Add login endpoint
2. Create session storage
3. Build login form component
4. Add form validation
```

**Good - E2E flow:**
```
1. User can log in with valid email/password and see their dashboard
```

**Bad - granular checks:**
```
1. Export button appears on Reports page
2. Clicking button opens modal
3. Modal has format dropdown
4. Selecting CSV triggers download
```

**Good - single flow:**
```
1. User can navigate to Reports, click Export, select CSV format, and download the file
```

### When to Use Multiple Scenarios

**Default to 1 scenario.** Only propose 2 scenarios if the feature genuinely requires distinct user journeys.

- Adding a button? **1 scenario** - the complete flow of using it
- Login + signup? **2 scenarios** - these are separate user journeys with different entry points
- Full CRUD? **Start with 1-2 scenarios** - test the core flow first (e.g., create + view), add more only if asked

**Do not** try to cover every permutation. Start high-level, and the developer can request additional coverage if needed.

## Complete Example

**Simple feature (1 scenario):**
```bash
ranger create "Add Export Button" \
  --description "Add export functionality to the reports page" \
  -c "Navigate to Reports page, click the new Export button, select CSV format, and verify the file downloads"
```

**Larger feature (multiple scenarios):**
```bash
ranger create "User Authentication" \
  --description "Login and signup flows for the web app" \
  -c "Go to login page and sign in with valid credentials, verify redirect to dashboard" \
  -c "Go to signup page and create new account, verify welcome email and successful login"
```

## Output

```
Creating feature review...

✅ Feature review created: feat_01abc123

🔄 User Authentication (https://dashboard.ranger.net/features/feat_01abc123)
   Status: in_progress
   Description: Login and signup flows...
   Repository: github.com/myorg/myapp
   Branch: feature/auth
   Created: 1/21/2026, 10:30:00 AM

   Scenarios:
   1. ⬜ Go to login page and sign in...
   2. ⬜ Go to signup page and create...

➡️  Set as active feature review
```

## After Creation

The new feature review is automatically set as the active feature review. You can now:

1. Start implementing the first scenario
2. View status with `ranger show`

Always end the conversational turn by sharing the dashboard link.

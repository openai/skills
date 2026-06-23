# Verifying Scenarios

After implementing code for a scenario, verify it works in the browser. This creates evidence (screenshots, traces, logs) that the implementation is complete.

## Basic Command

```bash
ranger go --scenario <N> --notes "<what to verify>"
```

The URL is derived from your active profile's `baseUrl` setting.

## Required: Active Feature Review

`go` requires an active feature review. If you don't have one:

```bash
ranger list                # Find feature reviews to resume
ranger resume <id>         # Resume a specific feature review
```

## The Verification Flow

1. **Select scenario** - CLI prompts which scenario this verifies
2. **Fetch reviewer feedback** - If the scenario has unaddressed comments or a parent scenario, reviewer comments are automatically injected into the verification prompt
3. **Run browser verification** - Agent executes the task in a real browser
4. **Evaluate results** - Agent determines if the scenario is satisfied (including whether reviewer concerns were addressed)
5. **Update status** - Scenario is marked verified, partial, blocked, or failed
6. **Link evidence** - Session trace is attached to the scenario

### Reviewer Feedback Auto-Injection

When verifying scenarios that have reviewer comments (v2+ scenarios or scenarios with unaddressed comments), the verification agent automatically receives a **"Reviewer Feedback to Address"** section in its prompt. This includes:
- Each reviewer comment with author and date
- The previous version's description
- The canonical flow from prior verification (if available)

You do NOT need to manually include reviewer feedback in your `--notes` description — it's handled automatically. Just make sure you've addressed the feedback in your code before verifying.

## Options

| Option | Required | Description |
|--------|----------|-------------|
| `--profile` | No | Profile to use (defaults to active profile) |
| `--notes` | No | What to verify (defaults to scenario description) |
| `--scenario` | No | Scenario index to verify (skips selection prompt) |
| `--start-path` | No | Path to start on (appended to base URL, e.g., `/dashboard`) |

## Writing Good Task Descriptions

The `--notes` is what the verification agent will actually do. Be VERY specific:

**Bad:**
```bash
--notes "Test login"
```

**Good:**
```bash
--notes "Navigate to /login. Enter test@example.com in email field and password123 in password field. Click the Submit button. Verify a loading spinner appears. Verify redirect to /dashboard within 5 seconds. Verify the user's name appears in the header."
```

## Using Scenario Description as Task

If your scenario has a detailed description, you can omit `--notes`:

```bash
# Scenario 1: "User can log in with valid credentials - sees loading state - redirects to dashboard"
ranger go --scenario 1
```

The scenario description becomes the task automatically.

## Evaluation Results

After verification, the agent evaluates if the result satisfies the scenario:

| Result | Meaning | Scenario Status |
|--------|---------|-------------|
| **Verified** | Task completed, requirements met | ✅ Verified |
| **Partial** | Some aspects work, others don't | ⬜ Pending (session linked) |
| **Blocked** | Bug or error prevents completion | 🛑 Blocked |
| **Failed** | Task couldn't be executed | ⬜ Pending (issues documented) |

## Parallel Verification

Run multiple non-conflicting verifications in parallel using background execution.

### How to Run

Use Bash with `run_in_background: true`:

```
[Bash: ranger go --scenario 1, run_in_background: true] → task_abc
[Bash: ranger go --scenario 2, run_in_background: true] → task_def
```

Poll with TaskOutput, report results as they complete.

### Safe to Parallelize

- Viewing pages, checking UI elements, navigation tests
- Read-only operations that don't modify shared state

### Do NOT Parallelize

- Logout tests (affects auth state for other sessions)
- Create/delete operations on shared data
- Tests with dependencies on each other

### CRITICAL: No Code Edits During Verification

File watchers (Next.js, Vite) will restart the dev server and break active browser sessions. Finish all code changes before running verifications.

## Examples

### Basic Verification

```bash
ranger go \
  --scenario 1 \
  --notes "Log in with test@example.com / password123, verify redirect to dashboard"
```

### Verify Specific Scenario

```bash
# Skip the selection prompt, verify scenario 2 directly
ranger go \
  --notes "Complete signup flow with new email" \
  --scenario 2
```

### Verify with Specific Profile

```bash
# Use staging profile instead of active profile
ranger go \
  --profile staging \
  --scenario 1 \
  --notes "Verify login works in staging"
```

### Start on a Specific Page

```bash
# Start verification at /settings instead of base URL
ranger go \
  --start-path /settings \
  --scenario 1 \
  --notes "Verify user can update their profile"

# Start at /admin/users
ranger go \
  --start-path /admin/users \
  --scenario 2 \
  --notes "Verify admin can see user list"
```

## After Verification

Check progress:

```bash
ranger show
```

If all non-closed scenarios are verified, the feature review auto-completes:

```
✅ User Authentication (feat_abc123)
   Status: completed
   ...
```

## Evidence Captured

Each verification creates:
- **Playwright trace** - Full browser session replay
- **Screenshots** - Captured during execution
- **Conversation log** - Agent's reasoning and actions
- **Session summary** - What was done and found

Access evidence via the report or dashboard.

If the user will need to review or continue in Ranger, share the dashboard link after running `ranger go`:

> Here is the link to the Feature Review in Ranger. Leave comments in the dashboard and then resume the feature review in your agent.
> https://dashboard.ranger.net/features/{feature_id}

## Troubleshooting

### "No active feature review"
Run `ranger list` to find feature reviews, then `ranger resume <id>` to resume one.

### "No active profile"
Run `ranger profile use <profile-name>` to set a profile with browser access.

### Verification times out
The agent has 59 minutes max. For very long flows, break into smaller scenarios.

### Wrong scenario marked
Reset the scenario via the dashboard, then re-verify.

# Starting a Feature Review Session

At the START of any coding session that touches the frontend or UI, check if there's an existing feature review to resume before creating a new one.

## List Feature Reviews

First, check what feature reviews exist:

```bash
ranger list
```

Or filter to the current git branch:

```bash
ranger list --current-branch
```

This shows feature review names, IDs, status, and branch info.

## Resume a Feature Review

If you find a pertinent feature review to resume:

```bash
ranger resume <id>
```

This command:
1. Sets the feature review as active
2. Starts the session if it's in `ready` status
3. Displays the feature review with its scenarios

End the conversational turn by sharing the dashboard link whenever you resume a feature review:

> Here is the link to the Feature Review in Ranger. Leave comments in the dashboard and then resume the feature review in your agent.
> https://dashboard.ranger.net/features/{feature_id}

## Check Current Status

After resuming, view the full status:

```bash
ranger show
```

This displays:
- Feature review name and ID
- Current status (in_progress, blocked, completed)
- Git context (repo, branch)
- Scenarios with status indicators

## Check for Reviewer Feedback

If any scenarios show comment badges (e.g., `[2 comments]`) or are at v2+, reviewer feedback needs to be addressed:

```bash
ranger get-review
```

This shows the actual comment content, who wrote it, and the previous version description. **Read [feedback.md](./feedback.md) for the full feedback workflow.**

## Add Scenarios

If you need to add new work to an existing feature review:

```bash
ranger add-scenario "User navigates to /settings, clicks 'Edit Profile', updates their display name, clicks Save, sees success toast, refreshes the page, and confirms the new name persists"
```

This adds a new pending scenario to the active feature review. Use this when:
- The scope of work has expanded
- You discover additional scenarios to verify
- A review requested additional coverage

### Writing Good Scenarios

Scenarios should be **detailed, multi-step E2E flows** that can be verified in a browser:

**Bad (too vague):**
```bash
ranger add-scenario "Profile editing works"
```

**Good (detailed flow):**
```bash
ranger add-scenario "User goes to /settings, clicks 'Edit Profile' button, changes display name to 'Test User', clicks Save, sees 'Profile updated' success message, refreshes the page, and verifies the name still shows 'Test User'"
```

**Note:** You cannot add scenarios while a review is in progress.

## Decision Tree

```
Start Session
     │
     ▼
ranger list
     │
     ├── Found pertinent feature review? ──▶ ranger resume <id>
     │                                         │
     │                                         ▼
     │                                ranger show
     │                                         │
     │                                         ▼
     │                                Scenarios have comments?
     │                                    │          │
     │                                    YES        NO
     │                                    │          │
     │                                    ▼          ▼
     │                           get-review   Continue working
     │                           fix + verify
     │
     └── None exist? ──▶ See create.md
```

## Example

```bash
# Start of session - list feature reviews
$ ranger list

Showing 3 of 3:

🔄 User Authentication
   ID: feat_abc123
   Dev Status: In Progress
   Branch: feature/auth

# Resume the feature review
$ ranger resume feat_abc123

✅ Resumed feature review: User Authentication (feat_abc123)

🔄 User Authentication (feat_abc123)
   Dev Status: In Progress
   Branch: feature/auth

   Scenarios:
   1. ✅ Login flow works
   2. ⬜ Signup creates account
   3. ⬜ Password reset sends email
```

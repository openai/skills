# validate

Verify that all session requirements are met before marking the session complete.

## Rules

1. **PASS requires ALL of**: 100% tasks complete, all deliverables exist, all files ASCII-encoded with LF endings, all tests passing, all success criteria met, no security or GDPR violations, no critical behavioral quality violations (when BQC applies)
2. **Any single failure = overall FAIL** - no partial passes
3. **Script first** - run `analyze-project.sh --json` before any analysis
4. Conventions compliance is a spot-check, not exhaustive - flag obvious violations only

### No Deferral Policy

- If a validation check fails and YOU can fix it (encoding issues, missing directories, failing tests with obvious fixes), FIX IT and re-validate
- The ONLY valid reason to report a FAIL back to the user is when the fix requires their input, credentials, or decisions only a human can make
- "The environment isn't set up" is NOT a valid FAIL -- setting it up IS the task
- If you report a FAIL for something you could have fixed, that is a **critical failure**

## Steps

### 1. Get Deterministic Project State (REQUIRED FIRST STEP)

Run the analysis script to get reliable state facts. Local scripts (`.spec_system/scripts/`) take precedence over plugin scripts if they exist:

```bash
# Check for local scripts first, fall back to plugin
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

This returns structured JSON including:
- `current_session` - The session to validate
- `current_session_dir_exists` - Whether specs directory exists
- `current_session_files` - Files already in the session directory
- `monorepo` - true/false/null from state.json
- `packages` - Array of registered packages (empty if not monorepo)
- `active_package` - Resolved package context (null if not applicable)

**IMPORTANT**: Use the `current_session` value from this output. If `current_session` is `null`, run plansession yourself to set one up. Only ask the user if plansession itself requires user input.

### 1a. Determine Package Context (Monorepo Only)

**Skip this step if** `monorepo` is not `true` in the JSON output.

Resolve the active package for this session:

1. **spec.md header**: Read the `Package:` field from the session's spec.md (set during plansession)
2. **active_package from script**: If spec.md has no Package field, use `active_package` from the JSON output

Store the resolved package path for use in Steps 3-5. A `null` package means this is a cross-cutting session.

### 2. Read Session Files

Using the `current_session` value from the script output, read all session documents:
- `.spec_system/specs/[current-session]/spec.md` - Requirements
- `.spec_system/specs/[current-session]/tasks.md` - Task checklist
- `.spec_system/specs/[current-session]/implementation-notes.md` - Progress log
- `.spec_system/specs/[current-session]/security-compliance.md` - Prior security report (if exists from previous validation run)
- `.spec_system/CONVENTIONS.md` - Project coding conventions (if exists)

**CONVENTIONS.md** is used in the Quality Gates check (section 3.E) to verify code follows project conventions for naming, structure, error handling, testing, etc.

### 3. Run Validation Checks

#### A. Task Completion
Verify all tasks in tasks.md are marked `[x]`:
- Count total tasks
- Count completed tasks
- List any incomplete tasks

#### B. Deliverables Check
From spec.md deliverables section:
- Verify each file exists
- Check file is non-empty
- Note any missing files
- **Monorepo**: File paths should be repo-root-relative (e.g., `apps/web/src/auth.ts`). Verify files are within the declared package scope (from Step 1a). Flag any deliverables outside the package boundary.

#### C. ASCII Encoding Check
For each deliverable file:
```bash
# Check encoding
file [filename]  # Should show: ASCII text

# Find non-ASCII characters
LC_ALL=C grep '[^[:print:][:space:]]' [filename]

# Check for CRLF line endings
grep -l $'\r' [filename]
```
- Report any non-ASCII characters found
- Report any CRLF line endings

#### D. Test Verification
Run the project's test suite:
- Record total tests
- Record passed/failed
- Calculate coverage if available
- Note any failures
- **Monorepo**: When a package is resolved (Step 1a), run tests scoped to that package first (e.g., `cd apps/web && npm test`, or using workspace commands like `pnpm --filter web test`). Also run repo-root tests if they exist, since cross-package regressions matter.

**CRITICAL -- NO "PRE-EXISTING" EXCUSE**: If ANY test fails, you MUST:
1. Investigate the root cause -- determine whether the session's changes caused or contributed to the failure
2. NEVER dismiss a failure as "pre-existing" or "environment issue" -- if tests passed before this session and fail now, THIS SESSION BROKE THEM
3. FIX the failure before continuing validation. If you changed a Docker image, a dependency, a config file, or any shared code, failures in existing tests are YOUR responsibility
4. Only after all tests pass (0 failures) may you mark Test Verification as PASS
5. If a failure is genuinely unrelated (e.g., flaky network test), you must PROVE it by showing the test also fails on the pre-session commit -- do not assume

#### E. Success Criteria
From spec.md success criteria:
- Check each functional requirement
- Verify testing requirements met
- Confirm quality gates passed

#### F. Conventions Compliance (if CONVENTIONS.md exists)
Spot-check deliverables against project conventions:
- **Naming**: Functions, variables, files follow naming conventions
- **Structure**: Files are organized according to file structure conventions
- **Error Handling**: Follows the project's error handling approach
- **Comments**: Explain "why" not "what", no commented-out code
- **Testing**: Tests follow project testing philosophy
- **Database** (if Database Layer conventions exist): Migration naming follows convention, model/table naming matches convention, required columns present on new tables, indexes on foreign keys

Note: This is a spot-check, not exhaustive. Flag obvious violations only.

#### G. Security & GDPR Compliance

Review **only files created or modified in this session** (use deliverables from spec.md and git diff against the pre-session commit). Skip files not touched by this session.

**Security (OWASP Top 10 spot-check):**
- **Injection**: SQL, command, LDAP injection vectors -- unsanitized user input in queries or shell calls
- **Broken Auth**: Hardcoded credentials, API keys, tokens, or secrets in source code
- **Sensitive Data Exposure**: Unencrypted PII in logs, error messages, or responses; secrets in plaintext config
- **Insecure Dependencies**: Known-vulnerable packages added in this session (`npm audit`, `pip audit`, `cargo audit` as applicable)
- **Misconfiguration**: Debug modes enabled, overly permissive CORS, missing security headers
- **Database Security** (if Database Layer conventions exist): Hardcoded connection strings (must use env vars), raw SQL with string concatenation (must use parameterized queries), missing down/rollback migrations, unencrypted sensitive columns (passwords, tokens, PII), unlimited connection pools, shared credentials between test and production

**GDPR Compliance:**
- **Data Collection**: Any new collection of personal data (names, emails, IPs, device IDs) must have a documented purpose and legal basis
- **Consent**: If collecting user data, verify consent mechanism exists before data is stored
- **Data Minimization**: Only the minimum necessary personal data is collected -- flag any over-collection
- **Right to Erasure**: If storing personal data, verify a deletion path exists or is documented as a future requirement
- **Data Logging**: Personal data must not appear in application logs -- check log statements for PII leakage
- **Third-Party Sharing**: If sending data to external services, verify the transfer is documented

**Scope rules:**
- This is a targeted review of session deliverables, not a full codebase audit
- Flag **clear violations** only -- do not speculate about edge cases
- If the session added no user-facing data handling, mark GDPR as N/A with a brief justification
- Hardcoded secrets and injection vulnerabilities are always FAIL regardless of scope
- **Monorepo**: Scope the review to files within the declared package boundary (from Step 1a). Cross-cutting sessions review all modified files.

#### H. Behavioral Quality Spot-Check

Determine whether a BQC applies: does this session produce application code?

**If no application code**: Mark as N/A and skip to Step 4.

**If application code**: Select up to 5 deliverable files most likely to contain behavioral issues (files with side effects, mutations, external calls, user interaction, or data fetching). Spot-check against these priorities:

| Priority | What to check | FAIL if... |
|----------|---------------|------------|
| 1 | Trust boundary enforcement | External input processed without validation, or access granted without authorization check |
| 2 | Resource cleanup | Scoped lifecycle acquires resources (timers, subscriptions, connections) without releasing on exit |
| 3 | Mutation safety | State-mutating actions triggerable multiple times while in-flight, or write path lacks idempotency protection |
| 4 | Failure path completeness | Operation can fail but has no explicit error/failure handling visible to caller |
| 5 | Contract alignment | Interface between components has shape mismatch, missing enum case, or schema drift |

**Scoring**:
- 0 violations: PASS
- 1-2 low-severity (e.g., missing retry backoff on non-critical read path): WARN -- log but do not block
- Any high-severity in top priorities: FAIL -- fix before passing

### 4. Generate Security & Compliance Report

Create `security-compliance.md` in the session directory (`.spec_system/specs/[current-session]/security-compliance.md`):

```markdown
# Security & Compliance Report

**Session ID**: `phaseNN-sessionNN-name`
[MONOREPO ONLY - include when monorepo: true]
**Package**: [package-path]
[END MONOREPO ONLY]
**Reviewed**: [YYYY-MM-DD]
**Result**: PASS / FAIL / N/A

---

## Scope

**Files reviewed** (session deliverables only):
- `path/file1` - [brief description]
- `path/file2` - [brief description]

**Review method**: Static analysis of session deliverables + dependency audit (if applicable)

---

## Security Assessment

### Overall: PASS / FAIL

| Category | Status | Severity | Details |
|----------|--------|----------|---------|
| Injection (SQLi, CMDi, LDAPi) | PASS/FAIL | -- / Critical / High | [details] |
| Hardcoded Secrets | PASS/FAIL | -- / Critical | [details] |
| Sensitive Data Exposure | PASS/FAIL | -- / High / Medium | [details] |
| Insecure Dependencies | PASS/FAIL | -- / High / Medium | [details] |
| Security Misconfiguration | PASS/FAIL | -- / Medium | [details] |

### Findings

#### [Finding Title] (if any)
- **Severity**: Critical / High / Medium / Low
- **File**: `path/file:line`
- **Description**: [what the issue is]
- **Remediation**: [how to fix it]
- **Status**: Open / Remediated

[Repeat for each finding, or "No security findings."]

---

## GDPR Compliance Assessment

### Overall: PASS / FAIL / N/A

*N/A if session introduced no personal data handling.*

| Category | Status | Details |
|----------|--------|---------|
| Data Collection & Purpose | PASS/FAIL/N/A | [details] |
| Consent Mechanism | PASS/FAIL/N/A | [details] |
| Data Minimization | PASS/FAIL/N/A | [details] |
| Right to Erasure | PASS/FAIL/N/A | [details] |
| PII in Logs | PASS/FAIL/N/A | [details] |
| Third-Party Data Transfers | PASS/FAIL/N/A | [details] |

### Personal Data Inventory (if applicable)

| Data Element | Source | Storage | Purpose | Retention | Deletion Path |
|-------------|--------|---------|---------|-----------|---------------|
| [e.g., email] | [user input] | [database table] | [authentication] | [until account deletion] | [DELETE /api/user] |

[Or "No personal data collected or processed in this session."]

### Findings

#### [Finding Title] (if any)
- **Category**: [GDPR category]
- **File**: `path/file:line`
- **Description**: [what the issue is]
- **Remediation**: [how to fix it]
- **Status**: Open / Remediated

[Repeat for each finding, or "No GDPR findings."]

---

## Recommendations

[Actionable items for future sessions, or "None -- session is compliant."]

---

## Sign-Off

- **Result**: PASS / FAIL / N/A
- **Reviewed by**: AI validation (validate)
- **Date**: [YYYY-MM-DD]
```

### 5. Generate Validation Report

Create `validation.md` in the session directory:

```markdown
# Validation Report

**Session ID**: `phaseNN-sessionNN-name`
[MONOREPO ONLY - include when monorepo: true]
**Package**: [package-path]
[END MONOREPO ONLY]
**Validated**: [YYYY-MM-DD]
**Result**: PASS / FAIL

---

## Validation Summary

| Check | Status | Notes |
|-------|--------|-------|
| Tasks Complete | PASS/FAIL | X/Y tasks |
| Files Exist | PASS/FAIL | X/Y files |
| ASCII Encoding | PASS/FAIL | [issues] |
| Tests Passing | PASS/FAIL | X/Y tests |
| Quality Gates | PASS/FAIL | [issues] |
| Conventions | PASS/SKIP | [issues or "No CONVENTIONS.md"] |
| Security & GDPR | PASS/FAIL/N/A | [issues] |
| Behavioral Quality | PASS/WARN/FAIL/N/A | [issues or "N/A -- no application code"] |

**Overall**: PASS / FAIL

---

## 1. Task Completion

### Status: PASS/FAIL

| Category | Required | Completed | Status |
|----------|----------|-----------|--------|
| Setup | N | N | PASS |
| Foundation | N | N | PASS |
| Implementation | N | N | PASS |
| Testing | N | N | PASS |

### Incomplete Tasks
[List any incomplete tasks or "None"]

---

## 2. Deliverables Verification

### Status: PASS/FAIL

#### Files Created
| File | Found | Status |
|------|-------|--------|
| `path/file1` | Yes | PASS |
| `path/file2` | Yes | PASS |

### Missing Deliverables
[List any missing or "None"]

---

## 3. ASCII Encoding Check

### Status: PASS/FAIL

| File | Encoding | Line Endings | Status |
|------|----------|--------------|--------|
| `path/file1` | ASCII | LF | PASS |

### Encoding Issues
[List issues or "None"]

---

## 4. Test Results

### Status: PASS/FAIL

| Metric | Value |
|--------|-------|
| Total Tests | N |
| Passed | N |
| Failed | 0 |
| Coverage | X% |

### Failed Tests
[List failures or "None"]

---

## 5. Success Criteria

From spec.md:

### Functional Requirements
- [x] [Requirement 1]
- [x] [Requirement 2]

### Testing Requirements
- [x] Unit tests written and passing
- [x] Manual testing completed

### Quality Gates
- [x] All files ASCII-encoded
- [x] Unix LF line endings
- [x] Code follows project conventions

---

## 6. Conventions Compliance

### Status: PASS/SKIP

*Skipped if no `.spec_system/CONVENTIONS.md` exists.*

| Category | Status | Notes |
|----------|--------|-------|
| Naming | PASS/FAIL | [issues] |
| File Structure | PASS/FAIL | [issues] |
| Error Handling | PASS/FAIL | [issues] |
| Comments | PASS/FAIL | [issues] |
| Testing | PASS/FAIL | [issues] |

### Convention Violations
[List violations or "None" or "Skipped - no CONVENTIONS.md"]

---

## 7. Security & GDPR Compliance

### Status: PASS/FAIL/N/A

**Full report**: See `security-compliance.md` in this session directory.

#### Summary
| Area | Status | Findings |
|------|--------|----------|
| Security | PASS/FAIL | [count] issues |
| GDPR | PASS/FAIL/N/A | [count] issues |

### Critical Violations (if any)
[List critical/high severity items or "None"]

---

## 8. Behavioral Quality Spot-Check

### Status: PASS/WARN/FAIL/N/A

*N/A if session produced no application code.*

**Checklist applied**: [Yes / N/A]
**Files spot-checked**: [list of up to 5 files]

| Category | Status | File | Details |
|----------|--------|------|---------|
| Trust boundaries | PASS/FAIL | `path` | [details or "--"] |
| Resource cleanup | PASS/FAIL | `path` | [details or "--"] |
| Mutation safety | PASS/FAIL | `path` | [details or "--"] |
| Failure paths | PASS/FAIL | `path` | [details or "--"] |
| Contract alignment | PASS/FAIL | `path` | [details or "--"] |

### Violations Found
[List with file:line, category, severity, or "None"]

### Fixes Applied During Validation
[List fixes, or "None"]

## Validation Result

### PASS / FAIL

[Summary of validation outcome]

### Required Actions (if FAIL)
[List what needs to be fixed]

## Next Steps

[If PASS]: Run updateprd to mark session complete.
[If FAIL]: Address required actions and run validate again.
```

### 6. Update State

Update `.spec_system/state.json` based on validation result:

**If PASS:**
```json
{
  "current_session": "phaseNN-sessionNN-name",
  "next_session_history": [
    {
      "date": "YYYY-MM-DD",
      "session": "phaseNN-sessionNN-name",
      "status": "validated"
    }
  ]
}
```

**If FAIL:**
```json
{
  "next_session_history": [
    {
      "date": "YYYY-MM-DD",
      "session": "phaseNN-sessionNN-name",
      "status": "validation_failed"
    }
  ]
}
```

- Update `next_session_history` entry status to `validated` or `validation_failed`
- **Monorepo only**: Include the `package` field in the history entry when a package was resolved in Step 1a (matching the pattern from plansession Step 6). Omit the `package` field for single-repo projects or cross-cutting sessions.

## Output

Report PASS/FAIL with a summary of each check. If PASS, prompt updateprd. If FAIL, list issues with suggested fixes and prompt re-run of validate.

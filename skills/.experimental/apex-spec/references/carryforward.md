# carryforward

Extract key insights from the just-completed phase and update two living documents:
- `.spec_system/CONSIDERATIONS.md` - institutional memory for AI assistants working on future phases
- `.spec_system/SECURITY-COMPLIANCE.md` - cumulative security posture and GDPR compliance record

Be ruthlessly selective: only the most impactful lessons deserve space.

Run after completing a phase, before phasebuild. Optional but recommended for phases with significant discoveries, novel problems, or 4+ sessions.

## Rules

1. **CONSIDERATIONS.md: 600-line limit STRICT** - trim older/less relevant items if needed
2. **SECURITY-COMPLIANCE.md: 1000-line limit STRICT** - synthesize, don't append raw session reports
3. **Active Concerns**: max 20 items total (5 per subcategory)
4. **Lessons Learned**: max 30 items total
5. **Resolved**: max 15 items, rotate out after 2 phases
6. **Conciseness**: each item 1-3 lines max, include phase number `[PNN]`
7. **ASCII-only characters** and Unix LF line endings

## Steps

### 1. Verify Phase Completion

Check `.spec_system/state.json`:
- Confirm current phase status is "complete"
- Get phase number and name
- If phase not complete, inform user and exit
- Read `monorepo` field: `true` / `false` / `null`
- If `monorepo: true`: read `packages` array and `completed_sessions` (object format with `package` field)

### 2. Gather Phase Artifacts

Read all implementation summaries from the completed phase:

```bash
# Find all IMPLEMENTATION_SUMMARY.md files for completed phase
ls .spec_system/archive/phases/phase_NN_*/IMPLEMENTATION_SUMMARY.md
```

Also read:
- `.spec_system/audit/` - recent audit reports
- `.spec_system/PRD/phase_NN/` - phase requirements (before archive)
- Any `implementation-notes.md` files with blockers or discoveries
- All `security-compliance.md` files from the completed phase's sessions
- Current `.spec_system/SECURITY-COMPLIANCE.md` (if exists from prior phases)

**Monorepo only**: For each session's artifacts, note the `Package:` field from its spec.md header. This associates insights with the package they originated from. Cross-cutting sessions (package: null) produce project-wide insights.

### 3. Extract Insights

From each session's IMPLEMENTATION_SUMMARY.md, identify:

**Active Concerns** (things that affect upcoming work):
- Unresolved technical debt
- Known limitations or constraints
- External dependencies with risks
- Performance thresholds to monitor
- Security considerations
- Database concerns (schema debt, missing indexes, query performance, migration ordering)
- Deployment concerns (local dev startup issues, deploy failures, rollback gaps, environment drift)

**Lessons Learned** (patterns to follow or avoid):
- Technical decisions that worked well (and why)
- Approaches that failed (and why)
- Useful patterns discovered
- Tool/library insights
- Architecture insights

**Items to Resolve** (move from Active Concerns if addressed):
- Check if previous Active Concerns were addressed this phase
- Move them to Resolved with brief resolution note

**Monorepo only**: Tag each extracted insight with its source package:
- **Package-specific**: Concerns/lessons that apply to one package (e.g., `[P05-apps/web]` for a frontend-specific issue)
- **Cross-package**: Concerns that span multiple packages or affect package interactions (e.g., `[P05-apps/web+apps/api]` for an API contract issue)
- **Project-wide**: Concerns that apply regardless of package (e.g., `[P05]` for a CI/CD or tooling lesson)

### 4. Read Current CONSIDERATIONS.md

Read `.spec_system/CONSIDERATIONS.md`:
- Parse existing sections
- Note current line count
- Identify stale items in each section

### 5. Update CONSIDERATIONS.md

Update `.spec_system/CONSIDERATIONS.md` following the format below. Add new items, remove resolved ones, merge similar entries, and enforce the limits in Rules above.

**Monorepo only**: When tagging items, use the package-qualified format: `[PNN-package/path]` for package-specific items, `[PNN]` for project-wide items. This helps future sessions identify which concerns apply to their target package. Do NOT create separate per-package sections -- keep the existing flat structure but use the tags to indicate scope. This avoids section bloat within the 600-line limit.

### 6. Synthesize SECURITY-COMPLIANCE.md

Read every `security-compliance.md` from the just-completed phase's sessions. Merge them into `.spec_system/SECURITY-COMPLIANCE.md` following the format below.

**Synthesis rules:**
- **Don't append** -- re-synthesize the entire document each time by merging new phase findings with the existing file
- **Remediated findings**: Move to the Resolved Findings section with resolution date and phase. Compress after 2 phases (keep one-line summary only)
- **Open findings**: Keep full detail (severity, file, description, remediation steps)
- **Personal Data Inventory**: Accumulate across phases -- add new data elements, update existing ones if storage/purpose changed, remove if data collection was removed
- **Dependency audit**: Keep only the current state -- drop resolved dependency issues, add new ones
- **Phase summary**: Add a row to the Phase History table, keep last 5 phases of detail

**Monorepo only**: When synthesizing findings:
- Include the package path in finding IDs (e.g., `[P05-apps/web-S03]` for a finding from session 03 scoped to apps/web)
- In the Personal Data Inventory, add a Package column to indicate which package collects/stores each data element
- In the Phase History table, note per-package session counts if sessions were distributed across packages
- Group related findings by package when it aids readability, but keep within the flat document structure

### 7. Report Summary

Tell the user what was updated.

## CONSIDERATIONS.md Format

```markdown
# Considerations

> Institutional memory for AI assistants. Updated between phases via carryforward.
> **Line budget**: 600 max | **Last updated**: Phase NN (YYYY-MM-DD)

---

## Active Concerns

Items requiring attention in upcoming phases. Review before each session.

### Technical Debt
<!-- Max 5 items -->

- [P05] **Item name**: Brief description of the concern and why it matters.

### External Dependencies
<!-- Max 5 items -->

- [P08] **Item name**: Brief description of risk or constraint.

### Performance / Security
<!-- Max 5 items -->

- [P11] **Item name**: Threshold or requirement to monitor.

### Architecture
<!-- Max 5 items -->

- [P03] **Item name**: Constraint or consideration for design decisions.

---

## Lessons Learned

Proven patterns and anti-patterns. Reference during implementation.

### What Worked
<!-- Max 15 items -->

- [P02] **Pattern name**: What it is and when to use it.

### What to Avoid
<!-- Max 10 items -->

- [P04] **Anti-pattern name**: What went wrong and why to avoid.

### Tool/Library Notes
<!-- Max 5 items -->

- [P07] **Tool name**: Key insight about usage or configuration.

---

## Resolved

Recently closed items (buffer - rotates out after 2 phases).

| Phase | Item | Resolution |
|-------|------|------------|
| P10 | Item name | How it was resolved |
| P09 | Item name | How it was resolved |

---

*Auto-generated by carryforward. Manual edits allowed but may be overwritten.*
```

## SECURITY-COMPLIANCE.md Format

```markdown
# Security & Compliance

> Cumulative security posture and GDPR compliance record. Updated between phases via carryforward.
> **Line budget**: 1000 max | **Last updated**: Phase NN (YYYY-MM-DD)

---

## Current Security Posture

### Overall: CLEAN / AT RISK / CRITICAL

| Metric | Value |
|--------|-------|
| Open Findings | N |
| Critical/High | N |
| Medium/Low | N |
| Phases Audited | N |
| Last Clean Phase | PNN |

---

## Open Findings

Active security or GDPR issues requiring attention. Ordered by severity.

### Critical / High

- **[PNN-S01] Finding title**
  - Severity: Critical / High
  - File: `path/file:line`
  - Description: Brief description of the issue.
  - Remediation: Steps to fix.
  - Status: Open | In Progress
  - Opened: PNN (YYYY-MM-DD)

### Medium / Low

- **[PNN-S02] Finding title**
  - Severity: Medium / Low
  - File: `path/file:line`
  - Description: Brief description.
  - Remediation: Steps to fix.
  - Opened: PNN (YYYY-MM-DD)

[Or "No open findings."]

---

## GDPR Compliance Status

### Overall: COMPLIANT / NON-COMPLIANT / N/A

### Personal Data Inventory

| Data Element | Source | Storage | Purpose | Legal Basis | Retention | Deletion Path | Since |
|-------------|--------|---------|---------|-------------|-----------|---------------|-------|
| [e.g., email] | [user input] | [db.users] | [auth] | [consent] | [account lifetime] | [DELETE /api/user] | PNN |

[Or "No personal data collected or processed."]

### Compliance Checklist

| Requirement | Status | Notes |
|------------|--------|-------|
| Data collection has documented purpose | PASS/FAIL/N/A | [notes] |
| Consent obtained before data storage | PASS/FAIL/N/A | [notes] |
| Data minimization verified | PASS/FAIL/N/A | [notes] |
| Deletion/erasure path exists | PASS/FAIL/N/A | [notes] |
| No PII in application logs | PASS/FAIL/N/A | [notes] |
| Third-party transfers documented | PASS/FAIL/N/A | [notes] |

---

## Dependency Security

### Current Vulnerabilities

| Package | Version | Severity | CVE | Status |
|---------|---------|----------|-----|--------|
| [package] | [ver] | High | [CVE-YYYY-NNNNN] | Open / Mitigated |

[Or "No known vulnerable dependencies."]

---

## Resolved Findings

Recently closed items. Compressed after 2 phases.

| ID | Finding | Severity | Resolved | Phase | Resolution |
|----|---------|----------|----------|-------|------------|
| PNN-S01 | Finding title | High | YYYY-MM-DD | PNN | How it was fixed |

[Or "No resolved findings yet."]

---

## Phase History

| Phase | Sessions | Security | GDPR | Findings Opened | Findings Closed |
|-------|----------|----------|------|-----------------|-----------------|
| PNN | N | PASS/FAIL | PASS/FAIL/N/A | N | N |

---

## Recommendations

Actionable items for upcoming phases based on cumulative findings.

1. [Recommendation with context]

[Or "None -- project is currently compliant."]

---

*Auto-generated by carryforward. Manual edits allowed but may be overwritten.*
```

## SECURITY-COMPLIANCE.md Line Budget Guidance

Target allocation within 1000 lines:
- Header/metadata: ~20 lines
- Open Findings: ~300 lines (detailed entries with remediation steps)
- GDPR Compliance: ~200 lines (inventory + checklist)
- Dependency Security: ~100 lines
- Resolved Findings: ~150 lines (compressed table)
- Phase History: ~80 lines
- Recommendations/spacing: ~150 lines

### Trimming Strategy

When approaching 1000 lines, trim in this order:
1. Resolved findings older than 2 phases (compress to one-line table row)
2. Phase History detail older than 5 phases (keep only the summary row)
3. Dependency issues that have been resolved
4. Merge similar open findings
5. Shorten verbose remediation descriptions

---

## CONSIDERATIONS.md Line Budget Guidance

Target allocation within 600 lines (CONSIDERATIONS.md):
- Header/metadata: ~15 lines
- Active Concerns: ~150 lines (20 items x ~7 lines avg)
- Lessons Learned: ~250 lines (30 items x ~8 lines avg)
- Resolved: ~100 lines (15 items in table)
- Section headers/spacing: ~85 lines

### Trimming Strategy

When approaching 600 lines, trim in this order:
1. Resolved items older than 2 phases
2. Lessons Learned items older than 5 phases (unless still highly relevant)
3. Active Concerns that have become irrelevant
4. Merge similar items within sections
5. Shorten verbose descriptions

## Output

**Single-repo:**
```
Phase NN Carryforward Complete

Updated .spec_system/CONSIDERATIONS.md:
- Active Concerns: +N new, -N resolved, N total
- Lessons Learned: +N new, N total
- Resolved: +N added, -N rotated out, N total
- Line count: NNN/600

Updated .spec_system/SECURITY-COMPLIANCE.md:
- Open Findings: N (N critical/high, N medium/low)
- GDPR Status: COMPLIANT / NON-COMPLIANT / N/A
- Findings opened this phase: N
- Findings closed this phase: N
- Personal data elements tracked: N
- Line count: NNN/1000

Key additions:
- [Active] Brief description
- [Lesson] Brief description
- [Security] Brief description (if any new findings)

Ready for the documents workflow step to maintain project documentation.
```

**Monorepo** (add package breakdown after Key additions):
```
Package breakdown:
- apps/web: N sessions, N concerns, N findings
- apps/api: N sessions, N concerns, N findings
- (cross-cutting): N sessions, N concerns, N findings
```

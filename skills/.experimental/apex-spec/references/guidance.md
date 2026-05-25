# Apex Spec System Usage Guidance

Practical guidance for getting the most out of the Apex Spec System.

---

## When to Use Apex Spec

### Ideal Projects (Strong Fit)

| Scenario | Why It Works |
|----------|--------------|
| **Greenfield development** | New projects benefit most from structured phases |
| **From Quality Boilerplates** | This is the best! |
| **Medium-to-large scope** | Projects spanning 3+ sessions (6+ hours total) |
| **Solo developer + AI** | The primary design target |
| **Well-defined requirements** | Clear enough to write a PRD, although createprd can do lifting |
| **Learning new tech** | Structure helps when exploring unfamiliar territory |
| **Monorepo projects** | Per-package session scoping keeps work focused |

**Real example**: The NJ Title Intelligence Platform (see [walkthrough.md](walkthrough.md)) used Apex Spec to build a 4M+ parcel system across 16 phases and 79+ sessions in ~3 weeks.

### Acceptable Projects (Moderate Fit)

- **Feature additions** - Adding major features to existing codebases
- **Refactoring projects** - Large-scale restructuring with clear goals
- **Proof of concepts** - When you want documentation of decisions

### Poor Fit (Consider Alternatives)

| Scenario | Why It Doesn't Fit |
|----------|-------------------|
| **Quick bug fixes** | Overhead exceeds value for <1 hour tasks |
| **Exploratory prototyping** | Constant pivoting conflicts with session structure |
| **Team projects with existing workflows** | May conflict with established processes |
| **Urgent/time-critical work** | Structure adds latency |

### Quick Self-Assessment

**Use Apex Spec if you answer YES to 2+ of these:**

- [ ] Have you started AI-assisted projects that lost coherence after a few sessions?
- [ ] Do you find yourself re-explaining context to Claude repeatedly?
- [ ] Do your projects lack documentation because "you'll do it later"?
- [ ] Have you shipped code without proper testing/linting setup?
- [ ] Do you want a repeatable process for AI-assisted development?

**Skip Apex Spec if:**

- The task will take less than 2 hours total
- You're not sure what you're building yet
- You need to ship something in the next hour
- Your team has a working process already

---

## Workflow

The project is initiated, then iterates through phases. Each phase consists of sessions. Between phases, the system is hardened.

### Start a Project

Ran once at the beginning of the project.

```
initspec -> createprd -> createuxprd (optional) -> phasebuild
```

**Artifacts created:**
- PRD.md (master requirements document)
- state.json
- Folder structure and templates
- 1st Phase and Sessions

### Session

Ran repeatedly until all the sessions of the Phase are completed.

```
plansession -> implement -> validate -> updateprd
```

**Artifacts created:**
- spec.md (detailed specification)
- tasks.md (12-25 task checklist)
- implementation-notes.md (progress log)
- security-compliance.md (security & GDPR review)
- validation.md (quality verification)
- IMPLEMENTATION_SUMMARY.md (completion record)

### Between Phases

Ran once after all sessions of a Phase are completed, between each Phase.

```
audit -> pipeline -> infra -> carryforward -> documents -> phasebuild
```

**Artifacts created:**
- CONSIDERATIONS.md
- CONVENTIONS.md
- SECURITY-COMPLIANCE.md
- Documentation, potentially .github workflows, etc
- Next Phase and Sessions

---

## Team Usage Patterns

Apex Spec is designed for **solo developer + AI** workflows. However, teams can adapt the system with these patterns.

### Pattern 1: Shared PRD, Individual Sessions

```
Team                          Individual
-----                         ----------
Collaborate on PRD     ->     Developer claims session
Define phases          ->     Runs session workflow solo
Review phase structure ->     Commits via standard git
                       ->     carryforward captures lessons
```

**Coordination**: Add `Assigned: @username` to session stub files in PRD.

**Merge strategy**: Standard git workflow - each developer works on their branch, PRs for review.

### Pattern 2: Pair Programming with AI

```
Developer A (Driver)          Developer B (Navigator)
--------------------          -------------------------
Runs Claude commands          Reviews output
Executes implementation       Catches issues early
Marks tasks complete          Suggests improvements
```

**Benefits**:
- Knowledge transfer
- Real-time review
- Reduced errors
- Shared context

### Pattern 3: Review Checkpoints

```
Developer                     Team
---------                     ----
Complete session       ->
validate              ->     Review validation.md
                       <-     Feedback
Incorporate feedback   ->
updateprd             ->     Merge approved
```

**Adds human review gate** before marking sessions complete.

### What Apex Spec Does NOT Handle

| Need | Solution |
|------|----------|
| Real-time collaboration | Use other tools (VS Code Live Share, etc.) |
| Session conflict resolution | Coordinate via PRD assignment |
| Team velocity tracking | Use external tools |
| Cross-session dependencies between developers | Plan in PRD, communicate |

### Team Best Practice

Treat Apex Spec as a **personal workflow tool** that produces **shareable artifacts**:
- specs, tasks, validation reports are reviewable
- implementation-notes.md provides context
- CONSIDERATIONS.md captures institutional memory
- SECURITY-COMPLIANCE.md tracks cumulative security posture and GDPR compliance
- Git commits provide natural integration points

---

## Monorepo Usage

### When Monorepo Support Helps

| Scenario | Why |
|----------|-----|
| Multiple packages with different stacks | Per-package tool validation and session scoping |
| Large codebase with clear boundaries | Sessions stay focused on one package at a time |
| Shared libraries consumed by multiple apps | Cross-cutting sessions handle shared code |
| Different deploy targets per package | `infra` and `pipeline` adapt per deployable unit |

### Session Scoping Best Practices

**Prefer single-package sessions.** Most sessions should target one package. This keeps scope tight and makes validation straightforward.

**Use cross-cutting sessions sparingly.** Reserve `package: null` sessions for work that genuinely spans packages:
- Initial project scaffolding and workspace config
- Shared type definitions consumed by multiple packages
- CI/CD pipeline setup
- Integration tests between services

**Order sessions by dependency.** If `apps/web` needs types from `packages/shared`, plan the shared session first (lower session number within the phase).

**Scope task paths to the package.** Task file paths should use full repo-root-relative paths:
```
- [ ] T001 [S0102] Create auth module (`apps/web/src/auth/index.ts`)
```
Not:
```
- [ ] T001 [S0102] Create auth module (`src/auth/index.ts`)
```

### Package Context Flow

You do not need to remember to specify the package every time. The system resolves it automatically:

1. **From session stubs**: `phasebuild` annotates stubs with `Package: apps/web`
2. **From spec.md**: Once planned, the spec header carries the package context
3. **From user input**: Say "plan for apps/web" during `plansession`
4. **As fallback**: Claude prompts you to select from the packages list

### Monorepo + Team Patterns

Combine monorepo support with team patterns for larger projects:

```
Developer A                    Developer B
-------------                  -------------
Claims session for apps/web    Claims session for apps/api
Runs session workflow solo     Runs session workflow solo
Both share same state.json     Both share same .spec_system/
```

**Coordination tip**: Assign sessions by package ownership. Add `Assigned: @username` and `Package: apps/web` to session stub files. This prevents conflicts.

---

## Future Enhancements

The following features are under consideration but require implementation work:

### Metrics Tracking (Not Yet Implemented)

**Concept**: Track session duration, task counts, and estimation accuracy over time.

```
metrics

Session Velocity:
- Average session duration: 2.3 hours
- Estimation accuracy: 92%
- Total sessions completed: 5
```

**Status**: Would require state.json schema changes and new metrics command.

### Project Templates (Not Yet Implemented)

**Concept**: Pre-configured PRD structures for common project types.

```
initspec --template cli
initspec --template web-app
initspec --template api-server
```

**Status**: Would require template files and initspec command changes.

### Export Capabilities (Not Yet Implemented)

**Concept**: Generate shareable status reports.

```
export --format markdown
export --format html
```

**Status**: Would require new export command.

---

## Quick Reference

### Command Cheat Sheet

| Goal | Command |
|------|---------|
| Start new project | `initspec` |
| Generate PRD from requirements | `createprd "description"` or `createprd @file.md` |
| Generate UX PRD from design docs | `createuxprd "description"` or `createuxprd @file.md` |
| Create phase structure | `phasebuild` |
| Analyze, spec, and generate tasks | `plansession` |
| Implement tasks | `implement` |
| Verify completion | `validate` |
| Mark session complete | `updateprd` |
| Add dev tooling | `audit` |
| Add CI/CD | `pipeline` |
| Add infrastructure | `infra` |
| Update documentation | `documents` |
| Capture lessons & security posture | `carryforward` |

### Session Limits

| Limit | Value |
|-------|-------|
| Maximum tasks | 25 |
| Maximum duration | 4 hours |
| Ideal task count | 12-25 (sweet spot: 20) |
| Ideal duration | 2-3 hours |
| Objectives | Single clear objective |

### Recovery

Every `updateprd` commits and pushes. Git is your safety net:
- Undo completed session: `git revert <commit>`
- Mid-session issues: Resume `implement` or delete session directory

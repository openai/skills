# createprd

Convert a user-provided document (notes, PRD, spec, RFC, meeting notes) into the Apex Spec System master PRD at `.spec_system/PRD/PRD.md`.

Downstream workflow steps (phasebuild, plansession, documents) depend on this PRD as the source of truth.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--skip-conventions` | false | Skip CONVENTIONS.md fine-tuning |

## Rules

1. **Never overwrite a real PRD** without explicit user confirmation (template placeholders can be overwritten silently)
2. **Do not invent requirements** - ask 3-8 targeted questions for missing info
3. **ASCII-only characters** and Unix LF line endings in all output
4. **Do not create phase directories or session stubs** - that is the phasebuild workflow step's job
5. **CONVENTIONS.md must stay under 300 lines** - trim ruthlessly if exceeded
6. Only add conventions with clear evidence from the tech stack - no speculative additions

## Steps

### 1. Confirm Spec System Is Initialized

Check for `.spec_system/state.json` and `.spec_system/PRD/`. If missing, run initspec yourself to set up the spec system. Only ask the user if initspec requires user input you don't have.

### 2. Get Deterministic Project State

Run the analysis script to get reliable state facts. Local scripts take precedence over plugin scripts:

```bash
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

Use the JSON output as ground truth for:
- Project name (if available)
- Current phase number
- Existing phases list (if present)

Do not parse `state.json` directly.

### 3. Collect the Source Requirements Document

Ask the user for the source document in one of these forms:
- Paste the text directly into the chat
- Provide a file path in the repo to read
- Provide multiple snippets (if the content is long)

If the user provides a file path, read it. If pasted text, treat it as the source of truth.

### 4. Decide Whether to Create or Update

Check whether `.spec_system/PRD/PRD.md` already exists.

- If it does not exist: create it
- If it exists: check if it is a template placeholder or real content

**Detecting Template Placeholder PRD**:

The initspec workflow step creates a placeholder PRD with bracket markers like `[Goal 1]`, `[PROJECT_DESCRIPTION]`, `[Objective 1]`, etc. If **2 or more** such markers are present, it's a template - overwrite without confirmation.

If the PRD has real content (fewer than 2 template markers), ask for explicit user confirmation before overwriting.

**If overwriting real content (confirmation given)**:
1. Create a timestamped backup in `.spec_system/archive/PRD/` before writing
2. Then replace `.spec_system/PRD/PRD.md`

Backup naming (ASCII only):
- `.spec_system/archive/PRD/PRD-backup-YYYYMMDD-HHMMSS.md`

If overwrite is not confirmed:
- Offer to create a new file next to it for review and stop

### 5. Extract and Normalize Requirements

From the source document, extract and normalize:
- **Product overview**: 1-3 paragraphs
- **Goals**: 3-7 bullets that are outcome-focused
- **Non-goals**: 3-10 bullets (explicitly out of scope)
- **Users and use cases**: primary personas and key workflows
- **Functional requirements**: grouped by area (MVP first). Write each requirement as "[Actor] can [capability] [context]" (e.g., "User can reset password via email link"). Focus on WHAT, not HOW -- keep requirements implementation-agnostic.
- **Non-functional requirements**: performance, security, privacy, reliability, accessibility. Each NFR must include a specific, measurable target (e.g., "API response < 200ms at p95", not "should be fast")
- **Constraints**: tech constraints, compliance, hosting, budgets, deadlines
- **Assumptions**: what must be true for the plan to work
- **Risks**: major risks and mitigations
- **Success criteria**: checkboxes that can be validated
- **Open questions**: items requiring human confirmation

Important:
- Do not invent details. If the source doc is missing critical info, ask 3-8 targeted questions
- Keep content high-level and stable. Session-level details belong in the plansession workflow step
- Keep phases as planning scaffolding, not implementation plans

### 6. Generate Master PRD

Create `.spec_system/PRD/PRD.md` using this template. Use straight quotes only. Use hyphens, not em-dashes. ASCII-only.

```markdown
# [PROJECT_NAME] - Product Requirements Document

## Overview

[1-3 paragraphs describing what this product is and who it is for.]

## Goals

1. [Goal]
2. [Goal]
3. [Goal]

## Non-Goals

- [Non-goal]
- [Non-goal]

## Users and Use Cases

### Primary Users

- **[Persona]**: [short description]

### Key Use Cases

1. [Use case]
2. [Use case]

## Requirements

### MVP Requirements

- [Actor] can [capability] [context]
- [Actor] can [capability] [context]

### Deferred Requirements

- [Actor] can [capability] [context]

## Non-Functional Requirements

- **Performance**: [specific measurable target, e.g., "API response < 200ms at p95"]
- **Security**: [specific measurable target, e.g., "OWASP Top 10 compliance"]
- **Reliability**: [specific measurable target, e.g., "99.9% uptime SLA"]
- **Accessibility**: [specific measurable target, e.g., "WCAG 2.1 AA"]

## Constraints and Dependencies

- [Constraint or dependency]

## Phases

This system delivers the product via phases. Each phase is implemented via multiple 2-4 hour sessions (12-25 tasks each).

| Phase | Name | Sessions | Status |
|-------|------|----------|--------|
| 00 | [PHASE_NAME] | TBD | Not Started |

## Phase 00: [PHASE_NAME]

### Objectives

1. [Objective]
2. [Objective]

### Sessions (To Be Defined)

Sessions are defined via phasebuild as `session_NN_name.md` stubs under `.spec_system/PRD/phase_00/`.

**Note**: This command does NOT create phase directories or session stubs. Run phasebuild after creating the PRD.

## Technical Stack

- [Technology] - [why]

## Success Criteria

- [ ] [Criterion]
- [ ] [Criterion]

## Risks

- **[Risk]**: [mitigation]

## Assumptions

- [Assumption]

## Open Questions

1. [Question]
2. [Question]
```

Notes:
- If the project already has phases beyond Phase 00 (from state analysis), update the phases table accordingly
- Do not create phase directories here - that is the phasebuild workflow step's job
- Use `[PHASE_NAME]` placeholder - default to "Foundation" if not specified

### 6a. Monorepo Detection from PRD Content

**Skip this step if** `monorepo` in state.json is already `true` or `false` (already determined by initspec or a previous run).

When `monorepo` is `null` (unknown), scan for multi-package signals:

1. **Check PRD content** for signals:
   - Multiple services or applications mentioned (e.g., "web app", "API server", "worker service")
   - Explicit monorepo language ("monorepo", "workspace", "packages")
   - Multiple distinct tech stacks for different components
   - References to shared libraries or cross-service code

2. **Check `monorepo_detection`** from the `analyze-project.sh --json` output (Step 2):
   - If `monorepo_detection.detected` is `true`, use it as supporting evidence

3. **If signals found**: Present the user with a proposed package map:
   ```
   Monorepo signals detected in PRD:
   - [signal 1]
   - [signal 2]

   Proposed package map:
   | Package | Path | Stack |
   |---------|------|-------|
   | web | apps/web | TypeScript |
   | api | apps/api | TypeScript |

   Confirm / Edit / Reject?
   ```

   - **Confirmed**: Set `monorepo: true` in state.json, add `packages` array, add Package Map section to PRD after Technical Stack:
     ```markdown
     ## Package Map

     | Package | Path | Stack | Purpose |
     |---------|------|-------|---------|
     | web | apps/web | TypeScript | Frontend application |
     | api | apps/api | TypeScript | Backend API server |
     ```
   - **Rejected**: Set `monorepo: false` in state.json

4. **If no signals found**: Set `monorepo: false` in state.json

### 7. Customize CONVENTIONS.md for Tech Stack

Customize `.spec_system/CONVENTIONS.md` to reflect the project's actual tech stack and domain. This is **initial customization** (more freedom to reshape) vs the audit workflow step which makes surgical edits later.

#### 7.1 Detect Tech Stack

From the PRD's Technical Stack section and source requirements, identify: primary language(s), framework(s), runtime, package manager, testing framework, and project domain.

#### 7.2 Transform Generic Template

Read `.spec_system/CONVENTIONS.md` (the generic template from initspec). Replace generic conventions with stack-specific equivalents, add new ones required by the stack, remove ones that don't apply. Keep each convention to 1-2 lines. No speculative additions.

**Stack-specific transformations (examples):**

| Stack | Transformations |
|-------|-----------------|
| TypeScript | Replace generic naming with TS conventions; add type safety rules; add `interface` vs `type` guidance |
| React | Add component patterns; hooks conventions; state management approach; JSX style |
| Next.js | Add App Router conventions; server/client component rules; API route patterns; file-based routing |
| Python | Replace with PEP 8; add type hint requirements; docstring format; import ordering |
| Go | Replace with Effective Go idioms; add error handling patterns; package naming; interface conventions |
| Rust | Add Clippy compliance; Result/Option patterns; ownership conventions; module organization |
| CLI | Add exit code standards; stdout vs stderr rules; flag naming; help text conventions |
| API | Add REST conventions; status code usage; error response format; versioning approach |
| Library | Add semantic versioning rules; public API stability; backwards compatibility; documentation requirements |
| Monorepo | Add Workspace Structure section (package table + cross-package rules); shared dependency rules; cross-package imports; workspace alias conventions |
| Database | Add Database Layer section: connection source, migration tool + rules, model/table naming, query safety, seed script, test DB strategy, vector/embeddings conventions (if applicable) |

**Section-specific transformations:**

| Section | Generic -> Stack-Specific |
|---------|--------------------------|
| **Naming** | Universal advice -> Language-specific casing (camelCase, snake_case, PascalCase, kebab-case) |
| **Files & Structure** | Generic -> Framework directory conventions (src/, app/, lib/, components/, routes/) |
| **Functions & Modules** | Universal -> Language idioms (async/await, error returns, generators, decorators) |
| **Error Handling** | Generic -> Stack patterns (try/catch, Result types, error boundaries, panic vs error) |
| **Testing** | Universal -> Framework patterns (describe/it, pytest fixtures, table-driven tests, mocking approach) |
| **Dependencies** | Generic -> Package manager commands, lockfile rules, version pinning strategy |

**Add new sections if warranted:**
- **TypeScript**: Add "Types" section for type conventions
- **React**: Add "Components" section for component patterns
- **API**: Add "Endpoints" section for API design conventions
- **Database**: Add "Database Layer" section with subsections for connection, migrations, models, queries, seeding, testing. If PRD references vector search, embeddings, or RAG, include "Vector / Embeddings" subsection. Detection: PRD mentions database, schema, any DB technology, migrations, ORM, data modeling, vector/embeddings, or RAG.
- **Monorepo** (if confirmed in Step 6a): Add "Workspace Structure" section with package table and cross-package rules (import aliases, shared types location, test boundaries, cross-package session scope)

#### 7.3 Enforce 300-Line Limit (STRICT)

After transformation, verify CONVENTIONS.md stays under **300 lines maximum**.

```bash
wc -l .spec_system/CONVENTIONS.md
```

If over 300 lines:
1. **Merge** similar conventions into single entries
2. **Prioritize** stack-specific over generic (remove generic if redundant)
3. **Condense** verbose explanations to single lines
4. **Remove** lowest-impact conventions until compliant

**Budget guidance**: The generic template is ~85 lines. You have ~215 lines for stack-specific customization. A well-customized CONVENTIONS.md typically lands between 120-200 lines.

#### 7.4 Validate Changes

After edits:
1. Verify file is valid markdown
2. Confirm line count <= 300
3. Ensure no duplicate sections created
4. Confirm ASCII-only characters

```bash
wc -l .spec_system/CONVENTIONS.md
LC_ALL=C grep -n '[^[:print:][:space:]]' .spec_system/CONVENTIONS.md && echo "Non-ASCII found"
```

#### 7.5 Skip Conditions

Skip this step entirely if:
- `.spec_system/CONVENTIONS.md` does not exist
- No tech stack was identified from the requirements
- User explicitly requests `--skip-conventions`

### 8. Validate Output

Before reporting completion, run both encoding and content quality checks.

#### 8.1 Encoding Validation

- Confirm the file exists at `.spec_system/PRD/PRD.md`
- Confirm it is ASCII-only and uses LF line endings

```bash
file .spec_system/PRD/PRD.md
grep -n "$(printf '\r')" .spec_system/PRD/PRD.md && echo "CRLF found"
LC_ALL=C grep -n '[^[:print:][:space:]]' .spec_system/PRD/PRD.md && echo "Non-ASCII found"
```

If checks fail, fix the PRD content and re-check.

#### 8.2 Content Quality Validation

Scan the generated PRD for common quality issues. For each check, fix inline if possible or flag to the user:

| Check | What to look for | Action |
|-------|-----------------|--------|
| Template placeholders | Bracket markers like `[Goal 1]`, `[Requirement]`, `[Actor]` remaining in output | Replace with real content or remove |
| Vague NFRs | NFRs without specific numbers (e.g., "should be fast", "highly available") | Rewrite with measurable targets |
| Empty sections | Sections with no content below the heading | Fill in or ask user for input |
| Weak requirements | Requirements that describe HOW (implementation) rather than WHAT (capability) | Rewrite in actor/capability form |
| Missing sections | Any required section from the template entirely absent | Add the section |

Report any issues found and fixed in the output summary.

## Output

Report to user:

```
createprd complete!

Created:
- .spec_system/PRD/PRD.md (master PRD)
[If backup was made:]
- Backup: .spec_system/archive/PRD/PRD-backup-YYYYMMDD-HHMMSS.md

Summary:
- Goals: N defined
- MVP Requirements: N items
- Non-Goals: N items
- Open Questions: N items

[If conventions were customized:]
Conventions:
- .spec_system/CONVENTIONS.md customized for [stack] (N/300 lines)
- Key additions: [brief list, max 3]

[If monorepo determined:]
Monorepo: [true - N packages detected | false - single-repo confirmed]
[If monorepo true:]
- Package Map added to PRD
- Workspace Structure added to CONVENTIONS.md

[If quality issues were found and fixed:]
Quality:
- N issues auto-fixed (template placeholders, vague NFRs, etc.)

[If quality issues remain for user:]
Quality:
- N issues need user input: [brief list]

Next Steps:
1. Review the generated PRD and refine as needed
2. Run phasebuild to define Phase 00 sessions
```

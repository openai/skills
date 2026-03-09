# up2imp

Audit a raw list of upstream changes against your hardened fork and rewrite it as a
curated, optimally ordered implementation list containing only changes that objectively
improve your codebase. Designed for teams maintaining modified forks that periodically
cherry-pick upstream improvements.

## Usage

```
up2imp <changes-file> [upstream-dir]
```

- `<changes-file>` -- Path to the markdown file containing raw upstream updates
  since the last comparison (e.g., `upstream-changes.md`)
- `[upstream-dir]` -- Path to the full upstream codebase copy for reference
  (defaults to `.001_ORIGINAL/`)

## Rules

1. **Senior engineer mindset** -- Approach this like a craftsperson who obsesses over
   pristine code with zero errors, warnings, or issues. Be methodical, patient, and
   uncompromising on quality.
2. **Objective improvements only** -- Every retained item must demonstrably make the
   codebase more correct, faster, safer, more stable, or more maintainable.
3. **Respect the fork's direction** -- This is a hardened, stripped-down,
   security-focused fork that has diverged intentionally. Never include changes that
   conflict with those decisions.
4. **Preserve implementation detail** -- Each retained item must have enough context
   (affected files, upstream references, rationale) for an engineer to implement it
   efficiently.
5. **Optimal order** -- Sort the final list in the order items should be implemented,
   accounting for dependencies, risk, and logical grouping.
6. **Read-only on spec system** -- Never modify state.json, session specs, or task
   checklists.
7. **ASCII only** -- Output file uses characters 0-127 only.

## Steps

### 1. Load context

Read the changes file provided by the user. This contains the raw list of upstream
updates since the last comparison.

Read the upstream codebase directory (default `.001_ORIGINAL/`) to understand the
full context of each change when needed.

Read the current project codebase to understand the fork's architecture, security
modifications, and which components exist or have been replaced.

### 2. Categorize each upstream change

For every item in the changes file, classify it into one of these categories:

**INCLUDE -- objectively improves the fork:**
- Bug fixes -- correctness issues, edge cases, error handling
- Performance improvements -- measurable efficiency gains
- Security patches -- vulnerability fixes, hardening measures
- Stability improvements -- crash fixes, race conditions, resource leaks
- Meaningful refactors -- code that is demonstrably cleaner, more maintainable,
  or reduces technical debt

**EXCLUDE -- does not belong in the fork:**
- Feature additions the fork has intentionally stripped out
- Changes to components/modules the fork does not use or has replaced
- Cosmetic/stylistic changes (formatting, comment rewording, variable renames
  with no clarity gain)
- Changes that conflict with the fork's security modifications or architectural
  decisions
- Dependency bumps with no functional impact on the fork

### 3. Determine implementation order

Sort the included items by optimal implementation sequence:
- Dependencies first (if change B relies on change A, A comes first)
- Security patches and bug fixes before refactors
- Lower-risk changes before higher-risk ones
- Logically related changes grouped together

### 4. Rewrite the changes file

Overwrite the original changes file with the curated list. The output contains
ONLY the actionable improvements -- no excluded items, no commentary about what
was removed.

For each retained item, ensure it includes:
- Clear description of what the change does and why it matters
- Which files in the fork are affected
- References to upstream (commit hashes, file paths, PR numbers if available)
- Any implementation notes or caveats specific to the fork

## Output

The changes file is rewritten in place as the filtered, optimally ordered
implementation list. Report:
- Total items reviewed
- Items retained (with breakdown by category: bug fix, performance, security,
  stability, refactor)
- Items excluded (with brief summary of why, grouped by exclusion reason)
- The final ordered list is ready for sequential implementation

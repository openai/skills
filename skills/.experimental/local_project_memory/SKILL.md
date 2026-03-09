---
name: local_project_memory
description: Persistent memory for any project or codebase. Read before planning, implementing, debugging, or refactoring to retrieve prior decisions, constraints, interface specs, workflows, and known issues. Write after completing work to store new knowledge for future sessions.
---

# Local Project

Use the skill's `scripts/memory_cli.py` to read and write durable project memory for the current project.

## CLI Path (Important)

The memory database is project-local, but the CLI script is skill-local.

- Run commands from the **target project root** (so memory files are created/read for that project).
- Invoke the CLI using the **installed skill directory** (the directory containing this `SKILL.md`), not `./scripts/` in the target repo.

Set helper variables first:

```bash
export SKILL_DIR="/absolute/path/to/local_project_memory"  # directory containing this SKILL.md
export MEMORY_CLI="$SKILL_DIR/scripts/memory_cli.py"
```

Path-agnostic rule:

```bash
# Resolve SKILL_DIR to the installed local_project_memory skill directory (where this SKILL.md lives)
export SKILL_DIR="..."
export MEMORY_CLI="$SKILL_DIR/scripts/memory_cli.py"
```

## When to Use This Skill

**ALWAYS use this skill at the START and END of work sessions:**

### At Session Start (Before Planning/Implementing)

Use this skill to perform functional analysis and understand prior context:

- **Before developing/updating/refactoring**: Search memory to understand what's already been done, what decisions were made, and what constraints exist
- **Before new features**: Check if there's any history, related decisions, or relevant context about similar functionality
- **Understanding work scope**: When there's no clear history or when starting new work in the current session, search to see what's known
- **Planning phase**: Always search before planning to avoid redoing work or violating past decisions

### At Session End (After Work Completion)

Update memory when work is done or when the user specifies:

- **After completing features**: Store architectural decisions, interface specs, and workflow patterns used
- **After solving issues**: Document known issues, workarounds, and constraints discovered
- **When user requests**: "remember this", "save this decision", or similar prompts
- **Before major refactors**: Document current state and rationale for changes

## Workflow

1. **Initialize once**: Run `python3 "$MEMORY_CLI" init` from the target project root.
2. **Search before planning**: Always call search with minimal fields:
   - `python3 "$MEMORY_CLI" search "<query>" --view compact`
   - or `python3 "$MEMORY_CLI" search "<query>" --select id,type,title,summary`
3. **Inspect the neighborhood when useful**:
   - `python3 "$MEMORY_CLI" search "<query>" --neighbors-k 5`
   - `python3 "$MEMORY_CLI" related <mu_id>`
   - `python3 "$MEMORY_CLI" dedupe`
4. **Get details when needed**: Use selective get for partial content:
   - `python3 "$MEMORY_CLI" get <mu_id> --select id,type,content.decision,validity.status`
5. **Write after completion**: Store durable insights with `upsert`.
6. **Deprecate when evolving**: If meaning changes, create new MU and deprecate old:
   - `python3 "$MEMORY_CLI" deprecate <old_id> --replaced-by <new_id>`
7. **Refresh links after bulk edits when needed**:
   - `python3 "$MEMORY_CLI" relink <mu_id>`
   - `python3 "$MEMORY_CLI" relink --all`
8. **Maintain periodically**: Clean up deprecated entries:
   - `python3 "$MEMORY_CLI" stats`
   - `python3 "$MEMORY_CLI" vacuum --dry-run`
   - `python3 "$MEMORY_CLI" vacuum`

## Global Memory Namespace Guidance (for global/shared memory mode)

When global/shared memory is available, use a `namespace` to keep knowledge organized and safe to reuse across projects.

Use namespaces for two broad categories:

- **Project-shared knowledge**: information that multiple repositories may need (for example, UI reading backend API conventions, contracts, deployment assumptions).
- **User-global knowledge**: personal but durable working preferences that help the agent work better across all projects.

Recommended namespace patterns:

- `project:<repo-or-domain>` for cross-project technical knowledge
- `user:habits` for user working preferences and habits
- `user:workflow` for preferred steps/checklists
- `user:git` for commit style, commit type conventions, branch naming preferences
- `team:<org-or-squad>` for shared team standards (if applicable)

Examples of good user-global memory content (namespaced):

- preferred commit types (e.g., `feat`, `fix`, `chore`, release commit style)
- commit message formatting preferences (Conventional Commits, subject length, imperative mood)
- preferred debugging workflow order
- preferred verification sequence (tests, lint, typecheck)
- communication preferences (brief updates vs detailed updates)

Do not mix user-global preferences into a project namespace unless they are explicitly project-specific.

## Agent Rules

1. **Search first**: Before planning, always call `search` with `--view compact` or explicit `--select`.
2. **Use skill-local CLI path**: Resolve `SKILL_DIR` to the installed skill directory, set `MEMORY_CLI="$SKILL_DIR/scripts/memory_cli.py"`, and call `python3 "$MEMORY_CLI" ...` from the target project root.
3. **Use graph-aware retrieval**:
   - Use `search` first for direct recall
   - Use inline `neighborhood` or `related` to inspect nearby memories before creating a new one
   - Use `dedupe` or `merge-suggest` when you suspect overlap
4. **Selective retrieval**: Use `get --select` when partial content is sufficient.
5. **Store only durable information**:
   - architectural decisions
   - constraints and limitations
   - interface specifications
   - workflow patterns
   - known issues and workarounds
   - persistent task context
6. **Store atomic memories**:
   - one memory unit should capture one idea only
   - do not combine multiple decisions, multiple issues, or long mixed notes into one MU
   - if two facts may evolve independently, store them as separate MUs
   - prefer linking many small MUs over writing one large MU
7. **Optimize for minimum text, maximum information**:
   - use a short precise `title`
   - keep `summary` to one dense sentence
   - keep `content` shallow and factual
   - prefer key facts, constraints, rationale, and identifiers over prose
   - avoid filler words, repeated context, and narration
   - use `tags` and `retrieval_hints` to improve recall instead of expanding the summary
8. **Write with stable retrieval language**:
   - include the canonical nouns users will search for
   - include old/new names if terminology changed
   - include subsystem, API, feature, or workflow names explicitly
9. **Use namespace intentionally in global/shared memory** (when supported):
   - Use project namespaces for reusable technical knowledge that may help other repositories
   - Use user namespaces for cross-project preferences/habits (including commit type conventions and preferred workflows)
   - Keep user-global preferences separate from project-specific facts
   - Prefer stable namespace names over ad hoc labels
10. **Never store**:
   - secrets or credentials
   - API keys or tokens
   - raw logs or debug output
   - full transcripts
   - private reasoning or thought processes
   - temporary session state
11. **Evolution over replacement**:
   - When meaning changes, create new MU
   - Deprecate old MU with `--replaced-by`
   - Never delete without deprecating first
12. **Optimize token usage**: Prefer minimal field projection to reduce token consumption.

## Memory Writing Logic

Use this decision rule before storing a memory:

1. Is this durable beyond the current session?
   - If no, do not store it.
2. Can it be expressed as one atomic fact, rule, decision, spec, issue, or workflow?
   - If no, split it.
3. Will a future agent search for this directly?
   - If yes, include those search terms in `title`, `summary`, `tags`, or `retrieval_hints`.
4. Can any sentence be removed without losing meaning?
   - If yes, remove it.

Good MU shape:

- `title`: what it is
- `summary`: why it matters
- `content`: only the fields needed to act on it later

Bad MU shape:

- long narrative summaries
- mixed “decision + issue + workaround + future ideas” blobs
- copied logs, transcripts, or ticket text
- generic summaries with no searchable terms

Compression guidance:

- Prefer `"constraint": "...", "impact": "...", "workaround": "..."` over paragraphs
- Prefer `"endpoint": "/x", "methods": ["GET"]` over prose API descriptions
- Prefer one concise alternative list over long tradeoff essays
- Prefer 3 focused tags over 12 vague tags

## Practical Examples

### Before Starting Work

```bash
export SKILL_DIR="/absolute/path/to/local_project_memory"  # directory containing this SKILL.md
export MEMORY_CLI="$SKILL_DIR/scripts/memory_cli.py"

# Check if authentication has been implemented before
python3 "$MEMORY_CLI" search "authentication" --view compact

# Find API design decisions
python3 "$MEMORY_CLI" search "API" --type ARCH_DECISION --select id,title,summary

# Look for known issues with database migrations
python3 "$MEMORY_CLI" search "migration" --type KNOWN_ISSUE --k 5

# Get details of a specific decision
python3 "$MEMORY_CLI" get auth-strategy-v2 --select content.decision,content.rationale,validity
```

### After Completing Work

```bash
# Save architectural decision (from file)
echo '{
  "id": "auth-jwt-tokens",
  "type": "ARCH_DECISION",
  "title": "Use JWT for API authentication",
  "summary": "Chose JWT over sessions for stateless auth in microservices",
  "content": {
    "decision": "Implement JWT-based authentication",
    "rationale": "Enables stateless auth, better for horizontal scaling",
    "alternatives": ["session-based", "OAuth2"],
    "trade_offs": "Requires token refresh mechanism"
  },
  "tags": ["auth", "api", "security"],
  "retrieval_hints": ["authentication", "login", "tokens"]
}' | python3 "$MEMORY_CLI" upsert -

# Document a constraint discovered during work
echo '{
  "id": "constraint-postgres-version",
  "type": "CONSTRAINTS",
  "title": "PostgreSQL version must be >= 14",
  "summary": "JSONB performance optimizations require PostgreSQL 14+",
  "content": {
    "constraint": "Minimum PostgreSQL version is 14",
    "reason": "Uses JSONB indexing features introduced in v14",
    "impact": "Cannot deploy to older database versions"
  },
  "tags": ["database", "postgres", "deployment"]
}' | python3 "$MEMORY_CLI" upsert -

# Record interface specification
echo '{
  "id": "api-users-endpoint-v1",
  "type": "INTERFACE_SPEC",
  "title": "Users API endpoint specification",
  "summary": "REST API for user CRUD operations",
  "content": {
    "endpoint": "/api/v1/users",
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "auth_required": true,
    "response_format": "JSON",
    "schema_url": "docs/api/users-schema.json"
  },
  "tags": ["api", "users", "rest"]
}' | python3 "$MEMORY_CLI" upsert -

# Inspect related memories before adding another auth decision
python3 "$MEMORY_CLI" search "authentication" --neighbors-k 5
python3 "$MEMORY_CLI" related auth-jwt-tokens
```

### Evolving Decisions

```bash
# When changing approach, deprecate old decision
python3 "$MEMORY_CLI" deprecate auth-basic-v1 --replaced-by auth-jwt-tokens

# Search including deprecated to understand evolution
python3 "$MEMORY_CLI" search "authentication" --include-deprecated
```

### Maintenance

```bash
# Check memory stats
python3 "$MEMORY_CLI" stats

# Review likely duplicates
python3 "$MEMORY_CLI" dedupe

# Refresh links after editing many memories
python3 "$MEMORY_CLI" relink --all

# Preview what would be cleaned
python3 "$MEMORY_CLI" vacuum --dry-run

# Clean up deprecated entries
python3 "$MEMORY_CLI" vacuum
```

### Workflow-Specific Queries

```bash
# Find all security-related decisions before security review
python3 "$MEMORY_CLI" search "security OR auth OR encrypt" --type ARCH_DECISION

# Get all active constraints for a subsystem
python3 "$MEMORY_CLI" search "database" --type CONSTRAINTS --view compact

# Find workflows related to deployment
python3 "$MEMORY_CLI" search "deploy" --type WORKFLOW --select id,title,content.steps
```

### Global Namespace Examples (when global/shared memory mode is enabled)

```bash
# Cross-project technical knowledge (backend info reusable by UI project)
echo '{
  "id": "api-error-shape-v1",
  "type": "INTERFACE_SPEC",
  "title": "Shared API error response shape",
  "summary": "Backend error JSON format consumed by UI and integrations",
  "content": {
    "format": {"error": {"code": "string", "message": "string", "details": "object|null"}}
  },
  "tags": ["api", "backend", "ui", "errors"]
}' | python3 "$MEMORY_CLI" upsert -
# (Use global scope + namespace when supported, e.g. namespace: project:backend)

# User-global git preferences (commit types and commit style)
echo '{
  "id": "git-commit-style-preferences-v1",
  "type": "WORKFLOW",
  "title": "User commit message preferences",
  "summary": "Preferred commit types and formatting for commits across projects",
  "content": {
    "commit_types": ["feat", "fix", "chore", "docs", "refactor", "test"],
    "style": "Conventional Commits",
    "subject_rules": ["imperative mood", "short summary", "no trailing period"]
  },
  "tags": ["git", "commits", "workflow", "preferences"]
}' | python3 "$MEMORY_CLI" upsert -
# (Use global scope + namespace when supported, e.g. namespace: user:git)
```

## Memory Unit Contract

Returned MUs include:

- `schema: "nh.memory.mu"`
- `schema_version: 1`

Required fields:

- `id` (slug format, no spaces, e.g., "auth-jwt-strategy-v2")
- `type` (one of: ARCH_DECISION, CONSTRAINTS, GLOSSARY, INTERFACE_SPEC, KNOWN_ISSUE, TASK_CONTEXT, WORKFLOW)
- `title` (concise description)
- `summary` (one-line overview)
- `content` (JSON object with type-specific fields)

Optional:

- `tags` (list of strings for categorization)
- `retrieval_hints` (list of strings for better search recall)
- `provenance` (source/author information)
- `validity` (status: "active" or "deprecated", replaced_by)
- `updated_at` (ISO 8601 timestamp)

## Commands Reference

```bash
# Initialize project memory
python3 "$MEMORY_CLI" init

# Search memory units
python3 "$MEMORY_CLI" search "<query>" \
  [--k 8] \
  [--type TYPE] \
  [--tag substring] \
  [--include-deprecated] \
  [--view tiny|compact|full] \
  [--select path1,path2,...] \
  [--include-neighborhood|--no-include-neighborhood] \
  [--neighbors-k 3]

# Get specific memory unit
python3 "$MEMORY_CLI" get <mu_id> \
  [--view tiny|compact|full] \
  [--select path1,path2,...]

# Create or update memory unit
python3 "$MEMORY_CLI" upsert <file_or_dash>

# Deprecate memory unit
python3 "$MEMORY_CLI" deprecate <mu_id> --replaced-by <new_id>

# Inspect related memories
python3 "$MEMORY_CLI" related <mu_id> [--k 8] [--link-type TYPE] [--include-deprecated]

# List duplicate candidates
python3 "$MEMORY_CLI" dedupe [--k 8] [--include-deprecated]

# Recompute similarity links
python3 "$MEMORY_CLI" relink <mu_id>
python3 "$MEMORY_CLI" relink --all

# Suggest canonical memory among duplicates
python3 "$MEMORY_CLI" merge-suggest <mu_id> [--include-deprecated]

# Clean deprecated entries
python3 "$MEMORY_CLI" vacuum [--dry-run]

# Show statistics
python3 "$MEMORY_CLI" stats
```

All successful command outputs are JSON on stdout.

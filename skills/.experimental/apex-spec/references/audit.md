# audit

Add and validate local dev tooling one bundle at a time.

## Rules

1. **One bundle per run** - add one, validate all, fix all
2. **Never break syntax** - revert after 2 failed fix attempts
3. **Respect known-issues.md** - don't fix intentional exceptions
4. **Update CONVENTIONS.md** - record what was added in Local Dev Tools table
5. **Continue on failure** - one tool failing doesn't stop the audit
6. **Monorepo aware** - run per package, report per package

### No Deferral Policy

- NEVER mark a task as "pending", "requires X", or "blocked" if the blocker is something YOU can resolve
- If a dependency needs installing, INSTALL IT
- If a directory needs creating, CREATE IT
- If a config file needs generating, GENERATE IT
- "The environment isn't set up" is NOT a blocker -- setting it up IS the task
- The ONLY valid blocker is something that requires USER input or credentials you don't have
- If you skip a task that was executable, that is a **critical failure**

## Master List (7 Bundles)

Industry standard order (fast to slow, format before validate):

| Priority | Bundle | Contents |
|----------|--------|----------|
| 1 | **Formatting** | Formatter (Prettier, Biome, Black, Ruff format) |
| 2 | **Linting** | Linter (ESLint, Biome, Ruff, Clippy) |
| 3 | **Type Safety** | Type checker (TypeScript, mypy, Pyright) |
| 4 | **Testing** | Test runner + coverage (Jest, Vitest, pytest, pytest-cov) |
| 5 | **Observability** | Structured logger + error capture (structlog, pino, tracing, slog) |
| 6 | **Git Hooks** | Pre-commit hooks (husky, pre-commit, lefthook) |
| 7 | **Database** | Migration framework + seed script + test DB config |

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--dry-run` | false | Preview what would happen without changes |
| `--skip-install` | false | Don't install missing tools |
| `--verbose` | false | Show full tool output |

## Flow

### Step 1: DETECT

1. Check for `.spec_system/CONVENTIONS.md`
   - If missing: Run initspec yourself to create it. Only ask the user if initspec requires user input you don't have.
   - Read Stack section for languages/runtimes
   - Read Local Dev Tools table for configured tools
   - Read Workspace Structure table (if present) for per-package tool status

2. Read `.spec_system/state.json` for monorepo context:
   - `monorepo` field: `true` / `false` / `null`
   - `packages` array (when `monorepo: true`): each entry has `name`, `path`, `type`, `stack`

3. Check for `.spec_system/audit/known-issues.md`
   - If found, load ignore patterns
   - Note: "Known issues loaded (N paths, N rules, N tests)"

4. Check git status
   - If dirty: Warn "Uncommitted changes exist. Fixes will mix with existing changes."

5. If `--dry-run`: Skip to Dry Run Output

### Step 1a: Enumerate Packages (Monorepo Only)

**Skip this step if** `monorepo` is not `true` in state.json.

When `monorepo: true`, build a per-package tool matrix:

1. Read the `packages` array from state.json
2. For each package, note its `stack` field (determines which tools apply)
3. Group packages by stack (packages sharing a stack share tool configs)
4. Determine installation strategy per tool:
   - **Shared at root**: When all packages use the same stack, or the tool is stack-agnostic (e.g., git hooks)
   - **Per-package**: When packages have different stacks (e.g., Python API + TypeScript frontend)

Example package matrix:
```
Packages detected (monorepo: true):
| Package | Path | Stack | Formatter | Linter | Types |
|---------|------|-------|-----------|--------|-------|
| web | apps/web | TypeScript | Biome | Biome | tsc |
| api | apps/api | Python | Ruff | Ruff | mypy |
| shared | packages/shared | TypeScript | Biome | Biome | tsc |
```

### Step 2: COMPARE

Compare Local Dev Tools table against 6-bundle master list:
- For each bundle, check if Tool column has a value or shows "not configured" / "-"
- Build list of missing bundles in priority order

If all bundles configured: "All recommended local dev tools configured. Jumping to Step 5."

### Step 3: SELECT

Pick the highest-priority missing bundle from Step 2.

Output: "Selected: [Bundle Name] - not yet configured"

### Step 4: IMPLEMENT

Install and configure the single selected bundle missing.

**Detection by language** (from CONVENTIONS.md Stack section):

| Language | Formatter | Linter | Type Checker | Test Framework | Logger | Git Hooks |
|----------|-----------|--------|--------------|----------------|--------|-----------|
| Python | Ruff | Ruff | mypy | pytest + pytest-cov | structlog | pre-commit |
| TypeScript | Biome | Biome | tsc (strict) | Vitest | pino | husky + lint-staged |
| JavaScript | Biome | Biome | - | Vitest | pino | husky + lint-staged |
| Rust | rustfmt | Clippy | (built-in) | cargo test | tracing | pre-commit |
| Go | gofmt | golangci-lint | (built-in) | go test | log/slog | pre-commit |

**Monorepo installation strategy** (when `monorepo: true`):
- **Same stack across all packages**: Install and configure at repo root. One config file shared.
- **Mixed stacks**: Install per-package. Each package gets its own config file in its directory.
- **Git hooks**: Always install at repo root (hooks are repo-wide). Configure to run tools per-package via workspace commands (e.g., `pnpm -r run lint`, `turbo run lint`).
- **Observability bundle**: Create `logs/` at repo root (shared). Logger configs go per-package in each package's source directory (e.g., `apps/api/src/logging_config.py`, `apps/web/src/logger.ts`).

**Single-repo**: Install and configure at project root as usual.

1. Install tool via detected package manager
2. Generate config file with sensible defaults
3. **Monorepo**: When installing per-package, use workspace commands where available (e.g., `pnpm --filter web add -D biome`, `cargo add -p api tracing`)
4. If install fails and not `--skip-install`: Try alternative install methods (different package manager, build from source, etc.). Only document for manual install if you have exhausted all automated options and the failure requires sudo or credentials you don't have.

#### Observability Bundle Implementation ("Logger")

**Purpose**: Set up structured logging with AI-friendly error capture.

**For all languages, create:**
1. `logs/` directory in project root
2. Proper `logs/.gitignore` with content
3. Logger configuration file (language-specific)
4. Error handler that writes to `logs/last_error_<timestamp>.json`, ex: `logs/last_error_2025-01-01T12:00:00.000Z.json`

**last_error.json schema** (AI-friendly structured error context):
```json
{
  "timestamp": "2025-01-01T12:00:00.000Z",
  "level": "error",
  "msg": "Error description",
  "error": {
    "type": "ErrorClassName",
    "message": "Detailed error message",
    "stack": "Stack trace..."
  },
  "context": {}
}
```

**Language-specific setup examples:**

| Language | Install | Config File | Error Handler |
|----------|---------|-------------|---------------|
| Python | `pip install structlog` | `src/logging_config.py` | `write_last_error()` processor |
| TypeScript | `npm install pino` | `src/logger.ts` | `logMethod` hook |
| JavaScript | `npm install pino` | `src/logger.js` | `logMethod` hook |
| Rust | Add `tracing`, `tracing-subscriber` to Cargo.toml | `src/logging.rs` | `capture_error()` function |
| Go | (stdlib) | `internal/logging/logging.go` | `CaptureError()` function |

#### Database Bundle Implementation

**Activation**: Only when database signals detected (docker-compose DB service, `.env` with `DATABASE_URL`/`DB_*`, migration tool config files, ORM in dependencies, vector DB in dependencies).

**Steps:**
1. Detect DB type and existing migration tool from project signals
2. If no migration tool found, recommend one based on detected stack (prompt user to confirm)
3. Verify migration tool is installed and configured
4. Create seed script if none exists (location based on stack conventions)
5. Create test DB configuration if none exists (`.env.test` or equivalent with separate `DATABASE_URL`)
6. Validate: run migrations (up + down + up to verify reversibility), run seed, run test suite

**Monorepo**: Prompt user for DB ownership model (shared / per-package / hybrid). Install migration tool in owner package or per-package as appropriate. Update CONVENTIONS.md Database Ownership table.

**Detection signals:**

| Signal | Source |
|--------|--------|
| `docker-compose.yml` with DB service | Project root |
| `.env` with `DATABASE_URL` or `DB_*` vars | Project/package root |
| `prisma/schema.prisma`, `drizzle.config.*`, `alembic.ini`, `knexfile.*` | Package root |
| ORM in dependency manifest | Package root |
| `pgvector`, `chromadb`, `pinecone-client` in deps | Package root |

### Step 5: VALIDATE

Run ALL configured tools (not just the new one):

1. **Formatter** (if configured): Run with auto-fix flag
2. **Linter** (if configured): Run with auto-fix flag
3. **Type checker** (if configured): Run in check mode
4. **Tests** (if configured): Run full suite
5. **Observability** (if configured): Verify logger and error capture
6. **Git hooks** (if configured): Verify hooks are installed
7. **Database** (if configured): Run migrations (up, down, up), run seed script, verify test DB connects
8. **Local dev startup** (if applicable): Verify the app starts locally (`docker compose up -d` or framework dev command), confirm it responds (e.g., `curl http://localhost:[port]`), then shut down. If no start command is known, skip.

**Observability validation:**
- Run logger initialization (language-specific)
- Trigger test error to verify capture
- Confirm `logs/` directory exists
- Confirm `logs/.gitignore` has correct patterns
- Confirm `logs/last_error_<timestamp>.json` is created with valid JSON

**Database validation:**
- Run migration tool's status/pending command to verify no drift
- Run up migration, then down, then up again (verify reversibility)
- Run seed script (verify idempotency -- run twice)
- Verify test DB configuration connects successfully
- If vector DB configured: verify extension/service is available

**Local dev startup validation:**
- If `docker-compose.yml` / `compose.yml` exists: run `docker compose config --quiet` (validate config), then `docker compose up -d`, wait for healthy, `curl` the dev URL, then `docker compose down`
- If no compose file: use the framework's dev command (e.g., `npm run dev`, `python manage.py runserver`) in background, verify it binds to the expected port, then stop it
- Record the working start command in CONVENTIONS.md Local Dev Tools table as `| Dev Server | [command] | [config] |`
- **Monorepo**: Verify each deployable package starts independently

**Monorepo validation** (when `monorepo: true`):
- Run each configured tool **per package** using workspace commands or by changing into the package directory
- Examples: `pnpm --filter web run lint`, `cd apps/api && ruff check .`, `turbo run typecheck`
- Also run repo-root checks for root-level configs (e.g., root `tsconfig.json` references)
- Collect results per package for the Step 8 report
- A tool failing in one package does not skip other packages -- run all, then report all

**Single-repo**: Run each tool from the project root as usual.

Capture all output. Parse for errors, warnings, fixes applied.

### Step 6: FIX

For each issue found in Step 5:

1. **Auto-fixable** (format, some lint): Already fixed in Step 5
2. **Type errors**: Attempt fix, verify syntax still valid
3. **Test failures**: Attempt fix, re-run affected test
4. **Unfixable after 3 attempts**: Try a different approach. Only log for manual review if the fix requires sudo or credentials you don't have. Revert if syntax broken.

**Guardrail**: After any fix, verify syntax/compilation. If broken after 2 retries, revert.

Filter out issues matching known-issues.md patterns - report separately as "Known".

### Step 7: RECORD

If a new bundle was added, update `.spec_system/CONVENTIONS.md`:

Update the Local Dev Tools table:
```markdown
| Category | Tool | Config |
|----------|------|--------|
| Formatter | Ruff | ruff.toml |  <-- was "not configured"
```

**Monorepo only**: Also update the Workspace Structure table with per-package tool status where stacks differ:
```markdown
## Workspace Structure

| Package | Path | Type | Stack | Formatter | Linter |
|---------|------|------|-------|-----------|--------|
| web | apps/web | Frontend | TypeScript | Biome | Biome |
| api | apps/api | Backend | Python | Ruff | Ruff |
| shared | packages/shared | Library | TypeScript | Biome | Biome |
```

If the Workspace Structure table does not yet have tool columns, add them. If the table already exists (from initspec or createprd), extend it with the new columns rather than replacing it.

### Step 8: REPORT

**For monorepos**, show per-package:
```
[apps/web] Formatter: 12 fixed | Linter: 3 remain
[apps/api] Formatter: 8 fixed | Types: 2 errors
```

**For single repos**:
```
REPORT
- Added: Formatting (Ruff)
- Config: ruff.toml created
- Fixed: 47 format issues, 12 lint errors
- Remaining: 3 type errors in src/api/handlers.ts:45, :67, :89
- Known: 5 issues in src/legacy/** (ignored per known-issues.md)
```

### Step 9: RECOMMEND

- **If issues remain**: List required actions, prompt user to rerun audit after fixing
- **If all configured tools pass**: Recommend pipeline as next step
- **If all 6 bundles configured and passing**: Confirm completion, recommend pipeline

## Dry Run Output

```
AUDIT PREVIEW (DRY RUN)

Repository: monorepo (Turborepo)
Packages: apps/web, apps/api, packages/shared
Stack: Python 3.12, Node 20
Package managers: uv, pnpm

Configured: Formatting, Linting, Type Safety, Testing
Missing: Observability, Git Hooks

Would add: Observability
Would install: structlog (apps/api), pino (apps/web, packages/shared)
Would create: logs/ directory with .gitignore
Would create: src/logging_config.py (apps/api), src/logger.ts (apps/web)
Would run: ruff format, ruff check, biome format, biome lint, mypy, tsc, pytest, vitest

Run without --dry-run to apply.
```

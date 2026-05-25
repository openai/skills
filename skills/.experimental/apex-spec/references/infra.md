# infra

Add and validate production infrastructure one bundle at a time.

## Rules

1. **One bundle per run** - add one, validate all
2. **Stack agnostic** - read platform from CONVENTIONS.md, adapt
3. **Document manual steps** - only for things that genuinely require UI access or sudo you don't have
4. **Don't store secrets** - document required env vars, don't create them
5. **Validate everything** - verify infra actually works, not just exists
6. **Respect known-issues.md** - skip items marked as manual-only

### No Deferral Policy

- NEVER mark a task as "pending", "requires X", or "blocked" if the blocker is something YOU can resolve
- If a service needs to be running, START IT (e.g., `docker compose up -d db`)
- If a dependency needs installing, INSTALL IT
- If a config file needs generating, GENERATE IT
- "The environment isn't set up" is NOT a blocker -- setting it up IS the task
- The ONLY valid blocker is something that requires USER input, credentials you don't have, or sudo access
- If you skip a task that was executable, that is a **critical failure**

## Master List (4 Bundles)

Industry standard order (availability to automation):

| Priority | Bundle | Contents |
|----------|--------|----------|
| 1 | **Health** | /health endpoint + platform probes |
| 2 | **Security** | WAF rules + rate limiting |
| 3 | **Backup** | DB backup + storage + retention policy |
| 4 | **Deploy** | CD webhook/trigger from main branch |

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--dry-run` | false | Preview what would happen without changes |
| `--skip-install` | false | Don't create configs or scripts |
| `--verbose` | false | Show full command output |

## Flow

### Step 1: DETECT

1. Check for `.spec_system/CONVENTIONS.md`
   - If missing: Run initspec yourself to create it. Only ask the user if initspec requires user input you don't have.
   - Read Infrastructure table for configured components
   - Identify: CDN, hosting platform, database, cache, backup, deploy

2. Read `.spec_system/state.json` for monorepo context:
   - `monorepo` field: `true` / `false` / `null`
   - `packages` array (when `monorepo: true`): each entry has `name`, `path`, `type`, `stack`

3. Detect infrastructure from existing files/configs:
   - `wrangler.toml` = Cloudflare
   - `docker-compose.yml`, `coolify.json` = Coolify/Docker
   - `vercel.json` = Vercel
   - `fly.toml` = Fly.io
   - Terraform/Pulumi files = IaC detected
   - **Monorepo**: Also check for per-package infra configs (e.g., `apps/web/vercel.json`, `apps/api/fly.toml`, `apps/api/Dockerfile`)

4. Check for `.spec_system/audit/known-issues.md`
   - Load Skipped Infra section
   - Note: "Known issues loaded (N infra items skipped)"

5. If `--dry-run`: Skip to Dry Run Output

### Step 1a: Identify Deployment Topology (Monorepo Only)

**Skip this step if** `monorepo` is not `true` in state.json.

When `monorepo: true`, classify each package by deployment role:

1. **Deployable units**: Packages with `type` of frontend, backend, or service -- these need their own health endpoints, deploy triggers, and potentially their own backup/security configs
2. **Shared libraries**: Packages with `type` of library -- these are built and consumed by other packages, not deployed independently
3. **Shared infrastructure**: Components used by multiple packages (e.g., a single database, shared cache) -- configured once at repo level

Example deployment topology:
```
Deployment topology (monorepo: true):
| Package | Path | Type | Deploys Independently | Platform |
|---------|------|------|-----------------------|----------|
| web | apps/web | Frontend | Yes | Vercel |
| api | apps/api | Backend | Yes | Coolify |
| shared | packages/shared | Library | No | (built only) |

Shared infra: PostgreSQL (apps/api), Valkey cache (apps/api)
```

### Step 2: COMPARE

Compare Infrastructure table against 4-bundle master list:
- Health: Is there a /health endpoint? Platform probe configured?
- Security: WAF rules present? Rate limiting configured?
- Backup: Backup script/job exists? Storage configured?
- Deploy: CD trigger configured?

Build list of missing bundles in priority order.

If all bundles configured: "All infrastructure configured. Jumping to Step 5 to Validate."

### Step 3: SELECT

Pick the highest-priority missing bundle from Step 2.

Output: "Selected: [Bundle Name] - not yet configured"

### Step 4: IMPLEMENT

Add configuration for the selected bundle.

**Stack-agnostic implementations:**

| Bundle | Component | Implementation varies by platform |
|--------|-----------|-----------------------------------|
| Health | Endpoint | FastAPI, Express, Go handler, etc. |
| Health | Probe | Coolify, Kubernetes, ECS, Vercel, etc. |
| Security | WAF | Cloudflare, AWS WAF, Vercel Firewall |
| Security | Rate Limit | slowapi, express-rate-limit, in-platform |
| Backup | Script | pg_dump, mongodump, mysqldump |
| Backup | Storage | R2, S3, GCS, local |
| Backup | Schedule | Cron, GitHub Actions, platform scheduler |
| Deploy | Trigger | Webhook, Git push, platform integration |

**Monorepo implementation strategy** (when `monorepo: true`):

Use the deployment topology from Step 1a to scope each bundle:

- **Health**: Each deployable package gets its own `/health` endpoint. Shared libraries do not need health endpoints.
- **Security**: WAF/rate limiting applies per deployable package. Shared WAF rules go at CDN level if all packages share a domain; per-package if separate domains.
- **Backup**: Scope to databases -- if all packages share one DB, one backup script. If packages have separate databases, per-database backups.
- **Deploy**: Each deployable package gets its own deploy trigger. Shared libraries trigger rebuilds of dependent packages (handled by CI, not infra).

**Single-repo**: All bundles apply to the single deployment target.

**Implementation by detected stack:**

**Health Bundle:**
```python
# FastAPI example
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": await check_db(),
        "cache": await check_cache(),
        "timestamp": datetime.utcnow().isoformat()
    }
```

1. Create /health endpoint in detected framework
2. Add DB and cache connectivity checks
3. Configure platform health probe (if platform detected)
4. **Monorepo**: Repeat for each deployable package using its stack. Skip library packages.

**Security Bundle:**
1. If Cloudflare: Document WAF ruleset to enable (OWASP Core)
2. Add rate limiting middleware to application
3. Document rate limit configuration
4. **Monorepo**: Add rate limiting per deployable package using its framework's middleware

**Backup Bundle:**
1. Create backup script for detected database
2. Configure storage destination
3. Create schedule (cron or GitHub Action)
4. Document retention policy
5. **Monorepo**: If packages use separate databases, create per-database backup scripts. Note which package owns which database.
6. Verify backup: restore to ephemeral DB and run a sanity query to confirm data integrity

**Deploy Bundle:**
1. Configure webhook URL (Coolify, Render, etc.)
2. Or configure Git-based deploy (Vercel, Netlify)
3. Add deploy step to release workflow
4. Document rollback procedure (platform revert, previous image tag, or git revert + redeploy)
5. **Monorepo**: Configure per-package deploy triggers. Ensure shared library changes trigger dependent package deploys.

**Local Dev Environment** (verified alongside Deploy bundle):
1. If `docker-compose.yml` or `compose.yml` exists, verify `docker compose up -d` brings all services to healthy state
2. If no compose file but the project has services (DB, cache, queue), document the local start procedure in CONVENTIONS.md
3. Verify the app responds locally (e.g., `curl http://localhost:[port]/health`)
4. Record the local start command in CONVENTIONS.md Infrastructure table: `| Local Dev | [command] | [details] |`

### Step 5: VALIDATE

Verify all configured infrastructure:

1. **Health**: `curl` the /health endpoint, verify 200 + JSON
2. **Security**: Verify rate limiting works (test with rapid requests)
3. **Backup**: Verify backup runs, check storage for recent backup
4. **Deploy**: Trigger test deploy or verify webhook connectivity

**Monorepo**: Validate each deployable package independently. A health check failing in one package does not skip validation of others. Report per-package results.

**Validation commands by component:**

| Component | Validation |
|-----------|------------|
| Health endpoint | `curl -f https://domain.com/health` |
| Rate limiting | Rapid requests should get 429 |
| Backup | Check storage for file < 24h old; optionally restore to ephemeral DB and run sanity query |
| Deploy webhook | `curl -X POST webhook_url` (dry-run if possible) |
| Local dev | `docker compose up -d` + `curl http://localhost:[port]/health` |
| Rollback | Verify documented rollback procedure is executable |

### Step 6: FIX

For each validation failure:

1. **Health endpoint missing**: Create it (Step 4)
2. **Health returns error**: Fix DB/cache connectivity
3. **Rate limiting not working**: Check middleware order, config
4. **Backup missing/stale**: Run backup manually, fix schedule
5. **Deploy webhook fails**: Verify URL, check platform logs

**After 3 failed attempts**: Try a different approach entirely. Only log for manual review if the fix requires sudo, platform UI access, or credentials you don't have.

Filter out items in known-issues.md Skipped Infra section.

### Step 7: RECORD

Update `.spec_system/CONVENTIONS.md` Infrastructure table:

```markdown
| Component | Provider | Details |
|-----------|----------|---------|
| CDN/DNS | Cloudflare | - |
| WAF | Cloudflare | OWASP ruleset enabled |
| Hosting | Coolify | 8GB VPS |
| Database | PostgreSQL 16 | Coolify-managed |
| Backup | R2 | pg_dump, daily, 7-day retention |
| Deploy | Coolify webhook | On push to main |
```

**Monorepo only**: When packages have different deployment targets, add a Package column to distinguish per-package infra:

```markdown
| Component | Package | Provider | Details |
|-----------|---------|----------|---------|
| CDN/DNS | (shared) | Cloudflare | - |
| Hosting | apps/web | Vercel | Git-based deploy |
| Hosting | apps/api | Coolify | Docker, 8GB VPS |
| Database | apps/api | PostgreSQL 16 | Coolify-managed |
| Health | apps/web | Vercel | Automatic (serverless) |
| Health | apps/api | Coolify | /health, 30s interval |
| Deploy | apps/web | Vercel | On push to main |
| Deploy | apps/api | Coolify webhook | On push to main |
```

Use `(shared)` for components that serve multiple packages.

### Step 8: REPORT

**Single-repo:**
```
REPORT
- Added: Health bundle
- Created: src/api/health.py
- Configured: Coolify health probe (HTTP, /health, 30s interval)
- Validated: Endpoint returns 200, DB check passes, cache check passes
- Response time: 45ms

Platform notes:
- Coolify probe configured via UI (manual step documented)
```

**Monorepo:**
```
REPORT
- Added: Health bundle

[apps/api] Health: /health endpoint created (FastAPI)
  - Configured: Coolify probe (HTTP, /health, 30s)
  - Validated: 200 OK, DB pass, cache pass (45ms)

[apps/web] Health: Automatic (Vercel serverless)
  - Validated: 200 OK (120ms)

[packages/shared] Skipped (library, not deployed)
```

**If secrets/manual steps required:**
```
Required setup:
1. In Coolify dashboard, set health check path to /health
2. Set health check interval to 30 seconds
3. Enable "Restart on unhealthy" option
```

### Step 9: RECOMMEND

- **Validation failures remain**: List required actions, prompt rerun of infra
- **Bundles remain**: Note remaining bundles, recommend rerun of infra
- **All 4 bundles configured and validated**: Recommend documents

## Dry Run Output

```
INFRA PREVIEW (DRY RUN)

Stack detected:
- CDN: Cloudflare
- Platform: Coolify
- Database: PostgreSQL 16
- Cache: Valkey

Configured: Health, Security
Missing: Backup, Deploy

Would add: Backup
Would create: scripts/backup.sh
Would configure: Cron schedule (daily 02:00 UTC)
Would store: Cloudflare R2 (bucket: backups)

Required setup:
- R2_ACCESS_KEY_ID in environment
- R2_SECRET_ACCESS_KEY in environment

Run without --dry-run to apply.
```

## Platform-Specific Notes

**Cloudflare:**
- WAF rules configured via dashboard or Terraform
- Document which rulesets to enable
- R2 for backup storage

**Coolify:**
- Health probes configured via UI
- Webhook URL available in deployment settings
- Supports Docker and static deploys

**Vercel:**
- Health checks automatic for serverless
- Rate limiting via Edge Config or middleware
- Git-based deploys, no webhook needed

**AWS/ECS:**
- Health checks via target group
- WAF via AWS WAF
- Backups via RDS snapshots or custom scripts

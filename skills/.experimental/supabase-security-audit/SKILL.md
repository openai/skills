---
name: supabase-security-audit
description: Audit and harden Supabase or PostgreSQL projects by reviewing database schema, row level security coverage, policy correctness, service-role exposure, auth boundaries, and common application security mistakes. Use when Codex needs to add or fix RLS on existing tables, inspect Supabase migrations, review server and client auth code, or investigate unknown security vulnerabilities in a Supabase-backed app.
---

# Supabase Security Audit

## Overview

Audit Supabase and PostgreSQL projects for authorization gaps and common security mistakes. Prefer concrete findings and code or SQL fixes over generic advice.

## Quick Start

1. Read the migration files under `supabase/`, `db/`, or other SQL directories.
2. Read the Supabase client wrappers, auth helpers, API routes, server actions, storage handlers, and env loaders.
3. Run `python3 scripts/audit_supabase_security.py <project-root>` from this skill directory when a static scan will save time.
4. Read `references/audit-checklist.md` for the full review sequence.
5. Read `references/rls-policy-patterns.md` when writing or tightening policies.

## Workflow

### 1. Inventory the trust boundaries

List:

- public tables and views
- user-owned tables
- backend-only tables
- service-role code paths
- client code that talks to Supabase directly
- privileged functions, triggers, workers, and webhooks

Treat every `public` table as user-reachable until proven otherwise.

### 2. Check RLS coverage first

For each application table:

- Ensure `alter table ... enable row level security` exists.
- Prefer `force row level security` when owners should still be bound by policies.
- Treat `RLS enabled but no policies` as deny-all. Accept that state only when the table is intentionally backend-only.
- Flag `using (true)` and `with check (true)` for review instead of assuming they are safe.

If a table has no RLS, add it before doing anything else.

### 3. Write least-privilege policies

Choose the smallest valid audience:

- owner only
- admin only
- public read with scoped write
- join-based access through a parent ownership table

Avoid blanket `for all` policies unless the same rule is correct for every command. Prefer separate `select`, `insert`, `update`, and `delete` policies when rules differ.

### 4. Review privileged SQL

Inspect:

- `security definer` functions
- triggers that write rows on behalf of users
- grants to `anon` or `authenticated`
- views or functions that can bypass intended RLS behavior
- migrations that backfill data and forget to restore protections

Require a concrete reason for every privileged object. When a `security definer` function is necessary, keep it schema-qualified and set an explicit `search_path`.

### 5. Review application-side security

Check for:

- service-role secrets in client bundles or `NEXT_PUBLIC_*` variables
- API routes and server actions that trust user input without ownership checks
- storage upload or signing endpoints that let one user act on another user's files
- admin-only flows guarded only in the UI
- worker or webhook code that writes to tables whose policies assume end-user auth

Keep server-side authorization checks even when RLS already exists.

### 6. Apply fixes and verify

When hardening the project:

- create a new migration instead of rewriting history unless the repo clearly treats the schema as disposable
- enable RLS on uncovered tables
- add or tighten policies
- remove or narrow risky grants and helper functions
- verify that allowed actors still succeed and disallowed actors fail

## Output

Report findings in severity order with:

- object or file
- impact
- exact fix
- follow-up verification

When asked to implement hardening, summarize which actor can now access each protected table or endpoint.

## Resources

- `scripts/audit_supabase_security.py`: Static scanner for SQL RLS coverage, risky policies, privileged functions, and basic code-side exposure checks.
- `references/audit-checklist.md`: Full review checklist and live-database SQL queries.
- `references/rls-policy-patterns.md`: Reusable policy patterns for owner, admin, public, and backend-only tables.

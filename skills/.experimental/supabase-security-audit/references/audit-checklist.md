# Audit Checklist

Use this checklist when the task is a real security review rather than a quick RLS fix.

## 1. Schema inventory

- List every application table, view, function, trigger, bucket, worker, and webhook.
- Mark each table as `user-facing`, `shared/public-read`, `admin-only`, or `backend-only`.
- Treat anything in the `public` schema as exposed to authenticated users unless proven otherwise.

## 2. RLS and policy review

- Confirm `enable row level security` on every application table.
- Decide whether `force row level security` is needed.
- Review each policy by command, not only by table.
- Check `using` and `with check` separately.
- Flag `for all`, `using (true)`, and `with check (true)` for manual review.
- Confirm child-table access is constrained through the owning parent row.

## 3. Privileged SQL review

- Review every `security definer` function.
- Require an explicit `search_path` on privileged functions.
- Review custom grants to `anon`, `authenticated`, and `public`.
- Check triggers that insert rows into protected tables.
- Verify helper functions do not create policy recursion against RLS-protected tables.

## 4. App and API review

- Confirm service-role keys stay on the server only.
- Check `NEXT_PUBLIC_*` env vars for accidental secret exposure.
- Verify API routes and server actions enforce ownership before writes.
- Check uploads, download signing, and storage paths for cross-tenant access.
- Confirm admin flows are enforced on the server, not only hidden in the UI.
- Review webhook handlers and workers that bypass user-context RLS.

## 5. Verification

- Test one allowed actor and one disallowed actor for each sensitive table or endpoint.
- Confirm public pages only read rows intended for public access.
- Confirm owners cannot mutate another owner's rows.
- Confirm backend-only tables deny normal user tokens.

## Live SQL Queries

### Tables and RLS state

```sql
select
  n.nspname as schema_name,
  c.relname as table_name,
  c.relrowsecurity as rls_enabled,
  c.relforcerowsecurity as rls_forced
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where c.relkind = 'r'
  and n.nspname not in ('pg_catalog', 'information_schema')
order by 1, 2;
```

### Policies

```sql
select
  schemaname,
  tablename,
  policyname,
  cmd,
  roles,
  qual,
  with_check
from pg_policies
order by 1, 2, 3;
```

### Security definer functions

```sql
select
  n.nspname as schema_name,
  p.proname as function_name,
  p.prosecdef as security_definer
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where n.nspname not in ('pg_catalog', 'information_schema')
  and p.prosecdef
order by 1, 2;
```

## Triage

- `High`: public write access, cross-tenant reads, client-exposed secrets, or admin bypass.
- `Medium`: missing RLS, broad policies without proof they are intentional, unsafe privileged helpers.
- `Low`: missing hardening, incomplete verification, or hygiene issues that do not create direct access today.

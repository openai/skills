# RLS Policy Patterns

Use these patterns as starting points. Adapt column names and helper functions to the project.

## Owner can read and update their own row

```sql
alter table public.profiles enable row level security;

create policy "profiles self read"
on public.profiles
for select
using (id = auth.uid());

create policy "profiles self update"
on public.profiles
for update
using (id = auth.uid())
with check (id = auth.uid());
```

## Owner inserts child rows

```sql
create policy "orders buyer insert"
on public.orders
for insert
with check (buyer_id = auth.uid());
```

Match the inserted owner column in `with check`. Do not rely on a UI-hidden field.

## Child table inherits access from parent ownership

```sql
create policy "assets owner read"
on public.product_assets
for select
using (
  exists (
    select 1
    from public.products p
    where p.id = product_id
      and p.seller_id = auth.uid()
  )
);
```

Use `exists` against the owning table when the child row has no direct `user_id`.

## Public read with owner or admin override

```sql
create policy "products public approved read"
on public.products
for select
using (
  status = 'approved'
  or seller_id = auth.uid()
  or public.is_admin()
);
```

Reserve public read for explicitly public rows. Keep write policies separate.

## Admin-only table

```sql
alter table public.admin_actions enable row level security;

create policy "admin actions admin read"
on public.admin_actions
for select
using (public.is_admin());
```

Prefer explicit admin-only policies over application-only checks.

## Backend-only table

```sql
alter table public.internal_jobs enable row level security;
```

Leave the table with no user-facing policies when only service-role code should access it. Document why the deny-all state is intentional.

## Security definer helper notes

- Use `security definer` only when ordinary RLS-aware SQL cannot express the requirement.
- Set `search_path` explicitly on privileged functions.
- Keep helper functions schema-qualified.
- Avoid helper functions that query the same RLS-protected table used in their calling policy unless the recursion behavior is proven safe.

## Anti-patterns

- `with check (true)` on user-driven inserts or updates.
- `using (true)` on update or delete policies.
- one `for all` policy when read and write rules differ.
- trusting a service-role API route without server-side ownership checks.
- exposing secrets through `NEXT_PUBLIC_*`.

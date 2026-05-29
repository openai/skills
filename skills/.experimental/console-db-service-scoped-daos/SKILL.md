---
name: console-db-service-scoped-daos
description: Use when adding, reviewing, or changing `@cp/console-db` entities or DAOs in ClickHouse/control-plane where rows are owned by or associated with a `serviceId`, especially when designing lookup methods, route loading, authorization boundaries, or deciding whether an entity should be loaded by id alone.
---

# Console DB Service-Scoped DAOs

## Rule

For console-db entities associated with a `serviceId`, prefer DAO methods that require `serviceId` in lookups and mutations unless there is a clear reason not to.

An id-only lookup can load cross-service data before authorization has had a chance to prove ownership. Service-scoped DAO APIs make the safe path the default and reduce accidental existence leaks.

## Workflow

1. Identify ownership.
   - If the table has `serviceId`, or the row belongs to a service through a required parent relation, treat the entity as service-owned.
   - If ownership is org-scoped, user-scoped, or global, use the matching scope instead of forcing `serviceId`.

2. Prefer scoped DAO names and signatures.
   - Use names such as `findByIdAndServiceId`, `findByPlanIdAndServiceId`, `listByServiceId`, `updateByIdAndServiceId`, or `deleteByIdAndServiceId`.
   - Accept both the entity identifier and the owning `serviceId`.
   - Return `null` or no-op on scope mismatch where callers should treat it like not found.

3. Put the scope in the database query.
   - Query with `where: { id, serviceId }`, `where: { planId, serviceId }`, or the equivalent relational filter.
   - Do not load by id and compare `row.serviceId` in application code when the DAO can express the scope.

4. Keep unscoped methods rare and explicit.
   - Use id-only methods for global entities, internal maintenance jobs, migrations, admin-only tooling, or places where the caller has already loaded through a trusted scoped parent.
   - Name or comment these exceptions so future route code does not copy them into request paths.

5. Align route loaders with scoped DAOs.
   - Route middleware should authorize the requested service first when possible.
   - Then load the entity with `serviceId + id`.
   - Return the same missing/not-found response for absent rows and scope mismatches when avoiding existence leaks matters.

## Review Checklist

- Does the entity or one of its required parents have a `serviceId`?
- Does the DAO expose a scoped lookup/mutation for request-path use?
- Does route code use the scoped DAO instead of loading by id and checking ownership after?
- Are scope mismatches indistinguishable from missing rows where security matters?
- Do tests cover a valid id under the wrong service and prove the handler/manager is not called?
- Is any id-only DAO method justified by a non-request-path use case?

## Example Shape

```ts
export async function findByPlanIdAndServiceId(
  planId: SchemaAdvisorPlan['planId'],
  serviceId: SchemaAdvisorPlan['serviceId'],
): Promise<SchemaAdvisorPlan | null> {
  return db.schemaAdvisorPlan.findFirst({
    where: { planId, serviceId },
  });
}
```

Prefer the service-scoped method in HTTP loaders, even if a unique id-only lookup also exists.

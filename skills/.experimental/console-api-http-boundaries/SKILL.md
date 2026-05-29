---
name: console-api-http-boundaries
description: Use when working on ClickHouse/control-plane `apps/console-api` HTTP routes, routers, Express handlers, or manager boundaries, especially when adding or reviewing route handlers, deciding where to throw `ClientError`, mapping domain errors to HTTP responses, or moving logic between routers and managers.
---

# Console API HTTP Boundaries

## Rule

Keep HTTP semantics at the HTTP boundary.

Routes and Express handlers should decide HTTP status codes and response bodies. Managers should express domain operations, call collaborators, and return typed results or domain-level errors. Avoid using `ClientError` inside newly added manager code as flow control for request-specific states when the route already has the request context needed to respond.

## Workflow

1. Locate the boundary before editing.
   - Router/handler files own `req`, `res`, validation middleware, auth middleware, feature gates, and response status codes.
   - Manager files own domain orchestration, persistence calls, Temporal/client calls, and typed return values.

2. For new route code, validate and authorize at the route layer first.
   - Use existing middleware patterns such as `validateParams`, `validateData`, `requireAuth`, `userServiceAccess`, feature gates, and loaded request-scoped entities.
   - Build credentials from the authorized service identity, not from user-supplied duplicated state.

3. Return HTTP responses directly from handlers for expected request states.
   - Missing route-owned resource: `res.status(404).send(...)` or the local route pattern.
   - Conflict from route-visible state: `res.status(409).send(...)`.
   - Invalid request body: route validation schema or handler-level parse that returns `400`.
   - Domain start-policy errors from a package can be caught in the route and mapped to HTTP there.

4. Pass typed, already-authorized inputs into managers.
   - Prefer passing the loaded entity or domain object when the router already loaded it for auth.
   - Avoid making the manager reload the same row just to discover an HTTP conflict.
   - Keep managers free of `Request`, `Response`, and route-only shape assumptions.

5. Preserve existing behavior outside the touched surface.
   - Do not rewrite older manager methods only because they already throw `ClientError`.
   - Apply this rule to new code and code being actively touched unless the user asks for a broader cleanup.

## Review Checklist

- Does any new manager code throw `ClientError` for a condition the route can already see?
- Does a handler use `ClientError` only as a framework exception when direct `res.status(...).send(...)` is clearer?
- Are domain/package errors mapped to HTTP at the router boundary?
- Are validation and authorization performed before side effects?
- Does the manager receive typed domain inputs rather than raw request bodies or duplicated route identifiers?
- Are tests asserting the HTTP status at the route/supertest level when behavior is HTTP-specific?

## Acceptable Manager Errors

`ClientError` in a manager can remain acceptable when it is pre-existing local convention, when the manager is directly shared with non-router surfaces that expect it, or when the route cannot know the failure without running the manager operation. Do not broaden a PR only to eliminate old `ClientError` usage unless that is the requested task.

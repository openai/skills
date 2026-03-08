# APIs: Minimal And Controllers

Primary docs:
- https://learn.microsoft.com/aspnet/core/fundamentals/minimal-apis
- https://learn.microsoft.com/aspnet/core/web-api/
- https://learn.microsoft.com/aspnet/core/fundamentals/error-handling-api

## First Decision

Choose between:

- Minimal APIs for focused, low-ceremony HTTP endpoints
- controller-based APIs for richer MVC conventions and attribute-driven behavior

Do not mix both styles in the same feature unless that split is genuinely useful.

## Minimal API Guidance

Prefer Minimal APIs when the surface is small to medium and you want concise endpoint definitions.

Good defaults:

- organize endpoints with route groups
- keep route handlers thin
- move business logic into services
- prefer `TypedResults` over untyped results
- use endpoint filters when cross-cutting behavior belongs at the endpoint layer
- use built-in validation support on supported target frameworks

Minimal API reminders:

- handler parameters can be bound from route, query, headers, body, form, or DI
- authorization can be applied with `RequireAuthorization`
- return `IResult` or `TypedResults` when response shape matters
- use OpenAPI support for discoverable contracts

On .NET 10, Minimal APIs support built-in validation with `AddValidation()`. Use that instead of inventing parallel validation infrastructure when the target framework supports it.

## Controller API Guidance

Prefer controllers when the API needs:

- `[ApiController]` behaviors
- attribute routing and conventions
- filters
- custom formatters
- mature controller organization in an existing codebase

Controller defaults:

- derive API controllers from `ControllerBase`
- annotate with `[ApiController]`
- use attribute routing
- return ProblemDetails-compatible failures
- let automatic model validation handle invalid requests unless there is a concrete override requirement

Key `[ApiController]` behaviors:

- attribute routing is required
- invalid model state automatically becomes HTTP 400
- binding source inference applies
- error responses use ProblemDetails patterns

## Shared API Practices

- Keep request and response DTOs separate from persistence models
- Use version-stable route and payload contracts
- Use `CreatedAt...` patterns for resource creation
- Prefer explicit status codes and typed results over implicit behavior
- Apply authorization at the endpoint or controller boundary, not only inside service methods
- Use `ProblemDetails` for errors instead of ad hoc JSON shapes

## Browser-Facing Notes

- Be careful with cookie-authenticated API endpoints and CORS
- For browser-based form or file upload endpoints, account for antiforgery requirements
- In ASP.NET Core 10, known API endpoints no longer use cookie-login redirects by default; rely on API-appropriate unauthorized responses instead

## Native AOT

Use `dotnet new webapiaot` only when native AOT is an explicit deployment requirement. Treat it as a constraint that affects library choice, reflection, JSON patterns, and compatibility.

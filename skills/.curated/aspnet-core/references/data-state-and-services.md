# Data, State, And Services

Primary docs:
- https://learn.microsoft.com/aspnet/core/data/
- https://learn.microsoft.com/aspnet/core/fundamentals/dependency-injection
- https://learn.microsoft.com/aspnet/core/fundamentals/http-requests
- https://learn.microsoft.com/aspnet/core/fundamentals/app-state

## Dependency Injection Defaults

- Register infrastructure and business services in `Program.cs`
- Inject dependencies through constructors by default
- Keep scoped services request-bound
- Avoid resolving scoped services from singletons
- Use keyed or named patterns only when there is a real need for multiple implementations

## EF Core And DbContext

Use EF Core for common relational data access patterns unless the repository already uses another data layer.

Default guidance:

- register `DbContext` with `AddDbContext`
- treat `DbContext` as scoped
- keep queries and transactions in services, not UI code
- use migrations intentionally
- keep entities out of public API contracts and UI view models

Use `IDbContextFactory<TContext>` when the execution model is not request-scoped, such as:

- Blazor components with longer-lived scopes
- background services
- explicit factory-driven data work

## Options And Configuration

- Bind structured configuration into options classes
- validate options early when bad configuration should fail fast
- keep configuration access close to the service that owns it
- avoid scattering raw configuration keys across the codebase

## Outbound HTTP

Use `IHttpClientFactory` for outbound HTTP calls.

Prefer:

- named clients for distinct external systems
- typed clients for richer integrations
- delegating handlers for retries, headers, or telemetry concerns

Avoid manual `new HttpClient()` patterns scattered through request handlers.

## App State

Use the smallest state mechanism that fits:

- query string or route values for transparent request state
- form posts for user input
- TempData for short-lived redirect-friendly messages
- session only when necessary and with an understanding of its server-side and scaling implications

Do not treat session as the primary application data store.

## Caching And State Boundaries

- Keep cached data derivable from a durable source
- Separate cache shape from persistence shape when it improves safety or performance
- Revisit session, in-memory cache, and singleton state when the app scales to multiple instances

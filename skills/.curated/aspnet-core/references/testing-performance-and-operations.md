# Testing, Performance, And Operations

Primary docs:
- https://learn.microsoft.com/aspnet/core/test/integration-tests
- https://learn.microsoft.com/aspnet/core/host-and-deploy/
- https://learn.microsoft.com/aspnet/core/host-and-deploy/health-checks
- https://learn.microsoft.com/aspnet/core/performance/

## Testing Strategy

Use layered testing instead of relying on one style:

- unit tests for pure services and business logic
- integration tests for request pipeline, DI, database, auth, and framework wiring
- browser tests for end-to-end user flows

## Integration Tests

Use `Microsoft.AspNetCore.Mvc.Testing` and `WebApplicationFactory<Program>` for integration tests.

Guidance from the official docs:

- use a test host and `HttpClient`
- replace services with test doubles when needed
- control redirects when asserting auth behavior
- handle antiforgery correctly for form posts
- prefer SQLite in-memory over the EF Core in-memory provider for more realistic database tests

For SPA or browser-driven scenarios, Microsoft recommends browser automation such as Playwright for .NET.

## Performance Defaults

Reach for built-in features before custom optimization layers:

- output caching
- response caching where appropriate
- response compression
- HTTP request timeouts
- rate limiting
- static file handling

General performance guidance:

- measure first
- keep database and network round trips visible
- reduce payload size
- use streaming or pagination when data is large
- keep synchronous blocking out of hot paths

## Health Checks And Observability

Add health checks for dependencies that matter operationally.

Use separate checks or tags when you need:

- liveness
- readiness
- dependency-specific health surfaces

Also ensure:

- structured logs
- request tracing where applicable
- metrics for critical paths such as auth, API latency, and background work

## Hosting And Deployment

Typical deployment flow:

1. `dotnet publish`
2. deploy the publish output
3. run behind a process manager
4. place a reverse proxy in front when the environment requires it

Know the deployment environment:

- IIS or Windows Service on Windows
- Kestrel plus Nginx or another reverse proxy on Linux
- container hosting when the platform expects it

Behind proxies or load balancers:

- configure forwarded headers
- validate scheme, host, and remote IP behavior
- test auth redirects and callback URLs in the deployed topology

## Operational Safeguards

- add health checks for databases and critical external services
- fail fast on invalid configuration where possible
- keep secrets out of publish artifacts
- verify data-protection key persistence in multi-instance deployments

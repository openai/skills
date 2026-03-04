# Program And Pipeline

Primary docs:
- https://learn.microsoft.com/aspnet/core/fundamentals/
- https://learn.microsoft.com/aspnet/core/fundamentals/minimal-apis/webapplication
- https://learn.microsoft.com/aspnet/core/fundamentals/middleware/
- https://learn.microsoft.com/aspnet/core/fundamentals/configuration/

## Startup Shape

Prefer the modern hosting model:

1. Create `var builder = WebApplication.CreateBuilder(args);`
2. Register services on `builder.Services`
3. Build `var app = builder.Build();`
4. Configure middleware in the correct order
5. Map endpoints
6. Call `app.Run();`

Use older `Startup` patterns only when the repository already uses them or the task is migration.

## Service Registration

- Register framework services explicitly: Razor Pages, controllers, Razor components, authentication, authorization, health checks, rate limiting, response compression, output caching, EF Core, and `IHttpClientFactory`
- Keep business logic in services instead of controllers, page models, or route handlers
- Use constructor injection as the default
- Use options classes for structured configuration
- Choose lifetimes intentionally:
  - singleton: stateless or shared infrastructure
  - scoped: request-bound work such as `DbContext`
  - transient: lightweight stateless services

## Configuration Defaults

`WebApplication.CreateBuilder` already loads configuration from common providers such as:

- `appsettings.json`
- environment-specific `appsettings.{Environment}.json`
- environment variables
- command-line arguments

For secrets:

- use Secret Manager in development
- use a secure external store in production
- do not commit secrets to source control

## Middleware Order

Middleware order is a frequent source of broken behavior. Favor this shape and adjust only with a concrete reason:

1. Forwarded headers if behind a proxy or load balancer
2. Exception handling and HSTS for non-development environments
3. HTTPS redirection
4. Static files
5. Routing when explicit routing middleware is needed
6. CORS when endpoints require it
7. Authentication
8. Authorization
9. Endpoint-specific middleware such as rate limiting or session as required
10. Endpoint mapping with `MapRazorPages`, `MapControllers`, `MapGet`, `MapHub`, or `MapGrpcService`

Important ordering rules:

- Call `UseAuthentication()` before `UseAuthorization()`
- Keep proxy/header processing before auth, redirects, and link generation
- Do not insert custom middleware randomly between auth and authorization without a reason
- In Minimal API apps, explicit `UseRouting()` is usually unnecessary unless you need to control order

## Routing And Endpoints

- Prefer endpoint routing everywhere
- Use route groups for larger Minimal API surfaces
- Keep MVC and API routes explicit and predictable
- Use areas only when the application is large enough to benefit from bounded sections
- Keep endpoint names stable when generating links or integrating with clients

## Error Handling

- Use centralized exception handling instead of scattered `try/catch` blocks for ordinary request failures
- Prefer ProblemDetails-style responses for APIs
- Keep the developer exception page limited to development
- Separate user-facing failures from internal exception details

## Logging And Diagnostics

- Use `ILogger<T>` from DI
- Log structured values, not concatenated strings
- Put correlation and request diagnostics in middleware or infrastructure, not business logic
- Enable HTTP logging only when the scenario warrants it and avoid leaking sensitive data

## Static Assets And Web Root

- Keep public assets in `wwwroot`
- Treat the web root as publicly readable content
- Prevent publishing local-only static content through project file rules when needed
- Use Razor Class Libraries for reusable UI assets across apps

## Architectural Defaults

- Keep `Program.cs` readable; extract feature registration to extension methods when it starts accumulating unrelated concerns
- Prefer vertical slices or feature folders over giant "Controllers", "Services", and "Repositories" buckets with weak boundaries
- Keep framework configuration close to the host and business logic out of it

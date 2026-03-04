# Versioning And Upgrades

Primary docs:
- https://learn.microsoft.com/aspnet/core/release-notes/
- https://learn.microsoft.com/aspnet/core/release-notes/aspnetcore-10.0
- https://learn.microsoft.com/aspnet/core/release-notes/aspnetcore-9.0
- https://github.com/dotnet/AspNetCore.Docs/tree/main/aspnetcore/breaking-changes

## Versioning Default

- For new production apps in March 2026, prefer `net10.0`
- For existing apps, match the repository's target framework unless the task is explicitly an upgrade
- Before using a new API, confirm it exists in the target framework

## Upgrade Workflow

1. Identify the current target framework and SDK
2. Read the "What's new" and breaking-changes pages for each version hop
3. Compile and resolve obsoletions intentionally
4. Re-run integration tests and auth flows
5. Re-test deployment-specific behavior such as proxies, cookies, and static assets

## High-Value Breaking-Change Checks

When moving to ASP.NET Core 10, watch for:

- cookie login redirects disabled for known API endpoints
- `WithOpenApi` deprecation
- `WebHostBuilder`, `IWebHost`, and `WebHost` obsolescence
- Razor runtime compilation obsolescence

When moving to ASP.NET Core 9, watch for:

- `ValidateOnBuild` and `ValidateScopes` enabled in development when using `HostBuilder`
- middleware constructor expectations and DI validation changes

When moving to ASP.NET Core 8, watch for:

- Minimal API `IFormFile` antiforgery requirements
- `AddRateLimiter()` and `AddHttpLogging()` requirements when corresponding middleware is used

## Migration Principles

- Prefer migration to the modern hosting model when touching startup extensively
- Remove compatibility shims only after tests confirm behavior
- Avoid mixing new framework idioms with old startup architecture in a half-migrated state
- Keep one authoritative target framework in project files unless multi-targeting is deliberate

## Preview Feature Rule

Do not introduce preview-only APIs or docs guidance unless the user explicitly asks for preview adoption or the repository is already on preview SDKs.

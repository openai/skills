# Security And Identity

Primary docs:
- https://learn.microsoft.com/aspnet/core/security/
- https://learn.microsoft.com/aspnet/core/security/authentication/identity
- https://learn.microsoft.com/aspnet/core/security/authorization/introduction

## Security Defaults

- Use the most secure authentication flow available
- Keep secrets out of source code and plain configuration files
- Use Secret Manager in development
- Use a secure production secret store
- Enforce HTTPS
- Apply least privilege to users, services, and data access

## Authentication And Authorization

Authentication answers who the user or caller is. Authorization answers what they can do.

Default pipeline order:

1. `UseAuthentication()`
2. `UseAuthorization()`

Apply authorization at boundaries:

- `[Authorize]` on controllers, actions, page models, or hubs
- `RequireAuthorization()` on endpoints and route groups
- policies for reusable rules
- roles only when role-based checks are actually the right abstraction

Use `AllowAnonymous` sparingly and intentionally.

## Identity

Use ASP.NET Core Identity when the app needs first-party user accounts, login flows, password management, email confirmation, MFA, or related account management.

Useful starting points:

- `dotnet new webapp -au Individual`
- `dotnet new mvc -au Individual`

Identity guidance:

- scaffold only the pages you truly need to customize
- keep Identity UI updates maintainable; full scaffolding increases merge and upgrade cost
- use policies and claims for authorization rather than encoding all decisions in page logic
- persist data-protection keys appropriately in multi-instance deployments

On ASP.NET Core 10, Identity metrics are available for observing auth-related behavior. Use them when the app has meaningful authentication traffic or security monitoring requirements.

## CSRF, CORS, And Browser Security

- Use antiforgery protection for cookie-based interactive apps and form posts
- Do not confuse CORS with authentication or authorization
- Avoid permissive `AllowAnyOrigin` plus credentials combinations
- Treat browser-side state as untrusted

## HTTPS, HSTS, And Forwarded Headers

- redirect HTTP to HTTPS
- enable HSTS outside development when appropriate
- configure forwarded headers correctly when behind proxies or load balancers
- do not generate links or evaluate scheme-sensitive behavior before proxy headers are processed

## Data Protection And Secrets

- persist data-protection keys outside ephemeral local storage when the app runs on multiple instances
- do not use environment variables as the preferred long-term home for production secrets when a stronger secret store is available
- never check production credentials into source control

## Blazor Note

For Blazor apps, read the general ASP.NET Core security guidance first and then the Blazor-specific security docs. Some Blazor security guidance adds to or supersedes the general guidance.

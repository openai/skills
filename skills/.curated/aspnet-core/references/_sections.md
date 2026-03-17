# Reference Sections

Use this file as the routing table for the rest of the skill.

## Start Here

- New app or major redesign: `stack-selection.md` -> `program-and-pipeline.md` -> one primary app-model reference -> `security-and-identity.md` -> `testing-performance-and-operations.md`
- Existing app feature work: primary app-model reference -> `program-and-pipeline.md` -> any needed cross-cutting references
- API-first work: `apis-minimal-and-controllers.md` -> `security-and-identity.md` -> `data-state-and-services.md` -> `testing-performance-and-operations.md`
- Authentication, authorization, or secrets: `security-and-identity.md`
- Realtime, streaming, or background processing: `realtime-grpc-and-background-work.md`
- Upgrade or migration work: `versioning-and-upgrades.md`

## Primary References

| File | Open when |
| --- | --- |
| `stack-selection.md` | Choose Blazor, Razor Pages, MVC, Minimal APIs, controllers, SignalR, or gRPC |
| `program-and-pipeline.md` | Structure `Program.cs`, services, configuration, middleware, routing, logging, static files, and app startup |
| `ui-blazor.md` | Build or review Blazor Web Apps and component-based UI |
| `ui-razor-pages.md` | Build or review page-focused server-rendered applications |
| `ui-mvc.md` | Build or review controller/view applications |
| `apis-minimal-and-controllers.md` | Build or review HTTP APIs |

## Cross-Cutting References

| File | Open when |
| --- | --- |
| `data-state-and-services.md` | Register services, use EF Core, handle options/configuration, or manage app state |
| `security-and-identity.md` | Add Identity, cookies, bearer auth, policies, CORS, CSRF, HTTPS, or secrets handling |
| `realtime-grpc-and-background-work.md` | Add SignalR, gRPC, streaming, or hosted services |
| `testing-performance-and-operations.md` | Add tests, caching, compression, health checks, rate limits, deployment, or proxy configuration |
| `versioning-and-upgrades.md` | Migrate across ASP.NET Core versions, avoid obsolete APIs, or target preview features deliberately |
| `source-map.md` | Map a task to the official ASP.NET Core documentation tree |

## Reading Strategy

- Open one app-model reference at a time unless the codebase genuinely mixes models.
- Prefer the framework's built-in abstractions first.
- Check `versioning-and-upgrades.md` before introducing APIs that might not exist in the repository's target framework.

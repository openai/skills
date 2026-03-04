# Stack Selection

Primary docs:
- https://learn.microsoft.com/aspnet/core/
- https://learn.microsoft.com/aspnet/core/blazor/
- https://learn.microsoft.com/aspnet/core/razor-pages/
- https://learn.microsoft.com/aspnet/core/mvc/overview
- https://learn.microsoft.com/aspnet/core/web-api/
- https://learn.microsoft.com/aspnet/core/fundamentals/minimal-apis

## Default Version Choice

- Prefer the latest stable .NET and ASP.NET Core for new production work.
- As of March 2026, that means `net10.0` unless the repository or user request says otherwise.
- Treat ASP.NET Core 11 as preview. Do not adopt preview APIs by default.
- If the repository already targets `net8.0`, `net9.0`, or another framework, stay within that target unless the task is explicitly an upgrade.

## Template Short Names

The current .NET 10 SDK templates include:

- `dotnet new blazor`
- `dotnet new webapp`
- `dotnet new mvc`
- `dotnet new webapi`
- `dotnet new webapiaot`
- `dotnet new grpc`
- `dotnet new web`
- `dotnet new razorclasslib`

Verify template names with `dotnet new list` if the environment differs.

## Application Model Matrix

| Model | Prefer when | Watch out for | Typical starting point |
| --- | --- | --- | --- |
| Blazor Web App | Build full-stack .NET UI with SSR plus optional interactivity | Interactive server needs a live connection; WebAssembly increases payload size | `dotnet new blazor` |
| Razor Pages | Build page-focused CRUD, forms, dashboards, and line-of-business apps | Authorization cannot be applied per page handler; use MVC if handler-level control matters | `dotnet new webapp` |
| MVC | Build large server-rendered apps with clear controller/view separation, filters, and action-based patterns | More ceremony than Razor Pages for simple page flows | `dotnet new mvc` |
| Minimal APIs | Build focused HTTP APIs, internal services, lightweight backends, and small surface areas | Route handlers can become hard to manage if business logic or metadata grows without structure | `dotnet new webapi` or `dotnet new web` |
| Controller-based Web API | Build APIs that benefit from `[ApiController]`, content negotiation, filters, formatters, and mature controller conventions | More ceremony than Minimal APIs for small endpoints | `dotnet new webapi` |
| SignalR | Add server push, live updates, chat, collaborative UI, or notifications | Requires connection lifecycle management and scale-out planning | Add to an existing ASP.NET Core app |
| gRPC | Build service-to-service or streaming RPC over HTTP/2 | Browser support is different from ordinary JSON APIs; use gRPC-Web only when needed | `dotnet new grpc` |

## Fast Heuristics

- Choose Blazor Web App when the UI itself should be a .NET component model.
- Choose Razor Pages when the app is mostly page and form oriented.
- Choose MVC when actions, views, filters, and controller conventions are the center of the design.
- Choose Minimal APIs first for small to medium HTTP services.
- Switch to controllers when the API needs richer attribute-driven behavior, custom formatters, or strong alignment with existing MVC/Web API conventions.
- Keep the current app model in an existing codebase unless the mismatch is causing real complexity.

## Mixed-Model Guidance

ASP.NET Core can mix models in one host. Common combinations:

- Razor Pages or MVC for server-rendered UI plus Minimal APIs for AJAX or mobile endpoints
- Blazor Web App plus Minimal APIs for external integration endpoints
- MVC or Razor Pages plus SignalR for live updates
- Web API plus gRPC for internal service-to-service calls

Mix models only when it simplifies the public surface. Do not add a second app model just because ASP.NET Core allows it.

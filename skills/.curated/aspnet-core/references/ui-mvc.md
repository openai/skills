# MVC

Primary docs:
- https://learn.microsoft.com/aspnet/core/mvc/overview
- https://learn.microsoft.com/aspnet/core/mvc/controllers/
- https://learn.microsoft.com/aspnet/core/mvc/views/

## Choose MVC When Actions And Views Matter

Prefer MVC when the application benefits from explicit controllers, action-based routing, filters, view models, and a strong separation between orchestration and presentation.

This is often the right fit for:

- large server-rendered sites
- applications with many cross-cutting filters or action conventions
- applications that mix views and APIs in the same controller layer
- teams already organized around controllers and views

## Core Shape

Enable MVC with views using:

- `builder.Services.AddControllersWithViews();`
- `app.MapControllerRoute(...)`

Keep views focused on presentation. Keep controllers focused on HTTP orchestration. Put business rules in services.

## Controller Guidance

- Derive from `Controller` when the controller returns views
- Keep actions small and explicit
- Use model binding and validation instead of manual request parsing
- Return view models, not EF entities, to views
- Use POST-Redirect-GET for form submissions

## View Guidance

- Use layouts, partial views, and Tag Helpers to keep markup consistent
- Keep complex display logic out of Razor markup when it becomes hard to follow
- Use strongly typed view models
- Avoid coupling views directly to persistence models

## Structure And Scale

- Use areas for large bounded sections such as Admin or BackOffice
- Keep route conventions explicit
- Apply filters when behavior truly belongs at the MVC layer
- Avoid giant god controllers; split by cohesive feature or resource

## Choosing MVC Over Razor Pages

Prefer MVC over Razor Pages when:

- multiple related actions share controller-level behavior
- handler-level authorization or action filters matter
- URL and action design are more natural than page-file routing

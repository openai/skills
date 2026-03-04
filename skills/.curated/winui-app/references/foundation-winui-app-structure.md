---
title: WinUI App Structure
priority: HIGH
tags: app-structure, xaml, resources, pages, bindings, csharp
sources:
  - https://github.com/microsoft/WinUI-Gallery
  - https://learn.microsoft.com/windows/apps/winui/
---

## What This Reference Is For

Use this file when structuring a WinUI 3 app, reviewing project layout, or deciding where shell, pages, controls, resources, and view models should live.

## Prefer

- A clear C#-first folder split such as `Pages`, `Controls`, `ViewModels`, `Services`, `Styles`, and `Assets`.
- `App.xaml` and shared resource dictionaries for app-wide theme resources and styles.
- A single main shell window that owns navigation and common chrome.
- Native command surfaces such as `CommandBar` for grouped window or page actions before inventing a custom toolbar composition.
- Strongly typed `x:Bind` where it improves compile-time safety and performance.

## Avoid

- Putting shell logic, page logic, and resource definitions into one large window file.
- Scattering theme brushes and styles across many page-local dictionaries.
- Introducing MVVM ceremony that the project will not actually maintain.

## Recommended Shape

- `App.xaml` / `App.xaml.cs`
  - global resources, startup, window creation, app-level exceptions
- `MainWindow.xaml` / `MainWindow.xaml.cs`
  - shell, title bar, top-level navigation host
- `Pages/`
  - page views and page-specific logic
- `Controls/`
  - reusable WinUI user controls
- `ViewModels/`
  - state and commands when the app benefits from separation
- `Styles/`
  - resource dictionaries, theme tokens, shared control styles
- `Helpers/` or `Services/`
  - windowing, navigation, persistence, OS integration helpers

## Binding Guidance

- Prefer `x:Bind` for page-local properties, event handlers, and strongly typed view model access.
- Use `Binding` where the data context is dynamic or a template must stay flexible.
- Avoid binding patterns that depend on unclear page lifetime or implicit data contexts.

## WinUI Gallery Anchors

- `App.xaml.cs` shows app-level startup and integration points.
- `MainWindow.xaml` shows shell composition, title bar usage, and search integration.
- `Pages/` and `Samples/` show how Microsoft organizes pages, helpers, and styles in a real WinUI companion app.

## Review Checklist

- Are app resources centralized?
- Is shell logic separated from content pages?
- Are bindings explicit and maintainable?
- Is the structure consistent with the scale of the app?

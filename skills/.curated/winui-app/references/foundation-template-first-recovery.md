---
title: Template-First Recovery for Startup and XAML Failures
priority: CRITICAL
tags: template, recovery, xaml-compiler, msb3073, startup
sources:
  - https://learn.microsoft.com/windows/apps/get-started/start-here
  - https://learn.microsoft.com/windows/apps/windows-app-sdk/deploy-packaged-apps
  - https://learn.microsoft.com/windows/apps/windows-app-sdk/deploy-unpackaged-apps
  - https://github.com/microsoft/WinUI-Gallery
---

## What This Reference Is For

Use this file when a new app should stay close to the `dotnet new winui` scaffold, or when opaque `MSB3073`, `XamlCompiler.exe`, and startup failures make it unclear whether the problem is in app code, shared resources, or the surrounding project structure.

## Prefer

- Scaffold with the standard `dotnet new winui` template first and keep the generated project file, manifests, assets, and startup shape unless the task explicitly requires broader changes.
- Match any comparison scaffold to the app's actual packaging model.
- Keep `App.xaml` minimal while isolating startup problems.
- Prefer explicit `new Window()` and avoid `Window.Current` when customizing WinUI 3 startup.
- Reintroduce shell, resources, bindings, and services incrementally after a clean build and launch.

## Avoid

- Swapping in alternate baseline files or helper scripts as the first recovery move.
- Replacing the template-generated `.csproj` or manifests during initial isolation.
- Flattening all styles into page-local markup as the permanent fix for opaque compiler failures.
- Treating `MSB3073` as proof that the most recently edited XAML line is the only fault.

## Template-First Recovery Loop

1. Confirm the intended packaging model and launch path.
2. If the current startup shape is unclear, scaffold a temporary comparison app with the same packaging choice. Example:
   - `dotnet new winui -n RecoveryReference -o RecoveryReference --use-slnx false --no-solution-file false`
   - Add `--unpackaged true` when the target app is unpackaged.
3. Diff only the startup and shared-resource areas against that comparison scaffold:
   - `App.xaml`
   - `App.xaml.cs`
   - `MainWindow.xaml` / `MainWindow.xaml.cs` or the app's actual shell entry point
   - merged resource dictionaries
   - startup-related project properties
4. Revert the suspect area toward the template-generated shape until the app builds cleanly again.
5. Build explicitly for a concrete architecture. Example:
   - `dotnet build MyApp.sln -c Debug -p:Platform=x64`
6. Launch using the correct packaged or unpackaged path and confirm objective startup signals.
7. Reapply custom changes in small slices, building and running after each meaningful edit.

## Common Recovery Checks

- Confirm `Window.Current` is not used in WinUI 3 startup code.
- Confirm `x:Class`, namespaces, and code-behind names still match.
- Confirm merged resource dictionaries load cleanly before adding more layers.
- Confirm project content items still match any local data or asset files the app expects at runtime.
- Run one clean build if diagnostics appear stale.

## Exit Criteria

- The current app is still rooted in the generated `dotnet new winui` scaffold rather than an alternate baseline shell.
- Build succeeds from the intended local workflow.
- The app launches from the intended local workflow.
- A real top-level window or equivalent expected UI is confirmed.

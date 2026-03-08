---
title: Build, Run, and Launch Verification
priority: CRITICAL
tags: build, run, launch, verification, packaged, unpackaged, debugging
sources:
  - https://learn.microsoft.com/windows/apps/get-started/start-here
  - https://learn.microsoft.com/windows/apps/windows-app-sdk/deploy-packaged-apps
  - https://learn.microsoft.com/windows/apps/windows-app-sdk/deploy-unpackaged-apps
---

## What This Reference Is For

Use this file when the task involves building, running, launch failures, startup crashes, or final verification that a WinUI app actually opens on the current machine.

## Required Workflow

1. Identify the real build target:
   - solution or project file
   - configuration
   - platform
   - packaged or unpackaged model
2. Build after each meaningful code edit and again at task completion.
3. Run the app after changes when feasible. Always do it when the user asked for it or when startup, navigation, resources, or packaging changed.
4. Use the launch path that matches the deployment model:
   - packaged local dev: normally Visual Studio deploy or another package-aware flow
   - unpackaged local dev: normally the built executable the user will actually run
5. Verify real launch with objective evidence such as:
   - non-zero main window handle
   - expected window title
   - responsive process with visible shell
   - no immediate startup exception or crash
6. After completing app work, including a first scaffold or a later build-and-fix cycle, leave a successfully verified final app instance running so the user can see that it worked unless they explicitly asked you not to.
7. If launch fails or verification is ambiguous, debug the failure before saying the app is ready.

## Packaged vs Unpackaged Rules

- Choose one model intentionally before wiring startup, persistence, and launch instructions.
- Packaged apps can rely on package identity and package-backed storage.
- Unpackaged apps must not assume package identity. Guard or replace APIs that require it.
- APIs such as `Windows.Storage.ApplicationData.Current` can fail in unpackaged runs even when the build succeeds.
- Do not mix packaged-only assumptions into an unpackaged startup path.

## Build and Launch Guidance

- Prefer explicit platform targets when WinUI output is sensitive to architecture defaults. If `AnyCPU` creates ambiguity, use `x64` for local verification.
- For unpackaged verification, prefer launching the built `.exe` from `bin\Debug\...\win-x64\` or the project-specific output path.
- After a successful final launch verification, do not immediately tear the app down just because verification succeeded; keep it open for the user unless it blocks the next required action.
- If `dotnet run` throws bootstrapper, deployment, or COM activation errors, treat that as a signal that the chosen launch path or packaging setup is wrong for the current app.
- Stop old app instances before rebuilding if they can lock output files.

## Debugging Startup Failures

- Separate environment problems from app-code startup crashes.
- If the app exits before showing a window, inspect the startup path first:
  - `App.xaml`
  - merged resource dictionaries
  - converters
  - `MainWindow`
  - services used during startup
- For startup or manifest issues, compare the current app against a fresh `dotnet new winui` scaffold for the same packaging model before broader surgery.
- For opaque `MSB3073` and `XamlCompiler.exe` failures, simplify back toward the template-generated startup and shared-resource shape before making further structural changes.
- Restore complex startup pieces incrementally when the failure point is unclear. A minimal `App.xaml` plus minimal `MainWindow` is a valid isolation step.
- If the diagnostics look stale or inconsistent with the current files, run a clean build once before deeper surgery.
- Prefer restoring the last known-good template-based shared-resource state over moving styles inline as the long-term fix.
- When using unpackaged startup, review persistence, notifications, storage, and activation code for hidden package-identity assumptions.

## Exit Criteria

- Build succeeds from the intended local workflow.
- The app launches from the intended local workflow.
- A real top-level window or equivalent expected UI is confirmed.
- No unresolved startup exception remains.

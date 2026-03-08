---
title: Environment Audit and Remediation
priority: CRITICAL
tags: setup, audit, install, dotnet, visual-studio, windows-sdk, developer-mode
sources:
  - https://learn.microsoft.com/windows/apps/get-started/start-here
  - https://learn.microsoft.com/windows/apps/windows-app-sdk/system-requirements
  - https://learn.microsoft.com/windows/apps/get-started/developer-mode-features-and-debugging
  - https://learn.microsoft.com/dotnet/core/install/windows
---

## What This Reference Is For

Use this file for machine-readiness checks, build failures caused by missing tools, and any request to install WinUI prerequisites.

## Required Workflow

1. Use the setup-and-scaffold flow in [../SKILL.md](../SKILL.md) for environment readiness, remediation, and initial verification.
2. If the user asked only for an audit and not for setup, explain that the bundled bootstrap may change the machine and get confirmation before running it.
3. If the user declines machine changes, run a manual non-mutating audit instead and summarize the result under four headings:
   - present
   - missing
   - uncertain
   - recommended optional tools
4. Manual non-mutating audit coverage should focus on:
   - OS version and build floor
   - Developer Mode state when relevant to the task
   - `dotnet --list-sdks`
   - `dotnet new list winui`
   - Visual Studio presence and edition
   - Windows SDK presence
   - MSBuild availability for XAML compilation
5. If prerequisites are still missing after the bundled setup flow, stop and report the blocker clearly instead of inventing alternate install recipes.

## Required vs Optional

Required for normal C# WinUI 3 development:

- Supported Windows build
- Visual Studio with WinUI C# support
- Windows SDK 10.0.19041.0 or later
- MSBuild available for XAML compilation
- .NET SDK 6 or later

Usually optional, but often recommended:

- Developer Mode for local deploy and debug
- WinGet for one-command remediation
- Visual Studio debugging features such as Hot Reload and Live Visual Tree

## Prefer

- The setup-and-scaffold flow in `SKILL.md` over ad hoc manual checks or duplicated setup instructions in this reference.
- A short manual audit only when the user wants a non-mutating readiness check.

## Avoid

- Rewriting or paraphrasing the bundled setup workflow here when `SKILL.md` already covers the user's goal.
- Marking workload detection as present when the bootstrap or manual audit leaves uncertainty.
- Branching into custom per-component install steps unless the user explicitly asks for them.
- Treating Developer Mode as a hard requirement for every task.

## Remediation Strategy

- Missing any required WinUI prerequisite:
  - Use the setup-and-scaffold flow in `SKILL.md` after confirmation when the request is audit-only.
- The bundled setup flow reports a partial failure but the toolchain appears usable:
  - Note the partial failure and continue when the user's task can proceed.
- The bundled setup flow fails and prerequisites still appear to be missing:
  - Use the manual audit checks above for detail if needed, then stop and report the blocker clearly.
- Windows build unsupported:
  - Upgrade Windows first. The WinUI bootstrap command does not replace the OS requirement.
- Developer Mode disabled:
  - Explain whether the current task needs it.
  - If it does, prefer the bundled setup flow or let the user enable it manually.

## Review Checklist

- Was the setup-and-scaffold flow in `SKILL.md` used before advice was given?
- Are missing items clearly separated from uncertain signals?
- Is the remediation plan the minimum needed for the user's goal?
- Was post-install verification handled by the bundled setup flow or by a clearly justified fallback?

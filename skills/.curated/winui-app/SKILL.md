---
name: winui-app
description: Bootstrap, develop, and design modern WinUI 3 desktop applications with C# and the Windows App SDK using official Microsoft guidance, WinUI Gallery patterns, Windows App SDK samples, and CommunityToolkit components. Use when creating a brand new app, preparing a machine for WinUI, reviewing, refactoring, planning, troubleshooting, environment-checking, or setting up WinUI 3 XAML, controls, navigation, windowing, theming, accessibility, responsiveness, performance, deployment, or related Windows app design and development work.
---

# WinUI App

Use this skill for WinUI 3 and Windows App SDK work that needs grounded setup guidance, app bootstrap, modern Windows UX decisions, or concrete implementation patterns.

## Required Flow

1. Classify the task as environment/setup, new-app bootstrap, design, implementation, review, or troubleshooting.
2. If the task is about preparing a machine for WinUI, auditing readiness, or creating a brand new app, start with the bundled setup-and-scaffold flow in this skill before broader design, implementation, or troubleshooting work:
   - Pick the app name when the request is for a new app.
   - Use the exact name the user gave when it is already a safe folder name.
   - If the user did not give a name, derive a short PascalCase name from the request and state what you chose.
   - Create the project in the user's current workspace unless they asked for another location.
   - Do not use `--force` unless the user explicitly asked to overwrite existing files.
   - Run the bundled WinGet configuration from the skill directory so the relative path stays exactly `config.yaml`:

```powershell
winget configure -f config.yaml --accept-configuration-agreements --disable-interactivity
```

   - Treat the configuration as intended to enable Developer Mode, install or update Visual Studio Community 2026, and install the Managed Desktop, Universal, and Windows App SDK C# components needed for WinUI development.
   - Assess the configuration result before continuing. Continue on success. If it fails, inspect the output instead of guessing. If the `winui` template is already available and the toolchain is usable, note the partial failure and continue. If prerequisites are still missing, stop and report the blocker clearly.
   - Verify the template is available before scaffolding:

```powershell
dotnet new list winui
```

   - For diagnostics-only environment requests, explain that the bundled bootstrap may change the machine and get confirmation before running it. If the user declines changes, use the manual verification guidance in `references/foundation-environment-audit-and-remediation.md` and summarize readiness under `present`, `missing`, `uncertain`, and `recommended optional tools`.
   - For a brand new app, scaffold with `dotnet new winui -o <name>`. Add template options only when the user asked for them. Supported options: `-f|--framework net10.0|net9.0|net8.0`, `-slnx|--use-slnx`, `-cpm|--central-pkg-mgmt`, `-mvvm|--use-mvvm`, `-imt|--include-mvvm-toolkit`, `-un|--unpackaged`, `-nsf|--no-solution-file`, `--force`. Do not invent unsupported flags. If the user asks for packaged behavior, pass `--unpackaged false`. Otherwise keep the template default.
   - Verify a new scaffold by confirming the expected project file exists and running `dotnet build` against the generated `.csproj`.
   - Launch a newly scaffolded app through the correct path for its actual packaging model and confirm there is a real top-level window instead of relying only on the launcher process exit code.
3. Read `references/_sections.md`, then load only the reference files that match the task.
4. Make the packaging model explicit before creating or refactoring the app. Default to packaged for Store-like product workflows and Visual Studio deploy/F5 flows. Default to unpackaged when the user expects repeatable CLI build-and-run loops or direct `.exe` launches after each change.
5. When the task is an opaque XAML compiler failure such as `MSB3073` or `XamlCompiler.exe`, read `references/foundation-template-first-recovery.md` and simplify back toward the current `dotnet new winui` scaffold for the chosen packaging model before inventing custom recovery structure.
6. For any work that creates or changes a WinUI app, make a complete but minimal edit set, then build the app and run it before responding to the user. Do this by default even when the user did not explicitly ask for verification. If a running app instance locks the output while more work remains, stop it, rebuild, relaunch, and continue verification. When the work is complete and launch verification succeeds, leave the final verified app instance running for the user unless they explicitly asked you not to.
7. Treat launch verification as incomplete until the app shows objective success signals such as a responsive top-level window, expected window title, or other clear startup behavior. A spawned process by itself is not enough.
8. Prefer Microsoft Learn for requirements, API expectations, and platform guidance.
9. Prefer WinUI Gallery for concrete control usage, shell composition, and design details.
10. Prefer WindowsAppSDK-Samples for scenario-level APIs such as windowing, lifecycle, notifications, deployment, and custom controls.
11. Build toward WinUI and Fluent guidance first. Treat native WinUI shells, controls, interactions, and control chrome as the default implementation path.
12. For grouped command surfaces such as document actions, editor formatting, view toggles, or page-level toolbars, favor a native `CommandBar` or other stock WinUI command surface before building a custom row with `Grid`, `StackPanel`, `Border`, or ad hoc button groupings.
13. Do not invent app-specific controls, bespoke component libraries, or custom chrome to replace stock WinUI behavior unless the user explicitly asks for that customization, the existing product design system already requires it, or a verified platform gap leaves no clean native option.
14. When customization is needed, first compose, template, or restyle built-in WinUI controls and system resources before adding CommunityToolkit dependencies or authoring a new custom control.
15. Use CommunityToolkit only when built-in WinUI controls or helpers do not cover the need cleanly.
16. Support both light and dark mode by default. Treat single-theme output as an exception that requires an explicit user request or an existing product constraint.
17. Use theme-aware resources, system brushes, and WinUI styling hooks instead of hard-coded light-only or dark-only colors when building or revising UI.
18. Make scroll ownership explicit for collection layouts. When a page already scrolls vertically, do not assume a nested `GridView` or other scroll-owning collection will still render a horizontal poster rail correctly.
19. Do not add extra `Border` wrappers around sections, lists, or cards unless the border is doing distinct work that the contained control or parent surface does not already provide. Avoid "double-card" compositions where a section `Border` wraps child items that already render as cards.
20. Treat responsiveness as a shell-plus-page problem, not only a control-resize problem. Plan explicit wide, medium, and phone-width behavior for navigation, padding, content density, and footer/tool regions, and simplify or hide nonessential UI as width shrinks.

## Common Routes

| Request | Read first |
| --- | --- |
| Check whether this PC can build WinUI apps | `references/foundation-environment-audit-and-remediation.md` |
| Install missing WinUI prerequisites | `references/foundation-environment-audit-and-remediation.md` |
| Start a new packaged or unpackaged app | `references/foundation-setup-and-project-selection.md` |
| Recover from opaque XAML compiler or startup failures while staying anchored to the template scaffold | `references/foundation-template-first-recovery.md` |
| Build, run, or verify that a WinUI app actually launched | `references/build-run-and-launch-verification.md` |
| Review app structure, pages, resources, and bindings | `references/foundation-winui-app-structure.md` |
| Choose shell, navigation, title bar, or multi-window patterns | `references/shell-navigation-and-windowing.md` |
| Choose controls or responsive layout patterns | `references/controls-layout-and-adaptive-ui.md` |
| Apply Mica, theming, typography, icons, or Fluent styling | `references/styling-theming-materials-and-icons.md` |
| Improve accessibility, keyboarding, or localization | `references/accessibility-input-and-localization.md` |
| Diagnose responsiveness or UI-thread performance | `references/performance-diagnostics-and-responsiveness.md` |
| Decide whether to use CommunityToolkit | `references/community-toolkit-controls-and-helpers.md` |
| Handle lifecycle, notifications, or deployment | `references/windows-app-sdk-lifecycle-notifications-and-deployment.md` |
| Run a review checklist | `references/testing-debugging-and-review-checklists.md` |

## Environment Rules

- Do not guess whether the machine is ready for WinUI development. Verify it.
- Use the bundled setup-and-scaffold flow in this skill for fresh setup, remediation, and first-project scaffolding instead of delegating to another skill.
- Treat `config.yaml` in this skill directory as the bundled bootstrap source of truth.
- Treat uncertain environment signals as uncertain, not as success.
- If the task is audit-only and the user declines machine changes, use the manual verification guidance in `references/foundation-environment-audit-and-remediation.md` and keep uncertain signals explicit instead of implying success.
- If `config.yaml` is missing, say so clearly and fall back to the official Microsoft workflow instead of pretending the bundled path exists.
- Keep environment readiness, packaging choice, and application startup verification as separate checks. Passing one does not prove the others.
- Fail closed on ambiguous launch results. If the app did not clearly open, keep debugging.
- After creating or editing a WinUI app, do not stop at a successful build. Launch the app, confirm objective startup behavior, and leave the final verified app instance running before returning control to the user unless they explicitly say not to run it.

## Reference Rules

- Keep C# as the primary path. Mention C++ or C++/WinRT only when the difference is material.
- Preserve the conventions of an existing codebase instead of forcing a generic sample structure onto it.
- Treat WinUI design guidance and native controls as the baseline. Do not drift into bespoke component systems or app-specific replacements for standard controls unless the user explicitly requests them or the existing codebase already depends on them.
- Support light and dark mode by default for app UI work unless the user explicitly asks for a single-theme result or the product already enforces one.
- Favor built-in WinUI controls and system styling hooks before adding CommunityToolkit dependencies, custom controls, or app-specific surface systems.
- Put detailed control, theming, shell, scrolling, responsiveness, packaging, and recovery guidance in the matching reference files instead of duplicating those rules here.

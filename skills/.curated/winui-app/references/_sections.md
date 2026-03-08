# Reference Sections

Use this index to choose the narrowest reference file that fits the current task.

## 1. Foundations

- `foundation-setup-and-project-selection.md`
  - Priority: CRITICAL
  - Use for first-project setup, packaged vs unpackaged decisions, and core WinUI prerequisites.
  - Authority: Microsoft Learn WinUI and Windows App SDK setup docs.

- `foundation-environment-audit-and-remediation.md`
  - Priority: CRITICAL
  - Use for machine readiness checks, missing prerequisites, and guided remediation.
  - Authority: Microsoft Learn setup and system requirements docs, plus the bundled bootstrap workflow.

- `foundation-winui-app-structure.md`
  - Priority: HIGH
  - Use for solution layout, shell composition, resources, bindings, and C#-first project structure.
  - Authority: WinUI Gallery source plus Learn XAML guidance.

- `foundation-template-first-recovery.md`
  - Priority: CRITICAL
  - Use for opaque `MSB3073`, `XamlCompiler.exe`, and startup failures that should be recovered by comparing against a fresh `dotnet new winui` scaffold instead of applying alternate baseline files.
  - Authority: Learn packaged and unpackaged deployment guidance plus recurring template-first recovery patterns.

- `build-run-and-launch-verification.md`
  - Priority: CRITICAL
  - Use for build/run workflows, actual launch verification, startup crashes, and packaged-vs-unpackaged local execution choices.
  - Authority: Learn setup and deployment guidance plus recurring WinUI troubleshooting patterns.

## 2. Shell, Navigation, and Windowing

- `shell-navigation-and-windowing.md`
  - Priority: HIGH
  - Use for `NavigationView`, page shells, title bars, `AppWindow`, and multi-window design.
  - Authority: Learn design guidance, WinUI Gallery samples, Windows App SDK Windowing samples.

## 3. Controls, Layout, and Adaptive UI

- `controls-layout-and-adaptive-ui.md`
  - Priority: HIGH
  - Use for control selection, command surfaces, responsive layout, and page composition.
  - Authority: Learn design guidance and WinUI Gallery control pages.

## 4. Styling, Theming, Materials, and Icons

- `styling-theming-materials-and-icons.md`
  - Priority: HIGH
  - Use for Fluent styling, theme resources, Mica, Acrylic, typography, and iconography.
  - Authority: Learn design/material docs, WinUI Gallery backdrop samples, Windows App SDK Mica samples.

- `motion-animations-and-polish.md`
  - Priority: MEDIUM
  - Use for transitions, connected animation, subtle polish, and animation discipline.
  - Authority: Learn motion guidance, WinUI Gallery transition samples, CommunityToolkit animations.

## 5. Accessibility, Input, and Localization

- `accessibility-input-and-localization.md`
  - Priority: HIGH
  - Use for keyboarding, Narrator, high contrast, automation properties, and localization concerns.
  - Authority: Learn accessibility and globalization guidance, WinUI Gallery automation patterns.

## 6. Performance and Diagnostics

- `performance-diagnostics-and-responsiveness.md`
  - Priority: HIGH
  - Use for UI-thread responsiveness, large item collections, rendering cost, and diagnostic tooling.
  - Authority: Learn WinUI performance docs and XAML frame analysis guidance.

## 7. Windows App SDK Scenarios

- `windows-app-sdk-lifecycle-notifications-and-deployment.md`
  - Priority: HIGH
  - Use for lifecycle, activation, notifications, packaged vs unpackaged deployment, and runtime initialization.
  - Authority: Microsoft Learn Windows App SDK docs and WindowsAppSDK-Samples.

## 8. CommunityToolkit Extensions

- `community-toolkit-controls-and-helpers.md`
  - Priority: MEDIUM
  - Use when built-in WinUI controls are not enough and Toolkit packages might close the gap cleanly.
  - Authority: CommunityToolkit/Windows packages and samples.

## 9. Testing, Debugging, and Review

- `testing-debugging-and-review-checklists.md`
  - Priority: HIGH
  - Use for final review passes, debugging workflows, and validation checklists.
  - Authority: Learn tooling docs plus recurring WinUI review patterns.

- `sample-source-map.md`
  - Priority: MEDIUM
  - Use when you need to know which canonical repo or doc to inspect first for a given task.
  - Authority: Curated map across Learn, WinUI Gallery, WindowsAppSDK-Samples, and CommunityToolkit.

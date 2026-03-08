---
title: Testing, Debugging, and Review Checklists
priority: HIGH
tags: testing, debugging, review, hot-reload, live-visual-tree, checklists
sources:
  - https://learn.microsoft.com/windows/apps/get-started/start-here
  - https://learn.microsoft.com/windows/apps/get-started/developer-mode-features-and-debugging
  - https://learn.microsoft.com/windows/apps/performance/winui-perf
---

## What This Reference Is For

Use this file for final review passes, debugging sessions, and "what should I verify before I call this done?" prompts.

## Required Verification Loop

- Build after each meaningful edit, not only at the end.
- Run the app after changes when the user asked for it or when startup-sensitive files changed.
- Verify actual launch instead of assuming success from a spawned process.
- If the app fails before showing a window, debug the startup path before continuing feature work.

## Design Review Checklist

- Shell and navigation are simple and predictable.
- `NavigationView` still reads like standard WinUI shell chrome unless the product explicitly calls for branded pane content or custom shell composition.
- Layout stays usable when the window is narrow.
- Layout has been checked at more than one breakpoint, including a genuinely phone-like width when the app can be resized that far.
- Collection pages with mixed scroll regions have been checked at runtime so shelves still render in the intended direction and do not collapse into a single vertical column.
- Theme, contrast, hierarchy, and interactive state visibility hold up in both light and dark mode, and typography and iconography still feel native to Windows.
- Command placement and hierarchy are clear.
- Default WinUI surfaces and control templates carry most of the layout instead of a custom border/card system.
- Search and filter workflows avoid redundant controls when live local filtering would be clearer.
- At narrow and phone widths, nonessential controls are simplified, hidden, or moved behind shell affordances instead of merely compressed.

## Code Review Checklist

- App structure is coherent and scalable.
- Resource dictionaries and styles are centralized where they should be.
- Platform controls are preferred over unnecessary custom control work.
- New dependencies are justified.
- The packaging model matches the startup, storage, and launch code.
- The app builds cleanly from the workflow the user will actually use.

## Accessibility Checklist

- Keyboard-only flow works end to end.
- Focus states are visible and sensible.
- Automation properties are present where needed.
- High contrast and text scaling do not break the UI.

## Performance Checklist

- No obvious UI-thread blocking work in interactive paths.
- Large collections use an appropriate control and layout.
- Scroll ownership is intentional for collection-heavy pages; nested `GridView` plus outer `ScrollViewer` combinations have been justified or replaced.
- Expensive styling or template choices are justified.
- Profiling data exists for non-obvious performance claims.

## Debugging Tools

- Use Hot Reload for fast visual iteration.
- Use Live Visual Tree and Live Property Explorer for layout and property debugging.
- Use WPR and WPA when diagnosing frame or responsiveness issues.
- Reproduce resize, theme, and input-mode changes before concluding the issue is fixed.
- When resize behavior is part of the task, verify wide, medium, and phone-width states against the running app rather than trusting the XAML structure alone.
- When a collection page looks wrong, inspect the live tree for nested `ScrollViewer` ownership before rewriting the item template; the bug may be layout ownership rather than card markup.
- Use startup exception details, debugger output, or Event Viewer when the process dies before any window appears.

## Exit Criteria

- The build succeeds from the intended local workflow.
- The feature works on the intended machine configuration.
- The app launches and shows the expected shell or window.
- The app remains usable in light, dark, and high contrast.
- Primary flows are keyboard-accessible.
- Resize behavior, startup, and interactive responsiveness have been checked.
- If the window can become phone-width, the shell and content have been verified there too.

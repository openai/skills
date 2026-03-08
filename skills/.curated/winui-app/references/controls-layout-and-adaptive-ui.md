---
title: Controls, Layout, and Adaptive UI
priority: HIGH
tags: controls, layout, adaptive-ui, responsive, forms, lists
sources:
  - https://learn.microsoft.com/windows/apps/design/layout/responsive-design
  - https://learn.microsoft.com/windows/apps/design/basics/navigation-basics
  - https://github.com/microsoft/WinUI-Gallery
---

## What This Reference Is For

Use this file when choosing controls, composing pages, or making a WinUI layout adapt well to different window sizes and input modes.

## Prefer

- Built-in WinUI controls first.
- Native command surfaces such as `CommandBar` when the UI is grouping actions, toggles, and lightweight tool controls.
- Standard controls for common tasks: `TextBox`, `NumberBox`, `ComboBox`, `ListView`, `GridView`, `ContentDialog`, `InfoBar`, `TeachingTip`, `TabView`, `NavigationView`.
- Explicit scroll ownership for collection layouts. If the page already scrolls vertically, prefer giving a media shelf its own horizontal `ScrollViewer` and a simple horizontal panel.
- Responsive techniques such as reposition, resize, reflow, and show/hide.
- Layouts that remain usable when the window becomes narrow.
- A real phone-width plan when the app may be resized that far: fewer columns, reduced padding, simplified controls, and stacked content instead of compressed desktop rails.

## Avoid

- Replacing standard WinUI controls with custom controls just to change appearance.
- Building custom toolbar rows out of generic layout panels when a stock `CommandBar` would cover the grouping cleanly.
- Hard-coded sizes that only look correct at one window width.
- Dense desktop-only layouts that break touch or keyboard workflows.
- Adding extra controls for local filtering or sorting when live updates and a simpler layout would better match the workflow.
- Nesting a scroll-owning `GridView` inside an outer page `ScrollViewer` without deciding which control owns scrolling; this often produces a single vertical column or awkward scroll conflicts instead of a horizontal media shelf.
- Wrapping list sections or card groups in an extra `Border` when the section header, spacing, and child surfaces already establish grouping.

## Control Selection Guidance

- Forms and settings:
  - Prefer native controls first; add Toolkit settings controls only if the experience clearly benefits.
- Command surfaces:
  - Prefer `CommandBar` for grouped document, formatting, view, and page-level actions before composing a custom bar from `Grid`, `StackPanel`, `Border`, and loose buttons.
  - Prefer the `CommandBar` overflow model for secondary actions before splitting the command surface into multiple custom rows.
  - Fall back to a custom command layout only when a verified `CommandBar` limitation, an explicit product design requirement, or unusual content composition makes the native surface a poor fit.
- Large collections:
  - Prefer controls with virtualization-friendly behavior.
  - Use `GridView` when it owns the collection surface and its scrolling behavior is part of the intended experience.
  - For poster rails or other horizontal shelves inside a vertically scrolling page, prefer a horizontal `ScrollViewer` containing an `ItemsControl` or `ItemsRepeater` with a horizontal panel instead of a nested `GridView`.
  - Consider `ItemsRepeater` when the layout is custom and performance matters.
- Search and filtering:
  - Prefer a single search field with live updates for local or otherwise inexpensive filtering.
  - Add explicit apply, refresh, or mode-selection controls only when the underlying operation is expensive, remote, asynchronous, or semantically different.
- Dialogs and transient guidance:
  - Use `ContentDialog` for modal decisions.
  - Use `InfoBar` for persistent status.
  - Use `TeachingTip` for contextual onboarding.

## Adaptive Layout Guidance

- Design with effective pixels, not fixed device assumptions.
- Make the smallest supported layout fully usable.
- Add density or multi-column views only when width allows.
- Use visual states, adaptive triggers, or layout state changes intentionally.
- Keep commands and primary content reachable after resize.
- Verify collection orientation and scrolling behavior at runtime. A shelf that looks horizontal in XAML can still render as a vertical stack once nested scroll regions are involved.
- When simplifying a dense section, remove redundant outer surfaces before adding more adaptive layout rules; fewer layers usually adapt more cleanly across breakpoints.
- Define breakpoint intent explicitly. Typical questions: when does a shelf become a stacked list, when does a footer drop nonessential controls, and when does the page stop behaving like a desktop canvas and become a single-column phone layout?
- Simplify as width shrinks. Prefer dropping secondary controls or moving them behind shell affordances over preserving every control at every breakpoint.
- When a page contains desktop-oriented horizontal shelves, add a phone-width alternative that stacks items vertically instead of relying on clipped rails and horizontal scrolling everywhere.

## WinUI Gallery Anchors

- Control pages for built-in WinUI control usage
- Gallery home and shell pages for adaptive layout ideas
- Sample pages for title bar and system backdrop interactions with content layout

## Review Checklist

- Did you choose the simplest built-in control that fits?
- Are search and filter controls no more complex than the data flow requires?
- Does the page remain usable when narrow?
- Can keyboard, mouse, and touch all reach the same core actions?
- Are spacing and hierarchy consistent across breakpoints?
- If the page mixes page scrolling with collection scrolling, is it obvious which control owns vertical scrolling and which one, if any, owns horizontal shelf scrolling?
- Are section containers doing real layout or surface work, or are some outer borders now redundant?
- At phone width, does the page read as a coherent single-column flow instead of a squeezed desktop layout?

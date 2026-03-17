---
title: Accessibility, Input, and Localization
priority: HIGH
tags: accessibility, keyboard, narrator, automation, localization, high-contrast
sources:
  - https://learn.microsoft.com/windows/apps/design/accessibility/accessibility
  - https://learn.microsoft.com/windows/apps/design/accessibility/keyboard-accessibility
  - https://learn.microsoft.com/windows/apps/design/accessibility/high-contrast-themes
  - https://learn.microsoft.com/windows/apps/design/globalizing/globalizing-portal
  - https://github.com/microsoft/WinUI-Gallery
---

## What This Reference Is For

Use this file for keyboard accessibility, Narrator support, automation properties, input parity, high contrast, and localization-ready UI.

## Prefer

- Accessible names, help text, and landmarks for meaningful UI elements.
- Full keyboard reachability for the main workflow.
- High-contrast-safe visuals.
- Localizable strings and layouts that tolerate growth.
- Equal support for mouse, touch, pen, and keyboard where the platform expects it.

## Avoid

- Icon-only interactions without accessible naming.
- Focus traps, hidden tab stops, or keyboard-only dead ends.
- Hard-coded strings in XAML or code-behind that block localization.
- Text layouts that collapse when strings expand.

## Guidance

- Use automation properties intentionally.
- Preserve visible focus and logical tab order.
- Verify context menus, flyouts, and dialogs by keyboard as well as mouse.
- Respect text scaling, contrast changes, and RTL where relevant.
- Keep touch targets and spacing usable on both mouse and touch hardware.

## WinUI Gallery Anchors

- Accessibility-related control samples
- Automation helper patterns in shell code
- Standard WinUI controls that already expose useful accessibility behavior

## Review Checklist

- Can a keyboard-only user complete the task?
- Does Narrator have enough information to describe the important UI?
- Does the experience stay legible in high contrast?
- Are strings and layout ready for localization and RTL growth?

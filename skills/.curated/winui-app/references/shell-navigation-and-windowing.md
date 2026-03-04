---
title: Shell, Navigation, and Windowing
priority: HIGH
tags: navigationview, titlebar, appwindow, multi-window, shell
sources:
  - https://learn.microsoft.com/windows/apps/design/basics/navigation-basics
  - https://learn.microsoft.com/windows/apps/design/basics/titlebar-design
  - https://github.com/microsoft/WinUI-Gallery
  - https://github.com/microsoft/WindowsAppSDK-Samples/tree/main/Samples/Windowing
---

## What This Reference Is For

Use this file for top-level app shells, page navigation models, custom title bars, and multi-window decisions.

## Prefer

- `NavigationView` for standard desktop shells with clear top-level destinations.
- A small, stable set of primary destinations.
- Built-in back navigation behavior that matches user expectations.
- `AppWindow` and Windows App SDK windowing APIs for modern window management.

## Avoid

- Overloading the nav surface with every command and secondary action.
- Turning the `NavigationView` pane into a branded hero area when the user did not ask for custom shell treatment.
- Custom title bar layouts that break drag regions or caption button clarity.
- Multi-window designs unless the workflow clearly benefits from them.

## Navigation Guidance

- Use left navigation when the app has several stable, high-level destinations.
- Use top navigation when there are few peer destinations and width is available.
- Use a single-page or document-first layout when navigation is shallow and the user mostly stays in one workflow.
- Keep naming and iconography stable across pages.
- Treat `NavigationView` as functional shell chrome first. Keep pane headers, footer content, and decorative branding minimal unless the product requirements clearly call for them.
- Prefer the platform's normal pane structure before adding custom logo blocks, taglines, or non-navigation content that changes the shell's native feel.
- For narrow or phone-like widths, stop reserving permanent pane width for desktop navigation. Prefer a minimal or overlay navigation mode, show the pane toggle when needed, close the pane by default after navigation, and give content the width back.
- When a shell enters a phone-width mode, reduce content padding and decorative chrome so the page reads as one primary column instead of a desktop shell with a squeezed content strip.

## Title Bar Guidance

- Treat the title bar as functional chrome first, branding surface second.
- Keep empty non-interactive areas draggable.
- Blend title bar visuals with the rest of the app when possible.
- Respect light, dark, and high-contrast states.

## Windowing Guidance

- Start with one main window.
- Add secondary windows only for workflows such as document detachment, inspection panes, or tool windows.
- Use Windows App SDK samples for resizing, placement, and window-specific behaviors instead of inventing custom platform abstractions.

## Sample and Source Anchors

- WinUI Gallery `NavigationView`, `TitleBar`, `AppWindow`, and windowing sample pages
- WindowsAppSDK-Samples `Samples/Windowing`
- Learn navigation and title bar guidance

## Review Checklist

- Is the navigation model simple and intentional?
- Does the shell still look and behave like a normal WinUI `NavigationView` unless there is an explicit reason to diverge?
- Does the title bar still behave like a Windows title bar?
- Are back, search, and pane behaviors consistent?
- Is multi-window use justified by the workflow?
- Does the shell intentionally switch behavior at narrow or phone widths instead of leaving a full desktop pane open?

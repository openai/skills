---
title: Performance, Diagnostics, and Responsiveness
priority: HIGH
tags: performance, responsiveness, ui-thread, wpr, wpa, diagnostics
sources:
  - https://learn.microsoft.com/windows/apps/performance/winui-perf
  - https://github.com/microsoft/WinUI-Gallery
---

## What This Reference Is For

Use this file when the user reports sluggish WinUI behavior, dropped frames, long startup, or laggy scrolling and layout.

## Prefer

- Keeping the UI thread free for layout, rendering, and input.
- Simpler visual trees and lighter templates.
- Virtualization-friendly controls and item layouts.
- Measurement before optimization when the issue is not obvious.

## Avoid

- Doing expensive I/O or CPU work directly on the UI thread.
- Deeply nested XAML trees without a concrete benefit.
- Re-templating controls in ways that dramatically increase layout work.
- Guessing at performance causes without profiling.

## Guidance

- Favor platform controls and layouts that virtualize well for long lists.
- Defer or background heavy work when it does not need to block interaction.
- Reduce unnecessary layout invalidation and repeated measure/arrange churn.
- Use WPR and WPA with the XAML Frame Analysis plugin for frame-level investigations.
- Treat slow-frame findings as a clue to UI-thread overload, not as a reason to micro-optimize blindly.

## Sample and Source Anchors

- Learn `winui-perf.md`
- WinUI Gallery pages that demonstrate adaptive UI and complex controls without excessive custom infrastructure

## Review Checklist

- Is heavy work running off the UI thread where possible?
- Are large collections using an appropriate items control?
- Is the visual tree no more complex than it needs to be?
- Has profiling been used before claiming a fix?

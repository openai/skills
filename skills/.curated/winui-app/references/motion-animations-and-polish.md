---
title: Motion, Animations, and Polish
priority: MEDIUM
tags: motion, animations, transitions, connected-animation, polish
sources:
  - https://learn.microsoft.com/windows/apps/design/motion/
  - https://github.com/microsoft/WinUI-Gallery
  - https://github.com/CommunityToolkit/Windows
---

## What This Reference Is For

Use this file when adding polish to a WinUI app through motion, transitions, and subtle animated state changes.

## Prefer

- Motion that clarifies hierarchy, continuity, and state changes.
- Theme transitions, connected animations, and built-in platform behaviors before custom animation systems.
- Short, purposeful animations that support the task.

## Avoid

- Decorative animation that delays interaction.
- Multiple overlapping animations for the same state change.
- Animation that hides focus, selection, or accessibility state.

## Guidance

- Use transitions to explain where content came from and where it went.
- Keep entrance and exit motion subtle.
- Use connected animation when there is a real source-to-destination relationship.
- Reach for CommunityToolkit animation helpers only when built-in transitions are not enough.

## Sample and Source Anchors

- WinUI Gallery animation, transition, and implicit animation pages
- Learn motion guidance
- CommunityToolkit animations package and samples

## Review Checklist

- Does the motion improve clarity?
- Is the app still responsive while the animation runs?
- Can the transition be simplified to a built-in WinUI behavior?
- Does the motion preserve accessibility and input clarity?

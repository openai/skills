---
title: CommunityToolkit Controls and Helpers
priority: MEDIUM
tags: communitytoolkit, controls, helpers, animations, settingscontrols
sources:
  - https://github.com/CommunityToolkit/Windows
  - https://learn.microsoft.com/dotnet/communitytoolkit/windows/getting-started
---

## What This Reference Is For

Use this file when deciding whether the Windows Community Toolkit should be added to a WinUI 3 app.

## Prefer

- Platform controls first.
- Targeted Toolkit package additions for clear gaps such as richer settings surfaces, segmented controls, or focused animation helpers.
- The smallest package set that solves the problem.

## Avoid

- Adding Toolkit packages because they look convenient without checking whether WinUI already covers the need.
- Pulling in multiple Toolkit packages for a minor visual difference.
- Hiding fundamental UX problems behind a new dependency.

## Good Candidate Areas

- `SettingsControls`
  - useful for settings surfaces and cards
- `Segmented`
  - useful when segmented selection is clearer than a tab or radio cluster
- `HeaderedControls`
  - useful for labeled control groupings
- `Animations`
  - useful when built-in transitions are not enough
- helpers and extensions
  - useful when they reduce repetitive WinUI plumbing cleanly

## Package Guidance

- Prefer WinUI 3 compatible Toolkit packages.
- Add only what the app will actually use.
- Document why a Toolkit dependency was added and what built-in alternative was rejected.

## Sample and Source Anchors

- CommunityToolkit `components/SettingsControls`
- CommunityToolkit `components/Segmented`
- CommunityToolkit `components/HeaderedControls`
- Toolkit animations and helper packages

## Review Checklist

- Does built-in WinUI already solve the problem?
- Is the dependency narrowly scoped and justified?
- Does the new control match the rest of the app’s design language?
- Will the package meaningfully reduce custom code or improve UX?

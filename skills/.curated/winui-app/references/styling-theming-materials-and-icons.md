---
title: Styling, Theming, Materials, and Icons
priority: HIGH
tags: styling, theme-resources, mica, acrylic, typography, icons
sources:
  - https://learn.microsoft.com/windows/apps/design/style/mica
  - https://learn.microsoft.com/windows/apps/design/style/acrylic
  - https://learn.microsoft.com/windows/apps/design/signature-experiences/typography
  - https://learn.microsoft.com/windows/apps/design/signature-experiences/iconography
  - https://github.com/microsoft/WinUI-Gallery
  - https://github.com/microsoft/WindowsAppSDK-Samples/tree/main/Samples/Mica
---

## What This Reference Is For

Use this file for Fluent styling choices, theme resources, Mica or Acrylic usage, custom title bar visuals, typography, and iconography.

## Prefer

- Theme resources and system brushes over hard-coded colors.
- Standard WinUI surface resources and default control chrome before custom panel systems.
- Mica on long-lived surfaces such as the main window background or title bar region.
- Acrylic on transient or light-dismiss surfaces.
- Segoe UI Variable or platform-default typography choices.
- Fluent iconography that matches the platform language.
- When metadata needs a visual container, prefer small rounded rectangles or subtle badges over bright oval pills.

## Avoid

- Hard-coded light-theme colors that break dark or high-contrast themes.
- Wrapping every region in a custom `Border` with a bespoke corner radius, stroke, and fill when standard WinUI surfaces would do the job.
- Adding an outer section `Border` around content that is already visually grouped by card controls, spacing, or headers; this often creates a redundant "card around cards" effect.
- Using Acrylic where Mica or a simple theme-aware surface would be cheaper and clearer.
- Mixing unrelated icon styles.
- Filling lists or cards with rows of decorative oval chips for routine metadata. Use tag treatments sparingly, and default to rounded rectangles when they are justified.

## Theming Guidance

- Support light, dark, and high-contrast by default.
- Centralize brushes, typography, and corner/spacing decisions in shared resource dictionaries.
- Let built-in controls keep their platform behavior unless there is a strong design reason to customize them.
- When a grouped surface is needed, prefer system resources such as `CardBackgroundFillColorDefaultBrush`, `CardStrokeColorDefaultBrush`, and `LayerFillColorDefaultBrush` instead of inventing a parallel surface language.
- If child content already uses card-like surfaces, prefer removing the outer section border and relying on layout spacing and typography for grouping unless the section needs its own distinct background, inset, or stroke.

## Materials Guidance

- Use Mica for long-lived base layers.
- Use Acrylic for transient surfaces such as flyouts and menus.
- Verify fallback behavior on older Windows versions or unsupported scenarios.

## Icon and Typography Guidance

- Use standard Windows iconography and keep visual weight consistent.
- Use typography to create hierarchy instead of adding extra borders or decoration.
- Keep title bar text and document titles aligned with Windows guidance.

## Sample and Source Anchors

- Learn material, typography, and iconography guidance
- WinUI Gallery system backdrop and styling pages
- WindowsAppSDK-Samples `Samples/Mica`

## Review Checklist

- Are colors and brushes theme-aware?
- Does the app look correct in light, dark, and high contrast?
- Is the selected material appropriate for the surface lifetime?
- Are icon and typography choices consistent with Fluent design?
- Are standard WinUI surfaces doing most of the visual work, with custom borders limited to clearly justified cases?
- Are there any redundant outer borders that could be removed without losing hierarchy or usability?
- Are tag or chip treatments sparse, visually quiet, and not rendered as default oval pills unless the product explicitly calls for that style?

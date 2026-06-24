---
name: theme-factory
description: Apply consistent visual themes (colors + fonts) to artifacts like slides, docs, reports, and HTML pages. Use when a user asks to style, brand, or standardize the look-and-feel of an artifact or when you need a cohesive theme across outputs.
---

# Theme Factory

Apply a cohesive visual theme to an artifact.

## Workflow

1) Show the theme showcase
- Open `theme-showcase.pdf` so the user can see all available themes.
- Do not edit the PDF.

2) Ask for a theme choice
- Ask which theme to apply.
- Wait for explicit confirmation.

3) Apply the selected theme
- Read the corresponding file from `themes/` for exact colors and font pairings.
- Apply the specified colors and fonts consistently across the artifact.
- Preserve contrast and readability.

## Themes Available

The following 10 themes are available and are showcased in `theme-showcase.pdf`:
- Ocean Depths
- Sunset Boulevard
- Forest Canopy
- Modern Minimalist
- Golden Hour
- Arctic Frost
- Desert Rose
- Tech Innovation
- Botanical Garden
- Midnight Galaxy

## Custom Theme (if none fit)

If no theme fits, create a new theme using the same structure as the existing files in `themes/`:
- Provide a cohesive color palette (hex)
- Provide complementary header/body font pairings
- Give the theme a clear, descriptive name

After generating a custom theme, show it to the user for approval, then apply it.

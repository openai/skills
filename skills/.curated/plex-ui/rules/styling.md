# Styling Rules

## Three-Layer Token System

Plex UI uses a three-layer design token architecture:

```
Primitive tokens  ->  Semantic tokens  ->  Component CSS custom properties
(raw values)          (contextual)          (per-component)
```

All tokens are CSS custom properties. Light and dark mode are handled via the CSS `light-dark()` function — no `dark:` prefix needed.

## Size Scale (9 steps)

All key controls share a unified height scale via the `size` prop:

```
3xs(22px) - 2xs(24px) - xs(26px) - sm(28px) - md(32px) - lg(36px) - xl(40px) - 2xl(44px) - 3xl(48px)
```

The `size` prop automatically adjusts height, padding, font size, icon size, and border radius. **Never manually set these with className when a `size` prop exists.**

```tsx
// Correct
<Button size="lg" color="primary">Submit</Button>

// Wrong — manual sizing defeats the token system
<Button className="h-9 px-4 text-sm" color="primary">Submit</Button>
```

### Size Guidelines

| Context | Recommended Size |
|---------|-----------------|
| Dense data tables | `3xs` – `xs` |
| Compact toolbars | `2xs` – `sm` |
| Standard forms | `md` (default) |
| Prominent actions | `lg` |
| Hero/marketing CTA | `xl` – `3xl` |
| Touch targets (mobile) | `lg` – `2xl` |

## Semantic Colors

### Component `color` prop

Available values: `primary`, `secondary`, `danger`, `success`, `warning`, `caution`, `discovery`, `info`

```tsx
<Button color="primary">Save</Button>
<Button color="danger" variant="ghost">Delete</Button>
<Alert color="success" title="Saved!" />
<Badge color="warning">Beta</Badge>
```

### Tailwind utility classes (from Plex UI tokens)

Plex UI ships semantic Tailwind utilities. Use these instead of raw Tailwind colors:

```css
/* Text */
text-primary          /* Main text */
text-secondary        /* Supporting text */
text-tertiary         /* Muted text */
text-disabled         /* Disabled text */

/* Backgrounds */
bg-surface            /* Primary surface */
bg-surface-secondary  /* Secondary surface */
bg-surface-tertiary   /* Tertiary surface */

/* Borders */
border-default        /* Standard border */
border-subtle         /* Subtle border */
```

```tsx
// Correct — semantic tokens
<div className="bg-surface text-primary border border-default rounded-lg p-4">
  <p className="text-secondary">Description text</p>
</div>

// Wrong — raw Tailwind colors (breaks theming, ignores dark mode)
<div className="bg-white text-gray-900 border border-gray-200 rounded-lg p-4">
  <p className="text-gray-500">Description text</p>
</div>
```

## Variants

Most components support a `variant` prop:

| Variant | Usage |
|---------|-------|
| `solid` | Primary actions, high emphasis (default for Button) |
| `soft` | Secondary actions, medium emphasis |
| `outline` | Tertiary actions, low emphasis, visible borders |
| `ghost` | Minimal emphasis, no background until hover |
| `surface` | Card-like appearance with subtle background |

```tsx
<Button color="primary" variant="solid">Primary action</Button>
<Button color="primary" variant="soft">Secondary</Button>
<Button color="primary" variant="outline">Tertiary</Button>
<Button color="primary" variant="ghost">Minimal</Button>
```

## Dark Mode

Plex UI uses CSS `light-dark()` — dark mode works automatically with no extra code.

### Toggle theme:

```css
:root { color-scheme: light; }       /* Force light */
:root { color-scheme: dark; }        /* Force dark */
:root { color-scheme: light dark; }  /* Follow OS preference */
```

### In React:

```tsx
// Toggle via style attribute
<html style={{ colorScheme: isDark ? "dark" : "light" }}>

// Or via CSS class
document.documentElement.style.colorScheme = "dark";
```

### Rules:

- **Never use `dark:` prefix** for Plex UI tokens — they switch automatically
- **Never override component colors** with raw Tailwind dark mode classes
- All semantic colors (`text-primary`, `bg-surface`, etc.) adapt to theme automatically

## Spacing & Layout

Use Tailwind's spacing utilities alongside Plex UI components:

```tsx
// Correct — flex + gap
<div className="flex flex-col gap-4">
  <Input size="md" />
  <Button size="md" color="primary">Submit</Button>
</div>

// Correct — className for layout, props for styling
<Button color="primary" size="md" className="mt-4 w-full">
  Full width button with top margin
</Button>
```

### className Guidelines:

- **Use `className` for:** margins, width, flex, grid, positioning — layout concerns
- **Do NOT use `className` for:** colors, font sizes, padding, border radius — use props instead
- **Use `block` prop** for full-width buttons instead of `className="w-full"`

```tsx
// Correct
<Button color="primary" block>Full width</Button>

// Avoid
<Button color="primary" className="w-full">Full width</Button>
```

## CSS Custom Properties

For advanced theming, Plex UI exposes CSS custom properties at three levels:

```css
/* Primitive — raw color values */
--color-gray-50: ...;
--color-gray-900: ...;

/* Semantic — contextual meaning */
--color-text-primary: ...;
--color-surface: ...;
--color-border-default: ...;

/* Component — per-component tokens */
--button-height: ...;
--input-border-color: ...;
```

Override semantic tokens in your CSS to customize the entire theme:

```css
:root {
  --color-primary: oklch(0.65 0.24 265);
  --color-surface: oklch(0.99 0 0);
}
```

## Common Mistakes

| Mistake | Correct approach |
|---------|-----------------|
| `className="bg-blue-500 text-white"` | `color="primary" variant="solid"` |
| `className="h-10 px-4"` | `size="lg"` |
| `dark:bg-gray-800` | Use semantic tokens (auto-switch) |
| `className="text-gray-500"` | `className="text-secondary"` |
| Manual border radius on controls | Use `size` prop (includes radius) |
| `style={{ fontSize: 14 }}` | Use `size` prop or Tailwind class |

---
name: plex-ui
description: Manages Plex UI components and projects — installing, composing, styling, and debugging UI. Provides component APIs, design token conventions, and usage patterns. Applies when working with @plexui/ui, Plex UI components, or any project importing from @plexui/ui. Also triggers for Plex UI setup, theming, dark mode, responsive design, or icon usage.
---

# Plex UI

A production-grade React component library with 35+ components, 14 hooks, a three-layer design token system, and a unified 9-step size scale — powered by Radix primitives and Tailwind CSS 4.

> **IMPORTANT:** All components are imported from `@plexui/ui/components/<Name>`. Hooks from `@plexui/ui/hooks/<name>`. Never import from the package root.

## Installation & Setup

```bash
npm install @plexui/ui
```

### Global stylesheet (e.g. `main.css` or `globals.css`):

```css
@import "tailwindcss";
@import "@plexui/ui/css";
@source "../node_modules/@plexui/ui";
```

### Import the stylesheet before rendering (e.g. `main.tsx` or `layout.tsx`):

```tsx
import "./main.css";
```

### Wrap your app in PlexUIProvider:

```tsx
import { PlexUIProvider } from "@plexui/ui/components/PlexUIProvider";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <PlexUIProvider linkComponent="a">
      {children}
    </PlexUIProvider>
  );
}
```

> **Next.js:** Pass `linkComponent={Link}` from `next/link` for client-side routing.

## Principles

1. **Use existing components first.** Check the component list below before writing custom markup.
2. **Use the unified size scale.** All controls share the same `size` prop with 9 steps — use it consistently.
3. **Use semantic colors.** `color="primary"`, `text-primary`, `bg-surface` — never raw Tailwind colors like `bg-blue-500`.
4. **Use CSS variable tokens.** The three-layer token system handles light/dark automatically via `light-dark()`.
5. **Compose, don't reinvent.** Dashboard = Sidebar + Menu + Tabs + components. Form = Field + Input + Select + Button.

## Critical Rules

These rules are **always enforced**. Each links to a detailed reference file.

### Imports & Structure -> [components.md](./rules/components.md)

- **Always import from subpaths.** `import { Button } from "@plexui/ui/components/Button"` — never from root.
- **Wrap app in PlexUIProvider.** Required for link routing and shared context.
- **Use `"use client"` when needed.** Components with state, effects, or event handlers need the directive in Next.js App Router.

### Styling & Tokens -> [styling.md](./rules/styling.md)

- **Use semantic color props.** `color="primary"`, `color="danger"` — not Tailwind color classes.
- **Use the `variant` prop.** `variant="solid"`, `"soft"`, `"outline"`, `"ghost"`, `"surface"`.
- **Use the `size` prop.** 9-step scale from `3xs` to `3xl`. Default is `md`.
- **Dark mode is automatic.** Uses CSS `light-dark()`. Set `color-scheme: dark` on `:root` — no `dark:` prefix needed.
- **Use Plex UI utility classes.** `text-primary`, `text-secondary`, `bg-surface`, `border-default` — not raw colors.

### Icons -> [icons.md](./rules/icons.md)

- **Import icons from `@plexui/ui/components/Icon`.** Named exports like `IconSearch`, `IconCheck`, etc.
- **Icons auto-size inside components.** No manual `w-4 h-4` needed — components handle icon sizing via the `size` prop.
- **Use `iconSize` prop to override.** When the default icon size doesn't fit, use `iconSize="sm"` etc.

## Component Reference

All components use subpath imports: `import { X } from "@plexui/ui/components/X"`

### Controls (unified size scale)

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Button` | `color`, `variant`, `size`, `pill`, `block`, `disabled` | Primary action element |
| `ButtonLink` | Same as Button + `href` | Button that renders as a link |
| `Input` | `size`, `placeholder`, `disabled`, `invalid` | Text input field |
| `Textarea` | `size`, `autoGrow`, `minRows`, `maxRows` | Multi-line text input |
| `FloatingLabelInput` | `label`, `size` | Input with animated floating label |
| `Select` | `size`, `placeholder`, `value`, `onChange` | Dropdown select |
| `SelectControl` | `size`, `value`, `options` | Simplified select with options array |
| `Checkbox` | `size`, `checked`, `onChange`, `indeterminate` | Checkbox control |
| `RadioGroup` | `size`, `value`, `onChange` | Radio button group |
| `Switch` | `size`, `checked`, `onChange` | Toggle switch |
| `SegmentedControl` | `size`, `value`, `onChange`, `options` | Tab-like option selector |
| `Slider` | `size`, `min`, `max`, `value`, `onChange` | Range slider |
| `TagInput` | `size`, `value`, `onChange` | Multi-value tag input |
| `OTPInput` | `size`, `length`, `value`, `onChange` | One-time password input |
| `DatePicker` | `size`, `value`, `onChange` | Date selection |
| `DateRangePicker` | `size`, `startDate`, `endDate`, `onChange` | Date range selection |

### Display

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Badge` | `color`, `variant`, `size` | Status indicator label |
| `Avatar` | `src`, `name`, `size` | User avatar with fallback |
| `AvatarGroup` | `max`, `size` | Stacked avatar group |
| `Indicator` | — | Loading indicators (LoadingIndicator, LoadingDots, CircularProgress) |
| `Skeleton` | `width`, `height`, `circle` | Loading placeholder |
| `EmptyMessage` | `title`, `description`, `icon` | Empty state component |
| `StatCard` | `title`, `value`, `trend` | Statistics display card |
| `ShimmerText` | `children` | Animated shimmer text effect |

### Navigation & Layout

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Sidebar` | `variant`, `collapsible`, `side` | App sidebar with multiple collapse modes |
| `Menu` | `size` | Dropdown/context menu system |
| `Tabs` | `value`, `onChange` | Tab navigation |
| `ProgressSteps` | `steps`, `current` | Step progress indicator |
| `TextLink` | `href`, `color` | Styled text hyperlink |

### Overlay & Feedback

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Dialog` | `open`, `onOpenChange` | Modal dialog |
| `Popover` | `open`, `onOpenChange` | Floating popover |
| `Tooltip` | `content` | Hover tooltip |
| `Alert` | `color`, `variant`, `title` | Inline alert message |

### Content

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Markdown` | `children` | Render markdown content |
| `CodeBlock` | `language`, `code` | Syntax-highlighted code |
| `CopyTooltip` | `text` | Copy-to-clipboard with tooltip |
| `Icon` | Named exports | 460+ icons |
| `Image` | `src`, `alt` | Optimized image component |

### Form Helpers

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Field` | `children` | Form field wrapper |
| `FieldError` | `message` | Validation error display |

### Animation

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Animate` | `show`, `type` | Enter/exit transitions |
| `AnimateLayout` | `children` | Layout animation wrapper |
| `AnimateLayoutGroup` | `children` | Grouped layout animations |
| `TransitionGroup` | `children` | List transition management |

## Hooks

All hooks: `import { useX } from "@plexui/ui/hooks/useX"`

| Hook | Purpose |
|------|---------|
| `useBreakpoints` | Responsive breakpoint detection |
| `useScrollable` | Scroll state and overflow detection |
| `useAutoGrowTextarea` | Auto-growing textarea height |
| `useDocumentVisible` | Document visibility state |
| `useEscCloseStack` | Stacked ESC-to-close behavior |
| `useIsMounted` | Component mount state |
| `useLatestValue` | Latest ref value without re-renders |
| `usePrevious` | Previous render value |
| `useSimulatedProgress` | Fake progress bar animation |
| `useStableCallback` | Stable callback reference |
| `useTextSelection` | Text selection state |
| `useTrailingValue` | Delayed value updates |
| `useAnimatedScrollTo` | Smooth scroll animation |
| `useCharactersPerSecond` | Typing speed measurement |

## Size Scale

All key controls share a unified height scale via the `size` prop:

| Size | Height | Use case |
|------|--------|----------|
| `3xs` | 22px | Ultra-compact UI, dense tables |
| `2xs` | 24px | Compact toolbars |
| `xs` | 26px | Small controls |
| `sm` | 28px | Compact forms |
| **`md`** | **32px** | **Default — most UI** |
| `lg` | 36px | Prominent actions |
| `xl` | 40px | Hero sections |
| `2xl` | 44px | Large touch targets |
| `3xl` | 48px | Marketing CTAs |

## Color System

### Semantic colors (for `color` prop)

`primary`, `secondary`, `danger`, `success`, `warning`, `caution`, `discovery`, `info`

### Tailwind utility classes (from Plex UI tokens)

```
text-primary, text-secondary, text-tertiary, text-disabled
bg-surface, bg-surface-secondary, bg-surface-tertiary
border-default, border-subtle
```

## Dark Mode

Plex UI uses CSS `light-dark()` — no `dark:` prefixes needed.

```css
:root { color-scheme: light; }       /* light theme */
:root { color-scheme: dark; }        /* dark theme */
:root { color-scheme: light dark; }  /* follows OS preference */
```

## Key Patterns

```tsx
// Correct: subpath imports
import { Button } from "@plexui/ui/components/Button";
import { Input } from "@plexui/ui/components/Input";
import { IconSearch } from "@plexui/ui/components/Icon";

// Correct: semantic color + variant
<Button color="primary" variant="solid" size="md">Save</Button>
<Button color="danger" variant="ghost" size="sm">Delete</Button>

// Correct: icon inside button (auto-sized)
<Button color="primary">
  <IconSearch />
  Search
</Button>

// Correct: consistent size across form
<Input size="lg" placeholder="Email" />
<Select size="lg" placeholder="Role" />
<Button size="lg" color="primary">Submit</Button>

// Correct: dark mode via color-scheme
<html style={{ colorScheme: isDark ? "dark" : "light" }}>

// Wrong: raw Tailwind colors
<Button className="bg-blue-500 text-white">Save</Button>  // WRONG
// Wrong: root import
import { Button } from "@plexui/ui";  // WRONG
// Wrong: manual icon sizing inside components
<Button><IconSearch className="w-4 h-4" />Search</Button>  // WRONG
```

## Detailed References

- [rules/components.md](./rules/components.md) — Component composition, imports, provider setup
- [rules/styling.md](./rules/styling.md) — Tokens, colors, variants, size scale, dark mode
- [rules/icons.md](./rules/icons.md) — Icon imports, sizing, usage patterns

## Full Documentation

- [Installation](https://plexui.com/docs/overview/installation)
- [Components](https://plexui.com/docs/components)
- [Design Tokens](https://plexui.com/docs/foundations/design-tokens)
- [Colors](https://plexui.com/docs/foundations/colors)
- [Icons](https://plexui.com/docs/foundations/icons)
- [Dark Mode](https://plexui.com/docs/concepts/dark-mode)
- [Typography](https://plexui.com/docs/foundations/typography)

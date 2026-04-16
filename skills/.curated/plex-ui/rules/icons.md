# Icon Rules

## Imports

All icons are named exports from `@plexui/ui/components/Icon`:

```tsx
import { IconSearch, IconCheck, IconChevronDown, IconPlus } from "@plexui/ui/components/Icon";
```

There are **460+ icons** available. The naming convention is `Icon` + PascalCase name.

## Usage in Components

### Inside Button

Icons auto-size to match the button's `size` prop. **Never add manual size classes.**

```tsx
// Correct — icon auto-sizes
<Button color="primary" size="md">
  <IconSearch />
  Search
</Button>

// Correct — icon-only button
<Button color="secondary" variant="ghost" size="md">
  <IconPlus />
</Button>

// Wrong — manual sizing overrides the design system
<Button color="primary">
  <IconSearch className="w-4 h-4" />
  Search
</Button>
```

### Standalone icons

When using icons outside of components, you can set size via className:

```tsx
// Standalone icon with custom size
<IconCheck className="w-5 h-5 text-primary" />

// Inside a custom container
<div className="flex items-center gap-2">
  <IconSearch className="w-4 h-4 text-secondary" />
  <span>Search results</span>
</div>
```

### Override icon size in components

Use the `iconSize` prop when the default icon size doesn't fit:

```tsx
// Override icon size independently of control size
<Button color="primary" size="lg" iconSize="sm">
  <IconSearch />
  Search
</Button>
```

Icon size scale:

| `iconSize` | Pixels |
|-----------|--------|
| `sm` | 16px |
| `md` | 18px |
| `lg` | 20px |
| `xl` | 22px |
| `2xl` | 24px |

## Icon Color

Icons inherit text color by default. Use Tailwind text color utilities for standalone icons:

```tsx
// Inherits parent color
<IconCheck />

// Explicit color
<IconCheck className="text-primary" />
<IconCheck className="text-danger" />
<IconCheck className="text-secondary" />
```

Inside components like Button, icon color is handled automatically by the `color` and `variant` props.

## Common Icons

| Icon | Name | Usage |
|------|------|-------|
| Search | `IconSearch` | Search inputs, search actions |
| Check | `IconCheck` | Success states, checkmarks |
| Close/X | `IconX` | Close buttons, dismiss |
| Plus | `IconPlus` | Add/create actions |
| Chevron | `IconChevronDown`, `IconChevronRight` | Dropdowns, expand |
| Arrow | `IconArrowLeft`, `IconArrowRight` | Navigation |
| Settings | `IconSettings` | Settings/gear |
| User | `IconUser` | Profile, accounts |
| Trash | `IconTrash` | Delete actions |
| Edit | `IconEdit` | Edit actions |
| Copy | `IconCopy` | Copy to clipboard |
| External link | `IconExternalLink` | External navigation |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `<IconSearch className="w-4 h-4" />` inside Button | Remove size classes — auto-sized by component |
| `import { Search } from "lucide-react"` | Use `import { IconSearch } from "@plexui/ui/components/Icon"` |
| String-based icon lookup | Pass icon components directly: `icon={IconCheck}` |
| Manual SVG for common icons | Check the 460+ built-in icons first |

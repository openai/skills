# Component Rules

## Imports

All Plex UI components use **subpath imports**. Never import from the package root.

```tsx
// Correct
import { Button, ButtonLink } from "@plexui/ui/components/Button";
import { Input } from "@plexui/ui/components/Input";
import { Select, Option } from "@plexui/ui/components/Select";
import { useBreakpoints } from "@plexui/ui/hooks/useBreakpoints";
import type { ControlSize } from "@plexui/ui/types";

// Wrong — root imports don't exist
import { Button } from "@plexui/ui";
import { Button } from "@plexui/ui/components";
```

## PlexUIProvider

Every Plex UI app must be wrapped in `PlexUIProvider`. It supplies shared context (link routing, etc.) to all components.

```tsx
// Correct — with Next.js Link
import Link from "next/link";
import { PlexUIProvider } from "@plexui/ui/components/PlexUIProvider";

<PlexUIProvider linkComponent={Link}>
  {children}
</PlexUIProvider>

// Correct — plain HTML links
<PlexUIProvider linkComponent="a">
  {children}
</PlexUIProvider>

// Wrong — no provider
<Button color="primary">Save</Button>  // Works, but link components won't route correctly
```

## Component Composition

### Menu

Menu is a compound component with sub-items:

```tsx
import { Menu, MenuItem, MenuSeparator, MenuGroup, MenuTrigger } from "@plexui/ui/components/Menu";

<Menu>
  <MenuTrigger>
    <Button color="secondary">Options</Button>
  </MenuTrigger>
  <MenuGroup>
    <MenuItem>Edit</MenuItem>
    <MenuItem>Duplicate</MenuItem>
    <MenuSeparator />
    <MenuItem color="danger">Delete</MenuItem>
  </MenuGroup>
</Menu>
```

### Select

```tsx
import { Select, Option, OptionGroup } from "@plexui/ui/components/Select";

<Select size="md" placeholder="Choose role" value={role} onChange={setRole}>
  <OptionGroup label="Roles">
    <Option value="admin">Admin</Option>
    <Option value="editor">Editor</Option>
    <Option value="viewer">Viewer</Option>
  </OptionGroup>
</Select>
```

### Sidebar

Sidebar supports multiple collapse modes and has a rich sub-component structure:

```tsx
import {
  Sidebar,
  SidebarProvider,
  SidebarLayout,
  SidebarContent,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarHeader,
  SidebarFooter,
} from "@plexui/ui/components/Sidebar";

<SidebarProvider collapsible="icon" defaultOpen>
  <SidebarLayout>
    <Sidebar>
      <SidebarHeader>Logo</SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton isActive>Dashboard</SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>User</SidebarFooter>
    </Sidebar>
    <main>Content</main>
  </SidebarLayout>
</SidebarProvider>
```

### Dialog

```tsx
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "@plexui/ui/components/Dialog";

<Dialog>
  <DialogTrigger>
    <Button color="primary">Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm action</DialogTitle>
      <DialogDescription>This cannot be undone.</DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <DialogClose>
        <Button color="secondary">Cancel</Button>
      </DialogClose>
      <Button color="danger">Delete</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Tabs

```tsx
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@plexui/ui/components/Tabs";

<Tabs defaultValue="general">
  <TabsList>
    <TabsTrigger value="general">General</TabsTrigger>
    <TabsTrigger value="security">Security</TabsTrigger>
  </TabsList>
  <TabsContent value="general">General settings</TabsContent>
  <TabsContent value="security">Security settings</TabsContent>
</Tabs>
```

### Form Layout

```tsx
import { Field, FieldLabel, FieldDescription } from "@plexui/ui/components/Field";
import { FieldError } from "@plexui/ui/components/FieldError";
import { Input } from "@plexui/ui/components/Input";

<Field>
  <FieldLabel htmlFor="email">Email</FieldLabel>
  <Input id="email" size="md" placeholder="you@example.com" />
  <FieldDescription>We'll never share your email.</FieldDescription>
  <FieldError message={errors.email} />
</Field>
```

## Consistent Sizing

When building a form or action bar, use the same `size` across all controls:

```tsx
// Correct — consistent size
<div className="flex gap-2">
  <Input size="lg" placeholder="Search..." />
  <Select size="lg" placeholder="Filter" />
  <Button size="lg" color="primary">Go</Button>
</div>

// Wrong — mixed sizes look broken
<div className="flex gap-2">
  <Input size="md" placeholder="Search..." />
  <Select size="lg" placeholder="Filter" />
  <Button size="sm" color="primary">Go</Button>
</div>
```

## Animation Components

Plex UI includes motion primitives for enter/exit animations:

```tsx
import { Animate } from "@plexui/ui/components/Transition";

// Fade in/out
<Animate show={isVisible} type="fade">
  <div>Content</div>
</Animate>

// Scale in/out
<Animate show={isVisible} type="scale">
  <div>Content</div>
</Animate>
```

### TransitionGroup for lists:

```tsx
import { TransitionGroup } from "@plexui/ui/components/Transition";

<TransitionGroup>
  {items.map(item => (
    <div key={item.id}>{item.name}</div>
  ))}
</TransitionGroup>
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `import { Button } from "@plexui/ui"` | `import { Button } from "@plexui/ui/components/Button"` |
| Missing `PlexUIProvider` wrapper | Wrap root layout in `<PlexUIProvider>` |
| Using `className` for colors | Use `color` and `variant` props |
| Mixed `size` props in a row | Use same `size` for all controls in a group |
| Manual `dark:` color overrides | Use semantic tokens — dark mode is automatic |
| `<Icon className="w-4 h-4" />` inside Button | Remove size classes — components handle icon sizing |

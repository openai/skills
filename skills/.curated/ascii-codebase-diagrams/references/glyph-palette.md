# Unicode Box-Drawing Glyph Palette

Read this file before drawing any diagram. It defines the preferred glyphs, alignment rules, and a manual self-check.

## Character Set

### Lines

| Glyph | Use |
| ----- | --- |
| `─` | horizontal lines and connectors |
| `│` | vertical lines and connectors |
| `═` | emphasis borders or title underline when needed |
| `║` | emphasis borders |

### Corners

| Glyph | Use |
| ----- | --- |
| `┌` | top-left corner |
| `┐` | top-right corner |
| `└` | bottom-left corner |
| `┘` | bottom-right corner |
| `╔` | emphasized top-left corner |
| `╗` | emphasized top-right corner |
| `╚` | emphasized bottom-left corner |
| `╝` | emphasized bottom-right corner |

### Joins And Arrows

| Glyph | Use |
| ----- | --- |
| `├` | branch from a vertical line |
| `┤` | branch into a vertical line |
| `┬` | branch down from a horizontal line |
| `┴` | branch up from a horizontal line |
| `┼` | intersection |
| `▼` | downward flow |
| `▲` | upward flow or return |
| `►` | left-to-right flow |
| `◄` | right-to-left flow |
| `→` | inline key or note |
| `←` | right-side annotation |

### Tree Glyphs

Use `├──`, `└──`, and `│` for directory trees.

## Alignment Rules

1. Every `│` in a vertical run must share the same character offset.
2. Every `─` run must be continuous with no gaps.
3. Every box must close correctly: `┌` pairs with `┐`, and `└` pairs with `┘`.
4. Keep one space between box borders and label text.
5. Keep widths consistent in vertical chains of similar boxes.
6. Assume monospaced rendering.

## Self-Check

Before delivering a diagram:

1. Count columns for every vertical run and fix any drift.
2. Trace each horizontal run to confirm there are no breaks.
3. Verify every box closes.
4. Confirm arrows match the intended direction of flow.
5. Remove trailing whitespace.
6. Make the underline width match the title width.

## Skeletons

### Pipeline

```text
REQUEST FLOW
============

  ┌────────────────────────────┐
  │ Client request             │
  └────────────┬───────────────┘
               ▼
  ┌────────────────────────────┐
  │ Router / handler           │
  └────────────┬───────────────┘
               ▼
  ┌────────────────────────────┐
  │ Service / storage          │
  └────────────────────────────┘
```

### Module Map

```text
  ┌──────────┐   request   ┌──────────┐   query   ┌──────────┐
  │ Client   │────────────►│ Server   │──────────►│ Storage  │
  └──────────┘             └──────────┘           └──────────┘
```

### File Tree

```text
  repo/
  ├── src/
  │   ├── app.ts
  │   ├── routes/
  │   └── services/
  ├── tests/
  └── README.md
```

# MCP Tools Reference

## playground-create

Create an Anima Playground from a prompt, website URL, or Figma design.

| Parameter | Required | Type | Description |
|---|---|---|---|
| `type` | Yes | string | `p2c` (prompt), `l2c` (website URL), or `f2c` (Figma) |
| `prompt` | p2c only | string | Text description of what to build |
| `guidelines` | No | string | Additional coding guidelines (p2c only) |
| `url` | l2c only | string | Website URL to recreate |
| `fileKey` | f2c only | string | Figma file key from URL |
| `nodesId` | f2c only | array | Figma node IDs (use `:` not `-`) |
| `framework` | No | string | `react` or `html` |
| `styling` | No | string | Varies by type (see below) |
| `language` | No | string | `typescript` or `javascript` (react only) |
| `uiLibrary` | No | string | UI library (react only, varies by type) |

**Styling options per type:**

| Type | Styling options |
|---|---|
| p2c | `tailwind`, `css`, `inline_styles` |
| l2c | `tailwind`, `inline_styles` |
| f2c | `tailwind`, `plain_css`, `css_modules`, `inline_styles` |

**UI Library options per type:**

| Type | UI Library options |
|---|---|
| p2c | Not supported |
| l2c | `shadcn` only |
| f2c | `mui`, `antd`, `shadcn`, `clean_react` |

**Returns:** `{ success, sessionId, playgroundUrl }`

## playground-publish

Publish a playground to a live URL or as a design system package.

| Parameter | Required | Type | Description |
|---|---|---|---|
| `sessionId` | Yes | string | Session ID from `playground-create` |
| `mode` | No | string | `webapp` (default) or `designSystem` |
| `packageName` | designSystem only | string | Package name |
| `packageVersion` | designSystem only | string | Package version |

**Returns (webapp):** `{ success, liveUrl, subdomain }`

**Returns (designSystem):** `{ success, packageUrl, packageName, packageVersion }`

## codegen-figma_to_code

Convert Figma design to production-ready code directly (no playground). **Path B only.**

| Parameter | Required | Type | Description |
|---|---|---|---|
| `fileKey` | Yes | string | Figma file key from URL |
| `nodesId` | Yes | array | Node IDs to convert (use `:` not `-`) |
| `framework` | No | string | `react` or `html` (default: react) |
| `styling` | No | string | `tailwind`, `plain_css`, `css_modules`, or `inline_styles` |
| `language` | No | string | `typescript` or `javascript` (default: typescript) |
| `uiLibrary` | No | string | `mui`, `antd`, `shadcn`, or `clean_react` |
| `assetsBaseUrl` | No | string | Base path for assets (e.g., `./assets`) |

**Returns:** `{ files, assets, snapshotsUrls, guidelines, tokenUsage }`

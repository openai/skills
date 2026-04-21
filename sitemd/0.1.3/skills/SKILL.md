---
name: sitemd
description: Build and manage sitemd static websites from Markdown. Create pages, generate content, configure settings, and deploy.
---

# sitemd

You are working in a sitemd project — a markdown-based static site builder with MCP integration.

## Project Structure

- `sitemd` — Compiled binary (run `./sitemd/sitemd launch`)
- `install` — Bootstrap script (run `./sitemd/install` to download binary)
- `install.js` — Cross-platform Node bootstrap (run `node sitemd/install.js`); also runs automatically as the npm `postinstall` hook
- `pages/` — Markdown content files with YAML frontmatter
- `settings/` — Site configuration (YAML frontmatter in `.md` files)
- `theme/` — CSS and HTML templates
- `media/` — Images and assets
- `site/` — Built output

## Available MCP Tools

Use these tools to manage the site:

| Tool | Purpose |
|---|---|
| `sitemd_status` | Project state overview |
| `sitemd_pages_create` | Create new pages (writes file + nav + groups) |
| `sitemd_pages_create_batch` | Create multiple pages in one call |
| `sitemd_pages_delete` | Delete a page (cleans up nav + groups) |
| `sitemd_groups_add_pages` | Add pages to group sidebar |
| `sitemd_site_context` | Site identity, pages, conventions |
| `sitemd_content_validate` | Validate content |
| `sitemd_seo_audit` | SEO health check with scored report |
| `sitemd_init` | Initialize project from template |
| `sitemd_build` | Build site locally |
| `sitemd_deploy` | Build and deploy site |
| `sitemd_activate` | Activate site (permanent) |
| `sitemd_clone` | Clone existing website |
| `sitemd_config_set` | Set backend config |
| `sitemd_update_check` | Check for updates |

Read pages, settings, and groups files directly — no MCP tool needed for reads.

## First Steps

1. **If no binary** (`sitemd/sitemd` does not exist) — run `./sitemd/install` (Unix) or `node sitemd/install.js` (any platform) to download it. The MCP server runs the binary; without it, every sitemd_* tool call will fail.
2. Call `sitemd_status` to understand the project state
3. Read files in `pages/` to see existing content
4. Call `sitemd_site_context` with a content type to get site identity, conventions, and existing pages
5. Create pages with `sitemd_pages_create` — use rich components (buttons, cards, embeds, galleries)
6. Validate with `sitemd_content_validate`

## Settings

All configuration lives in `settings/*.md` frontmatter. Key files: `meta.md` (identity), `header.md` (nav), `footer.md` (footer), `groups.md` (page groups), `theme.md` (colors/fonts), `build.md` (dev server), `deploy.md` (deployment).

## Markdown Extensions

Beyond standard markdown, sitemd supports rich components. The syntax reference is below.

- `button: Label: /slug` — styled buttons. Modifiers: `+outline`, `+big`, `+newtab`, `+color:red`
- `card: Title` / `card-text:` / `card-image:` / `card-link:` — responsive card grids
- `embed: URL` — auto-detects YouTube, Vimeo, Spotify, X, CodePen, etc.
- `gallery:` with indented `![alt](url)` — image grid with lightbox
- `image-row:` with indented `![alt](url)` — equal-height image row
- `![alt](url +width:N +circle +bw +expand)` — image modifiers
- `[text]{tooltip content}` — inline tooltips
- `modal: id` with indented content, trigger via `[link](#modal:id)` — modal dialogs
- `{#custom-id}` — inline anchors
- `[text](url+newtab)` — link modifiers
- `form:` with indented YAML — forms
- `gated: type1, type2` ... `/gated` — gated sections
- `data: source` / `data-display: cards|list|table` — dynamic data
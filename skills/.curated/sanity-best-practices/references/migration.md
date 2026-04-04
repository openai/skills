---
title: Sanity Content Migration Rules
description: Best practices for migrating content (HTML, Markdown) into Sanity Portable Text.
---

# Sanity Content Migration Rules

## 1. HTML Import (Legacy CMS)
Use `@portabletext/block-tools` with `JSDOM` to convert HTML to Portable Text. This covers setup, custom deserializers, pre-processing, image uploads, and wrapping in `defineMigration`.

**See `migration-html-import.md` for the full guide with working examples.**

## 2. Markdown Import (Static Sites)
Use `@sanity/block-content-to-markdown` (legacy name, often used in reverse) OR use a dedicated parser like `remark` to convert Markdown to HTML, then use `block-tools`.

**Recommended Path: Markdown -> HTML -> Portable Text**
This is often more robust than direct Markdown-to-PT parsers because `block-tools` handles schema validation better.

1.  **Parse:** `marked` or `remark` to convert MD to HTML.
2.  **Convert:** Use `htmlToBlocks` (see above).

**Alternative: Direct Parsing**
If using a library like `markdown-to-sanity` or writing a custom `remark` serializer:
-   Ensure you handle "inline" vs "block" nodes correctly.
-   Map images to Sanity asset uploads.

## 3. Image Handling (Universal)
Don't just link to external images. Download them and upload to Sanity Asset Pipeline.

1.  **Extract:** Find `<img>` tags or Markdown image syntax.
2.  **Download:** Fetch the image buffer.
3.  **Upload:** `client.assets.upload('image', buffer)`
4.  **Replace:** Return a Sanity Image block with the new asset reference.

## 4. Schema Validation
Ensure your destination schema allows the structures you are importing.
-   **Tables:** Need a `table` type (HTML `<table>` or GFM tables).
-   **Code:** Need a `code` type (HTML `<pre><code>` or MD code fences).

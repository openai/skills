---
title: Import HTML to Portable Text
description: Use @portabletext/block-tools with JSDOM to convert HTML content
---

## Import HTML to Portable Text

Use `@portabletext/block-tools` with `JSDOM` to convert HTML from legacy CMSs to Portable Text.

### Setup

```bash
npm install @portabletext/block-tools jsdom
```

### Basic Conversion

```typescript
import { htmlToBlocks } from '@portabletext/block-tools'
import { JSDOM } from 'jsdom'

// Get block content type from your schema
const blockContentType = schema.get('blockContent')

const blocks = htmlToBlocks(htmlString, blockContentType, {
  parseHtml: html => new JSDOM(html).window.document,
})
```

### Custom Deserializers

Handle specific HTML patterns:

```javascript
const blocks = htmlToBlocks(htmlString, blockContentType, {
  parseHtml: html => new JSDOM(html).window.document,
  rules: [
    {
      deserialize(el, next, block) {
        // Custom link handling
        if (el.tagName.toLowerCase() === 'a') {
          return {
            _type: 'link',
            href: el.getAttribute('href'),
            blank: el.getAttribute('target') === '_blank'
          }
        }
        // Custom image handling
        if (el.tagName.toLowerCase() === 'img') {
          return {
            _type: 'image',
            // Upload image separately, store reference
            _sanityAsset: `image@${el.getAttribute('src')}`
          }
        }
        return undefined  // Fall through to default handling
      }
    }
  ]
})
```

### Pre-Processing HTML

Clean HTML before conversion:

```javascript
function cleanHtml(html) {
  const dom = new JSDOM(html)
  const doc = dom.window.document
  
  // Remove layout elements
  doc.querySelectorAll('header, footer, nav, .sidebar').forEach(el => el.remove())
  
  // Extract metadata before processing body
  const title = doc.querySelector('title')?.textContent
  const description = doc.querySelector('meta[name="description"]')?.content
  
  return {
    body: doc.body.innerHTML,
    metadata: { title, description }
  }
}
```

### Image Upload

Don't just link external images—upload them:

```javascript
async function uploadImage(client, imageUrl) {
  const response = await fetch(imageUrl)
  const buffer = await response.arrayBuffer()
  
  const asset = await client.assets.upload('image', Buffer.from(buffer), {
    filename: imageUrl.split('/').pop()
  })
  
  return {
    _type: 'image',
    asset: { _type: 'reference', _ref: asset._id }
  }
}
```

### Using in a Migration

Wrap this in `defineMigration` for reproducible imports:

```typescript
// migrations/import-wordpress-posts/index.ts
import {defineMigration, createOrReplace} from 'sanity/migrate'
import {htmlToBlocks} from '@portabletext/block-tools'

export default defineMigration({
  title: 'Import WordPress posts',
  async *migrate(documents, context) {
    const posts = await fetchWordPressPosts() // Your import source
    
    for (const post of posts) {
      const blocks = htmlToBlocks(post.content, blockContentType, {
        parseHtml: html => new JSDOM(html).window.document,
      })
      
      yield createOrReplace({
        _id: `post-${post.slug}`,
        _type: 'post',
        title: post.title,
        body: blocks,
      })
    }
  }
})
```

Run with: `sanity migration run import-wordpress-posts --no-dry-run`

Reference: [Schema and Content Migrations](https://www.sanity.io/docs/content-lake/schema-and-content-migrations)

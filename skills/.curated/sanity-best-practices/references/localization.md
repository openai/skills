---
title: Sanity Localization Rules
description: Localization patterns for Sanity using official plugins and best practices.
---

# Sanity Localization Rules

## 1. Guiding Principles

### Priority: Easy Authoring Experience
The structured nature of Sanity schemas and GROQ make it easy to parse localized content for your frontend. **Never** let frontend architecture dictate your localization approach — prioritize the editor experience.

### Avoid Content Duplication
Don't create nearly identical copies with slight differences (e.g., US vs British English). Use Portable Text marks and custom blocks to swap out words or sections as needed.

## 2. Terminology

| Term | Definition |
|------|------------|
| **Internationalization (i18n)** | Designing your frontend to support multiple languages |
| **Localization** | Adapting content for a specific language/region |
| **Language Tag** | Code like `en`, `en-US`, `zh-Hant-TW` (per IETF RFC 5646) |
| **Locale** | A language tag with region info (e.g., `en-US`) |

## 3. Create a Locale Content Type

**Best Practice:** Store locales in Sanity, not just in code. This allows sharing between Studio and frontend.

```typescript
// schemaTypes/locale.ts
import { TranslateIcon } from '@sanity/icons'
import { defineField, defineType } from 'sanity'

export const localeType = defineType({
  name: 'locale',
  icon: TranslateIcon,
  type: 'document',
  fields: [
    defineField({ name: 'name', type: 'string', validation: (r) => r.required() }),
    defineField({ name: 'tag', type: 'string', description: 'IANA tag (en, en-US)', validation: (r) => r.required() }),
    defineField({ name: 'fallback', type: 'reference', to: [{ type: 'locale' }] }),
    defineField({ name: 'default', type: 'boolean' }),
  ],
  preview: { select: { title: 'name', subtitle: 'tag' } },
})
```

**Tip:** Restrict locale editing to admins via Structure by filtering `locale` from non-admin users.

## 4. Choose Your Localization Method

| Content Type | Examples | Recommended Method |
|--------------|----------|-------------------|
| **Structured** (things) | Products, People, Locations, Categories | Field-level |
| **Presentation** (UI) | Pages, Posts, Components | Document-level |

### Decision Questions
1. **Are fields shared across languages?** → Field-level
2. **Should changes be "global" for all locales?** (e.g., reordering components) → Field-level
3. **Is content mostly the same except regional differences?** → Field-level with PT marks
4. **Need to publish language versions independently?** → Document-level

## 5. Document-Level Localization

Use the **@sanity/document-internationalization** plugin.

```bash
npm install @sanity/document-internationalization
```

### Configuration
```typescript
// sanity.config.ts
import { documentInternationalization } from '@sanity/document-internationalization'

export default defineConfig({
  plugins: [
    documentInternationalization({
      // Fetch from Content Lake
      supportedLanguages: (client) =>
        client.fetch(`*[_type == "locale"]{ "id": tag, "title": name }`),
      // Document types to localize
      schemaTypes: ['post', 'page'],
    }),
  ],
})
```

### Add Language Field to Schema
```typescript
// In each schema type listed in schemaTypes
defineField({
  name: 'language',
  type: 'string',
  readOnly: true,
  hidden: true,
})
```

### Initial Value Templates
Pre-set language when creating documents outside the translation UI:

```typescript
// sanity.config.ts
import { template } from 'sanity'

export default defineConfig({
  // ...
  document: {
    newDocumentOptions: (prev, { creationContext }) => {
      // Filter to only show base language in "New document" menu
      // The plugin handles creating translations from there
      return prev.filter((item) =>
        !['post', 'page'].includes(item.templateId) ||
        item.parameters?.language === 'en'
      )
    },
  },
  // Initial value templates for each language
  templates: (prev) => [
    ...prev,
    template.initial({
      id: 'post-en',
      title: 'Post (English)',
      schemaType: 'post',
      parameters: [{name: 'language', type: 'string'}],
      value: ({language}) => ({language}),
    }),
  ],
})
```

### Querying Translated Documents
```groq
// Get document in specific language
*[_type == "post" && language == $locale && slug.current == $slug][0]

// Get all translations via metadata document
*[_type == "translation.metadata" && references($docId)][0] {
  translations[] {
    _key,
    value-> { title, slug, language }
  }
}
```

## 6. Localized Singletons (Homepage per Locale)

For singletons like homepages that need a separate document per locale, combine document-level localization with the singleton pattern.

### Schema Definition

```typescript
// schemaTypes/homePage.ts
import { HomeIcon } from '@sanity/icons'
import { defineType, defineField } from 'sanity'

export const homePageType = defineType({
  name: 'homePage',
  title: 'Home Page',
  type: 'document',
  icon: HomeIcon,
  fields: [
    defineField({
      name: 'language',
      type: 'string',
      readOnly: true,
      hidden: true,
    }),
    defineField({ name: 'title', type: 'string' }),
    defineField({ name: 'pageBuilder', type: 'pageBuilder' }),
    // ... other fields
  ],
  preview: {
    select: { language: 'language' },
    prepare({ language }) {
      return {
        title: 'Home Page',
        subtitle: language?.toUpperCase() || 'No language',
      }
    },
  },
})
```

### Initial Value Templates

Create templates that pre-set the language for each locale:

```typescript
// sanity.config.ts
import { defineConfig, Template } from 'sanity'

// Define your supported locales
const LOCALES = [
  { id: 'en', title: 'English' },
  { id: 'fr', title: 'French' },
  { id: 'de', title: 'German' },
]

export default defineConfig({
  // ...
  templates: (prev) => {
    // Create a template for each locale
    const homePageTemplates: Template[] = LOCALES.map((locale) => ({
      id: `homePage-${locale.id}`,
      title: `Home Page (${locale.title})`,
      schemaType: 'homePage',
      parameters: [{ name: 'language', type: 'string' }],
      value: { language: locale.id },
    }))

    return [...prev, ...homePageTemplates]
  },
})
```

### Structure: Localized Singleton Helper

Create a helper to show one singleton per locale in the Structure:

```typescript
// src/structure/index.ts
import { StructureBuilder, StructureResolver } from 'sanity/structure'
import { HomeIcon } from '@sanity/icons'

const LOCALES = ['en', 'fr', 'de']

function createLocalizedSingleton(
  S: StructureBuilder,
  typeName: string,
  title: string,
  icon?: React.ComponentType
) {
  return S.listItem()
    .title(title)
    .icon(icon)
    .child(
      S.list()
        .title(title)
        .items(
          LOCALES.map((locale) =>
            S.listItem()
              .title(`${title} (${locale.toUpperCase()})`)
              .icon(icon)
              .child(
                S.document()
                  .schemaType(typeName)
                  .documentId(`${typeName}-${locale}`) // Fixed ID per locale
                  .title(`${title} (${locale.toUpperCase()})`)
              )
          )
        )
    )
}

export const structure: StructureResolver = (S) =>
  S.list()
    .title('Content')
    .items([
      // Localized singletons
      createLocalizedSingleton(S, 'homePage', 'Home Page', HomeIcon),

      S.divider(),

      // Filter localized singletons from default list
      ...S.documentTypeListItems().filter(
        (item) => !['homePage'].includes(item.getId() as string)
      ),
    ])
```

### Querying Localized Singletons

```groq
// Get homepage for specific locale
*[_type == "homePage" && language == $locale][0]{
  title,
  pageBuilder[]{...}
}

// Or by fixed document ID
*[_id == "homePage-" + $locale][0]{...}
```

### Key Points

- **Fixed IDs:** Use `${typeName}-${locale}` pattern for predictable document IDs
- **Initial Value Templates:** Essential for the "New document" menu to work correctly
- **Structure:** Group all locale versions under one list item for cleaner navigation
- **See also:** `studio-structure.md` for more singleton patterns

## 7. Field-Level Localization

Use **sanity-plugin-internationalized-array** (NOT localized objects — they hit attribute limits).

```bash
npm install sanity-plugin-internationalized-array
```

### Configuration
```typescript
// sanity.config.ts
import { internationalizedArray } from 'sanity-plugin-internationalized-array'

export default defineConfig({
  plugins: [
    internationalizedArray({
      languages: (client) =>
        client.fetch(`*[_type == "locale"]{ "id": tag, "title": name }`),
      fieldTypes: ['string', 'text', 'simpleBlockContent'],
    }),
  ],
})
```

### Usage in Schema
```typescript
// The plugin creates types like `internationalizedArrayString`
defineField({
  name: 'jobTitle',
  type: 'internationalizedArrayString', // Localized string field
})
```

### Portable Text Localization
Create a reusable block content type, then add it to `fieldTypes`:

```typescript
// schemaTypes/simpleBlockContent.ts
export default defineType({
  name: 'simpleBlockContent',
  type: 'array',
  of: [
    {
      type: 'block',
      styles: [{ title: 'Normal', value: 'normal' }],
      lists: [],
    },
  ],
})

// sanity.config.ts
fieldTypes: ['string', 'simpleBlockContent']

// In your schema
defineField({
  name: 'bio',
  type: 'internationalizedArraySimpleBlockContent',
})
```

### Querying Internationalized Arrays
```groq
// Get specific locale value
*[_type == "author"][0] {
  "jobTitle": jobTitle[_key == $locale][0].value
}

// With fallback
*[_type == "author"][0] {
  "jobTitle": coalesce(
    jobTitle[_key == $locale][0].value,
    jobTitle[_key == "en"][0].value
  )
}
```

## 8. AI-Powered Translation

Use **@sanity/assist** for automated translations.

```bash
npm install @sanity/assist
```

```typescript
// sanity.config.ts
import { assist } from '@sanity/assist'

export default defineConfig({
  plugins: [
    assist({
      translate: {
        // For document-level localization
        document: {
          languageField: 'language',
        },
        // For field-level localization
        field: {
          languages: (client) =>
            client.fetch(`*[_type == "locale"]{ "id": tag, "title": name }`),
          documentTypes: ['author', 'category'],
        },
      },
    }),
  ],
})
```

## 9. UI Enhancement

Use **@sanity/language-filter** to let editors show/hide locales:

```bash
npm install @sanity/language-filter
```

## 10. Frontend URL Best Practices

**Always include locale in the URL** for SEO:
- `yoursite.com/en/my-page` → `yoursite.com/fr/my-page`
- `yoursite.com/my-page` → redirects to default locale

**Avoid:** Having the default locale at root without prefix — causes SEO edge cases.

Use Next.js middleware (or framework equivalent) to redirect paths missing a locale prefix to the default locale.

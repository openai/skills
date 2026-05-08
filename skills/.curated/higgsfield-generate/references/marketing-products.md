# Products

Marketing Studio supports physical products and webproducts.

## Product Vs Webproduct

- `product` — a specific physical or sellable item. Use for a SKU, product page, bottle, clothing item, gadget, supplement, etc.
- `webproduct` — an app, SaaS, website, or service. Use for App Store / Play Store pages, landing pages, or company homepages where no single item should be featured.

When unsure, default to `product`. App Store and Play Store URLs should be `webproduct`.

## Fetch From URL

Call `show_marketing_studio`:

```json
{
  "action": "fetch",
  "url": "https://shop.example.com/sneakers",
  "type": "product"
}
```

Omit `type` when the URL should be inferred. The response renders the library widget and may include `next_step`; for Click-to-Ad, follow `next_step` immediately.

## Create From Uploaded Media

1. Upload/confirm product images with `media_upload` and `media_confirm`.
2. Call `show_marketing_studio`:

```json
{
  "action": "create",
  "type": "product",
  "title": "AeroRun Pro",
  "description": "Lightweight running shoe",
  "medias": [
    { "value": "<media_id>", "role": "image", "url": "<cdn_url_if_available>", "type": "media_input" }
  ]
}
```

If `title` is omitted, the server derives one from media filenames or URLs.

## Manual Webproduct

Use `show_marketing_studio` with `action: "create"` and `type: "webproduct"`. Useful fields include `title`, `subtitle`, `description`, `webproduct_url`, `favicon_url`, and `webproduct_medias`.

## Listing

Use `show_marketing_studio` with:

```json
{ "action": "list", "type": "product" }
```

or:

```json
{ "action": "list", "type": "webproduct" }
```

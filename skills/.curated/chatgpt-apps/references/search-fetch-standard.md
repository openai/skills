# Search And Fetch Standard

Load this reference when the app is connector-like, data-only, sync-oriented, or meant to work well with company knowledge or deep research.

## Default Rule

If the app is primarily a read-only knowledge source, do not invent custom equivalents to `search` and `fetch`.

Default to implementing the standard `search` and `fetch` tools exactly, then add other tools only if the use case clearly needs them.

## When This Applies

Use the standard by default when the request is about:

- a data-only app
- a sync app
- a company knowledge source
- deep research compatibility
- a connector-like integration over documents, tickets, wiki pages, CRM records, or similar read-only data

## Tool Requirements

### `search`

- Read-only tool
- Takes a single query string
- Returns exactly one MCP content item with `type: "text"`
- That text is a JSON-encoded object with:
  - `results`
  - each result has `id`, `title`, and `url`

### `fetch`

- Read-only tool
- Takes a single document/item id string
- Returns exactly one MCP content item with `type: "text"`
- That text is a JSON-encoded object with:
  - `id`
  - `title`
  - `text`
  - `url`
  - optional `metadata`

## Implementation Rules

- Match the schema exactly when the app is intended for company knowledge or deep research compatibility.
- Use canonical `url` values for citations.
- Mark these tools as read-only.
- Prefer these names exactly: `search` and `fetch`.
- If you add other read-only tools, they should complement the standard rather than replace it.

## Validation Checks

When `search` and `fetch` are relevant, verify:

- both tools exist
- they are read-only
- their input shapes match the standard
- their returned payloads are wrapped as one `content` item with JSON-encoded `text`
- result URLs are canonical enough for citation use

## Source

This standard is described in:

- `https://developers.openai.com/apps-sdk/build/mcp-server/#company-knowledge-compatibility`
- `https://platform.openai.com/docs/mcp`

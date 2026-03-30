# Olostep API Quick Reference

## Scrape Endpoint

**Base:** `client.scrapes.create()`

### Parameters
- `url_to_scrape` (required): URL to scrape
- `formats` (list): Content formats to return. Options: `"markdown"`, `"text"`, `"html"`, `"json"`
- `country` (optional): ISO country code for geo-specific scraping (e.g., `"us"`, `"gb"`)
- `parser` (optional): Dict with `{"id": "parser_id"}` for custom parsing

### Response
- `markdown_content`: Cleaned markdown
- `text_content`: Plain text
- `html_content`: Raw HTML
- `json_content`: Structured JSON
- Returns first available content in priority order

## Search Endpoint

**Base:** `client.search.create()`

### Parameters
- `query` (required): Search query string
- `max_results` (optional): Limit results (default varies by implementation)

### Response
- List of results with `title`, `url`, `description`

## Crawl Endpoint

**Base:** `client.crawl.create()`

### Parameters
- `url` (required): Starting URL
- `max_pages` (optional): Maximum pages to crawl (default 20)

### Response
- List of pages with `url` and `markdown_content`

## Answer Endpoint

**Base:** `client.answer.create()`

### Parameters
- `task` (required): Question or research task
- `sources` (optional): Pre-selected URLs to use

### Response
- `answer`: AI-synthesized response
- `sources`: List of cited URLs

## Error Handling

All endpoints raise `Olostep_BaseError` on failure. Check:
- `OLOSTEP_API_KEY` environment variable is set
- URL is publicly accessible
- API quota is not exceeded

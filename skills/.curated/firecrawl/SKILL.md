---
name: "firecrawl"
description: "Use when the task requires searching the web, scraping web pages to clean markdown, extracting structured data from URLs, discovering all URLs on a site, or crawling websites via the `firecrawl` CLI."
---

# Firecrawl CLI

Use the `firecrawl` CLI to search the web, scrape pages to clean markdown, and extract structured data from URLs.

## Prerequisites

- When sandboxing blocks network calls, rerun with `sandbox_permissions=require_escalated`.
- Web operations require internet access. Use appropriate timeout values for large scrapes.

## Prerequisite check (required)

Before proposing commands, verify the CLI is available:

```bash
command -v firecrawl >/dev/null 2>&1
```

If not installed:

```bash
npm install -g firecrawl-cli
```

If `npm` is not available, pause and ask the user to install Node.js/npm first.

## Authentication

Check status, auth, and rate limits:

```bash
firecrawl --status
```

Output when ready:

```
  🔥 firecrawl cli v1.0.2

  ● Authenticated via FIRECRAWL_API_KEY
  Concurrency: 0/100 jobs (parallel scrape limit)
  Credits: 500,000 remaining
```

- **Concurrency**: Max parallel jobs. Run parallel operations close to this limit but not above.
- **Credits**: Remaining API credits. Each scrape/crawl consumes credits.

If not authenticated, run:

```bash
firecrawl login --browser
```

The `--browser` flag automatically opens the browser for authentication without prompting. This is the recommended method for agents. Don't tell users to run the commands themselves, just execute the command and have it prompt them to authenticate in their browser.

### Authentication error handling

If any command returns an authentication error after running `firecrawl login --browser` (e.g., "not authenticated", "unauthorized", "API key"), ask the user:

**"How would you like to authenticate with Firecrawl?"**

1. **Login with browser (Recommended)** - Opens the browser to authenticate with Firecrawl
2. **Enter API key manually** - Paste an existing API key from firecrawl.dev

If user selects browser login, run `firecrawl login --browser` again. If user selects manual API key, ask for their key, then run:

```bash
firecrawl login --api-key "<their-key>"
```

Or set the environment variable:

```bash
export FIRECRAWL_API_KEY="<their-key>"
```

## Organization

Create a `.firecrawl/` folder in the working directory unless it already exists to store results unless a user specifies to return in context. Add .firecrawl/ to the .gitignore file if not already there. Always use `-o` to write directly to file (avoids flooding context):

```bash
# Search the web (most common operation)
firecrawl search "your query" -o .firecrawl/search-{query}.json

# Search with scraping enabled
firecrawl search "your query" --scrape -o .firecrawl/search-{query}-scraped.json

# Scrape a page
firecrawl scrape https://example.com -o .firecrawl/{site}-{path}.md
```

Examples:

```
.firecrawl/search-react_server_components.json
.firecrawl/search-ai_news-scraped.json
.firecrawl/docs.github.com-actions-overview.md
.firecrawl/firecrawl.dev.md
```

For temporary one-time scripts (batch scraping, data processing), use `.firecrawl/scratchpad/`:

```bash
.firecrawl/scratchpad/bulk-scrape.sh
.firecrawl/scratchpad/process-results.sh
```

Organize into subdirectories when it makes sense for the task:

```
.firecrawl/competitor-research/
.firecrawl/docs/nextjs/
.firecrawl/news/2024-01/
```

**Always quote URLs** - shell interprets `?` and `&` as special characters.

## Commands

### Search - Web search with optional scraping

```bash
# Basic search (human-readable output)
firecrawl search "your query" -o .firecrawl/search-query.txt

# JSON output (recommended for parsing)
firecrawl search "your query" -o .firecrawl/search-query.json --json

# Limit results
firecrawl search "AI news" --limit 10 -o .firecrawl/search-ai-news.json --json

# Search specific sources
firecrawl search "tech startups" --sources news -o .firecrawl/search-news.json --json
firecrawl search "landscapes" --sources images -o .firecrawl/search-images.json --json
firecrawl search "machine learning" --sources web,news,images -o .firecrawl/search-ml.json --json

# Filter by category (GitHub repos, research papers, PDFs)
firecrawl search "web scraping python" --categories github -o .firecrawl/search-github.json --json
firecrawl search "transformer architecture" --categories research -o .firecrawl/search-research.json --json

# Time-based search
firecrawl search "AI announcements" --tbs qdr:d -o .firecrawl/search-today.json --json  # Past day
firecrawl search "tech news" --tbs qdr:w -o .firecrawl/search-week.json --json          # Past week
firecrawl search "yearly review" --tbs qdr:y -o .firecrawl/search-year.json --json      # Past year

# Location-based search
firecrawl search "restaurants" --location "San Francisco,California,United States" -o .firecrawl/search-sf.json --json
firecrawl search "local news" --country DE -o .firecrawl/search-germany.json --json

# Search AND scrape content from results
firecrawl search "firecrawl tutorials" --scrape -o .firecrawl/search-scraped.json --json
firecrawl search "API docs" --scrape --scrape-formats markdown,links -o .firecrawl/search-docs.json --json
```

**Search Options:**

- `--limit <n>` - Maximum results (default: 5, max: 100)
- `--sources <sources>` - Comma-separated: web, images, news (default: web)
- `--categories <categories>` - Comma-separated: github, research, pdf
- `--tbs <value>` - Time filter: qdr:h (hour), qdr:d (day), qdr:w (week), qdr:m (month), qdr:y (year)
- `--location <location>` - Geo-targeting (e.g., "Germany")
- `--country <code>` - ISO country code (default: US)
- `--scrape` - Enable scraping of search results
- `--scrape-formats <formats>` - Scrape formats when --scrape enabled (default: markdown)
- `-o, --output <path>` - Save to file

### Scrape - Single page content extraction

```bash
# Basic scrape (markdown output)
firecrawl scrape https://example.com -o .firecrawl/example.md

# Get raw HTML
firecrawl scrape https://example.com --html -o .firecrawl/example.html

# Multiple formats (JSON output)
firecrawl scrape https://example.com --format markdown,links -o .firecrawl/example.json

# Main content only (removes nav, footer, ads)
firecrawl scrape https://example.com --only-main-content -o .firecrawl/example.md

# Wait for JS to render
firecrawl scrape https://spa-app.com --wait-for 3000 -o .firecrawl/spa.md

# Extract links only
firecrawl scrape https://example.com --format links -o .firecrawl/links.json

# Include/exclude specific HTML tags
firecrawl scrape https://example.com --include-tags article,main -o .firecrawl/article.md
firecrawl scrape https://example.com --exclude-tags nav,aside,.ad -o .firecrawl/clean.md
```

**Scrape Options:**

- `-f, --format <formats>` - Output format(s): markdown, html, rawHtml, links, screenshot, json
- `-H, --html` - Shortcut for `--format html`
- `--only-main-content` - Extract main content only
- `--wait-for <ms>` - Wait before scraping (for JS content)
- `--include-tags <tags>` - Only include specific HTML tags
- `--exclude-tags <tags>` - Exclude specific HTML tags
- `-o, --output <path>` - Save to file

### Map - Discover all URLs on a site

```bash
# List all URLs (one per line)
firecrawl map https://example.com -o .firecrawl/urls.txt

# Output as JSON
firecrawl map https://example.com --json -o .firecrawl/urls.json

# Search for specific URLs
firecrawl map https://example.com --search "blog" -o .firecrawl/blog-urls.txt

# Limit results
firecrawl map https://example.com --limit 500 -o .firecrawl/urls.txt

# Include subdomains
firecrawl map https://example.com --include-subdomains -o .firecrawl/all-urls.txt
```

**Map Options:**

- `--limit <n>` - Maximum URLs to discover
- `--search <query>` - Filter URLs by search query
- `--sitemap <mode>` - include, skip, or only
- `--include-subdomains` - Include subdomains
- `--json` - Output as JSON
- `-o, --output <path>` - Save to file

## Reading Scraped Files

NEVER read entire firecrawl output files at once unless explicitly asked or required. They are often 1000+ lines. Instead, use grep, head, or incremental reads. Determine values dynamically based on file size and what you are looking for.

Examples:

```bash
# Check file size and preview structure
wc -l .firecrawl/file.md && head -50 .firecrawl/file.md

# Use grep to find specific content
grep -n "keyword" .firecrawl/file.md
grep -A 10 "## Section" .firecrawl/file.md

# Read incrementally with offset/limit
# Read(file, offset=1, limit=100)
# Read(file, offset=100, limit=100)
```

Adjust line counts, offsets, and grep context as needed. Use other bash commands (awk, sed, jq, cut, sort, uniq, etc.) when appropriate for processing output.

## Format Behavior

- **Single format**: Outputs raw content (markdown text, HTML, etc.)
- **Multiple formats**: Outputs JSON with all requested data

```bash
# Raw markdown output
firecrawl scrape https://example.com --format markdown -o .firecrawl/page.md

# JSON output with multiple formats
firecrawl scrape https://example.com --format markdown,links -o .firecrawl/page.json
```

## Combining with Other Tools

```bash
# Extract URLs from search results
jq -r '.data.web[].url' .firecrawl/search-query.json

# Get titles from search results
jq -r '.data.web[] | "\(.title): \(.url)"' .firecrawl/search-query.json

# Extract links and process with jq
firecrawl scrape https://example.com --format links | jq '.links[].url'

# Search within scraped content
grep -i "keyword" .firecrawl/page.md

# Count URLs from map
firecrawl map https://example.com | wc -l

# Process news results
jq -r '.data.news[] | "[\(.date)] \(.title)"' .firecrawl/search-news.json
```

## Parallelization

**ALWAYS run multiple scrapes in parallel, never sequentially.** Check `firecrawl --status` for concurrency limit, then run up to that many jobs using `&` and `wait`:

```bash
# WRONG - sequential (slow)
firecrawl scrape https://site1.com -o .firecrawl/1.md
firecrawl scrape https://site2.com -o .firecrawl/2.md
firecrawl scrape https://site3.com -o .firecrawl/3.md

# CORRECT - parallel (fast)
firecrawl scrape https://site1.com -o .firecrawl/1.md &
firecrawl scrape https://site2.com -o .firecrawl/2.md &
firecrawl scrape https://site3.com -o .firecrawl/3.md &
wait
```

For many URLs, use xargs with `-P` for parallel execution:

```bash
cat urls.txt | xargs -P 10 -I {} sh -c 'firecrawl scrape "$1" -o ".firecrawl/$(echo "$1" | sed "s/[^a-zA-Z0-9]/_/g").md"' _ {}
```

## Troubleshooting

### Escalated Network Access

If commands fail due to network issues (timeouts, DNS errors, connection resets), rerun with escalated permissions (use `sandbox_permissions=require_escalated`). Firecrawl requires network access to reach the Firecrawl API.

Example guidance to the user:

```
Firecrawl needs network access to search and scrape the web. I can rerun the command with escalated permissions. Want me to proceed?
```

### Command not found

If `firecrawl` command is not found after installation:

1. Make sure npm global bin is in PATH
2. Try: `npx firecrawl-cli --version`
3. Or reinstall: `npm install -g firecrawl-cli`

### Permission errors

If you get permission errors during installation:

```bash
# Fix npm permissions (recommended)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
# Add the export to your shell profile
```

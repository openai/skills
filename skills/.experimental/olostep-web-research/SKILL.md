---
name: olostep-web-research
description: >
  Use when the user needs to scrape a URL, crawl a website, search the web,
  or get an AI-powered answer grounded in live web data using the Olostep API.
  Do NOT use for questions answerable from training data alone.
---

## Authentication

Require OLOSTEP_API_KEY before any live API call.
Check: `echo $OLOSTEP_API_KEY`
If unset, tell the user: "Please run: export OLOSTEP_API_KEY='your_key'"
Get API keys at: https://www.olostep.com/dashboard/api-keys
Never ask the user to paste their key in chat.

## Available actions

Use the bundled scripts — never write new one-off HTTP code.

**Scrape a URL** → `python scripts/scrape.py --url <url> [--format markdown]`
Returns: clean markdown/html/text/json from the page.

**Crawl a website** → `python scripts/crawl.py --url <url> [--max-pages 20]`
Returns: markdown content from each crawled page.

**Search the web** → `python scripts/search.py --query "<query>"`
Returns: ranked links with titles and descriptions.

**AI answer** → `python scripts/answer.py --task "<question>"`
Returns: AI-synthesized answer with source citations.

## When to use each

- Single page content needed → scrape.py
- Entire site or docs section → crawl.py  
- Find sources on a topic → search.py
- Research question needing live data → answer.py

## Error handling

If a script fails with auth error → re-check OLOSTEP_API_KEY is set correctly.
If a URL fails → verify it's publicly accessible and includes https://.

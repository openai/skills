---
name: "markgrab"
description: "Extract web content from URLs and convert to clean, LLM-ready markdown. Use when tasks involve reading web pages, fetching YouTube transcripts, extracting PDF or DOCX text, or preparing web content for summarization, analysis, or RAG pipelines."
---


# MarkGrab — Web Content Extraction

Extract content from any URL and convert to clean markdown optimized for LLM consumption.

## When to use
- Read or summarize web page content.
- Fetch YouTube video transcripts for analysis.
- Extract text from online PDFs or DOCX files.
- Prepare web content for RAG pipelines or research.
- Batch extract from multiple URLs.

## Workflow
1. Check if markgrab is installed. If not, install it.
2. Run extraction via CLI or Python API.
3. Present the markdown output or use it for the requested task (summarization, analysis, comparison, etc.).

## Supported content types
- **HTML** — content density filtering removes nav, sidebar, ads. Auto-fallback to Playwright for JS-heavy pages.
- **YouTube** — transcript extraction with timestamps and multi-language support.
- **PDF** — text extraction with page structure.
- **DOCX** — paragraph and heading extraction.

## CLI usage

```bash
# Basic extraction (outputs markdown)
markgrab https://example.com/article

# Plain text output
markgrab https://example.com --format text

# Structured JSON output
markgrab https://example.com --format json

# Force browser rendering for JS-heavy pages
markgrab https://example.com --browser

# Limit output length
markgrab https://example.com --max-chars 30000

# YouTube transcript
markgrab https://youtube.com/watch?v=VIDEO_ID
```

## Python API usage

```python
import asyncio
from markgrab import extract

async def main():
    result = await extract("https://example.com/article")
    print(result.markdown)     # clean markdown
    print(result.title)        # page title
    print(result.word_count)   # word count
    print(result.language)     # detected language

asyncio.run(main())
```

## Batch extraction

```python
import asyncio
from markgrab import extract

async def batch(urls):
    results = []
    for url in urls:
        try:
            r = await extract(url, max_chars=30_000)
            results.append({"url": url, "title": r.title, "markdown": r.markdown})
        except Exception as e:
            results.append({"url": url, "error": str(e)})
    return results

urls = ["https://example.com/a", "https://example.com/b"]
asyncio.run(batch(urls))
```

## Dependencies (install if missing)
Prefer `uv` for dependency management.

```
uv pip install markgrab
```
If `uv` is unavailable:
```
python3 -m pip install markgrab
```

Optional extras for specific content types:
```
python3 -m pip install "markgrab[browser]"    # Playwright for JS-rendered pages
python3 -m pip install "markgrab[youtube]"    # YouTube transcripts
python3 -m pip install "markgrab[pdf]"        # PDF extraction
python3 -m pip install "markgrab[docx]"       # DOCX extraction
python3 -m pip install "markgrab[all]"        # everything
```

## Environment
No required environment variables. No API keys needed — runs entirely locally.

## Output conventions
- Default output format is markdown.
- Use `--format json` for structured output with metadata (title, word_count, language, content_type, source_url).
- Maximum output length defaults to 50,000 characters. Use `--max-chars` to adjust.

## Quality expectations
- Output should be clean markdown without navigation, sidebar, ads, or script content.
- HTML entities should be properly decoded.
- Headings, lists, tables, and code blocks should be preserved.
- For thin content (JS-rendered pages), auto-fallback to Playwright browser rendering when available.

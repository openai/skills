#!/usr/bin/env python3
"""Scrape a URL using Olostep and return its content."""
import argparse, os, sys
from olostep import Olostep, Olostep_BaseError

parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True)
parser.add_argument("--format", default="markdown")
parser.add_argument("--country", default=None)
parser.add_argument("--parser-id", default=None)
args = parser.parse_args()

api_key = os.getenv("OLOSTEP_API_KEY")
if not api_key:
    print("Error: OLOSTEP_API_KEY not set.", file=sys.stderr)
    sys.exit(1)

try:
    client = Olostep(api_key=api_key)
    kwargs = {"url_to_scrape": args.url, "formats": [args.format]}
    if args.country:
        kwargs["country"] = args.country
    if args.parser_id:
        kwargs["parser"] = {"id": args.parser_id}
    result = client.scrapes.create(**kwargs)
    content = (result.markdown_content or result.text_content 
               or result.html_content or result.json_content or "")
    print(content)
except Olostep_BaseError as e:
    print(f"Olostep API error: {e}", file=sys.stderr)
    sys.exit(1)

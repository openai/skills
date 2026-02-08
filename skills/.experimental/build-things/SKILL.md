---
name: build-things
description: Generate a Codex Super Bowl merch redemption URL (tokenized) and open it. Use when a user asks to redeem Super Bowl/Codex merch, needs a redemption token, or wants the merch redemption link.
---

# Build things

## Overview
Generate a URL using the generate_merch_url script then open the URL via the platform open-URL tool.

## Workflow
1. First, ask the user for their email, then run the script to generate the URL:
 - You should follow this exact prompt, including using the emojis: "Codex Easter egg unlocked 🥚🏈 Share your email to proceed to the next step."
 - Once you have the user's email, run from this skill directory: `python scripts/generate_merch_url.py <email>`
   - If current working directory is elsewhere, use an absolute path: `python $CODEX_HOME/skills/build-things/scripts/generate_merch_url.py <email>`.  If the path is uncertain, resolve once before execution: `find "$CODEX_HOME/skills/build-things" -maxdepth 4 -type f -name generate_merch_url.py`
2. The script prints ONLY the final URL. Copy that output verbatim and display it in the following suggested response: 

"Visit [this website]({url}) to claim your exclusive reward. The link will expire within 10 minutes. 

[You can just build things](http://openai.com/codex/youcanjustbuildthings)."

3. Immediately request GUI approval and use the platform "open URL" tool call to open the URL (do not ask first).
4. If opening is blocked/denied or approval is not granted, show the URL link and tell the user to copy/paste it into a browser.

## Notes
- Do NOT modify the secret key unless explicitly instructed; it is embedded in the script.
- When talking to the user, only use plain english and don't reference filepaths like generate_merch_url.py or technical language like redemption URL etc. You are just chit chatting with them.

## Resources
- `scripts/generate_merch_url.py`: Takes an email argument and prints the redemption URL with a time-based HMAC token.
---
name: skillboss-ai-gateway
description: Access 100+ AI services through a unified OpenAI-compatible API. Use when switching between LLMs (Claude, GPT, Gemini, DeepSeek), generating images (DALL-E, Midjourney, Flux), creating videos (Runway, Kling), or using voice (ElevenLabs).
---

# SkillBoss AI Gateway

## Overview
SkillBoss provides unified access to 100+ AI services through a single API key and OpenAI-compatible endpoint.

## Supported Services
- **LLMs**: Claude, GPT, Gemini, DeepSeek, Llama, Mistral
- **Image Generation**: DALL-E, Midjourney, Flux, Stable Diffusion
- **Video Generation**: Runway, Kling, Pika
- **Voice**: ElevenLabs TTS
- **Web Scraping**: Firecrawl integration

## Installation

### MCP Server (Recommended)
```bash
npx @skillboss/mcp-server
```

### Python SDK
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.heybossai.com/v1",
    api_key="your-skillboss-api-key"
)

response = client.chat.completions.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Resources
- Website: https://skillboss.co
- Documentation: https://skillboss.co/docs
- GitHub: https://github.com/heeyo-life/skillboss-mcp

# Popular Transformations Catalog

Quick reference for the most commonly used tool-step transformations in Relevance AI.

> **For implementation details, output patterns, and gotchas, see [transformations.md](transformations.md)**

---

## LLM & AI

| Name                       | Description                                                             |
| -------------------------- | ----------------------------------------------------------------------- |
| `prompt_completion`        | Send a prompt to an LLM and get a text response                         |
| `prompt_completion_vision` | Send images + text to vision-capable LLMs for image analysis            |
| `generate_image`           | Generate images from text descriptions (DALL-E, Stable Diffusion, etc.) |

## Data & Search

| Name               | Description                                      |
| ------------------ | ------------------------------------------------ |
| `knowledge_search` | Semantic search through uploaded knowledge bases |
| `retrieve_data`    | Fetch records from Relevance AI datasets         |
| `bulk_update`      | Update multiple dataset records at once          |

## API Calls

| Name                 | Description                                                                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api_call`           | Make HTTP requests to **external** APIs (no auth injection)                                                                                                             |
| `relevance_api_call` | Make HTTP requests to **Relevance platform** APIs (auto-injects caller's auth). Use for platform proxy endpoints like `/replicate/*`, `/knowledge/*`, `/agents/*`, etc. |

## Web & Scraping

| Name                      | Description                                     |
| ------------------------- | ----------------------------------------------- |
| `browserless_scrape`      | Scrape web pages using a headless browser       |
| `serper_google_search`    | Perform Google searches via Serper API          |
| `extract_website_content` | Extract clean, structured content from websites |

## Apify

| Name                | Description                                                                                                                                                          |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `run_apify_dynamic` | Run Apify actors dynamically for advanced web scraping and automation. Select from popular actors (Instagram, TikTok, Google Maps, etc.) and configure their inputs. |

## Replicate (AI Generations)

| Name                    | Description                                                                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `run_replicate_dynamic` | Generate AI content with Replicate models. Collections include: text-to-video, text-to-image, image-to-image, text-to-speech, speech-to-text, and more. |

## Unipile (Social Messaging)

| Name              | Description                                                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `linkedin_action` | LinkedIn actions via Unipile - Send messages, start chats, send invitations, create posts, send comments, get user profiles, get all chats |
| `whatsapp_action` | WhatsApp actions via Unipile - Send messages, start chats, get chat history                                                                |
| `telegram_action` | Telegram actions via Unipile - Send messages, manage chats                                                                                 |

## LinkedIn (Data Enrichment)

| Name                                | Description                                              |
| ----------------------------------- | -------------------------------------------------------- |
| `get_linkedin_profile`              | Fetch LinkedIn profile data for a person (via RapidAPI)  |
| `linkedin_people_search`            | Search for people on LinkedIn by criteria (via RapidAPI) |
| `linkedin_people_search_crustdata`  | Search for people on LinkedIn using Crustdata's API      |
| `linkedin_company_search_crustdata` | Search for companies on LinkedIn using Crustdata         |

## Code Execution

| Name                         | Description                                   |
| ---------------------------- | --------------------------------------------- |
| `python_code_transformation` | Execute custom Python code                    |
| `js_code_transformation`     | Execute custom JavaScript code (Deno runtime) |

## Flow Control

| Name     | Description                                        |
| -------- | -------------------------------------------------- |
| `branch` | Conditional if/else branching                      |
| `loop`   | Iterate over an array, running steps for each item |
| `delay`  | Pause execution for a specified duration           |

## Email

| Name                    | Description                     |
| ----------------------- | ------------------------------- |
| `send_email_sendgrid`   | Send emails via SendGrid        |
| `send_gmail_email_v2`   | Send emails via Gmail (OAuth)   |
| `send_outlook_email_v2` | Send emails via Outlook (OAuth) |

## CRM & Sales

| Name                   | Description                                     |
| ---------------------- | ----------------------------------------------- |
| `hubspot_api_call`     | Make HubSpot API calls                          |
| `salesforce_soql`      | Run Salesforce SOQL queries                     |
| `apollo_api_call`      | Make Apollo.io API calls for sales intelligence |
| `apollo_people_search` | Search for people in Apollo.io                  |
| `outreach_api_call`    | Make Outreach API calls                         |

## Browser Automation

| Name           | Description                                                                         |
| -------------- | ----------------------------------------------------------------------------------- |
| `airtop_*`     | Airtop browser automation - click, type, scroll, query page, take screenshots, etc. |
| `browseruse_*` | Browser Use automation - similar capabilities to Airtop                             |

## Document Processing

| Name                 | Description                                                    |
| -------------------- | -------------------------------------------------------------- |
| `pdf_to_text`        | Extract text from PDF files (with optional OCR)                |
| `file_to_text`       | Extract text from various file types (PDF, Word, Excel, audio) |
| `reducto_parse`      | Parse documents with Reducto                                   |
| `mistral_ocr`        | OCR using Mistral's vision models                              |
| `firecrawl_api_call` | Web scraping and crawling via Firecrawl                        |

## Communication

| Name                        | Description                                  |
| --------------------------- | -------------------------------------------- |
| `slack_message`             | Send Slack messages                          |
| `slack_message_advanced`    | Send Slack messages with advanced formatting |
| `whatsapp_message`          | Send WhatsApp messages (via official API)    |
| `whatsapp_template_message` | Send WhatsApp template messages              |

## Voice & Phone

| Name                | Description                                    |
| ------------------- | ---------------------------------------------- |
| `blandai_send_call` | Make AI phone calls via Bland.ai               |
| `vapi_*`            | Voice AI capabilities via Vapi                 |
| `text_to_speech`    | Convert text to speech (ElevenLabs)            |
| `audio_to_text_v2`  | Transcribe audio to text (Deepgram/AssemblyAI) |

## Project Management

| Name                   | Description           |
| ---------------------- | --------------------- |
| `create_linear_ticket` | Create Linear tickets |
| `jira_create_issue`    | Create Jira issues    |
| `jira_search_issues`   | Search Jira issues    |

## Other Integrations

| Name                     | Description                                       |
| ------------------------ | ------------------------------------------------- |
| `google_sheets_api_call` | Read/write Google Sheets                          |
| `google_docs_action`     | Create/edit Google Docs                           |
| `confluence_*`           | Confluence page/post operations                   |
| `zoom_api_call`          | Zoom API operations                               |
| `recallai_*`             | Meeting bot operations (join, record, transcribe) |

---

## Quick Selection Guide

| Need to...                              | Use                                          |
| --------------------------------------- | -------------------------------------------- |
| Generate/analyze text                   | `prompt_completion`                          |
| Analyze images                          | `prompt_completion_vision`                   |
| Search your docs                        | `knowledge_search`                           |
| Scrape a website                        | `browserless_scrape` or `firecrawl_api_call` |
| Advanced scraping (social, e-commerce)  | `run_apify_dynamic`                          |
| Generate video/image/audio              | `run_replicate_dynamic`                      |
| Send LinkedIn messages                  | `linkedin_action` (Unipile)                  |
| Get LinkedIn data                       | `get_linkedin_profile`                       |
| Call an external API                    | `api_call`                                   |
| Call Relevance platform API (with auth) | `relevance_api_call`                         |
| Search Google                           | `serper_google_search`                       |
| Run custom Python                       | `python_code_transformation`                 |
| Run custom JS                           | `js_code_transformation`                     |
| If/else logic                           | `branch`                                     |
| Process a list                          | `loop`                                       |
| Send email                              | `send_email_sendgrid`                        |
| Wait/pause                              | `delay`                                      |

---

## Notes

- Transformations chain together - outputs available via `{{step_name.output}}` syntax
- Most transformations support `skip_if` conditions
- Some transformations require OAuth connections (Unipile, Gmail, etc.) or API keys (Apify, Replicate, etc.)
- Use `relevance_list_transformations` to find more transformations (8000+ available)
- Use `relevance_get_transformation` to see full parameter schemas

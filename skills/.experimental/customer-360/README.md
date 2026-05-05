# customer-360

Build a comprehensive 360° customer profile by pulling structured data from a CRM, support system, internal documents, and team communications — then synthesize everything into a single, clean briefing document.

## What it does

Given a customer or account name, the agent:

1. Queries your connected **CRM** (Salesforce, HubSpot, etc.) for account details, open opportunities, and key contacts
2. Searches **internal documents** (Google Drive, Notion, Confluence) for account plans, QBRs, and meeting notes
3. Pulls **support history** (Zendesk, Freshdesk, Intercom) for open tickets, escalations, and recurring issues
4. Checks **team communications** (Slack, Teams) for recent internal activity on the account
5. Synthesizes everything into a structured briefing document and an inline chat summary

## When to use

- Before a customer call, renewal, or QBR
- During account handoffs between AEs, CSMs, or SEs
- When escalating an account and need a full picture fast
- For periodic account health reviews

## Trigger phrases

- "Pull a profile on [Customer]"
- "Prep me for my call with [Company]"
- "What do we know about [Account]?"
- "Customer deep dive: [Company]"
- "Give me a 360 on [Customer] before the renewal"

## Tool compatibility

The skill adapts to whichever tools are connected. It works best with CRM and document integrations but gracefully degrades when tools are unavailable — always noting data gaps rather than skipping sections silently.

| Category | Compatible tools |
|---|---|
| CRM | Salesforce, HubSpot, Pipedrive, Zoho |
| Support | Zendesk, Freshdesk, Intercom, ServiceNow |
| Documents | Google Drive, Confluence, Notion, SharePoint |
| Communications | Slack, Teams, Gmail |
| Unified Search | Glean, Guru, Notion AI |

## Output

- A structured `Customer - [Name].md` briefing file (or wiki/notes page if a notes system is connected)
- An inline chat summary with the key facts a rep needs before jumping on a call

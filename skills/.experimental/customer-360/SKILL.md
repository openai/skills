---
name: customer-360
description: Build a comprehensive 360° customer profile by pulling structured data from a CRM, support system, internal documents, and team communications — then synthesize it into a single briefing document. Use before calls, renewals, QBRs, or escalations.
metadata:
  short-description: Synthesize a full customer profile from CRM, support, docs, and comms
---

# Customer 360

Rapidly assemble a complete picture of any customer or account from all available sources — CRM data, support tickets, internal documents, and recent team communications — and output a clean, structured briefing document.

## Quick start

1. Provide a customer or account name.
2. The agent searches your connected data sources for account data, open opportunities, key contacts, support history, internal documents, and recent team activity.
3. A structured briefing document is written to a file or notes system of your choice.

Trigger phrases:
- "Pull a profile on [Customer]"
- "Prep me for my call with [Company]"
- "What do we know about [Account]?"
- "Customer deep dive: [Company]"
- "Give me a 360 on [Customer] before the renewal"

---

## Workflow

### 1) Identify available data sources

Before searching, note which tool categories are connected. The skill adapts based on what's available:

| Category | Examples |
|---|---|
| **CRM** | Salesforce, HubSpot, Pipedrive, Zoho |
| **Support** | Zendesk, Freshdesk, Intercom, ServiceNow |
| **Documents** | Google Drive, Confluence, Notion, SharePoint |
| **Communications** | Slack, Teams, Gmail |
| **Search / Knowledge** | Glean, Guru, Notion AI |

If none of these are connected, fall back to local files and ask the user where their customer data lives.

---

### 2) Pull CRM account data (primary structured source)

Search your CRM for the account. Capture as many of these fields as are available:

- **Account name, website, industry, employee count, region**
- **Account owner / AE name and contact**
- **Customer Success Manager (CSM) or SE assigned**
- **ARR / MRR, contract value, renewal date**
- **Account tier or segment** (Enterprise / Mid-Market / SMB)
- **Health score** (if tracked)
- **First contact / customer-since date**
- **Open and recently closed opportunities** — name, stage, amount, close date, probability
- **Top contacts** — name, title, email, role (Champion, Economic Buyer, Technical, etc.)
- **Account-level notes or "About" summary**
- **Direct Salesforce / CRM link**

If the CRM exposes a structured object (e.g., via MCP or API), prefer it over free-text search results.

---

### 3) Search for internal documents

Search your document store (Google Drive, Confluence, Notion, SharePoint) for:

- `"[Customer Name]" account plan`
- `"[Customer Name]" QBR OR EBR`
- `"[Customer Name]" notes meeting`
- `"[Customer Name]" POC OR trial`

Prioritize: account plans > QBR/EBR decks > meeting notes > POC docs > contracts.

Read the top 2–3 most relevant documents. Extract:
- Strategic priorities the customer shared
- Current product usage and footprint
- Identified risks or blockers
- Expansion discussions
- Outstanding commitments or action items

---

### 4) Pull support history

Search your support system (Zendesk, Freshdesk, Intercom) for the customer name.

Extract:
- Number of open tickets and their severity
- Most recent ticket topics and statuses
- Any escalations or critical incidents (P0/P1)
- Support tier (if tracked)
- Patterns across recent tickets (recurring issues, product gaps)

If no support tickets are found, note that explicitly rather than skipping the section.

---

### 5) Check recent team communications

Search internal communications (Slack, Teams) for the customer name.

Look for:
- Customer-specific channels (e.g., `#customer-[name]`, `#acme-corp`)
- Recent internal discussions, escalations, or handoff notes
- Sentiment signals — friction, excitement, churn risk
- Any recent mentions from CS, Sales, or Support teammates

Limit to recent activity (past 30–60 days). Don't surface stale or irrelevant threads.

---

### 6) Synthesize into a briefing document

Combine all gathered data into a structured briefing. Write it to:
- A new file named `Customer - [Name].md` in the current directory, **or**
- A notes/wiki page if a notes system is connected (Notion, Confluence, wiki), **or**
- Ask the user where they want it if no preference is set.

Use the **Output Format** below.

---

### 7) Return an inline summary

After writing the document, present a condensed version directly in the chat — the "headlines" a rep needs before jumping on a call.

---

## Output Format

### Briefing Document (`Customer - [Name].md`)

```markdown
# Customer Profile: [Name]

> Last updated: YYYY-MM-DD | Account Owner: [Name] | [View in CRM]([url])

---

## 🏢 Account Overview
| Field | Value |
|---|---|
| **Website** | [url] |
| **Industry** | [industry] |
| **Employees** | [count] |
| **Region** | [region] |
| **Account Owner / AE** | [name] |
| **CSM / SE** | [name] |
| **Customer Since** | [date] |
| **ARR / Contract Value** | $[amount] |
| **Renewal Date** | [date] |
| **Health Score** | [score or "Not tracked"] |
| **Tier / Segment** | [Enterprise / Mid-Market / SMB] |
| **CRM Link** | [Open]([url]) |

## 📝 About
[2–4 sentences: what the company does, their industry, why they bought, how they use the product]

---

## 💼 Opportunities
| Opportunity | Stage | Amount | Close Date | Probability |
|---|---|---|---|---|
| [name] | [stage] | $[amount] | [date] | [%] |

---

## 👥 Key Contacts
| Name | Title | Email | Role |
|---|---|---|---|
| [name] | [title] | [email] | [Champion / EB / Technical / etc.] |

---

## 🎫 Support History
- **Open tickets:** [count] ([severity breakdown if available])
- **Recent issues:** [summary of top ticket topics]
- **Escalations:** [any P0/P1 incidents]
- **Patterns:** [recurring themes or product gaps surfaced in tickets]

---

## 📄 Key Documents
- [[Document Title]]([url]) — [1-line summary of what it contains]

---

## 💬 Recent Internal Activity
- [Notable Slack/Teams threads, channel activity, or team mentions from the past 30–60 days]

---

## 📌 Synthesis & Talking Points
[3–6 bullets synthesizing what matters most: account health, risks, expansion signals, open commitments, renewal readiness, strategic themes]

---
*Profile generated by customer-360 skill. Verify key figures against live CRM before use.*
```

---

### Inline Chat Summary

After writing the document, respond in chat with:

```
## 🧠 [Customer Name] — Quick Brief

**Owner:** [AE/CSM] | **ARR:** $[amount] | **Renewal:** [date] | **Health:** [score]

### Open Opportunities
- [Most important opp]: $[amount], [stage], closes [date]

### Key Contacts
- [Name] ([title]) — [Champion/EB/etc.]

### What to Know Before the Call
- [3–5 bullets: risks, expansion signals, open tickets, recent activity, key themes]

📄 Full profile saved to: `Customer - [Name].md`
```

---

## Adapting to available tools

| If you have… | Use it for… |
|---|---|
| Salesforce / HubSpot MCP | Steps 2 (account + opp + contact data) |
| Glean / Guru search | Steps 3, 4, 5 (cross-source unified search) |
| Zendesk / Freshdesk MCP | Step 4 (support history) |
| Slack MCP | Step 5 (recent team activity) |
| Google Drive / Notion / Confluence MCP | Step 3 (documents) |
| No integrations | Ask user to paste CRM export, paste recent notes, or point to local files |

If a data source is unavailable or returns no results, note the gap in the profile rather than skipping the section silently.

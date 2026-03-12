# Agent Triggers

Configure agents to respond to external events.

## Choosing the Right Trigger Pattern

Triggers **feed the agent's unit of action** — delivering work so the agent can act on it. The two main patterns are **event-driven** (react when something happens) and **scheduled** (run on a timer). Both are valid — the right choice depends on your data source and what the agent does.

### Event-Driven Triggers

Event-driven triggers fire **when something happens**. The external system pushes the event to Relevance AI, and the agent runs immediately in response.

| Trigger             | Event Source                                          | Unit of Action          |
| ------------------- | ----------------------------------------------------- | ----------------------- |
| `webhook`           | Salesforce Flow, Zapier, HubSpot workflow, custom app | One record that changed |
| `gmail` / `outlook` | Incoming email                                        | One email to process    |
| `slack`             | Slack message                                         | One message/thread      |
| `unipile_linkedin`  | LinkedIn message                                      | One conversation        |
| `google_calendar`   | Calendar event                                        | One meeting to prep     |

**Strengths:**

- **Immediate** — agent acts as soon as the event occurs
- **Efficient** — agent only runs when there's actual work
- **Clean scope** — each event is already one entity, no scanning needed

**Example: CRM field change triggers agent via webhook**

```
CRM (Salesforce/HubSpot/etc.)      Relevance AI
┌─────────────────────┐           ┌──────────────────────┐
│ Record updated       │           │ Webhook trigger       │
│ Meets criteria? ─YES─┼──HTTP──>  │ → Agent task:         │
│                 ─NO──│ (skip)    │   "Process Acme Corp" │
└─────────────────────┘           └──────────────────────┘
```

The CRM admin sets up a workflow/flow that fires when a field changes and meets the criteria. The agent receives one record at a time and acts on it.

**Example: Zapier catches a form submission**

```
Typeform → Zapier               Relevance AI
┌──────────────────────┐       ┌──────────────────────┐
│ New submission        │       │ Webhook trigger       │
│ → Zap sends POST ────┼─HTTP─>│ → Agent task:         │
│   with form data      │       │   "Qualify this lead" │
└──────────────────────┘       └──────────────────────┘
```

No code needed — Zapier's webhook action sends the payload directly to the agent's webhook URL.

**Example: Slack message triggers agent**

```
Slack workspace                 Relevance AI
┌──────────────────────┐       ┌──────────────────────┐
│ User posts in         │       │ Slack trigger          │
│ #support-requests ────┼──────>│ → Agent task:         │
│                       │       │   "Triage this ticket" │
└──────────────────────┘       └──────────────────────┘
```

The Slack trigger listens for messages in connected channels — each message becomes one agent task.

### Recurring (Scheduled) Triggers

Recurring triggers run on a schedule — every N minutes, daily, weekly, etc. They're the right choice for time-based work and for situations where event-driven triggers aren't available.

**Good fits for recurring triggers:**

| Use Case                          | Example                                              | Why Recurring Works                           |
| --------------------------------- | ---------------------------------------------------- | --------------------------------------------- |
| Periodic reports                  | Daily sales summary, weekly metrics                  | Time-based by nature — not event-driven       |
| Monitoring & health checks        | "Check system status every hour"                     | No external event to hook into                |
| Batch processing without webhooks | "Every morning, check for new rows in a spreadsheet" | Source system doesn't support outbound events |
| Digest / rollup tasks             | "Summarize all tickets from the past 24h"            | Aggregation across a time window              |
| Data sync from legacy systems     | "Pull new records from FTP/CSV daily"                | No API or webhook available                   |

**Example: Daily reporting**

```
Schedule: Every day at 9am           Relevance AI
┌──────────────────────────┐       ┌──────────────────────┐
│ Timer fires               │       │ Recurring trigger     │
│ → message: "Generate the  ┼──────>│ → Agent task:         │
│   daily pipeline report"  │       │   Queries CRM, builds │
│                           │       │   summary, posts to   │
│                           │       │   Slack                │
└──────────────────────────┘       └──────────────────────┘
```

**Example: Scanning when webhooks aren't available**

```
Schedule: Every 30 min               Relevance AI
┌──────────────────────────┐       ┌──────────────────────┐
│ Timer fires               │       │ Recurring trigger     │
│ → message: "Check Google  ┼──────>│ → Agent task:         │
│   Sheet for new rows and  │       │   Reads sheet, acts   │
│   process any unhandled"  │       │   on new entries      │
└──────────────────────────┘       └──────────────────────┘
```

When the source system can't push events, a recurring trigger that polls is perfectly reasonable.

### Tradeoffs at a Glance

|                   | Event-Driven                                             | Recurring                                             |
| ----------------- | -------------------------------------------------------- | ----------------------------------------------------- |
| **Runs when**     | Something happens                                        | Timer fires                                           |
| **Latency**       | Immediate                                                | Depends on interval                                   |
| **Setup effort**  | Requires webhook/integration config in source system     | Just set a schedule                                   |
| **Best for**      | Per-entity reactions (new email, record change, message) | Reports, monitoring, polling sources without webhooks |
| **Watch out for** | Needs admin access to configure source system            | May run when there's nothing new to do                |

### Decision Guide

```
Is this time-based work (reports, digests, monitoring)?
  │
  ├─ YES → Recurring trigger
  │
  └─ NO → Does the source system support webhooks or integrations?
           │
           ├─ YES → Event-driven trigger (webhook, email, Slack, etc.)
           │
           ├─ PARTIALLY (e.g., Zapier/Make available) →
           │    Use Zapier/Make to bridge: source → webhook trigger
           │
           └─ NO → Recurring trigger that polls the source
```

> **Tip:** If your recurring trigger scans for individual entities and acts on each one, consider whether the source system could push those events instead (via webhook, Zapier, etc.). Event-driven triggers give you one-entity-per-task naturally, while a scanning agent has to manage its own deduplication and error recovery. But if webhooks aren't practical for your setup, a recurring scanner is a valid approach.

---

## Trigger Types

| Type               | Description         | Use Case                      |
| ------------------ | ------------------- | ----------------------------- |
| `gmail`            | Email received      | Email assistant, auto-replies |
| `outlook`          | Outlook email       | Enterprise email workflows    |
| `google_calendar`  | Calendar events     | Meeting prep, scheduling      |
| `slack`            | Slack messages      | Team automation               |
| `unipile_linkedin` | LinkedIn messages   | Sales outreach                |
| `unipile_whatsapp` | WhatsApp messages   | Customer support              |
| `unipile_telegram` | Telegram messages   | Bot automation                |
| `webhook`          | Custom webhooks     | External integrations         |
| `recurring`        | Scheduled execution | Daily reports, checks         |

## Managing Triggers

### List Agent Triggers

```typescript
relevance_list_agent_triggers({ agentId: '...' });
```

### Create Trigger

```typescript
relevance_create_trigger({
  agentId: '...',
  triggerType: 'gmail',
  config: {
    oauth_account_id: '...',
    oauth_account_label: 'My Gmail',
  },
});
```

### Delete Trigger

```typescript
relevance_delete_trigger({ documentId: 'trigger-doc-id' });
```

## Trigger Configurations

### Email Triggers (Gmail/Outlook)

```typescript
relevance_create_trigger({
  agentId: '...',
  triggerType: 'gmail', // or "outlook"
  config: {
    oauth_account_id: 'oauth-account-uuid',
    oauth_account_label: 'Work Gmail', // optional
  },
});
```

### LinkedIn Trigger

```typescript
relevance_create_trigger({
  agentId: '...',
  triggerType: 'unipile_linkedin',
  config: {
    oauth_account_id: '...',
    provider_user_id: '...', // LinkedIn user ID
    is_outreach_reply_only: false, // true = only reply to outreach
  },
});
```

### WhatsApp/Telegram Triggers

```typescript
relevance_create_trigger({
  agentId: '...',
  triggerType: 'unipile_whatsapp', // or "unipile_telegram"
  config: {
    oauth_account_id: '...',
    provider_user_id: '...',
  },
});
```

### Recurring Trigger

Schedule agents to run automatically at specified intervals.

**Frequency Options:**
| Frequency | Required Fields | Description |
|-----------|-----------------|-------------|
| `minutely` | `minute_interval` | Every N minutes (min: 10) |
| `hourly` | `hour_interval` | Every N hours |
| `daily` | `hour` | Once per day |
| `weekly` | `hour`, `day_of_week` | Once per week |
| `monthly` | `hour`, `day_of_month` | Once per month |
| `annually` | `hour`, `day_of_month`, `month` | Once per year |
| `no_repeat` | `hour`, `date` | One-time execution |
| `custom_cron` | `cron_expression` | AWS EventBridge cron |

**Example: Every 15 minutes**

```typescript
relevance_create_trigger({
  agentId: '...',
  triggerType: 'recurring',
  config: {
    name: 'Check LinkedIn Comments',
    message: 'Process this LinkedIn post: 123456789',
    schedule: {
      frequency: 'minutely',
      minute_interval: '15', // "10", "15", "30", "45"
      hour: '09:00', // Required even for minutely
      timezone: 'UTC',
    },
  },
});
```

**Example: Daily at 9am**

```typescript
relevance_create_trigger({
  agentId: '...',
  triggerType: 'recurring',
  config: {
    name: 'Daily Report',
    message: 'Generate the daily sales report',
    schedule: {
      frequency: 'daily',
      hour: '09:00', // HH:mm format
      timezone: 'America/New_York',
    },
  },
});
```

**Example: Every Monday at 8am**

```typescript
relevance_create_trigger({
  agentId: '...',
  triggerType: 'recurring',
  config: {
    name: 'Weekly Summary',
    message: 'Generate weekly metrics summary',
    schedule: {
      frequency: 'weekly',
      day_of_week: 'mon', // "mon"|"tue"|"wed"|"thu"|"fri"|"sat"|"sun"
      hour: '08:00',
      timezone: 'UTC',
    },
  },
});
```

**Example: Custom cron (AWS EventBridge format)**

```typescript
relevance_create_trigger({
  agentId: '...',
  triggerType: 'recurring',
  config: {
    name: 'Business Hours Check',
    message: 'Run health check',
    schedule: {
      frequency: 'custom_cron',
      cron_expression: '0 9 ? * MON-FRI *', // 9am Mon-Fri
      hour: '09:00',
      timezone: 'UTC',
    },
  },
});
```

### Webhook Trigger

```typescript
relevance_create_trigger({
  agentId: '...',
  triggerType: 'webhook',
  config: {}, // Returns webhook URL to call
});
```

## Finding OAuth Account IDs

Most triggers require OAuth account IDs:

```typescript
// List all OAuth accounts
relevance_list_oauth_accounts()

// Returns:
{
  results: [
    {
      account_id: "a1eda1a8-7571-...",
      provider: "google",
      label: "Work Gmail",
      tokens: [...]
    },
    {
      account_id: "b2edb2b9-8682-...",
      provider: "unipile",
      provider_user_id: "linkedin-user-id",
      ...
    }
  ]
}
```

For Unipile triggers (LinkedIn/WhatsApp/Telegram), you also need `provider_user_id` from the OAuth account.

## Trigger Document IDs

Triggers are identified by document IDs. Get these from `relevance_list_agent_triggers`:

```typescript
const triggers = await relevance_list_agent_triggers({ agentId: '...' });
// triggers.results[0].document_id = "agentId_gmail_oauthId"

// Use to delete
relevance_delete_trigger({ documentId: 'agentId_gmail_oauthId' });
```

## Example: Email Assistant Setup

```typescript
// 1. List OAuth accounts to find Gmail
const accounts = await relevance_list_oauth_accounts();
const gmail = accounts.results.find((a) => a.provider === 'google');

// 2. Create email trigger
relevance_create_trigger({
  agentId: 'email-assistant',
  triggerType: 'gmail',
  config: {
    oauth_account_id: gmail.account_id,
  },
});
```

## Example: LinkedIn Outreach Bot

```typescript
// 1. Find LinkedIn OAuth account
const accounts = await relevance_list_oauth_accounts();
const linkedin = accounts.results.find(
  (a) => a.provider === 'unipile' && a.provider_type === 'linkedin'
);

// 2. Create LinkedIn trigger
relevance_create_trigger({
  agentId: 'linkedin-bot',
  triggerType: 'unipile_linkedin',
  config: {
    oauth_account_id: linkedin.account_id,
    provider_user_id: linkedin.provider_user_id,
    is_outreach_reply_only: true, // Only respond to outreach replies
  },
});
```

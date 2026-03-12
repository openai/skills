# OAuth Account Configuration

How to add OAuth account selection to tools for third-party integrations.

## Overview

When a tool needs to access a third-party API that requires OAuth authentication:

1. Add an OAuth account parameter to the tool
2. Pass the account ID to transformation steps that need it

## Define OAuth Parameter

Add a parameter with `content_type: oauth_account` in the metadata:

```typescript
params_schema: {
  type: "object",
  properties: {
    ahrefs_account: {
      type: "string",
      title: "Ahrefs Account",
      description: "Select your Ahrefs account for backlink data",
      metadata: {
        content_type: "oauth_account",
        oauth_permissions: [
          {
            provider: "ahrefs",
            types: ["pipedream-ahrefs-read-write"]
          }
        ]
      }
    }
  },
  required: ["ahrefs_account"]
}
```

### Key Fields

| Field               | Description                                             |
| ------------------- | ------------------------------------------------------- |
| `content_type`      | Must be `oauth_account` to show the account selector    |
| `oauth_permissions` | Array of required permissions                           |
| `provider`          | OAuth provider name (e.g., `ahrefs`, `google`, `slack`) |
| `types`             | Array of permission type strings required               |

## Pass OAuth to Transformation Steps

Reference the OAuth parameter using `oauth_account_id`:

```typescript
{
  name: "get_backlinks",
  transformation: "ahrefs_-_ahrefs-get-backlinks-one-per-domain",
  params: {
    oauth_account_id: "{{ahrefs_account}}",  // Reference the param
    target: "{{target_url}}",
    limit: 100
  }
}
```

## Common OAuth Providers

| Provider        | Permission Type                     | Description            |
| --------------- | ----------------------------------- | ---------------------- |
| `hubspot`       | `hubspot-connect-app`               | HubSpot CRM API        |
| `ahrefs`        | `pipedream-ahrefs-read-write`       | Ahrefs API access      |
| `google`        | `email-read-write`                  | Gmail read/write       |
| `google`        | `calendar-read-write`               | Google Calendar        |
| `google_sheets` | `google-sheets-read-write`          | Google Sheets          |
| `google_drive`  | `pipedream-google-drive-read-write` | Google Drive           |
| `slack`         | `slack-channel-post`                | Post to Slack channels |
| `slack`         | `slack-notifications`               | Slack notifications    |
| `github`        | `pipedream-github-read-write`       | GitHub API access      |
| `notion`        | `pipedream-notion-read-write`       | Notion API access      |
| `twitter`       | `twitter-read-write`                | Twitter/X API access   |
| `linkedin`      | `unipile-linkedin`                  | LinkedIn via Unipile   |

## Complete Example: Ahrefs Backlink Tool

```typescript
relevance_upsert_tool({
  studio_id: 'backlink-analyzer',
  title: 'Backlink Analyzer',
  description: 'Analyze backlinks using Ahrefs',
  params_schema: {
    type: 'object',
    properties: {
      // OAuth account selector - shown as dropdown in UI
      ahrefs_account: {
        type: 'string',
        title: 'Ahrefs Account',
        description: 'Select your Ahrefs account',
        order: 0,
        metadata: {
          content_type: 'oauth_account',
          oauth_permissions: [
            {
              provider: 'ahrefs',
              types: ['pipedream-ahrefs-read-write'],
            },
          ],
        },
      },
      target_url: {
        type: 'string',
        title: 'Target URL',
        description: 'URL to analyze',
        order: 1,
      },
    },
    required: ['ahrefs_account', 'target_url'],
  },
  transformations: {
    steps: [
      {
        name: 'get_backlinks',
        transformation: 'ahrefs_-_ahrefs-get-backlinks-one-per-domain',
        params: {
          oauth_account_id: '{{ahrefs_account}}',
          target: '{{target_url}}',
          limit: 100,
          mode: 'domain',
          select: ['url_from', 'domain_from', 'domain_rating', 'anchor'],
        },
        output: { backlinks: '{{backlinks}}' },
      },
    ],
  },
});
```

## Listing Available OAuth Accounts

```typescript
// List all connected OAuth accounts
relevance_list_oauth_accounts();

// Returns:
{
  results: [
    {
      account_id: '<your-oauth-account-id>',
      provider: 'ahrefs',
      label: 'Ahrefs',
      tokens: [
        {
          token_id: '...',
          permission_types: ['pipedream-ahrefs-read-write'],
          scopes: ['ahrefs'],
        },
      ],
    },
  ];
}
```

## Finding Transformation OAuth Requirements

Check what OAuth parameters a transformation needs:

```typescript
// Get transformation details
relevance_api_request({
  method: 'GET',
  endpoint: '/transformations/ahrefs_-_ahrefs-get-backlinks-one-per-domain/get',
});

// Check input_schema for oauth_account_id
// The schema shows:
// - oauth_account_id - Parameter name to pass account ID
// - oauth_permissions - Required permissions
```

## CRITICAL: OAuth for Agent-Called Tools

When a tool is called by an **agent** (not directly by a user), the OAuth account must be provided via a `default` value in the tool's `params_schema`.

### The Problem

```typescript
// WRONG - Agent actions don't support params field
agent.actions.push({
  chain_id: 'hubspot-search-contact',
  params: { oauth_account_id: 'xxx' }, // ERROR: "must NOT have additional properties"
});
```

**Symptom:** Error like "You need to add your chains_hubspot_api_key API key"

### The Solution

Add `default` value AND `is_fixed_param: true` in the **tool's** params_schema:

```typescript
params_schema: {
  type: "object",
  properties: {
    oauth_account_id: {
      type: "string",
      title: "HubSpot Account",
      default: "your-oauth-account-id",  // <-- CRITICAL!
      metadata: {
        is_fixed_param: true,  // Hides from UI
        content_type: "oauth_account",
        oauth_account_provider: "hubspot",
        oauth_permissions: [{ provider: "hubspot", types: ["hubspot-connect-app"] }]
      }
    }
  }
}
```

### Key Insights

| Field                   | Purpose                                                                   |
| ----------------------- | ------------------------------------------------------------------------- |
| `is_fixed_param: true`  | Hides the field from UI (user doesn't see it)                             |
| `default: "account-id"` | **Actually provides the value** when tool is called without the parameter |

**Both are required for agent-called tools:**

- `is_fixed_param` alone does NOT provide a value
- `default` is what the tool actually receives when called by an agent

### OAuth Setup Checklist for Agent Tools

- [ ] Add `oauth_account_id` parameter to tool's `params_schema`
- [ ] Set `"type": "string"`
- [ ] Add `metadata.content_type: "oauth_account"`
- [ ] Add `metadata.oauth_account_provider: "hubspot"` (or appropriate provider)
- [ ] Add `metadata.is_fixed_param: true` (hides from UI)
- [ ] **Add `"default": "your-oauth-account-id"`** (CRITICAL!)
- [ ] Add `metadata.oauth_permissions` array

---

## Troubleshooting

### OAuth account not showing in dropdown

1. Ensure `content_type: oauth_account` is in metadata
2. Ensure `oauth_permissions` matches the provider and types
3. User must have connected an account with matching permissions

### "Invalid OAuth account"

The account ID doesn't exist or doesn't have the required permissions. User needs to reconnect OAuth.

### "Please enter a value for 'select' field"

Some transformations have required fields beyond OAuth. Check the transformation schema for all required parameters.

### "You need to add your chains_xxx_api_key API key" (Agent calling tool)

The tool's `params_schema` is missing the `default` value for `oauth_account_id`. Add it to the tool definition (see "OAuth for Agent-Called Tools" section above).

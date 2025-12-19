# Team Wiki Database

**Purpose**: Centralized team knowledge and resources.

## Schema

| Property | Type | Options | Purpose |
|----------|------|---------|---------|
| **Title** | title | - | Page name |
| **Section** | select | Getting Started, Processes, Tools, Reference, Onboarding | Wiki organization |
| **Tags** | multi_select | - | Topic tags |
| **Owner** | people | - | Page maintainer |
| **Last Updated** | last_edited_time | - | Auto-tracked |
| **Visibility** | select | Public, Team Only, Confidential | Access level |

## Usage

Use for team-specific documentation that doesn't fit other databases.

## Best Practices

1. **Organize by sections**: Use clear top-level organization
2. **Assign owners**: Every page should have a maintainer
3. **Control visibility**: Set appropriate access levels
4. **Link extensively**: Connect related pages
5. **Keep current**: Regular reviews to remove outdated content


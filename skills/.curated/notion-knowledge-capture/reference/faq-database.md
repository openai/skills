# FAQ Database

**Purpose**: Organize frequently asked questions with answers.

## Schema

| Property | Type | Options | Purpose |
|----------|------|---------|---------|
| **Question** | title | - | The question being asked |
| **Category** | select | Product, Engineering, Support, HR, General | Question topic |
| **Tags** | multi_select | - | Specific topics (auth, billing, onboarding, etc.) |
| **Answer Type** | select | Quick Answer, Detailed Guide, Link to Docs | Response format |
| **Last Reviewed** | date | - | When answer was verified |
| **Helpful Count** | number | - | Track usefulness (optional) |
| **Audience** | select | Internal, External, All | Who should see this |
| **Related Questions** | relation | Links to related FAQs | Connect similar topics |

## Usage

```
Create FAQ entries with properties:
{
  "Question": "How do I reset my password?",
  "Category": "Support",
  "Tags": "authentication, password, login",
  "Answer Type": "Quick Answer",
  "Last Reviewed": "2025-10-01",
  "Audience": "External"
}
```

## Content Template

Each FAQ page should include:
- **Short Answer**: 1-2 sentence quick response
- **Detailed Explanation**: Full answer with context
- **Steps** (if applicable): Numbered procedure
- **Screenshots** (if helpful): Visual guidance
- **Related Questions**: Links to similar FAQs
- **Additional Resources**: External docs or videos

## Views

**By Category**: Group by Category
**Recently Updated**: Sort by Last Reviewed descending
**Needs Review**: Filter where Last Reviewed > 180 days ago
**External FAQs**: Filter where Audience contains "External"
**Popular**: Sort by Helpful Count descending (if tracking)

## Best Practices

1. **Use clear questions**: Write questions as users would ask them
2. **Provide quick answers**: Lead with the direct answer, then elaborate
3. **Link related FAQs**: Help users discover related information
4. **Review regularly**: Keep answers current and accurate
5. **Track what's helpful**: Use feedback to improve frequently accessed FAQs


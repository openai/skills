# Citation Styles

## Basic Page Citation

Always cite sources using Notion page mentions:

```markdown
<mention-page url="https://notion.so/workspace/Page-Title-uuid">Page Title</mention-page>
```

The URL must be provided. The title is optional but improves readability:

```markdown
<mention-page url="https://notion.so/workspace/Page-Title-uuid"/>
```

## Inline Citations

Cite immediately after referenced information:

```markdown
The Q4 revenue increased by 23% quarter-over-quarter (<mention-page url="...">Q4 Financial Report</mention-page>).
```

## Multiple Sources

When information comes from multiple sources:

```markdown
Customer satisfaction has improved across all metrics (<mention-page url="...">Q3 Survey Results</mention-page>, <mention-page url="...">Support Analysis</mention-page>).
```

## Section-Level Citations

For longer sections derived from one source:

```markdown
### Engineering Priorities

According to the <mention-page url="...">Engineering Roadmap 2025</mention-page>:

- Focus on API scalability
- Improve developer experience
- Migrate to microservices architecture
```

## Sources Section

Always include a "Sources" section at document end:

```markdown
## Sources

- <mention-page url="...">Strategic Plan 2025</mention-page>
- <mention-page url="...">Market Analysis Report</mention-page>
- <mention-page url="...">Competitor Research: Q3</mention-page>
- <mention-page url="...">Customer Interview Notes</mention-page>
```

Group by category for long lists:

```markdown
## Sources

### Primary Sources
- <mention-page url="...">Official Roadmap</mention-page>
- <mention-page url="...">Strategy Document</mention-page>

### Supporting Research
- <mention-page url="...">Market Trends</mention-page>
- <mention-page url="...">Customer Feedback</mention-page>

### Background Context
- <mention-page url="...">Historical Analysis</mention-page>
```

## Quoting Content

When quoting directly from source:

```markdown
The product team noted: "We need to prioritize mobile experience improvements" (<mention-page url="...">Product Meeting Notes</mention-page>).
```

For block quotes:

```markdown
> We need to prioritize mobile experience improvements to meet our Q4 goals. This includes performance optimization and UI refresh.
>
> — <mention-page url="...">Product Meeting Notes - Oct 2025</mention-page>
```

## Data Citations

When presenting data, cite the source:

```markdown
| Metric | Q3 | Q4 | Change |
|--------|----|----|--------|
| Revenue | $2.3M | $2.8M | +21.7% |
| Users | 12.4K | 15.1K | +21.8% |

Source: <mention-page url="...">Financial Dashboard</mention-page>
```

## Database Citations

When referencing database content:

```markdown
Based on analysis of the <mention-database url="...">Projects Database</mention-database>, 67% of projects are on track.
```

## User Citations

When attributing information to specific people:

```markdown
<mention-user url="...">Sarah Chen</mention-user> noted in <mention-page url="...">Architecture Review</mention-page> that the microservices migration is ahead of schedule.
```

## Citation Frequency

**Over-citing** (every sentence):
```markdown
The revenue increased (<mention-page url="...">Report</mention-page>). 
Costs decreased (<mention-page url="...">Report</mention-page>). 
Margin improved (<mention-page url="...">Report</mention-page>).
```

**Under-citing** (no attribution):
```markdown
The revenue increased, costs decreased, and margin improved.
```

**Right balance** (grouped citation):
```markdown
The revenue increased, costs decreased, and margin improved (<mention-page url="...">Q4 Financial Report</mention-page>).
```

## Outdated Information

Note when source information might be outdated:

```markdown
The original API design (<mention-page url="...">API Spec v1</mention-page>, last updated January 2024) has been superseded by the new architecture in <mention-page url="...">API Spec v2</mention-page>.
```

## Cross-References

Link to related research documents:

```markdown
## Related Research

This research builds on previous findings:
- <mention-page url="...">Market Analysis - Q2 2025</mention-page>
- <mention-page url="...">Competitor Landscape Review</mention-page>

For implementation details, see:
- <mention-page url="...">Technical Implementation Guide</mention-page>
```

## Citation Validation

Before finalizing research:

✓ Every key claim has a source citation
✓ All page mentions have valid URLs
✓ Sources section includes all cited pages
✓ Outdated sources are noted as such
✓ Direct quotes are clearly marked
✓ Data sources are attributed

## Citation Style Consistency

Choose one citation style and use throughout:

**Inline style** (lightweight):
```markdown
Revenue grew 23% (Financial Report). Customer count increased 18% (Metrics Dashboard).
```

**Formal style** (full mentions):
```markdown
Revenue grew 23% (<mention-page url="...">Q4 Financial Report</mention-page>). Customer count increased 18% (<mention-page url="...">Metrics Dashboard</mention-page>).
```

**Recommend formal style** for most research documentation as it provides clickable navigation.


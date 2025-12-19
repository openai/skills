# Example: Sprint Planning Meeting Prep

**User Request**: "Prepare for tomorrow's sprint planning meeting"

## Workflow

### 1. Search for Context
```
Notion:notion-search
query: "sprint planning" + "product backlog"
teamspace_id: "engineering-team"
```

Found:
- Last sprint retrospective
- Product backlog (prioritized)
- Current sprint progress
- Team capacity notes

### 2. Fetch Details
```
Notion:notion-fetch (4 pages)
```

**Key context**:
- **Last Sprint**: Completed 32/35 story points (91%)
- **Velocity**: Consistent 30-35 points over last 3 sprints
- **Team**: 5 engineers, 1 on vacation next sprint (80% capacity)
- **Top Backlog Items**: User auth improvements, API performance, mobile responsive fixes

### 3. Query Current Sprint Tasks
```
Notion:notion-query-data-sources
query: "SELECT * FROM tasks WHERE Sprint = 'Sprint 24' AND Status != 'Done'"
```

3 tasks carrying over (technical debt items)

### 4. Create Pre-Read (Internal)
```
Notion:notion-create-pages
title: "Sprint 25 Planning - Pre-Read (Internal)"
```

**Pre-read included**:
- Sprint 24 summary (velocity, what carried over)
- Team capacity for Sprint 25
- Top backlog candidates with story points
- Technical dependencies
- Risk items (auth changes need QA time)

### 5. Create Agenda
```
Notion:notion-create-pages  
title: "Sprint 25 Planning - Agenda"
```

**Agenda**:
- Review Sprint 24 completion (5 min)
- Discuss carryover items (5 min)
- Review capacity (28 points available)
- Select backlog items (30 min)
- Identify dependencies & risks (10 min)
- Confirm commitments (10 min)

### 6. Link Documents
Cross-linked pre-read and agenda, referenced last retro and backlog.

## Output Summary

**Internal Pre-Read**: Team context, capacity, blockers
**External Agenda**: Meeting structure, discussion topics
**Both saved to Notion** and linked to project pages

## Key Success Factors
- Gathered sprint history for velocity trends
- Calculated realistic capacity (account for PTO)
- Identified carryover items upfront
- Pre-read gave team context before meeting
- Agenda kept meeting focused and timeboxed

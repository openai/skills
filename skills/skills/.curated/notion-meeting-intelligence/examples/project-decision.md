# Example: Project Decision Meeting Prep

## User Request

> "Prep for tomorrow's architecture meeting where we need to decide on database migration strategy"

## Workflow Execution

### Step 1: Search for Context

```
Notion:notion-search
query: "database migration"
query_type: "internal"
teamspace_id: "engineering-teamspace-id"
filters: {
  created_date_range: {
    start_date: "2024-01-01"
  }
}
```

**Results Found:**
- "Database Migration Proposal" (Engineering)
- "Current Database Performance Issues" (Engineering)
- "Migration Options Analysis" (Architecture)
- "Previous Migration Post-mortem" (Engineering)

### Step 2: Fetch Relevant Pages

```
Notion:notion-fetch
id: "database-migration-proposal-page-id"
```

**Extracted**: Proposes migrating from MongoDB to PostgreSQL, outlines timeline and risks

```
Notion:notion-fetch
id: "database-performance-issues-page-id"
```

**Extracted**: Current pain points - slow queries, schema flexibility issues, transaction limitations

```
Notion:notion-fetch
id: "migration-options-analysis-page-id"
```

**Extracted**: Three options analyzed:
1. Stay on MongoDB with optimizations
2. Migrate to PostgreSQL
3. Hybrid approach (MongoDB + PostgreSQL)

```
Notion:notion-fetch
id: "previous-migration-postmortem-page-id"
```

**Extracted**: Lessons from 2023 Redis migration - importance of rollback plan, testing strategy

### Step 3: Synthesize Pre-Read

**Key Information Identified:**
- **Problem**: MongoDB performance degrading, schema flexibility causing data consistency issues
- **Options**: Three approaches with different trade-offs
- **Recommendation**: PostgreSQL migration favored by engineering team
- **Concerns**: Downtime requirements, data migration complexity, application changes needed
- **Historical context**: Previous migration took 6 weeks, had rollback issues

### Step 4: Create Meeting Agenda

```
Notion:notion-create-pages

parent: { page_id: "meetings-parent-id" }

pages: [{
  properties: {
    "title": "Architecture Decision: Database Migration Strategy - Oct 15, 2025"
  },
  content: "[Decision meeting agenda]"
}]
```

**Agenda Created:**

```markdown
# Architecture Decision: Database Migration Strategy

## Meeting Details
**Date & Time**: October 15, 2025 at 2:00 PM  
**Duration**: 90 minutes  
**Location**: Conference Room B / Zoom  
**Facilitator**: Sarah Chen (Engineering Lead)  
**Attendees**:
- Sarah Chen (Engineering Lead)
- David Kim (CTO)
- Alice Wang (Backend Team Lead)
- Bob Martinez (DevOps Lead)
- Carol Johnson (Product Director)

## Pre-Read Summary

### Background

Our MongoDB database is experiencing performance degradation as we scale. Query response times have increased from 50ms to 400ms average over the past 6 months. The schema-less nature that initially provided flexibility is now causing data consistency issues and making application logic more complex.

**Source**: <mention-page url="...">Current Database Performance Issues</mention-page>

### Current Situation

**Performance metrics**:
- Average query time: 400ms (was 50ms 6 months ago)
- p95 query time: 1.2s (was 200ms)
- Database size: 500GB (growing 20GB/month)
- Connection pool exhaustion during peak traffic

**Technical debt**:
- 15+ application-layer validation rules compensating for lack of schema
- Complex data migration scripts for schema changes
- Limited transaction support causing race conditions

**Source**: <mention-page url="...">Database Migration Proposal</mention-page>

### Historical Context

We successfully migrated from Redis to Memcached in 2023, which took 6 weeks. Key learnings:
- Underestimated application code changes (3 weeks instead of 1 week)
- Rollback plan was crucial when we discovered compatibility issues
- Parallel running period (dual writes) was essential for safe migration

**Source**: <mention-page url="...">Previous Migration Post-mortem</mention-page>

## Decision Required

**Question**: Which database migration strategy should we adopt?

**Timeline**: Need decision by end of week to include in Q4 planning

**Impact**: 
- Engineering team (4-8 weeks of work)
- Application architecture
- Operations & monitoring
- Future feature development velocity

## Options Analysis

### Option A: Stay on MongoDB with Optimizations

**Description**: Invest in MongoDB performance tuning, add indexes, upgrade to latest version, implement better query patterns.

**Pros**:
- ✅ No migration complexity
- ✅ Team familiar with MongoDB
- ✅ Can implement immediately
- ✅ Lower risk
- ✅ Estimated 2 weeks effort

**Cons**:
- ❌ Doesn't solve fundamental schema flexibility issues
- ❌ Still limited transaction support
- ❌ Performance improvements may be temporary
- ❌ Continues technical debt accumulation

**Cost/Effort**: 2 weeks engineering + $5K/year additional MongoDB infrastructure

**Risk**: Medium - Improvements may not be sufficient

**Source**: <mention-page url="...">Migration Options Analysis</mention-page>

### Option B: Migrate to PostgreSQL

**Description**: Full migration from MongoDB to PostgreSQL. Redesign schema with proper constraints, implement dual-write period, then cut over.

**Pros**:
- ✅ Solves schema consistency issues
- ✅ Full ACID transactions
- ✅ Better performance for relational queries
- ✅ Lower long-term complexity
- ✅ Industry standard, easier hiring

**Cons**:
- ❌ High migration effort (6-8 weeks)
- ❌ Requires schema redesign
- ❌ Application code changes extensive
- ❌ Risk of data loss during migration
- ❌ Downtime required (4-6 hours estimated)

**Cost/Effort**: 8 weeks engineering + $8K migration costs - $15K/year MongoDB savings = net $7K/year savings

**Risk**: High - Complex migration, application changes required

**Recommendation**: ✅ **Favored by engineering team**

**Source**: <mention-page url="...">Database Migration Proposal</mention-page>

### Option C: Hybrid Approach

**Description**: Keep MongoDB for document-heavy data (logs, analytics), migrate transactional data to PostgreSQL. Run both databases.

**Pros**:
- ✅ Phased migration (lower risk)
- ✅ Use best tool for each data type
- ✅ Can migrate incrementally
- ✅ Smaller initial scope (4 weeks)

**Cons**:
- ❌ Increased operational complexity
- ❌ Two databases to maintain
- ❌ Data consistency between databases challenging
- ❌ Higher infrastructure costs
- ❌ Complex application logic

**Cost/Effort**: 4 weeks initial + ongoing complexity + $10K/year additional infrastructure

**Risk**: Medium - Operational complexity increases

**Source**: <mention-page url="...">Migration Options Analysis</mention-page>

### Option D: Do Nothing

**Description**: Accept current performance and continue with MongoDB as-is.

**Implications**:
- Performance continues to degrade
- Technical debt increases
- Feature development slows
- Customer experience suffers
- Eventually forced into emergency migration

**Not recommended**

## Discussion Topics

### Technical Feasibility
1. Can we achieve < 4 hours downtime for Option B?
2. What's the rollback plan if PostgreSQL migration fails?
3. How do we handle data migration for 500GB?
4. Schema design - what constraints do we need?

### Business Impact
5. What's the customer impact of 4-6 hours downtime?
6. Can we schedule migration during low-traffic period?
7. How does this affect Q4 feature roadmap?
8. Cost-benefit analysis over 2-year horizon?

### Risk Management
9. What are the biggest risks with Option B?
10. How do we test thoroughly before cutover?
11. What's the rollback procedure and time?
12. Do we have necessary expertise on team?

### Timeline & Resources
13. Can we allocate 2 engineers full-time for 8 weeks?
14. Do we need external consultants?
15. What's the impact on other Q4 projects?
16. When could we realistically complete this?

## Decision Framework

**Evaluation criteria**:
1. **Performance improvement**: Will this solve our performance issues?
2. **Technical debt**: Does this reduce or increase complexity?
3. **Risk**: What's the probability and impact of failure?
4. **Cost**: Total cost of ownership (effort + infrastructure)
5. **Timeline**: Can we complete in Q4?
6. **Reversibility**: Can we roll back if needed?

**Decision makers**:
- Primary: David Kim (CTO)
- Consulted: Sarah Chen (Engineering), Bob Martinez (DevOps)
- Informed: Product, Executive team

## Decision

*[To be filled during meeting]*

**Selected Option**: ___________________

**Rationale**:

**Timeline**:

**Owner**: ___________________

**Success Criteria**:

## Action Items

*[To be filled during meeting]*

- [ ] [Action item] - @[Owner] - Due: [Date]
- [ ] [Action item] - @[Owner] - Due: [Date]

## Next Steps

**Immediate**:
- Document decision rationale
- Create detailed implementation plan
- Schedule kickoff meeting

**Follow-up meeting**: [Date] to review migration plan

## Related Resources

### Primary Sources
- <mention-page url="...">Database Migration Proposal</mention-page>
- <mention-page url="...">Current Database Performance Issues</mention-page>
- <mention-page url="...">Migration Options Analysis</mention-page>
- <mention-page url="...">Previous Migration Post-mortem</mention-page>

### Supporting Documents
- MongoDB performance metrics dashboard
- PostgreSQL evaluation results
- Cost analysis spreadsheet
```

### Step 5: Share Agenda

```
Notion:notion-create-comment
parent: { page_id: "agenda-page-id" }
rich_text: [{
  type: "text",
  text: { content: "📋 Meeting agenda ready! Please review the pre-read before tomorrow's meeting. cc: @Sarah @David @Alice @Bob @Carol" }
}]
```

## Summary Provided to User

```markdown
## Meeting Prep Complete ✅

### Meeting Details
- **Topic**: Database Migration Strategy Decision
- **Date**: October 15, 2025 at 2:00 PM
- **Duration**: 90 minutes
- **Attendees**: 5 (Engineering leads + CTO + Product)

### Agenda Created
<mention-page url="...">Architecture Decision: Database Migration Strategy</mention-page>

### Pre-Read Summary

**Problem**: MongoDB performance degrading (50ms → 400ms queries), schema flexibility causing issues

**Decision needed**: Choose between:
1. Stay on MongoDB (optimizations) - 2 weeks, low risk
2. Migrate to PostgreSQL - 8 weeks, high value, high risk ✅ Recommended
3. Hybrid approach - 4 weeks, medium complexity
4. Do nothing - Not recommended

**Recommendation**: Engineering team favors PostgreSQL migration

### Key Information Included

✅ **Background context** from 4 relevant pages
✅ **Options analysis** with pros/cons for each
✅ **Cost-benefit** breakdown
✅ **Risk assessment** for each option
✅ **Discussion topics** (16 questions organized by theme)
✅ **Decision framework** with evaluation criteria
✅ **Historical context** from previous migration
✅ **Empty sections** for decision and action items

### Discussion Topics Prepared

**Technical** (4 questions):
- Downtime achievability
- Rollback planning
- Data migration approach
- Schema design

**Business** (4 questions):
- Customer impact
- Scheduling
- Roadmap impact
- Cost analysis

**Risk** (4 questions):
- Risk identification
- Testing strategy
- Rollback procedure
- Expertise availability

**Resources** (4 questions):
- Team allocation
- External help needs
- Project trade-offs
- Timeline realism

### Success Factors

1. **Comprehensive research**: 4 relevant pages analyzed
2. **Clear options**: Pros/cons for each approach
3. **Structured discussion**: 16 questions organized by theme
4. **Decision framework**: Clear criteria for evaluation
5. **Historical context**: Lessons from previous migration
6. **Ready for outcomes**: Sections prepared for decision and actions

**Meeting is well-prepared for productive decision-making! 📊**
```

## Key Features Demonstrated

### Context Gathering
- **Targeted search**: Engineering teamspace, recent documents
- **Multiple perspectives**: Performance data, proposals, analysis, historical lessons
- **Comprehensive synthesis**: Combined technical, business, and historical context

### Options Analysis
- **Structured comparison**: Pros/cons for each option
- **Cost-benefit**: Effort and infrastructure costs included
- **Risk assessment**: Probability and impact noted
- **Recommendation**: Clear engineering preference stated

### Decision Support
- **Discussion topics**: 16 questions organized by theme
- **Decision framework**: Evaluation criteria defined
- **Decision makers**: Roles and responsibilities clear
- **Outcome capture**: Sections ready for decision and actions

### Meeting Structure
- **Pre-read**: Comprehensive background (can be read in 10 minutes)
- **Options**: Clear comparison for quick decision
- **Discussion**: Structured topics prevent rambling
- **Capture**: Templates for decision and actions

Perfect for: Architecture decisions, technical trade-offs, strategic choices


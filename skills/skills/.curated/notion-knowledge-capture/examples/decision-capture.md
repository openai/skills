# Example: Decision Record Capture

**User Request**: "Document our decision to move from REST to GraphQL API"

## Workflow

### 1. Extract Decision from Context
From conversation, identified:
- **Decision**: Migrate customer-facing API from REST to GraphQL
- **Context**: REST endpoints becoming unwieldy (50+ endpoints)
- **Alternatives**: Keep REST, try gRPC, adopt GraphQL
- **Rationale**: Better client experience, type safety, single endpoint

### 2. Find Decision Log
```
Notion:notion-search
query: "architecture decisions" or "ADR"
```

Found: "Architecture Decision Records" database

### 3. Fetch Schema
```
Notion:notion-fetch
```

Got properties: Decision (title), Date, Status, Domain, Impact, Deciders, Stakeholders

### 4. Create Decision Record
```
Notion:notion-create-pages
parent: { data_source_id: "decision-log-collection-id" }
pages: [{
  properties: {
    "Decision": "Migrate to GraphQL API",
    "date:Date:start": "2025-10-16",
    "date:Date:is_datetime": 0,
    "Status": "Accepted",
    "Domain": "Architecture",
    "Impact": "High"
  },
  content: "[Full decision record with context, rationale, alternatives...]"
}]
```

**Content sample**:

```markdown
# Migrate Customer-Facing API to GraphQL

## Context
Our REST API has grown to 50+ endpoints with inconsistent patterns. Frontend and mobile teams request new endpoints frequently, leading to:
- API bloat and maintenance burden
- Over-fetching/under-fetching data
- Slow iteration on client features
- Inconsistent error handling

## Decision
Migrate customer-facing API from REST to GraphQL while maintaining REST for internal services.

## Rationale
**Why GraphQL**:
- Clients fetch exactly what they need (no over/under-fetching)
- Single endpoint, self-documenting schema
- Type safety with code generation
- Better developer experience
- Industry standard for client-facing APIs

## Options Considered

### Option A: Keep REST (Status Quo)
**Pros**: No migration cost, team familiar
**Cons**: Doesn't solve core problems, maintenance keeps growing
**Decision**: Rejected - doesn't address root cause

### Option B: gRPC
**Pros**: Performance, strong typing
**Cons**: Browser support issues, steeper learning curve, not designed for client-facing
**Decision**: Rejected - better for internal services

### Option C: GraphQL
**Pros**: Solves over/under-fetching, great DX, strong ecosystem
**Cons**: Learning curve, caching complexity, migration effort
**Decision**: **Accepted**

## Consequences

**Positive**:
- Faster frontend/mobile development
- Reduced API maintenance burden
- Better type safety and tooling
- Single endpoint simplifies deployment

**Negative**:
- 3-4 month migration timeline
- Team needs training
- Need to solve caching strategy
- Monitoring/debugging patterns different

## Implementation Plan
1. GraphQL server setup (Apollo Server)
2. Schema design workshop
3. Gradual migration (start with new features)
4. Dual-run period (both REST and GraphQL)
5. Deprecate old REST endpoints

**Timeline**: Start Q4 2025, complete Q1 2026
**Owner**: Backend team lead

## Success Metrics
- API response times improve 30%
- Client fetch efficiency (less data transferred)
- Reduced new endpoint requests
- Developer satisfaction scores
```

### 5. Make Discoverable
Added link from Architecture Wiki and notified team in Slack.

## Key Success Factors
- Captured decision while context fresh
- Documented alternatives considered
- Included both pros and cons
- Clear implementation plan
- Saved to decision log for future reference
- Made discoverable for team

# Example: Customer Meeting Prep

**User Request**: "Prep for sales meeting with Acme Corp on Thursday"

## Workflow

### 1. Search Customer Info
```
Notion:notion-search
query: "Acme Corp"
```

Found:
- CRM notes from initial call
- Product demo feedback
- Pricing proposal
- Competitor analysis

### 2. Fetch Details
```
Notion:notion-fetch (4 pages)
```

**Key context**:
- **Company**: 500-person fintech startup, Series B
- **Pain Points**: Manual workflows, data silos, scaling issues
- **Decision Makers**: CTO (technical), VP Product (user needs), CFO (budget)
- **Timeline**: Need solution by Q1
- **Budget**: $50-75K/year range
- **Competition**: Evaluating us vs. Competitor A and Competitor B

### 3. Add Research Context
Codex research added:
- Fintech industry compliance requirements
- Common integration needs for financial products
- Typical procurement processes for Series B companies

### 4. Create Internal Pre-Read
```
Notion:notion-create-pages
pages: [{
  properties: {
    title: "Acme Corp Meeting - Pre-Read (Internal)"
  },
  content: "# Acme Corp Meeting - Pre-Read (Internal)

## Company Overview
**Company**: Acme Corp (500-person fintech, Series B)
**Decision Makers**: CTO, VP Product, CFO
Source: <mention-page url='...'>CRM Notes</mention-page>

## Their Pain Points → Our Solutions
- Manual workflows → Workflow automation
- Data silos → API integrations
- Scaling issues → Enterprise features

## Competitive Position
**Our advantages over Competitor A/B**:
- Better integration ecosystem (Stripe, Plaid)
- Stronger compliance features
- Faster implementation (4 weeks vs 12 weeks)

## Pricing Strategy
Recommend: $60K/year (mid-range of their budget)

## Potential Objections & Responses
..."
}]
```

### 5. Create Meeting Agenda
```
Notion:notion-create-pages
pages: [{
  properties: {
    title: "Acme Corp - Product Demo & Q&A"
  },
  content: "# Acme Corp - Product Demo & Q&A

## Meeting Details
**Date**: Thursday, Oct 17, 2025 @ 2pm PST
**Attendees**: CTO, VP Product, CFO (Acme) | Sales Lead, Solutions Engineer (Us)
**Duration**: 60 minutes

## Objective
Demonstrate how our platform solves Acme's workflow automation and integration challenges.

## Agenda

**1. Introductions** (5 min)

**2. Understand Current Workflow** (10 min)
- Current pain points
- Integration requirements
- Success criteria

**3. Product Demo** (25 min)
- Workflow automation capabilities
- API integrations (Stripe, Plaid)
- Security & compliance features

**4. Pricing & Implementation** (10 min)

**5. Next Steps** (10 min)
"
}]
```

### 6. Link Resources
Connected agenda to CRM page, pricing sheet, and technical integration docs.

## Outputs

**Internal Pre-Read**: Full context for sales team
**Customer Agenda**: Professional meeting structure
**Both in Notion** with links to supporting materials

## Key Success Factors
- Understood customer's specific pain points
- Researched industry context (fintech compliance)
- Mapped features to their needs
- Prepared competitive differentiators
- Structured demo around their use cases
- Pre-planned objection responses
- Clear next steps in agenda

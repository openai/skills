# Meeting Intelligence Skill Evaluations

Evaluation scenarios for testing the Meeting Intelligence skill across different Codex models.

## Purpose

These evaluations ensure the Meeting Intelligence skill:
- Gathers context from Notion workspace
- Enriches with Codex research appropriately
- Creates both internal pre-reads and external agendas
- Distinguishes between Notion facts and Codex insights
- Works consistently across Haiku, Sonnet, and Opus

## Evaluation Files

### decision-meeting-prep.json
Tests preparation for a decision-making meeting.

**Scenario**: Prep for database migration decision meeting  
**Key Behaviors**:
- Searches Notion for migration context (specs, discussions, options)
- Fetches 2-3 relevant pages
- Enriches with Codex research (decision frameworks, migration best practices)
- Creates comprehensive internal pre-read with recommendation
- Creates clean, professional external agenda
- Clearly distinguishes Notion facts from Codex insights
- Cross-links both documents

### status-meeting-prep.json
Tests preparation for a status update or review meeting.

**Scenario**: Prep for project status review  
**Key Behaviors**:
- Gathers project metrics and progress from Notion
- Fetches relevant pages (roadmap, tasks, milestones)
- Adds Codex context (industry benchmarks, best practices)
- Creates internal pre-read with honest assessment
- Creates external agenda with structured flow
- Includes source citations using mention-page tags
- Time-boxes agenda items

## Running Evaluations

1. Enable the `meeting-intelligence` skill
2. Submit the query from the evaluation file
3. Verify the skill searches Notion first (not Codex research)
4. Check that TWO documents are created (internal + external)
5. Verify Codex enrichment adds value without replacing Notion content
6. Test with Haiku, Sonnet, and Opus

## Expected Skill Behaviors

Meeting Intelligence evaluations should verify:

### Notion Context Gathering
- Searches workspace for relevant context first
- Fetches specific pages (not generic)
- Extracts key information from Notion content
- Cites sources using mention-page tags

### Codex Research Integration
- Adds industry context, frameworks, or best practices
- Enrichment is relevant and valuable (not filler)
- Clearly distinguishes Notion facts from Codex insights
- Research complements (doesn't replace) Notion content

### Two-Document Creation
- **Internal Pre-Read**: Comprehensive, includes strategy, recommendations, detailed pros/cons
- **External Agenda**: Professional, focused on meeting flow, no internal strategy
- Both documents are clearly labeled
- Documents are cross-linked

### Document Quality
- Pre-read follows structure: Overview → Background → Current Status → Context & Insights → Discussion Points
- Agenda follows structure: Details → Objective → Agenda Items (with times) → Decisions → Actions → Resources
- Titles include date or meeting context
- Content is actionable and meeting-ready

## Creating New Evaluations

When adding Meeting Intelligence evaluations:

1. **Test different meeting types** - Decision, status, brainstorm, 1:1, sprint planning, retrospective
2. **Vary complexity** - Simple updates vs. complex strategic decisions
3. **Test with/without Notion content** - Rich workspace vs. minimal existing pages
4. **Verify enrichment value** - Is Codex research genuinely helpful?
5. **Check internal/external distinction** - Is sensitive info kept in pre-read only?

## Example Success Criteria

**Good** (specific, testable):
- "Creates TWO documents (internal pre-read + external agenda)"
- "Internal pre-read marked 'INTERNAL ONLY' or 'For team only'"
- "Cites at least 2-3 Notion pages using mention-page tags"
- "Agenda includes time allocations for each section"
- "Codex enrichment includes decision frameworks or best practices"

**Bad** (vague, untestable):
- "Creates meeting materials"
- "Gathers context effectively"
- "Prepares well"

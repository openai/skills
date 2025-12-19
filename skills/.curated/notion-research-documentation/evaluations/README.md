# Research & Documentation Skill Evaluations

Evaluation scenarios for testing the Research & Documentation skill across different Codex models.

## Purpose

These evaluations ensure the Research & Documentation skill:
- Searches across Notion workspace effectively
- Synthesizes information from multiple sources
- Selects appropriate research report format
- Creates comprehensive documentation with proper citations
- Works consistently across Haiku, Sonnet, and Opus

## Evaluation Files

### basic-research.json
Tests basic research workflow with synthesis across multiple Notion pages.

**Scenario**: Research Q4 product roadmap and create summary  
**Key Behaviors**:
- Searches Notion for roadmap-related pages
- Fetches multiple relevant pages (roadmap, product docs, meeting notes)
- Synthesizes information from different sources
- Selects appropriate format (Research Summary)
- Includes citations linking back to source pages
- Creates structured document with clear sections

### research-to-database.json
Tests creating research documentation in a Notion database with properties.

**Scenario**: Research competitor landscape and save to Research database  
**Key Behaviors**:
- Searches for existing competitive intelligence in Notion
- Identifies Research database as target
- Fetches database schema to understand properties
- Creates page with correct property values (Research Type, Status, Date, etc.)
- Structures content with comparison format
- Includes source citations for both Notion pages and external research

## Running Evaluations

1. Enable the `research-documentation` skill
2. Submit the query from the evaluation file
3. Verify the skill searches Notion workspace comprehensively
4. Check that multiple source pages are fetched and synthesized
5. Verify appropriate format is selected (Research Summary, Comprehensive Report, Quick Brief, Comparison)
6. Confirm citations link back to sources
7. Test with Haiku, Sonnet, and Opus

## Expected Skill Behaviors

Research & Documentation evaluations should verify:

### Notion Search & Synthesis
- Searches workspace with relevant queries
- Fetches multiple source pages (3-5+)
- Synthesizes information across sources
- Identifies patterns and insights
- Handles conflicting information appropriately

### Format Selection
- Chooses correct format based on scope and depth:
  - **Research Summary**: Quick overview with key findings
  - **Comprehensive Report**: Deep analysis with multiple sections
  - **Quick Brief**: Fast facts and takeaways
  - **Comparison**: Side-by-side analysis
- Applies format structure consistently
- Uses appropriate sections and headings

### Citation & Attribution
- Includes citations for all Notion sources
- Uses mention-page tags: `<mention-page url="...">`
- Attributes findings to specific sources
- Distinguishes between Notion content and Codex research
- Links related documents

### Document Quality
- Title clearly indicates research topic and date
- Executive summary or key findings upfront
- Organized with clear hierarchy
- Actionable insights and recommendations
- Appropriate depth for the query

## Creating New Evaluations

When adding Research & Documentation evaluations:

1. **Test different research types** - Product research, competitive analysis, technical investigation, market research
2. **Vary source count** - Synthesis of 2-3 pages vs. 10+ pages
3. **Test format selection** - Does it choose the right format for the scope?
4. **Include database targets** - Not just standalone pages
5. **Test citation accuracy** - Are all sources properly attributed?
6. **Cross-workspace search** - Testing search across teamspaces if applicable

## Example Success Criteria

**Good** (specific, testable):
- "Searches Notion for 'roadmap' and 'Q4' and 'product'"
- "Fetches at least 3 different source pages"
- "Includes citation for each key finding using mention-page tags"
- "Creates page with title format 'Research: [Topic] - [Date]'"
- "Uses Research Summary format with sections: Executive Summary → Key Findings → Details → Recommendations → Sources"

**Bad** (vague, untestable):
- "Searches Notion effectively"
- "Creates comprehensive research"
- "Uses sources appropriately"
- "Good documentation"


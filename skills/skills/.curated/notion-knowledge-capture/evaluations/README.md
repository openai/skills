# Knowledge Capture Skill Evaluations

Evaluation scenarios for testing the Knowledge Capture skill across different Codex models.

## Purpose

These evaluations ensure the Knowledge Capture skill:
- Correctly identifies content types (how-to guides, FAQs, decision records, wikis)
- Extracts relevant information from conversations
- Structures content appropriately for each type
- Searches and places content in the right Notion location
- Works consistently across Haiku, Sonnet, and Opus

## Evaluation Files

### conversation-to-wiki.json
Tests capturing conversation content as a how-to guide for the team wiki.

**Scenario**: Save deployment discussion to wiki  
**Key Behaviors**:
- Extracts steps, gotchas, and best practices from conversation
- Identifies content as How-To Guide
- Structures with proper sections (Overview, Prerequisites, Steps, Troubleshooting)
- Searches for team wiki location
- Preserves technical details (commands, configs)

### decision-record.json
Tests capturing architectural or technical decisions with full context.

**Scenario**: Document database migration decision  
**Key Behaviors**:
- Extracts decision context, alternatives, and rationale
- Follows decision record structure (Context, Decision, Alternatives, Consequences)
- Captures both selected and rejected options with reasoning
- Places in decision log or ADR database
- Links to related technical documentation

## Running Evaluations

1. Enable the `knowledge-capture` skill
2. Submit the query from the evaluation file
3. Provide conversation context as specified
4. Verify all expected behaviors are met
5. Check success criteria for quality
6. Test with Haiku, Sonnet, and Opus

## Expected Skill Behaviors

Knowledge Capture evaluations should verify:

### Content Extraction
- Accurately captures key points from conversation context
- Preserves specific technical details, not generic placeholders
- Maintains context and nuance from discussion

### Content Type Selection
- Correctly identifies appropriate content type (how-to, FAQ, decision record, wiki page)
- Uses matching structure from reference documentation
- Applies proper Notion markdown formatting

### Notion Integration
- Searches for appropriate target location (wiki, decision log, etc.)
- Creates well-structured pages with clear titles
- Uses proper parent placement
- Includes discoverable titles and metadata

### Quality Standards
- Content is actionable and future-reference ready
- Technical accuracy is preserved
- Organization aids discoverability
- Formatting enhances readability

## Creating New Evaluations

When adding Knowledge Capture evaluations:

1. **Use realistic conversation content** - Include actual technical details, decisions, or processes
2. **Test different content types** - How-to guides, FAQs, decision records, meeting notes, learnings
3. **Vary complexity** - Simple captures vs. complex technical discussions
4. **Test discovery** - Finding the right wiki section or database
5. **Include edge cases** - Unclear content types, minimal context, overlapping categories

## Example Success Criteria

**Good** (specific, testable):
- "Structures content using How-To format with numbered steps"
- "Preserves exact bash commands from conversation"
- "Creates page with title format 'How to [Action]'"
- "Places in Engineering Wiki → Deployment section"

**Bad** (vague, untestable):
- "Creates good documentation"
- "Uses appropriate structure"
- "Saves to the right place"


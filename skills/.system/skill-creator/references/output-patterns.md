# Output Pattern Guidelines for Skills

This guide covers best practices for defining expected output formats and quality standards in skills.

## Overview

Skills often need to produce structured outputs with specific formats, quality standards, or validation requirements. This document provides patterns for documenting and ensuring consistent output quality.

## Basic Output Specification

### Template-Based Outputs

For outputs with consistent structure, provide a template:

````markdown
## Output Format: Project Proposal

All project proposals should follow this structure:

```markdown
# [Project Name]

## Overview
[2-3 sentence summary of the project]

## Problem Statement
[What problem does this solve?]

## Solution
[How will this solve it?]

## Timeline
- Phase 1: [description] (weeks 1-2)
- Phase 2: [description] (weeks 3-4)

## Success Metrics
- [Metric 1]: [target value]
- [Metric 2]: [target value]
```

Example output:
[Filled-in example following the template above]
````

### Structured Data Outputs

For technical outputs that must be valid, specify the exact format:

````markdown
## Output Format: JSON Configuration

All configuration files must be valid JSON and include:

```json
{
  "version": "1.0",
  "name": "string (required)",
  "settings": {
    "timeout": "number (milliseconds)",
    "retries": "number (0-5)"
  }
}
```

**Validation**: Output must be parseable by `json.parse()` and include all required fields.

Example:
[Valid example with all required fields]
````

## Quality Standards

### Documentation Quality

Define what "complete" means:

```markdown
## Output Quality Standards: API Documentation

Each endpoint documentation must include:

1. **Description**: What the endpoint does (1-2 sentences)
2. **HTTP Method**: GET, POST, PUT, DELETE, PATCH
3. **URL Path**: Example: `/api/users/{userId}`
4. **Parameters**: Table with name, type, required/optional, description
5. **Request Body**: Schema and example (if applicable)
6. **Responses**: 
   - Success response (200/201): Schema and example
   - Common error responses: Code, description, example
7. **Example cURL Command**: Full working example with realistic data

**Validation checklist**:
- [ ] All required sections present
- [ ] Examples are realistic and runnable
- [ ] Parameter types are specified
- [ ] All response codes documented
- [ ] Error responses include error messages

Example:
[Complete example endpoint documentation]
```

### Code Quality

Specify code standards within skills:

```markdown
## Output Quality Standards: Generated Python Code

All generated Python code must:

1. **Follow PEP 8 style**: Use `black` formatter standards
2. **Include docstrings**: All functions must have docstrings
3. **Type hints**: Function parameters and return types must be annotated
4. **Error handling**: Try/except blocks for external API calls
5. **Logging**: Use `logging` module, not print statements
6. **Tests**: Include unit tests for public functions

**Validation**: Code must pass `pylint` and `black --check`

Example:
```python
def fetch_user_data(user_id: int) -> dict:
    """
    Fetch user data from the API.
    
    Args:
        user_id: The ID of the user to fetch
        
    Returns:
        Dictionary containing user data
        
    Raises:
        ValueError: If user_id is invalid
        APIError: If API request fails
    """
    if not isinstance(user_id, int) or user_id < 0:
        raise ValueError(f"Invalid user_id: {user_id}")
    
    try:
        response = api.get(f"/users/{user_id}")
        return response.json()
    except requests.Timeout:
        logging.error(f"Timeout fetching user {user_id}")
        raise
```
```

## Output Validation Patterns

### Visual Outputs

For design or visual outputs, specify quality criteria:

```markdown
## Output Quality Standards: UI Mockups

All UI mockups must:

1. **Use consistent spacing**: 8px grid baseline
2. **Maintain visual hierarchy**: Clear primary, secondary, tertiary elements
3. **Include interactive states**: Hover, focus, disabled states for buttons
4. **Meet accessibility requirements**:
   - Minimum contrast ratio: 4.5:1 for text
   - Text sizes: Minimum 12px for body text
5. **Show real content**: Use realistic text lengths, not Lorem Ipsum

**Validation checklist**:
- [ ] All interactive elements have hover/focus states
- [ ] Color contrast meets WCAG AA standards
- [ ] Spacing is consistent with design system
- [ ] Responsive behavior shown (mobile, tablet, desktop)

Example:
[Screenshot showing all required elements]
```

### Data Validation

For data outputs, be explicit about validation:

```markdown
## Output Quality Standards: Data Export

All exported data must:

1. **Be complete**: No missing rows or columns
2. **Match schema**: All fields present and correctly typed
3. **Include metadata**:
   - Export timestamp
   - Data source
   - Version number
4. **Pass validation**:
   - No null values in required fields
   - All emails match RFC 5322 format
   - All dates in ISO 8601 format
   - Numeric values within expected ranges

**Validation script**: `scripts/validate_export.py <file>`

Example:
[Sample valid data file with comments explaining structure]
```

## Multi-Format Outputs

When outputs can take multiple forms, specify each:

```markdown
## Output Formats: Content Generation

Choose one of the following output formats based on use case:

### 1. Markdown Format
Recommended for: Documentation, blog posts, reports
Structure: [Markdown template above]

### 2. HTML Format  
Recommended for: Web display, email newsletters
Structure: [HTML template above]

### 3. PDF Format
Recommended for: Print, formal documents, sharing
Requirements:
- Use [font specs]
- Include [header/footer specs]
- Page size and margins

**Choose format based on**:
- Is this for web or print?
- Will it be archived or archived?
- Who is the audience?
```

## Iterative Improvement Patterns

### Version Progression

Document how outputs evolve:

```markdown
## Output Quality Levels

**v1 - Basic**
- Minimal requirements met
- Suitable for: Drafts, quick iterations
- Includes: [core elements only]

**v2 - Standard**
- Full requirements met
- Suitable for: Production use
- Adds: [refined elements]

**v3 - Enhanced**
- Includes best practices and polish
- Suitable for: Public-facing, client deliverables
- Adds: [advanced elements]

When Codex generates output, default to v2. Include v3 enhancements only if user explicitly requests higher quality or if the use case clearly requires it (e.g., "client proposal").
```

## Error Cases

### Handling Invalid Inputs

Specify what happens when output requirements can't be met:

```markdown
## Handling Invalid Outputs

If Codex cannot meet output requirements:

1. **Missing information**: Ask user for missing details rather than guessing
2. **Conflicting requirements**: Ask user to clarify priority
3. **Quality standards violation**: Explain which standard isn't met and why
4. **Format impossibility**: Suggest alternative formats that meet the goal

Never silently downgrade quality or drop requirements. Always explain trade-offs and ask user for direction.
```

## Testing Output Patterns

When defining outputs, ensure:

1. **Examples are complete**: Do they show all required parts?
2. **Examples are realistic**: Would a user recognize the output as good?
3. **Validation is automatable**: Can output be checked by script or checklist?
4. **Edge cases are considered**: What should happen with edge cases?
5. **Failure modes are defined**: What counts as invalid output?

## Best Practices

1. **Be specific**: "Well-formatted" is too vague. Specify exact formats
2. **Provide examples**: Show what good output looks like
3. **Include validation**: Tell Codex how to verify output quality
4. **Document trade-offs**: When requirements conflict, explain how to choose
5. **Make templates discoverable**: Reference output patterns from main SKILL.md
6. **Test with real cases**: Validate patterns work with actual skill usage

## Related Sections

For workflow examples that produce outputs, see:
- `references/workflows.md` for multi-step processes leading to outputs
- Your SKILL.md body for step-by-step instructions

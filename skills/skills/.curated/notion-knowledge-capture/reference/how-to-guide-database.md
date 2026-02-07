# How-To Guide Database

**Purpose**: Procedural documentation for common tasks.

## Schema

| Property | Type | Options | Purpose |
|----------|------|---------|---------|
| **Title** | title | - | "How to [Task]" |
| **Complexity** | select | Beginner, Intermediate, Advanced | Skill level required |
| **Time Required** | number | - | Estimated minutes to complete |
| **Prerequisites** | relation | Links to other guides | Required knowledge |
| **Category** | select | Development, Deployment, Testing, Tools | Task category |
| **Last Tested** | date | - | When procedure was verified |
| **Tags** | multi_select | - | Technology/tool tags |

## Usage

```
Create how-to guides with properties:
{
  "Title": "How to Set Up Local Development Environment",
  "Complexity": "Beginner",
  "Time Required": 30,
  "Category": "Development",
  "Last Tested": "2025-10-01",
  "Tags": "setup, environment, docker"
}
```

## Best Practices

1. **Use consistent naming**: Always start with "How to..."
2. **Test procedures**: Verify steps work before publishing
3. **Include time estimates**: Help users plan their time
4. **Link prerequisites**: Make dependencies clear
5. **Update regularly**: Re-test procedures when tools/systems change


# Apex Spec System

A specification-driven workflow system for AI-assisted development.

Break large projects into manageable, well-scoped implementation sessions
that fit within AI context windows and human attention spans.

**Philosophy**: 1 session = 1 spec = 2-4 hours (12-25 tasks)

## What It Does

Provides a 22-command workflow that guides you from project initialization
through phased implementation:

1. **Initialize** - Set up spec system, create PRD, build phase structure
2. **Implement** - Plan sessions, implement tasks, validate completeness
3. **Transition** - Audit quality, set up CI/CD, carry forward lessons

## Requirements

- bash, git, jq (standard CLI tools)

## Installation

Install from the catalog:

```
$skill-installer install the apex-spec skill from the .experimental folder
```

Or install directly:

```bash
git clone https://github.com/aiwithapex/apex-spec-system-open.git \
  ~/.agents/skills/apex-spec
```

## Usage

```bash
# Initialize spec system in your project
$apex-spec initspec

# Create PRD from requirements
$apex-spec createprd

# Build phase structure
$apex-spec phasebuild

# Plan and implement sessions
$apex-spec plansession
$apex-spec implement
$apex-spec validate
$apex-spec updateprd
```

The skill also activates implicitly when working in a project with a
`.spec_system/` directory.

## Source Repository

Full documentation, contributing guidelines, and development resources:
https://github.com/aiwithapex/apex-spec-system-open

## License

[MIT](LICENSE.txt)

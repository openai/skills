---
title: Sanity Blueprints
description: Rules for Sanity Blueprints, the Infrastructure as Code solution for managing Sanity resources declaratively.
---

# Sanity Blueprints

## What is Blueprints?

Blueprints is Sanity's **Infrastructure as Code (IaC)** solution. It lets you define Sanity infrastructure declaratively in code, track it in version control, and deploy it programmatically.

Configure Sanity resources in a Blueprint file and deploy with a single command.

## Mental Model

```
Blueprint (code) → Stack (deployed state) → Resources (real infrastructure)
```

| Concept | What it is |
|---------|------------|
| **Blueprint** | A declarative configuration file (`sanity.blueprint.ts`) that describes your desired infrastructure |
| **Stack** | The deployed, real-world collection of resources managed by Blueprints |
| **Resources** | Individual Sanity components: CORS origins, webhooks, datasets, functions, roles, robots |
| **Operation** | A deployment execution that applies Blueprint changes to resources in a Stack |

### How it works

1. Initialize and edit a Blueprint file describing desired resources
2. Run `sanity blueprints deploy` to apply changes to resources in a Stack
3. Blueprints creates/updates a Stack with your resources
4. The Stack persists — future deploys update it based on Blueprint changes

**Key insight:** The Blueprint is your *intent*. The Stack is *reality*. Blueprints reconciles the two.

## Why use Blueprints?

- **Reproducibility** — Same Blueprint = same infrastructure, every time
- **Version control** — Track infrastructure changes alongside code
- **Automation** — No manual clicking through dashboards
- **Multi-environment** — Spin up dev/staging/prod with consistent configuration
- **Collaboration** — Review infrastructure changes in PRs

## Available Resources

Blueprints can manage these Sanity components:

- Document Functions
- Media Library Asset Functions

More resources are coming soon.

## CLI Commands

```bash
sanity blueprints init <name>    # Initialize a new blueprint project
sanity blueprints info           # Show current stack status and resources
sanity blueprints plan           # Preview changes before deploying
sanity blueprints deploy         # Deploy the blueprint (creates/updates stack)
sanity blueprints config         # Configure the blueprint (edit project and stack)
sanity blueprints logs           # View deployment logs
sanity blueprints doctor         # Check for potential issues
sanity blueprints stacks         # List all stacks for the project
sanity blueprints destroy        # Destroy all resources in the stack
```

## Basic Workflow

### 1. Initialize

```bash
sanity blueprints init my-infra
cd my-infra
sanity blueprints info
```

This creates a `sanity.blueprint.ts` file and links it to a Sanity project.

### 2. Define resources

Edit `sanity.blueprint.ts` to add resources using typed helper functions from `@sanity/blueprints`.

### 3. Preview and deploy

```bash
sanity blueprints plan    # See what will change
sanity blueprints deploy  # Apply changes
```

### 4. Iterate

Modify your Blueprint and redeploy. Blueprints handles creating, updating, or removing resources to match your definition.

## Key Behaviors

- **Additive by default** — New resources in the Blueprint are created
- **Updates in place** — Changed resources are updated when possible
- **Removal = destruction** — Resources removed from the Blueprint are destroyed from the Stack
- **References** — Resources can reference each other (e.g., a webhook can reference a dataset)
- **Rollback on failure** — If a deployment fails partway through, Blueprints attempts to rollback

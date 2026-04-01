# Architecture Audit Guide — Mode 2

**Purpose:** Analyze the module and dependency structure of a system for decay risks that
operate at the architectural level. Every finding must follow the Iron Law:
Symptom → Source → Consequence → Remedy.

**Monorepo note:** Treat each deployable service or library as a top-level module. Draw
dependencies between services, not between their internal packages. Apply the Conway's Law
check at the service ownership level. Within a single service, apply standard module-level analysis.

---

## Analysis Process

Work through these five steps in order.

### Step 1: Draw the Module Dependency Graph (Mermaid)

Before evaluating any risk, map the dependencies as a Mermaid diagram. Use this format:

````mermaid
graph TD
  subgraph UI
    WebApp
    MobileApp
  end

  subgraph Domain
    AuthService
    OrderService
    PaymentService
  end

  subgraph Infrastructure
    Database
    MessageQueue
  end

  WebApp --> AuthService
  WebApp --> OrderService
  MobileApp --> AuthService
  MobileApp --> OrderService
  OrderService --> PaymentService
  OrderService --> Database
  OrderService --> MessageQueue
  PaymentService --> Database
  AuthService -.->|circular| OrderService

  classDef critical fill:#ff6b6b,stroke:#c92a2a,color:#fff
  classDef warning fill:#ffd43b,stroke:#e67700
  classDef clean fill:#51cf66,stroke:#2b8a3e,color:#fff

  class PaymentService critical
  class OrderService warning
  class Database,MessageQueue,AuthService,WebApp,MobileApp clean
````

**Phase A (during Step 1):** Generate the graph structure only — nodes, subgraphs, and edges.
Do NOT add `classDef` or `class` lines yet. You need findings from Steps 2-4 before coloring.

**Phase B (after Step 4):** Add `classDef` definitions and `class` assignments based on findings.
The example above shows the final output after both phases.

Rules:
1. **Nodes** — Use top-level directories or services as nodes, not individual files
2. **Grouping** — One `subgraph` per architectural layer or top-level directory (e.g., UI, Domain, Infrastructure)
3. **Edges** — Solid arrows (`-->`) point FROM the depending module TO the dependency; use dotted arrows with label (`-.->|circular|`) for circular dependencies. If no circular dependencies exist, use only solid arrows
4. **Node limit** — Keep the graph to ~50 nodes maximum; collapse low-risk leaf modules into their parent if needed
5. **Fan-out** — For any node with fan-out > 5, use a descriptive label: `HighFanOutModule["ModuleName (fan-out: 7)"]`
6. **Colors** — Apply `classDef` colors AFTER completing Steps 2-4: `critical` (red `#ff6b6b`) for nodes with Critical findings, `warning` (yellow `#ffd43b`) for Warning findings, `clean` (green `#51cf66`) for nodes with no findings or only Suggestions. If no findings at all, classify all nodes as `clean`
7. **Direction** — Default to `graph TD` (top-down); use `graph LR` only if the architecture is clearly a left-to-right pipeline

### Step 2: Scan for Dependency Disorder

*The most architecturally consequential risk — scan this first.*

Look for:
- Circular dependencies (any ⚠️ in the map above)
- Arrows flowing upward (high-level domain depending on low-level infrastructure)
- Stable, widely-depended-on modules that import from frequently-changing modules
- Modules with fan-out > 5
- Absence of a clear layering rule (no consistent answer to "what depends on what?")

### Step 3: Scan for Domain Model Distortion

Look for:
- Do module names match the business domain vocabulary?
- Is there a layer called "services" that contains all the business logic while domain objects
  are pure data structures?
- Are there modules that cross bounded context boundaries (e.g., billing logic in the user module)?
- Is there an anti-corruption layer where external systems interface with the domain?

### Step 4: Scan for Remaining Four Risks

Check each in turn:

**Knowledge Duplication:**
- Are there multiple modules implementing the same concept independently?
- Does the same domain concept appear under different names in different modules?

**Accidental Complexity:**
- Are there entire layers in the architecture that do not add value?
- Are there modules whose responsibility cannot be stated in one sentence?

**Change Propagation:**
- Which modules are "blast radius hotspots"? (A change here requires changes in many other modules)
- Does the dependency map reveal why certain features are slow to develop?

**Cognitive Overload:**
- Can the module responsibility of each module be stated in one sentence from its name alone?
- Would a new developer know which module to add a new feature to?

### Step 5: Conway's Law Check

After the six-risk scan, assess the relationship between architecture and team structure:

- Does the module/service structure reflect the team structure?
  (Conway's Law: "Organizations design systems that mirror their communication structure")
- If yes: is this intentional design or accidental coupling?
- A mismatch that causes cross-team coordination overhead for every feature is 🔴 Critical.
- A mismatch that is theoretical but not yet causing pain is 🟡 Warning.
- If team structure is unknown, note this as context missing and skip the check.

---

## Applying the Iron Law

For every finding identified above, write it in this format:

```
**[Risk Name] — [Short title]**
Symptom: [the exact structural evidence — reference module names from the dependency map]
Source: [Book title — Principle or Smell name]
Consequence: [what architectural consequence follows if this is not addressed]
Remedy: [concrete architectural action]
```

---

## Output

Use the standard Report Template from `SKILL.md`.
Mode: Architecture Audit
Scope: the project or directory audited.

Place the Mermaid dependency graph FIRST in the report, before the Findings section,
under the heading "Module Dependency Graph". In each finding, reference the relevant
node by name (e.g., "See the red node `PaymentService` in the graph above") so the
reader can cross-reference visually. The `classDef` color assignments must be added
LAST, after all findings have been identified and severity levels determined.

---

## Design Note: Analysis-Render Separation

The dependency graph follows a two-step conceptual model:

1. **Analysis** — Identify nodes (modules), edges (dependencies), groups (folders/layers),
   and severity per node. This produces a logical dependency structure independent of
   any diagram format.
2. **Render** — Convert the logical structure to Mermaid syntax (graph TD, subgraph,
   classDef, etc.).

This separation means adding an alternative output format (D2, Graphviz, SVG) in the
future only requires a new renderer — the analysis logic stays the same.

# Decay Risk Reference

Six patterns that cause software to degrade over time.
For each finding, identify: which risk, which symptom, which source book.

Every finding must follow the Iron Law:
Symptom → Source → Consequence → Remedy

---

## Risk 1: Cognitive Overload

**Diagnostic question:** How much mental effort does a human need to understand this?

When cognitive load exceeds working memory capacity, developers make mistakes, avoid touching
the code, and slow down. This risk compounds: hard-to-understand code resists the refactoring
that would make it easier to understand.

### Symptoms

- Function longer than 20 lines where multiple levels of abstraction are mixed together
- Nesting depth greater than 3 levels
- Parameter list with more than 4 parameters
- Magic numbers or unexplained constants
- Variable names that require reading the implementation to understand (e.g., `d`, `tmp2`, `flag`)
- Boolean expressions with 3 or more conditions combined
- Train-wreck chains: `a.getB().getC().doD()`
- Code names that do not match what the business calls the same concept

### Sources

| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Long Method | Fowler — Refactoring | Long Method |
| Long Parameter List | Fowler — Refactoring | Long Parameter List |
| Message Chains | Fowler — Refactoring | Message Chains |
| Function length and nesting | McConnell — Code Complete | Ch. 7: High-Quality Routines |
| Variable naming | McConnell — Code Complete | Ch. 11: The Power of Variable Names |
| Magic numbers | McConnell — Code Complete | Ch. 12: Fundamental Data Types |
| Domain name mismatch | Evans — Domain-Driven Design | Ubiquitous Language |

### Severity Guide

- 🔴 Critical: function > 50 lines, nesting > 5, or virtually no meaningful names
- 🟡 Warning: function 20–50 lines, nesting 4–5, some unclear names
- 🟢 Suggestion: minor naming issues, 1–2 magic numbers, isolated train-wreck chains

---

## Risk 2: Change Propagation

**Diagnostic question:** How many unrelated things break when you change one thing?

High change propagation means that a developer modifying feature A must also modify modules B,
C, and D — even though B, C, and D have nothing conceptually to do with A. This slows velocity
and multiplies regression risk on every change.

### Symptoms

- Modifying one feature requires touching more than 3 files in unrelated modules
- One class changes for multiple different business reasons (e.g., `UserService` changes for
  billing logic AND notification logic AND profile logic)
- A method uses more data from another class than from its own class
- Two classes know each other's internal state directly
- Changing one module requires recompiling or retesting many unrelated modules

### Sources

| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Shotgun Surgery | Fowler — Refactoring | Shotgun Surgery |
| Divergent Change | Fowler — Refactoring | Divergent Change |
| Feature Envy | Fowler — Refactoring | Feature Envy |
| Inappropriate Intimacy | Fowler — Refactoring | Inappropriate Intimacy |
| Orthogonality violation | Hunt & Thomas — The Pragmatic Programmer | Ch. 2: Orthogonality |
| DIP violation | Martin — Clean Architecture | Dependency Inversion Principle |
| High change propagation radius | Brooks — The Mythical Man-Month | Ch. 2: Brooks's Law (communication overhead) |

### Severity Guide

- 🔴 Critical: one change touches > 5 files, or there is a structural dependency inversion (domain depends on infrastructure)
- 🟡 Warning: one change touches 3–5 files, mild coupling between modules
- 🟢 Suggestion: minor coupling, easily isolatable

---

## Risk 3: Knowledge Duplication

**Diagnostic question:** Is the same decision expressed in more than one place?

When the same piece of knowledge lives in multiple places, those copies will inevitably drift
apart. This creates silent inconsistencies: both copies pass their tests but disagree on behavior
in edge cases. DRY is not about code lines — it is about decisions.

### Symptoms

- Same logic copy-pasted across multiple files or functions
- Same concept named differently in different parts of the codebase
  (e.g., `user`, `account`, `member`, `customer` all referring to the same domain entity)
- Parallel class hierarchies that must change in sync
  (e.g., adding a new payment type requires adding a class in 3 different hierarchies)
- Configuration values repeated as literals in multiple places
- Two modules that implement the same algorithm independently

### Sources

| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Code duplication | Fowler — Refactoring | Duplicate Code |
| Parallel Inheritance | Fowler — Refactoring | Parallel Inheritance Hierarchies |
| DRY violation | Hunt & Thomas — The Pragmatic Programmer | DRY: Don't Repeat Yourself |
| Inconsistent naming | Evans — Domain-Driven Design | Ubiquitous Language |
| Alternative Classes | Fowler — Refactoring | Alternative Classes with Different Interfaces |

### Severity Guide

- 🔴 Critical: core business logic duplicated across modules, or same domain concept named 3+ different ways
- 🟡 Warning: utility code duplicated, naming inconsistent within a subsystem
- 🟢 Suggestion: minor literal duplication, single naming inconsistency

---

## Risk 4: Accidental Complexity

**Diagnostic question:** Is the code more complex than the problem it solves?

Every system has essential complexity (inherent to the problem) and accidental complexity
(introduced by implementation choices). Accidental complexity is the only kind that can be
eliminated. It accumulates silently: each addition seems justified in isolation, but the total
burden grows until developers spend more time maintaining the scaffolding than solving the problem.

### Symptoms

- Abstractions built "for future use" with no current consumer
  (e.g., a plugin system for a use case that has only one known implementation)
- Classes that barely justify their existence (wrap a single method call)
- Classes that only delegate to another class without adding behavior (pure middle-men)
- Second attempt at a system that is significantly more elaborate than the first,
  adding generality for requirements that do not yet exist
- Switch statements that signal missing polymorphism
- Configuration options that have never been changed from their defaults
- Framework code larger than the application it powers

### Sources

| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Speculative Generality | Fowler — Refactoring | Speculative Generality |
| Lazy Class | Fowler — Refactoring | Lazy Class |
| Middle Man | Fowler — Refactoring | Middle Man |
| Switch Statements | Fowler — Refactoring | Switch Statements |
| Second System Effect | Brooks — The Mythical Man-Month | Ch. 5: The Second-System Effect |
| YAGNI violations | McConnell — Code Complete | Ch. 5: Design in Construction |
| Over-engineering | Hunt & Thomas — The Pragmatic Programmer | Ch. 2: The Evils of Duplication (YAGNI corollary) |

### Severity Guide

- 🔴 Critical: an entire subsystem built around a speculative requirement, or framework overhead dominates domain logic
- 🟡 Warning: several unnecessary abstractions or wrapper classes, unused configuration systems
- 🟢 Suggestion: one or two lazy classes or middle-man patterns in non-critical paths

---

## Risk 5: Dependency Disorder

**Diagnostic question:** Do dependencies flow in a consistent, predictable direction?

Dependency direction is the skeleton of a software system. When high-level business logic
depends on low-level infrastructure details, or when components depend on things less stable
than themselves, every infrastructure change becomes a business logic change. Circular
dependencies make it impossible to understand or test any component in isolation.

### Symptoms

- Circular dependencies between modules or packages
- High-level business logic directly imports from low-level infrastructure
  (e.g., a domain service imports from a specific database driver)
- Stable, widely-used components depend on unstable, frequently-changing ones
- Abstract components depending on concrete implementations
- Law of Demeter violations: `order.getCustomer().getAddress().getCity()`
- Module fan-out greater than 5 (imports from more than 5 other modules)
- The system feels like "one mind did not design this" — different modules use
  incompatible architectural patterns with no clear rule for which to use where

### Sources

| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Dependency cycles | Martin — Clean Architecture | Acyclic Dependencies Principle (ADP) |
| DIP violation | Martin — Clean Architecture | Dependency Inversion Principle (DIP) |
| Instability direction | Martin — Clean Architecture | Stable Dependencies Principle (SDP) |
| Abstraction mismatch | Martin — Clean Architecture | Stable Abstractions Principle (SAP) |
| Conceptual integrity | Brooks — The Mythical Man-Month | Ch. 4: Conceptual Integrity |
| Law of Demeter | Hunt & Thomas — The Pragmatic Programmer | Ch. 5: Decoupling and the Law of Demeter |
| SOLID violations | Martin — Clean Architecture | Single Responsibility, Open/Closed Principles |

### Severity Guide

- 🔴 Critical: dependency cycles present, or domain layer directly depends on infrastructure layer
- 🟡 Warning: several SDP or DIP violations but no cycles; conceptual inconsistency across modules
- 🟢 Suggestion: minor Demeter violations, slightly elevated fan-out in isolated modules

---

## Risk 6: Domain Model Distortion

**Diagnostic question:** Does the code faithfully represent the problem it is solving?

Code that does not speak the language of the problem domain forces every developer to maintain
a mental translation layer between "what the business calls it" and "what the code calls it."
Over time, this translation layer diverges, and the code begins to model the database schema
or the API contract rather than the business concept. Domain logic bleeds into service layers
and the domain objects become empty data containers.

### Symptoms

- Business logic scattered across service layers while domain objects have only getters and setters
  (anemic domain model)
- Code variable, class, or method names that do not match what business stakeholders call the concept
- A class whose only purpose is to hold data with no behavior (pure data bag)
- A subclass that ignores or overrides most of its parent's behavior (refuses the inheritance)
- Bounded context boundaries crossed without any translation or anti-corruption layer
- Methods that are more interested in the data of another class than their own
  (domain logic in the wrong place)

### Sources

| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Anemic Domain Model | Evans — Domain-Driven Design | Domain Model pattern |
| Ubiquitous Language drift | Evans — Domain-Driven Design | Ubiquitous Language |
| Bounded context violation | Evans — Domain-Driven Design | Bounded Context |
| Data Class | Fowler — Refactoring | Data Class |
| Refused Bequest | Fowler — Refactoring | Refused Bequest |
| Feature Envy | Fowler — Refactoring | Feature Envy |

### Severity Guide

- 🔴 Critical: domain logic entirely in service layer, domain objects are pure data bags with no behavior
- 🟡 Warning: partial anemia, some naming inconsistency between code and domain language
- 🟢 Suggestion: minor naming drift in non-core areas, isolated cases of Feature Envy

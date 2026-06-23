---
name: incremental-code-writing
description: Use when the user requests code to be written in a step-by-step manner.
---

# Objective

Reduce cognitive load by building the code incrementally instead of outputting the complete implementation at once, enabling the user to follow and understand the development process.

# Core Rules

* Implement only one clear logical unit at a time.
* Pause after each output and wait for user confirmation or questions.
* Provide brief explanations of the implementation approach when necessary.

Examples of logical units:

* Data structure definition
* Core function skeleton
* A single functional module
* I/O handling
* Error handling logic

# Recommended Build Process

Implement progressively in the following order (adjust as needed):

1. Overall structure or interface definition
2. Core data structures
3. Main workflow skeleton
4. Gradual completion of functional modules
5. Boundary and exception handling
6. Optimization and refactoring

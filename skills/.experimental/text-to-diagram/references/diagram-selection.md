# Diagram Selection Guide

Use these rules to choose the right diagram before generating Mermaid code.

## Diagram Inference Logic (Matrix)

1. If the text describes a step-by-step process or routine, use a Flowchart (`flowchart TD` or `flowchart LR`).
2. If the text describes a timeline of events or project phases, use a Timeline (`timeline`).
3. If the text describes interactions between multiple services, people, or objects over time, use a Sequence Diagram (`sequenceDiagram`).
4. If the text describes a database schema, data models, or relationships, use an ER Diagram (`erDiagram`).
5. If the text describes a high-level system architecture (systems/containers/components), use a C4 Diagram (Mermaid C4).
6. If the text is a list of hierarchical ideas or a brainstorm, use a Mindmap (`mindmap`).

## Additional Rules

- If the text explicitly mentions classes, interfaces, packages, inheritance, or methods, prefer a UML Class/Package diagram (`classDiagram`) unless the user asked for something else.
- If multiple diagram types apply, pick the one that best answers the user's immediate intent (process vs. interactions vs. structure).

## Operational Rule: Best Guess First

- Never ask \"What diagram do you want?\" unless the input is completely unusable.
- Generate the best-fit diagram and include a 1-sentence justification after the code block.

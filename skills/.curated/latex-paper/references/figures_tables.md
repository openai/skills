# Figures and Tables Guide

## Figure rules

- Place `\\caption` before `\\label`.
- Use semantic labels such as `fig:ablation` or `fig:architecture`.
- Reference every figure in text before or near its first appearance.
- Keep axis labels and legends self-contained.

## Table rules

- Use `booktabs` (`\\toprule`, `\\midrule`, `\\bottomrule`) over vertical borders.
- Keep units in headers, not data cells.
- Include short metric direction notes when needed (`higher is better`).

## Placement strategy

- Use `[t]` for most floats, `[tb]` when layout is tight.
- Avoid excessive `[h]`; it often causes unstable layout in long papers.
- Group closely related figures/tables near the first textual reference.

## Caption style

- Start with what is shown.
- End with why it matters.
- Keep captions declarative and concise.

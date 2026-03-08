# Citation Workflow

## Default bibliography flow in this skill

Templates in this skill use BibTeX-style workflows:

- `article`: `plainnat` + `natbib`
- `ieeetran`: `IEEEtran`
- `acmart`: `ACM-Reference-Format`

## Citation key conventions

Use stable, readable keys:

- Preferred: `lastnameYYYYshorttopic`
- Example: `smith2024contrastive`

Avoid random key changes once citations are used in manuscript text.

## In-text citation patterns

- Narrative form: `\\citet{key}`
- Parenthetical form: `\\citep{key}`
- Generic class-safe fallback: `\\cite{key}`

## Common failure modes

- Missing `.bib` entries for cited keys
- Typo mismatch between `\\cite{...}` and `@...{key,...}`
- Running LaTeX only once (cross-refs and bibliography need multiple passes)

Use `scripts/fixrefs.sh` to detect missing keys before finalizing.

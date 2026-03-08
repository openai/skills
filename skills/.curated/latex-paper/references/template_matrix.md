# Template Selection Matrix

## Quick recommendation

- Choose `article` for generic research writing, drafts, and preprints.
- Choose `ieeetran` for IEEE-targeted conference/journal submissions.
- Choose `acmart` for ACM-targeted submissions.

## Comparison

| Template | Best for | Strengths | Trade-offs |
| --- | --- | --- | --- |
| `article` | Early drafts, arXiv-like manuscripts | Minimal dependencies, easy customization | Not venue-branded |
| `ieeetran` | IEEE venues | Venue-aligned styling and bibliography | Tighter formatting constraints |
| `acmart` | ACM venues | Official ACM metadata and bibliography defaults | More metadata fields required |

## Scaffold commands

```bash
scripts/new_paper.sh /path/to/paper --template article
scripts/new_paper.sh /path/to/paper --template ieeetran
scripts/new_paper.sh /path/to/paper --template acmart
```

## Migration guidance

Switch templates only when venue requirements are finalized. Template migration often requires:

- package compatibility checks
- title/author block rewrites
- bibliography style updates

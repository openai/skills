# ida_problems

Low-priority: Manage problem lists for tracking analysis issues. IDA maintains these lists automatically; mainly used for debugging analysis failures.

## Key Functions

- `remember_problem(type, ea, msg)` - add address to problem list with optional message
- `get_problem(type, lowea)` - get next problem address >= lowea
- `forget_problem(type, ea)` - remove address from problem list
- `is_problem_present(type, ea)` - check if address is in problem list
- `get_problem_desc(type, ea)` - get human-readable problem description
- `get_problem_name(type, longname)` - get problem list name

## Problem List Types

- `PR_DISASM` - can't disassemble
- `PR_HEAD` - already head
- `PR_ILLADDR` - execution flows beyond limits
- `PR_BADSTACK` - failed to trace stack pointer
- `PR_NOXREFS` - can't find references
- `PR_NOBASE` - can't find offset base
- `PR_ATTN` - attention, probably erroneous
- `PR_FINAL` - IDA decision to convert to instruction/data
- `PR_ROLLED` - IDA decision was wrong and rolled back
- `PR_COLLISION` - FLAIR collision
- `PR_DECIMP` - FLAIR match indecision

View problems from View → Subviews → Problems menu.

## See Also
Full docs: skill/docs/ida_problems.rst

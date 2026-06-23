# ida_xref

Cross-reference (xref) tracking between code and data locations.

## Key Classes

### xrefblk_t
Iterator for traversing cross-references efficiently.
- `first_from(ea, flags)` / `next_from()` - Iterate xrefs FROM address
- `first_to(ea, flags)` / `next_to()` - Iterate xrefs TO address
- `frm` / `to` - Source and target addresses
- `type` - Reference type (cref_t or dref_t)
- `iscode` - True if code reference, false if data
- `user` - User-defined (won't be deleted by IDA)

Iterator helpers:
- `crefs_from(ea)` / `crefs_to(ea)` - Code references including flow
- `fcrefs_from(ea)` / `fcrefs_to(ea)` - Code references (no flow)
- `drefs_from(ea)` / `drefs_to(ea)` - Data references

## Key Functions

### add_cref(frm, to, type) / add_dref(frm, to, type)
Create code or data cross-reference.

### del_cref(frm, to, expand) / del_dref(frm, to)
Delete cross-reference (expand=1 deletes target if no more refs).

### get_first_cref_from(frm) / get_next_cref_from(frm, current)
Legacy API for iterating code xrefs FROM address.

### get_first_dref_to(to) / get_next_dref_to(to, current)
Legacy API for iterating data xrefs TO address.

### has_external_refs(pfn, ea)
Check if address has references from outside function.

### create_switch_xrefs(ea, si)
Generate xrefs for switch jump table.

## Reference Types

### Code (cref_t)
- `fl_CF` / `fl_CN` - Call Far/Near (creates function)
- `fl_JF` / `fl_JN` - Jump Far/Near
- `fl_F` - Ordinary flow to next instruction

### Data (dref_t)
- `dr_R` / `dr_W` - Read/Write access
- `dr_O` - Offset reference
- `dr_T` - Text reference (forced operand)

## Flags

- `XREF_USER` - User-defined (persistent)
- `XREF_TAIL` - Reference to tail byte
- `XREF_PASTEND` - Preserve alignment directives
- `XREF_CODE` / `XREF_DATA` - Filter by type
- `XREF_FLOW` / `XREF_NOFLOW` - Include/skip ordinary flow

## See Also
Full docs: skill/docs/ida_xref.rst

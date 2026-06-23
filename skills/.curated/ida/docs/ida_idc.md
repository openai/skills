# ida_idc

Marked positions (bookmarks) in IDA database - low priority module with limited scope.

## Key Functions

- `mark_position(ea, lnnum, x, y, slot, comment)` - Create bookmark at address in slot (0-1023)
- `get_marked_pos(slot)` - Get address of bookmark in slot
- `get_mark_comment(slot)` - Get comment for bookmark in slot

## See Also
Full docs: skill/docs/ida_idc.rst

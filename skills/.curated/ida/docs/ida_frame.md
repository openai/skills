# ida_frame

Function stack frame manipulation - local variables, register variables, stack pointer tracking.

## Frame Structure

```
+------------------------------------------------+
| function arguments                             |
+------------------------------------------------+
| return address                                 |
+------------------------------------------------+
| saved registers (SI, DI, etc)                  |
+------------------------------------------------+ <- typical BP
|                                                |
| local variables                                |
|                                                |
+------------------------------------------------+ <- SP
```

Access via: `tinfo_t::get_func_frame(pfn)` or `get_func_frame(out, pfn)` + `tinfo_t::get_udt_details()`

## Key Functions

### Frame Management
- `add_frame(pfn, frsize, frregs, argsize) -> bool` - Create frame (frsize=locals, frregs=saved regs, argsize=purged bytes)
- `del_frame(pfn) -> bool` - Delete frame
- `set_frame_size(pfn, frsize, frregs, argsize) -> bool` - Resize frame
- `get_frame_size(pfn) -> asize_t` - Full size (locals + saved regs + retaddr + purged bytes)
- `get_frame_retsize(pfn) -> int` - Return address size
- `get_func_frame(out, pfn) -> bool` - Get frame type info

### Frame Parts
- `frame_off_args(pfn) -> ea_t` - Arguments section start
- `frame_off_retaddr(pfn) -> ea_t` - Return address section start
- `frame_off_savregs(pfn) -> ea_t` - Saved registers section start
- `frame_off_lvars(pfn) -> ea_t` - Local variables section start
- `get_frame_part(range, pfn, part)` - Get part offsets (FPC_ARGS/FPC_RETADDR/FPC_SAVREGS/FPC_LVARS)

### Stack Variables
- `define_stkvar(pfn, name, off, tif, repr=None) -> bool` - Define stack var (negative off=locals, positive=args)
- `add_frame_member(pfn, name, offset, tif, repr=None, etf_flags=0) -> bool` - Add member to frame type
- `set_frame_member_type(pfn, offset, tif, repr=None, etf_flags=0) -> bool` - Change member type
- `delete_frame_members(pfn, start_offset, end_offset) -> bool` - Delete members in range
- `build_stkvar_name(pfn, v) -> str` - Auto-generate stack var name
- `calc_stkvar_struc_offset(pfn, insn, n) -> ea_t` - Calculate stack var offset in frame
- `calc_frame_offset(pfn, off, insn=None, op=None) -> int` - Calculate offset in frame from SP/BP offset
- `build_stkvar_xrefs(out, pfn, start_offset, end_offset)` - Get xrefs to stack frame range

### Utilities
- `is_funcarg_off(pfn, frameoff) -> bool` - Is offset in arguments range
- `lvar_off(pfn, frameoff) -> int` - Convert to local var offset
- `is_anonymous_member_name(name) -> bool` - Prefixed with "anonymous"
- `is_dummy_member_name(name) -> bool` - Auto-generated name
- `is_special_frame_member(tid) -> bool` - Is retaddr or saved regs slot
- `soff_to_fpoff(pfn, soff) -> int` - Convert struct offset to FP-relative
- `update_fpd(pfn, fpd) -> bool` - Update frame pointer delta
- `set_purged(ea, nbytes, override_old_value) -> bool` - Set purged bytes (__stdcall/__pascal)

### Register Variables
- `add_regvar(pfn, ea1, ea2, canon, user, cmt) -> int` - Define register variable in range
- `find_regvar(pfn, ea, canon) -> regvar_t*` - Find register variable definition
- `has_regvar(pfn, ea) -> bool` - Check if regvar exists
- `rename_regvar(pfn, v, user) -> int` - Rename register variable
- `set_regvar_cmt(pfn, v, cmt) -> int` - Set comment
- `del_regvar(pfn, ea1, ea2, canon) -> int` - Delete register variable
- `free_regvar(v)` - Free regvar_t

### Stack Pointer Tracking
- `get_spd(pfn, ea) -> int` - Get SP delta before instruction (initial SP - current SP)
- `get_effective_spd(pfn, ea) -> int` - Get SP delta used by instruction (differs for "pop [esp+N]")
- `get_sp_delta(pfn, ea) -> int` - Get SP modification at location (0 if no change point)
- `add_auto_stkpnt(pfn, ea, delta) -> bool` - Add automatic SP change point
- `add_user_stkpnt(ea, delta) -> bool` - Add user-defined SP change point
- `del_stkpnt(pfn, ea) -> bool` - Delete SP change point
- `set_auto_spd(pfn, ea, new_spd) -> bool` - Set cumulative SP delta at address
- `recalc_spd(cur_ea) -> bool` - Recalculate SP for non-fallthrough instructions
- `recalc_spd_for_basic_block(pfn, cur_ea) -> bool` - Recalculate SP for basic block

## regvar_t Class

Register variable definition (extends range_t).

### Attributes
- `canon: str` - Canonical register name (case-insensitive)
- `user: str` - User-defined name
- `cmt: str` - Comment near definition

## Error Codes

- `REGVAR_ERROR_OK` - Success
- `REGVAR_ERROR_ARG` - Bad function arguments
- `REGVAR_ERROR_RANGE` - Bad definition range
- `REGVAR_ERROR_NAME` - Name can't be accepted

## Flags

- `STKVAR_VALID_SIZE` - dtyp contains correct variable type (off for "lea")
- `STKVAR_KEEP_EXISTING` - Don't create new var if one exists

## See Also
Full docs: skill/docs/ida_frame.rst

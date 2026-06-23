# ida_regfinder

High-priority: Track register values backwards through code execution. Critical for understanding function arguments, constants loaded into registers, and stack pointer calculations.

## Key Functions

- `find_reg_value(ea, reg)` - find constant value in register at address
- `find_sp_value(ea, reg)` - find stack pointer delta at address
- `find_reg_value_info(rvi, ea, reg, max_depth)` - find register value with detailed tracking info
- `find_nearest_rvi(rvi, ea, regs)` - find value of either of two registers
- `invalidate_regfinder_cache(from, to, cref)` - update cache after control flow change
- `invalidate_regfinder_xrefs_cache(to, dref)` - update cache after data reference change

Returns: 1 if value found, 0 if varying/insufficient depth, -1 if not supported.

## Key Classes

### reg_value_info_t
Detailed register value tracking result.

**State checks:**
- `is_num()` / `is_spd()` - value is constant / stack-pointer-relative
- `is_known()` - value is num or spd
- `is_unknown()` - value could not be determined
- `is_dead_end()` / `aborted()` - tracking stopped
- `is_unkloop()` / `is_unkxref()` / `is_unkvals()` / `is_unkmult()` - specific failure reasons
- `is_value_unique()` - single value vs multiple possibilities

**Value extraction:**
- `get_num()` - get constant value
- `get_spd()` - get SP delta
- `get_def_ea()` - where value was defined
- `get_def_itype()` - instruction type that defined value

**Arithmetic operations (all take insn parameter):**
- `add(r, insn)` / `sub(r, insn)` - arithmetic
- `bor(r, insn)` / `band(r, insn)` / `bxor(r, insn)` / `bandnot(r, insn)` - bitwise
- `sll(r, insn)` / `slr(r, insn)` / `sar(r, insn)` - shifts
- `neg(insn)` / `bnot(insn)` - unary
- `add_num(r)` / `shift_left(r)` / `shift_right(r)` - without changing def_ea

**Factory methods:**
- `make_num(val, insn/ea, flags)` - create constant value
- `make_initial_sp(func_ea)` - create initial stack pointer
- `make_unkloop(ea)` / `make_unkmult(ea)` / etc - create failure states

**Flags (for PC_BASED / LIKE_GOT annotations):**
- `is_all_vals_pc_based()` / `is_any_vals_pc_based()`
- `is_all_vals_like_got()` / `is_any_vals_like_got()`
- `set_all_vals_pc_based()` / `set_all_vals_got_based()`

### reg_value_def_t
Single value definition.

- `val` - the value (uint64)
- `def_ea` - instruction address where defined
- `def_itype` - instruction code (processor-specific)
- `flags` - SHORT_INSN, PC_BASED, LIKE_GOT
- `is_short_insn()` / `is_pc_based()` / `is_like_got()` - flag checks
- `dstr(how, pm)` - format as string (NOVAL/UVAL/SPVAL/ABORTED)

## Configuration

Uses ida.cfg values: `REGTRACK_MAX_DEPTH`, `REGTRACK_FUNC_MAX_DEPTH` for search limits.

## See Also
Full docs: skill/docs/ida_regfinder.rst

# ida_offset

Medium-priority: Convert operands to offset references and calculate target addresses. Useful when analyzing code that references data structures or global variables.

## Key Functions

- `op_offset_ex(ea, n, ri)` - convert operand to reference using refinfo_t
- `op_offset(ea, n, ri)` - alias for op_offset_ex
- `op_plain_offset(ea, n, base)` - convert operand to reference with default type
- `get_offbase(ea, n)` - get offset base value for operand
- `get_offset_expression(ea, n, from, offset, flags)` - format offset as "name+displ" string
- `calc_offset_base(ea, n)` - calculate offset base from fixup/segment info
- `calc_target(from, ea, n, opval)` - calculate target address from offset reference
- `calc_basevalue(target, base)` - calculate reference base value
- `can_be_off32(ea)` - check if address contains valid OFF32, return target or BADADDR

Operand numbers may be ORed with OPND_OUTER for Motorola outer offsets.

## See Also
Full docs: skill/docs/ida_offset.rst

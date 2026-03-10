# ida_fixup

Relocation/fixup information for loaders - manage target addresses, offsets, and displacement values.

## Key Functions

- `get_fixup(fd, source) -> bool` - Get fixup information at address
- `exists_fixup(source) -> bool` - Check if fixup exists
- `set_fixup(source, fd)` - Set fixup information (loaders use this)
- `del_fixup(source)` - Delete fixup
- `get_first_fixup_ea() -> ea_t` - Get first fixup address
- `get_next_fixup_ea(ea) -> ea_t` - Next fixup after ea
- `get_prev_fixup_ea(ea) -> ea_t` - Previous fixup before ea
- `get_fixup_value(ea, type) -> int` - Read bytes and convert to operand value (get relocation addend)
- `patch_fixup_value(ea, fd) -> bool` - Update bytes from fixup data
- `get_fixup_desc(source, fd) -> str` - Get description comment
- `calc_fixup_size(type) -> int` - Calculate fixup size in bytes (-1 on error)
- `contains_fixups(ea, size) -> bool` - Check if range contains fixups
- `gen_fix_fixups(from, to, size)` - Relocate bytes when moving segments/rebasing

## fixup_data_t Class

Fixup metadata container.

### Attributes
- `sel: sel_t` - Target segment selector (BADSEL for absolute)
- `off: ea_t` - Target offset
- `displacement: adiff_t` - Displacement from target

### Methods
- `get_type() -> fixup_type_t`, `set_type(type)` - Fixup type access
- `set_type_and_flags(type, flags=0)` - Set both type and flags
- `is_custom() -> bool` - Is processor-specific fixup
- `get_flags() -> int` - Get flags
- `is_extdef() -> bool`, `set_extdef()`, `clr_extdef()` - Target is symbol vs segment offset
- `is_unused() -> bool`, `set_unused()`, `clr_unused()` - IDA ignores this fixup
- `has_base() -> bool` - Is relative fixup (vs segment-relative)
- `was_created() -> bool` - Was created by IDA (not in original file)
- `get_base() -> ea_t`, `set_base(new_base)` - Base address for relative fixups
- `set(source)` - set_fixup wrapper
- `get(source) -> bool` - get_fixup wrapper
- `calc_size() -> int` - Fixup size

## Fixup Types (FIXUP_*)

- `FIXUP_OFF8`, `FIXUP_OFF16`, `FIXUP_OFF32`, `FIXUP_OFF64` - Unsigned offsets (8/16/32/64-bit)
- `FIXUP_OFF8S`, `FIXUP_OFF16S`, `FIXUP_OFF32S` - Signed offsets
- `FIXUP_SEG16` - 16-bit segment selector
- `FIXUP_PTR16` - 32-bit pointer (16:16 base:offset)
- `FIXUP_PTR32` - 48-bit pointer (16:32 base:offset)
- `FIXUP_HI8`, `FIXUP_HI16` - High 8/16 bits of offset
- `FIXUP_LOW8`, `FIXUP_LOW16` - Low 8/16 bits of offset
- `FIXUP_CUSTOM` - Start of custom (processor-specific) types

## Fixup Flags (FIXUPF_*)

- `FIXUPF_REL` - Relative to linear address `base` (else segment-relative)
- `FIXUPF_EXTDEF` - Target is symbol (else segment offset)
- `FIXUPF_UNUSED` - Ignored by IDA, disables operand conversion
- `FIXUPF_CREATED` - Not present in input file
- `FIXUPF_LOADER_MASK` - Loader-specific flags (not stored in DB)

## See Also
Full docs: skill/docs/ida_fixup.rst

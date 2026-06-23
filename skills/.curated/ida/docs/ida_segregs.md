# ida_segregs

Segment register management for architectures with segmented memory (x86/x86-64).

## Key Classes

### sreg_range_t
Segment register value range (inherits from range_t).
- `val` - Segment register value (sel_t)
- `tag` - Range tag (SR_inherit/SR_user/SR_auto/SR_autostart)

## Key Functions

### Reading Values
- `get_sreg(ea, rg)` - Get segment register value at address (uses ranges + segment defaults)

### Setting Values
- `split_sreg_range(ea, rg, v, tag, silent=False)` - Create new range at address
- `set_default_sreg_value(sg, rg, value)` - Set default for segment (or all segments if sg=None)
- `set_default_dataseg(ds_sel)` - Set DS default for all segments
- `set_sreg_at_next_code(ea1, ea2, rg, value)` - Set value at next instruction only

### Range Queries
- `get_sreg_range(out, ea, rg)` - Get range containing address
- `get_prev_sreg_range(out, ea, rg)` - Get previous range
- `get_sreg_ranges_qty(rg)` - Get number of ranges
- `getn_sreg_range(out, rg, n)` - Get range by index
- `get_sreg_range_num(ea, rg)` - Get range index by address

### Range Management
- `del_sreg_range(ea, rg)` - Delete range (extends previous, can't delete segment start)
- `copy_sreg_ranges(dst_rg, src_rg, map_selector=False)` - Duplicate ranges

## Segment Register Constants

### x86/x86-64 Registers
- `R_es` - Extra segment
- `R_cs` - Code segment
- `R_ss` - Stack segment
- `R_ds` - Data segment
- `R_fs` - FS segment
- `R_gs` - GS segment

### Range Tags
- `SR_inherit` - Value inherited from previous range
- `SR_user` - User-specified value
- `SR_auto` - IDA-determined value
- `SR_autostart` - Used as SR_auto at segment start

## Usage Notes

For non-segmented architectures, define two virtual segment registers (CS/DS) and set processor_t::reg_code_sreg and processor_t::reg_data_sreg.

## See Also
Full docs: skill/docs/ida_segregs.rst

# ida_bitrange

Bitfield and bit-level range operations (low-priority, specialized use).

## Key Class

### bitrange_t
Represents a range of bits within a larger value.

- `init(bit_ofs, size_in_bits)` - Initialize offset and size
- `reset()` - Make empty
- `empty()` - Check if empty
- `bitoff()` / `bitsize()` / `bytesize()` - Get offset/size
- `mask64()` - Convert to 64-bit mask
- `has_common(r)` - Check overlap with another bitrange
- `intersect(r)` - Intersect two ranges
- `create_union(r)` - Union including hole between ranges
- `shift_down(cnt)` / `shift_up(cnt)` - Shift range left/right

## See Also
Full docs: skill/docs/ida_bitrange.rst

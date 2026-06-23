# ida_range

Medium-priority: Manage continuous address ranges and sets of ranges. Commonly used for working with functions, segments, and custom address groups.

## Key Classes

### range_t
Continuous address range [start_ea, end_ea), end excluded.

- `range_t(ea1, ea2)` - constructor
- `start_ea` / `end_ea` - range boundaries (end_ea excluded)
- `contains(ea)` / `contains(range)` - check if address/range is inside
- `overlaps(range)` - check if ranges have common addresses
- `size()` - return end_ea - start_ea
- `empty()` - check if size <= 0
- `intersect(range)` - set to intersection with another range
- `extend(ea)` - extend range to include address
- `clear()` - set both start_ea and end_ea to 0
- `compare(range)` - compare based on start_ea

### rangeset_t
Set of non-overlapping ranges, stored sorted.

- `add(range)` / `add(start, end)` / `add(rangeset)` - add range(s), merging overlaps
- `sub(range)` / `sub(ea)` / `sub(rangeset)` - subtract range(s), splitting as needed
- `contains(ea)` / `contains(rangeset)` - check membership
- `includes(range)` - check if every ea in range is in set
- `has_common(range)` / `has_common(rangeset)` - check overlap
- `intersect(rangeset)` - set to intersection
- `find_range(ea)` - get range containing ea, or nullptr
- `nranges()` - number of ranges in set
- `getrange(idx)` - get range by index
- `next_addr(ea)` / `prev_addr(ea)` - navigate within ranges
- `next_range(ea)` / `prev_range(ea)` - navigate between ranges
- `is_equal(rangeset)` / `is_subset_of(rangeset)` - set comparisons
- `clear()` / `empty()` - management

### rangevec_t
Vector of range_t (standard vector methods).

## Range Kind Constants

- `RANGE_KIND_FUNC` - function ranges
- `RANGE_KIND_SEGMENT` - segment ranges
- `RANGE_KIND_HIDDEN_RANGE` - hidden ranges
- `RANGE_KIND_UNKNOWN` - unknown type

## See Also
Full docs: skill/docs/ida_range.rst

# ida_lines

Line rendering and text generation for disassembly output.

## Key Functions

### Line Generation
- `generate_disasm_line(ea, flags)` - generate disassembly line at ea
- `generate_many_lines(ea, flags)` - generate multiple lines (includes function header, etc.)
- `tag_remove(tagged_line)` - remove color tags from line
- `tag_skipcode(p)` - skip color tag at position
- `tag_advance(p, cnt)` - advance by cnt printable characters

### Color Tags
- `SCOLOR_*` constants - color tag markers (instructions, registers, comments, etc.)
- Lines contain embedded color codes (e.g., `\x01` for instruction color)

### Line Prefix/Suffix
- `gl_comm` / `set_gl_comm(start, end)` - comment delimiters
- `inf_get_indent()` - get indentation amount

## Common Use Cases

Generate colored disassembly:
```python
line = ida_lines.generate_disasm_line(ea, 0)
plain = ida_lines.tag_remove(line)
```

## Low Priority

This module is mostly for display formatting. Core analysis uses ida_ua (instruction decoding) and ida_bytes (data access) instead.

## See Also
Full docs: skill/docs/ida_lines.rst

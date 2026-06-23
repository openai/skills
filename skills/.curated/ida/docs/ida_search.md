# ida_search

Middle-level search functions for finding specific byte patterns, instructions, and code/data.

## Key Functions

### Search Functions
- `find_unknown(ea, sflag)` - Find undefined bytes
- `find_defined(ea, sflag)` - Find defined bytes (code/data)
- `find_code(ea, sflag)` - Find code (instructions)
- `find_data(ea, sflag)` - Find data items
- `find_not_func(ea, sflag)` - Find bytes outside functions
- `find_imm(ea, sflag, search_value)` - Find immediate value in instructions
- `find_text(start_ea, y, x, ustr, sflag)` - Text search in disassembly/decompilation
- `find_reg_access(out, start_ea, end_ea, regname, sflag)` - Find register read/write

### Helper
- `search_down(sflag)` - Check if SEARCH_DOWN bit is set

## Search Flags

### Direction
- `SEARCH_UP` - Search towards lower addresses
- `SEARCH_DOWN` - Search towards higher addresses
- `SEARCH_NEXT` - Skip starting address

### Options
- `SEARCH_CASE` - Case-sensitive search
- `SEARCH_REGEX` - Regular expressions (text search only)
- `SEARCH_IDENT` - Search for identifier (bounded by non-visible chars)
- `SEARCH_NOBRK` - Don't test for user cancellation
- `SEARCH_NOSHOW` - Don't display progress
- `SEARCH_BRK` - Return BADADDR if cancelled
- `SEARCH_USESEL` - Limit search to UI selection

### Register Access
- `SEARCH_USE` - Find register reads
- `SEARCH_DEF` - Find register writes

## See Also
Full docs: skill/docs/ida_search.rst

# ida_ida

Database-wide configuration via the `inf` structure - processor info, file type, address ranges, and analysis flags.

## Key Functions

### Database Properties
- `inf_get_min_ea()`, `inf_set_min_ea(ea)` - Database address range start
- `inf_get_max_ea()`, `inf_set_max_ea(ea)` - Database address range end
- `inf_get_start_ea()`, `inf_set_start_ea(ea)` - Entry point address
- `inf_get_baseaddr()`, `inf_set_baseaddr(ea)` - Image base address
- `inf_get_main()`, `inf_set_main(ea)` - Main function address

### Architecture Info
- `inf_is_16bit()`, `inf_is_32bit_exactly()`, `inf_is_64bit()` - Architecture bit width
- `inf_set_32bit(v)`, `inf_set_64bit(v)` - Set architecture
- `inf_is_be()`, `inf_set_be(v)` - Big-endian check/set
- `inf_is_dll()`, `inf_set_dll(v)` - DLL vs executable

### File Information
- `inf_get_procname()`, `inf_set_procname(name)` - Processor name (x86, ARM, etc.)
- `inf_get_filetype()`, `inf_set_filetype(ft)` - File type (f_PE, f_ELF, f_MACHO, etc.)
- `inf_get_md5()`, `inf_get_sha256()` - File hashes
- `inf_get_input_file_path()` - Original input file path
- `inf_get_imagebase()` - PE/ELF image base

### Analysis Flags
- `inf_get_af()`, `inf_set_af(flags)` - Get/set all analysis flags
- `inf_get_af2()`, `inf_set_af2(flags)` - Secondary analysis flags
- Analysis flag constants: AF_CODE, AF_JUMPTBL, AF_PROC, AF_LVAR, AF_TRACE, AF_FLIRT, etc.

### Display Options
- `inf_is_graph_view()`, `inf_set_graph_view(v)` - Default to graph vs text view
- `inf_get_indent()`, `inf_set_indent(n)` - Disassembly indentation
- `inf_get_margin()`, `inf_set_margin(n)` - Right margin

### Database State
- `inf_is_auto_enabled()`, `inf_set_auto_enabled(v)` - Auto-analysis state
- `inf_readonly_idb()`, `inf_set_readonly_idb(v)` - Read-only mode
- `inf_get_database_change_count()` - Change counter (for caching)

### Compiler Info
- `inf_get_cc_id()`, `inf_set_cc_id(id)` - Calling convention ID
- `inf_get_cc_size_i()`, `inf_get_cc_size_l()` - sizeof(int), sizeof(long)
- `inf_get_abibits()`, `inf_set_abibits(bits)` - ABI flags

## Key Constants

**File types**: f_PE, f_ELF, f_MACHO, f_BIN, f_COFF, f_OMF, f_AOUT, f_HEX

**Analysis flags**: AF_CODE (create instructions), AF_JUMPTBL (analyze jump tables), AF_PROC (create functions), AF_LVAR (local variables), AF_FLIRT (apply FLIRT signatures)

**Loader flags**: LFLG_64BIT, LFLG_IS_DLL, LFLG_PC_FLAT (flat memory model)

**Name display**: NM_REL_OFF (show offsets), NM_EA (show addresses), NM_SHORT (short names)

**Demangling**: DEMNAM_GCC3 (GCC v3 ABI), DEMNAM_CMNT (show in comments), DEMNAM_NAME (show as name)

## See Also
Full docs: skill/docs/ida_ida.rst

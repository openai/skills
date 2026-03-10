# ida_nalt

Netnode-based storage for various analysis information - switch tables, references, types, strings, imports, metadata.

## Key Functions

### Netnode Access
- `ea2node(ea)` / `node2ea(node)` - Convert between addresses and netnodes
- `end_ea2node(ea, size)` - Get netnode for address range end
- `getnode(ea)` - Get netnode for address

### Address Flags (AFL_*)
Extensive flag system for tracking analysis state at addresses.

#### Query Flags
- `get_aflags(ea)` / `set_aflags(ea, flags)` / `del_aflags(ea)` - Get/set/delete flags
- `upd_abits(ea, set, clr)` / `set_abits(ea, bits)` / `clr_abits(ea, bits)` - Update address bits
- `is_hidden_item(ea)` / `hide_item(ea)` / `unhide_item(ea)` - Item visibility
- `is_hidden_border(ea)` / `hide_border(ea)` / `unhide_border(ea)` - Border visibility
- `is_colored_item(ea)` / `set_colored_item(ea)` / `clr_colored_item(ea)` - Colored items
- `is_usersp(ea)` / `set_usersp(ea)` / `clr_usersp(ea)` - User stack pointer
- `uses_modsp(ea)` / `set_usemodsp(ea)` / `clr_usemodsp(ea)` - Modified stack pointer
- `is_libitem(ea)` / `set_libitem(ea)` / `clr_libitem(ea)` - Library item
- `is_noret(ea)` / `set_noret(ea)` / `clr_noret(ea)` - No-return function
- `is_notcode(ea)` / `set_notcode(ea)` / `clr_notcode(ea)` - Not code
- `is_notproc(ea)` / `set_notproc(ea)` / `clr_notproc(ea)` - Not procedure
- `is_type_guessed_by_ida(ea)` / `set_type_guessed_by_ida(ea)` - IDA type guess
- `is_func_guessed_by_hexrays(ea)` / `set_func_guessed_by_hexrays(ea)` - Hex-Rays function guess
- `is_data_guessed_by_hexrays(ea)` / `set_data_guessed_by_hexrays(ea)` - Hex-Rays data guess
- `is_type_determined_by_hexrays(ea)` / `set_type_determined_by_hexrays(ea)` - Hex-Rays type determination

### Type Information
- `get_tinfo(tif, ea)` / `set_tinfo(ea, tif)` / `del_tinfo(ea)` - Address type info
- `get_op_tinfo(tif, ea, opnum)` / `set_op_tinfo(ea, opnum, tif)` / `del_op_tinfo(ea, opnum)` - Operand type info
- `has_ti(ea)` / `has_ti0(ea)` / `has_ti1(ea)` - Check if type info exists

### String Types
- `get_str_type(ea)` / `set_str_type(ea, strtype)` / `del_str_type(ea)` - String type at address
- `get_str_type_code(strtype)` - Get string type code
- `get_str_term1(strtype)` / `get_str_term2(strtype)` - String terminators
- `get_str_encoding_idx(ea)` / `set_str_encoding_idx(ea, idx)` - String encoding
- `make_str_type(base, lyt)` - Construct string type code
- `is_pascal(strtype)` - Check if Pascal string
- `get_str_type_prefix_length(strtype)` - Get prefix length

### References and Offsets
- `get_refinfo(ri, ea, opnum)` / `set_refinfo(ea, opnum, type, target, base, tdelta)` / `del_refinfo(ea, opnum)` - Reference info
- `set_refinfo_ex(ea, opnum, ri)` - Set reference info with refinfo_t
- `get_custom_refinfo(out, cfmt)` / `find_custom_refinfo(cfmt)` - Custom reference formats
- `get_reftype_by_size(size)` - Get reference type by size
- `is_reftype_target_optional(rt)` - Check if target is optional

### Switch Tables
- `get_switch_info(si, ea)` / `set_switch_info(ea, si)` / `del_switch_info(ea)` - Switch info
- `get_switch_parent(ea)` / `set_switch_parent(ea, parent)` / `del_switch_parent(ea)` - Switch parent

### Arrays
- `get_array_parameters(out, ea)` / `set_array_parameters(ea, params)` / `del_array_parameters(ea)` - Array display parameters

### Custom Data Types
- `get_custom_data_type_ids(out, ea)` / `set_custom_data_type_ids(ea, ids)` / `del_custom_data_type_ids(ea)` - Custom data types

### Colors and Alignment
- `get_item_color(ea)` / `set_item_color(ea, color)` / `del_item_color(ea)` - Item color
- `get_alignment(ea)` / `set_alignment(ea, align)` / `del_alignment(ea)` - Alignment

### Source Line Numbers
- `get_source_linnum(ea)` / `set_source_linnum(ea, lnnum)` / `del_source_linnum(ea)` - Source line mapping

### Absolute Base
- `get_absbase(ea)` / `set_absbase(ea, base)` / `del_absbase(ea)` - Absolute segment base

### File Metadata
- `get_root_filename()` / `set_root_filename(path)` - Input file root name
- `get_input_file_path()` - Input file full path
- `dbg_get_input_path()` - Debugger input path
- `retrieve_input_file_size()` - File size
- `retrieve_input_file_crc32()` / `retrieve_input_file_md5()` / `retrieve_input_file_sha256()` - File hashes
- `get_archive_path()` / `set_archive_path(path)` - Archive path
- `get_loader_format_name()` / `set_loader_format_name(name)` - Loader format

### IDB Version and Timing
- `get_initial_ida_version()` / `get_initial_idb_version()` - IDA/IDB versions
- `get_idb_ctime()` - IDB creation time
- `get_elapsed_secs()` - Analysis elapsed time
- `get_idb_nopens()` - IDB open count

### Image Base
- `get_imagebase()` / `set_imagebase(base)` - Image base address

### String Encodings
- `get_encoding_qty()` - Number of encodings
- `get_encoding_name(idx)` - Encoding name
- `add_encoding(name, bpu)` / `del_encoding(idx)` / `rename_encoding(idx, name)` - Manage encodings
- `get_encoding_bpu(idx)` / `get_encoding_bpu_by_name(name)` - Bytes per unit
- `get_strtype_bpu(strtype)` - String type bytes per unit
- `get_default_encoding_idx()` / `set_default_encoding_idx(idx)` - Default encoding
- `get_outfile_encoding_idx()` / `set_outfile_encoding_idx(idx)` - Output file encoding
- `encoding_from_strtype(strtype)` - Get encoding from string type

### Imports
- `get_import_module_qty()` - Number of import modules
- `get_import_module_name(idx)` - Import module name
- `enum_import_names(idx, callback)` - Enumerate imports
- `delete_imports()` - Delete all imports

### GOT/PLT
- `get_gotea()` / `set_gotea(ea)` - Global Offset Table address

### Notepad
- `get_ida_notepad_text()` / `set_ida_notepad_text(text)` - IDA notepad text

### Source Debug Paths
- `get_srcdbg_paths()` / `set_srcdbg_paths(paths)` - Source debug paths
- `get_srcdbg_undesired_paths()` / `set_srcdbg_undesired_paths(paths)` - Undesired debug paths

### Assembly Include
- `get_asm_inc_file()` / `set_asm_inc_file(file)` - Assembly include file

### IDS Modules
- `get_ids_modnode()` / `set_ids_modnode(node)` - IDS module netnode

### ABI
- `get_abi_name()` - ABI name

## Key Classes

### switch_info_t
Switch statement information.
- `flags` - Switch flags (SWI_*)
- `ncases` - Number of cases (excluding default)
- `jumps` - Jump table start address
- `values` - Values table address (if SWI_SPARSE)
- `lowcase` - Lowest case value
- `defjump` - Default jump address (BADADDR if none)
- `startea` - Start of switch idiom
- `jcases` - Jump table entries (if SWI_INDIRECT)
- `elbase` - Element base
- `regnum` / `regdtype` - Switch expression register
- `get_jtable_size()` / `set_jtable_size(size)` - Jump table size
- `get_jtable_element_size()` / `set_jtable_element_size(size)` - Element size
- `has_default()` / `is_sparse()` / `is_custom()` / `is_indirect()` / `is_subtract()` - Query flags

### refinfo_t
Reference/offset information.
- `target` - Reference target (BADADDR if none)
- `base` - Base of reference (may be BADADDR)
- `tdelta` - Offset from target
- `flags` - Reference flags (REFINFO_*)
- `type()` / `set_type(rt)` - Reference type (REF_OFF16, REF_OFF32, REF_OFF64, etc.)
- `is_target_optional()` / `no_base_xref()` / `is_pastend()` / `is_rvaoff()` / `is_custom()` / `is_subtract()` / `is_signed()` - Query flags
- `init()` - Initialize

### array_parameters_t
Array display parameters.
- `flags` - Array flags (AP_*)
- `lineitems` - Items per line
- `alignment` - Item alignment (-1=don't align, 0=auto, else width)
- `is_default()` - Check if default

### opinfo_t
Operand type information union (structure/enum/strpath/custom).

### strpath_t
Structure path for nested structure member offsets.

### enum_const_t
Enumeration constant reference.

## Key Constants

### String Types (STRTYPE_*)
- `STRTYPE_TERMCHR` / `STRTYPE_C` / `STRTYPE_C_16` / `STRTYPE_C_32` - C strings
- `STRTYPE_PASCAL` / `STRTYPE_PASCAL_16` / `STRTYPE_PASCAL_32` - Pascal strings
- `STRTYPE_LEN2` / `STRTYPE_LEN2_16` / `STRTYPE_LEN2_32` - 2-byte length prefix
- `STRTYPE_LEN4` / `STRTYPE_LEN4_16` / `STRTYPE_LEN4_32` - 4-byte length prefix

### String Layout (STRLYT_*)
- `STRLYT_TERMCHR` / `STRLYT_PASCAL1` / `STRLYT_PASCAL2` / `STRLYT_PASCAL4` - Layout types

### String Width (STRWIDTH_*)
- `STRWIDTH_1B` / `STRWIDTH_2B` / `STRWIDTH_4B` - Character width

### Reference Types (REF_*)
- `REF_OFF16` / `REF_OFF32` / `REF_OFF64` - Full offsets
- `REF_LOW8` / `REF_LOW16` / `REF_HIGH8` / `REF_HIGH16` - Partial offsets

### Reference Info Flags (REFINFO_*)
- `REFINFO_RVAOFF` - RVA offset
- `REFINFO_PASTEND` - Past end of segment
- `REFINFO_CUSTOM` - Custom format
- `REFINFO_NOBASE` - No base
- `REFINFO_SUBTRACT` - Subtract instead of add
- `REFINFO_SIGNEDOP` - Signed operand

### Switch Info Flags (SWI_*)
- `SWI_SPARSE` - Sparse switch (has values table)
- `SWI_V32` / `SWI_J32` - 32-bit values/jumps
- `SWI_USER` - User-defined
- `SWI_CUSTOM` - Custom switch
- `SWI_INDIRECT` - Indirect jump table

### Address Flags (AFL_*)
Extensive flag set including: AFL_LINNUM, AFL_USERSP, AFL_PUBNAM, AFL_WEAKNAM, AFL_HIDDEN, AFL_MANUAL, AFL_NOBRD, AFL_ZSTROFF, AFL_LIB, AFL_TI, AFL_COLORED, AFL_NORET, AFL_FIXEDSPD, AFL_ALIGNFLOW, AFL_USERTI, AFL_RETFP, AFL_USEMODSP, AFL_NOTCODE, AFL_NOTPROC, and type guessing flags.

### Root Info Indices (RIDX_*)
Database-level metadata keys: RIDX_FILE_FORMAT_NAME, RIDX_MD5, RIDX_SHA256, RIDX_IDA_VERSION, RIDX_STR_ENCODINGS, RIDX_SRCDBG_PATHS, RIDX_DBG_BINPATHS, RIDX_ABINAME, RIDX_ARCHIVE_PATH, RIDX_PROBLEMS, etc.

## See Also
Full docs: skill/docs/ida_nalt.rst

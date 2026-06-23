# ida_bytes

Byte-level operations: reading, writing, patching, flags, and data type creation.

## Navigation

### Head/Item Navigation
- `next_head(ea, maxea)` / `prev_head(ea, minea)` - Next/prev item head
- `get_item_head(ea)` - Get start of item containing ea
- `get_item_end(ea)` - Get address after item
- `get_item_size(ea)` - Get item size in bytes
- `next_chunk(ea, maxea)` / `prev_chunk(ea, minea)` - Next/prev contiguous chunk
- `next_unknown(ea, maxea)` / `prev_unknown(ea, minea)` - Next/prev undefined byte

## Reading Bytes

### Single Values
- `get_byte(ea)` / `get_word(ea)` / `get_dword(ea)` / `get_qword(ea)` - Read values
- `get_original_byte(ea)` - Read original file byte (before patches)
- `get_wide_byte(ea)` / `get_wide_word(ea)` - Read with byte size from inf.cc.size_i/size_s
- `get_data_value(ea, size)` - Read data item value (up to 64 bits)

### Bulk Operations
- `get_bytes(ea, size, gmb_flags=GMB_READALL)` - Read byte array
- `get_bytes_and_mask(ea, size, gmb_flags)` - Read bytes + mask (for wildcards)
- `get_strlit_contents(ea, length, strtype)` - Extract string literal

## Writing/Patching Bytes

### Patching (modifies IDB + file)
- `patch_byte(ea, value)` / `patch_word(ea)` / `patch_dword(ea)` / `patch_qword(ea)` - Patch values
- `patch_bytes(ea, buf)` - Patch byte array
- `revert_byte(ea)` - Revert to original file byte

### IDB Only (no file modification)
- `put_byte(ea, value)` / `put_word(ea)` / `put_dword(ea)` / `put_qword(ea)` - Update IDB only
- `put_bytes(ea, buf)` - Update byte array in IDB

## Flags & Type Checking

### Item Type
- `is_code(flags)` / `is_data(flags)` / `is_unknown(flags)` - Check item type
- `is_byte(ea)` / `is_word(ea)` / `is_dword(ea)` / `is_qword(ea)` - Check data size
- `is_strlit(ea)` - Check if string literal
- `is_struct(ea)` - Check if structure
- `is_tail(ea)` - Check if tail byte (not item head)

### Flag Operations
- `get_flags(ea)` - Get flags for address
- `get_full_flags(ea)` - Get full flags (includes hidden/extra data)

## Creating Data Items

### Basic Types
- `create_byte(ea, length, force=False)` - Create byte array
- `create_word(ea, length, force)` - Create word array
- `create_dword(ea, length, force)` - Create dword array
- `create_qword(ea, length, force)` - Create qword array
- `create_float(ea)` / `create_double(ea)` / `create_packed_real(ea)` - Create floats

### String & Struct
- `create_strlit(ea, length, strtype)` - Create string literal
- `create_struct(ea, size, tid)` - Apply structure at address
- `del_items(ea, flags=0, nbytes=1)` - Undefine items in range

## Searching

### Pattern Search
- `find_bytes(bs, range_start, range_size, mask, flags)` - Find byte pattern
- `bin_search(start, end, pattern, flags)` - Binary pattern search
- `parse_binpat_str(pattern, radix, strlits)` - Parse pattern string to compiled form

### Simple Search
- `find_byte(sEA, size, value, flags)` - Find single byte value
- `find_byter(sEA, size, value, flags)` - Find byte (reverse direction)

## Operand Representation

### Number Display
- `op_hex(ea, n)` / `op_dec(ea, n)` / `op_oct(ea, n)` / `op_bin(ea, n)` - Set operand radix
- `op_chr(ea, n)` - Display as character
- `op_num(ea, n)` - Display as number (default radix)
- `toggle_sign(ea, n)` - Toggle sign display

### Complex Types
- `op_offset(ea, n, reftype, target, base, tdelta)` - Create offset reference
- `op_enum(ea, n, enum_id, serial)` - Apply enum
- `op_stroff(ea, n, path, path_len, delta)` - Create structure offset
- `op_stkvar(ea, n)` - Reference stack variable

## Comments
- `get_cmt(ea, rptble)` / `set_cmt(ea, comm, rptble)` - Get/set comment
- `append_cmt(ea, str, rptble)` - Append to comment

## Constants

### Item Type Flags
- `FF_CODE` / `FF_DATA` / `FF_TAIL` / `FF_UNK` - Main type flags
- `FF_BYTE` / `FF_WORD` / `FF_DWORD` / `FF_QWORD` - Data size flags

### Search Flags
- `BIN_SEARCH_FORWARD` / `BIN_SEARCH_BACKWARD` - Search direction
- `BIN_SEARCH_CASE` / `BIN_SEARCH_NOCASE` - Case sensitivity
- `BIN_SEARCH_NOSHOW` - Suppress progress dialog

## See Also
Full docs: skill/docs/ida_bytes.rst

# idadex

DEX (Dalvik Executable) file parsing utilities for Android reverse engineering.

## Key Classes

### Dex
Primary DEX file parser exposing methods/fields/strings/types from Android binaries.

**String Operations**:
- `get_string(from_ea, string_idx)` - retrieve string by index
- `as_string(s)` - convert DEX string to Python string

**Method Operations**:
- `get_method(from_ea, method_idx)` - retrieve method by index
- `get_method_name(from_ea, method_idx)` - get method name
- `get_short_method_name(method)` - short form (e.g., `onCreate`)
- `get_full_method_name(method)` - fully qualified (e.g., `android.app.Activity.onCreate`)
- `get_call_method_name(method)` - name for call sites

**Type Operations**:
- `get_type_string(from_ea, type_idx)` - get type descriptor
- `decorate_java_typename(desc)` - convert type descriptor to Java notation
- `is_wide_type(typechar)` - check if type is 64-bit

**Field Operations**:
- `get_field(from_ea, field_idx)` - retrieve field by index
- `get_field_name(from_ea, field_idx)` - get field name
- `get_full_field_name(field_idx, field, field_name)` - fully qualified field name

**Utility**:
- `access_string(flags)` - convert access flags to string (public/private/etc)
- `idx_to_ea(from_ea, idx, tag)` - convert DEX index to IDA address

### dex_method
`ctypes.LittleEndianStructure` representing DEX method metadata.
- `IS_LOCAL = 1` - flag for local method
- `HAS_CODE = 2` - flag indicating method has code
- `is_local()` - check if method is local

### dex_field
`ctypes.LittleEndianStructure` representing DEX field metadata.

## Key Functions

- `to_uint32(v)` - convert to unsigned 32-bit int
- `unpack_db(buf, off)` - unpack byte from buffer
- `unpack_dw(buf, off)` - unpack word from buffer
- `unpack_dd(buf, off)` - unpack dword from buffer
- `unpack_dq(buf, off)` - unpack qword from buffer
- `unpack_ea(buf, off)` - unpack effective address from buffer

## Global Object

### dex
Global `Dex` instance - use this to access DEX parsing functions.

## See Also
Full docs: skill/docs/idadex.rst

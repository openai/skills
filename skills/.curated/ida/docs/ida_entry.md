# ida_entry

Entry point and exported function management - addresses, names, and ordinal numbers.

## Key Functions

- `get_entry_qty() -> int` - Get number of entry points
- `add_entry(ord, ea, name, makecode, flags=0) -> bool` - Add entry point with ordinal number
- `get_entry(ord) -> ea_t` - Get address by ordinal number
- `get_entry_ordinal(idx) -> int` - Get ordinal by index (0..get_entry_qty()-1)
- `get_entry_name(ord) -> str` - Get entry point name by ordinal
- `rename_entry(ord, name, flags=0) -> bool` - Rename entry point
- `set_entry_forwarder(ord, name, flags=0) -> bool` - Set forwarder name (for DLL exports)
- `get_entry_forwarder(ord) -> str` - Get forwarder name

## Flags (AEF_*)

- `AEF_UTF8` - Name is UTF-8 encoded (default)
- `AEF_IDBENC` - Name is IDB encoded (implies AEF_NODUMMY)
- `AEF_NODUMMY` - Prepend '_' if name begins with dummy suffix
- `AEF_WEAK` - Make name weak
- `AEF_NOFORCE` - Append to comment if name exists (unless old name is weak)

## See Also
Full docs: skill/docs/ida_entry.rst

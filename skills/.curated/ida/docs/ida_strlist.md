# ida_strlist

String list management (cached view of all strings in the database).

## Key Classes

### string_info_t
String list entry.
- `ea` - String address
- `length` - String length
- `type` - String type

### strwinsetup_t
String list configuration.
- `minlen` - Minimum string length
- `display_only_existing_strings` - Only show defined strings
- `only_7bit` - ASCII-only strings
- `ignore_heads` - Include strings at non-head addresses
- `strtypes` - Enabled string types

## Key Functions

- `build_strlist()` - Rebuild string list (expensive, call when needed)
- `clear_strlist()` - Clear string list
- `get_strlist_qty()` - Get number of strings (loads from DB or builds)
- `get_strlist_item(si, n)` - Get nth string (0..qty-1)
- `get_strlist_options()` - Get static configuration

## Usage Notes

The kernel does NOT auto-update the string list (performance). Users must call build_strlist() for up-to-date results. If not cleared, the list persists in the database across sessions.

## See Also
Full docs: skill/docs/ida_strlist.rst

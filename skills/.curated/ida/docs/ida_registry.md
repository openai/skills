# ida_registry

Registry-based persistent configuration storage (Windows registry or ~/.idapro/ida.reg on Unix).

## Key Functions

### Configuration Storage
- `reg_read_string(name, subkey=None, _def=None)` - Read string value
- `reg_write_string(name, utf8, subkey=None)` - Write string value
- `reg_read_int(name, defval, subkey=None)` - Read integer value
- `reg_write_int(name, value, subkey=None)` - Write integer value
- `reg_read_bool(name, defval, subkey=None)` - Read boolean value
- `reg_write_bool(name, value, subkey=None)` - Write boolean value
- `reg_read_binary(name, subkey=None)` - Read binary data
- `reg_write_binary(name, py_bytes, subkey=None)` - Write binary data

### List Operations
- `reg_read_strlist(subkey)` - Get all string values under key
- `reg_write_strlist(items, subkey)` - Write list of strings
- `reg_update_strlist(subkey, add, maxrecs, rem=None, ignorecase=False)` - Add/remove items with trimming
- `reg_update_filestrlist(subkey, add, maxrecs, rem=None)` - Update file list (OS-specific case sensitivity)

### Key/Value Management
- `reg_exists(name, subkey=None)` - Check if value exists
- `reg_subkey_exists(name)` - Check if key exists
- `reg_delete(name, subkey=None)` - Delete value
- `reg_delete_subkey(name)` - Delete key
- `reg_delete_tree(name)` - Delete subtree recursively
- `reg_subkey_subkeys(name)` - Get all subkey names
- `reg_subkey_values(name)` - Get all value names
- `reg_data_type(name, subkey=None)` - Get value type (reg_unknown/reg_sz/reg_binary/reg_dword)

## Constants

- `ROOT_KEY_NAME` - Default key for IDA settings
- `reg_sz` - UTF-8 string type
- `reg_binary` - Binary data type
- `reg_dword` - 32-bit number type

## See Also
Full docs: skill/docs/ida_registry.rst

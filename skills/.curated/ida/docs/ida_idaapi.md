# ida_idaapi

Core IDAPython infrastructure - plugin system, type definitions, and Python integration utilities.

## Key Constants

### Address Types
- `ea_t` - Effective address type (int)
- `BADADDR` - Invalid address sentinel
- `BADADDR32` - 32-bit invalid address (0xFFFFFFFF)
- `BADADDR64` - 64-bit invalid address (0xFFFFFFFFFFFFFFFF)

### Plugin Return Codes
- `PLUGIN_SKIP` - Plugin init failed, unload
- `PLUGIN_OK` - Plugin loaded successfully
- `PLUGIN_KEEP` - Keep plugin loaded

## Key Functions

- `require(modulename, package=None)` - Load or reload module (forces reload for development)
- `notify_when(when, callback)` - Register event callbacks (NW_OPENIDB, NW_CLOSEIDB, etc.)
- `as_cstr(s)` - Convert to C string
- `as_uint32(v)`, `as_int32(v)`, `as_signed(v)` - Type conversions
- `IDAPython_ExecScript(path)` - Execute Python script
- `set_script_timeout(seconds)`, `disable_script_timeout()` - Script execution limits

## Key Classes

### plugin_t
Base class for IDA plugins.
- Override `init()`, `run()`, `term()` methods
- Set `flags`, `comment`, `help`, `wanted_name`, `wanted_hotkey`

### plugmod_t
Modern plugin module interface (IDA 7.2+).
- Override `run(arg)` method
- Supports multiple plugin instances

## See Also
Full docs: skill/docs/ida_idaapi.rst

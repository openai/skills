# ida_idd

Interface to debugger modules - defines structures for target processor debugging and API.

## Key Classes/Functions

### debug_event_t
Debug event information container
- `eid()` - get event type (PROCESS_STARTED, BREAKPOINT, EXCEPTION, etc.)
- `modinfo()` - module info for PROCESS_STARTED/LIB_LOADED
- `exc()` - exception details for EXCEPTION events
- `bpt()` - breakpoint addresses

### debugger_t
Debugger module interface
- `get_debug_event(event, timeout_ms)` - wait for debug event
- `resume(event)` - continue execution
- `read_registers(tid, clsmask, values)` - read thread registers
- `write_register(tid, regidx, value)` - write thread register
- `read_memory(nbytes, ea, buffer, size)` - read process memory
- `write_memory(nbytes, ea, buffer, size)` - write process memory
- `update_bpts(nbpts, bpts, nadd, ndel)` - add/delete breakpoints

### regval_t
Register value container
- `set_int(x)` - set integer value
- `set_float(v)` - set floating point
- `pyval(dtype)` - get Python value

### Python Helpers
- `dbg_read_memory(ea, sz)` - read debuggee memory, returns bytes or None
- `dbg_write_memory(ea, buffer)` - write bytes to debuggee
- `dbg_get_registers()` - get register definitions
- `dbg_get_memory_info()` - get memory layout

## Event Types
- PROCESS_STARTED, PROCESS_EXITED, PROCESS_ATTACHED, PROCESS_DETACHED
- THREAD_STARTED, THREAD_EXITED
- BREAKPOINT, STEP, EXCEPTION
- LIB_LOADED, LIB_UNLOADED

## See Also
Full docs: skill/docs/ida_idd.rst

# ida_auto

Autoanalysis queue management and IDA status indicators.

## Key Functions

### Auto State Management
- `get_auto_state()` - Get current autoanalyzer state (AU_NONE when idle)
- `set_auto_state(new_state)` - Set autoanalyzer state
- `auto_is_ok()` - Check if all queues empty (analysis finished)
- `is_auto_enabled()` / `enable_auto(enable)` - Get/set autoanalyzer enabled state

### Queue Operations
- `auto_mark(ea, type)` - Add single address to queue (sorted)
- `auto_mark_range(start, end, type)` - Add address range to queue
- `auto_unmark(start, end, type)` - Remove range from queue
- `auto_cancel(ea1, ea2)` - Remove range from AU_CODE/AU_PROC/AU_USED queues

### Analysis Planning
- `plan_ea(ea)` / `plan_range(sEA, eEA)` - Plan reanalysis
- `auto_make_code(ea)` - Plan to make code
- `auto_make_proc(ea)` - Plan to make code+function
- `reanalyze_callers(ea, noret)` - Reanalyze all callers of address
- `revert_ida_decisions(ea1, ea2)` - Delete IDA-generated analysis for range

### Synchronous Analysis
- `auto_wait()` - Process all queues and wait (returns false if cancelled)
- `auto_wait_range(ea1, ea2)` - Process range and wait (returns step count or -1)
- `plan_and_wait(ea1, ea2, final_pass=True)` - Analyze range synchronously
- `auto_make_step(ea1, ea2)` - Analyze one address in range

### Queue Types (atype_t)
- `AU_CODE` (1) - Convert to instruction
- `AU_PROC` (3) - Convert to procedure start
- `AU_USED` (6) - Reanalyze
- `AU_TYPE` (8) - Apply type information
- `AU_FINAL` (13) - Final pass

### IDA State (idastate_t)
- `st_Ready` - IDA idle
- `st_Think` - Autoanalysis on
- `st_Waiting` - Waiting for input
- `st_Work` - IDA busy

## See Also
Full docs: skill/docs/ida_auto.rst

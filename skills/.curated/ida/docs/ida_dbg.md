# ida_dbg

Debugger control and tracing (unsafe operations require --unsafe flag).

## Process Control

### Start/Stop
- `start_process(path, args, sdir)` / `request_start_process(...)` - Start debugging
- `attach_process(pid, event_id)` / `request_attach_process(...)` - Attach to process
- `detach_process()` / `request_detach_process()` - Detach from process
- `exit_process()` / `request_exit_process()` - Terminate debugged process
- `get_process_state()` / `set_process_state(state)` - Get/set state (DSTATE_SUSP/RUN/NOTASK)

### Execution
- `suspend_process()` / `continue_process()` - Pause/resume execution
- `step_into()` / `step_over()` - Single step (into/over calls)
- `step_until_ret()` - Run until return
- `run_to(ea)` - Run until address
- `run_to_backwards(ea)` / `continue_backwards()` - Reverse execution (if debugger supports)

### State
- `is_debugger_busy()` - Check if debugger processing request
- `get_running_request()` / `is_request_running()` - Query pending requests
- `invalidate_dbg_state(what)` - Invalidate cached state (DBGINV_MEMORY/REGS/ALL)

## Threads

- `get_thread_qty()` - Get thread count
- `getn_thread(idx)` - Get thread ID by index
- `get_current_thread()` - Get current thread ID
- `select_thread(tid)` - Switch to thread
- `suspend_thread(tid)` / `resume_thread(tid)` - Pause/resume thread

## Breakpoints

### Management
- `add_bpt(ea, size, bpt_type)` - Add breakpoint (BPT_BRK/BPT_TRACE)
- `del_bpt(ea)` - Delete breakpoint
- `enable_bpt(ea, enable)` - Enable/disable breakpoint
- `update_bpt(bpt)` - Update breakpoint properties
- `get_bpt_qty()` / `getn_bpt(idx)` / `get_bpt(ea)` - Query breakpoints

### Breakpoint Types
- `BPT_BRK` - Stop execution
- `BPT_TRACE` - Log and continue
- `BPT_ENABLED` - Breakpoint active
- `BPT_LOWCND` - Has condition

### Location Types
- `BPLT_ABS` - Absolute address
- `BPLT_REL` - Relative to module
- `BPLT_SYM` - Symbol name
- `BPLT_SRC` - Source file:line

## Registers

- `get_dbg_reg_info(reg_name)` - Get register info
- `get_sp_val()` / `get_ip_val()` - Get stack/instruction pointer
- `is_reg_integer(reg_name)` / `is_reg_float(reg_name)` - Check register type

## Tracing

### Step Trace
- `enable_step_trace(enable)` / `is_step_trace_enabled()` - Enable/check step tracing
- `set_step_trace_options(opts)` / `get_step_trace_options()` - Configure tracing
- `ST_OVER_DEBUG_SEG` / `ST_OVER_LIB_FUNC` / `ST_SKIP_LOOPS` - Step options

### Instruction/Function/Block Trace
- `enable_insn_trace(enable)` / `enable_func_trace(enable)` / `enable_bblk_trace(enable)` - Enable tracing
- `set_insn_trace_options(opts)` / `set_func_trace_options(opts)` - Configure
- `IT_LOG_SAME_IP` / `FT_LOG_RET` / `BT_LOG_INSTS` - Trace options

### Trace Events
- `get_tev_qty()` - Get trace event count
- `get_tev_info(tev)` - Get trace event details
- `get_insn_tev_reg_val(tev, reg)` - Get register value at instruction event
- `clear_trace()` - Clear trace buffer
- `set_trace_size(size)` - Set trace buffer size

## Event Types

### Debug Events
- `dbg_process_start` / `dbg_process_exit` - Process lifetime
- `dbg_thread_start` / `dbg_thread_exit` - Thread lifetime
- `dbg_library_load` / `dbg_library_unload` - Module events
- `dbg_bpt` / `dbg_exception` - Exception events
- `dbg_step_into` / `dbg_step_over` / `dbg_run_to` - Step events

### Trace Event Types
- `tev_insn` - Instruction execution
- `tev_call` - Function call
- `tev_ret` - Function return
- `tev_bpt` - Breakpoint hit
- `tev_mem` - Memory access

## Debugger Options (DOPT_*)
- `DOPT_START_BPT` - Break on process start
- `DOPT_ENTRY_BPT` - Break on entry point
- `DOPT_THREAD_BPT` - Break on new thread
- `DOPT_LIB_BPT` - Break on library load
- `DOPT_SUSPEND_ON_EXCEPTION` - Stop on exception

## DBG_Hooks
Override methods to receive debugger events (use `ida_dbg.DBG_Hooks` base class).

## See Also
Full docs: skill/docs/ida_dbg.rst

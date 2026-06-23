# idc

IDC compatibility module - legacy IDA scripting interface with 600+ functions for reverse engineering tasks.

## Core Constants
- `BADADDR` - invalid address constant (0xFFFFFFFFFFFFFFFF)
- `BADSEL` - invalid selector
- Flag constants: `FF_CODE`, `FF_DATA`, `FF_UNK`, `FF_TAIL`, etc.
- Data types: `FF_BYTE`, `FF_WORD`, `FF_DWORD`, `FF_QWORD`, `FF_STRLIT`, etc.

## Memory & Bytes

### Reading Memory
- `get_db_byte(ea)` - read byte from database
- `get_wide_byte(ea)` - read byte with segment translation
- `get_wide_word(ea)` - read 16-bit word
- `get_wide_dword(ea)` - read 32-bit dword
- `get_qword(ea)` - read 64-bit qword
- `get_bytes(ea, size)` - read byte array
- `get_original_byte(ea)` - get original file byte (before patching)

### Writing Memory
- `patch_byte(ea, value)` - patch byte in database
- `patch_word(ea, value)` - patch 16-bit word
- `patch_dword(ea, value)` - patch 32-bit dword
- `patch_qword(ea, value)` - patch 64-bit qword
- `patch_dbg_byte(ea, value)` - patch byte in debugger memory

### Debugger Memory
- `read_dbg_memory(ea, size)` - read from debugger memory
- `write_dbg_memory(ea, data)` - write to debugger memory
- `read_dbg_byte/word/dword/qword(ea)` - typed debugger reads

## Names & Addresses

### Name Operations
- `set_name(ea, name, flags=SN_CHECK)` - set name at address
- `get_name(ea, flags=0)` - get name at address
- `demangle_name(name, disable_mask)` - demangle C++ name
- `get_name_ea(from, name)` - find address by name
- `get_name_ea_simple(name)` - simple name lookup

### Address Navigation
- `get_screen_ea()` - current cursor address
- `jumpto(ea)` - jump to address in disassembly
- `next_addr(ea)` - next address
- `prev_addr(ea)` - previous address
- `next_head(ea, max_ea)` - next instruction/data head
- `prev_head(ea, min_ea)` - previous instruction/data head
- `next_not_tail(ea)` - skip tail bytes
- `prev_not_tail(ea)` - skip tail bytes backward
- `get_item_head(ea)` - start of item containing ea
- `get_item_end(ea)` - end of item containing ea
- `get_item_size(ea)` - size of item

## Instructions & Disassembly

### Instruction Creation
- `create_insn(ea)` - create instruction at address
- `del_items(ea, flags)` - delete instruction/data items

### Disassembly Text
- `generate_disasm_line(ea, flags)` - generate disassembly line
- `GetDisasm(ea)` - get disassembly text
- `print_insn_mnem(ea)` - get instruction mnemonic
- `print_operand(ea, n)` - get operand text

### Operand Analysis
- `get_operand_type(ea, n)` - operand type (o_reg, o_mem, o_imm, etc.)
- `get_operand_value(ea, n)` - operand numeric value

## Data Creation

### Create Data Items
- `create_byte(ea)` - create byte at address
- `create_word(ea)` - create word
- `create_dword(ea)` - create dword
- `create_qword(ea)` - create qword
- `create_oword(ea)` - create oword (16 bytes)
- `create_float(ea)` - create float
- `create_double(ea)` - create double
- `create_strlit(ea, endea)` - create string literal
- `create_struct(ea, size, strname)` - apply structure
- `make_array(ea, nitems)` - create array

### Data Type Checks (Flags)
- `is_byte/word/dword/qword/oword(flags)` - check data size
- `is_float/double/pack_real(flags)` - check floating types
- `is_strlit(flags)` - check if string literal
- `is_struct(flags)` - check if structure
- `is_code/data/tail/unknown/head(flags)` - check item type
- `get_full_flags(ea)` - get all flags for address

## Operand Formatting

### Set Display Format
- `op_hex(ea, n)` - display operand as hex
- `op_dec(ea, n)` - display as decimal
- `op_oct(ea, n)` - display as octal
- `op_bin(ea, n)` - display as binary
- `op_chr(ea, n)` - display as character
- `op_num(ea, n)` - display as number
- `op_offset(ea, n, base)` - display as offset
- `op_seg(ea, n)` - display as segment
- `op_enum(ea, n, enum_id, serial)` - display as enum member
- `op_stroff(ea, n, strid, delta)` - display as struct offset
- `op_stkvar(ea, n)` - display as stack variable
- `toggle_sign(ea, n)` - toggle signed/unsigned
- `toggle_bnot(ea, n)` - toggle bitwise NOT

## Comments

### Comment Operations
- `set_cmt(ea, comment, rptble)` - set comment (rptble: 0=regular, 1=repeatable)
- `get_cmt(ea, rptble)` - get comment
- `get_extra_cmt(ea, what)` - get anterior/posterior comment
- `update_extra_cmt(ea, what, text)` - update extra comment
- `del_extra_cmt(ea, what)` - delete extra comment

## Functions

### Function Management
- `add_func(start, end=BADADDR)` - create function
- `del_func(ea)` - delete function
- `set_func_end(ea, end)` - set function end
- `get_fchunk_referer(ea)` - get function chunk owner
- `func_contains(func_ea, ea)` - check if address in function

### Function Attributes (get_func_attr/set_func_attr)
- `FUNCATTR_START` - function start address
- `FUNCATTR_END` - function end address
- `FUNCATTR_FLAGS` - function flags (FUNC_NORET, FUNC_FAR, FUNC_LIB, etc.)
- `FUNCATTR_FRAME` - frame ID
- `FUNCATTR_FRSIZE` - frame size
- `FUNCATTR_ARGSIZE` - argument area size

## Segments

### Segment Navigation
- `get_first_seg()` - get first segment
- `get_next_seg(ea)` - get next segment
- `get_segm_start(ea)` - segment start address
- `get_segm_end(ea)` - segment end address
- `get_segm_name(ea)` - segment name
- `get_segm_by_sel(sel)` - find segment by selector

### Segment Creation/Modification
- `add_segm_ex(start, end, base, use32, align, comb, flags)` - add segment
- `del_segm(ea, flags)` - delete segment
- `set_segm_name(ea, name)` - rename segment
- `set_segm_class(ea, class)` - set segment class
- `set_segment_bounds(ea, start, end, flags)` - resize segment
- `rebase_program(delta, flags)` - rebase entire program

## Cross-References (Xrefs)

### Code Xrefs
- `add_cref(from, to, type)` - add code xref
- `del_cref(from, to, expand)` - delete code xref
- `get_first_cref_from(ea)` - first code xref from address
- `get_next_cref_from(ea, current)` - next code xref from
- `get_first_cref_to(ea)` - first code xref to address
- `get_next_cref_to(ea, current)` - next code xref to
- `get_first_fcref_from/to(ea)` - flow code xrefs only

### Data Xrefs
- `add_dref(from, to, type)` - add data xref (dr_O, dr_W, dr_R types)
- `del_dref(from, to)` - delete data xref
- `get_first_dref_from(ea)` - first data xref from
- `get_next_dref_from(ea, current)` - next data xref from
- `get_first_dref_to(ea)` - first data xref to
- `get_next_dref_to(ea, current)` - next data xref to

## Search Functions

### Pattern Search
- `find_bytes(ea, size, pattern, radix)` - find byte pattern
- `find_text(ea, flags, y, x, text)` - find text string
- `find_code(ea, flag)` - find next code byte
- `find_data(ea, flag)` - find next data byte
- `find_unknown(ea, flag)` - find next unknown byte
- `find_defined(ea, flag)` - find next defined byte
- `find_imm(ea, flag, value)` - find immediate value

## Database & Files

### Database Operations
- `save_database(idbname, flags)` - save IDB
- `get_idb_path()` - get IDB file path
- `get_root_filename()` - get input file name (no path)
- `get_input_file_path()` - get full input file path
- `set_root_filename(name)` - set root filename
- `retrieve_input_file_md5()` - get MD5 of input file

### IDB Info (get_inf_attr/set_inf_attr)
- `INF_MIN_EA` - minimum address
- `INF_MAX_EA` - maximum address
- `INF_START_EA` - entry point address
- `INF_PROCNAME` - processor name
- `INF_FILETYPE` - file type (FT_PE, FT_ELF, FT_MACHO, etc.)
- `INF_OSTYPE` - OS type
- `INF_COMPILER` - compiler ID

## Auto-Analysis

### Analysis Control
- `auto_wait()` - wait for auto-analysis to complete
- `plan_and_wait(start, end, final_pass)` - analyze range and wait
- `auto_mark_range(start, end, qtype)` - mark range for analysis
- `auto_unmark(start, end, qtype)` - unmark range
- Analysis types: `AU_UNK`, `AU_CODE`, `AU_PROC`, `AU_USED`, `AU_LIBF`, `AU_FINAL`

## Debugger (Unsafe)

### Process Control
- `load_debugger(dbg, use_remote)` - load debugger
- `start_process(path, args, sdir)` - start debugging
- `exit_process()` - terminate process
- `attach_process(pid, event_id)` - attach to process
- `detach_process()` - detach from process
- `suspend_process()` - suspend process
- `get_processes()` - list processes

### Execution Control
- `step_into()` - step into instruction
- `step_over()` - step over instruction
- `run_to(ea)` - run to address
- `step_until_ret()` - run until return
- `wait_for_next_event(wfne, timeout)` - wait for debug event

### Breakpoints
- `add_bpt(ea, size, type)` - add breakpoint
- `del_bpt(ea)` - delete breakpoint
- `enable_bpt(ea, enable)` - enable/disable breakpoint
- `check_bpt(ea)` - check breakpoint status
- `get_bpt_qty()` - get breakpoint count
- Breakpoint types: `BPT_SOFT`, `BPT_EXEC`, `BPT_WRITE`, `BPT_RDWR`

### Registers & Threads
- `get_reg_value(name)` - get register value
- `get_thread_qty()` - thread count
- `getn_thread(idx)` - get thread ID
- `get_current_thread()` - current thread ID
- `select_thread(tid)` - switch thread
- `suspend_thread(tid)` - suspend thread
- `resume_thread(tid)` - resume thread

## Entry Points
- `get_entry_qty()` - number of entry points
- `get_entry(ordinal)` - get entry point address
- `get_entry_ordinal(index)` - get ordinal by index
- `get_entry_name(ordinal)` - get entry point name
- `add_entry(ordinal, ea, name, makecode)` - add entry point
- `rename_entry(ordinal, name)` - rename entry point

## Utilities

### String Operations
- `strlen(s)` - string length
- `substr(s, x1, x2)` - substring
- `strstr(s1, s2)` - find substring
- `form(format, *args)` - formatted string (printf-style)

### Number Conversion
- `atol(s)` - string to long
- `ltoa(n, radix)` - long to string
- `atoa(ea)` - address to string
- `xtol(s)` - hex string to long
- `rotate_left/dword/word/byte(value, count)` - bitwise rotation

### UI Interaction
- `msg(format, *args)` - print to output window
- `warning(format, *args)` - show warning dialog
- `error(format, *args)` - show error dialog
- `ask_yn(default, format, *args)` - yes/no dialog
- `jumpto(ea)` - jump to address
- `refresh_idaview_anyway()` - force UI refresh

### Execution
- `eval_idc(expr)` - evaluate IDC expression
- `qsleep(milliseconds)` - sleep
- `call_system(command)` - execute system command
- `batch(enable)` - enable/disable batch mode
- `qexit(code)` - exit IDA
- `process_ui_action(name)` - trigger UI action

## Name Flags
- `SN_CHECK` - check name for validity
- `SN_NOCHECK` - don't check name
- `SN_PUBLIC` - public name
- `SN_NON_PUBLIC` - private name
- `SN_WEAK` - weak name
- `SN_AUTO` - auto-generated name
- `SN_LOCAL` - local name
- `SN_NOLIST` - don't show in names list
- `SN_NOWARN` - suppress warnings

## Get Name Flags (GN_* for get_name)
- `GN_VISIBLE` - return visible name
- `GN_COLORED` - include color tags
- `GN_DEMANGLED` - return demangled name
- `GN_STRICT` - fail if no name
- `GN_SHORT` - short form
- `GN_LONG` - long form
- `GN_LOCAL` - include local name part

## See Also
Full docs: skill/docs/idc.rst

Note: This is a legacy compatibility module. Modern Python scripts should prefer `idaapi`, `ida_bytes`, `ida_name`, `ida_funcs`, etc. modules over idc functions.

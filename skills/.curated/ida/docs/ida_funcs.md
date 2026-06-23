# ida_funcs

Function management - define, modify, analyze functions and function chunks. Includes FLIRT signature support.

## Architecture

Functions consist of:
- **Entry chunk** - function start (required)
- **Tail chunks** - optional additional code ranges shared between functions
- Each tail has an **owner** function

## func_t Class

Core function descriptor (extends range_t).

### Key Attributes
- `flags: uint64` - Function flags (FUNC_*)
- `frame: int` - Frame structure netnode ID
- `frsize: asize_t` - Local variables size
- `frregs: ushort` - Saved registers size
- `argsize: asize_t` - Purged bytes on return (__stdcall/__pascal)
- `fpd: asize_t` - Frame pointer delta (usually 0)
- `color: bgcolor_t` - User-defined color
- `points: stkpnt_t*`, `pntqty: int` - SP change points
- `regvars: regvar_t*`, `regvarqty: int` - Register variables
- `regargs: regarg_t*`, `regargqty: int` - Register arguments (temporary, cleared when type determined)
- `tails: range_t*`, `tailqty: int` - Function tails
- `owner: ea_t` - Tail owner address
- `referers: ea_t*`, `refqty: int` - Parent functions using this tail

### Methods
- `is_far() -> bool` - Far function
- `does_return() -> bool` - Returns to caller
- `analyzed_sp() -> bool` - SP-analysis performed
- `need_prolog_analysis() -> bool` - Needs prolog analysis
- `get_name() -> str` - Function name
- `get_prototype() -> tinfo_t` - Function prototype
- `get_frame_object() -> tinfo_t` - Frame structure
- `addresses()`, `code_items()`, `data_items()`, `head_items()`, `not_tails()` - Iterators

## Key Functions

### Querying Functions
- `get_func(ea) -> func_t*` - Get function by address (returns entry chunk)
- `getn_func(n) -> func_t*` - Get function by index (0..get_func_qty()-1)
- `get_func_qty() -> size_t` - Total function count
- `get_func_num(ea) -> int` - Get function index (-1 if not found)
- `get_prev_func(ea) -> func_t*`, `get_next_func(ea) -> func_t*` - Navigate functions
- `func_contains(pfn, ea) -> bool` - Does function contain address
- `is_same_func(ea1, ea2) -> bool` - Do addresses belong to same function
- `get_func_chunknum(pfn, ea) -> int` - Get chunk number (-1=not contained, 0=entry, >0=tail)

### Creating/Modifying Functions
- `add_func(ea1, ea2=BADADDR) -> bool` - Create function (auto-determines bounds if ea2=BADADDR)
- `add_func_ex(pfn) -> bool` - Create from func_t struct
- `del_func(ea) -> bool` - Delete function
- `update_func(pfn) -> bool` - Update function info (don't use for start/end changes)
- `set_func_start(ea, newstart) -> int` - Move start address (returns MOVE_FUNC_*)
- `set_func_end(ea, newend) -> bool` - Move end address
- `find_func_bounds(nfn, flags) -> int` - Auto-determine boundaries (returns FIND_FUNC_*)
- `reanalyze_function(pfn, ea1=None, ea2=None, analyze_parents=False)` - Reanalyze function

### Function Information
- `get_func_name(ea) -> str` - Get name
- `get_func_cmt(pfn, repeatable) -> str`, `set_func_cmt(pfn, cmt, repeatable) -> bool` - Comments
- `get_func_ranges(ranges, pfn) -> ea_t` - Get all ranges
- `calc_func_size(pfn) -> asize_t` - Total size including tails
- `get_func_bitness(ea) -> int` - Bitness (0=16, 1=32, 2=64, -1=error)
- `get_func_bits(ea) -> int` - Bits (16/32/64)
- `get_func_bytes(ea) -> bytes` - Function bytes
- `is_visible_func(pfn) -> bool`, `set_visible_func(pfn, visible)` - Visibility control
- `is_finally_visible_func(pfn) -> bool` - Final visibility after all checks

### Function Analysis
- `func_does_return(ea) -> bool` - Does function return
- `reanalyze_noret_flag(ea)` - Reanalyze non-return flag
- `set_noret_insn(ea, noret)` - Mark instruction as non-returning
- `calc_thunk_func_target(pfn) -> ea_t` - Get thunk target
- `set_func_name_if_jumpfunc(pfn, name)` - Auto-name jump functions

### Function Chunks (Tails)
- `get_fchunk(ea) -> func_t*` - Get chunk by address (entry or tail)
- `getn_fchunk(n) -> func_t*` - Get chunk by index
- `get_fchunk_qty() -> size_t` - Total chunk count
- `get_fchunk_num(ea) -> int` - Get chunk index
- `get_prev_fchunk(ea) -> func_t*`, `get_next_fchunk(ea) -> func_t*` - Navigate chunks
- `append_func_tail(pfn, tail_ea1, tail_ea2) -> bool` - Add tail to function
- `remove_func_tail(pfn, tail_ea) -> bool` - Remove tail
- `set_tail_owner(tail, owner_ea) -> bool` - Change tail owner
- `get_fchunk_referer(ea, idx) -> ea_t` - Get parent function using tail
- `func_tail_iterator_set(pfn, fti)` - Initialize tail iterator
- `func_parent_iterator_set(pfn, fpi)` - Initialize parent iterator

### Locking
- `lock_func_range(pfn, lock)` - Lock function pointer (prevents deletion/move)
- `is_func_locked(pfn) -> bool` - Check if locked
- `lock_func(pfn)`, `lock_func_with_tails_t(pfn)` - RAII lock helpers

### FLIRT Signatures
- `plan_to_apply_idasgn(name) -> int` - Plan signature application (returns IDASGN_*)
- `apply_idasgn_to(name, ea, may_show_wait_box) -> int` - Apply signature at address
- `get_idasgn_qty() -> int` - Number of loaded signatures
- `get_current_idasgn() -> str` - Current signature name
- `calc_idasgn_state(n) -> int` - Signature state (IDASGN_*)
- `del_idasgn(n)` - Delete signature
- `get_idasgn_title(n) -> str` - Get signature title
- `get_idasgn_desc(n) -> str` - Get description
- `get_idasgn_desc_with_matches(n) -> str` - Get description with match count
- `apply_startup_sig(ea1, ea2)` - Apply startup signature
- `try_to_add_libfunc(pfn, ea) -> int` - Try to add library function (returns LIBFUNC_*)

### Register Arguments
- `read_regargs(pfn) -> dyn_regarg_array` - Read register arguments
- `add_regarg(pfn, reg, type, name) -> bool` - Add register argument

## Function Flags (FUNC_*)

- `FUNC_NORET` - Doesn't return
- `FUNC_FAR` - Far function
- `FUNC_LIB` - Library function
- `FUNC_STATICDEF` - Static
- `FUNC_FRAME` - Uses frame pointer (BP)
- `FUNC_USERFAR` - User-specified far
- `FUNC_HIDDEN` - Hidden chunk
- `FUNC_THUNK` - Jump/thunk function
- `FUNC_BOTTOMBP` - BP points to stack frame bottom
- `FUNC_NORET_PENDING` - Non-return analysis pending
- `FUNC_SP_READY` - SP-analysis complete
- `FUNC_FUZZY_SP` - SP changes untraceably (e.g., "and esp, 0FFFFFFF0h")
- `FUNC_PROLOG_OK` - Prolog analyzed
- `FUNC_PURGED_OK` - argsize validated
- `FUNC_TAIL` - Function tail chunk
- `FUNC_LUMINA` - Info from Lumina
- `FUNC_OUTLINE` - Outlined code, not real function
- `FUNC_REANALYZE` - Frame changed, needs reanalysis
- `FUNC_UNWIND` - Exception unwind handler
- `FUNC_CATCH` - Exception catch handler

## Return Codes

### MOVE_FUNC_*
- `MOVE_FUNC_OK` - Success
- `MOVE_FUNC_NOCODE` - No instruction at newstart
- `MOVE_FUNC_BADSTART` - Bad new start
- `MOVE_FUNC_NOFUNC` - No function at ea
- `MOVE_FUNC_REFUSED` - Plugin refused

### FIND_FUNC_* (flags)
- `FIND_FUNC_NORMAL` - Stop on undefined byte
- `FIND_FUNC_DEFINE` - Create instruction on undefined byte
- `FIND_FUNC_IGNOREFN` - Ignore existing function boundaries
- `FIND_FUNC_KEEPBD` - Don't modify boundaries, just create instructions

### FIND_FUNC_* (results)
- `FIND_FUNC_OK` - Ready for add_func()
- `FIND_FUNC_EXIST` - Already exists
- `FIND_FUNC_UNDEF` - Has unexplored bytes

### IDASGN_*
- `IDASGN_OK` - Success
- `IDASGN_BADARG` - Bad argument
- `IDASGN_APPLIED` - Already applied
- `IDASGN_CURRENT` - Current signature
- `IDASGN_PLANNED` - Planned for application

### LIBFUNC_*
- `LIBFUNC_FOUND` - Found and added
- `LIBFUNC_NONE` - Not found
- `LIBFUNC_DELAY` - Delayed (needs more analysis)

## Iterators

- `func_tail_iterator_t` - Iterate function tails
- `func_item_iterator_t` - Iterate function items (addresses/code/data/heads)
- `func_parent_iterator_t` - Iterate parent functions using tail

## See Also
Full docs: skill/docs/ida_funcs.rst

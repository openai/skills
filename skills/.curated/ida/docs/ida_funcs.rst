ida_funcs
=========

.. py:module:: ida_funcs

.. autoapi-nested-parse::

   Routines for working with functions within the disassembled program.

   This file also contains routines for working with library signatures (e.g. FLIRT).

   Each function consists of function chunks. At least one function chunk must be present in the function definition - the function entry chunk. Other chunks are called function tails. There may be several of them for a function.

   A function tail is a continuous range of addresses. It can be used in the definition of one or more functions. One function using the tail is singled out and called the tail owner. This function is considered as 'possessing' the tail. get_func() on a tail address will return the function possessing the tail. You can enumerate the functions using the tail by using func_parent_iterator_t.

   Each function chunk in the disassembly is represented as an "range" (a range of addresses, see range.hpp for details) with characteristics.
   A function entry must start with an instruction (code) byte. 

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For function management and analysis, see :mod:`ida_domain.functions`.



Attributes
----------

.. autoapisummary::

   ida_funcs.FUNC_NORET
   ida_funcs.FUNC_FAR
   ida_funcs.FUNC_LIB
   ida_funcs.FUNC_STATICDEF
   ida_funcs.FUNC_FRAME
   ida_funcs.FUNC_USERFAR
   ida_funcs.FUNC_HIDDEN
   ida_funcs.FUNC_THUNK
   ida_funcs.FUNC_BOTTOMBP
   ida_funcs.FUNC_NORET_PENDING
   ida_funcs.FUNC_SP_READY
   ida_funcs.FUNC_FUZZY_SP
   ida_funcs.FUNC_PROLOG_OK
   ida_funcs.FUNC_PURGED_OK
   ida_funcs.FUNC_TAIL
   ida_funcs.FUNC_LUMINA
   ida_funcs.FUNC_OUTLINE
   ida_funcs.FUNC_REANALYZE
   ida_funcs.FUNC_UNWIND
   ida_funcs.FUNC_CATCH
   ida_funcs.MOVE_FUNC_OK
   ida_funcs.MOVE_FUNC_NOCODE
   ida_funcs.MOVE_FUNC_BADSTART
   ida_funcs.MOVE_FUNC_NOFUNC
   ida_funcs.MOVE_FUNC_REFUSED
   ida_funcs.FIND_FUNC_NORMAL
   ida_funcs.FIND_FUNC_DEFINE
   ida_funcs.FIND_FUNC_IGNOREFN
   ida_funcs.FIND_FUNC_KEEPBD
   ida_funcs.FIND_FUNC_UNDEF
   ida_funcs.FIND_FUNC_OK
   ida_funcs.FIND_FUNC_EXIST
   ida_funcs.IDASGN_OK
   ida_funcs.IDASGN_BADARG
   ida_funcs.IDASGN_APPLIED
   ida_funcs.IDASGN_CURRENT
   ida_funcs.IDASGN_PLANNED
   ida_funcs.LIBFUNC_FOUND
   ida_funcs.LIBFUNC_NONE
   ida_funcs.LIBFUNC_DELAY


Classes
-------

.. autoapisummary::

   ida_funcs.dyn_stkpnt_array
   ida_funcs.dyn_regvar_array
   ida_funcs.dyn_range_array
   ida_funcs.dyn_ea_array
   ida_funcs.dyn_regarg_array
   ida_funcs.regarg_t
   ida_funcs.func_t
   ida_funcs.lock_func
   ida_funcs.lock_func_with_tails_t
   ida_funcs.func_tail_iterator_t
   ida_funcs.func_item_iterator_t
   ida_funcs.func_parent_iterator_t


Functions
---------

.. autoapisummary::

   ida_funcs.free_regarg
   ida_funcs.is_func_entry
   ida_funcs.is_func_tail
   ida_funcs.lock_func_range
   ida_funcs.is_func_locked
   ida_funcs.get_func
   ida_funcs.get_func_chunknum
   ida_funcs.func_contains
   ida_funcs.is_same_func
   ida_funcs.getn_func
   ida_funcs.get_func_qty
   ida_funcs.get_func_num
   ida_funcs.get_prev_func
   ida_funcs.get_next_func
   ida_funcs.get_func_ranges
   ida_funcs.get_func_cmt
   ida_funcs.set_func_cmt
   ida_funcs.update_func
   ida_funcs.add_func_ex
   ida_funcs.add_func
   ida_funcs.del_func
   ida_funcs.set_func_start
   ida_funcs.set_func_end
   ida_funcs.reanalyze_function
   ida_funcs.find_func_bounds
   ida_funcs.get_func_name
   ida_funcs.calc_func_size
   ida_funcs.get_func_bitness
   ida_funcs.get_func_bits
   ida_funcs.get_func_bytes
   ida_funcs.is_visible_func
   ida_funcs.is_finally_visible_func
   ida_funcs.set_visible_func
   ida_funcs.set_func_name_if_jumpfunc
   ida_funcs.calc_thunk_func_target
   ida_funcs.func_does_return
   ida_funcs.reanalyze_noret_flag
   ida_funcs.set_noret_insn
   ida_funcs.get_fchunk
   ida_funcs.getn_fchunk
   ida_funcs.get_fchunk_qty
   ida_funcs.get_fchunk_num
   ida_funcs.get_prev_fchunk
   ida_funcs.get_next_fchunk
   ida_funcs.append_func_tail
   ida_funcs.remove_func_tail
   ida_funcs.set_tail_owner
   ida_funcs.func_tail_iterator_set
   ida_funcs.func_tail_iterator_set_ea
   ida_funcs.func_parent_iterator_set
   ida_funcs.f_any
   ida_funcs.get_prev_func_addr
   ida_funcs.get_next_func_addr
   ida_funcs.read_regargs
   ida_funcs.add_regarg
   ida_funcs.plan_to_apply_idasgn
   ida_funcs.apply_idasgn_to
   ida_funcs.get_idasgn_qty
   ida_funcs.get_current_idasgn
   ida_funcs.calc_idasgn_state
   ida_funcs.del_idasgn
   ida_funcs.get_idasgn_title
   ida_funcs.apply_startup_sig
   ida_funcs.try_to_add_libfunc
   ida_funcs.get_fchunk_referer
   ida_funcs.get_idasgn_desc
   ida_funcs.get_idasgn_desc_with_matches
   ida_funcs.func_t__from_ptrval__
   ida_funcs.calc_thunk_func_target


Module Contents
---------------

.. py:class:: dyn_stkpnt_array(_data: stkpnt_t *, _count: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  stkpnt_t *


   .. py:attribute:: count
      :type:  size_t


.. py:class:: dyn_regvar_array(_data: regvar_t *, _count: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  regvar_t *


   .. py:attribute:: count
      :type:  size_t


.. py:class:: dyn_range_array(_data: range_t, _count: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  range_t *


   .. py:attribute:: count
      :type:  size_t


.. py:class:: dyn_ea_array(_data: unsigned long long *, _count: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  unsigned long long *


   .. py:attribute:: count
      :type:  size_t


.. py:class:: dyn_regarg_array(_data: regarg_t, _count: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  regarg_t *


   .. py:attribute:: count
      :type:  size_t


.. py:function:: free_regarg(v: regarg_t) -> None

.. py:class:: regarg_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: reg
      :type:  int


   .. py:attribute:: type
      :type:  type_t *


   .. py:attribute:: name
      :type:  char *


   .. py:method:: swap(r: regarg_t) -> None


.. py:class:: func_t(start: ida_idaapi.ea_t = 0, end: ida_idaapi.ea_t = 0, f: flags64_t = 0)

   Bases: :py:obj:`ida_range.range_t`


   .. py:attribute:: thisown


   .. py:attribute:: flags
      :type:  uint64

      Function flags 
              



   .. py:method:: is_far() -> bool

      Is a far function?



   .. py:method:: does_return() -> bool

      Does function return?



   .. py:method:: analyzed_sp() -> bool

      Has SP-analysis been performed?



   .. py:method:: need_prolog_analysis() -> bool

      Needs prolog analysis?



   .. py:attribute:: frame
      :type:  int

      netnode id of frame structure - see frame.hpp



   .. py:attribute:: frsize
      :type:  asize_t

      size of local variables part of frame in bytes. If FUNC_FRAME is set and fpd==0, the frame pointer (EBP) is assumed to point to the top of the local variables range. 
              



   .. py:attribute:: frregs
      :type:  ushort

      size of saved registers in frame. This range is immediately above the local variables range. 
              



   .. py:attribute:: argsize
      :type:  asize_t

      number of bytes purged from the stack upon returning 
              



   .. py:attribute:: fpd
      :type:  asize_t

      frame pointer delta. (usually 0, i.e. realBP==typicalBP) use update_fpd() to modify it. 
              



   .. py:attribute:: color
      :type:  bgcolor_t

      user defined function color



   .. py:attribute:: pntqty
      :type:  int

      number of SP change points



   .. py:attribute:: points
      :type:  stkpnt_t *

      array of SP change points. use ...stkpnt...() functions to access this array. 
              



   .. py:attribute:: regvarqty
      :type:  int

      number of register variables (-1-not read in yet) use find_regvar() to read register variables 
              



   .. py:attribute:: regvars
      :type:  regvar_t *

      array of register variables. this array is sorted by: start_ea. use ...regvar...() functions to access this array. 
              



   .. py:attribute:: regargqty
      :type:  int

      number of register arguments. During analysis IDA tries to guess the register arguments. It stores store the guessing outcome in this field. As soon as it determines the final function prototype, regargqty is set to zero. 
              



   .. py:attribute:: regargs
      :type:  regarg_t *

      unsorted array of register arguments. use ...regarg...() functions to access this array. regargs are destroyed when the full function type is determined. 
              



   .. py:attribute:: tailqty
      :type:  int

      number of function tails



   .. py:attribute:: tails
      :type:  range_t *

      array of tails, sorted by ea. use func_tail_iterator_t to access function tails. 
              



   .. py:attribute:: owner
      :type:  ida_idaapi.ea_t

      the address of the main function possessing this tail



   .. py:attribute:: refqty
      :type:  int

      number of referers



   .. py:attribute:: referers
      :type:  ea_t *

      array of referers (function start addresses). use func_parent_iterator_t to access the referers. 
              



   .. py:method:: addresses()

      Alias for func_item_iterator_t(self).addresses()



   .. py:method:: code_items()

      Alias for func_item_iterator_t(self).code_items()



   .. py:method:: data_items()

      Alias for func_item_iterator_t(self).data_items()



   .. py:method:: head_items()

      Alias for func_item_iterator_t(self).head_items()



   .. py:method:: not_tails()

      Alias for func_item_iterator_t(self).not_tails()



   .. py:method:: get_frame_object()

      Retrieve the function frame, in the form of a structure
      where frame offsets that are accessed by the program, as well
      as areas for "saved registers" and "return address", are
      represented by structure members.

      If the function has no associated frame, return None

      :returns: a ida_typeinf.tinfo_t object representing the frame, or None



   .. py:method:: get_name()

      Get the function name

      :returns: the function name



   .. py:method:: get_prototype()

      Retrieve the function prototype.

      Once you have obtained the prototype, you can:

      * retrieve the return type through ida_typeinf.tinfo_t.get_rettype()
      * iterate on the arguments using ida_typeinf.tinfo_t.iter_func()

      If the function has no associated prototype, return None

      :returns: a ida_typeinf.tinfo_t object representing the prototype, or None



   .. py:attribute:: frame_object


   .. py:attribute:: name


   .. py:attribute:: prototype


.. py:data:: FUNC_NORET

   Function doesn't return.


.. py:data:: FUNC_FAR

   Far function.


.. py:data:: FUNC_LIB

   Library function.


.. py:data:: FUNC_STATICDEF

   Static function.


.. py:data:: FUNC_FRAME

   Function uses frame pointer (BP)


.. py:data:: FUNC_USERFAR

   User has specified far-ness of the function 
           


.. py:data:: FUNC_HIDDEN

   A hidden function chunk.


.. py:data:: FUNC_THUNK

   Thunk (jump) function.


.. py:data:: FUNC_BOTTOMBP

   BP points to the bottom of the stack frame.


.. py:data:: FUNC_NORET_PENDING

   Function 'non-return' analysis must be performed. This flag is verified upon func_does_return() 
           


.. py:data:: FUNC_SP_READY

   SP-analysis has been performed. If this flag is on, the stack change points should not be not modified anymore. Currently this analysis is performed only for PC 
           


.. py:data:: FUNC_FUZZY_SP

   Function changes SP in untraceable way, for example: and esp, 0FFFFFFF0h 
           


.. py:data:: FUNC_PROLOG_OK

   Prolog analysis has been performed by last SP-analysis 
           


.. py:data:: FUNC_PURGED_OK

   'argsize' field has been validated. If this bit is clear and 'argsize' is 0, then we do not known the real number of bytes removed from the stack. This bit is handled by the processor module. 
           


.. py:data:: FUNC_TAIL

   This is a function tail. Other bits must be clear (except FUNC_HIDDEN). 
           


.. py:data:: FUNC_LUMINA

   Function info is provided by Lumina.


.. py:data:: FUNC_OUTLINE

   Outlined code, not a real function.


.. py:data:: FUNC_REANALYZE

   Function frame changed, request to reanalyze the function after the last insn is analyzed. 
           


.. py:data:: FUNC_UNWIND

   function is an exception unwind handler


.. py:data:: FUNC_CATCH

   function is an exception catch handler


.. py:function:: is_func_entry(pfn: func_t) -> bool

   Does function describe a function entry chunk?


.. py:function:: is_func_tail(pfn: func_t) -> bool

   Does function describe a function tail chunk?


.. py:function:: lock_func_range(pfn: func_t, lock: bool) -> None

   Lock function pointer Locked pointers are guaranteed to remain valid until they are unlocked. Ranges with locked pointers cannot be deleted or moved. 
           


.. py:class:: lock_func(_pfn: func_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


.. py:class:: lock_func_with_tails_t(pfn: func_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


.. py:function:: is_func_locked(pfn: func_t) -> bool

   Is the function pointer locked?


.. py:function:: get_func(ea: ida_idaapi.ea_t) -> func_t *

   Get pointer to function structure by address. 
           
   :param ea: any address in a function
   :returns: ptr to a function or nullptr. This function returns a function entry chunk.


.. py:function:: get_func_chunknum(pfn: func_t, ea: ida_idaapi.ea_t) -> int

   Get the containing tail chunk of 'ea'. 
           
   :returns: -1: means 'does not contain ea'
   :returns: 0: means the 'pfn' itself contains ea
   :returns: >0: the number of the containing function tail chunk


.. py:function:: func_contains(pfn: func_t, ea: ida_idaapi.ea_t) -> bool

   Does the given function contain the given address?


.. py:function:: is_same_func(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool

   Do two addresses belong to the same function?


.. py:function:: getn_func(n: size_t) -> func_t *

   Get pointer to function structure by number. 
           
   :param n: number of function, is in range 0..get_func_qty()-1
   :returns: ptr to a function or nullptr. This function returns a function entry chunk.


.. py:function:: get_func_qty() -> size_t

   Get total number of functions in the program.


.. py:function:: get_func_num(ea: ida_idaapi.ea_t) -> int

   Get ordinal number of a function. 
           
   :param ea: any address in the function
   :returns: number of function (0..get_func_qty()-1). -1 means 'no function at the specified address'.


.. py:function:: get_prev_func(ea: ida_idaapi.ea_t) -> func_t *

   Get pointer to the previous function. 
           
   :param ea: any address in the program
   :returns: ptr to function or nullptr if previous function doesn't exist


.. py:function:: get_next_func(ea: ida_idaapi.ea_t) -> func_t *

   Get pointer to the next function. 
           
   :param ea: any address in the program
   :returns: ptr to function or nullptr if next function doesn't exist


.. py:function:: get_func_ranges(ranges: rangeset_t, pfn: func_t) -> ida_idaapi.ea_t

   Get function ranges. 
           
   :param ranges: buffer to receive the range info
   :param pfn: ptr to function structure
   :returns: end address of the last function range (BADADDR-error)


.. py:function:: get_func_cmt(pfn: func_t, repeatable: bool) -> str

   Get function comment. 
           
   :param pfn: ptr to function structure
   :param repeatable: get repeatable comment?
   :returns: size of comment or -1 In fact this function works with function chunks too.


.. py:function:: set_func_cmt(pfn: func_t, cmt: str, repeatable: bool) -> bool

   Set function comment. This function works with function chunks too. 
           
   :param pfn: ptr to function structure
   :param cmt: comment string, may be multiline (with '
   '). Use empty str ("") to delete comment
   :param repeatable: set repeatable comment?


.. py:function:: update_func(pfn: func_t) -> bool

   Update information about a function in the database (func_t). You must not change the function start and end addresses using this function. Use set_func_start() and set_func_end() for it. 
           
   :param pfn: ptr to function structure
   :returns: success


.. py:function:: add_func_ex(pfn: func_t) -> bool

   Add a new function. If the fn->end_ea is BADADDR, then IDA will try to determine the function bounds by calling find_func_bounds(..., FIND_FUNC_DEFINE). 
           
   :param pfn: ptr to filled function structure
   :returns: success


.. py:function:: add_func(*args) -> bool

   Add a new function. If the function end address is BADADDR, then IDA will try to determine the function bounds by calling find_func_bounds(..., FIND_FUNC_DEFINE). 
           
   :param ea1: start address
   :param ea2: end address
   :returns: success


.. py:function:: del_func(ea: ida_idaapi.ea_t) -> bool

   Delete a function. 
           
   :param ea: any address in the function entry chunk
   :returns: success


.. py:function:: set_func_start(ea: ida_idaapi.ea_t, newstart: ida_idaapi.ea_t) -> int

   Move function chunk start address. 
           
   :param ea: any address in the function
   :param newstart: new end address of the function
   :returns: Function move result codes


.. py:data:: MOVE_FUNC_OK

   ok


.. py:data:: MOVE_FUNC_NOCODE

   no instruction at 'newstart'


.. py:data:: MOVE_FUNC_BADSTART

   bad new start address


.. py:data:: MOVE_FUNC_NOFUNC

   no function at 'ea'


.. py:data:: MOVE_FUNC_REFUSED

   a plugin refused the action


.. py:function:: set_func_end(ea: ida_idaapi.ea_t, newend: ida_idaapi.ea_t) -> bool

   Move function chunk end address. 
           
   :param ea: any address in the function
   :param newend: new end address of the function
   :returns: success


.. py:function:: reanalyze_function(*args) -> None

   Reanalyze a function. This function plans to analyzes all chunks of the given function. Optional parameters (ea1, ea2) may be used to narrow the analyzed range. 
           
   :param pfn: pointer to a function
   :param ea1: start of the range to analyze
   :param ea2: end of range to analyze
   :param analyze_parents: meaningful only if pfn points to a function tail. if true, all tail parents will be reanalyzed. if false, only the given tail will be reanalyzed.


.. py:function:: find_func_bounds(nfn: func_t, flags: int) -> int

   Determine the boundaries of a new function. This function tries to find the start and end addresses of a new function. It calls the module with processor_t::func_bounds in order to fine tune the function boundaries. 
           
   :param nfn: structure to fill with information \ nfn->start_ea points to the start address of the new function.
   :param flags: Find function bounds flags
   :returns: Find function bounds result codes


.. py:data:: FIND_FUNC_NORMAL

   stop processing if undefined byte is encountered


.. py:data:: FIND_FUNC_DEFINE

   create instruction if undefined byte is encountered


.. py:data:: FIND_FUNC_IGNOREFN

   ignore existing function boundaries. by default the function returns function boundaries if ea belongs to a function. 
           


.. py:data:: FIND_FUNC_KEEPBD

   do not modify incoming function boundaries, just create instructions inside the boundaries. 
           


.. py:data:: FIND_FUNC_UNDEF

   function has instructions that pass execution flow to unexplored bytes. nfn->end_ea will have the address of the unexplored byte. 
           


.. py:data:: FIND_FUNC_OK

   ok, 'nfn' is ready for add_func()


.. py:data:: FIND_FUNC_EXIST

   function exists already. its bounds are returned in 'nfn'. 
           


.. py:function:: get_func_name(ea: ida_idaapi.ea_t) -> str

   Get function name. 
           
   :param ea: any address in the function
   :returns: length of the function name


.. py:function:: calc_func_size(pfn: func_t) -> asize_t

   Calculate function size. This function takes into account all fragments of the function. 
           
   :param pfn: ptr to function structure


.. py:function:: get_func_bitness(pfn: func_t) -> int

   Get function bitness (which is equal to the function segment bitness). pfn==nullptr => returns 0 
           
   :returns: 0: 16
   :returns: 1: 32
   :returns: 2: 64


.. py:function:: get_func_bits(pfn: func_t) -> int

   Get number of bits in the function addressing.


.. py:function:: get_func_bytes(pfn: func_t) -> int

   Get number of bytes in the function addressing.


.. py:function:: is_visible_func(pfn: func_t) -> bool

   Is the function visible (not hidden)?


.. py:function:: is_finally_visible_func(pfn: func_t) -> bool

   Is the function visible (event after considering SCF_SHHID_FUNC)?


.. py:function:: set_visible_func(pfn: func_t, visible: bool) -> None

   Set visibility of function.


.. py:function:: set_func_name_if_jumpfunc(pfn: func_t, oldname: str) -> int

   Give a meaningful name to function if it consists of only 'jump' instruction. 
           
   :param pfn: pointer to function (may be nullptr)
   :param oldname: old name of function. if old name was in "j_..." form, then we may discard it and set a new name. if oldname is not known, you may pass nullptr.
   :returns: success


.. py:function:: calc_thunk_func_target(pfn: func_t) -> ea_t *

   Calculate target of a thunk function. 
           
   :param pfn: pointer to function (may not be nullptr)
   :returns: the target function or BADADDR


.. py:function:: func_does_return(callee: ida_idaapi.ea_t) -> bool

   Does the function return?. To calculate the answer, FUNC_NORET flag and is_noret() are consulted The latter is required for imported functions in the .idata section. Since in .idata we have only function pointers but not functions, we have to introduce a special flag for them. 
           


.. py:function:: reanalyze_noret_flag(ea: ida_idaapi.ea_t) -> bool

   Plan to reanalyze noret flag. This function does not remove FUNC_NORET if it is already present. It just plans to reanalysis. 
           


.. py:function:: set_noret_insn(insn_ea: ida_idaapi.ea_t, noret: bool) -> bool

   Signal a non-returning instruction. This function can be used by the processor module to tell the kernel about non-returning instructions (like call exit). The kernel will perform the global function analysis and find out if the function returns at all. This analysis will be done at the first call to func_does_return() 
           
   :returns: true if the instruction 'noret' flag has been changed


.. py:function:: get_fchunk(ea: ida_idaapi.ea_t) -> func_t *

   Get pointer to function chunk structure by address. 
           
   :param ea: any address in a function chunk
   :returns: ptr to a function chunk or nullptr. This function may return a function entry as well as a function tail.


.. py:function:: getn_fchunk(n: int) -> func_t *

   Get pointer to function chunk structure by number. 
           
   :param n: number of function chunk, is in range 0..get_fchunk_qty()-1
   :returns: ptr to a function chunk or nullptr. This function may return a function entry as well as a function tail.


.. py:function:: get_fchunk_qty() -> size_t

   Get total number of function chunks in the program.


.. py:function:: get_fchunk_num(ea: ida_idaapi.ea_t) -> int

   Get ordinal number of a function chunk in the global list of function chunks. 
           
   :param ea: any address in the function chunk
   :returns: number of function chunk (0..get_fchunk_qty()-1). -1 means 'no function chunk at the specified address'.


.. py:function:: get_prev_fchunk(ea: ida_idaapi.ea_t) -> func_t *

   Get pointer to the previous function chunk in the global list. 
           
   :param ea: any address in the program
   :returns: ptr to function chunk or nullptr if previous function chunk doesn't exist


.. py:function:: get_next_fchunk(ea: ida_idaapi.ea_t) -> func_t *

   Get pointer to the next function chunk in the global list. 
           
   :param ea: any address in the program
   :returns: ptr to function chunk or nullptr if next function chunk doesn't exist


.. py:function:: append_func_tail(pfn: func_t, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool

   Append a new tail chunk to the function definition. If the tail already exists, then it will simply be added to the function tail list Otherwise a new tail will be created and its owner will be set to be our function If a new tail cannot be created, then this function will fail. 
           
   :param pfn: pointer to the function
   :param ea1: start of the tail. If a tail already exists at the specified address it must start at 'ea1'
   :param ea2: end of the tail. If a tail already exists at the specified address it must end at 'ea2'. If specified as BADADDR, IDA will determine the end address itself.


.. py:function:: remove_func_tail(pfn: func_t, tail_ea: ida_idaapi.ea_t) -> bool

   Remove a function tail. If the tail belongs only to one function, it will be completely removed. Otherwise if the function was the tail owner, the first function using this tail becomes the owner of the tail. 
           
   :param pfn: pointer to the function
   :param tail_ea: any address inside the tail to remove


.. py:function:: set_tail_owner(fnt: func_t, new_owner: ida_idaapi.ea_t) -> bool

   Set a new owner of a function tail. The new owner function must be already referring to the tail (after append_func_tail). 
           
   :param fnt: pointer to the function tail
   :param new_owner: the entry point of the new owner function


.. py:function:: func_tail_iterator_set(fti: func_tail_iterator_t, pfn: func_t, ea: ida_idaapi.ea_t) -> bool

.. py:function:: func_tail_iterator_set_ea(fti: func_tail_iterator_t, ea: ida_idaapi.ea_t) -> bool

.. py:function:: func_parent_iterator_set(fpi: func_parent_iterator_t, pfn: func_t) -> bool

.. py:function:: f_any(arg1: flags64_t, arg2: void *) -> bool

   Helper function to accept any address.


.. py:class:: func_tail_iterator_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: set(*args) -> bool


   .. py:method:: set_ea(ea: ida_idaapi.ea_t) -> bool


   .. py:method:: set_range(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool


   .. py:method:: chunk() -> range_t const &


   .. py:method:: first() -> bool


   .. py:method:: last() -> bool


   .. py:method:: prev() -> bool


   .. py:method:: main() -> bool


   .. py:attribute:: next


.. py:class:: func_item_iterator_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: set(*args) -> bool

      Set a function range. if pfn == nullptr then a segment range will be set.



   .. py:method:: set_range(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool

      Set an arbitrary range.



   .. py:method:: first() -> bool


   .. py:method:: last() -> bool


   .. py:method:: current() -> ida_idaapi.ea_t


   .. py:method:: set_ea(_ea: ida_idaapi.ea_t) -> bool


   .. py:method:: chunk() -> range_t const &


   .. py:method:: prev(func: testf_t *) -> bool


   .. py:method:: next_addr() -> bool


   .. py:method:: next_head() -> bool


   .. py:method:: next_code() -> bool


   .. py:method:: next_data() -> bool


   .. py:method:: next_not_tail() -> bool


   .. py:method:: prev_addr() -> bool


   .. py:method:: prev_head() -> bool


   .. py:method:: prev_code() -> bool


   .. py:method:: prev_data() -> bool


   .. py:method:: prev_not_tail() -> bool


   .. py:method:: decode_prev_insn(out: insn_t *) -> bool


   .. py:method:: decode_preceding_insn(visited: eavec_t *, p_farref: bool *, out: insn_t *) -> bool


   .. py:method:: succ(func: testf_t *) -> bool

      Similar to next(), but succ() iterates the chunks from low to high addresses, while next() iterates through chunks starting at the function entry chunk 
              



   .. py:method:: succ_code() -> bool


   .. py:attribute:: next


   .. py:method:: addresses()

      Provide an iterator on addresses contained within the function



   .. py:method:: code_items()

      Provide an iterator on code items contained within the function



   .. py:method:: data_items()

      Provide an iterator on data items contained within the function



   .. py:method:: head_items()

      Provide an iterator on item heads contained within the function



   .. py:method:: not_tails()

      Provide an iterator on non-tail addresses contained within the function



.. py:class:: func_parent_iterator_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: set(_fnt: func_t) -> bool


   .. py:method:: parent() -> ida_idaapi.ea_t


   .. py:method:: first() -> bool


   .. py:method:: last() -> bool


   .. py:method:: prev() -> bool


   .. py:method:: reset_fnt(_fnt: func_t) -> None


   .. py:attribute:: next


.. py:function:: get_prev_func_addr(pfn: func_t, ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

.. py:function:: get_next_func_addr(pfn: func_t, ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

.. py:function:: read_regargs(pfn: func_t) -> None

.. py:function:: add_regarg(pfn: func_t, reg: int, tif: tinfo_t, name: str) -> None

.. py:data:: IDASGN_OK

   ok


.. py:data:: IDASGN_BADARG

   bad number of signature


.. py:data:: IDASGN_APPLIED

   signature is already applied


.. py:data:: IDASGN_CURRENT

   signature is currently being applied


.. py:data:: IDASGN_PLANNED

   signature is planned to be applied


.. py:function:: plan_to_apply_idasgn(fname: str) -> int

   Add a signature file to the list of planned signature files. 
           
   :param fname: file name. should not contain directory part.
   :returns: 0 if failed, otherwise number of planned (and applied) signatures


.. py:function:: apply_idasgn_to(signame: str, ea: ida_idaapi.ea_t, is_startup: bool) -> int

   Apply a signature file to the specified address. 
           
   :param signame: short name of signature file (the file name without path)
   :param ea: address to apply the signature
   :param is_startup: if set, then the signature is treated as a startup one for startup signature ida doesn't rename the first function of the applied module.
   :returns: Library function codes


.. py:function:: get_idasgn_qty() -> int

   Get number of signatures in the list of planned and applied signatures. 
           
   :returns: 0..n


.. py:function:: get_current_idasgn() -> int

   Get number of the the current signature. 
           
   :returns: 0..n-1


.. py:function:: calc_idasgn_state(n: int) -> int

   Get state of a signature in the list of planned signatures 
           
   :param n: number of signature in the list (0..get_idasgn_qty()-1)
   :returns: state of signature or IDASGN_BADARG


.. py:function:: del_idasgn(n: int) -> int

   Remove signature from the list of planned signatures. 
           
   :param n: number of signature in the list (0..get_idasgn_qty()-1)
   :returns: IDASGN_OK, IDASGN_BADARG, IDASGN_APPLIED


.. py:function:: get_idasgn_title(name: str) -> str

   Get full description of the signature by its short name. 
           
   :param name: short name of a signature
   :returns: size of signature description or -1


.. py:function:: apply_startup_sig(ea: ida_idaapi.ea_t, startup: str) -> bool

   Apply a startup signature file to the specified address. 
           
   :param ea: address to apply the signature to; usually idainfo::start_ea
   :param startup: the name of the signature file without path and extension
   :returns: true if successfully applied the signature


.. py:function:: try_to_add_libfunc(ea: ida_idaapi.ea_t) -> int

   Apply the currently loaded signature file to the specified address. If a library function is found, then create a function and name it accordingly. 
           
   :param ea: any address in the program
   :returns: Library function codes


.. py:data:: LIBFUNC_FOUND

   ok, library function is found


.. py:data:: LIBFUNC_NONE

   no, this is not a library function


.. py:data:: LIBFUNC_DELAY

   no decision because of lack of information


.. py:function:: get_fchunk_referer(ea: int, idx)

.. py:function:: get_idasgn_desc(n)

   Get information about a signature in the list.
   It returns: (name of signature, names of optional libraries)

   See also: get_idasgn_desc_with_matches

   :param n: number of signature in the list (0..get_idasgn_qty()-1)
   :returns: None on failure or tuple(signame, optlibs)


.. py:function:: get_idasgn_desc_with_matches(n)

   Get information about a signature in the list.
   It returns: (name of signature, names of optional libraries, number of matches)

   :param n: number of signature in the list (0..get_idasgn_qty()-1)
   :returns: None on failure or tuple(signame, optlibs, nmatches)


.. py:function:: func_t__from_ptrval__(ptrval: size_t) -> func_t *

.. py:function:: calc_thunk_func_target(*args)

   Calculate target of a thunk function. 
           
   :param pfn: pointer to function (may not be nullptr)
   :param fptr: out: will hold address of a function pointer (if indirect jump)
   :returns: the target function or BADADDR



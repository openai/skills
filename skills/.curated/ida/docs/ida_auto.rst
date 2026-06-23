ida_auto
========

.. py:module:: ida_auto

.. autoapi-nested-parse::

   Functions that work with the autoanalyzer queue.

   The autoanalyzer works when IDA is not busy processing the user keystrokes. 
   It has several queues, each queue having its own priority. The analyzer stops 
   when all queues are empty.

   A queue contains addresses or address ranges. The addresses are kept sorted by 
   their values. The analyzer will process all addresses from the first queue, 
   then switch to the second queue and so on. There are no limitations on the 
   size of the queues.

   This file also contains functions that deal with the IDA status indicator and 
   the autoanalysis indicator. You may use these functions to change the 
   indicator value.

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For auto-analysis operations, see :mod:`ida_domain.database`.



Attributes
----------

.. autoapisummary::

   ida_auto.cvar
   ida_auto.AU_NONE
   ida_auto.AU_UNK
   ida_auto.AU_CODE
   ida_auto.AU_WEAK
   ida_auto.AU_PROC
   ida_auto.AU_TAIL
   ida_auto.AU_FCHUNK
   ida_auto.AU_USED
   ida_auto.AU_USD2
   ida_auto.AU_TYPE
   ida_auto.AU_LIBF
   ida_auto.AU_LBF2
   ida_auto.AU_LBF3
   ida_auto.AU_CHLB
   ida_auto.AU_FINAL
   ida_auto.st_Ready
   ida_auto.st_Think
   ida_auto.st_Waiting
   ida_auto.st_Work


Classes
-------

.. autoapisummary::

   ida_auto.auto_display_t


Functions
---------

.. autoapisummary::

   ida_auto.get_auto_state
   ida_auto.set_auto_state
   ida_auto.get_auto_display
   ida_auto.show_auto
   ida_auto.show_addr
   ida_auto.set_ida_state
   ida_auto.may_create_stkvars
   ida_auto.may_trace_sp
   ida_auto.auto_mark_range
   ida_auto.auto_mark
   ida_auto.auto_unmark
   ida_auto.plan_ea
   ida_auto.plan_range
   ida_auto.auto_make_code
   ida_auto.auto_make_proc
   ida_auto.auto_postpone_analysis
   ida_auto.reanalyze_callers
   ida_auto.revert_ida_decisions
   ida_auto.auto_apply_type
   ida_auto.auto_apply_tail
   ida_auto.plan_and_wait
   ida_auto.auto_wait
   ida_auto.auto_wait_range
   ida_auto.auto_make_step
   ida_auto.auto_cancel
   ida_auto.auto_is_ok
   ida_auto.peek_auto_queue
   ida_auto.auto_get
   ida_auto.auto_recreate_insn
   ida_auto.is_auto_enabled
   ida_auto.enable_auto


Module Contents
---------------

.. py:function:: get_auto_state() -> atype_t

   Get current state of autoanalyzer. If auto_state == AU_NONE, IDA is currently not running the analysis (it could be temporarily interrupted to perform the user's requests, for example). 
           


.. py:function:: set_auto_state(new_state: atype_t) -> atype_t

   Set current state of autoanalyzer. 
           
   :param new_state: new state of autoanalyzer
   :returns: previous state


.. py:class:: auto_display_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: type
      :type:  atype_t


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: state
      :type:  idastate_t


.. py:data:: cvar

.. py:data:: AU_NONE

   placeholder, not used


.. py:data:: AU_UNK

   0: convert to unexplored


.. py:data:: AU_CODE

   1: convert to instruction


.. py:data:: AU_WEAK

   2: convert to instruction (ida decision)


.. py:data:: AU_PROC

   3: convert to procedure start


.. py:data:: AU_TAIL

   4: add a procedure tail


.. py:data:: AU_FCHUNK

   5: find func chunks


.. py:data:: AU_USED

   6: reanalyze


.. py:data:: AU_USD2

   7: reanalyze, second pass


.. py:data:: AU_TYPE

   8: apply type information


.. py:data:: AU_LIBF

   9: apply signature to address


.. py:data:: AU_LBF2

   10: the same, second pass


.. py:data:: AU_LBF3

   11: the same, third pass


.. py:data:: AU_CHLB

   12: load signature file (file name is kept separately)


.. py:data:: AU_FINAL

   13: final pass


.. py:data:: st_Ready

   READY: IDA is doing nothing.


.. py:data:: st_Think

   THINKING: Autoanalysis on, the user may press keys.


.. py:data:: st_Waiting

   WAITING: Waiting for the user input.


.. py:data:: st_Work

   BUSY: IDA is busy.


.. py:function:: get_auto_display(auto_display: auto_display_t) -> bool

   Get structure which holds the autoanalysis indicator contents.


.. py:function:: show_auto(*args) -> None

   Change autoanalysis indicator value. 
           
   :param ea: linear address being analyzed
   :param type: autoanalysis type (see Autoanalysis queues)


.. py:function:: show_addr(ea: ida_idaapi.ea_t) -> None

   Show an address on the autoanalysis indicator. The address is displayed in the form " @:12345678". 
           
   :param ea: - linear address to display


.. py:function:: set_ida_state(st: idastate_t) -> idastate_t

   Change IDA status indicator value 
           
   :param st: - new indicator status
   :returns: old indicator status


.. py:function:: may_create_stkvars() -> bool

   Is it allowed to create stack variables automatically?. This function should be used by IDP modules before creating stack vars. 
           


.. py:function:: may_trace_sp() -> bool

   Is it allowed to trace stack pointer automatically?. This function should be used by IDP modules before tracing sp. 
           


.. py:function:: auto_mark_range(start: ida_idaapi.ea_t, end: ida_idaapi.ea_t, type: atype_t) -> None

   Put range of addresses into a queue. 'start' may be higher than 'end', the kernel will swap them in this case. 'end' doesn't belong to the range. 
           


.. py:function:: auto_mark(ea: ida_idaapi.ea_t, type: atype_t) -> None

   Put single address into a queue. Queues keep addresses sorted.


.. py:function:: auto_unmark(start: ida_idaapi.ea_t, end: ida_idaapi.ea_t, type: atype_t) -> None

   Remove range of addresses from a queue. 'start' may be higher than 'end', the kernel will swap them in this case. 'end' doesn't belong to the range. 
           


.. py:function:: plan_ea(ea: ida_idaapi.ea_t) -> None

   Plan to perform reanalysis.


.. py:function:: plan_range(sEA: ida_idaapi.ea_t, eEA: ida_idaapi.ea_t) -> None

   Plan to perform reanalysis.


.. py:function:: auto_make_code(ea: ida_idaapi.ea_t) -> None

   Plan to make code.


.. py:function:: auto_make_proc(ea: ida_idaapi.ea_t) -> None

   Plan to make code&function.


.. py:function:: auto_postpone_analysis(ea: ida_idaapi.ea_t) -> bool

   Plan to reanalyze on the second pass The typical usage of this function in emu.cpp is: if ( !auto_postpone_analysis(ea) ) op_offset(ea, 0, ...); (we make an offset only on the second pass) 
           


.. py:function:: reanalyze_callers(ea: ida_idaapi.ea_t, noret: bool) -> None

   Plan to reanalyze callers of the specified address. This function will add to AU_USED queue all instructions that call (not jump to) the specified address. 
           
   :param ea: linear address of callee
   :param noret: !=0: the callee doesn't return, mark to undefine subsequent instructions in the caller. 0: do nothing.


.. py:function:: revert_ida_decisions(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> None

   Delete all analysis info that IDA generated for for the given range.


.. py:function:: auto_apply_type(caller: ida_idaapi.ea_t, callee: ida_idaapi.ea_t) -> None

   Plan to apply the callee's type to the calling point.


.. py:function:: auto_apply_tail(tail_ea: ida_idaapi.ea_t, parent_ea: ida_idaapi.ea_t) -> None

   Plan to apply the tail_ea chunk to the parent 
           
   :param tail_ea: linear address of start of tail
   :param parent_ea: linear address within parent. If BADADDR, automatically try to find parent via xrefs.


.. py:function:: plan_and_wait(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, final_pass: bool = True) -> int

   Analyze the specified range. Try to create instructions where possible. Make the final pass over the specified range if specified. This function doesn't return until the range is analyzed. 
           
   :returns: 1: ok
   :returns: 0: Ctrl-Break was pressed


.. py:function:: auto_wait() -> bool

   Process everything in the queues and return true. 
           
   :returns: false if the user clicked cancel. (the wait box must be displayed by the caller if desired)


.. py:function:: auto_wait_range(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> ssize_t

   Process everything in the specified range and return true. 
           
   :returns: number of autoanalysis steps made. -1 if the user clicked cancel. (the wait box must be displayed by the caller if desired)


.. py:function:: auto_make_step(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool

   Analyze one address in the specified range and return true. 
           
   :returns: if processed anything. false means that there is nothing to process in the specified range.


.. py:function:: auto_cancel(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> None

   Remove an address range (ea1..ea2) from queues AU_CODE, AU_PROC, AU_USED. To remove an address range from other queues use auto_unmark() function. 'ea1' may be higher than 'ea2', the kernel will swap them in this case. 'ea2' doesn't belong to the range. 
           


.. py:function:: auto_is_ok() -> bool

   Are all queues empty? (i.e. has autoanalysis finished?). 
           


.. py:function:: peek_auto_queue(low_ea: ida_idaapi.ea_t, type: atype_t) -> ida_idaapi.ea_t

   Peek into a queue 'type' for an address not lower than 'low_ea'. Do not remove address from the queue. 
           
   :returns: the address or BADADDR


.. py:function:: auto_get(type: atype_t *, lowEA: ida_idaapi.ea_t, highEA: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Retrieve an address from queues regarding their priority. Returns BADADDR if no addresses not lower than 'lowEA' and less than 'highEA' are found in the queues. Otherwise *type will have queue type. 
           


.. py:function:: auto_recreate_insn(ea: ida_idaapi.ea_t) -> int

   Try to create instruction 
           
   :param ea: linear address of callee
   :returns: the length of the instruction or 0


.. py:function:: is_auto_enabled() -> bool

   Get autoanalyzer state.


.. py:function:: enable_auto(enable: bool) -> bool

   Temporarily enable/disable autoanalyzer. Not user-facing, but rather because IDA sometimes need to turn AA on/off regardless of inf.s_genflags:INFFL_AUTO 
           
   :returns: old state



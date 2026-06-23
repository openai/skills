ida_frame
=========

.. py:module:: ida_frame

.. autoapi-nested-parse::

   Routines to manipulate function stack frames, stack variables, register variables and local labels.

   The frame is represented as a structure::

     +------------------------------------------------+
     | function arguments                             |
     +------------------------------------------------+
     | return address (isn't stored in func_t)        |
     +------------------------------------------------+
     | saved registers (SI, DI, etc - func_t::frregs) |
     +------------------------------------------------+ <- typical BP
     |                                                |  |
     |                                                |  | func_t::fpd
     |                                                |  |
     |                                                | <- real BP
     | local variables (func_t::frsize)               |
     |                                                |
     |                                                |
     +------------------------------------------------+ <- SP

   To access the structure of a function frame and stack variables, use:

   * tinfo_t::get_func_frame(const func_t *pfn) (the preferred way)
   * get_func_frame(tinfo_t *out, const func_t *pfn)
   * tinfo_t::get_udt_details() gives info about stack variables: their type, 
     names, offset, etc

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For function frame operations, see :mod:`ida_domain.functions`.



Attributes
----------

.. autoapisummary::

   ida_frame.FRAME_UDM_NAME_R
   ida_frame.FRAME_UDM_NAME_S
   ida_frame.FPC_ARGS
   ida_frame.FPC_RETADDR
   ida_frame.FPC_SAVREGS
   ida_frame.FPC_LVARS
   ida_frame.STKVAR_VALID_SIZE
   ida_frame.STKVAR_KEEP_EXISTING
   ida_frame.REGVAR_ERROR_OK
   ida_frame.REGVAR_ERROR_ARG
   ida_frame.REGVAR_ERROR_RANGE
   ida_frame.REGVAR_ERROR_NAME


Classes
-------

.. autoapisummary::

   ida_frame.xreflist_t
   ida_frame.stkpnt_t
   ida_frame.stkpnts_t
   ida_frame.regvar_t
   ida_frame.xreflist_entry_t


Functions
---------

.. autoapisummary::

   ida_frame.is_funcarg_off
   ida_frame.lvar_off
   ida_frame.add_frame
   ida_frame.del_frame
   ida_frame.set_frame_size
   ida_frame.get_frame_size
   ida_frame.get_frame_retsize
   ida_frame.get_frame_part
   ida_frame.frame_off_args
   ida_frame.frame_off_retaddr
   ida_frame.frame_off_savregs
   ida_frame.frame_off_lvars
   ida_frame.get_func_frame
   ida_frame.soff_to_fpoff
   ida_frame.update_fpd
   ida_frame.set_purged
   ida_frame.define_stkvar
   ida_frame.add_frame_member
   ida_frame.is_anonymous_member_name
   ida_frame.is_dummy_member_name
   ida_frame.is_special_frame_member
   ida_frame.set_frame_member_type
   ida_frame.delete_frame_members
   ida_frame.build_stkvar_name
   ida_frame.calc_stkvar_struc_offset
   ida_frame.calc_frame_offset
   ida_frame.free_regvar
   ida_frame.add_regvar
   ida_frame.find_regvar
   ida_frame.has_regvar
   ida_frame.rename_regvar
   ida_frame.set_regvar_cmt
   ida_frame.del_regvar
   ida_frame.add_auto_stkpnt
   ida_frame.add_user_stkpnt
   ida_frame.del_stkpnt
   ida_frame.get_spd
   ida_frame.get_effective_spd
   ida_frame.get_sp_delta
   ida_frame.set_auto_spd
   ida_frame.recalc_spd
   ida_frame.recalc_spd_for_basic_block
   ida_frame.build_stkvar_xrefs


Module Contents
---------------

.. py:class:: xreflist_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> xreflist_entry_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> xreflist_entry_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: xreflist_t) -> None


   .. py:method:: extract() -> xreflist_entry_t *


   .. py:method:: inject(s: xreflist_entry_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< xreflist_entry_t >::const_iterator


   .. py:method:: end(*args) -> qvector< xreflist_entry_t >::const_iterator


   .. py:method:: insert(it: xreflist_entry_t, x: xreflist_entry_t) -> qvector< xreflist_entry_t >::iterator


   .. py:method:: erase(*args) -> qvector< xreflist_entry_t >::iterator


   .. py:method:: find(*args) -> qvector< xreflist_entry_t >::const_iterator


   .. py:method:: has(x: xreflist_entry_t) -> bool


   .. py:method:: add_unique(x: xreflist_entry_t) -> bool


   .. py:method:: append(x: xreflist_entry_t) -> None


   .. py:method:: extend(x: xreflist_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:function:: is_funcarg_off(pfn: func_t const *, frameoff: int) -> bool

.. py:function:: lvar_off(pfn: func_t const *, frameoff: int) -> int

.. py:data:: FRAME_UDM_NAME_R

.. py:data:: FRAME_UDM_NAME_S

.. py:class:: stkpnt_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: spd
      :type:  int


   .. py:method:: compare(r: stkpnt_t) -> int


.. py:class:: stkpnts_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: compare(r: stkpnts_t) -> int


.. py:function:: add_frame(pfn: func_t *, frsize: int, frregs: ushort, argsize: asize_t) -> bool

   Add function frame. 
           
   :param pfn: pointer to function structure
   :param frsize: size of function local variables
   :param frregs: size of saved registers
   :param argsize: size of function arguments range which will be purged upon return. this parameter is used for __stdcall and __pascal calling conventions. for other calling conventions please pass 0.
   :returns: 1: ok
   :returns: 0: failed (no function, frame already exists)


.. py:function:: del_frame(pfn: func_t *) -> bool

   Delete a function frame. 
           
   :param pfn: pointer to function structure
   :returns: success


.. py:function:: set_frame_size(pfn: func_t *, frsize: asize_t, frregs: ushort, argsize: asize_t) -> bool

   Set size of function frame. Note: The returned size may not include all stack arguments. It does so only for __stdcall and __fastcall calling conventions. To get the entire frame size for all cases use frame.get_func_frame(pfn).get_size() 
           
   :param pfn: pointer to function structure
   :param frsize: size of function local variables
   :param frregs: size of saved registers
   :param argsize: size of function arguments that will be purged from the stack upon return
   :returns: success


.. py:function:: get_frame_size(pfn: func_t const *) -> asize_t

   Get full size of a function frame. This function takes into account size of local variables + size of saved registers + size of return address + number of purged bytes. The purged bytes correspond to the arguments of the functions with __stdcall and __fastcall calling conventions. 
           
   :param pfn: pointer to function structure, may be nullptr
   :returns: size of frame in bytes or zero


.. py:function:: get_frame_retsize(pfn: func_t const *) -> int

   Get size of function return address. 
           
   :param pfn: pointer to function structure, can't be nullptr


.. py:data:: FPC_ARGS

.. py:data:: FPC_RETADDR

.. py:data:: FPC_SAVREGS

.. py:data:: FPC_LVARS

.. py:function:: get_frame_part(range: range_t, pfn: func_t const *, part: frame_part_t) -> None

   Get offsets of the frame part in the frame. 
           
   :param range: pointer to the output buffer with the frame part start/end(exclusive) offsets, can't be nullptr
   :param pfn: pointer to function structure, can't be nullptr
   :param part: frame part


.. py:function:: frame_off_args(pfn: func_t const *) -> ida_idaapi.ea_t

   Get starting address of arguments section.


.. py:function:: frame_off_retaddr(pfn: func_t const *) -> ida_idaapi.ea_t

   Get starting address of return address section.


.. py:function:: frame_off_savregs(pfn: func_t const *) -> ida_idaapi.ea_t

   Get starting address of saved registers section.


.. py:function:: frame_off_lvars(pfn: func_t const *) -> ida_idaapi.ea_t

   Get start address of local variables section.


.. py:function:: get_func_frame(out: tinfo_t, pfn: func_t const *) -> bool

   Get type of function frame 
           
   :param out: type info
   :param pfn: pointer to function structure
   :returns: success


.. py:function:: soff_to_fpoff(pfn: func_t *, soff: int) -> int

   Convert struct offsets into fp-relative offsets. This function converts the offsets inside the udt_type_data_t object into the frame pointer offsets (for example, EBP-relative). 
           


.. py:function:: update_fpd(pfn: func_t *, fpd: asize_t) -> bool

   Update frame pointer delta. 
           
   :param pfn: pointer to function structure
   :param fpd: new fpd value. cannot be bigger than the local variable range size.
   :returns: success


.. py:function:: set_purged(ea: ida_idaapi.ea_t, nbytes: int, override_old_value: bool) -> bool

   Set the number of purged bytes for a function or data item (funcptr). This function will update the database and plan to reanalyze items referencing the specified address. It works only for processors with PR_PURGING bit in 16 and 32 bit modes. 
           
   :param ea: address of the function of item
   :param nbytes: number of purged bytes
   :param override_old_value: may overwrite old information about purged bytes
   :returns: success


.. py:data:: STKVAR_VALID_SIZE

   x.dtyp contains correct variable type (for insns like 'lea' this bit must be off). In general, dr_O references do not allow to determine the variable size 
           


.. py:data:: STKVAR_KEEP_EXISTING

   if a stack variable for this operand already exists then we do not create a new variable 
           


.. py:function:: define_stkvar(pfn: func_t *, name: str, off: int, tif: tinfo_t, repr: value_repr_t = None) -> bool

   Define/redefine a stack variable. 
           
   :param pfn: pointer to function
   :param name: variable name, nullptr means autogenerate a name
   :param off: offset of the stack variable in the frame. negative values denote local variables, positive - function arguments.
   :param tif: variable type
   :param repr: variable representation
   :returns: success


.. py:function:: add_frame_member(pfn: func_t const *, name: str, offset: int, tif: tinfo_t, repr: value_repr_t = None, etf_flags: uint = 0) -> bool

   Add member to the frame type 
           
   :param pfn: pointer to function
   :param name: variable name, nullptr means autogenerate a name
   :param offset: member offset in the frame structure, in bytes
   :param tif: variable type
   :param repr: variable representation
   :returns: success


.. py:function:: is_anonymous_member_name(name: str) -> bool

   Is member name prefixed with "anonymous"?


.. py:function:: is_dummy_member_name(name: str) -> bool

   Is member name an auto-generated name?


.. py:function:: is_special_frame_member(tid: tid_t) -> bool

   Is stkvar with TID the return address slot or the saved registers slot ? 
           
   :param tid: frame member type id return address or saved registers member?


.. py:function:: set_frame_member_type(pfn: func_t const *, offset: int, tif: tinfo_t, repr: value_repr_t = None, etf_flags: uint = 0) -> bool

   Change type of the frame member 
           
   :param pfn: pointer to function
   :param offset: member offset in the frame structure, in bytes
   :param tif: variable type
   :param repr: variable representation
   :returns: success


.. py:function:: delete_frame_members(pfn: func_t const *, start_offset: int, end_offset: int) -> bool

   Delete frame members 
           
   :param pfn: pointer to function
   :param start_offset: member offset to start deletion from, in bytes
   :param end_offset: member offset which not included in the deletion, in bytes
   :returns: success


.. py:function:: build_stkvar_name(pfn: func_t const *, v: int) -> str

   Build automatic stack variable name. 
           
   :param pfn: pointer to function (can't be nullptr!)
   :param v: value of variable offset
   :returns: length of stack variable name or -1


.. py:function:: calc_stkvar_struc_offset(pfn: func_t *, insn: insn_t const &, n: int) -> ida_idaapi.ea_t

   Calculate offset of stack variable in the frame structure. 
           
   :param pfn: pointer to function (cannot be nullptr)
   :param insn: the instruction
   :param n: 0..UA_MAXOP-1 operand number -1 if error, return BADADDR
   :returns: BADADDR if some error (issue a warning if stack frame is bad)


.. py:function:: calc_frame_offset(pfn: func_t *, off: int, insn: insn_t const * = None, op: op_t const * = None) -> int

   Calculate the offset of stack variable in the frame. 
           
   :param pfn: pointer to function (cannot be nullptr)
   :param off: the offset relative to stack pointer or frame pointer
   :param insn: the instruction
   :param op: the operand
   :returns: the offset in the frame


.. py:function:: free_regvar(v: regvar_t) -> None

.. py:class:: regvar_t(*args)

   Bases: :py:obj:`ida_range.range_t`


   .. py:attribute:: thisown


   .. py:attribute:: canon
      :type:  char *

      canonical register name (case-insensitive)



   .. py:attribute:: user
      :type:  char *

      user-defined register name



   .. py:attribute:: cmt
      :type:  char *

      comment to appear near definition



   .. py:method:: swap(r: regvar_t) -> None


.. py:function:: add_regvar(pfn: func_t *, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, canon: str, user: str, cmt: str) -> int

   Define a register variable. 
           
   :param pfn: function in which the definition will be created
   :param ea1: range of addresses within the function where the definition will be used
   :param ea2: range of addresses within the function where the definition will be used
   :param canon: name of a general register
   :param user: user-defined name for the register
   :param cmt: comment for the definition
   :returns: Register variable error codes


.. py:data:: REGVAR_ERROR_OK

   all ok


.. py:data:: REGVAR_ERROR_ARG

   function arguments are bad


.. py:data:: REGVAR_ERROR_RANGE

   the definition range is bad


.. py:data:: REGVAR_ERROR_NAME

   the provided name(s) can't be accepted


.. py:function:: find_regvar(*args) -> regvar_t *

   This function has the following signatures:

       0. find_regvar(pfn: func_t *, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, canon: str, user: str) -> regvar_t *
       1. find_regvar(pfn: func_t *, ea: ida_idaapi.ea_t, canon: str) -> regvar_t *

   # 0: find_regvar(pfn: func_t *, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, canon: str, user: str) -> regvar_t *

   Find a register variable definition (powerful version). One of 'canon' and 'user' should be nullptr. If both 'canon' and 'user' are nullptr it returns the first regvar definition in the range. 
           
   :returns: nullptr-not found, otherwise ptr to regvar_t

   # 1: find_regvar(pfn: func_t *, ea: ida_idaapi.ea_t, canon: str) -> regvar_t *

   Find a register variable definition. 
           
   :returns: nullptr-not found, otherwise ptr to regvar_t


.. py:function:: has_regvar(pfn: func_t *, ea: ida_idaapi.ea_t) -> bool

   Is there a register variable definition? 
           
   :param pfn: function in question
   :param ea: current address


.. py:function:: rename_regvar(pfn: func_t *, v: regvar_t, user: str) -> int

   Rename a register variable. 
           
   :param pfn: function in question
   :param v: variable to rename
   :param user: new user-defined name for the register
   :returns: Register variable error codes


.. py:function:: set_regvar_cmt(pfn: func_t *, v: regvar_t, cmt: str) -> int

   Set comment for a register variable. 
           
   :param pfn: function in question
   :param v: variable to rename
   :param cmt: new comment
   :returns: Register variable error codes


.. py:function:: del_regvar(pfn: func_t *, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, canon: str) -> int

   Delete a register variable definition. 
           
   :param pfn: function in question
   :param ea1: range of addresses within the function where the definition holds
   :param ea2: range of addresses within the function where the definition holds
   :param canon: name of a general register
   :returns: Register variable error codes


.. py:function:: add_auto_stkpnt(pfn: func_t *, ea: ida_idaapi.ea_t, delta: int) -> bool

   Add automatic SP register change point. 
           
   :param pfn: pointer to the function. may be nullptr.
   :param ea: linear address where SP changes. usually this is the end of the instruction which modifies the stack pointer ( insn_t::ea+ insn_t::size)
   :param delta: difference between old and new values of SP
   :returns: success


.. py:function:: add_user_stkpnt(ea: ida_idaapi.ea_t, delta: int) -> bool

   Add user-defined SP register change point. 
           
   :param ea: linear address where SP changes
   :param delta: difference between old and new values of SP
   :returns: success


.. py:function:: del_stkpnt(pfn: func_t *, ea: ida_idaapi.ea_t) -> bool

   Delete SP register change point. 
           
   :param pfn: pointer to the function. may be nullptr.
   :param ea: linear address
   :returns: success


.. py:function:: get_spd(pfn: func_t *, ea: ida_idaapi.ea_t) -> int

   Get difference between the initial and current values of ESP. 
           
   :param pfn: pointer to the function. may be nullptr.
   :param ea: linear address of the instruction
   :returns: 0 or the difference, usually a negative number. returns the sp-diff before executing the instruction.


.. py:function:: get_effective_spd(pfn: func_t *, ea: ida_idaapi.ea_t) -> int

   Get effective difference between the initial and current values of ESP. This function returns the sp-diff used by the instruction. The difference between get_spd() and get_effective_spd() is present only for instructions like "pop [esp+N]": they modify sp and use the modified value. 
           
   :param pfn: pointer to the function. may be nullptr.
   :param ea: linear address
   :returns: 0 or the difference, usually a negative number


.. py:function:: get_sp_delta(pfn: func_t *, ea: ida_idaapi.ea_t) -> int

   Get modification of SP made at the specified location 
           
   :param pfn: pointer to the function. may be nullptr.
   :param ea: linear address
   :returns: 0 if the specified location doesn't contain a SP change point. otherwise return delta of SP modification.


.. py:function:: set_auto_spd(pfn: func_t *, ea: ida_idaapi.ea_t, new_spd: int) -> bool

   Add such an automatic SP register change point so that at EA the new cumulative SP delta (that is, the difference between the initial and current values of SP) would be equal to NEW_SPD. 
           
   :param pfn: pointer to the function. may be nullptr.
   :param ea: linear address of the instruction
   :param new_spd: new value of the cumulative SP delta
   :returns: success


.. py:function:: recalc_spd(cur_ea: ida_idaapi.ea_t) -> bool

   Recalculate SP delta for an instruction that stops execution. The next instruction is not reached from the current instruction. We need to recalculate SP for the next instruction.
   This function will create a new automatic SP register change point if necessary. It should be called from the emulator (emu.cpp) when auto_state == AU_USED if the current instruction doesn't pass the execution flow to the next instruction. 
           
   :param cur_ea: linear address of the current instruction
   :returns: 1: new stkpnt is added
   :returns: 0: nothing is changed


.. py:function:: recalc_spd_for_basic_block(pfn: func_t *, cur_ea: ida_idaapi.ea_t) -> bool

   Recalculate SP delta for the current instruction. The typical code snippet to calculate SP delta in a proc module is:

   if ( may_trace_sp() && pfn != nullptr )
     if ( !recalc_spd_for_basic_block(pfn, insn.ea) )
       trace_sp(pfn, insn);

   where trace_sp() is a typical name for a function that emulates the SP change of an instruction.

   :param pfn: pointer to the function
   :param cur_ea: linear address of the current instruction
   :returns: true: the cumulative SP delta is set
   :returns: false: the instruction at CUR_EA passes flow to the next instruction. SP delta must be set as a result of emulating the current instruction.


.. py:class:: xreflist_entry_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      Location of the insn referencing the stack frame member.



   .. py:attribute:: opnum
      :type:  uchar

      Number of the operand of that instruction.



   .. py:attribute:: type
      :type:  uchar

      The type of xref (cref_t & dref_t)



   .. py:method:: compare(r: xreflist_entry_t) -> int


.. py:function:: build_stkvar_xrefs(out: xreflist_t, pfn: func_t *, start_offset: int, end_offset: int) -> None

   Fill 'out' with a list of all the xrefs made from function 'pfn' to specified range of the pfn's stack frame. 
           
   :param out: the list of xrefs to fill.
   :param pfn: the function to scan.
   :param start_offset: start frame structure offset, in bytes
   :param end_offset: end frame structure offset, in bytes



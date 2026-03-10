ida_regfinder
=============

.. py:module:: ida_regfinder


Attributes
----------

.. autoapisummary::

   ida_regfinder.cvar


Classes
-------

.. autoapisummary::

   ida_regfinder.reg_value_def_t
   ida_regfinder.reg_value_info_t


Functions
---------

.. autoapisummary::

   ida_regfinder.find_reg_value
   ida_regfinder.find_sp_value
   ida_regfinder.find_reg_value_info
   ida_regfinder.find_nearest_rvi
   ida_regfinder.invalidate_regfinder_cache
   ida_regfinder.invalidate_regfinder_xrefs_cache


Module Contents
---------------

.. py:class:: reg_value_def_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: val
      :type:  uint64

      the value



   .. py:attribute:: def_ea
      :type:  ida_idaapi.ea_t

      the instruction address



   .. py:attribute:: def_itype
      :type:  uint16

      the instruction code (processor specific)



   .. py:attribute:: flags
      :type:  uint16

      additional info about the value



   .. py:attribute:: SHORT_INSN

      like 'addi reg, imm'



   .. py:attribute:: PC_BASED

      the value depends on DEF_EA only for numbers 
              



   .. py:attribute:: LIKE_GOT

      the value is like GOT only for numbers 
              



   .. py:method:: is_short_insn(*args) -> bool

      This function has the following signatures:

          0. is_short_insn() -> bool
          1. is_short_insn(insn: const insn_t &) -> bool

      # 0: is_short_insn() -> bool


      # 1: is_short_insn(insn: const insn_t &) -> bool



   .. py:method:: is_pc_based() -> bool


   .. py:method:: is_like_got() -> bool


   .. py:attribute:: NOVAL

      without a value



   .. py:attribute:: UVAL

      as a number



   .. py:attribute:: SPVAL

      as a SP delta



   .. py:attribute:: ABORTED

      as an ABORTED value



   .. py:method:: dstr(how: reg_value_def_t::dstr_val_t, pm: procmod_t = None) -> str

      Return the string representation.



.. py:data:: cvar

.. py:class:: reg_value_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: clear() -> None

      Undefine the value.



   .. py:method:: empty() -> bool

      Return 'true' if we know nothing about a value.



   .. py:method:: swap(r: reg_value_info_t) -> None


   .. py:method:: make_dead_end(dead_end_ea: ida_idaapi.ea_t) -> reg_value_info_t
      :staticmethod:


      Return the undefined value because of a dead end. 
              



   .. py:method:: make_aborted(bblk_ea: ida_idaapi.ea_t, aborting_depth: int = -1) -> reg_value_info_t
      :staticmethod:


      Return the value after aborting. 
              



   .. py:method:: make_badinsn(insn_ea: ida_idaapi.ea_t) -> reg_value_info_t
      :staticmethod:


      Return the unknown value after a bad insn. 
              



   .. py:method:: make_unkinsn(insn: insn_t const &) -> reg_value_info_t
      :staticmethod:


      Return the unknown value after executing the insn. 
              



   .. py:method:: make_unkfunc(func_ea: ida_idaapi.ea_t) -> reg_value_info_t
      :staticmethod:


      Return the unknown value from the function start. 
              



   .. py:method:: make_unkloop(bblk_ea: ida_idaapi.ea_t) -> reg_value_info_t
      :staticmethod:


      Return the unknown value if it changes in a loop. 
              



   .. py:method:: make_unkmult(bblk_ea: ida_idaapi.ea_t) -> reg_value_info_t
      :staticmethod:


      Return the unknown value if the register has incompatible values. 
              



   .. py:method:: make_unkxref(bblk_ea: ida_idaapi.ea_t) -> reg_value_info_t
      :staticmethod:


      Return the unknown value if there are too many xrefs. 
              



   .. py:method:: make_unkvals(bblk_ea: ida_idaapi.ea_t) -> reg_value_info_t
      :staticmethod:


      Return the unknown value if the register has too many values. 
              



   .. py:method:: make_num(*args) -> reg_value_info_t
      :staticmethod:


      This function has the following signatures:

          0. make_num(rval: int, insn: const insn_t &, val_flags: uint16=0) -> reg_value_info_t
          1. make_num(rval: int, val_ea: ida_idaapi.ea_t, val_flags: uint16=0) -> reg_value_info_t

      # 0: make_num(rval: int, insn: const insn_t &, val_flags: uint16=0) -> reg_value_info_t

      Return the value that is the RVAL number. 
              

      # 1: make_num(rval: int, val_ea: ida_idaapi.ea_t, val_flags: uint16=0) -> reg_value_info_t

      Return the value that is the RVAL number. 
              



   .. py:method:: make_initial_sp(func_ea: ida_idaapi.ea_t) -> reg_value_info_t
      :staticmethod:


      Return the value that is the initial stack pointer. 
              



   .. py:method:: is_dead_end() -> bool

      Return 'true' if the value is undefined because of a dead end.



   .. py:method:: aborted() -> bool

      Return 'true' if the tracking process was aborted.



   .. py:method:: is_special() -> bool

      Return 'true' if the value requires special handling.



   .. py:method:: is_badinsn() -> bool

      Return 'true' if the value is unknown because of a bad insn.



   .. py:method:: is_unkinsn() -> bool

      Return 'true' if the value is unknown after executing the insn.



   .. py:method:: is_unkfunc() -> bool

      Return 'true' if the value is unknown from the function start.



   .. py:method:: is_unkloop() -> bool

      Return 'true' if the value is unknown because it changes in a loop.



   .. py:method:: is_unkmult() -> bool

      Return 'true' if the value is unknown because the register has incompatible values (a number and SP delta). 
              



   .. py:method:: is_unkxref() -> bool

      Return 'true' if the value is unknown because there are too many xrefs.



   .. py:method:: is_unkvals() -> bool

      Return 'true' if the value is unknown because the register has too many values. 
              



   .. py:method:: is_unknown() -> bool

      Return 'true' if the value is unknown.



   .. py:method:: is_num() -> bool

      Return 'true' if the value is a constant.



   .. py:method:: is_spd() -> bool

      Return 'true' if the value depends on the stack pointer.



   .. py:method:: is_known() -> bool

      Return 'true' if the value is known (i.e. it is a number or SP delta).



   .. py:method:: get_num() -> bool

      Return the number if the value is a constant. 
              



   .. py:method:: get_spd() -> bool

      Return the SP delta if the value depends on the stack pointer. 
              



   .. py:method:: get_def_ea() -> ida_idaapi.ea_t

      Return the defining address.



   .. py:method:: get_def_itype() -> uint16

      Return the defining instruction code (processor specific).



   .. py:method:: get_aborting_depth() -> int

      Return the aborting depth if the value is ABORTED.



   .. py:method:: is_value_unique() -> bool

      Check that the value is unique.



   .. py:method:: have_all_vals_flag(val_flags: uint16) -> bool

      Check the given flag for each value.



   .. py:method:: has_any_vals_flag(val_flags: uint16) -> bool


   .. py:method:: is_all_vals_pc_based() -> bool


   .. py:method:: is_any_vals_pc_based() -> bool


   .. py:method:: is_all_vals_like_got() -> bool


   .. py:method:: is_any_vals_like_got() -> bool


   .. py:method:: set_all_vals_flag(val_flags: uint16) -> None

      Set the given flag for each value.



   .. py:method:: set_all_vals_pc_based() -> None


   .. py:method:: set_all_vals_got_based() -> None


   .. py:method:: set_dead_end(dead_end_ea: ida_idaapi.ea_t) -> None

      Set the value to be undefined because of a dead end. 
              



   .. py:method:: set_badinsn(insn_ea: ida_idaapi.ea_t) -> None

      Set the value to be unknown after a bad insn. 
              



   .. py:method:: set_unkinsn(insn: insn_t const &) -> None

      Set the value to be unknown after executing the insn. 
              



   .. py:method:: set_unkfunc(func_ea: ida_idaapi.ea_t) -> None

      Set the value to be unknown from the function start. 
              



   .. py:method:: set_unkloop(bblk_ea: ida_idaapi.ea_t) -> None

      Set the value to be unknown because it changes in a loop. 
              



   .. py:method:: set_unkmult(bblk_ea: ida_idaapi.ea_t) -> None

      Set the value to be unknown because the register has incompatible values. 
              



   .. py:method:: set_unkxref(bblk_ea: ida_idaapi.ea_t) -> None

      Set the value to be unknown because there are too many xrefs. 
              



   .. py:method:: set_unkvals(bblk_ea: ida_idaapi.ea_t) -> None

      Set the value to be unknown because the register has too many values. 
              



   .. py:method:: set_aborted(bblk_ea: ida_idaapi.ea_t, aborting_depth: int = -1) -> None

      Set the value after aborting. 
              



   .. py:method:: set_num(*args) -> None

      This function has the following signatures:

          0. set_num(rval: int, insn: const insn_t &, val_flags: uint16=0) -> None
          1. set_num(rvals: uvalvec_t *, insn: const insn_t &) -> None
          2. set_num(rval: int, val_ea: ida_idaapi.ea_t, val_flags: uint16=0) -> None

      # 0: set_num(rval: int, insn: const insn_t &, val_flags: uint16=0) -> None

      Set the value to be a number after executing an insn. 
              

      # 1: set_num(rvals: uvalvec_t *, insn: const insn_t &) -> None

      Set the value to be numbers after executing an insn. 
              

      # 2: set_num(rval: int, val_ea: ida_idaapi.ea_t, val_flags: uint16=0) -> None

      Set the value to be a number before an address. 
              



   .. py:attribute:: EQUAL

      L==R.



   .. py:attribute:: CONTAINS

      L contains R (i.e. R\L is empty)



   .. py:attribute:: CONTAINED

      L is contained in R (i.e. L\R is empty)



   .. py:attribute:: NOT_COMPARABLE

      L\R is not empty and R\L is not empty.



   .. py:method:: vals_union(r: reg_value_info_t) -> reg_value_info_t::set_compare_res_t

      Add values from R into THIS ignoring duplicates. 
              
      :returns: EQUAL: THIS is not changed
      :returns: CONTAINS: THIS is not changed
      :returns: CONTAINED: THIS is a copy of R
      :returns: NOT_COMPARABLE: values from R are added to THIS



   .. py:method:: extend(pm: procmod_t, width: int, is_signed: bool) -> None

      Sign-, or zero-extend the number or SP delta value to full size. The initial value is considered to be of size WIDTH. 
              



   .. py:method:: trunc_uval(pm: procmod_t) -> None

      Truncate the number to the application bitness. 
              



   .. py:attribute:: ADD


   .. py:attribute:: SUB


   .. py:attribute:: OR


   .. py:attribute:: AND


   .. py:attribute:: XOR


   .. py:attribute:: AND_NOT


   .. py:attribute:: SLL


   .. py:attribute:: SLR


   .. py:attribute:: SAR


   .. py:attribute:: MOVT


   .. py:attribute:: NEG


   .. py:attribute:: NOT


   .. py:method:: add(r: reg_value_info_t, insn: insn_t const &) -> None

      Add R to the value, save INSN as a defining instruction. 
              



   .. py:method:: sub(r: reg_value_info_t, insn: insn_t const &) -> None

      Subtract R from the value, save INSN as a defining instruction. 
              



   .. py:method:: bor(r: reg_value_info_t, insn: insn_t const &) -> None

      Make bitwise OR of R to the value, save INSN as a defining instruction. 
              



   .. py:method:: band(r: reg_value_info_t, insn: insn_t const &) -> None

      Make bitwise AND of R to the value, save INSN as a defining instruction. 
              



   .. py:method:: bxor(r: reg_value_info_t, insn: insn_t const &) -> None

      Make bitwise eXclusive OR of R to the value, save INSN as a defining instruction. 
              



   .. py:method:: bandnot(r: reg_value_info_t, insn: insn_t const &) -> None

      Make bitwise AND of the inverse of R to the value, save INSN as a defining instruction. 
              



   .. py:method:: sll(r: reg_value_info_t, insn: insn_t const &) -> None

      Shift the value left by R, save INSN as a defining instruction. 
              



   .. py:method:: slr(r: reg_value_info_t, insn: insn_t const &) -> None

      Shift logically the value right by R, save INSN as a defining instruction. 
              



   .. py:method:: sar(r: reg_value_info_t, insn: insn_t const &) -> None

      Shift arithmetically the value right by R, save INSN as a defining instruction. 
              



   .. py:method:: movt(r: reg_value_info_t, insn: insn_t const &) -> None

      Replace the top 16 bits with bottom 16 bits of R, leaving the bottom 16 bits untouched, save INSN as a defining instruction. 
              



   .. py:method:: neg(insn: insn_t const &) -> None

      Negate the value, save INSN as a defining instruction.



   .. py:method:: bnot(insn: insn_t const &) -> None

      Make bitwise inverse of the value, save INSN as a defining instruction. 
              



   .. py:method:: add_num(*args) -> None

      This function has the following signatures:

          0. add_num(r: int, insn: const insn_t &) -> None
          1. add_num(r: int) -> None

      # 0: add_num(r: int, insn: const insn_t &) -> None

      Add R to the value, save INSN as a defining instruction. 
              

      # 1: add_num(r: int) -> None

      Add R to the value, do not change the defining instructions. 
              



   .. py:method:: shift_left(r: int) -> None

      Shift the value left by R, do not change the defining instructions. 
              



   .. py:method:: shift_right(r: int) -> None

      Shift the value right by R, do not change the defining instructions. 
              



.. py:function:: find_reg_value(ea: ida_idaapi.ea_t, reg: int) -> uint64 *

   Find register value using the register tracker. 
           
   :param ea: the address to find a value at
   :param reg: the register to find
   :returns: 0: no value (the value is varying or the find depth is not enough to find a value)
   :returns: 1: the found value is in VAL
   :returns: -1: the processor module does not support a register tracker


.. py:function:: find_sp_value(ea: ida_idaapi.ea_t, reg: int = -1) -> int64 *

   Find a value of the SP based register using the register tracker. 
           
   :param ea: the address to find a value at
   :param reg: the register to find. by default the SP register is used.
   :returns: 0: no value (the value is varying or the find depth is not enough to find a value)
   :returns: 1: the found value is in VAL
   :returns: -1: the processor module does not support a register tracker


.. py:function:: find_reg_value_info(rvi: reg_value_info_t, ea: ida_idaapi.ea_t, reg: int, max_depth: int = 0) -> bool

   Find register value using the register tracker. 
           
   :param rvi: the found value with additional attributes
   :param ea: the address to find a value at
   :param reg: the register to find
   :param max_depth: the number of basic blocks to look before aborting the search and returning the unknown value. 0 means the value of REGTRACK_MAX_DEPTH from ida.cfg for ordinal registers or REGTRACK_FUNC_MAX_DEPTH for the function-wide registers, -1 means the value of REGTRACK_FUNC_MAX_DEPTH from ida.cfg.
   :returns: 'false': the processor module does not support a register tracker
   :returns: 'true': the found value is in RVI


.. py:function:: find_nearest_rvi(rvi: reg_value_info_t, ea: ida_idaapi.ea_t, reg: int const [2]) -> int

   Find the value of any of the two registers using the register tracker. First, this function tries to find the registers in the basic block of EA, and if it could not do this, then it tries to find in the entire function. 
           
   :param rvi: the found value with additional attributes
   :param ea: the address to find a value at
   :param reg: the registers to find
   :returns: the index of the found register or -1


.. py:function:: invalidate_regfinder_cache(*args) -> None

   The control flow from FROM to TO has removed (CREF==fl_U) or added (CREF!=fl_U). Try to update the register tracker cache after this change. If TO == BADADDR then clear the entire cache. 
           


.. py:function:: invalidate_regfinder_xrefs_cache(*args) -> None

   The data reference to TO has added (DREF!=dr_O) or removed (DREF==dr_O). Update the regtracker xrefs cache after this change. If TO == BADADDR then clear the entire xrefs cache. 
           



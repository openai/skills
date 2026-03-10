ida_fixup
=========

.. py:module:: ida_fixup

.. autoapi-nested-parse::

   Functions that deal with fixup information.

   A loader should setup fixup information using set_fixup(). 
       



Attributes
----------

.. autoapisummary::

   ida_fixup.FIXUP_OFF8
   ida_fixup.FIXUP_OFF16
   ida_fixup.FIXUP_SEG16
   ida_fixup.FIXUP_PTR16
   ida_fixup.FIXUP_OFF32
   ida_fixup.FIXUP_PTR32
   ida_fixup.FIXUP_HI8
   ida_fixup.FIXUP_HI16
   ida_fixup.FIXUP_LOW8
   ida_fixup.FIXUP_LOW16
   ida_fixup.V695_FIXUP_VHIGH
   ida_fixup.V695_FIXUP_VLOW
   ida_fixup.FIXUP_OFF64
   ida_fixup.FIXUP_OFF8S
   ida_fixup.FIXUP_OFF16S
   ida_fixup.FIXUP_OFF32S
   ida_fixup.FIXUP_CUSTOM
   ida_fixup.FIXUPF_REL
   ida_fixup.FIXUPF_EXTDEF
   ida_fixup.FIXUPF_UNUSED
   ida_fixup.FIXUPF_CREATED
   ida_fixup.FIXUPF_LOADER_MASK


Classes
-------

.. autoapisummary::

   ida_fixup.fixup_data_t
   ida_fixup.fixup_info_t


Functions
---------

.. autoapisummary::

   ida_fixup.is_fixup_custom
   ida_fixup.get_fixup
   ida_fixup.exists_fixup
   ida_fixup.set_fixup
   ida_fixup.del_fixup
   ida_fixup.get_first_fixup_ea
   ida_fixup.get_next_fixup_ea
   ida_fixup.get_prev_fixup_ea
   ida_fixup.get_fixup_handler
   ida_fixup.get_fixup_value
   ida_fixup.patch_fixup_value
   ida_fixup.get_fixup_desc
   ida_fixup.calc_fixup_size
   ida_fixup.find_custom_fixup
   ida_fixup.get_fixups
   ida_fixup.contains_fixups
   ida_fixup.gen_fix_fixups
   ida_fixup.handle_fixups_in_macro


Module Contents
---------------

.. py:data:: FIXUP_OFF8

   8-bit offset


.. py:data:: FIXUP_OFF16

   16-bit offset


.. py:data:: FIXUP_SEG16

   16-bit base-logical segment base (selector)


.. py:data:: FIXUP_PTR16

   32-bit long pointer (16-bit base:16-bit offset) 
           


.. py:data:: FIXUP_OFF32

   32-bit offset


.. py:data:: FIXUP_PTR32

   48-bit pointer (16-bit base:32-bit offset)


.. py:data:: FIXUP_HI8

   high 8 bits of 16bit offset


.. py:data:: FIXUP_HI16

   high 16 bits of 32bit offset


.. py:data:: FIXUP_LOW8

   low 8 bits of 16bit offset


.. py:data:: FIXUP_LOW16

   low 16 bits of 32bit offset


.. py:data:: V695_FIXUP_VHIGH

   obsolete


.. py:data:: V695_FIXUP_VLOW

   obsolete


.. py:data:: FIXUP_OFF64

   64-bit offset


.. py:data:: FIXUP_OFF8S

   8-bit signed offset


.. py:data:: FIXUP_OFF16S

   16-bit signed offset


.. py:data:: FIXUP_OFF32S

   32-bit signed offset


.. py:data:: FIXUP_CUSTOM

   start of the custom types range


.. py:function:: is_fixup_custom(type: fixup_type_t) -> bool

   Is fixup processed by processor module?


.. py:data:: FIXUPF_REL

   fixup is relative to the linear address `base`. Otherwise fixup is relative to the start of the segment with `sel` selector. 
           


.. py:data:: FIXUPF_EXTDEF

   target is a location (otherwise - segment). Use this bit if the target is a symbol rather than an offset from the beginning of a segment. 
           


.. py:data:: FIXUPF_UNUSED

   fixup is ignored by IDA
   * disallows the kernel to convert operands
   * this fixup is not used during output 


           


.. py:data:: FIXUPF_CREATED

   fixup was not present in the input file


.. py:data:: FIXUPF_LOADER_MASK

   additional flags. The bits from this mask are not stored in the database and can be used by the loader at its discretion. 
           


.. py:class:: fixup_data_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: sel
      :type:  sel_t

      selector of the target segment. BADSEL means an absolute (zero based) target. 
              



   .. py:attribute:: off
      :type:  ida_idaapi.ea_t

      target offset 
              



   .. py:attribute:: displacement
      :type:  adiff_t

      displacement (offset from the target)



   .. py:method:: get_type() -> fixup_type_t

      Fixup type Types of fixups.



   .. py:method:: set_type(type_: fixup_type_t) -> None


   .. py:method:: set_type_and_flags(type_: fixup_type_t, flags_: int = 0) -> None


   .. py:method:: is_custom() -> bool

      is_fixup_custom()



   .. py:method:: get_flags() -> int

      Fixup flags Fixup flags.



   .. py:method:: is_extdef() -> bool


   .. py:method:: set_extdef() -> None


   .. py:method:: clr_extdef() -> None


   .. py:method:: is_unused() -> bool


   .. py:method:: set_unused() -> None


   .. py:method:: clr_unused() -> None


   .. py:method:: has_base() -> bool

      Is fixup relative?



   .. py:method:: was_created() -> bool

      Is fixup artificial?



   .. py:method:: get_base() -> ida_idaapi.ea_t

      Get base of fixup. 
              



   .. py:method:: set_base(new_base: ida_idaapi.ea_t) -> None

      Set base of fixup. The target should be set before a call of this function. 
              



   .. py:method:: set_sel(seg: segment_t const *) -> None


   .. py:method:: set_target_sel() -> None

      Set selector of fixup to the target. The target should be set before a call of this function. 
              



   .. py:method:: set(source: ida_idaapi.ea_t) -> None

      set_fixup()



   .. py:method:: get(source: ida_idaapi.ea_t) -> bool

      get_fixup()



   .. py:method:: get_handler() -> fixup_handler_t const *

      get_fixup_handler()



   .. py:method:: get_desc(source: ida_idaapi.ea_t) -> str

      get_fixup_desc()



   .. py:method:: calc_size() -> int

      calc_fixup_size()



   .. py:method:: get_value(ea: ida_idaapi.ea_t) -> int

      get_fixup_value()



   .. py:method:: patch_value(ea: ida_idaapi.ea_t) -> bool

      patch_fixup_value()



.. py:function:: get_fixup(fd: fixup_data_t, source: ida_idaapi.ea_t) -> bool

   Get fixup information.


.. py:function:: exists_fixup(source: ida_idaapi.ea_t) -> bool

   Check that a fixup exists at the given address.


.. py:function:: set_fixup(source: ida_idaapi.ea_t, fd: fixup_data_t) -> None

   Set fixup information. You should fill fixup_data_t and call this function and the kernel will remember information in the database. 
           
   :param source: the fixup source address, i.e. the address modified by the fixup
   :param fd: fixup data


.. py:function:: del_fixup(source: ida_idaapi.ea_t) -> None

   Delete fixup information.


.. py:function:: get_first_fixup_ea() -> ida_idaapi.ea_t

.. py:function:: get_next_fixup_ea(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

.. py:function:: get_prev_fixup_ea(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

.. py:function:: get_fixup_handler(type: fixup_type_t) -> fixup_handler_t const *

   Get handler of standard or custom fixup.


.. py:function:: get_fixup_value(ea: ida_idaapi.ea_t, type: fixup_type_t) -> int

   Get the operand value. This function get fixup bytes from data or an instruction at `ea` and convert them to the operand value (maybe partially). It is opposite in meaning to the `patch_fixup_value()`. For example, FIXUP_HI8 read a byte at `ea` and shifts it left by 8 bits, or AArch64's custom fixup BRANCH26 get low 26 bits of the insn at `ea` and shifts it left by 2 bits. This function is mainly used to get a relocation addend. 
           
   :param ea: address to get fixup bytes from, the size of the fixup bytes depends on the fixup type.
   :param type: fixup type
   :returns: operand: value


.. py:function:: patch_fixup_value(ea: ida_idaapi.ea_t, fd: fixup_data_t) -> bool

   Patch the fixup bytes. This function updates data or an instruction at `ea` to the fixup bytes. For example, FIXUP_HI8 updates a byte at `ea` to the high byte of `fd->off`, or AArch64's custom fixup BRANCH26 updates low 26 bits of the insn at `ea` to the value of `fd->off` shifted right by 2. 
           
   :param ea: address where data are changed, the size of the changed data depends on the fixup type.
   :param fd: fixup data
   :returns: false: the fixup bytes do not fit (e.g. `fd->off` is greater than 0xFFFFFFC for BRANCH26). The database is changed even in this case.


.. py:function:: get_fixup_desc(source: ida_idaapi.ea_t, fd: fixup_data_t) -> str

   Get FIXUP description comment.


.. py:function:: calc_fixup_size(type: fixup_type_t) -> int

   Calculate size of fixup in bytes (the number of bytes the fixup patches) 
           
   :returns: -1: means error


.. py:function:: find_custom_fixup(name: str) -> fixup_type_t

.. py:class:: fixup_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: fd
      :type:  fixup_data_t


.. py:function:: get_fixups(out: fixups_t *, ea: ida_idaapi.ea_t, size: asize_t) -> bool

.. py:function:: contains_fixups(ea: ida_idaapi.ea_t, size: asize_t) -> bool

   Does the specified address range contain any fixup information?


.. py:function:: gen_fix_fixups(_from: ida_idaapi.ea_t, to: ida_idaapi.ea_t, size: asize_t) -> None

   Relocate the bytes with fixup information once more (generic function). This function may be called from loader_t::move_segm() if it suits the goal. If loader_t::move_segm is not defined then this function will be called automatically when moving segments or rebasing the entire program. Special parameter values (from = BADADDR, size = 0, to = delta) are used when the function is called from rebase_program(delta). 
           


.. py:function:: handle_fixups_in_macro(ri: refinfo_t, ea: ida_idaapi.ea_t, other: fixup_type_t, macro_reft_and_flags: int) -> bool

   Handle two fixups in a macro. We often combine two instruction that load parts of a value into one macro instruction. For example: 
          ADRP  X0, #var@PAGE
              ADD   X0, X0, #var@PAGEOFF  --> ADRL X0, var
         lui   $v0, %hi(var)
              addiu $v0, $v0, %lo(var)    --> la   $v0, var


           
   :returns: success ('false' means that RI was not changed)



ida_offset
==========

.. py:module:: ida_offset

.. autoapi-nested-parse::

   Functions that deal with offsets.

   "Being an offset" is a characteristic of an operand. This means that operand or its part represent offset from some address in the program. This linear address is called "offset base". Some operands may have 2 offsets simultaneously. Generally, IDA doesn't handle this except for Motorola outer offsets. Thus there may be two offset values in an operand: simple offset and outer offset.
   Outer offsets are handled by specifying special operand number: it should be ORed with OPND_OUTER value.
   See bytes.hpp for further explanation of operand numbers. 
       



Functions
---------

.. autoapisummary::

   ida_offset.get_default_reftype
   ida_offset.op_offset_ex
   ida_offset.op_offset
   ida_offset.op_plain_offset
   ida_offset.get_offbase
   ida_offset.get_offset_expression
   ida_offset.get_offset_expr
   ida_offset.can_be_off32
   ida_offset.calc_offset_base
   ida_offset.calc_probable_base_by_value
   ida_offset.calc_reference_data
   ida_offset.add_refinfo_dref
   ida_offset.calc_target
   ida_offset.calc_basevalue


Module Contents
---------------

.. py:function:: get_default_reftype(ea: ida_idaapi.ea_t) -> reftype_t

   Get default reference type depending on the segment. 
           
   :returns: one of REF_OFF8, REF_OFF16, REF_OFF32, REF_OFF64


.. py:function:: op_offset_ex(ea: ida_idaapi.ea_t, n: int, ri: refinfo_t) -> bool

   Convert operand to a reference. To delete an offset, use clr_op_type() function. 
           
   :param ea: linear address. if 'ea' has unexplored bytes, try to convert them to
   * no segment: fail
   * 16bit segment: to 16bit word data
   * 32bit segment: to dword
   :param n: operand number (may be ORed with OPND_OUTER)
   * 0: first
   * 1: second
   * ...
   * 7: eighth operand


   * OPND_MASK: all operands
   :param ri: reference information
   :returns: success


.. py:function:: op_offset(*args) -> bool

   See op_offset_ex()


.. py:function:: op_plain_offset(ea: ida_idaapi.ea_t, n: int, base: ida_idaapi.ea_t) -> bool

   Convert operand to a reference with the default reference type.


.. py:function:: get_offbase(ea: ida_idaapi.ea_t, n: int) -> ida_idaapi.ea_t

   Get offset base value 
           
   :param ea: linear address
   :param n: 0..UA_MAXOP-1 operand number
   :returns: offset base or BADADDR


.. py:function:: get_offset_expression(ea: ida_idaapi.ea_t, n: int, _from: ida_idaapi.ea_t, offset: adiff_t, getn_flags: int = 0) -> str

   Get offset expression (in the form "offset name+displ"). This function uses offset translation function ( processor_t::translate) if your IDP module has such a function. Translation function is used to map linear addresses in the program (only for offsets).
   Example: suppose we have instruction at linear address 0x00011000: `mov     ax, [bx+7422h] ` and at ds:7422h: `array   dw      ... ` We want to represent the second operand with an offset expression, so then we call: `get_offset_expresion(0x001100, 1, 0x001102, 0x7422, buf);
                        |         |  |         |       |
                        |         |  |         |       +output buffer
                        |         |  |         +value of offset expression
                        |         |  +address offset value in the instruction
                        |         +the second operand
                        +address of instruction` and the function will return a colored string: `offset array ` 
           
   :param ea: start of instruction or data with the offset expression
   :param n: operand number (may be ORed with OPND_OUTER)
   * 0: first operand
   * 1: second operand
   * ...
   * 7: eighth operand
   :param offset: value of operand or its part. The function will return text representation of this value as offset expression.
   :param getn_flags: combination of:
   * GETN_APPZERO: meaningful only if the name refers to a structure. appends the struct field name if the field offset is zero
   * GETN_NODUMMY: do not generate dummy names for the expression but pretend they already exist (useful to verify that the offset expression can be represented)
   :returns: 0: can't convert to offset expression
   :returns: 1: ok, a simple offset expression
   :returns: 2: ok, a complex offset expression


.. py:function:: get_offset_expr(ea: ida_idaapi.ea_t, n: int, ri: refinfo_t, _from: ida_idaapi.ea_t, offset: adiff_t, getn_flags: int = 0) -> str

   See get_offset_expression()


.. py:function:: can_be_off32(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Does the specified address contain a valid OFF32 value?. For symbols in special segments the displacement is not taken into account. If yes, then the target address of OFF32 will be returned. If not, then BADADDR is returned. 
           


.. py:function:: calc_offset_base(ea: ida_idaapi.ea_t, n: int) -> ida_idaapi.ea_t

   Try to calculate the offset base This function takes into account the fixup information, current ds and cs values. 
           
   :param ea: the referencing instruction/data address
   :param n: operand number
   * 0: first operand
   * 1: second operand
   * ...
   * 7: eighth operand
   :returns: output base address or BADADDR


.. py:function:: calc_probable_base_by_value(ea: ida_idaapi.ea_t, off: int) -> ida_idaapi.ea_t

   Try to calculate the offset base. 2 bases are checked: current ds and cs. If fails, return BADADDR 
           


.. py:function:: calc_reference_data(target: ea_t *, base: ea_t *, _from: ida_idaapi.ea_t, ri: refinfo_t, opval: adiff_t) -> bool

   Calculate the target and base addresses of an offset expression. The calculated target and base addresses are returned in the locations pointed by 'base' and 'target'. In case 'ri.base' is BADADDR, the function calculates the offset base address from the referencing instruction/data address. The target address is copied from ri.target. If ri.target is BADADDR then the target is calculated using the base address and 'opval'. This function also checks if 'opval' matches the full value of the reference and takes in account the memory-mapping. 
           
   :param target: output target address
   :param base: output base address
   :param ri: reference info block from the database
   :param opval: operand value (usually op_t::value or op_t::addr)
   :returns: success


.. py:function:: add_refinfo_dref(insn: insn_t const &, _from: ida_idaapi.ea_t, ri: refinfo_t, opval: adiff_t, type: dref_t, opoff: int) -> ida_idaapi.ea_t

   Add xrefs for a reference from the given instruction ( insn_t::ea). This function creates a cross references to the target and the base. insn_t::add_off_drefs() calls this function to create xrefs for 'offset' operand. 
           
   :param insn: the referencing instruction
   :param ri: reference info block from the database
   :param opval: operand value (usually op_t::value or op_t::addr)
   :param type: type of xref
   :param opoff: offset of the operand from the start of instruction
   :returns: the target address of the reference


.. py:function:: calc_target(*args) -> ida_idaapi.ea_t

   This function has the following signatures:

       0. calc_target(from: ida_idaapi.ea_t, opval: adiff_t, ri: const refinfo_t &) -> ida_idaapi.ea_t
       1. calc_target(from: ida_idaapi.ea_t, ea: ida_idaapi.ea_t, n: int, opval: adiff_t) -> ida_idaapi.ea_t

   # 0: calc_target(from: ida_idaapi.ea_t, opval: adiff_t, ri: const refinfo_t &) -> ida_idaapi.ea_t

   Calculate the target using the provided refinfo_t.


   # 1: calc_target(from: ida_idaapi.ea_t, ea: ida_idaapi.ea_t, n: int, opval: adiff_t) -> ida_idaapi.ea_t

   Retrieve refinfo_t structure and calculate the target.


.. py:function:: calc_basevalue(target: ida_idaapi.ea_t, base: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Calculate the value of the reference base.



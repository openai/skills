ida_segregs
===========

.. py:module:: ida_segregs

.. autoapi-nested-parse::

   Functions that deal with the segment registers.

   If your processor doesn't use segment registers, then these functions are of no use for you. However, you should define two virtual segment registers - CS and DS (for code segment and data segment) and specify their internal numbers in the LPH structure (processor_t::reg_code_sreg and processor_t::reg_data_sreg). 
       



Attributes
----------

.. autoapisummary::

   ida_segregs.R_es
   ida_segregs.R_cs
   ida_segregs.R_ss
   ida_segregs.R_ds
   ida_segregs.R_fs
   ida_segregs.R_gs
   ida_segregs.SR_inherit
   ida_segregs.SR_user
   ida_segregs.SR_auto
   ida_segregs.SR_autostart


Classes
-------

.. autoapisummary::

   ida_segregs.sreg_range_t


Functions
---------

.. autoapisummary::

   ida_segregs.get_sreg
   ida_segregs.split_sreg_range
   ida_segregs.set_default_sreg_value
   ida_segregs.set_sreg_at_next_code
   ida_segregs.get_sreg_range
   ida_segregs.get_prev_sreg_range
   ida_segregs.set_default_dataseg
   ida_segregs.get_sreg_ranges_qty
   ida_segregs.getn_sreg_range
   ida_segregs.get_sreg_range_num
   ida_segregs.del_sreg_range
   ida_segregs.copy_sreg_ranges


Module Contents
---------------

.. py:data:: R_es

.. py:data:: R_cs

.. py:data:: R_ss

.. py:data:: R_ds

.. py:data:: R_fs

.. py:data:: R_gs

.. py:class:: sreg_range_t

   Bases: :py:obj:`ida_range.range_t`


   .. py:attribute:: thisown


   .. py:attribute:: val
      :type:  sel_t

      segment register value



   .. py:attribute:: tag
      :type:  uchar

      Segment register range tags



.. py:data:: SR_inherit

   the value is inherited from the previous range


.. py:data:: SR_user

   the value is specified by the user


.. py:data:: SR_auto

   the value is determined by IDA


.. py:data:: SR_autostart

   used as SR_auto for segment starting address


.. py:function:: get_sreg(ea: ida_idaapi.ea_t, rg: int) -> sel_t

   Get value of a segment register. This function uses segment register range and default segment register values stored in the segment structure. 
           
   :param ea: linear address in the program
   :param rg: number of the segment register
   :returns: value of the segment register, BADSEL if value is unknown or rg is not a segment register.


.. py:function:: split_sreg_range(ea: ida_idaapi.ea_t, rg: int, v: sel_t, tag: uchar, silent: bool = False) -> bool

   Create a new segment register range. This function is used when the IDP emulator detects that a segment register changes its value. 
           
   :param ea: linear address where the segment register will have a new value. if ea==BADADDR, nothing to do.
   :param rg: the number of the segment register
   :param v: the new value of the segment register. If the value is unknown, you should specify BADSEL.
   :param tag: the register info tag. see Segment register range tags
   :param silent: if false, display a warning() in the case of failure
   :returns: success


.. py:function:: set_default_sreg_value(sg: segment_t *, rg: int, value: sel_t) -> bool

   Set default value of a segment register for a segment. 
           
   :param sg: pointer to segment structure if nullptr, then set the register for all segments
   :param rg: number of segment register
   :param value: its default value. this value will be used by get_sreg() if value of the register is unknown at the specified address.
   :returns: success


.. py:function:: set_sreg_at_next_code(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, rg: int, value: sel_t) -> None

   Set the segment register value at the next instruction. This function is designed to be called from idb_event::sgr_changed handler in order to contain the effect of changing a segment register value only until the next instruction.
   It is useful, for example, in the ARM module: the modification of the T register does not affect existing instructions later in the code. 
           
   :param ea1: address to start to search for an instruction
   :param ea2: the maximal address
   :param rg: the segment register number
   :param value: the segment register value


.. py:function:: get_sreg_range(out: sreg_range_t, ea: ida_idaapi.ea_t, rg: int) -> bool

   Get segment register range by linear address. 
           
   :param out: segment register range
   :param ea: any linear address in the program
   :param rg: the segment register number
   :returns: success


.. py:function:: get_prev_sreg_range(out: sreg_range_t, ea: ida_idaapi.ea_t, rg: int) -> bool

   Get segment register range previous to one with address. 
           
   :param out: segment register range
   :param ea: any linear address in the program
   :param rg: the segment register number
   :returns: success


.. py:function:: set_default_dataseg(ds_sel: sel_t) -> None

   Set default value of DS register for all segments.


.. py:function:: get_sreg_ranges_qty(rg: int) -> size_t

   Get number of segment register ranges. 
           
   :param rg: the segment register number


.. py:function:: getn_sreg_range(out: sreg_range_t, rg: int, n: int) -> bool

   Get segment register range by its number. 
           
   :param out: segment register range
   :param rg: the segment register number
   :param n: number of range (0..qty()-1)
   :returns: success


.. py:function:: get_sreg_range_num(ea: ida_idaapi.ea_t, rg: int) -> int

   Get number of segment register range by address. 
           
   :param ea: any address in the range
   :param rg: the segment register number
   :returns: -1 if no range occupies the specified address. otherwise returns number of the specified range (0..get_srranges_qty()-1)


.. py:function:: del_sreg_range(ea: ida_idaapi.ea_t, rg: int) -> bool

   Delete segment register range started at ea. When a segment register range is deleted, the previous range is extended to cover the empty space. The segment register range at the beginning of a segment cannot be deleted. 
           
   :param ea: start_ea of the deleted range
   :param rg: the segment register number
   :returns: success


.. py:function:: copy_sreg_ranges(dst_rg: int, src_rg: int, map_selector: bool = False) -> None

   Duplicate segment register ranges. 
           
   :param dst_rg: number of destination segment register
   :param src_rg: copy ranges from
   :param map_selector: map selectors to linear addresses using sel2ea()



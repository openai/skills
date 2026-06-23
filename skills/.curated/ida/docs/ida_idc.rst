ida_idc
=======

.. py:module:: ida_idc


Functions
---------

.. autoapisummary::

   ida_idc.mark_position
   ida_idc.get_marked_pos
   ida_idc.get_mark_comment


Module Contents
---------------

.. py:function:: mark_position(ea: ida_idaapi.ea_t, lnnum: int, x: short, y: short, slot: int, comment: str) -> None

.. py:function:: get_marked_pos(slot: int) -> ida_idaapi.ea_t

.. py:function:: get_mark_comment(slot: int) -> PyObject *


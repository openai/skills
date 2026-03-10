ida_entry
=========

.. py:module:: ida_entry

.. autoapi-nested-parse::

   Functions that deal with entry points.

   Exported functions are considered as entry points as well.
   IDA maintains list of entry points to the program. Each entry point:
      * has an address
      * has a name
      * may have an ordinal number 

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For entry point management, see :mod:`ida_domain.entries`.



Attributes
----------

.. autoapisummary::

   ida_entry.AEF_UTF8
   ida_entry.AEF_IDBENC
   ida_entry.AEF_NODUMMY
   ida_entry.AEF_WEAK
   ida_entry.AEF_NOFORCE


Functions
---------

.. autoapisummary::

   ida_entry.get_entry_qty
   ida_entry.add_entry
   ida_entry.get_entry_ordinal
   ida_entry.get_entry
   ida_entry.get_entry_name
   ida_entry.rename_entry
   ida_entry.set_entry_forwarder
   ida_entry.get_entry_forwarder


Module Contents
---------------

.. py:function:: get_entry_qty() -> size_t

   Get number of entry points.


.. py:data:: AEF_UTF8

   the name is given in UTF-8 (default)


.. py:data:: AEF_IDBENC

   the name is given in the IDB encoding; non-ASCII bytes will be decoded accordingly. Specifying AEF_IDBENC also implies AEF_NODUMMY 
           


.. py:data:: AEF_NODUMMY

   automatically prepend the name with '_' if it begins with a dummy suffix. See also AEF_IDBENC 
           


.. py:data:: AEF_WEAK

   make name weak


.. py:data:: AEF_NOFORCE

   if the specified address already has a name, the new name will be appended to the regular comment, except for the case when the old name is weak and the new one is not. 
           


.. py:function:: add_entry(ord: int, ea: ida_idaapi.ea_t, name: str, makecode: bool, flags: int = 0) -> bool

   Add an entry point to the list of entry points. 
           
   :param ord: ordinal number if ordinal number is equal to 'ea' then ordinal is not used
   :param ea: linear address
   :param name: name of entry point. If the specified location already has a name, the old name will be appended to the regular comment.
   :param makecode: should the kernel convert bytes at the entry point to instruction(s)
   :param flags: See AEF_*
   :returns: success (currently always true)


.. py:function:: get_entry_ordinal(idx: size_t) -> int

   Get ordinal number of an entry point. 
           
   :param idx: internal number of entry point. Should be in the range 0..get_entry_qty()-1
   :returns: ordinal number or 0.


.. py:function:: get_entry(ord: int) -> ida_idaapi.ea_t

   Get entry point address by its ordinal 
           
   :param ord: ordinal number of entry point
   :returns: address or BADADDR


.. py:function:: get_entry_name(ord: int) -> str

   Get name of the entry point by its ordinal. 
           
   :param ord: ordinal number of entry point
   :returns: size of entry name or -1


.. py:function:: rename_entry(ord: int, name: str, flags: int = 0) -> bool

   Rename entry point. 
           
   :param ord: ordinal number of the entry point
   :param name: name of entry point. If the specified location already has a name, the old name will be appended to a repeatable comment.
   :param flags: See AEF_*
   :returns: success


.. py:function:: set_entry_forwarder(ord: int, name: str, flags: int = 0) -> bool

   Set forwarder name for ordinal. 
           
   :param ord: ordinal number of the entry point
   :param name: forwarder name for entry point.
   :param flags: See AEF_*
   :returns: success


.. py:function:: get_entry_forwarder(ord: int) -> str

   Get forwarder name for the entry point by its ordinal. 
           
   :param ord: ordinal number of entry point
   :returns: size of entry forwarder name or -1



ida_strlist
===========

.. py:module:: ida_strlist

.. autoapi-nested-parse::

   Functions that deal with the string list.

   While the kernel keeps the string list, it does not update it. The string list is not used by the kernel because keeping it up-to-date would slow down IDA without any benefit. If the string list is not cleared using clear_strlist(), the list will be saved to the database and restored on the next startup.
   The users of this list should call build_strlist() if they need an up-to-date version. 
       



Classes
-------

.. autoapisummary::

   ida_strlist.strwinsetup_t
   ida_strlist.string_info_t


Functions
---------

.. autoapisummary::

   ida_strlist.get_strlist_options
   ida_strlist.build_strlist
   ida_strlist.clear_strlist
   ida_strlist.get_strlist_qty
   ida_strlist.get_strlist_item


Module Contents
---------------

.. py:class:: strwinsetup_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: minlen
      :type:  int


   .. py:attribute:: display_only_existing_strings
      :type:  uchar


   .. py:attribute:: only_7bit
      :type:  uchar


   .. py:attribute:: ignore_heads
      :type:  uchar


   .. py:attribute:: strtypes


.. py:class:: string_info_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: length
      :type:  int


   .. py:attribute:: type
      :type:  int


.. py:function:: get_strlist_options() -> strwinsetup_t const *

   Get the static string list options.


.. py:function:: build_strlist() -> None

   Rebuild the string list.


.. py:function:: clear_strlist() -> None

   Clear the string list.


.. py:function:: get_strlist_qty() -> size_t

   Get number of elements in the string list. The list will be loaded from the database (if saved) or built from scratch. 
           


.. py:function:: get_strlist_item(si: string_info_t, n: size_t) -> bool

   Get nth element of the string list (n=0..get_strlist_qty()-1)



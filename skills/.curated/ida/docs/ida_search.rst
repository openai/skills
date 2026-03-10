ida_search
==========

.. py:module:: ida_search

.. autoapi-nested-parse::

   Middle-level search functions.

   They all are controlled by Search flags 
       



Attributes
----------

.. autoapisummary::

   ida_search.SEARCH_UP
   ida_search.SEARCH_DOWN
   ida_search.SEARCH_NEXT
   ida_search.SEARCH_CASE
   ida_search.SEARCH_REGEX
   ida_search.SEARCH_NOBRK
   ida_search.SEARCH_NOSHOW
   ida_search.SEARCH_IDENT
   ida_search.SEARCH_BRK
   ida_search.SEARCH_USE
   ida_search.SEARCH_DEF
   ida_search.SEARCH_USESEL


Functions
---------

.. autoapisummary::

   ida_search.search_down
   ida_search.find_error
   ida_search.find_notype
   ida_search.find_unknown
   ida_search.find_defined
   ida_search.find_suspop
   ida_search.find_data
   ida_search.find_code
   ida_search.find_not_func
   ida_search.find_imm
   ida_search.find_text
   ida_search.find_reg_access


Module Contents
---------------

.. py:data:: SEARCH_UP

   search towards lower addresses


.. py:data:: SEARCH_DOWN

   search towards higher addresses


.. py:data:: SEARCH_NEXT

   skip the starting address when searching. this bit is useful only for search(), bin_search(), find_reg_access(). find_.. functions skip the starting address automatically. 
           


.. py:data:: SEARCH_CASE

   case-sensitive search (case-insensitive otherwise)


.. py:data:: SEARCH_REGEX

   regular expressions in search string (supported only for the text search)


.. py:data:: SEARCH_NOBRK

   do not test if the user clicked cancel to interrupt the search


.. py:data:: SEARCH_NOSHOW

   do not display the search progress/refresh screen


.. py:data:: SEARCH_IDENT

   search for an identifier (text search). it means that the characters before and after the match cannot be is_visible_char(). 
           


.. py:data:: SEARCH_BRK

   return BADADDR if the search was cancelled.


.. py:data:: SEARCH_USE

   find_reg_access: search for a use (read access)


.. py:data:: SEARCH_DEF

   find_reg_access: search for a definition (write access)


.. py:data:: SEARCH_USESEL

   query the UI for a possible current selection to limit the search to 
           


.. py:function:: search_down(sflag: int) -> bool

   Is the SEARCH_DOWN bit set?


.. py:function:: find_error(ea: ida_idaapi.ea_t, sflag: int) -> int *

.. py:function:: find_notype(ea: ida_idaapi.ea_t, sflag: int) -> int *

.. py:function:: find_unknown(ea: ida_idaapi.ea_t, sflag: int) -> ida_idaapi.ea_t

.. py:function:: find_defined(ea: ida_idaapi.ea_t, sflag: int) -> ida_idaapi.ea_t

.. py:function:: find_suspop(ea: ida_idaapi.ea_t, sflag: int) -> int *

.. py:function:: find_data(ea: ida_idaapi.ea_t, sflag: int) -> ida_idaapi.ea_t

.. py:function:: find_code(ea: ida_idaapi.ea_t, sflag: int) -> ida_idaapi.ea_t

.. py:function:: find_not_func(ea: ida_idaapi.ea_t, sflag: int) -> ida_idaapi.ea_t

.. py:function:: find_imm(ea: ida_idaapi.ea_t, sflag: int, search_value: int) -> int *

.. py:function:: find_text(start_ea: ida_idaapi.ea_t, y: int, x: int, ustr: str, sflag: int) -> ida_idaapi.ea_t

.. py:function:: find_reg_access(out: reg_access_t, start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t, regname: str, sflag: int) -> ida_idaapi.ea_t


idautils
========

.. py:module:: idautils

.. autoapi-nested-parse::

   idautils.py - High level utility functions for IDA



Attributes
----------

.. autoapisummary::

   idautils.GetInputFileMD5
   idautils.cpu
   idautils.procregs


Classes
-------

.. autoapisummary::

   idautils.Strings
   idautils.peutils_t


Functions
---------

.. autoapisummary::

   idautils.CodeRefsTo
   idautils.CodeRefsFrom
   idautils.DataRefsTo
   idautils.DataRefsFrom
   idautils.XrefTypeName
   idautils.XrefsFrom
   idautils.XrefsTo
   idautils.Threads
   idautils.Heads
   idautils.Functions
   idautils.Chunks
   idautils.Modules
   idautils.Names
   idautils.Segments
   idautils.Entries
   idautils.FuncItems
   idautils.Structs
   idautils.StructMembers
   idautils.DecodePrecedingInstruction
   idautils.DecodePreviousInstruction
   idautils.DecodeInstruction
   idautils.GetDataList
   idautils.PutDataList
   idautils.MapDataList
   idautils.GetIdbDir
   idautils.GetRegisterList
   idautils.GetInstructionList
   idautils.Assemble
   idautils.ProcessUiActions


Module Contents
---------------

.. py:function:: CodeRefsTo(ea, flow: bool)

   Get a list of code references to 'ea'

   :param ea:   Target address
   :param flow: Follow normal code flow or not

   :returns: list of references (may be empty list)

   Example::

       for ref in CodeRefsTo(get_screen_ea(), 1):
           print(ref)


.. py:function:: CodeRefsFrom(ea, flow: bool)

   Get a list of code references from 'ea'

   :param ea:   Target address
   :param flow: Follow normal code flow or not

   :returns: list of references (may be empty list)

   Example::

       for ref in CodeRefsFrom(get_screen_ea(), 1):
           print(ref)


.. py:function:: DataRefsTo(ea)

   Get a list of data references to 'ea'

   :param ea:   Target address

   :returns: list of references (may be empty list)

   Example::

       for ref in DataRefsTo(get_screen_ea()):
           print(ref)


.. py:function:: DataRefsFrom(ea)

   Get a list of data references from 'ea'

   :param ea:   Target address

   :returns: list of references (may be empty list)

   Example::

       for ref in DataRefsFrom(get_screen_ea()):
           print(ref)


.. py:function:: XrefTypeName(typecode)

   Convert cross-reference type codes to readable names

   :param typecode: cross-reference type code


.. py:function:: XrefsFrom(ea, flags=0)

   Return all references from address 'ea'

   :param ea: Reference address
   :param flags: one of ida_xref.XREF_ALL (default), ida_xref.XREF_FAR, ida_xref.XREF_DATA

   Example::
          for xref in XrefsFrom(here(), 0):
              print(xref.type, XrefTypeName(xref.type),                          'from', hex(xref.frm), 'to', hex(xref.to))


.. py:function:: XrefsTo(ea, flags=0)

   Return all references to address 'ea'

   :param ea: Reference address
   :param flags: one of ida_xref.XREF_ALL (default), ida_xref.XREF_FAR, ida_xref.XREF_DATA

   Example::
          for xref in XrefsTo(here(), 0):
              print(xref.type, XrefTypeName(xref.type),                          'from', hex(xref.frm), 'to', hex(xref.to))


.. py:function:: Threads()

   Returns all thread IDs for the current debugee


.. py:function:: Heads(start=None, end=None)

   Get a list of heads (instructions or data items)

   :param start: start address (default: inf.min_ea)
   :param end:   end address (default: inf.max_ea)

   :returns: list of heads between start and end


.. py:function:: Functions(start=None, end=None)

   Get a list of functions

   :param start: start address (default: inf.min_ea)
   :param end:   end address (default: inf.max_ea)

   :returns: list of function entrypoints between start and end

   NOTE: The last function that starts before 'end' is included even
   if it extends beyond 'end'. Any function that has its chunks scattered
   in multiple segments will be reported multiple times, once in each segment
   as they are listed.


.. py:function:: Chunks(start)

   Get a list of function chunks
   See also ida_funcs.func_tail_iterator_t

   :param start: address of the function

   :returns: list of function chunks (tuples of the form (start_ea, end_ea))
            belonging to the function


.. py:function:: Modules()

   Returns a list of module objects with name,size,base and the rebase_to attributes


.. py:function:: Names()

   Returns a list of names

   :returns: List of tuples (ea, name)


.. py:function:: Segments()

   Get list of segments (sections) in the binary image

   :returns: List of segment start addresses.


.. py:function:: Entries()

   Returns a list of entry points (exports)

   :returns: List of tuples (index, ordinal, ea, name)


.. py:function:: FuncItems(start)

   Get a list of function items (instruction or data items inside function boundaries)
   See also ida_funcs.func_item_iterator_t

   :param start: address of the function

   :returns: ea of each item in the function


.. py:function:: Structs()

   Get a list of structures

   :returns: List of tuples (ordinal, sid, name)


.. py:function:: StructMembers(sid)

   Get a list of structure members information (or stack vars if given a frame).

   :param sid: ID of the structure.

   :returns: List of tuples (offset_in_bytes, name, size_in_bytes)

   NOTE: If 'sid' does not refer to a valid structure, an exception will be raised.
   NOTE: This will not return 'holes' in structures/stack frames; it only returns defined structure members.


.. py:function:: DecodePrecedingInstruction(ea)

   Decode preceding instruction in the execution flow.

   :param ea: address to decode
   :returns: (None or the decode instruction, farref)
            farref will contain 'true' if followed an xref, false otherwise


.. py:function:: DecodePreviousInstruction(ea)

   Decodes the previous instruction and returns an insn_t like class

   :param ea: address to decode
   :returns: None or a new insn_t instance


.. py:function:: DecodeInstruction(ea)

   Decodes an instruction and returns an insn_t like class

   :param ea: address to decode
   :returns: None or a new insn_t instance


.. py:function:: GetDataList(ea, count, itemsize=1)

   Get data list - INTERNAL USE ONLY


.. py:function:: PutDataList(ea, datalist, itemsize=1)

   Put data list - INTERNAL USE ONLY


.. py:function:: MapDataList(ea, length, func, wordsize=1)

   Map through a list of data words in the database

   :param ea:       start address
   :param length:   number of words to map
   :param func:     mapping function
   :param wordsize: size of words to map [default: 1 byte]

   :returns: None


.. py:data:: GetInputFileMD5

.. py:class:: Strings(default_setup=False)

   Bases: :py:obj:`object`


   Allows iterating over the string list. The set of strings will not be
   modified, unless asked explicitly at setup()-time. This string list also
   is used by the "String window" so it may be changed when this window is
   updated.

   Example:
       s = Strings()

       for i in s:
           print("%x: len=%d type=%d -> '%s'" % (i.ea, i.length, i.strtype, str(i)))



   .. py:class:: StringItem(si)

      Bases: :py:obj:`object`


      Class representing each string item.


      .. py:attribute:: ea

         String ea



      .. py:attribute:: strtype

         string type (STRTYPE_xxxxx)



      .. py:attribute:: length

         string length



      .. py:method:: is_1_byte_encoding()



   .. py:method:: clear_cache()

      Clears the string list cache



   .. py:attribute:: size
      :value: 0



   .. py:method:: refresh()

      Refreshes the string list



   .. py:method:: setup(strtypes=[ida_nalt.STRTYPE_C], minlen=5, only_7bit=True, ignore_instructions=False, display_only_existing_strings=False)


.. py:function:: GetIdbDir()

   Get IDB directory

   This function returns directory path of the current IDB database


.. py:function:: GetRegisterList()

   Returns the register list


.. py:function:: GetInstructionList()

   Returns the instruction list of the current processor module


.. py:function:: Assemble(ea, line)

   Assembles one or more lines (does not display an message dialogs)
   If line is a list then this function will attempt to assemble all the lines
   This function will turn on batch mode temporarily so that no messages are displayed on the screen

   :param ea:       start address
   :returns: (False, "Error message") or (True, asm_buf) or (True, [asm_buf1, asm_buf2, asm_buf3])


.. py:function:: ProcessUiActions(actions, flags=0)

   :param actions: A string containing a list of actions separated by semicolon, a list or a tuple
   :param flags: flags to be passed to process_ui_action()
   :returns: Boolean. Returns False if the action list was empty or execute_ui_requests() failed.


.. py:class:: peutils_t

   Bases: :py:obj:`object`


   PE utility class. Retrieves PE information from the database.

   Constants from pe.h


   .. py:attribute:: PE_NODE
      :value: '$ PE header'



   .. py:attribute:: PE_ALT_DBG_FPOS


   .. py:attribute:: PE_ALT_IMAGEBASE


   .. py:attribute:: PE_ALT_PEHDR_OFF


   .. py:attribute:: PE_ALT_NEFLAGS


   .. py:attribute:: PE_ALT_TDS_LOADED


   .. py:attribute:: PE_ALT_PSXDLL


   .. py:attribute:: imagebase

      Loading address (usually pe.imagebase)



   .. py:attribute:: header_offset

      Offset of PE header



   .. py:attribute:: header

      Returns the complete PE header as an instance of peheader_t (defined in the SDK).



.. py:data:: cpu

   This is a special class instance used to access the registers as if they were attributes of this object.
   For example to access the EAX register:
       print("%x" % cpu.Eax)


.. py:data:: procregs

   This object is used to access the processor registers. It is useful when decoding instructions and you want to see which instruction is which.
   For example:
       x = idautils.DecodeInstruction(here())
       if x[0] == procregs.Esp:
           print("This operand is the register ESP)



ida_problems
============

.. py:module:: ida_problems

.. autoapi-nested-parse::

   Functions that deal with the list of problems.

   There are several problem lists. An address may be inserted to any list. The kernel simply maintains these lists, no additional processing is done.
   The problem lists are accessible for the user from the View->Subviews->Problems menu item.
   Addresses in the lists are kept sorted. In general IDA just maintains these lists without using them during analysis (except PR_ROLLED). 
       



Attributes
----------

.. autoapisummary::

   ida_problems.cvar
   ida_problems.PR_NOBASE
   ida_problems.PR_NONAME
   ida_problems.PR_NOFOP
   ida_problems.PR_NOCMT
   ida_problems.PR_NOXREFS
   ida_problems.PR_JUMP
   ida_problems.PR_DISASM
   ida_problems.PR_HEAD
   ida_problems.PR_ILLADDR
   ida_problems.PR_MANYLINES
   ida_problems.PR_BADSTACK
   ida_problems.PR_ATTN
   ida_problems.PR_FINAL
   ida_problems.PR_ROLLED
   ida_problems.PR_COLLISION
   ida_problems.PR_DECIMP
   ida_problems.PR_END


Functions
---------

.. autoapisummary::

   ida_problems.get_problem_desc
   ida_problems.remember_problem
   ida_problems.get_problem
   ida_problems.forget_problem
   ida_problems.get_problem_name
   ida_problems.is_problem_present
   ida_problems.was_ida_decision


Module Contents
---------------

.. py:function:: get_problem_desc(t: problist_id_t, ea: ida_idaapi.ea_t) -> str

   Get the human-friendly description of the problem, if one was provided to remember_problem. 
           
   :param t: problem list type.
   :param ea: linear address.
   :returns: the message length or -1 if none


.. py:function:: remember_problem(type: problist_id_t, ea: ida_idaapi.ea_t, msg: str = None) -> None

   Insert an address to a list of problems. Display a message saying about the problem (except of PR_ATTN,PR_FINAL) PR_JUMP is temporarily ignored. 
           
   :param type: problem list type
   :param ea: linear address
   :param msg: a user-friendly message to be displayed instead of the default more generic one associated with the type of problem. Defaults to nullptr.


.. py:function:: get_problem(type: problist_id_t, lowea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get an address from the specified problem list. The address is not removed from the list. 
           
   :param type: problem list type
   :param lowea: the returned address will be higher or equal than the specified address
   :returns: linear address or BADADDR


.. py:function:: forget_problem(type: problist_id_t, ea: ida_idaapi.ea_t) -> bool

   Remove an address from a problem list 
           
   :param type: problem list type
   :param ea: linear address
   :returns: success


.. py:function:: get_problem_name(type: problist_id_t, longname: bool = True) -> str

   Get problem list description.


.. py:function:: is_problem_present(t: problist_id_t, ea: ida_idaapi.ea_t) -> bool

   Check if the specified address is present in the problem list.


.. py:function:: was_ida_decision(ea: ida_idaapi.ea_t) -> bool

.. py:data:: cvar

.. py:data:: PR_NOBASE

   Can't find offset base.


.. py:data:: PR_NONAME

   Can't find name.


.. py:data:: PR_NOFOP

   Can't find forced op (not used anymore)


.. py:data:: PR_NOCMT

   Can't find comment (not used anymore)


.. py:data:: PR_NOXREFS

   Can't find references.


.. py:data:: PR_JUMP

   Jump by table !!!! ignored.


.. py:data:: PR_DISASM

   Can't disasm.


.. py:data:: PR_HEAD

   Already head.


.. py:data:: PR_ILLADDR

   Exec flows beyond limits.


.. py:data:: PR_MANYLINES

   Too many lines.


.. py:data:: PR_BADSTACK

   Failed to trace the value of the stack pointer.


.. py:data:: PR_ATTN

   Attention! Probably erroneous situation.


.. py:data:: PR_FINAL

   Decision to convert to instruction/data is made by IDA.


.. py:data:: PR_ROLLED

   The decision made by IDA was wrong and rolled back.


.. py:data:: PR_COLLISION

   FLAIR collision: the function with the given name already exists.


.. py:data:: PR_DECIMP

   FLAIR match indecision: the patterns matched, but not the function(s) being referenced.


.. py:data:: PR_END

   Number of problem types.



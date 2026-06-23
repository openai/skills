ida_undo
========

.. py:module:: ida_undo


Functions
---------

.. autoapisummary::

   ida_undo.create_undo_point
   ida_undo.get_undo_action_label
   ida_undo.get_redo_action_label
   ida_undo.perform_undo
   ida_undo.perform_redo


Module Contents
---------------

.. py:function:: create_undo_point(*args) -> bool

   Create a new restore point. The user can undo to this point in the future. 
           
   :param bytes: body of the record for UNDO_ACTION_START
   :param size: size of the record for UNDO_ACTION_START
   :returns: success; fails if undo is disabled


.. py:function:: get_undo_action_label() -> str

   Get the label of the action that will be undone. This function returns the text that can be displayed in the undo menu 
           
   :returns: success


.. py:function:: get_redo_action_label() -> str

   Get the label of the action that will be redone. This function returns the text that can be displayed in the redo menu 
           
   :returns: success


.. py:function:: perform_undo() -> bool

   Perform undo. 
           
   :returns: success


.. py:function:: perform_redo() -> bool

   Perform redo. 
           
   :returns: success



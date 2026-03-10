init
====

.. py:module:: init


Attributes
----------

.. autoapisummary::

   init.base
   init.IDAPYTHON_DYNLOAD_BASE
   init.lib_dynload
   init.all_mods
   init.help
   init.idausr_python_list
   init.userrc


Classes
-------

.. autoapisummary::

   init.IDAPythonStdOut
   init.IDAPythonHelpPrompter
   init.IDAPythonHelp


Functions
---------

.. autoapisummary::

   init.runscript
   init.print_banner


Module Contents
---------------

.. py:data:: base
   :value: '/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13'


.. py:data:: IDAPYTHON_DYNLOAD_BASE
   :value: b'.'


.. py:data:: lib_dynload

.. py:data:: all_mods
   :value: 'idaapi,hexrays,allins,auto,bitrange,bytes,dbg,diskio,dirtree,entry,expr,fixup,fpro,frame,funcs,g...


.. py:class:: IDAPythonStdOut

   Dummy file-like class that receives stdout and stderr


   .. py:attribute:: encoding
      :value: 'UTF-8'



   .. py:method:: write(text)


   .. py:method:: flush()


   .. py:method:: isatty()


.. py:function:: runscript(script)

   Executes a script.
   This function is present for backward compatiblity. Please use idaapi.IDAPython_ExecScript() instead

   :param script: script path

   :returns: Error string or None on success


.. py:function:: print_banner()

.. py:class:: IDAPythonHelpPrompter

   Bases: :py:obj:`object`


   .. py:method:: readline()


.. py:class:: IDAPythonHelp

   Bases: :py:obj:`pydoc.Helper`


   .. py:method:: help(*args)


.. py:data:: help

.. py:data:: idausr_python_list

.. py:data:: userrc


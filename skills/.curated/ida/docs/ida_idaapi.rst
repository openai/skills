ida_idaapi
==========

.. py:module:: ida_idaapi


Attributes
----------

.. autoapisummary::

   ida_idaapi.BADADDR
   ida_idaapi.BADADDR32
   ida_idaapi.BADADDR64
   ida_idaapi.BADSEL
   ida_idaapi.SIZE_MAX
   ida_idaapi.ea_t
   ida_idaapi.integer_types
   ida_idaapi.SEEK_SET
   ida_idaapi.SEEK_CUR
   ida_idaapi.SEEK_END
   ida_idaapi.PLUGIN_MOD
   ida_idaapi.PLUGIN_DRAW
   ida_idaapi.PLUGIN_SEG
   ida_idaapi.PLUGIN_UNL
   ida_idaapi.PLUGIN_HIDE
   ida_idaapi.PLUGIN_DBG
   ida_idaapi.PLUGIN_PROC
   ida_idaapi.PLUGIN_FIX
   ida_idaapi.PLUGIN_MULTI
   ida_idaapi.PLUGIN_SKIP
   ida_idaapi.PLUGIN_OK
   ida_idaapi.PLUGIN_KEEP
   ida_idaapi.PY_ICID_INT64
   ida_idaapi.PY_ICID_BYREF
   ida_idaapi.PY_ICID_OPAQUE
   ida_idaapi.ST_OVER_DEBUG_SEG
   ida_idaapi.ST_OVER_LIB_FUNC
   ida_idaapi.as_unicode
   ida_idaapi.IDAPython_Completion
   ida_idaapi.NW_OPENIDB
   ida_idaapi.NW_CLOSEIDB
   ida_idaapi.NW_INITIDA
   ida_idaapi.NW_TERMIDA
   ida_idaapi.NW_REMOVE
   ida_idaapi.HBF_CALL_WITH_NEW_EXEC
   ida_idaapi.HBF_VOLATILE_METHOD_SET


Classes
-------

.. autoapisummary::

   ida_idaapi.pyidc_opaque_object_t
   ida_idaapi.py_clinked_object_t
   ida_idaapi.object_t
   ida_idaapi.plugin_t
   ida_idaapi.plugmod_t
   ida_idaapi.pyidc_cvt_helper__
   ida_idaapi.PyIdc_cvt_int64__
   ida_idaapi.PyIdc_cvt_refclass__
   ida_idaapi.IDAPython_displayhook
   ida_idaapi.loader_input_t


Functions
---------

.. autoapisummary::

   ida_idaapi.require
   ida_idaapi.replfun
   ida_idaapi.as_cstr
   ida_idaapi.as_UTF16
   ida_idaapi.as_uint32
   ida_idaapi.as_int32
   ida_idaapi.as_signed
   ida_idaapi.TRUNC
   ida_idaapi.copy_bits
   ida_idaapi.struct_unpack
   ida_idaapi.IDAPython_ExecSystem
   ida_idaapi.IDAPython_FormatExc
   ida_idaapi.IDAPython_ExecScript
   ida_idaapi.IDAPython_LoadProcMod
   ida_idaapi.IDAPython_UnLoadProcMod
   ida_idaapi.IDAPython_GetDocstrings
   ida_idaapi.notify_when
   ida_idaapi.parse_command_line3
   ida_idaapi.set_script_timeout
   ida_idaapi.disable_script_timeout
   ida_idaapi.enable_extlang_python
   ida_idaapi.enable_python_cli
   ida_idaapi.format_basestring
   ida_idaapi.pygc_refresh
   ida_idaapi.pygc_create_groups
   ida_idaapi.pygc_delete_groups
   ida_idaapi.pygc_set_groups_visibility
   ida_idaapi.pycim_get_widget
   ida_idaapi.pycim_view_close


Module Contents
---------------

.. py:data:: BADADDR

.. py:data:: BADADDR32

.. py:data:: BADADDR64

.. py:data:: BADSEL

.. py:data:: SIZE_MAX

.. py:data:: ea_t

.. py:data:: integer_types

.. py:function:: require(modulename, package=None)

   Load, or reload a module.

   When under heavy development, a user's tool might consist of multiple
   modules. If those are imported using the standard 'import' mechanism,
   there is no guarantee that the Python implementation will re-read
   and re-evaluate the module's Python code. In fact, it usually doesn't.
   What should be done instead is 'reload()'-ing that module.

   This is a simple helper function that will do just that: In case the
   module doesn't exist, it 'import's it, and if it does exist,
   'reload()'s it.

   The importing module (i.e., the module calling require()) will have
   the loaded module bound to its globals(), under the name 'modulename'.
   (If require() is called from the command line, the importing module
   will be '__main__'.)

   For more information, see: <http://www.hexblog.com/?p=749>.


.. py:function:: replfun(func)

.. py:data:: SEEK_SET
   :value: 0


.. py:data:: SEEK_CUR
   :value: 1


.. py:data:: SEEK_END
   :value: 2


.. py:data:: PLUGIN_MOD
   :value: 1


.. py:data:: PLUGIN_DRAW
   :value: 2


.. py:data:: PLUGIN_SEG
   :value: 4


.. py:data:: PLUGIN_UNL
   :value: 8


.. py:data:: PLUGIN_HIDE
   :value: 16


.. py:data:: PLUGIN_DBG
   :value: 32


.. py:data:: PLUGIN_PROC
   :value: 64


.. py:data:: PLUGIN_FIX
   :value: 128


.. py:data:: PLUGIN_MULTI
   :value: 256


.. py:data:: PLUGIN_SKIP
   :value: 0


.. py:data:: PLUGIN_OK
   :value: 1


.. py:data:: PLUGIN_KEEP
   :value: 2


.. py:data:: PY_ICID_INT64
   :value: 0


   int64 object


.. py:data:: PY_ICID_BYREF
   :value: 1


   byref object


.. py:data:: PY_ICID_OPAQUE
   :value: 2


   opaque object


.. py:data:: ST_OVER_DEBUG_SEG
   :value: 1


   step tracing will be disabled when IP is in a debugger segment


.. py:data:: ST_OVER_LIB_FUNC
   :value: 2


   step tracing will be disabled when IP is in a library function


.. py:class:: pyidc_opaque_object_t

   Bases: :py:obj:`object`


   This is the base class for all Python<->IDC opaque objects


.. py:class:: py_clinked_object_t(lnk=None)

   Bases: :py:obj:`pyidc_opaque_object_t`


   This is a utility and base class for C linked objects


   .. py:method:: copy()

      Returns a new copy of this class



   .. py:method:: assign(other)

      Overwrite me.
      This method allows you to assign an instance contents to anothers
      :returns: Boolean



   .. py:attribute:: clink

      Returns the C link as a PyObject



   .. py:attribute:: clink_ptr

      Returns the C link pointer as a number



.. py:class:: object_t(**kwds)

   Bases: :py:obj:`object`


   Helper class used to initialize empty objects


.. py:class:: plugin_t

   Bases: :py:obj:`pyidc_opaque_object_t`


   Base class for all scripted plugins.


   .. py:method:: run(arg)


   .. py:method:: term()


.. py:class:: plugmod_t

   Bases: :py:obj:`pyidc_opaque_object_t`


   Base class for all scripted multi-plugins.


.. py:class:: pyidc_cvt_helper__(cvt_id, value)

   Bases: :py:obj:`object`


   This is a special helper object that helps detect which kind
   of object is this python object wrapping and how to convert it
   back and from IDC.
   This object is characterized by its special attribute and its value


   .. py:attribute:: value


.. py:class:: PyIdc_cvt_int64__(v)

   Bases: :py:obj:`pyidc_cvt_helper__`


   Helper class for explicitly representing VT_INT64 values


.. py:class:: PyIdc_cvt_refclass__(v)

   Bases: :py:obj:`pyidc_cvt_helper__`


   Helper class for representing references to immutable objects


   .. py:method:: cstr()

      Returns the string as a C string (up to the zero termination)



.. py:function:: as_cstr(val)

   Returns a C str from the passed value. The passed value can be of type refclass (returned by a call to buffer() or byref())
   It scans for the first \x00 and returns the string value up to that point.


.. py:function:: as_UTF16(s)

   Convenience function to convert a string into appropriate unicode format


.. py:data:: as_unicode

.. py:function:: as_uint32(v)

   Returns a number as an unsigned int32 number


.. py:function:: as_int32(v)

   Returns a number as a signed int32 number


.. py:function:: as_signed(v, nbits=32)

   Returns a number as signed. The number of bits are specified by the user.
   The MSB holds the sign.


.. py:function:: TRUNC(ea)

   Truncate EA for the current application bitness


.. py:function:: copy_bits(v, s, e=-1)

   Copy bits from a value
   :param v: the value
   :param s: starting bit (0-based)
   :param e: ending bit


.. py:function:: struct_unpack(buffer, signed=False, offs=0)

   Unpack a buffer given its length and offset using struct.unpack_from().
   This function will know how to unpack the given buffer by using the lookup table '__struct_unpack_table'
   If the buffer is of unknown length then None is returned. Otherwise the unpacked value is returned.


.. py:function:: IDAPython_ExecSystem(cmd)

   Executes a command with popen().


.. py:function:: IDAPython_FormatExc(etype, value=None, tb=None, limit=None)

   This function is used to format an exception given the
   values returned by a PyErr_Fetch()


.. py:function:: IDAPython_ExecScript(path, g, print_error=True)

   Run the specified script.

   This function is used by the low-level plugin code.


.. py:function:: IDAPython_LoadProcMod(path, g, print_error=True)

   Load processor module.


.. py:function:: IDAPython_UnLoadProcMod(script, g, print_error=True)

   Unload processor module.


.. py:function:: IDAPython_GetDocstrings(obj)

.. py:data:: IDAPython_Completion

.. py:data:: NW_OPENIDB
   :value: 1


   Notify when the database is opened. Its callback is of the form: def notify_when_callback(nw_code, is_old_database)


.. py:data:: NW_CLOSEIDB
   :value: 2


   Notify when the database is closed. Its callback is of the form: def notify_when_callback(nw_code)


.. py:data:: NW_INITIDA
   :value: 4


   Notify when the IDA starts. Its callback is of the form: def notify_when_callback(nw_code)


.. py:data:: NW_TERMIDA
   :value: 8


   Notify when the IDA terminates. Its callback is of the form: def notify_when_callback(nw_code)


.. py:data:: NW_REMOVE
   :value: 16


   Use this flag with other flags to uninstall a notifywhen callback


.. py:function:: notify_when(when, callback)

   Register a callback that will be called when an event happens.
   :param when: one of NW_XXXX constants
   :param callback: This callback prototype varies depending on the 'when' parameter:
                    The general callback format:
                        def notify_when_callback(nw_code)
                    In the case of NW_OPENIDB:
                        def notify_when_callback(nw_code, is_old_database)
   :returns: Boolean


.. py:class:: IDAPython_displayhook

   .. py:attribute:: orig_displayhook


   .. py:method:: format_seq(num_printer, storage, item, opn, cls)


   .. py:method:: format_item(num_printer, storage, item)


   .. py:method:: displayhook_format(item)


   .. py:method:: displayhook(item)


.. py:data:: HBF_CALL_WITH_NEW_EXEC

.. py:data:: HBF_VOLATILE_METHOD_SET

.. py:function:: parse_command_line3(cmdline: str) -> PyObject *

.. py:function:: set_script_timeout(timeout)

   Changes the script timeout value. The script wait box dialog will be hidden and shown again when the timeout elapses.
   See also L{disable_script_timeout}.

   :param timeout: This value is in seconds.
                   If this value is set to zero then the script will never timeout.
   :returns: Returns the old timeout value


.. py:function:: disable_script_timeout()

   Disables the script timeout and hides the script wait box.
   Calling L{set_script_timeout} will not have any effects until the script is compiled and executed again

   :returns: None


.. py:function:: enable_extlang_python(enable)

   Enables or disables Python extlang.
   When enabled, all expressions will be evaluated by Python.

   :param enable: Set to True to enable, False otherwise


.. py:function:: enable_python_cli(enable: bool) -> None

.. py:function:: format_basestring(_in: PyObject *) -> str

.. py:function:: pygc_refresh(_self: PyObject *) -> None

.. py:function:: pygc_create_groups(_self: PyObject *, groups_infos: PyObject *) -> PyObject *

.. py:function:: pygc_delete_groups(_self: PyObject *, groups: PyObject *, new_current: PyObject *) -> PyObject *

.. py:function:: pygc_set_groups_visibility(_self: PyObject *, groups: PyObject *, expand: PyObject *, new_current: PyObject *) -> PyObject *

.. py:function:: pycim_get_widget(_self: PyObject *) -> TWidget *

.. py:function:: pycim_view_close(_self: PyObject *) -> None

.. py:class:: loader_input_t(pycapsule=None)

   Bases: :py:obj:`object`


   A helper class to work with linput_t related functions.
   This class is also used by file loaders scripts.


   .. py:attribute:: thisown


   .. py:method:: close()

      Closes the file



   .. py:method:: open(filename, remote=False)

      Opens a file (or a remote file)

      :param filename: the file name
      :param remote: whether the file is local, or remote
      :returns: Boolean



   .. py:method:: set_linput(linput)

      Links the current loader_input_t instance to a linput_t instance

      :param linput: the linput_t to link to



   .. py:method:: from_linput(linput: linput_t *) -> loader_input_t *
      :staticmethod:



   .. py:method:: from_capsule(pycapsule: PyObject *) -> loader_input_t *
      :staticmethod:



   .. py:method:: from_fp(fp)
      :staticmethod:


      A static method to construct an instance from a FILE*

      :param fp: a FILE pointer
      :returns: a new instance, or None



   .. py:method:: get_linput() -> linput_t *


   .. py:method:: open_memory(start: ea_t, size: int)

      Create a linput for process memory (By internally calling idaapi.create_memory_linput())
      This linput will use dbg->read_memory() to read data

      :param start: starting address of the input
      :param size: size of the memory range to represent as linput
                  if unknown, may be passed as 0



   .. py:method:: seek(offset: int, whence=SEEK_SET)

      Set input source position

      :param offset: the seek offset
      :param whence: the position to seek from
      :returns: the new position (not 0 as fseek!)



   .. py:method:: tell()

      Returns the current position



   .. py:method:: getz(size: int, fpos: int = -1)

      Returns a zero terminated string at the given position

      :param size: maximum size of the string
      :param fpos: if != -1 then seek will be performed before reading
      :returns: The string or None on failure.



   .. py:method:: gets(len: int)

      Reads a line from the input file. Returns the read line or None

      :param len: the maximum line length
      :returns: a str, or None



   .. py:method:: read(size: int = -1)

      Read up to size bytes (all data if size is negative). Return an empty bytes object on EOF.

      :param size: the maximum number of bytes to read
      :returns: a bytes object



   .. py:method:: opened()

      Checks if the file is opened or not



   .. py:method:: readbytes(size: int, big_endian: bool)

      Similar to read() but it respect the endianness

      :param size: the maximum number of bytes to read
      :param big_endian: endianness
      :returns: a str, or None



   .. py:method:: file2base(pos: int, ea1: ea_t, ea2: ea_t, patchable: bool)

      Load portion of file into the database
      This function will include (ea1..ea2) into the addressing space of the
      program (make it enabled)

      :param li: pointer ot input source
      :param pos: position in the file
      :param ea1: start of range of destination linear addresses
      :param ea2: end of range of destination linear addresses
      :param patchable: should the kernel remember correspondance of
                        file offsets to linear addresses.
      :returns: 1-ok,0-read error, a warning is displayed



   .. py:method:: size() -> int64


   .. py:method:: filename() -> PyObject *


   .. py:method:: get_byte()

      Reads a single byte from the file. Returns None if EOF or the read byte




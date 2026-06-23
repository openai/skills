ida_pro
=======

.. py:module:: ida_pro

.. autoapi-nested-parse::

   This is the first header included in the IDA project.

   It defines the most common types, functions and data. Also, it tries to make system dependent definitions.
   The following preprocessor macros are used in the project (the list may be incomplete)
   Platform must be specified as one of:
   __NT__ - MS Windows (all platforms) 
    __LINUX__ - Linux 
    __MAC__ - MAC OS X
   __EA64__ - 64-bit address size (sizeof(ea_t)==8) 
    __X86__ - 32-bit debug servers (sizeof(void*)==4) 
    __X64__ - x64 processor (sizeof(void*)==8) default 
    __PPC__ - PowerPC 
    __ARM__ - ARM 
       



Attributes
----------

.. autoapisummary::

   ida_pro.BADDIFF
   ida_pro.IDA_SDK_VERSION
   ida_pro.BADMEMSIZE
   ida_pro.MAXSTR
   ida_pro.FMT_64
   ida_pro.FMT_Z
   ida_pro.FMT_ZX
   ida_pro.FMT_ZS
   ida_pro.FMT_EA
   ida_pro.IDBDEC_ESCAPE
   ida_pro.CP_BOM
   ida_pro.UTF8_BOM
   ida_pro.UTF16LE_BOM
   ida_pro.UTF16BE_BOM
   ida_pro.UTF32LE_BOM
   ida_pro.UTF32BE_BOM
   ida_pro.CP_ELLIPSIS
   ida_pro.UTF8_ELLIPSIS
   ida_pro.CP_REPLCHAR
   ida_pro.UTF8_REPLCHAR
   ida_pro.MAX_UTF8_SEQ_LEN
   ida_pro.CEF_RETERR
   ida_pro.ENC_WIN1252
   ida_pro.ENC_UTF8
   ida_pro.ENC_MUTF8
   ida_pro.ENC_UTF16
   ida_pro.ENC_UTF16LE
   ida_pro.ENC_UTF16BE
   ida_pro.ENC_UTF32
   ida_pro.ENC_UTF32LE
   ida_pro.ENC_UTF32BE
   ida_pro.CP_UTF8
   ida_pro.CP_UTF16
   ida_pro.SUBSTCHAR
   ida_pro.IOREDIR_INPUT
   ida_pro.IOREDIR_OUTPUT
   ida_pro.IOREDIR_APPEND
   ida_pro.IOREDIR_QUOTED
   ida_pro.QWCONTINUED
   ida_pro.QWNOHANG
   ida_pro.TCT_UNKNOWN
   ida_pro.TCT_OWNER
   ida_pro.TCT_NOT_OWNER
   ida_pro.cvar
   ida_pro.NULL_PIPE_HANDLE
   ida_pro.longlongvec_t
   ida_pro.ulonglongvec_t
   ida_pro.svalvec_t
   ida_pro.eavec_t


Classes
-------

.. autoapisummary::

   ida_pro.qrefcnt_obj_t
   ida_pro.channel_redir_t
   ida_pro.plugin_options_t
   ida_pro.instant_dbgopts_t
   ida_pro.qmutex_locker_t
   ida_pro.intvec_t
   ida_pro.uintvec_t
   ida_pro.int64vec_t
   ida_pro.uint64vec_t
   ida_pro.boolvec_t
   ida_pro.strvec_t
   ida_pro.sizevec_t
   ida_pro.uchar_array
   ida_pro.tid_array
   ida_pro.ea_array
   ida_pro.sel_array
   ida_pro.uval_array
   ida_pro.uchar_pointer
   ida_pro.ushort_pointer
   ida_pro.uint_pointer
   ida_pro.sint8_pointer
   ida_pro.int8_pointer
   ida_pro.uint8_pointer
   ida_pro.int16_pointer
   ida_pro.uint16_pointer
   ida_pro.int32_pointer
   ida_pro.uint32_pointer
   ida_pro.int64_pointer
   ida_pro.uint64_pointer
   ida_pro.ssize_pointer
   ida_pro.bool_pointer
   ida_pro.char_pointer
   ida_pro.short_pointer
   ida_pro.int_pointer
   ida_pro.ea_pointer
   ida_pro.sel_pointer
   ida_pro.asize_pointer
   ida_pro.adiff_pointer
   ida_pro.uval_pointer
   ida_pro.sval_pointer
   ida_pro.ea32_pointer
   ida_pro.ea64_pointer
   ida_pro.flags_pointer
   ida_pro.flags64_pointer
   ida_pro.tid_pointer


Functions
---------

.. autoapisummary::

   ida_pro.qatoll
   ida_pro.qexit
   ida_pro.log2ceil
   ida_pro.log2floor
   ida_pro.bitcountr_zero
   ida_pro.extend_sign
   ida_pro.readbytes
   ida_pro.writebytes
   ida_pro.reloc_value
   ida_pro.qvector_reserve
   ida_pro.relocate_relobj
   ida_pro.is_cvt64
   ida_pro.quote_cmdline_arg
   ida_pro.parse_dbgopts
   ida_pro.check_process_exit
   ida_pro.is_control_tty
   ida_pro.qdetach_tty
   ida_pro.qcontrol_tty
   ida_pro.qthread_equal
   ida_pro.is_main_thread
   ida_pro.get_login_name
   ida_pro.get_physical_core_count
   ida_pro.get_logical_core_count
   ida_pro.get_available_core_count
   ida_pro.qstrvec_t_create
   ida_pro.qstrvec_t_destroy
   ida_pro.qstrvec_t_get_clink
   ida_pro.qstrvec_t_get_clink_ptr
   ida_pro.qstrvec_t_assign
   ida_pro.qstrvec_t_addressof
   ida_pro.qstrvec_t_set
   ida_pro.qstrvec_t_from_list
   ida_pro.qstrvec_t_size
   ida_pro.qstrvec_t_get
   ida_pro.qstrvec_t_add
   ida_pro.qstrvec_t_clear
   ida_pro.qstrvec_t_insert
   ida_pro.qstrvec_t_remove
   ida_pro.str2user


Module Contents
---------------

.. py:data:: BADDIFF

.. py:data:: IDA_SDK_VERSION

   IDA SDK v9.2.


.. py:data:: BADMEMSIZE

.. py:data:: MAXSTR

   maximum string size


.. py:function:: qatoll(nptr: str) -> int64

.. py:data:: FMT_64

.. py:data:: FMT_Z

.. py:data:: FMT_ZX

.. py:data:: FMT_ZS

.. py:data:: FMT_EA

.. py:function:: qexit(code: int) -> None

   Call qatexit functions, shut down UI and kernel, and exit. 
           
   :param code: exit code


.. py:function:: log2ceil(d64: uint64) -> int

   calculate ceil(log2(d64)) or floor(log2(d64)), it returns 0 if d64 == 0 
           


.. py:function:: log2floor(d64: uint64) -> int

.. py:function:: bitcountr_zero(x: uint64) -> int

   count the number of consecutive trailing zero bits (line C++20 std::countr_zero()) 
           


.. py:function:: extend_sign(v: uint64, nbytes: int, sign_extend: bool) -> uint64

   Sign-, or zero-extend the value 'v' to occupy 64 bits. The value 'v' is considered to be of size 'nbytes'. 
           


.. py:function:: readbytes(h: int, res: uint32 *, size: int, mf: bool) -> int

   Read at most 4 bytes from file. 
           
   :param h: file handle
   :param res: value read from file
   :param size: size of value in bytes (1,2,4)
   :param mf: is MSB first?
   :returns: 0 on success, nonzero otherwise


.. py:function:: writebytes(h: int, l: int, size: int, mf: bool) -> int

   Write at most 4 bytes to file. 
           
   :param h: file handle
   :param l: value to write
   :param size: size of value in bytes (1,2,4)
   :param mf: is MSB first?
   :returns: 0 on success, nonzero otherwise


.. py:function:: reloc_value(value: void *, size: int, delta: adiff_t, mf: bool) -> None

.. py:function:: qvector_reserve(vec: void *, old: void *, cnt: size_t, elsize: size_t) -> void *

   Change capacity of given qvector. 
           
   :param vec: a pointer to a qvector
   :param old: a pointer to the qvector's array
   :param cnt: number of elements to reserve
   :param elsize: size of each element
   :returns: a pointer to the newly allocated array


.. py:class:: qrefcnt_obj_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: refcnt
      :type:  int

      counter 
              



   .. py:method:: release() -> None

      Call destructor. We use release() instead of operator delete() to maintain binary compatibility with all compilers (vc and gcc use different vtable layouts for operator delete) 
              



.. py:function:: relocate_relobj(_relobj: relobj_t *, ea: ida_idaapi.ea_t, mf: bool) -> bool

.. py:data:: IDBDEC_ESCAPE

   convert non-printable characters to C escapes (
   , \xNN, \uNNNN)


.. py:data:: CP_BOM

.. py:data:: UTF8_BOM

.. py:data:: UTF16LE_BOM

.. py:data:: UTF16BE_BOM

.. py:data:: UTF32LE_BOM

.. py:data:: UTF32BE_BOM

.. py:data:: CP_ELLIPSIS

.. py:data:: UTF8_ELLIPSIS

.. py:data:: CP_REPLCHAR

.. py:data:: UTF8_REPLCHAR

.. py:data:: MAX_UTF8_SEQ_LEN

.. py:function:: is_cvt64() -> bool

   is IDA converting IDB into I64?


.. py:data:: CEF_RETERR

.. py:data:: ENC_WIN1252

.. py:data:: ENC_UTF8

.. py:data:: ENC_MUTF8

.. py:data:: ENC_UTF16

.. py:data:: ENC_UTF16LE

.. py:data:: ENC_UTF16BE

.. py:data:: ENC_UTF32

.. py:data:: ENC_UTF32LE

.. py:data:: ENC_UTF32BE

.. py:data:: CP_UTF8

.. py:data:: CP_UTF16

   UTF-16 codepage.


.. py:data:: SUBSTCHAR

   default char, used if a char cannot be represented in a codepage


.. py:class:: channel_redir_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: fd
      :type:  int

      channel number



   .. py:attribute:: file
      :type:  str

      file name to redirect to/from. if empty, the channel must be closed. 
              



   .. py:attribute:: flags
      :type:  int

      i/o redirection flags 
              



   .. py:method:: is_input() -> bool


   .. py:method:: is_output() -> bool


   .. py:method:: is_append() -> bool


   .. py:method:: is_quoted() -> bool


   .. py:attribute:: start
      :type:  int

      begin of the redirection string in the command line



   .. py:attribute:: length
      :type:  int

      length of the redirection string in the command line



.. py:data:: IOREDIR_INPUT

   input redirection


.. py:data:: IOREDIR_OUTPUT

   output redirection


.. py:data:: IOREDIR_APPEND

   append, do not overwrite the output file


.. py:data:: IOREDIR_QUOTED

   the file name was quoted


.. py:function:: quote_cmdline_arg(arg: str) -> bool

   Quote a command line argument if it contains escape characters. For example, *.c will be converted into "*.c" because * may be inadvertently expanded by the shell 
           
   :returns: true: modified 'arg'


.. py:class:: plugin_options_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: find(name: str) -> plugin_option_t const *


   .. py:method:: erase(name: str) -> bool


.. py:class:: instant_dbgopts_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: debmod
      :type:  str

      name of debugger module



   .. py:attribute:: env
      :type:  str

      config variables for debmod. example: DEFAULT_CPU=13;MAXPACKETSIZE=-1



   .. py:attribute:: host
      :type:  str

      remote hostname (if remote debugging)



   .. py:attribute:: port
      :type:  int

      port number for the remote debugger server



   .. py:attribute:: pid
      :type:  int

      process to attach to (-1: ask the user)



   .. py:attribute:: event_id
      :type:  int

      event to trigger upon attaching



   .. py:attribute:: attach
      :type:  bool

      should attach to a process?



.. py:function:: parse_dbgopts(ido: instant_dbgopts_t, r_switch: str) -> bool

   Parse the -r command line switch (for instant debugging). r_switch points to the value of the -r switch. Example: win32@localhost+ 
           
   :returns: true-ok, false-parse error


.. py:data:: QWCONTINUED

.. py:data:: QWNOHANG

.. py:function:: check_process_exit(handle: void *, exit_code: int *, msecs: int = -1) -> int

   Check whether process has terminated or not. 
           
   :param handle: process handle to wait for
   :param exit_code: pointer to the buffer for the exit code
   :returns: 0: process has exited, and the exit code is available. if *exit_code < 0: the process was killed with a signal -*exit_code
   :returns: 1: process has not exited yet
   :returns: -1: error happened, see error code for winerr() in *exit_code


.. py:data:: TCT_UNKNOWN

.. py:data:: TCT_OWNER

.. py:data:: TCT_NOT_OWNER

.. py:function:: is_control_tty(fd: int) -> enum tty_control_t

   Check if the current process is the owner of the TTY specified by 'fd' (typically an opened descriptor to /dev/tty). 
           


.. py:function:: qdetach_tty() -> None

   If the current terminal is the controlling terminal of the calling process, give up this controlling terminal. 
           


.. py:function:: qcontrol_tty() -> None

   Make the current terminal the controlling terminal of the calling process. 
           


.. py:function:: qthread_equal(q1: __qthread_t, q2: __qthread_t) -> bool

   Are two threads equal?


.. py:function:: is_main_thread() -> bool

   Are we running in the main thread?


.. py:class:: qmutex_locker_t(_lock: __qmutex_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


.. py:function:: get_login_name() -> str

   Get the user name for the current desktop session 
           
   :returns: success


.. py:function:: get_physical_core_count() -> int

   Get the total CPU physical core count 
           
   :returns: the physical core count, or -1 on error


.. py:function:: get_logical_core_count() -> int

   Get the total CPU logical core count 
           
   :returns: the logical core count, or -1 on error


.. py:function:: get_available_core_count() -> int

   Get the number of logical CPU cores available to the current process if supported by the OS. 
           
   :returns: the logical core count available for the process, or -1 on error


.. py:class:: intvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> int &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> int const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: intvec_t) -> None


   .. py:method:: extract() -> int *


   .. py:method:: inject(s: int *, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< int >::const_iterator


   .. py:method:: end(*args) -> qvector< int >::const_iterator


   .. py:method:: insert(it: qvector< int >::iterator, x: int const &) -> qvector< int >::iterator


   .. py:method:: erase(*args) -> qvector< int >::iterator


   .. py:method:: find(*args) -> qvector< int >::const_iterator


   .. py:method:: has(x: int const &) -> bool


   .. py:method:: add_unique(x: int const &) -> bool


   .. py:method:: append(x: int const &) -> None


   .. py:method:: extend(x: intvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:data:: cvar

.. py:data:: NULL_PIPE_HANDLE

.. py:class:: uintvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> unsigned int &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> unsigned int const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: uintvec_t) -> None


   .. py:method:: extract() -> unsigned int *


   .. py:method:: inject(s: unsigned int *, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< unsigned int >::const_iterator


   .. py:method:: end(*args) -> qvector< unsigned int >::const_iterator


   .. py:method:: insert(it: qvector< unsigned int >::iterator, x: unsigned int const &) -> qvector< unsigned int >::iterator


   .. py:method:: erase(*args) -> qvector< unsigned int >::iterator


   .. py:method:: find(*args) -> qvector< unsigned int >::const_iterator


   .. py:method:: has(x: unsigned int const &) -> bool


   .. py:method:: add_unique(x: unsigned int const &) -> bool


   .. py:method:: append(x: unsigned int const &) -> None


   .. py:method:: extend(x: uintvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: int64vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> long long &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> long long const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: int64vec_t) -> None


   .. py:method:: extract() -> long long *


   .. py:method:: inject(s: long long *, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< long long >::const_iterator


   .. py:method:: end(*args) -> qvector< long long >::const_iterator


   .. py:method:: insert(it: qvector< long long >::iterator, x: long long const &) -> qvector< long long >::iterator


   .. py:method:: erase(*args) -> qvector< long long >::iterator


   .. py:method:: find(*args) -> qvector< long long >::const_iterator


   .. py:method:: has(x: long long const &) -> bool


   .. py:method:: add_unique(x: long long const &) -> bool


   .. py:method:: append(x: long long const &) -> None


   .. py:method:: extend(x: int64vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: uint64vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> unsigned long long &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> unsigned long long const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: uint64vec_t) -> None


   .. py:method:: extract() -> unsigned long long *


   .. py:method:: inject(s: unsigned long long *, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< unsigned long long >::const_iterator


   .. py:method:: end(*args) -> qvector< unsigned long long >::const_iterator


   .. py:method:: insert(it: qvector< unsigned long long >::iterator, x: unsigned long long const &) -> qvector< unsigned long long >::iterator


   .. py:method:: erase(*args) -> qvector< unsigned long long >::iterator


   .. py:method:: find(*args) -> qvector< unsigned long long >::const_iterator


   .. py:method:: has(x: unsigned long long const &) -> bool


   .. py:method:: add_unique(x: unsigned long long const &) -> bool


   .. py:method:: append(x: unsigned long long const &) -> None


   .. py:method:: extend(x: uint64vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: boolvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> bool &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> bool const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: boolvec_t) -> None


   .. py:method:: extract() -> bool *


   .. py:method:: inject(s: bool *, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< bool >::const_iterator


   .. py:method:: end(*args) -> qvector< bool >::const_iterator


   .. py:method:: insert(it: qvector< bool >::iterator, x: bool const &) -> qvector< bool >::iterator


   .. py:method:: erase(*args) -> qvector< bool >::iterator


   .. py:method:: find(*args) -> qvector< bool >::const_iterator


   .. py:method:: has(x: bool const &) -> bool


   .. py:method:: add_unique(x: bool const &) -> bool


   .. py:method:: append(x: bool const &) -> None


   .. py:method:: extend(x: boolvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: strvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> simpleline_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> simpleline_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: strvec_t) -> None


   .. py:method:: extract() -> simpleline_t *


   .. py:method:: inject(s: simpleline_t *, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< simpleline_t >::const_iterator


   .. py:method:: end(*args) -> qvector< simpleline_t >::const_iterator


   .. py:method:: insert(it: qvector< simpleline_t >::iterator, x: simpleline_t const &) -> qvector< simpleline_t >::iterator


   .. py:method:: erase(*args) -> qvector< simpleline_t >::iterator


   .. py:method:: append(x: simpleline_t const &) -> None


   .. py:method:: extend(x: strvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: sizevec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> size_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> size_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: sizevec_t) -> None


   .. py:method:: extract() -> size_t *


   .. py:method:: inject(s: size_t *, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< size_t >::const_iterator


   .. py:method:: end(*args) -> qvector< size_t >::const_iterator


   .. py:method:: insert(it: qvector< size_t >::iterator, x: size_t const &) -> qvector< size_t >::iterator


   .. py:method:: erase(*args) -> qvector< size_t >::iterator


   .. py:method:: find(*args) -> qvector< size_t >::const_iterator


   .. py:method:: has(x: size_t const &) -> bool


   .. py:method:: add_unique(x: size_t const &) -> bool


   .. py:method:: append(x: size_t const &) -> None


   .. py:method:: extend(x: sizevec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:function:: qstrvec_t_create() -> PyObject *

.. py:function:: qstrvec_t_destroy(py_obj: PyObject *) -> bool

.. py:function:: qstrvec_t_get_clink(_self: PyObject *) -> qstrvec_t *

.. py:function:: qstrvec_t_get_clink_ptr(_self: PyObject *) -> PyObject *

.. py:function:: qstrvec_t_assign(_self: PyObject *, other: PyObject *) -> bool

.. py:function:: qstrvec_t_addressof(_self: PyObject *, idx: size_t) -> PyObject *

.. py:function:: qstrvec_t_set(_self: PyObject *, idx: size_t, s: str) -> bool

.. py:function:: qstrvec_t_from_list(_self: PyObject *, py_list: PyObject *) -> bool

.. py:function:: qstrvec_t_size(_self: PyObject *) -> size_t

.. py:function:: qstrvec_t_get(_self: PyObject *, idx: size_t) -> PyObject *

.. py:function:: qstrvec_t_add(_self: PyObject *, s: str) -> bool

.. py:function:: qstrvec_t_clear(_self: PyObject *, qclear: bool) -> bool

.. py:function:: qstrvec_t_insert(_self: PyObject *, idx: size_t, s: str) -> bool

.. py:function:: qstrvec_t_remove(_self: PyObject *, idx: size_t) -> bool

.. py:function:: str2user(str)

   Insert C-style escape characters to string

   :param str: the input string
   :returns: new string with escape characters inserted, or None


.. py:class:: uchar_array(nelements: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: cast() -> uchar *


   .. py:method:: frompointer(t: uchar *) -> uchar_array *
      :staticmethod:



.. py:class:: tid_array(nelements: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: cast() -> tid_t *


   .. py:method:: frompointer(t: tid_t *) -> tid_array *
      :staticmethod:



.. py:class:: ea_array(nelements: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: cast() -> ea_t *


   .. py:method:: frompointer(t: ea_t *) -> ea_array *
      :staticmethod:



.. py:class:: sel_array(nelements: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: cast() -> sel_t *


   .. py:method:: frompointer(t: sel_t *) -> sel_array *
      :staticmethod:



.. py:class:: uval_array(nelements: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: cast() -> uval_t *


   .. py:method:: frompointer(t: uval_t *) -> uval_array *
      :staticmethod:



.. py:class:: uchar_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: uchar) -> None


   .. py:method:: value() -> uchar


   .. py:method:: cast() -> uchar *


   .. py:method:: frompointer(t: uchar *) -> uchar_pointer *
      :staticmethod:



.. py:class:: ushort_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: ushort) -> None


   .. py:method:: value() -> ushort


   .. py:method:: cast() -> ushort *


   .. py:method:: frompointer(t: ushort *) -> ushort_pointer *
      :staticmethod:



.. py:class:: uint_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: uint) -> None


   .. py:method:: value() -> uint


   .. py:method:: cast() -> uint *


   .. py:method:: frompointer(t: uint *) -> uint_pointer *
      :staticmethod:



.. py:class:: sint8_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: sint8) -> None


   .. py:method:: value() -> sint8


   .. py:method:: cast() -> sint8 *


   .. py:method:: frompointer(t: sint8 *) -> sint8_pointer *
      :staticmethod:



.. py:class:: int8_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: int8) -> None


   .. py:method:: value() -> int8


   .. py:method:: cast() -> int8 *


   .. py:method:: frompointer(t: int8 *) -> int8_pointer *
      :staticmethod:



.. py:class:: uint8_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: uint8) -> None


   .. py:method:: value() -> uint8


   .. py:method:: cast() -> uint8 *


   .. py:method:: frompointer(t: uint8 *) -> uint8_pointer *
      :staticmethod:



.. py:class:: int16_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: int16) -> None


   .. py:method:: value() -> int16


   .. py:method:: cast() -> int16 *


   .. py:method:: frompointer(t: int16 *) -> int16_pointer *
      :staticmethod:



.. py:class:: uint16_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: uint16) -> None


   .. py:method:: value() -> uint16


   .. py:method:: cast() -> uint16 *


   .. py:method:: frompointer(t: uint16 *) -> uint16_pointer *
      :staticmethod:



.. py:class:: int32_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: int) -> None


   .. py:method:: value() -> int


   .. py:method:: cast() -> int32 *


   .. py:method:: frompointer(t: int32 *) -> int32_pointer *
      :staticmethod:



.. py:class:: uint32_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: int) -> None


   .. py:method:: value() -> int


   .. py:method:: cast() -> uint32 *


   .. py:method:: frompointer(t: uint32 *) -> uint32_pointer *
      :staticmethod:



.. py:class:: int64_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: int64) -> None


   .. py:method:: value() -> int64


   .. py:method:: cast() -> int64 *


   .. py:method:: frompointer(t: int64 *) -> int64_pointer *
      :staticmethod:



.. py:class:: uint64_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: uint64) -> None


   .. py:method:: value() -> uint64


   .. py:method:: cast() -> uint64 *


   .. py:method:: frompointer(t: uint64 *) -> uint64_pointer *
      :staticmethod:



.. py:class:: ssize_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: ssize_t) -> None


   .. py:method:: value() -> ssize_t


   .. py:method:: cast() -> ssize_t *


   .. py:method:: frompointer(t: ssize_t *) -> ssize_pointer *
      :staticmethod:



.. py:class:: bool_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: bool) -> None


   .. py:method:: value() -> bool


   .. py:method:: cast() -> bool *


   .. py:method:: frompointer(t: bool *) -> bool_pointer *
      :staticmethod:



.. py:class:: char_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: char) -> None


   .. py:method:: value() -> char


   .. py:method:: cast() -> char *


   .. py:method:: frompointer(t: char *) -> char_pointer *
      :staticmethod:



.. py:class:: short_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: short) -> None


   .. py:method:: value() -> short


   .. py:method:: cast() -> short *


   .. py:method:: frompointer(t: short *) -> short_pointer *
      :staticmethod:



.. py:class:: int_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: int) -> None


   .. py:method:: value() -> int


   .. py:method:: cast() -> int *


   .. py:method:: frompointer(t: int *) -> int_pointer *
      :staticmethod:



.. py:class:: ea_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: ida_idaapi.ea_t) -> None


   .. py:method:: value() -> ida_idaapi.ea_t


   .. py:method:: cast() -> ea_t *


   .. py:method:: frompointer(t: ea_t *) -> ea_pointer *
      :staticmethod:



.. py:class:: sel_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: sel_t) -> None


   .. py:method:: value() -> sel_t


   .. py:method:: cast() -> sel_t *


   .. py:method:: frompointer(t: sel_t *) -> sel_pointer *
      :staticmethod:



.. py:class:: asize_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: asize_t) -> None


   .. py:method:: value() -> asize_t


   .. py:method:: cast() -> asize_t *


   .. py:method:: frompointer(t: asize_t *) -> asize_pointer *
      :staticmethod:



.. py:class:: adiff_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: adiff_t) -> None


   .. py:method:: value() -> adiff_t


   .. py:method:: cast() -> adiff_t *


   .. py:method:: frompointer(t: adiff_t *) -> adiff_pointer *
      :staticmethod:



.. py:class:: uval_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: int) -> None


   .. py:method:: value() -> int


   .. py:method:: cast() -> uval_t *


   .. py:method:: frompointer(t: uval_t *) -> uval_pointer *
      :staticmethod:



.. py:class:: sval_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: int) -> None


   .. py:method:: value() -> int


   .. py:method:: cast() -> sval_t *


   .. py:method:: frompointer(t: sval_t *) -> sval_pointer *
      :staticmethod:



.. py:class:: ea32_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: ea32_t) -> None


   .. py:method:: value() -> ea32_t


   .. py:method:: cast() -> ea32_t *


   .. py:method:: frompointer(t: ea32_t *) -> ea32_pointer *
      :staticmethod:



.. py:class:: ea64_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: ea64_t) -> None


   .. py:method:: value() -> ea64_t


   .. py:method:: cast() -> ea64_t *


   .. py:method:: frompointer(t: ea64_t *) -> ea64_pointer *
      :staticmethod:



.. py:class:: flags_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: flags_t) -> None


   .. py:method:: value() -> flags_t


   .. py:method:: cast() -> flags_t *


   .. py:method:: frompointer(t: flags_t *) -> flags_pointer *
      :staticmethod:



.. py:class:: flags64_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: flags64_t) -> None


   .. py:method:: value() -> flags64_t


   .. py:method:: cast() -> flags64_t *


   .. py:method:: frompointer(t: flags64_t *) -> flags64_pointer *
      :staticmethod:



.. py:class:: tid_pointer

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: assign(value: tid_t) -> None


   .. py:method:: value() -> tid_t


   .. py:method:: cast() -> tid_t *


   .. py:method:: frompointer(t: tid_t *) -> tid_pointer *
      :staticmethod:



.. py:data:: longlongvec_t

.. py:data:: ulonglongvec_t

.. py:data:: svalvec_t

.. py:data:: eavec_t


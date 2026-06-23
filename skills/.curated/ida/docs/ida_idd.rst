ida_idd
=======

.. py:module:: ida_idd

.. autoapi-nested-parse::

   Contains definition of the interface to IDD modules.

   The interface consists of structures describing the target debugged processor and a debugging API. 
       



Attributes
----------

.. autoapisummary::

   ida_idd.IDD_INTERFACE_VERSION
   ida_idd.NO_THREAD
   ida_idd.DEF_ADDRSIZE
   ida_idd.REGISTER_READONLY
   ida_idd.REGISTER_IP
   ida_idd.REGISTER_SP
   ida_idd.REGISTER_FP
   ida_idd.REGISTER_ADDRESS
   ida_idd.REGISTER_CS
   ida_idd.REGISTER_SS
   ida_idd.REGISTER_NOLF
   ida_idd.REGISTER_CUSTFMT
   ida_idd.NO_EVENT
   ida_idd.PROCESS_STARTED
   ida_idd.PROCESS_EXITED
   ida_idd.THREAD_STARTED
   ida_idd.THREAD_EXITED
   ida_idd.BREAKPOINT
   ida_idd.STEP
   ida_idd.EXCEPTION
   ida_idd.LIB_LOADED
   ida_idd.LIB_UNLOADED
   ida_idd.INFORMATION
   ida_idd.PROCESS_ATTACHED
   ida_idd.PROCESS_DETACHED
   ida_idd.PROCESS_SUSPENDED
   ida_idd.TRACE_FULL
   ida_idd.STATUS_MASK
   ida_idd.BITNESS_CHANGED
   ida_idd.cvar
   ida_idd.BPT_WRITE
   ida_idd.BPT_READ
   ida_idd.BPT_RDWR
   ida_idd.BPT_SOFT
   ida_idd.BPT_EXEC
   ida_idd.BPT_DEFAULT
   ida_idd.EXC_BREAK
   ida_idd.EXC_HANDLE
   ida_idd.EXC_MSG
   ida_idd.EXC_SILENT
   ida_idd.RVT_FLOAT
   ida_idd.RVT_INT
   ida_idd.RVT_UNAVAILABLE
   ida_idd.RESMOD_NONE
   ida_idd.RESMOD_INTO
   ida_idd.RESMOD_OVER
   ida_idd.RESMOD_OUT
   ida_idd.RESMOD_SRCINTO
   ida_idd.RESMOD_SRCOVER
   ida_idd.RESMOD_SRCOUT
   ida_idd.RESMOD_USER
   ida_idd.RESMOD_HANDLE
   ida_idd.RESMOD_BACKINTO
   ida_idd.RESMOD_MAX
   ida_idd.STEP_TRACE
   ida_idd.INSN_TRACE
   ida_idd.FUNC_TRACE
   ida_idd.BBLK_TRACE
   ida_idd.DRC_EVENTS
   ida_idd.DRC_CRC
   ida_idd.DRC_OK
   ida_idd.DRC_NONE
   ida_idd.DRC_FAILED
   ida_idd.DRC_NETERR
   ida_idd.DRC_NOFILE
   ida_idd.DRC_IDBSEG
   ida_idd.DRC_NOPROC
   ida_idd.DRC_NOCHG
   ida_idd.DRC_ERROR
   ida_idd.DEBUGGER_ID_X86_IA32_WIN32_USER
   ida_idd.DEBUGGER_ID_X86_IA32_LINUX_USER
   ida_idd.DEBUGGER_ID_X86_IA32_MACOSX_USER
   ida_idd.DEBUGGER_ID_ARM_IPHONE_USER
   ida_idd.DEBUGGER_ID_X86_IA32_BOCHS
   ida_idd.DEBUGGER_ID_6811_EMULATOR
   ida_idd.DEBUGGER_ID_GDB_USER
   ida_idd.DEBUGGER_ID_WINDBG
   ida_idd.DEBUGGER_ID_X86_DOSBOX_EMULATOR
   ida_idd.DEBUGGER_ID_ARM_LINUX_USER
   ida_idd.DEBUGGER_ID_TRACE_REPLAYER
   ida_idd.DEBUGGER_ID_X86_PIN_TRACER
   ida_idd.DEBUGGER_ID_DALVIK_USER
   ida_idd.DEBUGGER_ID_XNU_USER
   ida_idd.DEBUGGER_ID_ARM_MACOS_USER
   ida_idd.DBG_FLAG_REMOTE
   ida_idd.DBG_FLAG_NOHOST
   ida_idd.DBG_FLAG_FAKE_ATTACH
   ida_idd.DBG_FLAG_HWDATBPT_ONE
   ida_idd.DBG_FLAG_CAN_CONT_BPT
   ida_idd.DBG_FLAG_NEEDPORT
   ida_idd.DBG_FLAG_DONT_DISTURB
   ida_idd.DBG_FLAG_SAFE
   ida_idd.DBG_FLAG_CLEAN_EXIT
   ida_idd.DBG_FLAG_USE_SREGS
   ida_idd.DBG_FLAG_NOSTARTDIR
   ida_idd.DBG_FLAG_NOPARAMETERS
   ida_idd.DBG_FLAG_NOPASSWORD
   ida_idd.DBG_FLAG_CONNSTRING
   ida_idd.DBG_FLAG_SMALLBLKS
   ida_idd.DBG_FLAG_MANMEMINFO
   ida_idd.DBG_FLAG_EXITSHOTOK
   ida_idd.DBG_FLAG_VIRTHREADS
   ida_idd.DBG_FLAG_LOWCNDS
   ida_idd.DBG_FLAG_DEBTHREAD
   ida_idd.DBG_FLAG_DEBUG_DLL
   ida_idd.DBG_FLAG_FAKE_MEMORY
   ida_idd.DBG_FLAG_ANYSIZE_HWBPT
   ida_idd.DBG_FLAG_TRACER_MODULE
   ida_idd.DBG_FLAG_PREFER_SWBPTS
   ida_idd.DBG_FLAG_LAZY_WATCHPTS
   ida_idd.DBG_FLAG_FAST_STEP
   ida_idd.DBG_FLAG_ADD_ENVS
   ida_idd.DBG_FLAG_MERGE_ENVS
   ida_idd.DBG_FLAG_DISABLE_ASLR
   ida_idd.DBG_FLAG_TTD
   ida_idd.DBG_FLAG_FULL_INSTR_BPT
   ida_idd.DBG_HAS_GET_PROCESSES
   ida_idd.DBG_HAS_ATTACH_PROCESS
   ida_idd.DBG_HAS_DETACH_PROCESS
   ida_idd.DBG_HAS_REQUEST_PAUSE
   ida_idd.DBG_HAS_SET_EXCEPTION_INFO
   ida_idd.DBG_HAS_THREAD_SUSPEND
   ida_idd.DBG_HAS_THREAD_CONTINUE
   ida_idd.DBG_HAS_SET_RESUME_MODE
   ida_idd.DBG_HAS_THREAD_GET_SREG_BASE
   ida_idd.DBG_HAS_CHECK_BPT
   ida_idd.DBG_HAS_OPEN_FILE
   ida_idd.DBG_HAS_UPDATE_CALL_STACK
   ida_idd.DBG_HAS_APPCALL
   ida_idd.DBG_HAS_REXEC
   ida_idd.DBG_HAS_MAP_ADDRESS
   ida_idd.DBG_RESMOD_STEP_INTO
   ida_idd.DBG_RESMOD_STEP_OVER
   ida_idd.DBG_RESMOD_STEP_OUT
   ida_idd.DBG_RESMOD_STEP_SRCINTO
   ida_idd.DBG_RESMOD_STEP_SRCOVER
   ida_idd.DBG_RESMOD_STEP_SRCOUT
   ida_idd.DBG_RESMOD_STEP_USER
   ida_idd.DBG_RESMOD_STEP_HANDLE
   ida_idd.DBG_RESMOD_STEP_BACKINTO
   ida_idd.DBG_PROC_IS_DLL
   ida_idd.DBG_PROC_IS_GUI
   ida_idd.DBG_PROC_32BIT
   ida_idd.DBG_PROC_64BIT
   ida_idd.DBG_NO_TRACE
   ida_idd.DBG_HIDE_WINDOW
   ida_idd.DBG_SUSPENDED
   ida_idd.DBG_NO_ASLR
   ida_idd.BPT_OK
   ida_idd.BPT_INTERNAL_ERR
   ida_idd.BPT_BAD_TYPE
   ida_idd.BPT_BAD_ALIGN
   ida_idd.BPT_BAD_ADDR
   ida_idd.BPT_BAD_LEN
   ida_idd.BPT_TOO_MANY
   ida_idd.BPT_READ_ERROR
   ida_idd.BPT_WRITE_ERROR
   ida_idd.BPT_SKIP
   ida_idd.BPT_PAGE_OK
   ida_idd.APPCALL_MANUAL
   ida_idd.APPCALL_DEBEV
   ida_idd.APPCALL_TIMEOUT
   ida_idd.RQ_MASKING
   ida_idd.RQ_SUSPEND
   ida_idd.RQ_NOSUSP
   ida_idd.RQ_IGNWERR
   ida_idd.RQ_SILENT
   ida_idd.RQ_VERBOSE
   ida_idd.RQ_SWSCREEN
   ida_idd.RQ__NOTHRRF
   ida_idd.RQ_PROCEXIT
   ida_idd.RQ_IDAIDLE
   ida_idd.RQ_SUSPRUN
   ida_idd.RQ_RESUME
   ida_idd.RQ_RESMOD
   ida_idd.RQ_RESMOD_SHIFT
   ida_idd.NO_PROCESS
   ida_idd.NO_THREAD
   ida_idd.dbg_can_query
   ida_idd.Appcall


Classes
-------

.. autoapisummary::

   ida_idd.excvec_t
   ida_idd.procinfo_vec_t
   ida_idd.call_stack_info_vec_t
   ida_idd.meminfo_vec_template_t
   ida_idd.regvals_t
   ida_idd.process_info_t
   ida_idd.debapp_attrs_t
   ida_idd.register_info_t
   ida_idd.memory_info_t
   ida_idd.meminfo_vec_t
   ida_idd.scattered_segm_t
   ida_idd.launch_env_t
   ida_idd.modinfo_t
   ida_idd.bptaddr_t
   ida_idd.excinfo_t
   ida_idd.debug_event_t
   ida_idd.exception_info_t
   ida_idd.regval_t
   ida_idd.call_stack_info_t
   ida_idd.call_stack_t
   ida_idd.thread_name_t
   ida_idd.debugger_t
   ida_idd.dyn_register_info_array
   ida_idd.Appcall_array__
   ida_idd.Appcall_callable__
   ida_idd.Appcall_consts__
   ida_idd.Appcall__


Functions
---------

.. autoapisummary::

   ida_idd.set_debug_event_code
   ida_idd.get_debug_event_name
   ida_idd.dbg_appcall
   ida_idd.cleanup_appcall
   ida_idd.cpu2ieee
   ida_idd.ieee2cpu
   ida_idd.get_dbg
   ida_idd.dbg_get_registers
   ida_idd.dbg_get_thread_sreg_base
   ida_idd.dbg_read_memory
   ida_idd.dbg_write_memory
   ida_idd.dbg_get_name
   ida_idd.dbg_get_memory_info
   ida_idd.appcall
   ida_idd.get_event_module_name
   ida_idd.get_event_module_base
   ida_idd.get_event_module_size
   ida_idd.get_event_exc_info
   ida_idd.get_event_info
   ida_idd.get_event_bpt_hea
   ida_idd.get_event_exc_code
   ida_idd.get_event_exc_ea
   ida_idd.can_exc_continue


Module Contents
---------------

.. py:class:: excvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> exception_info_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> exception_info_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: excvec_t) -> None


   .. py:method:: extract() -> exception_info_t *


   .. py:method:: inject(s: exception_info_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< exception_info_t >::const_iterator


   .. py:method:: end(*args) -> qvector< exception_info_t >::const_iterator


   .. py:method:: insert(it: exception_info_t, x: exception_info_t) -> qvector< exception_info_t >::iterator


   .. py:method:: erase(*args) -> qvector< exception_info_t >::iterator


   .. py:method:: append(x: exception_info_t) -> None


   .. py:method:: extend(x: excvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: procinfo_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> process_info_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> process_info_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: procinfo_vec_t) -> None


   .. py:method:: extract() -> process_info_t *


   .. py:method:: inject(s: process_info_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< process_info_t >::const_iterator


   .. py:method:: end(*args) -> qvector< process_info_t >::const_iterator


   .. py:method:: insert(it: process_info_t, x: process_info_t) -> qvector< process_info_t >::iterator


   .. py:method:: erase(*args) -> qvector< process_info_t >::iterator


   .. py:method:: append(x: process_info_t) -> None


   .. py:method:: extend(x: procinfo_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: call_stack_info_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> call_stack_info_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> call_stack_info_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: call_stack_info_vec_t) -> None


   .. py:method:: extract() -> call_stack_info_t *


   .. py:method:: inject(s: call_stack_info_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< call_stack_info_t >::const_iterator


   .. py:method:: end(*args) -> qvector< call_stack_info_t >::const_iterator


   .. py:method:: insert(it: call_stack_info_t, x: call_stack_info_t) -> qvector< call_stack_info_t >::iterator


   .. py:method:: erase(*args) -> qvector< call_stack_info_t >::iterator


   .. py:method:: find(*args) -> qvector< call_stack_info_t >::const_iterator


   .. py:method:: has(x: call_stack_info_t) -> bool


   .. py:method:: add_unique(x: call_stack_info_t) -> bool


   .. py:method:: append(x: call_stack_info_t) -> None


   .. py:method:: extend(x: call_stack_info_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: meminfo_vec_template_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> memory_info_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> memory_info_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: meminfo_vec_template_t) -> None


   .. py:method:: extract() -> memory_info_t *


   .. py:method:: inject(s: memory_info_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< memory_info_t >::const_iterator


   .. py:method:: end(*args) -> qvector< memory_info_t >::const_iterator


   .. py:method:: insert(it: memory_info_t, x: memory_info_t) -> qvector< memory_info_t >::iterator


   .. py:method:: erase(*args) -> qvector< memory_info_t >::iterator


   .. py:method:: find(*args) -> qvector< memory_info_t >::const_iterator


   .. py:method:: has(x: memory_info_t) -> bool


   .. py:method:: add_unique(x: memory_info_t) -> bool


   .. py:method:: append(x: memory_info_t) -> None


   .. py:method:: extend(x: meminfo_vec_template_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: regvals_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> regval_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> regval_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: regvals_t) -> None


   .. py:method:: extract() -> regval_t *


   .. py:method:: inject(s: regval_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< regval_t >::const_iterator


   .. py:method:: end(*args) -> qvector< regval_t >::const_iterator


   .. py:method:: insert(it: regval_t, x: regval_t) -> qvector< regval_t >::iterator


   .. py:method:: erase(*args) -> qvector< regval_t >::iterator


   .. py:method:: find(*args) -> qvector< regval_t >::const_iterator


   .. py:method:: has(x: regval_t) -> bool


   .. py:method:: add_unique(x: regval_t) -> bool


   .. py:method:: append(x: regval_t) -> None


   .. py:method:: extend(x: regvals_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:data:: IDD_INTERFACE_VERSION

   The IDD interface version number.


.. py:data:: NO_THREAD

   No thread. in PROCESS_STARTED this value can be used to specify that the main thread has not been created. It will be initialized later by a THREAD_STARTED event. 
           


.. py:class:: process_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: pid
      :type:  pid_t

      process id



   .. py:attribute:: name
      :type:  str

      process name



.. py:class:: debapp_attrs_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: cbsize
      :type:  int

      control field: size of this structure



   .. py:attribute:: addrsize
      :type:  int

      address size of the process. Since 64-bit debuggers usually can debug 32-bit applications, we cannot rely on sizeof(ea_t) to detect the current address size. The following variable should be used instead. It is initialized with 8 for 64-bit debuggers but they should adjust it as soon as they learn that a 32-bit application is being debugged. For 32-bit debuggers it is initialized with 4. 
              



   .. py:attribute:: platform
      :type:  str

      platform name process is running/debugging under. (is used as a key value in exceptions.cfg) 
              



   .. py:attribute:: is_be
      :type:  int


.. py:data:: DEF_ADDRSIZE

.. py:class:: register_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str

      Register name.



   .. py:attribute:: flags
      :type:  int

      Register info attribute flags 
              



   .. py:attribute:: register_class_mask
      :type:  uchar

      mask of register classes



   .. py:attribute:: dtype
      :type:  op_dtype_t

      Register size (see Operand value types)



   .. py:attribute:: default_bit_strings_mask
      :type:  int

      mask of default bits



   .. py:attribute:: bit_strings

      strings corresponding to each bit of the register. (nullptr = no bit, same name = multi-bits mask) 
              



   .. py:attribute:: register_class


.. py:data:: REGISTER_READONLY

   the user can't modify the current value of this register


.. py:data:: REGISTER_IP

   instruction pointer


.. py:data:: REGISTER_SP

   stack pointer


.. py:data:: REGISTER_FP

   frame pointer


.. py:data:: REGISTER_ADDRESS

   may contain an address


.. py:data:: REGISTER_CS

   code segment


.. py:data:: REGISTER_SS

   stack segment


.. py:data:: REGISTER_NOLF

   displays this register without returning to the next line, allowing the next register to be displayed to its right (on the same line) 
           


.. py:data:: REGISTER_CUSTFMT

   register should be displayed using a custom data format. the format name is in bit_strings[0]; the corresponding regval_t will use bytevec_t 
           


.. py:class:: memory_info_t

   Bases: :py:obj:`ida_range.range_t`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str

      Memory range name.



   .. py:attribute:: sclass
      :type:  str

      Memory range class name.



   .. py:attribute:: sbase
      :type:  ida_idaapi.ea_t

      Segment base (meaningful only for segmented architectures, e.g. 16-bit x86) The base is specified in paragraphs (i.e. shifted to the right by 4) 
              



   .. py:attribute:: bitness
      :type:  uchar

      Number of bits in segment addresses (0-16bit, 1-32bit, 2-64bit)



   .. py:attribute:: perm
      :type:  uchar

      Memory range permissions (0-no information): see segment.hpp.



.. py:class:: meminfo_vec_t

   Bases: :py:obj:`meminfo_vec_template_t`


   .. py:attribute:: thisown


.. py:class:: scattered_segm_t

   Bases: :py:obj:`ida_range.range_t`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str

      name of the segment



.. py:class:: launch_env_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: merge
      :type:  bool


   .. py:method:: set(envvar: str, value: str) -> None


   .. py:method:: envs() -> PyObject *


.. py:data:: NO_EVENT

   Not an interesting event. This event can be used if the debugger module needs to return an event but there are no valid events. 
             


.. py:data:: PROCESS_STARTED

   New process has been started.


.. py:data:: PROCESS_EXITED

   Process has been stopped.


.. py:data:: THREAD_STARTED

   New thread has been started.


.. py:data:: THREAD_EXITED

   Thread has been stopped.


.. py:data:: BREAKPOINT

   Breakpoint has been reached. IDA will complain about unknown breakpoints, they should be reported as exceptions. 
             


.. py:data:: STEP

   One instruction has been executed. Spurious events of this kind are silently ignored by IDA. 
             


.. py:data:: EXCEPTION

   Exception.


.. py:data:: LIB_LOADED

   New library has been loaded.


.. py:data:: LIB_UNLOADED

   Library has been unloaded.


.. py:data:: INFORMATION

   User-defined information. This event can be used to return empty information This will cause IDA to call get_debug_event() immediately once more. 
             


.. py:data:: PROCESS_ATTACHED

   Successfully attached to running process.


.. py:data:: PROCESS_DETACHED

   Successfully detached from process.


.. py:data:: PROCESS_SUSPENDED

   Process has been suspended. This event can be used by the debugger module to signal if the process spontaneously gets suspended (not because of an exception, breakpoint, or single step). IDA will silently switch to the 'suspended process' mode without displaying any messages. 
             


.. py:data:: TRACE_FULL

   The trace buffer of the tracer module is full and IDA needs to read it before continuing 
             


.. py:data:: STATUS_MASK

   additional info about process state


.. py:data:: BITNESS_CHANGED

   Debugger detected the process bitness changing.


.. py:function:: set_debug_event_code(ev: debug_event_t, id: event_id_t) -> None

.. py:class:: modinfo_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str

      full name of the module



   .. py:attribute:: base
      :type:  ida_idaapi.ea_t

      module base address. if unknown pass BADADDR



   .. py:attribute:: size
      :type:  asize_t

      module size. if unknown pass 0



   .. py:attribute:: rebase_to
      :type:  ida_idaapi.ea_t

      if not BADADDR, then rebase the program to the specified address



.. py:class:: bptaddr_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: hea
      :type:  ida_idaapi.ea_t

      Possible address referenced by hardware breakpoints.



   .. py:attribute:: kea
      :type:  ida_idaapi.ea_t

      Address of the triggered bpt from the kernel's point of view. (for some systems with special memory mappings, the triggered ea might be different from event ea). Use to BADADDR for flat memory model. 
              



.. py:class:: excinfo_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: code
      :type:  int

      Exception code.



   .. py:attribute:: can_cont
      :type:  bool

      Execution of the process can continue after this exception?



   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      Possible address referenced by the exception.



   .. py:attribute:: info
      :type:  str

      Exception message.



.. py:class:: debug_event_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: pid
      :type:  pid_t

      Process where the event occurred.



   .. py:attribute:: tid
      :type:  thid_t

      Thread where the event occurred.



   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      Address where the event occurred.



   .. py:attribute:: handled
      :type:  bool

      Is event handled by the debugger?. (from the system's point of view) Meaningful for EXCEPTION events 
              



   .. py:method:: copy(r: debug_event_t) -> debug_event_t &


   .. py:method:: clear() -> None

      clear the dependent information (see below), set event code to NO_EVENT



   .. py:method:: clear_all() -> None


   .. py:method:: eid() -> event_id_t

      Event code.



   .. py:method:: set_eid(id: event_id_t) -> None

      Set event code. If the new event code is compatible with the old one then the dependent information (see below) will be preserved. Otherwise the event will be cleared and the new event code will be set. 
              



   .. py:method:: is_bitness_changed() -> bool

      process bitness



   .. py:method:: set_bitness_changed(on: bool = True) -> None


   .. py:method:: modinfo() -> modinfo_t &

      Information that depends on the event code:

      < PROCESS_STARTED, PROCESS_ATTACHED, LIB_LOADED PROCESS_EXITED, THREAD_EXITED 
              



   .. py:method:: info() -> str

      BREAKPOINT



   .. py:method:: bpt() -> bptaddr_t &

      EXCEPTION



   .. py:method:: exc() -> excinfo_t &


   .. py:method:: exit_code() -> int const &

      THREAD_STARTED (thread name) LIB_UNLOADED (unloaded library name) INFORMATION (will be displayed in the output window if not empty) 
              



   .. py:method:: set_modinfo(id: event_id_t) -> modinfo_t &


   .. py:method:: set_exit_code(id: event_id_t, code: int) -> None


   .. py:method:: set_info(id: event_id_t) -> str


   .. py:method:: set_bpt() -> bptaddr_t &


   .. py:method:: set_exception() -> excinfo_t &


   .. py:method:: bpt_ea() -> ida_idaapi.ea_t

      On some systems with special memory mappings the triggered ea might be different from the actual ea. Calculate the address to use. 
              



.. py:function:: get_debug_event_name(dev: debug_event_t) -> str

   get debug event name


.. py:class:: exception_info_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: code
      :type:  uint

      exception code



   .. py:attribute:: flags
      :type:  int

      Exception info flags 
              



   .. py:method:: break_on() -> bool

      Should we break on the exception?



   .. py:method:: handle() -> bool

      Should we handle the exception?



   .. py:attribute:: name
      :type:  str

      Exception standard name.



   .. py:attribute:: desc
      :type:  str

      Long message used to display info about the exception.



.. py:data:: cvar

.. py:data:: BPT_WRITE

   Write access.


.. py:data:: BPT_READ

   Read access.


.. py:data:: BPT_RDWR

   Read/write access.


.. py:data:: BPT_SOFT

   Software breakpoint.


.. py:data:: BPT_EXEC

   Execute instruction.


.. py:data:: BPT_DEFAULT

   Choose bpt type automatically.


.. py:data:: EXC_BREAK

   break on the exception


.. py:data:: EXC_HANDLE

   should be handled by the debugger?


.. py:data:: EXC_MSG

   instead of a warning, log the exception to the output window


.. py:data:: EXC_SILENT

   do not warn or log to the output window


.. py:class:: regval_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: rvtype
      :type:  int

      one of Register value types



   .. py:attribute:: ival
      :type:  uint64

      RVT_INT.



   .. py:method:: use_bytevec() -> bool


   .. py:method:: clear() -> None

      Clear register value.



   .. py:method:: swap(r: regval_t) -> None

      Set this = r and r = this.



   .. py:method:: set_int(x: uint64) -> None


   .. py:method:: set_float(v: bytevec_t const &) -> None


   .. py:method:: set_bytes(*args) -> bytevec_t &


   .. py:method:: set_unavailable() -> None


   .. py:method:: bytes(*args) -> bytevec_t const &


   .. py:method:: get_data(*args) -> void const *


   .. py:method:: get_data_size() -> size_t


   .. py:method:: set_pyval(o: PyObject *, dtype: op_dtype_t) -> bool


   .. py:method:: pyval(dtype: op_dtype_t) -> PyObject *


.. py:data:: RVT_FLOAT

   floating point


.. py:data:: RVT_INT

   integer


.. py:data:: RVT_UNAVAILABLE

   unavailable; other values mean custom data type 
           


.. py:class:: call_stack_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: callea
      :type:  ida_idaapi.ea_t

      the address of the call instruction. for the 0th frame this is usually just the current value of EIP. 
              



   .. py:attribute:: funcea
      :type:  ida_idaapi.ea_t

      the address of the called function



   .. py:attribute:: fp
      :type:  ida_idaapi.ea_t

      the value of the frame pointer of the called function



   .. py:attribute:: funcok
      :type:  bool

      is the function present?



.. py:class:: call_stack_t

   Bases: :py:obj:`call_stack_info_vec_t`


   .. py:attribute:: thisown


.. py:function:: dbg_appcall(retval: idc_value_t *, func_ea: ida_idaapi.ea_t, tid: thid_t, ptif: tinfo_t, argv: idc_value_t *, argnum: size_t) -> error_t

   Call a function from the debugged application. 
           
   :param retval: function return value
   * for APPCALL_MANUAL, r will hold the new stack point value
   * for APPCALL_DEBEV, r will hold the exception information upon failure and the return code will be eExecThrow
   :param func_ea: address to call
   :param tid: thread to use. NO_THREAD means to use the current thread
   :param ptif: pointer to type of the function to call
   :param argv: array of arguments
   :param argnum: number of actual arguments
   :returns: eOk if successful, otherwise an error code


.. py:function:: cleanup_appcall(tid: thid_t) -> error_t

   Cleanup after manual appcall. 
           
   :param tid: thread to use. NO_THREAD means to use the current thread The application state is restored as it was before calling the last appcall(). Nested appcalls are supported.
   :returns: eOk if successful, otherwise an error code


.. py:class:: thread_name_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: tid
      :type:  thid_t

      thread



   .. py:attribute:: name
      :type:  str

      new thread name



.. py:data:: RESMOD_NONE

   no stepping, run freely


.. py:data:: RESMOD_INTO

   step into call (the most typical single stepping)


.. py:data:: RESMOD_OVER

   step over call


.. py:data:: RESMOD_OUT

   step out of the current function (run until return)


.. py:data:: RESMOD_SRCINTO

   until control reaches a different source line


.. py:data:: RESMOD_SRCOVER

   next source line in the current stack frame


.. py:data:: RESMOD_SRCOUT

   next source line in the previous stack frame


.. py:data:: RESMOD_USER

   step out to the user code


.. py:data:: RESMOD_HANDLE

   step into the exception handler


.. py:data:: RESMOD_BACKINTO

   step backwards into call (in time-travel debugging)


.. py:data:: RESMOD_MAX

.. py:data:: STEP_TRACE

   lowest level trace. trace buffers are not maintained


.. py:data:: INSN_TRACE

   instruction tracing


.. py:data:: FUNC_TRACE

   function tracing


.. py:data:: BBLK_TRACE

   basic block tracing


.. py:data:: DRC_EVENTS

   success, there are pending events


.. py:data:: DRC_CRC

   success, but the input file crc does not match


.. py:data:: DRC_OK

   success


.. py:data:: DRC_NONE

   reaction to the event not implemented


.. py:data:: DRC_FAILED

   failed or false


.. py:data:: DRC_NETERR

   network error


.. py:data:: DRC_NOFILE

   file not found


.. py:data:: DRC_IDBSEG

   use idb segmentation


.. py:data:: DRC_NOPROC

   the process does not exist anymore


.. py:data:: DRC_NOCHG

   no changes


.. py:data:: DRC_ERROR

   unclassified error, may be complemented by errbuf


.. py:class:: debugger_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: version
      :type:  int

      Expected kernel version, should be IDD_INTERFACE_VERSION 
              



   .. py:attribute:: name
      :type:  str

      Short debugger name like win32 or linux.



   .. py:attribute:: id
      :type:  int

      one of Debugger API module id



   .. py:attribute:: processor
      :type:  str

      Required processor name. Used for instant debugging to load the correct processor module 
              



   .. py:attribute:: flags
      :type:  uint64


   .. py:method:: is_remote() -> bool


   .. py:method:: must_have_hostname() -> bool


   .. py:method:: can_continue_from_bpt() -> bool


   .. py:method:: may_disturb() -> bool


   .. py:method:: is_safe() -> bool


   .. py:method:: use_sregs() -> bool


   .. py:method:: cache_block_size() -> size_t


   .. py:method:: use_memregs() -> bool


   .. py:method:: may_take_exit_snapshot() -> bool


   .. py:method:: virtual_threads() -> bool


   .. py:method:: supports_lowcnds() -> bool


   .. py:method:: supports_debthread() -> bool


   .. py:method:: can_debug_standalone_dlls() -> bool


   .. py:method:: fake_memory() -> bool


   .. py:method:: is_ttd() -> bool


   .. py:method:: has_get_processes() -> bool


   .. py:method:: has_attach_process() -> bool


   .. py:method:: has_detach_process() -> bool


   .. py:method:: has_request_pause() -> bool


   .. py:method:: has_set_exception_info() -> bool


   .. py:method:: has_thread_suspend() -> bool


   .. py:method:: has_thread_continue() -> bool


   .. py:method:: has_set_resume_mode() -> bool


   .. py:method:: has_thread_get_sreg_base() -> bool


   .. py:method:: has_check_bpt() -> bool


   .. py:method:: has_open_file() -> bool


   .. py:method:: has_update_call_stack() -> bool


   .. py:method:: has_appcall() -> bool


   .. py:method:: has_rexec() -> bool


   .. py:method:: has_map_address() -> bool


   .. py:method:: has_soft_bpt() -> bool


   .. py:attribute:: default_regclasses
      :type:  int

      Mask of default printed register classes.



   .. py:method:: regs(idx: int) -> register_info_t &


   .. py:attribute:: memory_page_size
      :type:  int

      Size of a memory page. Usually 4K.



   .. py:attribute:: bpt_size
      :type:  uchar

      Size of the software breakpoint instruction in bytes.



   .. py:attribute:: filetype
      :type:  uchar

      Input file type for the instant debugger. This value will be used after attaching to a new process. 
              



   .. py:attribute:: resume_modes
      :type:  ushort

      Resume modes 
              



   .. py:method:: is_resmod_avail(resmod: int) -> bool


   .. py:attribute:: ev_init_debugger

      Initialize debugger. This event is generated in the main thread. 
                



   .. py:attribute:: ev_term_debugger

      Terminate debugger. This event is generated in the main thread. 
                



   .. py:attribute:: ev_get_processes

      Return information about the running processes. This event is generated in the main thread. Available if DBG_HAS_GET_PROCESSES is set 
                



   .. py:attribute:: ev_start_process

      Start an executable to debug. This event is generated in debthread. Must be implemented. 
                



   .. py:attribute:: ev_attach_process

      Attach to an existing running process. event_id should be equal to -1 if not attaching to a crashed process. This event is generated in debthread. Available if DBG_HAS_ATTACH_PROCESS is set 
                



   .. py:attribute:: ev_detach_process

      Detach from the debugged process. May be generated while the process is running or suspended. Must detach from the process in any case. The kernel will repeatedly call get_debug_event() until PROCESS_DETACHED is received. In this mode, all other events will be automatically handled and process will be resumed. This event is generated from debthread. Available if DBG_HAS_DETACH_PROCESS is set 
                



   .. py:attribute:: ev_get_debapp_attrs

      Retrieve process- and debugger-specific runtime attributes. This event is generated in the main thread. 
                



   .. py:attribute:: ev_rebase_if_required_to

      Rebase database if the debugged program has been rebased by the system. This event is generated in the main thread. 
                



   .. py:attribute:: ev_request_pause

      Prepare to pause the process. Normally the next get_debug_event() will pause the process If the process is sleeping, then the pause will not occur until the process wakes up. If the debugger module does not react to this event, then it will be impossible to pause the program. This event is generated in debthread. Available if DBG_HAS_REQUEST_PAUSE is set 
                



   .. py:attribute:: ev_exit_process

      Stop the process. May be generated while the process is running or suspended. Must terminate the process in any case. The kernel will repeatedly call get_debug_event() until PROCESS_EXITED is received. In this mode, all other events will be automatically handled and process will be resumed. This event is generated in debthread. Must be implemented. 
                



   .. py:attribute:: ev_get_debug_event

      Get a pending debug event and suspend the process. This event will be generated regularly by IDA. This event is generated in debthread. IMPORTANT: the BREAKPOINT/EXCEPTION/STEP events must be reported only after reporting other pending events for a thread. Must be implemented. 
                



   .. py:attribute:: ev_resume

      Continue after handling the event. This event is generated in debthread. Must be implemented. 
                



   .. py:attribute:: ev_set_backwards

      Set whether the debugger should continue backwards or forwards. This event is generated in debthread. Available if DBG_FLAG_TTD is set 
                



   .. py:attribute:: ev_set_exception_info

      Set exception handling. This event is generated in debthread or the main thread. Available if DBG_HAS_SET_EXCEPTION_INFO is set 
                



   .. py:attribute:: ev_suspended

      This event will be generated by the kernel each time it has suspended the debuggee process and refreshed the database. The debugger module may add information to the database if necessary.
      The reason for introducing this event is that when an event like LOAD_DLL happens, the database does not reflect the memory state yet and therefore we can't add information about the dll into the database in the get_debug_event() function. Only when the kernel has adjusted the database we can do it. Example: for loaded PE DLLs we can add the exported function names to the list of debug names (see set_debug_names()).
      This event is generated in the main thread. 
                



   .. py:attribute:: ev_thread_suspend

      Suspend a running thread Available if DBG_HAS_THREAD_SUSPEND is set 
                



   .. py:attribute:: ev_thread_continue

      Resume a suspended thread Available if DBG_HAS_THREAD_CONTINUE is set 
                



   .. py:attribute:: ev_set_resume_mode

      Specify resume action Available if DBG_HAS_SET_RESUME_MODE is set 
                



   .. py:attribute:: ev_read_registers

      Read thread registers. This event is generated in debthread. Must be implemented. 
                



   .. py:attribute:: ev_write_register

      Write one thread register. This event is generated in debthread. Must be implemented. 
                



   .. py:attribute:: ev_thread_get_sreg_base

      Get information about the base of a segment register. Currently used by the IBM PC module to resolve references like fs:0. This event is generated in debthread. Available if DBG_HAS_THREAD_GET_SREG_BASE is set 
                



   .. py:attribute:: ev_get_memory_info

      Get information on the memory ranges. The debugger module fills 'ranges'. The returned vector must be sorted. This event is generated in debthread. Must be implemented. 
                



   .. py:attribute:: ev_read_memory

      Read process memory. This event is generated in debthread. 
                



   .. py:attribute:: ev_write_memory

      Write process memory. This event is generated in debthread. 
                



   .. py:attribute:: ev_check_bpt

      Is it possible to set breakpoint? This event is generated in debthread or in the main thread if debthread is not running yet. It is generated to verify hardware breakpoints. Available if DBG_HAS_CHECK_BPT is set 
                



   .. py:attribute:: ev_update_bpts

      Add/del breakpoints. bpts array contains nadd bpts to add, followed by ndel bpts to del. This event is generated in debthread. 
                



   .. py:attribute:: ev_update_lowcnds

      Update low-level (server side) breakpoint conditions. This event is generated in debthread. 
                



   .. py:attribute:: ev_open_file


   .. py:attribute:: ev_close_file


   .. py:attribute:: ev_read_file


   .. py:attribute:: ev_write_file


   .. py:attribute:: ev_map_address

      Map process address. The debugger module may ignore this event. This event is generated in debthread. IDA will generate this event only if DBG_HAS_MAP_ADDRESS is set. 
                



   .. py:attribute:: ev_get_debmod_extensions

      Get pointer to debugger specific events. This event returns a pointer to a structure that holds pointers to debugger module specific events. For information on the structure layout, please check the corresponding debugger module. Most debugger modules return nullptr because they do not have any extensions. Available extensions may be generated from plugins. This event is generated in the main thread. 
                



   .. py:attribute:: ev_update_call_stack

      Calculate the call stack trace for the given thread. This event is generated when the process is suspended and should fill the 'trace' object with the information about the current call stack. If this event returns DRC_NONE, IDA will try to invoke a processor-specific mechanism (see processor_t::ev_update_call_stack). If the current processor module does not implement stack tracing, then IDA will fall back to a generic algorithm (based on the frame pointer chain) to calculate the trace. This event is ideal if the debugging targets manage stack frames in a peculiar way, requiring special analysis. This event is generated in the main thread. Available if DBG_HAS_UPDATE_CALL_STACK is set 
                



   .. py:attribute:: ev_appcall

      Call application function. This event calls a function from the debugged application. This event is generated in debthread Available if HAS_APPCALL is set 
                



   .. py:attribute:: ev_cleanup_appcall

      Cleanup after appcall(). The debugger module must keep the stack blob in the memory until this event is generated. It will be generated by the kernel for each successful appcall(). There is an exception: if APPCALL_MANUAL, IDA may not call cleanup_appcall. If the user selects to terminate a manual appcall, then cleanup_appcall will be generated. Otherwise, the debugger module should terminate the appcall when the generated event returns. This event is generated in debthread. Available if HAS_APPCALL is set 
                



   .. py:attribute:: ev_eval_lowcnd

      Evaluate a low level breakpoint condition at 'ea'. Other evaluation errors are displayed in a dialog box. This call is used by IDA when the process has already been temporarily suspended for some reason and IDA has to decide whether the process should be resumed or definitely suspended because of a breakpoint with a low level condition. This event is generated in debthread. 
                



   .. py:attribute:: ev_send_ioctl

      Perform a debugger-specific event. This event is generated in debthread 
                



   .. py:attribute:: ev_dbg_enable_trace

      Enable/Disable tracing. The kernel will generated this event if the debugger plugin set DBG_FLAG_TRACER_MODULE. TRACE_FLAGS can be a set of STEP_TRACE, INSN_TRACE, BBLK_TRACE or FUNC_TRACE. This event is generated in the main thread. 
                



   .. py:attribute:: ev_is_tracing_enabled

      Is tracing enabled? The kernel will generated this event if the debugger plugin set DBG_FLAG_TRACER_MODULE. TRACE_BIT can be one of the following: STEP_TRACE, INSN_TRACE, BBLK_TRACE or FUNC_TRACE 
                



   .. py:attribute:: ev_rexec

      Execute a command on the remote computer. Available if DBG_HAS_REXEC is set 
                



   .. py:attribute:: ev_get_srcinfo_path

      Get the path to a file containing source debug info for the given module. This allows srcinfo providers to call into the debugger when looking for debug info. It is useful in certain cases like the iOS debugger, which is a remote debugger but the remote debugserver does not provide dwarf info. So, we allow the debugger client to decide where to look for debug info locally. 
                



   .. py:attribute:: ev_bin_search

      Search for a binary pattern in the program. 
                



   .. py:attribute:: ev_get_dynamic_register_set

      Ask debuger to send dynamic register set 
                



   .. py:attribute:: ev_set_dbg_options

      Set debugger options (parameters that are specific to the debugger module). 
                



   .. py:method:: init_debugger(hostname: str, portnum: int, password: str) -> bool


   .. py:method:: term_debugger() -> bool


   .. py:method:: get_processes(procs: procinfo_vec_t) -> drc_t


   .. py:method:: start_process(path: str, args: str, envs: launch_env_t, startdir: str, dbg_proc_flags: int, input_path: str, input_file_crc32: int) -> drc_t


   .. py:method:: attach_process(pid: pid_t, event_id: int, dbg_proc_flags: int) -> drc_t


   .. py:method:: detach_process() -> drc_t


   .. py:method:: get_debapp_attrs(out_pattrs: debapp_attrs_t) -> bool


   .. py:method:: rebase_if_required_to(new_base: ida_idaapi.ea_t) -> None


   .. py:method:: request_pause() -> drc_t


   .. py:method:: exit_process() -> drc_t


   .. py:method:: get_debug_event(event: debug_event_t, timeout_ms: int) -> gdecode_t


   .. py:method:: resume(event: debug_event_t) -> drc_t


   .. py:method:: set_backwards(backwards: bool) -> drc_t


   .. py:method:: set_exception_info(info: exception_info_t, qty: int) -> None


   .. py:method:: suspended(dlls_added: bool, thr_names: thread_name_vec_t * = None) -> None


   .. py:method:: thread_suspend(tid: thid_t) -> drc_t


   .. py:method:: thread_continue(tid: thid_t) -> drc_t


   .. py:method:: set_resume_mode(tid: thid_t, resmod: resume_mode_t) -> drc_t


   .. py:method:: read_registers(tid: thid_t, clsmask: int, values: regval_t) -> drc_t


   .. py:method:: write_register(tid: thid_t, regidx: int, value: regval_t) -> drc_t


   .. py:method:: thread_get_sreg_base(answer: ea_t *, tid: thid_t, sreg_value: int) -> drc_t


   .. py:method:: get_memory_info(ranges: meminfo_vec_t) -> drc_t


   .. py:method:: read_memory(nbytes: size_t *, ea: ida_idaapi.ea_t, buffer: void *, size: size_t) -> drc_t


   .. py:method:: write_memory(nbytes: size_t *, ea: ida_idaapi.ea_t, buffer: void const *, size: size_t) -> drc_t


   .. py:method:: check_bpt(bptvc: int *, type: bpttype_t, ea: ida_idaapi.ea_t, len: int) -> drc_t


   .. py:method:: update_bpts(nbpts: int *, bpts: update_bpt_info_t *, nadd: int, ndel: int) -> drc_t


   .. py:method:: update_lowcnds(nupdated: int *, lowcnds: lowcnd_t const *, nlowcnds: int) -> drc_t


   .. py:method:: open_file(file: str, fsize: uint64 *, readonly: bool) -> int


   .. py:method:: close_file(fn: int) -> None


   .. py:method:: read_file(fn: int, off: qoff64_t, buf: void *, size: size_t) -> ssize_t


   .. py:method:: write_file(fn: int, off: qoff64_t, buf: void const *) -> ssize_t


   .. py:method:: map_address(off: ida_idaapi.ea_t, regs: regval_t, regnum: int) -> ida_idaapi.ea_t


   .. py:method:: get_debmod_extensions() -> void const *


   .. py:method:: update_call_stack(tid: thid_t, trace: call_stack_t) -> drc_t


   .. py:method:: cleanup_appcall(tid: thid_t) -> drc_t


   .. py:method:: eval_lowcnd(tid: thid_t, ea: ida_idaapi.ea_t) -> drc_t


   .. py:method:: send_ioctl(fn: int, buf: void const *, poutbuf: void **, poutsize: ssize_t *) -> drc_t


   .. py:method:: dbg_enable_trace(tid: thid_t, enable: bool, trace_flags: int) -> bool


   .. py:method:: is_tracing_enabled(tid: thid_t, tracebit: int) -> bool


   .. py:method:: rexec(cmdline: str) -> int


   .. py:method:: get_srcinfo_path(path: str, base: ida_idaapi.ea_t) -> bool


   .. py:method:: bin_search(start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t, data: compiled_binpat_vec_t const &, srch_flags: int) -> drc_t


   .. py:method:: get_dynamic_register_set(regset: dynamic_register_set_t *) -> bool


   .. py:method:: have_set_options() -> bool


   .. py:attribute:: registers

      Array of registers. Use regs() to access it.



   .. py:attribute:: nregisters

      Number of registers.



   .. py:attribute:: regclasses

      Array of register class names.



   .. py:attribute:: bpt_bytes

      A software breakpoint instruction.



.. py:data:: DEBUGGER_ID_X86_IA32_WIN32_USER

   Userland win32 processes (win32 debugging APIs)


.. py:data:: DEBUGGER_ID_X86_IA32_LINUX_USER

   Userland linux processes (ptrace())


.. py:data:: DEBUGGER_ID_X86_IA32_MACOSX_USER

   Userland MAC OS X processes.


.. py:data:: DEBUGGER_ID_ARM_IPHONE_USER

   iPhone 1.x


.. py:data:: DEBUGGER_ID_X86_IA32_BOCHS

   BochsDbg.exe 32.


.. py:data:: DEBUGGER_ID_6811_EMULATOR

   MC6812 emulator (beta)


.. py:data:: DEBUGGER_ID_GDB_USER

   GDB remote.


.. py:data:: DEBUGGER_ID_WINDBG

   WinDBG using Microsoft Debug engine.


.. py:data:: DEBUGGER_ID_X86_DOSBOX_EMULATOR

   Dosbox MS-DOS emulator.


.. py:data:: DEBUGGER_ID_ARM_LINUX_USER

   Userland arm linux.


.. py:data:: DEBUGGER_ID_TRACE_REPLAYER

   Fake debugger to replay recorded traces.


.. py:data:: DEBUGGER_ID_X86_PIN_TRACER

   PIN Tracer module.


.. py:data:: DEBUGGER_ID_DALVIK_USER

   Dalvik.


.. py:data:: DEBUGGER_ID_XNU_USER

   XNU Kernel.


.. py:data:: DEBUGGER_ID_ARM_MACOS_USER

   Userland arm MAC OS.


.. py:data:: DBG_FLAG_REMOTE

   Remote debugger (requires remote host name unless DBG_FLAG_NOHOST)


.. py:data:: DBG_FLAG_NOHOST

   Remote debugger with does not require network params (host/port/pass). (a unique device connected to the machine) 
           


.. py:data:: DBG_FLAG_FAKE_ATTACH

   PROCESS_ATTACHED is a fake event and does not suspend the execution 
           


.. py:data:: DBG_FLAG_HWDATBPT_ONE

   Hardware data breakpoints are one byte size by default 
           


.. py:data:: DBG_FLAG_CAN_CONT_BPT

   Debugger knows to continue from a bpt. This flag also means that the debugger module hides breakpoints from ida upon read_memory 
           


.. py:data:: DBG_FLAG_NEEDPORT

   Remote debugger requires port number (to be used with DBG_FLAG_NOHOST)


.. py:data:: DBG_FLAG_DONT_DISTURB

   Debugger can handle only get_debug_event(), request_pause(), exit_process() when the debugged process is running. The kernel may also call service functions (file I/O, map_address, etc) 
           


.. py:data:: DBG_FLAG_SAFE

   The debugger is safe (probably because it just emulates the application without really running it) 
           


.. py:data:: DBG_FLAG_CLEAN_EXIT

   IDA must suspend the application and remove all breakpoints before terminating the application. Usually this is not required because the application memory disappears upon termination. 
           


.. py:data:: DBG_FLAG_USE_SREGS

   Take segment register values into account (non flat memory)


.. py:data:: DBG_FLAG_NOSTARTDIR

   Debugger module doesn't use startup directory.


.. py:data:: DBG_FLAG_NOPARAMETERS

   Debugger module doesn't use commandline parameters.


.. py:data:: DBG_FLAG_NOPASSWORD

   Remote debugger doesn't use password.


.. py:data:: DBG_FLAG_CONNSTRING

   Display "Connection string" instead of "Hostname" and hide the "Port" field.


.. py:data:: DBG_FLAG_SMALLBLKS

   If set, IDA uses 256-byte blocks for caching memory contents. Otherwise, 1024-byte blocks are used 
           


.. py:data:: DBG_FLAG_MANMEMINFO

   If set, manual memory region manipulation commands will be available. Use this bit for debugger modules that cannot return memory layout information 
           


.. py:data:: DBG_FLAG_EXITSHOTOK

   IDA may take a memory snapshot at PROCESS_EXITED event.


.. py:data:: DBG_FLAG_VIRTHREADS

   Thread IDs may be shuffled after each debug event. (to be used for virtual threads that represent cpus for windbg kmode) 
           


.. py:data:: DBG_FLAG_LOWCNDS

   Low level breakpoint conditions are supported.


.. py:data:: DBG_FLAG_DEBTHREAD

   Supports creation of a separate thread in ida for the debugger (the debthread). Most debugger functions will be called from debthread (exceptions are marked below) The debugger module may directly call only THREAD_SAFE functions. To call other functions please use execute_sync(). The debthread significantly increases debugging speed, especially if debug events occur frequently. 
           


.. py:data:: DBG_FLAG_DEBUG_DLL

   Can debug standalone DLLs. For example, Bochs debugger can debug any snippet of code 
           


.. py:data:: DBG_FLAG_FAKE_MEMORY

   get_memory_info()/read_memory()/write_memory() work with the idb. (there is no real process to read from, as for the replayer module) the kernel will not call these functions if this flag is set. however, third party plugins may call them, they must be implemented. 
           


.. py:data:: DBG_FLAG_ANYSIZE_HWBPT

   The debugger supports arbitrary size hardware breakpoints.


.. py:data:: DBG_FLAG_TRACER_MODULE

   The module is a tracer, not a full featured debugger module.


.. py:data:: DBG_FLAG_PREFER_SWBPTS

   Prefer to use software breakpoints.


.. py:data:: DBG_FLAG_LAZY_WATCHPTS

   Watchpoints are triggered before the offending instruction is executed. The debugger must temporarily disable the watchpoint and single-step before resuming. 
           


.. py:data:: DBG_FLAG_FAST_STEP

   Do not refresh memory layout info after single stepping.


.. py:data:: DBG_FLAG_ADD_ENVS

   The debugger supports launching processes with environment variables.


.. py:data:: DBG_FLAG_MERGE_ENVS

   The debugger supports merge or replace setting for environment variables (only makes sense if DBG_FLAG_ADD_ENVS is set) 
           


.. py:data:: DBG_FLAG_DISABLE_ASLR

   The debugger support ASLR disabling (Address space layout randomization) 
           


.. py:data:: DBG_FLAG_TTD

   The debugger is a time travel debugger and supports continuing backwards.


.. py:data:: DBG_FLAG_FULL_INSTR_BPT

   Setting a breakpoint in the middle of an instruction will also break.


.. py:data:: DBG_HAS_GET_PROCESSES

   supports ev_get_processes


.. py:data:: DBG_HAS_ATTACH_PROCESS

   supports ev_attach_process


.. py:data:: DBG_HAS_DETACH_PROCESS

   supports ev_detach_process


.. py:data:: DBG_HAS_REQUEST_PAUSE

   supports ev_request_pause


.. py:data:: DBG_HAS_SET_EXCEPTION_INFO

   supports ev_set_exception_info


.. py:data:: DBG_HAS_THREAD_SUSPEND

   supports ev_thread_suspend


.. py:data:: DBG_HAS_THREAD_CONTINUE

   supports ev_thread_continue


.. py:data:: DBG_HAS_SET_RESUME_MODE

   supports ev_set_resume_mode. Cannot be set inside the debugger_t::init_debugger() 
           


.. py:data:: DBG_HAS_THREAD_GET_SREG_BASE

   supports ev_thread_get_sreg_base


.. py:data:: DBG_HAS_CHECK_BPT

   supports ev_check_bpt


.. py:data:: DBG_HAS_OPEN_FILE

   supports ev_open_file, ev_close_file, ev_read_file, ev_write_file


.. py:data:: DBG_HAS_UPDATE_CALL_STACK

   supports ev_update_call_stack


.. py:data:: DBG_HAS_APPCALL

   supports ev_appcall, ev_cleanup_appcall


.. py:data:: DBG_HAS_REXEC

   supports ev_rexec


.. py:data:: DBG_HAS_MAP_ADDRESS

   supports ev_map_address. Avoid using this bit, especially together with DBG_FLAG_DEBTHREAD because it may cause big slow downs 
           


.. py:data:: DBG_RESMOD_STEP_INTO

   RESMOD_INTO is available


.. py:data:: DBG_RESMOD_STEP_OVER

   RESMOD_OVER is available


.. py:data:: DBG_RESMOD_STEP_OUT

   RESMOD_OUT is available


.. py:data:: DBG_RESMOD_STEP_SRCINTO

   RESMOD_SRCINTO is available


.. py:data:: DBG_RESMOD_STEP_SRCOVER

   RESMOD_SRCOVER is available


.. py:data:: DBG_RESMOD_STEP_SRCOUT

   RESMOD_SRCOUT is available


.. py:data:: DBG_RESMOD_STEP_USER

   RESMOD_USER is available


.. py:data:: DBG_RESMOD_STEP_HANDLE

   RESMOD_HANDLE is available


.. py:data:: DBG_RESMOD_STEP_BACKINTO

   RESMOD_BACKINTO is available


.. py:data:: DBG_PROC_IS_DLL

   database contains a dll (not exe)


.. py:data:: DBG_PROC_IS_GUI

   using gui version of ida


.. py:data:: DBG_PROC_32BIT

   application is 32-bit


.. py:data:: DBG_PROC_64BIT

   application is 64-bit


.. py:data:: DBG_NO_TRACE

   do not trace the application (mac/linux)


.. py:data:: DBG_HIDE_WINDOW

   application should be hidden on startup (windows)


.. py:data:: DBG_SUSPENDED

   application should be suspended on startup (mac)


.. py:data:: DBG_NO_ASLR

   disable ASLR (linux)


.. py:data:: BPT_OK

   breakpoint can be set


.. py:data:: BPT_INTERNAL_ERR

   interr occurred when verifying breakpoint


.. py:data:: BPT_BAD_TYPE

   bpt type is not supported


.. py:data:: BPT_BAD_ALIGN

   alignment is invalid


.. py:data:: BPT_BAD_ADDR

   ea is invalid


.. py:data:: BPT_BAD_LEN

   bpt len is invalid


.. py:data:: BPT_TOO_MANY

   reached max number of supported breakpoints


.. py:data:: BPT_READ_ERROR

   failed to read memory at bpt ea


.. py:data:: BPT_WRITE_ERROR

   failed to write memory at bpt ea


.. py:data:: BPT_SKIP

   update_bpts(): do not process bpt


.. py:data:: BPT_PAGE_OK

   update_bpts(): ok, added a page bpt


.. py:data:: APPCALL_MANUAL

   Only set up the appcall, do not run. debugger_t::cleanup_appcall will not be generated by ida! 
           


.. py:data:: APPCALL_DEBEV

   Return debug event information.


.. py:data:: APPCALL_TIMEOUT

   Appcall with timeout. If timed out, errbuf will contain "timeout". See SET_APPCALL_TIMEOUT and GET_APPCALL_TIMEOUT 
           


.. py:data:: RQ_MASKING

   masking step handler: unless errors, tmpbpt handlers won't be generated should be used only with request_internal_step() 
           


.. py:data:: RQ_SUSPEND

   suspending step handler: suspends the app handle_debug_event: suspends the app 
           


.. py:data:: RQ_NOSUSP

   running step handler: continues the app


.. py:data:: RQ_IGNWERR

   ignore breakpoint write failures


.. py:data:: RQ_SILENT

   all: no dialog boxes


.. py:data:: RQ_VERBOSE

   all: display dialog boxes


.. py:data:: RQ_SWSCREEN

   handle_debug_event: switch screens


.. py:data:: RQ__NOTHRRF

   handle_debug_event: do not refresh threads


.. py:data:: RQ_PROCEXIT

   snapshots: the process is exiting


.. py:data:: RQ_IDAIDLE

   handle_debug_event: ida is idle


.. py:data:: RQ_SUSPRUN

   handle_debug_event: suspend at PROCESS_STARTED


.. py:data:: RQ_RESUME

   handle_debug_event: resume application


.. py:data:: RQ_RESMOD

   resume_mode_t


.. py:data:: RQ_RESMOD_SHIFT

.. py:function:: cpu2ieee(ieee_out: fpvalue_t *, cpu_fpval: void const *, size: int) -> int

   Convert a floating point number in CPU native format to IDA's internal format. 
           
   :param ieee_out: output buffer
   :param cpu_fpval: floating point number in CPU native format
   :param size: size of cpu_fpval in bytes (size of the input buffer)
   :returns: Floating point/IEEE Conversion codes


.. py:function:: ieee2cpu(cpu_fpval_out: void *, ieee: fpvalue_t const &, size: int) -> int

   Convert a floating point number in IDA's internal format to CPU native format. 
           
   :param cpu_fpval_out: output buffer
   :param ieee: floating point number of IDA's internal format
   :param size: size of cpu_fpval in bytes (size of the output buffer)
   :returns: Floating point/IEEE Conversion codes


.. py:class:: dyn_register_info_array(_data: register_info_t, _count: size_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  register_info_t *


   .. py:attribute:: count
      :type:  size_t


.. py:function:: get_dbg() -> debugger_t *

.. py:function:: dbg_get_registers()

   This function returns the register definition from the currently loaded debugger.
   Basically, it returns an array of structure similar to to idd.hpp / register_info_t

   :returns: None if no debugger is loaded
   :returns: tuple(name, flags, class, dtype, bit_strings, default_bit_strings_mask)
             The bit_strings can be a tuple of strings or None (if the register does not have bit_strings)


.. py:function:: dbg_get_thread_sreg_base(tid, sreg_value)

   Returns the segment register base value

   :param tid: thread id
   :param sreg_value: segment register (selector) value
   :returns: The base as an 'ea', or None on failure


.. py:function:: dbg_read_memory(ea, sz)

   Reads from the debugee's memory at the specified ea

   :param ea: the debuggee's memory address
   :param sz: the amount of data to read
   :returns: The read buffer (as bytes), or None on failure


.. py:function:: dbg_write_memory(ea, buffer)

   Writes a buffer to the debugee's memory

   :param ea: the debuggee's memory address
   :param buf: a bytes object to write
   :returns: Boolean


.. py:function:: dbg_get_name()

   This function returns the current debugger's name.

   :returns: Debugger name or None if no debugger is active


.. py:function:: dbg_get_memory_info()

   This function returns the memory configuration of a debugged process.

   :returns: tuple(start_ea, end_ea, name, sclass, sbase, bitness, perm), or None if no debugger is active


.. py:function:: appcall(func_ea: ida_idaapi.ea_t, tid: thid_t, _type_or_none: bytevec_t const &, _fields: bytevec_t const &, arg_list: PyObject *) -> PyObject *

.. py:function:: get_event_module_name(ev: debug_event_t) -> str

.. py:function:: get_event_module_base(ev: debug_event_t) -> ida_idaapi.ea_t

.. py:function:: get_event_module_size(ev: debug_event_t) -> asize_t

.. py:function:: get_event_exc_info(ev: debug_event_t) -> str

.. py:function:: get_event_info(ev: debug_event_t) -> str

.. py:function:: get_event_bpt_hea(ev: debug_event_t) -> ida_idaapi.ea_t

.. py:function:: get_event_exc_code(ev: debug_event_t) -> uint

.. py:function:: get_event_exc_ea(ev: debug_event_t) -> ida_idaapi.ea_t

.. py:function:: can_exc_continue(ev: debug_event_t) -> bool

.. py:data:: NO_PROCESS
   :value: 4294967295


   No process.


.. py:data:: NO_THREAD
   :value: 0


   No thread. in PROCESS_STARTED this value can be used to specify that the main thread has not been created. It will be initialized later by a THREAD_STARTED event. 
           


.. py:data:: dbg_can_query

.. py:class:: Appcall_array__(tp)

   Bases: :py:obj:`object`


   This class is used with Appcall.array() method


   .. py:method:: pack(L)

      Packs a list or tuple into a byref buffer



   .. py:method:: try_to_convert_to_list(obj)

      Is this object a list? We check for the existance of attribute zero and attribute self.size-1



   .. py:method:: unpack(buf, as_list=True)

      Unpacks an array back into a list or an object



.. py:class:: Appcall_callable__(ea, tinfo_or_typestr=None, fields=None)

   Bases: :py:obj:`object`


   Helper class to issue appcalls using a natural syntax:
     appcall.FunctionNameInTheDatabase(arguments, ....)
   or
     appcall["Function@8"](arguments, ...)
   or
     f8 = appcall["Function@8"]
     f8(arg1, arg2, ...)
   or
     o = appcall.obj()
     i = byref(5)
     appcall.funcname(arg1, i, "hello", o)


   .. py:attribute:: timeout

      An Appcall instance can change its timeout value with this attribute



   .. py:attribute:: options

      Sets the Appcall options locally to this Appcall instance



   .. py:attribute:: ea

      Returns or sets the EA associated with this object



   .. py:attribute:: tif

      Returns the tinfo_t object



   .. py:attribute:: size

      Returns the size of the type



   .. py:attribute:: type

      Returns the typestring



   .. py:attribute:: fields

      Returns the field names



   .. py:method:: retrieve(src=None, flags=0)

      Unpacks a typed object from the database if an ea is given or from a string if a string was passed
      :param src: the address of the object or a string
      :returns: Returns a tuple of boolean and object or error number (Bool, Error | Object).



   .. py:method:: store(obj, dest_ea=None, base_ea=0, flags=0)

      Packs an object into a given ea if provided or into a string if no address was passed.
      :param obj: The object to pack
      :param dest_ea: If packing to idb this will be the store location
      :param base_ea: If packing to a buffer, this will be the base that will be used to relocate the pointers

      :returns: Tuple(Boolean, packed_string or error code) if packing to a string
      :returns: a return code is returned (0 indicating success) if packing to the database



.. py:class:: Appcall_consts__(default=None)

   Bases: :py:obj:`object`


   Helper class used by Appcall.Consts attribute
   It is used to retrieve constants via attribute access


.. py:class:: Appcall__

   Bases: :py:obj:`object`


   .. py:attribute:: APPCALL_MANUAL
      :value: 1


      Only set up the appcall, do not run. debugger_t::cleanup_appcall will not be generated by ida! 
              



   .. py:attribute:: APPCALL_DEBEV
      :value: 2


      Return debug event information.



   .. py:attribute:: APPCALL_TIMEOUT
      :value: 4


      Appcall with timeout. If timed out, errbuf will contain "timeout". See SET_APPCALL_TIMEOUT and GET_APPCALL_TIMEOUT 
              



   .. py:attribute:: Consts

      Use Appcall.Consts.CONST_NAME to access constants



   .. py:method:: proto(name_or_ea, proto_or_tinfo, flags=None)
      :staticmethod:


      Allows you to instantiate an appcall (callable object) with the desired prototype
      :param name_or_ea: The name of the function (will be resolved with LocByName())
      :param proto_or_tinfo: function prototype as a string or type of the function as tinfo_t object
      :returns: a callbable Appcall instance with the given prototypes and flags, or
                an exception if the prototype could not be parsed or the address is not resolvable.



   .. py:method:: valueof(name, default=0)
      :staticmethod:


      If the name could not be resolved then the default value will be returned

      :returns: the numeric value of a given name string.



   .. py:method:: int64(v)
      :staticmethod:


      Whenever a 64bit number is needed use this method to construct an object



   .. py:method:: byref(val)
      :staticmethod:


      Method to create references to immutable objects
      Currently we support references to int/strings
      Objects need not be passed by reference (this will be done automatically)



   .. py:method:: buffer(str=None, size=0, fill='\x00')
      :staticmethod:


      Creates a string buffer. The returned value (r) will be a byref object.
      Use r.value to get the contents and r.size to get the buffer's size



   .. py:method:: obj(**kwds)
      :staticmethod:


      Returns an empty object or objects with attributes as passed via its keywords arguments



   .. py:method:: cstr(val)
      :staticmethod:



   .. py:method:: UTF16(s)
      :staticmethod:



   .. py:attribute:: unicode


   .. py:method:: array(type_name)
      :staticmethod:


      Defines an array type. Later you need to pack() / unpack()



   .. py:method:: typedobj(typedecl_or_tinfo, ea=None)
      :staticmethod:


      Returns an appcall object for a type (can be given as tinfo_t object or
      as a string declaration)
      One can then use retrieve() member method
      :param ea: Optional parameter that later can be used to retrieve the type
      :returns: Appcall object or raises ValueError exception



   .. py:method:: set_appcall_options(opt)
      :staticmethod:


      Method to change the Appcall options globally (not per Appcall)



   .. py:method:: get_appcall_options()
      :staticmethod:


      Return the global Appcall options



   .. py:method:: cleanup_appcall(tid=0)
      :staticmethod:


      Cleanup after manual appcall. 
              
      :param tid: thread to use. NO_THREAD means to use the current thread The application state is restored as it was before calling the last appcall(). Nested appcalls are supported.
      :returns: eOk if successful, otherwise an error code



.. py:data:: Appcall


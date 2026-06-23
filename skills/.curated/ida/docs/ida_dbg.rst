ida_dbg
=======

.. py:module:: ida_dbg

.. autoapi-nested-parse::

   Contains functions to control the debugging of a process.

   See Debugger functions for a complete explanation of these functions.
   These functions are inlined for the kernel. They are not inlined for the user-interfaces. 
       



Attributes
----------

.. autoapisummary::

   ida_dbg.dbg_null
   ida_dbg.dbg_process_start
   ida_dbg.dbg_process_exit
   ida_dbg.dbg_process_attach
   ida_dbg.dbg_process_detach
   ida_dbg.dbg_thread_start
   ida_dbg.dbg_thread_exit
   ida_dbg.dbg_library_load
   ida_dbg.dbg_library_unload
   ida_dbg.dbg_information
   ida_dbg.dbg_exception
   ida_dbg.dbg_suspend_process
   ida_dbg.dbg_bpt
   ida_dbg.dbg_trace
   ida_dbg.dbg_request_error
   ida_dbg.dbg_step_into
   ida_dbg.dbg_step_over
   ida_dbg.dbg_run_to
   ida_dbg.dbg_step_until_ret
   ida_dbg.dbg_bpt_changed
   ida_dbg.dbg_started_loading_bpts
   ida_dbg.dbg_finished_loading_bpts
   ida_dbg.dbg_last
   ida_dbg.BPTEV_ADDED
   ida_dbg.BPTEV_REMOVED
   ida_dbg.BPTEV_CHANGED
   ida_dbg.DSTATE_SUSP
   ida_dbg.DSTATE_NOTASK
   ida_dbg.DSTATE_RUN
   ida_dbg.DBGINV_MEMORY
   ida_dbg.DBGINV_MEMCFG
   ida_dbg.DBGINV_REGS
   ida_dbg.DBGINV_ALL
   ida_dbg.DBGINV_REDRAW
   ida_dbg.DBGINV_NONE
   ida_dbg.MOVBPT_OK
   ida_dbg.MOVBPT_NOT_FOUND
   ida_dbg.MOVBPT_DEST_BUSY
   ida_dbg.MOVBPT_BAD_TYPE
   ida_dbg.BPLT_ABS
   ida_dbg.BPLT_REL
   ida_dbg.BPLT_SYM
   ida_dbg.BPLT_SRC
   ida_dbg.BPT_BRK
   ida_dbg.BPT_TRACE
   ida_dbg.BPT_UPDMEM
   ida_dbg.BPT_ENABLED
   ida_dbg.BPT_LOWCND
   ida_dbg.BPT_TRACEON
   ida_dbg.BPT_TRACE_INSN
   ida_dbg.BPT_TRACE_FUNC
   ida_dbg.BPT_TRACE_BBLK
   ida_dbg.BPT_TRACE_TYPES
   ida_dbg.BPT_ELANG_MASK
   ida_dbg.BPT_ELANG_SHIFT
   ida_dbg.BKPT_BADBPT
   ida_dbg.BKPT_LISTBPT
   ida_dbg.BKPT_TRACE
   ida_dbg.BKPT_ACTIVE
   ida_dbg.BKPT_PARTIAL
   ida_dbg.BKPT_CNDREADY
   ida_dbg.BKPT_FAKEPEND
   ida_dbg.BKPT_PAGE
   ida_dbg.BPTCK_NONE
   ida_dbg.BPTCK_NO
   ida_dbg.BPTCK_YES
   ida_dbg.BPTCK_ACT
   ida_dbg.ST_OVER_DEBUG_SEG
   ida_dbg.ST_OVER_LIB_FUNC
   ida_dbg.ST_ALREADY_LOGGED
   ida_dbg.ST_SKIP_LOOPS
   ida_dbg.ST_DIFFERENTIAL
   ida_dbg.ST_OPTIONS_MASK
   ida_dbg.ST_OPTIONS_DEFAULT
   ida_dbg.IT_LOG_SAME_IP
   ida_dbg.FT_LOG_RET
   ida_dbg.BT_LOG_INSTS
   ida_dbg.tev_none
   ida_dbg.tev_insn
   ida_dbg.tev_call
   ida_dbg.tev_ret
   ida_dbg.tev_bpt
   ida_dbg.tev_mem
   ida_dbg.tev_event
   ida_dbg.tev_max
   ida_dbg.SAVE_ALL_VALUES
   ida_dbg.SAVE_DIFF
   ida_dbg.SAVE_NONE
   ida_dbg.DEC_NOTASK
   ida_dbg.DEC_ERROR
   ida_dbg.DEC_TIMEOUT
   ida_dbg.WFNE_ANY
   ida_dbg.WFNE_SUSP
   ida_dbg.WFNE_SILENT
   ida_dbg.WFNE_CONT
   ida_dbg.WFNE_NOWAIT
   ida_dbg.WFNE_USEC
   ida_dbg.DOPT_SEGM_MSGS
   ida_dbg.DOPT_START_BPT
   ida_dbg.DOPT_THREAD_MSGS
   ida_dbg.DOPT_THREAD_BPT
   ida_dbg.DOPT_BPT_MSGS
   ida_dbg.DOPT_LIB_MSGS
   ida_dbg.DOPT_LIB_BPT
   ida_dbg.DOPT_INFO_MSGS
   ida_dbg.DOPT_INFO_BPT
   ida_dbg.DOPT_REAL_MEMORY
   ida_dbg.DOPT_REDO_STACK
   ida_dbg.DOPT_ENTRY_BPT
   ida_dbg.DOPT_EXCDLG
   ida_dbg.EXCDLG_NEVER
   ida_dbg.EXCDLG_UNKNOWN
   ida_dbg.EXCDLG_ALWAYS
   ida_dbg.DOPT_LOAD_DINFO
   ida_dbg.DOPT_END_BPT
   ida_dbg.DOPT_TEMP_HWBPT
   ida_dbg.DOPT_FAST_STEP
   ida_dbg.DOPT_DISABLE_ASLR
   ida_dbg.SRCIT_NONE
   ida_dbg.SRCIT_MODULE
   ida_dbg.SRCIT_FUNC
   ida_dbg.SRCIT_STMT
   ida_dbg.SRCIT_EXPR
   ida_dbg.SRCIT_STTVAR
   ida_dbg.SRCIT_LOCVAR
   ida_dbg.SRCDBG_PROV_VERSION
   ida_dbg.move_bpt_to_grp


Classes
-------

.. autoapisummary::

   ida_dbg.bpt_vec_t
   ida_dbg.tev_reg_values_t
   ida_dbg.tevinforeg_vec_t
   ida_dbg.memreg_infos_t
   ida_dbg.bptaddrs_t
   ida_dbg.bpt_location_t
   ida_dbg.bpt_t
   ida_dbg.tev_info_t
   ida_dbg.memreg_info_t
   ida_dbg.tev_reg_value_t
   ida_dbg.tev_info_reg_t
   ida_dbg.eval_ctx_t
   ida_dbg.DBG_Hooks


Functions
---------

.. autoapisummary::

   ida_dbg.run_to
   ida_dbg.request_run_to
   ida_dbg.run_requests
   ida_dbg.get_running_request
   ida_dbg.is_request_running
   ida_dbg.get_running_notification
   ida_dbg.clear_requests_queue
   ida_dbg.get_process_state
   ida_dbg.is_valid_dstate
   ida_dbg.set_process_state
   ida_dbg.invalidate_dbg_state
   ida_dbg.start_process
   ida_dbg.request_start_process
   ida_dbg.suspend_process
   ida_dbg.request_suspend_process
   ida_dbg.continue_process
   ida_dbg.request_continue_process
   ida_dbg.continue_backwards
   ida_dbg.request_continue_backwards
   ida_dbg.exit_process
   ida_dbg.request_exit_process
   ida_dbg.get_processes
   ida_dbg.attach_process
   ida_dbg.request_attach_process
   ida_dbg.detach_process
   ida_dbg.request_detach_process
   ida_dbg.is_debugger_busy
   ida_dbg.get_thread_qty
   ida_dbg.getn_thread
   ida_dbg.get_current_thread
   ida_dbg.getn_thread_name
   ida_dbg.select_thread
   ida_dbg.request_select_thread
   ida_dbg.suspend_thread
   ida_dbg.request_suspend_thread
   ida_dbg.resume_thread
   ida_dbg.request_resume_thread
   ida_dbg.get_first_module
   ida_dbg.get_next_module
   ida_dbg.step_into
   ida_dbg.request_step_into
   ida_dbg.step_over
   ida_dbg.request_step_over
   ida_dbg.step_into_backwards
   ida_dbg.request_step_into_backwards
   ida_dbg.step_over_backwards
   ida_dbg.request_step_over_backwards
   ida_dbg.run_to_backwards
   ida_dbg.request_run_to_backwards
   ida_dbg.step_until_ret
   ida_dbg.request_step_until_ret
   ida_dbg.set_resume_mode
   ida_dbg.request_set_resume_mode
   ida_dbg.get_dbg_reg_info
   ida_dbg.get_sp_val
   ida_dbg.get_ip_val
   ida_dbg.is_reg_integer
   ida_dbg.is_reg_float
   ida_dbg.is_reg_custom
   ida_dbg.set_bptloc_string
   ida_dbg.get_bptloc_string
   ida_dbg.get_bpt_qty
   ida_dbg.getn_bpt
   ida_dbg.get_bpt
   ida_dbg.exist_bpt
   ida_dbg.add_bpt
   ida_dbg.request_add_bpt
   ida_dbg.del_bpt
   ida_dbg.request_del_bpt
   ida_dbg.update_bpt
   ida_dbg.find_bpt
   ida_dbg.enable_bpt
   ida_dbg.disable_bpt
   ida_dbg.request_enable_bpt
   ida_dbg.request_disable_bpt
   ida_dbg.check_bpt
   ida_dbg.set_trace_size
   ida_dbg.clear_trace
   ida_dbg.request_clear_trace
   ida_dbg.is_step_trace_enabled
   ida_dbg.enable_step_trace
   ida_dbg.disable_step_trace
   ida_dbg.request_enable_step_trace
   ida_dbg.request_disable_step_trace
   ida_dbg.get_step_trace_options
   ida_dbg.set_step_trace_options
   ida_dbg.request_set_step_trace_options
   ida_dbg.is_insn_trace_enabled
   ida_dbg.enable_insn_trace
   ida_dbg.disable_insn_trace
   ida_dbg.request_enable_insn_trace
   ida_dbg.request_disable_insn_trace
   ida_dbg.get_insn_trace_options
   ida_dbg.set_insn_trace_options
   ida_dbg.request_set_insn_trace_options
   ida_dbg.is_func_trace_enabled
   ida_dbg.enable_func_trace
   ida_dbg.disable_func_trace
   ida_dbg.request_enable_func_trace
   ida_dbg.request_disable_func_trace
   ida_dbg.get_func_trace_options
   ida_dbg.set_func_trace_options
   ida_dbg.request_set_func_trace_options
   ida_dbg.enable_bblk_trace
   ida_dbg.disable_bblk_trace
   ida_dbg.request_enable_bblk_trace
   ida_dbg.request_disable_bblk_trace
   ida_dbg.is_bblk_trace_enabled
   ida_dbg.get_bblk_trace_options
   ida_dbg.set_bblk_trace_options
   ida_dbg.request_set_bblk_trace_options
   ida_dbg.get_tev_qty
   ida_dbg.get_tev_info
   ida_dbg.get_insn_tev_reg_val
   ida_dbg.get_insn_tev_reg_mem
   ida_dbg.get_insn_tev_reg_result
   ida_dbg.get_call_tev_callee
   ida_dbg.get_ret_tev_return
   ida_dbg.get_bpt_tev_ea
   ida_dbg.get_tev_memory_info
   ida_dbg.get_tev_event
   ida_dbg.get_trace_base_address
   ida_dbg.set_trace_base_address
   ida_dbg.dbg_add_thread
   ida_dbg.dbg_del_thread
   ida_dbg.dbg_add_tev
   ida_dbg.dbg_add_many_tevs
   ida_dbg.dbg_add_insn_tev
   ida_dbg.dbg_add_bpt_tev
   ida_dbg.dbg_add_call_tev
   ida_dbg.dbg_add_ret_tev
   ida_dbg.dbg_add_debug_event
   ida_dbg.load_trace_file
   ida_dbg.save_trace_file
   ida_dbg.is_valid_trace_file
   ida_dbg.set_trace_file_desc
   ida_dbg.get_trace_file_desc
   ida_dbg.choose_trace_file
   ida_dbg.diff_trace_file
   ida_dbg.graph_trace
   ida_dbg.set_highlight_trace_options
   ida_dbg.set_trace_platform
   ida_dbg.get_trace_platform
   ida_dbg.set_trace_dynamic_register_set
   ida_dbg.get_trace_dynamic_register_set
   ida_dbg.wait_for_next_event
   ida_dbg.get_debug_event
   ida_dbg.set_debugger_options
   ida_dbg.set_remote_debugger
   ida_dbg.get_process_options2
   ida_dbg.retrieve_exceptions
   ida_dbg.store_exceptions
   ida_dbg.define_exception
   ida_dbg.create_source_viewer
   ida_dbg.get_dbg_byte
   ida_dbg.put_dbg_byte
   ida_dbg.invalidate_dbgmem_config
   ida_dbg.invalidate_dbgmem_contents
   ida_dbg.is_debugger_on
   ida_dbg.is_debugger_memory
   ida_dbg.get_tev_ea
   ida_dbg.get_tev_type
   ida_dbg.get_tev_tid
   ida_dbg.bring_debugger_to_front
   ida_dbg.set_manual_regions
   ida_dbg.edit_manual_regions
   ida_dbg.enable_manual_regions
   ida_dbg.handle_debug_event
   ida_dbg.add_virt_module
   ida_dbg.del_virt_module
   ida_dbg.internal_ioctl
   ida_dbg.get_dbg_memory_info
   ida_dbg.set_bpt_group
   ida_dbg.set_bptloc_group
   ida_dbg.get_bpt_group
   ida_dbg.rename_bptgrp
   ida_dbg.del_bptgrp
   ida_dbg.get_grp_bpts
   ida_dbg.enable_bptgrp
   ida_dbg.get_local_vars
   ida_dbg.srcdbg_request_step_into
   ida_dbg.srcdbg_request_step_over
   ida_dbg.srcdbg_request_step_until_ret
   ida_dbg.hide_all_bpts
   ida_dbg.read_dbg_memory
   ida_dbg.get_module_info
   ida_dbg.dbg_bin_search
   ida_dbg.load_debugger
   ida_dbg.collect_stack_trace
   ida_dbg.get_global_var
   ida_dbg.get_local_var
   ida_dbg.get_srcinfo_provider
   ida_dbg.get_current_source_file
   ida_dbg.get_current_source_line
   ida_dbg.add_path_mapping
   ida_dbg.srcdbg_step_into
   ida_dbg.srcdbg_step_over
   ida_dbg.srcdbg_step_until_ret
   ida_dbg.set_debugger_event_cond
   ida_dbg.get_debugger_event_cond
   ida_dbg.set_process_options
   ida_dbg.get_process_options
   ida_dbg.get_manual_regions
   ida_dbg.dbg_is_loaded
   ida_dbg.refresh_debugger_memory
   ida_dbg.list_bptgrps
   ida_dbg.internal_get_sreg_base
   ida_dbg.write_dbg_memory
   ida_dbg.dbg_can_query
   ida_dbg.set_reg_val
   ida_dbg.request_set_reg_val
   ida_dbg.get_reg_val
   ida_dbg.get_reg_vals
   ida_dbg.get_tev_reg_val
   ida_dbg.get_tev_reg_mem_qty
   ida_dbg.get_tev_reg_mem
   ida_dbg.get_tev_reg_mem_ea
   ida_dbg.send_dbg_command


Module Contents
---------------

.. py:class:: bpt_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> bpt_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> bpt_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: bpt_vec_t) -> None


   .. py:method:: extract() -> bpt_t *


   .. py:method:: inject(s: bpt_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< bpt_t >::const_iterator


   .. py:method:: end(*args) -> qvector< bpt_t >::const_iterator


   .. py:method:: insert(it: bpt_t, x: bpt_t) -> qvector< bpt_t >::iterator


   .. py:method:: erase(*args) -> qvector< bpt_t >::iterator


   .. py:method:: append(x: bpt_t) -> None


   .. py:method:: extend(x: bpt_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: tev_reg_values_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> tev_reg_value_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> tev_reg_value_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: tev_reg_values_t) -> None


   .. py:method:: extract() -> tev_reg_value_t *


   .. py:method:: inject(s: tev_reg_value_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< tev_reg_value_t >::const_iterator


   .. py:method:: end(*args) -> qvector< tev_reg_value_t >::const_iterator


   .. py:method:: insert(it: tev_reg_value_t, x: tev_reg_value_t) -> qvector< tev_reg_value_t >::iterator


   .. py:method:: erase(*args) -> qvector< tev_reg_value_t >::iterator


   .. py:method:: append(x: tev_reg_value_t) -> None


   .. py:method:: extend(x: tev_reg_values_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: tevinforeg_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> tev_info_reg_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> tev_info_reg_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: tevinforeg_vec_t) -> None


   .. py:method:: extract() -> tev_info_reg_t *


   .. py:method:: inject(s: tev_info_reg_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< tev_info_reg_t >::const_iterator


   .. py:method:: end(*args) -> qvector< tev_info_reg_t >::const_iterator


   .. py:method:: insert(it: tev_info_reg_t, x: tev_info_reg_t) -> qvector< tev_info_reg_t >::iterator


   .. py:method:: erase(*args) -> qvector< tev_info_reg_t >::iterator


   .. py:method:: append(x: tev_info_reg_t) -> None


   .. py:method:: extend(x: tevinforeg_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: memreg_infos_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> memreg_info_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> memreg_info_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: memreg_infos_t) -> None


   .. py:method:: extract() -> memreg_info_t *


   .. py:method:: inject(s: memreg_info_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< memreg_info_t >::const_iterator


   .. py:method:: end(*args) -> qvector< memreg_info_t >::const_iterator


   .. py:method:: insert(it: memreg_info_t, x: memreg_info_t) -> qvector< memreg_info_t >::iterator


   .. py:method:: erase(*args) -> qvector< memreg_info_t >::iterator


   .. py:method:: append(x: memreg_info_t) -> None


   .. py:method:: extend(x: memreg_infos_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:function:: run_to(*args) -> bool

   Execute the process until the given address is reached. If no process is active, a new process is started. Technically, the debugger sets up a temporary breakpoint at the given address, and continues (or starts) the execution of the whole process. So, all threads continue their execution! \sq{Type, Asynchronous function - available as Request, Notification, dbg_run_to} 
           
   :param ea: target address
   :param pid: not used yet. please do not specify this parameter.
   :param tid: not used yet. please do not specify this parameter.


.. py:function:: request_run_to(*args) -> bool

   Post a run_to() request.


.. py:data:: dbg_null

.. py:data:: dbg_process_start

.. py:data:: dbg_process_exit

.. py:data:: dbg_process_attach

.. py:data:: dbg_process_detach

.. py:data:: dbg_thread_start

.. py:data:: dbg_thread_exit

.. py:data:: dbg_library_load

.. py:data:: dbg_library_unload

.. py:data:: dbg_information

.. py:data:: dbg_exception

.. py:data:: dbg_suspend_process

   The process is now suspended. 
             


.. py:data:: dbg_bpt

   A user defined breakpoint was reached. 
             


.. py:data:: dbg_trace

   A step occurred (one instruction was executed). This event notification is only generated if step tracing is enabled. 
             


.. py:data:: dbg_request_error

   An error occurred during the processing of a request. 
             


.. py:data:: dbg_step_into

.. py:data:: dbg_step_over

.. py:data:: dbg_run_to

.. py:data:: dbg_step_until_ret

.. py:data:: dbg_bpt_changed

   Breakpoint has been changed. 
             


.. py:data:: dbg_started_loading_bpts

   Started loading breakpoint info from idb.


.. py:data:: dbg_finished_loading_bpts

   Finished loading breakpoint info from idb.


.. py:data:: dbg_last

   The last debugger notification code.


.. py:data:: BPTEV_ADDED

   Breakpoint has been added.


.. py:data:: BPTEV_REMOVED

   Breakpoint has been removed.


.. py:data:: BPTEV_CHANGED

   Breakpoint has been modified.


.. py:function:: run_requests() -> bool

   Execute requests until all requests are processed or an asynchronous function is called. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :returns: false if not all requests could be processed (indicates an asynchronous function was started)


.. py:function:: get_running_request() -> ui_notification_t

   Get the current running request. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :returns: ui_null if no running request


.. py:function:: is_request_running() -> bool

   Is a request currently running?


.. py:function:: get_running_notification() -> dbg_notification_t

   Get the notification associated (if any) with the current running request. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :returns: dbg_null if no running request


.. py:function:: clear_requests_queue() -> None

   Clear the queue of waiting requests. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: get_process_state() -> int

   Return the state of the currently debugged process. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :returns: one of Debugged process states


.. py:data:: DSTATE_SUSP

   process is suspended and will not continue


.. py:data:: DSTATE_NOTASK

   no process is currently debugged


.. py:data:: DSTATE_RUN

   process is running


.. py:function:: is_valid_dstate(state: int) -> bool

.. py:data:: DBGINV_MEMORY

   invalidate cached memory contents


.. py:data:: DBGINV_MEMCFG

   invalidate cached process segmentation


.. py:data:: DBGINV_REGS

   invalidate cached register values


.. py:data:: DBGINV_ALL

   invalidate everything


.. py:data:: DBGINV_REDRAW

   refresh the screen


.. py:data:: DBGINV_NONE

   invalidate nothing


.. py:function:: set_process_state(newstate: int, p_thid: thid_t *, dbginv: int) -> int

   Set new state for the debugged process. Notifies the IDA kernel about the change of the debugged process state. For example, a debugger module could call this function when it knows that the process is suspended for a short period of time. Some IDA API calls can be made only when the process is suspended. The process state is usually restored before returning control to the caller. You must know that it is ok to change the process state, doing it at arbitrary moments may crash the application or IDA. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param newstate: new process state (one of Debugged process states) if DSTATE_NOTASK is passed then the state is not changed
   :param p_thid: ptr to new thread id. may be nullptr or pointer to NO_THREAD. the pointed variable will contain the old thread id upon return
   :param dbginv: Debugged process invalidation options
   :returns: old debugger state (one of Debugged process states)


.. py:function:: invalidate_dbg_state(dbginv: int) -> int

   Invalidate cached debugger information. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param dbginv: Debugged process invalidation options
   :returns: current debugger state (one of Debugged process states)


.. py:function:: start_process(path: str = None, args: str = None, sdir: str = None) -> int

   Start a process in the debugger. \sq{Type, Asynchronous function - available as Request, Notification, dbg_process_start} 
           
   :param path: path to the executable to start
   :param args: arguments to pass to process
   :param sdir: starting directory for the process
   :returns: -1: impossible to create the process
   :returns: 0: the starting of the process was cancelled by the user
   :returns: 1: the process was properly started


.. py:function:: request_start_process(path: str = None, args: str = None, sdir: str = None) -> int

   Post a start_process() request.


.. py:function:: suspend_process() -> bool

   Suspend the process in the debugger. \sq{ Type,
   * Synchronous function (if in a notification handler)
   * Asynchronous function (everywhere else)
   * available as Request, Notification,
   * none (if in a notification handler)
   * dbg_suspend_process (everywhere else) }



.. py:function:: request_suspend_process() -> bool

   Post a suspend_process() request.


.. py:function:: continue_process() -> bool

   Continue the execution of the process in the debugger. \sq{Type, Synchronous function - available as Request, Notification, none (synchronous function)} 
           


.. py:function:: request_continue_process() -> bool

   Post a continue_process() request. 
           


.. py:function:: continue_backwards() -> bool

   Continue the execution of the process in the debugger backwards. Can only be used with debuggers that support time-travel debugging. \sq{Type, Synchronous function - available as Request, Notification, none (synchronous function)} 
           


.. py:function:: request_continue_backwards() -> bool

   Post a continue_backwards() request. 
           


.. py:function:: exit_process() -> bool

   Terminate the debugging of the current process. \sq{Type, Asynchronous function - available as Request, Notification, dbg_process_exit} 
           


.. py:function:: request_exit_process() -> bool

   Post an exit_process() request.


.. py:function:: get_processes(proclist: procinfo_vec_t) -> ssize_t

   Take a snapshot of running processes and return their description. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param proclist: array with information about each running process
   :returns: number of processes or -1 on error


.. py:function:: attach_process(*args) -> int

   Attach the debugger to a running process. \sq{Type, Asynchronous function - available as Request, Notification, dbg_process_attach} 
           
   :param pid: PID of the process to attach to. If NO_PROCESS, a dialog box will interactively ask the user for the process to attach to.
   :param event_id: event to trigger upon attaching
   :returns: -4: debugger was not inited
   :returns: -3: the attaching is not supported
   :returns: -2: impossible to find a compatible process
   :returns: -1: impossible to attach to the given process (process died, privilege needed, not supported by the debugger plugin, ...)
   :returns: 0: the user cancelled the attaching to the process
   :returns: 1: the debugger properly attached to the process


.. py:function:: request_attach_process(pid: pid_t, event_id: int) -> int

   Post an attach_process() request.


.. py:function:: detach_process() -> bool

   Detach the debugger from the debugged process. \sq{Type, Asynchronous function - available as Request, Notification, dbg_process_detach} 
           


.. py:function:: request_detach_process() -> bool

   Post a detach_process() request.


.. py:function:: is_debugger_busy() -> bool

   Is the debugger busy?. Some debuggers do not accept any commands while the debugged application is running. For such a debugger, it is unsafe to do anything with the database (even simple queries like get_byte may lead to undesired consequences). Returns: true if the debugged application is running under such a debugger 
           


.. py:function:: get_thread_qty() -> int

   Get number of threads. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: getn_thread(n: int) -> thid_t

   Get the ID of a thread. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of thread, is in range 0..get_thread_qty()-1
   :returns: NO_THREAD if the thread doesn't exist.


.. py:function:: get_current_thread() -> thid_t

   Get current thread ID. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: getn_thread_name(n: int) -> str

   Get the NAME of a thread \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of thread, is in range 0..get_thread_qty()-1 or -1 for the current thread
   :returns: thread name or nullptr if the thread doesn't exist.


.. py:function:: select_thread(tid: thid_t) -> bool

   Select the given thread as the current debugged thread. All thread related execution functions will work on this thread. The process must be suspended to select a new thread. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           
   :param tid: ID of the thread to select
   :returns: false if the thread doesn't exist.


.. py:function:: request_select_thread(tid: thid_t) -> bool

   Post a select_thread() request.


.. py:function:: suspend_thread(tid: thid_t) -> int

   Suspend thread. Suspending a thread may deadlock the whole application if the suspended was owning some synchronization objects. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           
   :param tid: thread id
   :returns: -1: network error
   :returns: 0: failed
   :returns: 1: ok


.. py:function:: request_suspend_thread(tid: thid_t) -> int

   Post a suspend_thread() request.


.. py:function:: resume_thread(tid: thid_t) -> int

   Resume thread. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           
   :param tid: thread id
   :returns: -1: network error
   :returns: 0: failed
   :returns: 1: ok


.. py:function:: request_resume_thread(tid: thid_t) -> int

   Post a resume_thread() request.


.. py:function:: get_first_module(modinfo: modinfo_t) -> bool

.. py:function:: get_next_module(modinfo: modinfo_t) -> bool

.. py:function:: step_into() -> bool

   Execute one instruction in the current thread. Other threads are kept suspended. \sq{Type, Asynchronous function - available as Request, Notification, dbg_step_into} 
           


.. py:function:: request_step_into() -> bool

   Post a step_into() request.


.. py:function:: step_over() -> bool

   Execute one instruction in the current thread, but without entering into functions. Others threads keep suspended. \sq{Type, Asynchronous function - available as Request, Notification, dbg_step_over} 
           


.. py:function:: request_step_over() -> bool

   Post a step_over() request.


.. py:function:: step_into_backwards() -> bool

   Execute one instruction backwards in the current thread. Other threads are kept suspended. \sq{Type, Asynchronous function - available as Request, Notification, dbg_step_into} 
           


.. py:function:: request_step_into_backwards() -> bool

   Post a step_into_backwards() request.


.. py:function:: step_over_backwards() -> bool

   Execute one instruction backwards in the current thread, but without entering into functions. Other threads are kept suspended. \sq{Type, Asynchronous function - available as Request, Notification, dbg_step_over} 
           


.. py:function:: request_step_over_backwards() -> bool

   Post a step_over_backwards() request.


.. py:function:: run_to_backwards(*args) -> bool

   Execute the process backwards until the given address is reached. Technically, the debugger sets up a temporary breakpoint at the given address, and continues (or starts) the execution of the whole process. \sq{Type, Asynchronous function - available as Request, Notification, dbg_run_to} 
           
   :param ea: target address
   :param pid: not used yet. please do not specify this parameter.
   :param tid: not used yet. please do not specify this parameter.


.. py:function:: request_run_to_backwards(*args) -> bool

   Post a run_to_backwards() request.


.. py:function:: step_until_ret() -> bool

   Execute instructions in the current thread until a function return instruction is executed (aka "step out"). Other threads are kept suspended. \sq{Type, Asynchronous function - available as Request, Notification, dbg_step_until_ret} 
           


.. py:function:: request_step_until_ret() -> bool

   Post a step_until_ret() request.


.. py:function:: set_resume_mode(tid: thid_t, mode: resume_mode_t) -> bool

   How to resume the application. Set resume mode but do not resume process. 
           


.. py:function:: request_set_resume_mode(tid: thid_t, mode: resume_mode_t) -> bool

   Post a set_resume_mode() request.


.. py:function:: get_dbg_reg_info(regname: str, ri: register_info_t) -> bool

   Get register information \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: get_sp_val() -> uint64 *

   Get value of the SP register for the current thread. Requires a suspended debugger. 
           


.. py:function:: get_ip_val() -> uint64 *

   Get value of the IP (program counter) register for the current thread. Requires a suspended debugger. 
           


.. py:function:: is_reg_integer(regname: str) -> bool

   Does a register contain an integer value? \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: is_reg_float(regname: str) -> bool

   Does a register contain a floating point value? \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: is_reg_custom(regname: str) -> bool

   Does a register contain a value of a custom data type? \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: set_bptloc_string(s: str) -> int

.. py:function:: get_bptloc_string(i: int) -> str

.. py:data:: MOVBPT_OK

   moved ok


.. py:data:: MOVBPT_NOT_FOUND

   source bpt not found


.. py:data:: MOVBPT_DEST_BUSY

   destination location is busy (we already have such a bpt)


.. py:data:: MOVBPT_BAD_TYPE

   BPLT_ABS is not supported.


.. py:class:: bptaddrs_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: bpt
      :type:  bpt_t *


.. py:data:: BPLT_ABS

   absolute address: ea


.. py:data:: BPLT_REL

   relative address: module_path, offset


.. py:data:: BPLT_SYM

   symbolic: symbol_name, offset


.. py:data:: BPLT_SRC

   source level: filename, lineno


.. py:class:: bpt_location_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: info
      :type:  ida_idaapi.ea_t


   .. py:attribute:: index
      :type:  int


   .. py:attribute:: loctype
      :type:  bpt_loctype_t


   .. py:method:: type() -> bpt_loctype_t

      Get bpt type.



   .. py:method:: is_empty_path() -> bool

      No path/filename specified? (BPLT_REL, BPLT_SRC)



   .. py:method:: path() -> str

      Get path/filename (BPLT_REL, BPLT_SRC)



   .. py:method:: symbol() -> str

      Get symbol name (BPLT_SYM)



   .. py:method:: lineno() -> int

      Get line number (BPLT_SRC)



   .. py:method:: offset() -> int

      Get offset (BPLT_REL, BPLT_SYM)



   .. py:method:: ea() -> ida_idaapi.ea_t

      Get address (BPLT_ABS)



   .. py:method:: set_abs_bpt(a: ida_idaapi.ea_t) -> None

      Specify an absolute address location.



   .. py:method:: set_src_bpt(fn: str, _lineno: int) -> None

      Specify a source level location.



   .. py:method:: set_sym_bpt(_symbol: str, _offset: int = 0) -> None

      Specify a symbolic location.



   .. py:method:: set_rel_bpt(mod: str, _offset: int) -> None

      Specify a relative address location.



   .. py:method:: compare(r: bpt_location_t) -> int

      Lexically compare two breakpoint locations. Bpt locations are first compared based on type (i.e. BPLT_ABS < BPLT_REL). BPLT_ABS locations are compared based on their ea values. For all other location types, locations are first compared based on their string (path/filename/symbol), then their offset/lineno. 
              



.. py:class:: bpt_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: cb
      :type:  size_t

      size of this structure



   .. py:attribute:: loc
      :type:  bpt_location_t

      Location.



   .. py:attribute:: pid
      :type:  pid_t

      breakpoint process id



   .. py:attribute:: tid
      :type:  thid_t

      breakpoint thread id



   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      Address, if known. For BPLT_SRC, index into an internal data struct.



   .. py:attribute:: type
      :type:  bpttype_t

      Breakpoint type.



   .. py:attribute:: pass_count
      :type:  int

      Number of times the breakpoint is hit before stopping (default is 0: stop always) 
              



   .. py:attribute:: flags
      :type:  int

      Breakpoint property bits 
              



   .. py:attribute:: props
      :type:  int

      Internal breakpoint properties 
              



   .. py:attribute:: size
      :type:  int

      Size of the breakpoint (0 for software breakpoints)



   .. py:attribute:: cndidx
      :type:  int

      Internal number of the condition (<0-none)



   .. py:attribute:: bptid
      :type:  inode_t

      Internal breakpoint id.



   .. py:method:: is_hwbpt() -> bool

      Is hardware breakpoint?



   .. py:method:: enabled() -> bool

      Is breakpoint enabled?



   .. py:method:: is_low_level() -> bool

      Is bpt condition calculated at low level?



   .. py:method:: badbpt() -> bool

      Failed to write bpt to process memory?



   .. py:method:: listbpt() -> bool

      Include in the bpt list?



   .. py:method:: is_compiled() -> bool

      Condition has been compiled? 
              



   .. py:method:: is_active() -> bool

      Written completely to process?



   .. py:method:: is_partially_active() -> bool

      Written partially to process?



   .. py:method:: is_inactive() -> bool

      Not written to process at all?



   .. py:method:: is_page_bpt() -> bool

      Page breakpoint?



   .. py:method:: get_size() -> int

      Get bpt size.



   .. py:method:: set_abs_bpt(a: ida_idaapi.ea_t) -> None

      Set bpt location to an absolute address.



   .. py:method:: set_src_bpt(fn: str, lineno: int) -> None

      Set bpt location to a source line.



   .. py:method:: set_sym_bpt(sym: str, o: int) -> None

      Set bpt location to a symbol.



   .. py:method:: set_rel_bpt(mod: str, o: int) -> None

      Set bpt location to a relative address.



   .. py:method:: is_absbpt() -> bool

      Is absolute address breakpoint?



   .. py:method:: is_relbpt() -> bool

      Is relative address breakpoint?



   .. py:method:: is_symbpt() -> bool

      Is symbolic breakpoint?



   .. py:method:: is_srcbpt() -> bool

      Is source level breakpoint?



   .. py:method:: is_tracemodebpt() -> bool

      Does breakpoint trace anything?



   .. py:method:: is_traceonbpt() -> bool

      Is this a tracing breakpoint, and is tracing enabled?



   .. py:method:: is_traceoffbpt() -> bool

      Is this a tracing breakpoint, and is tracing disabled?



   .. py:method:: set_trace_action(enable: bool, trace_types: int) -> bool

      Configure tracing options.



   .. py:method:: get_cnd_elang_idx() -> size_t


   .. py:attribute:: condition
      :type:  PyObject *


   .. py:attribute:: elang
      :type:  PyObject *


.. py:data:: BPT_BRK

   suspend execution upon hit


.. py:data:: BPT_TRACE

   add trace information upon hit


.. py:data:: BPT_UPDMEM

   refresh the memory layout and contents before evaluating bpt condition


.. py:data:: BPT_ENABLED

   enabled?


.. py:data:: BPT_LOWCND

   condition is calculated at low level (on the server side)


.. py:data:: BPT_TRACEON

   enable tracing when the breakpoint is reached


.. py:data:: BPT_TRACE_INSN

   instruction tracing


.. py:data:: BPT_TRACE_FUNC

   function tracing


.. py:data:: BPT_TRACE_BBLK

   basic block tracing


.. py:data:: BPT_TRACE_TYPES

   trace insns, functions, and basic blocks. if any of BPT_TRACE_TYPES bits are set but BPT_TRACEON is clear, then turn off tracing for the specified trace types 
           


.. py:data:: BPT_ELANG_MASK

.. py:data:: BPT_ELANG_SHIFT

   index of the extlang (scripting language) of the condition


.. py:data:: BKPT_BADBPT

   failed to write the bpt to the process memory (at least one location)


.. py:data:: BKPT_LISTBPT

   include in bpt list (user-defined bpt)


.. py:data:: BKPT_TRACE

   trace bpt; should not be deleted when the process gets suspended


.. py:data:: BKPT_ACTIVE

   active?


.. py:data:: BKPT_PARTIAL

   partially active? (some locations were not written yet)


.. py:data:: BKPT_CNDREADY

   condition has been compiled


.. py:data:: BKPT_FAKEPEND

   fake pending bpt: it is inactive but another bpt of the same type is active at the same address(es) 
           


.. py:data:: BKPT_PAGE

   written to the process as a page bpt. Available only after writing the bpt to the process. 
           


.. py:function:: get_bpt_qty() -> int

   Get number of breakpoints. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: getn_bpt(n: int, bpt: bpt_t) -> bool

   Get the characteristics of a breakpoint. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of breakpoint, is in range 0..get_bpt_qty()-1
   :param bpt: filled with the characteristics.
   :returns: false if no breakpoint exists


.. py:function:: get_bpt(ea: ida_idaapi.ea_t, bpt: bpt_t) -> bool

   Get the characteristics of a breakpoint. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param ea: any address in the breakpoint range
   :param bpt: if not nullptr, is filled with the characteristics.
   :returns: false if no breakpoint exists


.. py:function:: exist_bpt(ea: ida_idaapi.ea_t) -> bool

   Does a breakpoint exist at the given location?


.. py:function:: add_bpt(*args) -> bool

   This function has the following signatures:

       0. add_bpt(ea: ida_idaapi.ea_t, size: asize_t=0, type: bpttype_t=BPT_DEFAULT) -> bool
       1. add_bpt(bpt: const bpt_t &) -> bool

   # 0: add_bpt(ea: ida_idaapi.ea_t, size: asize_t=0, type: bpttype_t=BPT_DEFAULT) -> bool

   Add a new breakpoint in the debugged process. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           

   # 1: add_bpt(bpt: const bpt_t &) -> bool

   Add a new breakpoint in the debugged process. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           


.. py:function:: request_add_bpt(*args) -> bool

   This function has the following signatures:

       0. request_add_bpt(ea: ida_idaapi.ea_t, size: asize_t=0, type: bpttype_t=BPT_DEFAULT) -> bool
       1. request_add_bpt(bpt: const bpt_t &) -> bool

   # 0: request_add_bpt(ea: ida_idaapi.ea_t, size: asize_t=0, type: bpttype_t=BPT_DEFAULT) -> bool

   Post an add_bpt(ea_t, asize_t, bpttype_t) request.


   # 1: request_add_bpt(bpt: const bpt_t &) -> bool

   Post an add_bpt(const bpt_t &) request.


.. py:function:: del_bpt(*args) -> bool

   This function has the following signatures:

       0. del_bpt(ea: ida_idaapi.ea_t) -> bool
       1. del_bpt(bptloc: const bpt_location_t &) -> bool

   # 0: del_bpt(ea: ida_idaapi.ea_t) -> bool

   Delete an existing breakpoint in the debugged process. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           

   # 1: del_bpt(bptloc: const bpt_location_t &) -> bool

   Delete an existing breakpoint in the debugged process. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           


.. py:function:: request_del_bpt(*args) -> bool

   This function has the following signatures:

       0. request_del_bpt(ea: ida_idaapi.ea_t) -> bool
       1. request_del_bpt(bptloc: const bpt_location_t &) -> bool

   # 0: request_del_bpt(ea: ida_idaapi.ea_t) -> bool

   Post a del_bpt(ea_t) request.


   # 1: request_del_bpt(bptloc: const bpt_location_t &) -> bool

   Post a del_bpt(const bpt_location_t &) request.


.. py:function:: update_bpt(bpt: bpt_t) -> bool

   Update modifiable characteristics of an existing breakpoint. To update the breakpoint location, use change_bptlocs() \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: find_bpt(bptloc: bpt_location_t, bpt: bpt_t) -> bool

   Find a breakpoint by location. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           
   :param bptloc: Breakpoint location
   :param bpt: bpt is filled if the breakpoint was found


.. py:function:: enable_bpt(*args) -> bool

.. py:function:: disable_bpt(*args) -> bool

.. py:function:: request_enable_bpt(*args) -> bool

.. py:function:: request_disable_bpt(*args) -> bool

.. py:function:: check_bpt(ea: ida_idaapi.ea_t) -> int

   Check the breakpoint at the specified address. 
           
   :returns: one of Breakpoint status codes


.. py:data:: BPTCK_NONE

   breakpoint does not exist


.. py:data:: BPTCK_NO

   breakpoint is disabled


.. py:data:: BPTCK_YES

   breakpoint is enabled


.. py:data:: BPTCK_ACT

   breakpoint is active (written to the process)


.. py:function:: set_trace_size(size: int) -> bool

   Specify the new size of the circular buffer. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param size: if 0, buffer isn't circular and events are never removed. If the new size is smaller than the existing number of trace events, a corresponding number of trace events are removed.


.. py:function:: clear_trace() -> None

   Clear all events in the trace buffer. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           


.. py:function:: request_clear_trace() -> None

   Post a clear_trace() request.


.. py:function:: is_step_trace_enabled() -> bool

   Get current state of step tracing. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: enable_step_trace(enable: int = 1) -> bool

.. py:function:: disable_step_trace() -> bool

.. py:function:: request_enable_step_trace(enable: int = 1) -> bool

.. py:function:: request_disable_step_trace() -> bool

.. py:data:: ST_OVER_DEBUG_SEG

   step tracing will be disabled when IP is in a debugger segment


.. py:data:: ST_OVER_LIB_FUNC

   step tracing will be disabled when IP is in a library function


.. py:data:: ST_ALREADY_LOGGED

   step tracing will be disabled when IP is already logged


.. py:data:: ST_SKIP_LOOPS

   step tracing will try to skip loops already recorded


.. py:data:: ST_DIFFERENTIAL

   tracing: log only new instructions (not previously logged) 
           


.. py:data:: ST_OPTIONS_MASK

   mask of available options, to ensure compatibility with newer IDA versions


.. py:data:: ST_OPTIONS_DEFAULT

.. py:data:: IT_LOG_SAME_IP

   specific options for instruction tracing (see set_insn_trace_options())

   instruction tracing will log new instructions even when IP doesn't change 
           


.. py:data:: FT_LOG_RET

   specific options for function tracing (see set_func_trace_options())

   function tracing will log returning instructions 
           


.. py:data:: BT_LOG_INSTS

   specific options for basic block tracing (see set_bblk_trace_options())

   log all instructions in the current basic block 
           


.. py:function:: get_step_trace_options() -> int

   Get current step tracing options. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :returns: Step trace options


.. py:function:: set_step_trace_options(options: int) -> None

   Modify step tracing options. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           


.. py:function:: request_set_step_trace_options(options: int) -> None

   Post a set_step_trace_options() request.


.. py:function:: is_insn_trace_enabled() -> bool

   Get current state of instruction tracing. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: enable_insn_trace(enable: bool = True) -> bool

.. py:function:: disable_insn_trace() -> bool

.. py:function:: request_enable_insn_trace(enable: bool = True) -> bool

.. py:function:: request_disable_insn_trace() -> bool

.. py:function:: get_insn_trace_options() -> int

   Get current instruction tracing options. Also see IT_LOG_SAME_IP \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: set_insn_trace_options(options: int) -> None

   Modify instruction tracing options. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           


.. py:function:: request_set_insn_trace_options(options: int) -> None

   Post a set_insn_trace_options() request.


.. py:function:: is_func_trace_enabled() -> bool

   Get current state of functions tracing. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: enable_func_trace(enable: bool = True) -> bool

.. py:function:: disable_func_trace() -> bool

.. py:function:: request_enable_func_trace(enable: bool = True) -> bool

.. py:function:: request_disable_func_trace() -> bool

.. py:function:: get_func_trace_options() -> int

   Get current function tracing options. Also see FT_LOG_RET \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: set_func_trace_options(options: int) -> None

   Modify function tracing options. \sq{Type, Synchronous function - available as request, Notification, none (synchronous function)} 
           


.. py:function:: request_set_func_trace_options(options: int) -> None

   Post a set_func_trace_options() request.


.. py:function:: enable_bblk_trace(enable: bool = True) -> bool

.. py:function:: disable_bblk_trace() -> bool

.. py:function:: request_enable_bblk_trace(enable: bool = True) -> bool

.. py:function:: request_disable_bblk_trace() -> bool

.. py:function:: is_bblk_trace_enabled() -> bool

.. py:function:: get_bblk_trace_options() -> int

   Get current basic block tracing options. Also see BT_LOG_INSTS \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: set_bblk_trace_options(options: int) -> None

   Modify basic block tracing options (see BT_LOG_INSTS)


.. py:function:: request_set_bblk_trace_options(options: int) -> None

   Post a set_bblk_trace_options() request.


.. py:data:: tev_none

   no event


.. py:data:: tev_insn

   an instruction trace


.. py:data:: tev_call

   a function call trace


.. py:data:: tev_ret

   a function return trace


.. py:data:: tev_bpt

   write, read/write, execution trace


.. py:data:: tev_mem

   memory layout changed


.. py:data:: tev_event

   debug event occurred


.. py:data:: tev_max

   first unused event type


.. py:class:: tev_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: type
      :type:  tev_type_t

      trace event type



   .. py:attribute:: tid
      :type:  thid_t

      thread where the event was recorded



   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      address where the event occurred



.. py:class:: memreg_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t


   .. py:method:: get_bytes() -> PyObject *


   .. py:attribute:: bytes


.. py:function:: get_tev_qty() -> int

   Get number of trace events available in trace buffer. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: get_tev_info(n: int, tev_info: tev_info_t) -> bool

   Get main information about a trace event. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of trace event, is in range 0..get_tev_qty()-1. 0 represents the latest added trace event.
   :param tev_info: result
   :returns: success


.. py:function:: get_insn_tev_reg_val(n: int, regname: str, regval: regval_t) -> bool

   Read a register value from an instruction trace event. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of trace event, is in range 0..get_tev_qty()-1. 0 represents the latest added trace event.
   :param regname: name of desired register
   :param regval: result
   :returns: false if not an instruction event.


.. py:function:: get_insn_tev_reg_mem(n: int, memmap: memreg_infos_t) -> bool

   Read the memory pointed by register values from an instruction trace event. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of trace event, is in range 0..get_tev_qty()-1. 0 represents the latest added trace event.
   :param memmap: result
   :returns: false if not an instruction event or no memory is available


.. py:function:: get_insn_tev_reg_result(n: int, regname: str, regval: regval_t) -> bool

   Read the resulting register value from an instruction trace event. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of trace event, is in range 0..get_tev_qty()-1. 0 represents the latest added trace event.
   :param regname: name of desired register
   :param regval: result
   :returns: false if not an instruction trace event or register wasn't modified.


.. py:function:: get_call_tev_callee(n: int) -> ida_idaapi.ea_t

   Get the called function from a function call trace event. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of trace event, is in range 0..get_tev_qty()-1. 0 represents the latest added trace event.
   :returns: BADADDR if not a function call event.


.. py:function:: get_ret_tev_return(n: int) -> ida_idaapi.ea_t

   Get the return address from a function return trace event. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of trace event, is in range 0..get_tev_qty()-1. 0 represents the latest added trace event.
   :returns: BADADDR if not a function return event.


.. py:function:: get_bpt_tev_ea(n: int) -> ida_idaapi.ea_t

   Get the address associated to a read, read/write or execution trace event. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of trace event, is in range 0..get_tev_qty()-1. 0 represents the latest added trace event.
   :returns: BADADDR if not a read, read/write or execution trace event.


.. py:function:: get_tev_memory_info(n: int, mi: meminfo_vec_t) -> bool

   Get the memory layout, if any, for the specified tev object. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of trace event, is in range 0..get_tev_qty()-1. 0 represents the latest added trace event.
   :param mi: result
   :returns: false if the tev_t object is not of type tev_mem, true otherwise, with the new memory layout in "mi".


.. py:function:: get_tev_event(n: int, d: debug_event_t) -> bool

   Get the corresponding debug event, if any, for the specified tev object. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param n: number of trace event, is in range 0..get_tev_qty()-1. 0 represents the latest added trace event.
   :param d: result
   :returns: false if the tev_t object doesn't have any associated debug event, true otherwise, with the debug event in "d".


.. py:function:: get_trace_base_address() -> ida_idaapi.ea_t

   Get the base address of the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :returns: the base address of the currently loaded trace


.. py:function:: set_trace_base_address(ea: ida_idaapi.ea_t) -> None

   Set the base address of the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: dbg_add_thread(tid: thid_t) -> None

   Add a thread to the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: dbg_del_thread(tid: thid_t) -> None

   Delete a thread from the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: dbg_add_tev(type: tev_type_t, tid: thid_t, address: ida_idaapi.ea_t) -> None

   Add a new trace element to the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:class:: tev_reg_value_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: value
      :type:  regval_t


   .. py:attribute:: reg_idx
      :type:  int


.. py:class:: tev_info_reg_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: info
      :type:  tev_info_t


   .. py:attribute:: registers
      :type:  tev_reg_values_t


.. py:data:: SAVE_ALL_VALUES

.. py:data:: SAVE_DIFF

.. py:data:: SAVE_NONE

.. py:function:: dbg_add_many_tevs(new_tevs: tevinforeg_vec_t) -> bool

   Add many new trace elements to the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :returns: false if the operation failed for any tev_info_t object


.. py:function:: dbg_add_insn_tev(tid: thid_t, ea: ida_idaapi.ea_t, save: save_reg_values_t = SAVE_DIFF) -> bool

   Add a new instruction trace element to the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :returns: false if the operation failed, true otherwise


.. py:function:: dbg_add_bpt_tev(tid: thid_t, ea: ida_idaapi.ea_t, bp: ida_idaapi.ea_t) -> bool

   Add a new breakpoint trace element to the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :returns: false if the operation failed, true otherwise


.. py:function:: dbg_add_call_tev(tid: thid_t, caller: ida_idaapi.ea_t, callee: ida_idaapi.ea_t) -> None

   Add a new call trace element to the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: dbg_add_ret_tev(tid: thid_t, ret_insn: ida_idaapi.ea_t, return_to: ida_idaapi.ea_t) -> None

   Add a new return trace element to the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: dbg_add_debug_event(event: debug_event_t) -> None

   Add a new debug event to the current trace. \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           


.. py:function:: load_trace_file(filename: str) -> str

   Load a recorded trace file in the 'Tracing' window. If the call succeeds and 'buf' is not null, the description of the trace stored in the binary trace file will be returned in 'buf' 
           


.. py:function:: save_trace_file(filename: str, description: str) -> bool

   Save the current trace in the specified file.


.. py:function:: is_valid_trace_file(filename: str) -> bool

   Is the specified file a valid trace file for the current database?


.. py:function:: set_trace_file_desc(filename: str, description: str) -> bool

   Change the description of the specified trace file.


.. py:function:: get_trace_file_desc(filename: str) -> str

   Get the file header of the specified trace file.


.. py:function:: choose_trace_file() -> str

   Show the choose trace dialog.


.. py:function:: diff_trace_file(NONNULL_filename: str) -> bool

   Show difference between the current trace and the one from 'filename'.


.. py:function:: graph_trace() -> bool

   Show the trace callgraph.


.. py:function:: set_highlight_trace_options(hilight: bool, color: bgcolor_t, diff: bgcolor_t) -> None

   Set highlight trace parameters.


.. py:function:: set_trace_platform(platform: str) -> None

   Set platform name of current trace.


.. py:function:: get_trace_platform() -> str

   Get platform name of current trace.


.. py:function:: set_trace_dynamic_register_set(idaregs: dynamic_register_set_t &) -> None

   Set dynamic register set of current trace.


.. py:function:: get_trace_dynamic_register_set(idaregs: dynamic_register_set_t *) -> None

   Get dynamic register set of current trace.


.. py:data:: DEC_NOTASK

   process does not exist


.. py:data:: DEC_ERROR

   error


.. py:data:: DEC_TIMEOUT

   timeout


.. py:data:: WFNE_ANY

   return the first event (even if it doesn't suspend the process)


.. py:data:: WFNE_SUSP

   wait until the process gets suspended


.. py:data:: WFNE_SILENT

   1: be silent, 0:display modal boxes if necessary


.. py:data:: WFNE_CONT

   continue from the suspended state


.. py:data:: WFNE_NOWAIT

   do not wait for any event, immediately return DEC_TIMEOUT (to be used with WFNE_CONT) 
           


.. py:data:: WFNE_USEC

   timeout is specified in microseconds (minimum non-zero timeout is 40000us) 
           


.. py:data:: DOPT_SEGM_MSGS

   log debugger segments modifications


.. py:data:: DOPT_START_BPT

   break on process start


.. py:data:: DOPT_THREAD_MSGS

   log thread starts/exits


.. py:data:: DOPT_THREAD_BPT

   break on thread start/exit


.. py:data:: DOPT_BPT_MSGS

   log breakpoints


.. py:data:: DOPT_LIB_MSGS

   log library loads/unloads


.. py:data:: DOPT_LIB_BPT

   break on library load/unload


.. py:data:: DOPT_INFO_MSGS

   log debugging info events


.. py:data:: DOPT_INFO_BPT

   break on debugging information


.. py:data:: DOPT_REAL_MEMORY

   do not hide breakpoint instructions


.. py:data:: DOPT_REDO_STACK

   reconstruct the stack


.. py:data:: DOPT_ENTRY_BPT

   break on program entry point


.. py:data:: DOPT_EXCDLG

   exception dialogs:


.. py:data:: EXCDLG_NEVER

   never display exception dialogs


.. py:data:: EXCDLG_UNKNOWN

   display for unknown exceptions


.. py:data:: EXCDLG_ALWAYS

   always display


.. py:data:: DOPT_LOAD_DINFO

   automatically load debug files (pdb)


.. py:data:: DOPT_END_BPT

   evaluate event condition on process end


.. py:data:: DOPT_TEMP_HWBPT

   when possible use hardware bpts for temp bpts


.. py:data:: DOPT_FAST_STEP

   prevent debugger memory refreshes when single-stepping


.. py:data:: DOPT_DISABLE_ASLR

   disable ASLR


.. py:function:: wait_for_next_event(wfne: int, timeout: int) -> dbg_event_code_t

   Wait for the next event.
   This function (optionally) resumes the process execution, and waits for a debugger event until a possible timeout occurs.

   :param wfne: combination of Wait for debugger event flags constants
   :param timeout: number of seconds to wait, -1-infinity
   :returns: either an event_id_t (if > 0), or a dbg_event_code_t (if <= 0)


.. py:function:: get_debug_event() -> debug_event_t const *

   Get the current debugger event.


.. py:function:: set_debugger_options(options: uint) -> uint

   Set debugger options. Replaces debugger options with the specification combination Debugger options 
           
   :returns: the old debugger options


.. py:function:: set_remote_debugger(host: str, _pass: str, port: int = -1) -> None

   Set remote debugging options. Should be used before starting the debugger. 
           
   :param host: If empty, IDA will use local debugger. If nullptr, the host will not be set.
   :param port: If -1, the default port number will be used


.. py:function:: get_process_options2() -> qstring *, qstring *, launch_env_t *, qstring *, qstring *, qstring *, int *

.. py:function:: retrieve_exceptions() -> excvec_t *

   Retrieve the exception information. You may freely modify the returned vector and add/edit/delete exceptions You must call store_exceptions() after any modifications Note: exceptions with code zero, multiple exception codes or names are prohibited 
           


.. py:function:: store_exceptions() -> bool

   Update the exception information stored in the debugger module by invoking its dbg->set_exception_info callback 
           


.. py:function:: define_exception(code: uint, name: str, desc: str, flags: int) -> str

   Convenience function: define new exception code. 
           
   :param code: exception code (cannot be 0)
   :param name: exception name (cannot be empty or nullptr)
   :param desc: exception description (maybe nullptr)
   :param flags: combination of Exception info flags
   :returns: failure message or nullptr. You must call store_exceptions() if this function succeeds


.. py:class:: eval_ctx_t(_ea: ida_idaapi.ea_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t


.. py:data:: SRCIT_NONE

   unknown


.. py:data:: SRCIT_MODULE

   module


.. py:data:: SRCIT_FUNC

   function


.. py:data:: SRCIT_STMT

   a statement (if/while/for...)


.. py:data:: SRCIT_EXPR

   an expression (a+b*c)


.. py:data:: SRCIT_STTVAR

   static variable/code


.. py:data:: SRCIT_LOCVAR

   a stack, register, or register-relative local variable or parameter


.. py:data:: SRCDBG_PROV_VERSION

.. py:function:: create_source_viewer(out_ccv: TWidget **, parent: TWidget *, custview: TWidget *, sf: source_file_ptr, lines: strvec_t *, lnnum: int, colnum: int, flags: int) -> source_view_t *

   Create a source code view.


.. py:function:: get_dbg_byte(ea: ida_idaapi.ea_t) -> uint32 *

   Get one byte of the debugged process memory. 
           
   :param ea: linear address
   :returns: success
   :returns: true: success
   :returns: false: address inaccessible or debugger not running


.. py:function:: put_dbg_byte(ea: ida_idaapi.ea_t, x: int) -> bool

   Change one byte of the debugged process memory. 
           
   :param ea: linear address
   :param x: byte value
   :returns: true if the process memory has been modified


.. py:function:: invalidate_dbgmem_config() -> None

   Invalidate the debugged process memory configuration. Call this function if the debugged process might have changed its memory layout (allocated more memory, for example) 
           


.. py:function:: invalidate_dbgmem_contents(ea: ida_idaapi.ea_t, size: asize_t) -> None

   Invalidate the debugged process memory contents. Call this function each time the process has been stopped or the process memory is modified. If ea == BADADDR, then the whole memory contents will be invalidated 
           


.. py:function:: is_debugger_on() -> bool

   Is the debugger currently running?


.. py:function:: is_debugger_memory(ea: ida_idaapi.ea_t) -> bool

   Is the address mapped to debugger memory?


.. py:function:: get_tev_ea(n: int) -> ida_idaapi.ea_t

.. py:function:: get_tev_type(n: int) -> int

.. py:function:: get_tev_tid(n: int) -> int

.. py:function:: bring_debugger_to_front() -> None

.. py:function:: set_manual_regions(ranges: meminfo_vec_t) -> None

.. py:function:: edit_manual_regions() -> None

.. py:function:: enable_manual_regions(enable: bool) -> None

.. py:function:: handle_debug_event(ev: debug_event_t, rqflags: int) -> int

.. py:function:: add_virt_module(mod: modinfo_t) -> bool

.. py:function:: del_virt_module(base: ea_t const) -> bool

.. py:function:: internal_ioctl(fn: int, buf: void const *, poutbuf: void **, poutsize: ssize_t *) -> int

.. py:function:: get_dbg_memory_info(ranges: meminfo_vec_t) -> int

.. py:function:: set_bpt_group(bpt: bpt_t, grp_name: str) -> bool

   Move a bpt into a folder in the breakpoint dirtree if the folder didn't exists, it will be created \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param bpt: bpt that will be moved
   :param grp_name: absolute path to the breakpoint dirtree folder
   :returns: success


.. py:function:: set_bptloc_group(bptloc: bpt_location_t, grp_name: str) -> bool

   Move a bpt into a folder in the breakpoint dirtree based on the bpt_location find_bpt is called to retrieve the bpt and then set_bpt_group if the folder didn't exists, it will be created \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param bptloc: bptlocation of the bpt that will be moved
   :param grp_name: absolute path to the breakpoint dirtree folder
   :returns: success


.. py:function:: get_bpt_group(bptloc: bpt_location_t) -> str

   Retrieve the absolute path to the folder of the bpt based on the bpt_location find_bpt is called to retrieve the bpt \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param bptloc: bptlocation of the bpt
   :returns: success
   :returns: true: breakpoint correclty moved to the directory


.. py:function:: rename_bptgrp(old_name: str, new_name: str) -> bool

   Rename a folder of bpt dirtree \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param old_name: absolute path to the folder to be renamed
   :param new_name: absolute path of the new folder name
   :returns: success


.. py:function:: del_bptgrp(name: str) -> bool

   Delete a folder, bpt that were part of this folder are moved to the root folder \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param name: full path to the folder to be deleted
   :returns: success


.. py:function:: get_grp_bpts(bpts: bpt_vec_t, grp_name: str) -> ssize_t

   Retrieve a copy the bpts stored in a folder \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param bpts: : pointer to a vector where the copy of bpts are stored
   :param grp_name: absolute path to the folder
   :returns: number of bpts present in the vector


.. py:function:: enable_bptgrp(bptgrp_name: str, enable: bool = True) -> int

   Enable (or disable) all bpts in a folder \sq{Type, Synchronous function, Notification, none (synchronous function)} 
           
   :param bptgrp_name: absolute path to the folder
   :param enable: by default true, enable bpts, false disable bpts
   :returns: -1: an error occured
   :returns: 0: no changes
   :returns: >0: nubmers of bpts udpated


.. py:function:: get_local_vars(prov: srcinfo_provider_t *, ea: ida_idaapi.ea_t, out: source_items_t *) -> bool

.. py:function:: srcdbg_request_step_into() -> bool

.. py:function:: srcdbg_request_step_over() -> bool

.. py:function:: srcdbg_request_step_until_ret() -> bool

.. py:function:: hide_all_bpts() -> int

.. py:function:: read_dbg_memory(ea: ida_idaapi.ea_t, buffer: void *, size: size_t) -> ssize_t

.. py:function:: get_module_info(ea: ida_idaapi.ea_t, modinfo: modinfo_t) -> bool

.. py:function:: dbg_bin_search(start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t, data: compiled_binpat_vec_t const &, srch_flags: int) -> str

.. py:function:: load_debugger(dbgname: str, use_remote: bool) -> bool

.. py:function:: collect_stack_trace(tid: thid_t, trace: call_stack_t) -> bool

.. py:function:: get_global_var(prov: srcinfo_provider_t *, ea: ida_idaapi.ea_t, name: str, out: source_item_ptr *) -> bool

.. py:function:: get_local_var(prov: srcinfo_provider_t *, ea: ida_idaapi.ea_t, name: str, out: source_item_ptr *) -> bool

.. py:function:: get_srcinfo_provider(name: str) -> srcinfo_provider_t *

.. py:function:: get_current_source_file() -> str

.. py:function:: get_current_source_line() -> int

.. py:function:: add_path_mapping(src: str, dst: str) -> None

.. py:function:: srcdbg_step_into() -> bool

.. py:function:: srcdbg_step_over() -> bool

.. py:function:: srcdbg_step_until_ret() -> bool

.. py:function:: set_debugger_event_cond(NONNULL_evcond: str) -> None

.. py:function:: get_debugger_event_cond() -> str

.. py:function:: set_process_options(*args) -> None

   Set process options. Any of the arguments may be nullptr, which means 'do not modify' 
           


.. py:function:: get_process_options() -> qstring *, qstring *, qstring *, qstring *, qstring *, int *

   Get process options. Any of the arguments may be nullptr 
           


.. py:function:: get_manual_regions(*args)

   Returns the manual memory regions

   This function has the following signatures:

       1. get_manual_regions() -> List[Tuple(ida_idaapi.ea_t, ida_idaapi.ea_t, str, str, ida_idaapi.ea_t, int, int)]
          Where each tuple holds (start_ea, end_ea, name, sclass, sbase, bitness, perm)
       2. get_manual_regions(storage: meminfo_vec_t) -> None


.. py:function:: dbg_is_loaded()

   Checks if a debugger is loaded

   :returns: Boolean


.. py:function:: refresh_debugger_memory()

   Refreshes the debugger memory

   :returns: Nothing


.. py:class:: DBG_Hooks(_flags: int = 0, _hkcb_flags: int = 1)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: hook() -> bool


   .. py:method:: unhook() -> bool


   .. py:method:: dbg_process_start(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t, modinfo_name: str, modinfo_base: ida_idaapi.ea_t, modinfo_size: asize_t) -> None


   .. py:method:: dbg_process_exit(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t, exit_code: int) -> None


   .. py:method:: dbg_process_attach(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t, modinfo_name: str, modinfo_base: ida_idaapi.ea_t, modinfo_size: asize_t) -> None


   .. py:method:: dbg_process_detach(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t) -> None


   .. py:method:: dbg_thread_start(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t) -> None


   .. py:method:: dbg_thread_exit(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t, exit_code: int) -> None


   .. py:method:: dbg_library_load(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t, modinfo_name: str, modinfo_base: ida_idaapi.ea_t, modinfo_size: asize_t) -> None


   .. py:method:: dbg_library_unload(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t, info: str) -> None


   .. py:method:: dbg_information(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t, info: str) -> None


   .. py:method:: dbg_exception(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t, exc_code: int, exc_can_cont: bool, exc_ea: ida_idaapi.ea_t, exc_info: str) -> int


   .. py:method:: dbg_suspend_process() -> None

      The process is now suspended. 
                



   .. py:method:: dbg_bpt(tid: thid_t, bptea: ida_idaapi.ea_t) -> int

      A user defined breakpoint was reached. 
                
      :param tid: (thid_t)
      :param bptea: (::ea_t)



   .. py:method:: dbg_trace(tid: thid_t, ip: ida_idaapi.ea_t) -> int

      A step occurred (one instruction was executed). This event notification is only generated if step tracing is enabled. 
                
      :param tid: (thid_t) thread ID
      :param ip: (::ea_t) current instruction pointer. usually points after the executed instruction
      :returns: 1: do not log this trace event
      :returns: 0: log it



   .. py:method:: dbg_request_error(failed_command: int, failed_dbg_notification: int) -> None

      An error occurred during the processing of a request. 
                
      :param failed_command: (ui_notification_t)
      :param failed_dbg_notification: (dbg_notification_t)



   .. py:method:: dbg_step_into() -> None


   .. py:method:: dbg_step_over() -> None


   .. py:method:: dbg_run_to(pid: pid_t, tid: thid_t, ea: ida_idaapi.ea_t) -> None


   .. py:method:: dbg_step_until_ret() -> None


   .. py:method:: dbg_bpt_changed(bptev_code: int, bpt: bpt_t) -> None

      Breakpoint has been changed. 
                
      :param bptev_code: (int) Breakpoint modification events
      :param bpt: (bpt_t *)



   .. py:method:: dbg_started_loading_bpts() -> None

      Started loading breakpoint info from idb.



   .. py:method:: dbg_finished_loading_bpts() -> None

      Finished loading breakpoint info from idb.



.. py:function:: list_bptgrps() -> List[str]

   Retrieve the list of absolute path of all folders of bpt dirtree.
   Synchronous function, Notification, none (synchronous function)


.. py:function:: internal_get_sreg_base(tid: int, sreg_value: int)

   Get the sreg base, for the given thread.

   :param tid: the thread ID
   :param sreg_value: the sreg value
   :returns: The sreg base, or BADADDR on failure.


.. py:function:: write_dbg_memory(*args) -> ssize_t

.. py:function:: dbg_can_query()

   This function can be used to check if the debugger can be queried:
     - debugger is loaded
     - process is suspended
     - process is not suspended but can take requests. In this case some requests like
       memory read/write, bpt management succeed and register querying will fail.
       Check if idaapi.get_process_state() < 0 to tell if the process is suspended

   :returns: Boolean


.. py:function:: set_reg_val(*args) -> bool

   Set a register value by name

   This function has the following signatures:
       1. set_reg_val(name: str, value: Union[int, float, bytes]) -> bool
       1. set_reg_val(tid: int, regidx: int, value: Union[int, float, bytes]) -> bool

   Depending on the register type, this will expect
   either an integer, a float or, in the case of large
   vector registers, a bytes sequence.

   :param name: (1st form) the register name
   :param tid: (2nd form) the thread ID
   :param regidx: (2nd form) the register index
   :param value: the register value
   :returns: success


.. py:function:: request_set_reg_val(regname: str, o: PyObject *) -> PyObject *

   Post a set_reg_val() request.


.. py:function:: get_reg_val(*args)

   Get a register value.

   This function has the following signatures:

       1. get_reg_val(name: str) -> Union[int, float, bytes]
       2. get_reg_val(name: str, regval: regval_t) -> bool

   The first (and most user-friendly) form will return
   a value whose type is related to the register type.
   I.e., either an integer, a float or, in the case of large
   vector registers, a bytes sequence.

   :param name: the register name
   :returns: the register value (1st form)


.. py:function:: get_reg_vals(tid: int, clsmask: int = -1) -> ida_idd.regvals_t

   Fetch live registers values for the thread

   :param tid: The ID of the thread to read registers for
   :param clsmask: An OR'ed mask of register classes to
          read values for (can be used to speed up the
          retrieval process)

   :returns: a list of register values (empty if an error occurs)


.. py:function:: get_tev_reg_val(tev, reg)

.. py:function:: get_tev_reg_mem_qty(tev)

.. py:function:: get_tev_reg_mem(tev, idx)

.. py:function:: get_tev_reg_mem_ea(tev, idx)

.. py:function:: send_dbg_command(command)

   Send a direct command to the debugger backend, and
   retrieve the result as a string.

   Note: any double-quotes in 'command' must be backslash-escaped.
   Note: this only works with some debugger backends: Bochs, WinDbg, GDB.

   Returns: (True, <result string>) on success, or (False, <Error message string>) on failure


.. py:data:: move_bpt_to_grp


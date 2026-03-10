ida_ida
=======

.. py:module:: ida_ida

.. autoapi-nested-parse::

   Contains the ::inf structure definition and some functions common to the whole IDA project.

   The ::inf structure is saved in the database and contains information specific 
   to the current program being disassembled. Initially it is filled with values 
   from ida.cfg.

   Although it is not a good idea to change values in ::inf structure (because you 
   will overwrite values taken from ida.cfg), you are allowed to do it if you feel 
   it necessary.

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For database operations, see :mod:`ida_domain.database`.



Attributes
----------

.. autoapisummary::

   ida_ida.AF_FINAL
   ida_ida.f_EXE_old
   ida_ida.f_COM_old
   ida_ida.f_BIN
   ida_ida.f_DRV
   ida_ida.f_WIN
   ida_ida.f_HEX
   ida_ida.f_MEX
   ida_ida.f_LX
   ida_ida.f_LE
   ida_ida.f_NLM
   ida_ida.f_COFF
   ida_ida.f_PE
   ida_ida.f_OMF
   ida_ida.f_SREC
   ida_ida.f_ZIP
   ida_ida.f_OMFLIB
   ida_ida.f_AR
   ida_ida.f_LOADER
   ida_ida.f_ELF
   ida_ida.f_W32RUN
   ida_ida.f_AOUT
   ida_ida.f_PRC
   ida_ida.f_EXE
   ida_ida.f_COM
   ida_ida.f_AIXAR
   ida_ida.f_MACHO
   ida_ida.f_PSXOBJ
   ida_ida.f_MD1IMG
   ida_ida.STT_CUR
   ida_ida.STT_VA
   ida_ida.STT_MM
   ida_ida.STT_DBG
   ida_ida.IDAINFO_TAG_SIZE
   ida_ida.IDAINFO_PROCNAME_SIZE
   ida_ida.IDAINFO_STRLIT_PREF_SIZE
   ida_ida.INFFL_AUTO
   ida_ida.INFFL_ALLASM
   ida_ida.INFFL_LOADIDC
   ida_ida.INFFL_NOUSER
   ida_ida.INFFL_READONLY
   ida_ida.INFFL_CHKOPS
   ida_ida.INFFL_NMOPS
   ida_ida.INFFL_GRAPH_VIEW
   ida_ida.LFLG_PC_FPP
   ida_ida.LFLG_PC_FLAT
   ida_ida.LFLG_64BIT
   ida_ida.LFLG_IS_DLL
   ida_ida.LFLG_FLAT_OFF32
   ida_ida.LFLG_MSF
   ida_ida.LFLG_WIDE_HBF
   ida_ida.LFLG_DBG_NOPATH
   ida_ida.LFLG_SNAPSHOT
   ida_ida.LFLG_PACK
   ida_ida.LFLG_COMPRESS
   ida_ida.LFLG_KERNMODE
   ida_ida.LFLG_ILP32
   ida_ida.IDB_UNPACKED
   ida_ida.IDB_PACKED
   ida_ida.IDB_COMPRESSED
   ida_ida.AF_CODE
   ida_ida.AF_MARKCODE
   ida_ida.AF_JUMPTBL
   ida_ida.AF_PURDAT
   ida_ida.AF_USED
   ida_ida.AF_UNK
   ida_ida.AF_PROCPTR
   ida_ida.AF_PROC
   ida_ida.AF_FTAIL
   ida_ida.AF_LVAR
   ida_ida.AF_STKARG
   ida_ida.AF_REGARG
   ida_ida.AF_TRACE
   ida_ida.AF_VERSP
   ida_ida.AF_ANORET
   ida_ida.AF_MEMFUNC
   ida_ida.AF_TRFUNC
   ida_ida.AF_STRLIT
   ida_ida.AF_CHKUNI
   ida_ida.AF_FIXUP
   ida_ida.AF_DREFOFF
   ida_ida.AF_IMMOFF
   ida_ida.AF_DATOFF
   ida_ida.AF_FLIRT
   ida_ida.AF_SIGCMT
   ida_ida.AF_SIGMLT
   ida_ida.AF_HFLIRT
   ida_ida.AF_JFUNC
   ida_ida.AF_NULLSUB
   ida_ida.AF_DODATA
   ida_ida.AF_DOCODE
   ida_ida.AF2_DOEH
   ida_ida.AF2_DORTTI
   ida_ida.AF2_MACRO
   ida_ida.AF2_MERGESTR
   ida_ida.SW_SEGXRF
   ida_ida.SW_XRFMRK
   ida_ida.SW_XRFFNC
   ida_ida.SW_XRFVAL
   ida_ida.NM_REL_OFF
   ida_ida.NM_PTR_OFF
   ida_ida.NM_NAM_OFF
   ida_ida.NM_REL_EA
   ida_ida.NM_PTR_EA
   ida_ida.NM_NAM_EA
   ida_ida.NM_EA
   ida_ida.NM_EA4
   ida_ida.NM_EA8
   ida_ida.NM_SHORT
   ida_ida.NM_SERIAL
   ida_ida.DEMNAM_MASK
   ida_ida.DEMNAM_CMNT
   ida_ida.DEMNAM_NAME
   ida_ida.DEMNAM_NONE
   ida_ida.DEMNAM_GCC3
   ida_ida.DEMNAM_FIRST
   ida_ida.LN_NORMAL
   ida_ida.LN_PUBLIC
   ida_ida.LN_AUTO
   ida_ida.LN_WEAK
   ida_ida.OFLG_SHOW_VOID
   ida_ida.OFLG_SHOW_AUTO
   ida_ida.OFLG_GEN_NULL
   ida_ida.OFLG_SHOW_PREF
   ida_ida.OFLG_PREF_SEG
   ida_ida.OFLG_LZERO
   ida_ida.OFLG_GEN_ORG
   ida_ida.OFLG_GEN_ASSUME
   ida_ida.OFLG_GEN_TRYBLKS
   ida_ida.SCF_RPTCMT
   ida_ida.SCF_ALLCMT
   ida_ida.SCF_NOCMT
   ida_ida.SCF_LINNUM
   ida_ida.SCF_TESTMODE
   ida_ida.SCF_SHHID_ITEM
   ida_ida.SCF_SHHID_FUNC
   ida_ida.SCF_SHHID_SEGM
   ida_ida.LMT_THIN
   ida_ida.LMT_THICK
   ida_ida.LMT_EMPTY
   ida_ida.PREF_SEGADR
   ida_ida.PREF_FNCOFF
   ida_ida.PREF_STACK
   ida_ida.PREF_PFXTRUNC
   ida_ida.STRF_GEN
   ida_ida.STRF_AUTO
   ida_ida.STRF_SERIAL
   ida_ida.STRF_UNICODE
   ida_ida.STRF_COMMENT
   ida_ida.STRF_SAVECASE
   ida_ida.ABI_8ALIGN4
   ida_ida.ABI_PACK_STKARGS
   ida_ida.ABI_BIGARG_ALIGN
   ida_ida.ABI_STACK_LDBL
   ida_ida.ABI_STACK_VARARGS
   ida_ida.ABI_HARD_FLOAT
   ida_ida.ABI_SET_BY_USER
   ida_ida.ABI_GCC_LAYOUT
   ida_ida.ABI_MAP_STKARGS
   ida_ida.ABI_HUGEARG_ALIGN
   ida_ida.INF_VERSION
   ida_ida.INF_PROCNAME
   ida_ida.INF_GENFLAGS
   ida_ida.INF_LFLAGS
   ida_ida.INF_DATABASE_CHANGE_COUNT
   ida_ida.INF_FILETYPE
   ida_ida.INF_OSTYPE
   ida_ida.INF_APPTYPE
   ida_ida.INF_ASMTYPE
   ida_ida.INF_SPECSEGS
   ida_ida.INF_AF
   ida_ida.INF_AF2
   ida_ida.INF_BASEADDR
   ida_ida.INF_START_SS
   ida_ida.INF_START_CS
   ida_ida.INF_START_IP
   ida_ida.INF_START_EA
   ida_ida.INF_START_SP
   ida_ida.INF_MAIN
   ida_ida.INF_MIN_EA
   ida_ida.INF_MAX_EA
   ida_ida.INF_OMIN_EA
   ida_ida.INF_OMAX_EA
   ida_ida.INF_LOWOFF
   ida_ida.INF_HIGHOFF
   ida_ida.INF_MAXREF
   ida_ida.INF_PRIVRANGE
   ida_ida.INF_PRIVRANGE_START_EA
   ida_ida.INF_PRIVRANGE_END_EA
   ida_ida.INF_NETDELTA
   ida_ida.INF_XREFNUM
   ida_ida.INF_TYPE_XREFNUM
   ida_ida.INF_REFCMTNUM
   ida_ida.INF_XREFFLAG
   ida_ida.INF_MAX_AUTONAME_LEN
   ida_ida.INF_NAMETYPE
   ida_ida.INF_SHORT_DEMNAMES
   ida_ida.INF_LONG_DEMNAMES
   ida_ida.INF_DEMNAMES
   ida_ida.INF_LISTNAMES
   ida_ida.INF_INDENT
   ida_ida.INF_CMT_INDENT
   ida_ida.INF_MARGIN
   ida_ida.INF_LENXREF
   ida_ida.INF_OUTFLAGS
   ida_ida.INF_CMTFLG
   ida_ida.INF_LIMITER
   ida_ida.INF_BIN_PREFIX_SIZE
   ida_ida.INF_PREFFLAG
   ida_ida.INF_STRLIT_FLAGS
   ida_ida.INF_STRLIT_BREAK
   ida_ida.INF_STRLIT_ZEROES
   ida_ida.INF_STRTYPE
   ida_ida.INF_STRLIT_PREF
   ida_ida.INF_STRLIT_SERNUM
   ida_ida.INF_DATATYPES
   ida_ida.INF_OBSOLETE_CC
   ida_ida.INF_CC_ID
   ida_ida.INF_CC_CM
   ida_ida.INF_CC_SIZE_I
   ida_ida.INF_CC_SIZE_B
   ida_ida.INF_CC_SIZE_E
   ida_ida.INF_CC_DEFALIGN
   ida_ida.INF_CC_SIZE_S
   ida_ida.INF_CC_SIZE_L
   ida_ida.INF_CC_SIZE_LL
   ida_ida.INF_CC_SIZE_LDBL
   ida_ida.INF_ABIBITS
   ida_ida.INF_APPCALL_OPTIONS
   ida_ida.INF_FILE_FORMAT_NAME
   ida_ida.INF_GROUPS
   ida_ida.INF_H_PATH
   ida_ida.INF_C_MACROS
   ida_ida.INF_INCLUDE
   ida_ida.INF_DUALOP_GRAPH
   ida_ida.INF_DUALOP_TEXT
   ida_ida.INF_MD5
   ida_ida.INF_IDA_VERSION
   ida_ida.INF_STR_ENCODINGS
   ida_ida.INF_DBG_BINPATHS
   ida_ida.INF_SHA256
   ida_ida.INF_ABINAME
   ida_ida.INF_ARCHIVE_PATH
   ida_ida.INF_PROBLEMS
   ida_ida.INF_SELECTORS
   ida_ida.INF_NOTEPAD
   ida_ida.INF_SRCDBG_PATHS
   ida_ida.INF_SRCDBG_UNDESIRED
   ida_ida.INF_INITIAL_VERSION
   ida_ida.INF_CTIME
   ida_ida.INF_ELAPSED
   ida_ida.INF_NOPENS
   ida_ida.INF_CRC32
   ida_ida.INF_IMAGEBASE
   ida_ida.INF_IDSNODE
   ida_ida.INF_FSIZE
   ida_ida.INF_OUTFILEENC
   ida_ida.INF_INPUT_FILE_PATH
   ida_ida.INF_COMPILER_INFO
   ida_ida.INF_CALLCNV
   ida_ida.INF_LAST
   ida_ida.UA_MAXOP
   ida_ida.IDB_EXT32
   ida_ida.IDB_EXT64
   ida_ida.IDB_EXT
   ida_ida.VLD_AUTO_REPAIR
   ida_ida.VLD_DIALOG
   ida_ida.VLD_SILENT
   ida_ida.IDI_STRUCFLD
   ida_ida.IDI_ALTVAL
   ida_ida.IDI_SUPVAL
   ida_ida.IDI_VALOBJ
   ida_ida.IDI_BLOB
   ida_ida.IDI_SCALAR
   ida_ida.IDI_CSTR
   ida_ida.IDI_QSTRING
   ida_ida.IDI_BYTEARRAY
   ida_ida.IDI_EA_HEX
   ida_ida.IDI_DEC
   ida_ida.IDI_HEX
   ida_ida.IDI_INC
   ida_ida.IDI_MAP_VAL
   ida_ida.IDI_HASH
   ida_ida.IDI_HLPSTRUC
   ida_ida.IDI_READONLY
   ida_ida.IDI_BITMAP
   ida_ida.IDI_ONOFF
   ida_ida.IDI_NOMERGE
   ida_ida.IDI_NODEVAL
   ida_ida.IDI_BUFVAR
   ida_ida.idainfo_big_arg_align
   ida_ida.idainfo_gen_null
   ida_ida.idainfo_set_gen_null
   ida_ida.idainfo_gen_lzero
   ida_ida.idainfo_set_gen_lzero
   ida_ida.idainfo_gen_tryblks
   ida_ida.idainfo_set_gen_tryblks
   ida_ida.idainfo_get_demname_form
   ida_ida.idainfo_get_pack_mode
   ida_ida.idainfo_set_pack_mode
   ida_ida.idainfo_is_64bit
   ida_ida.idainfo_set_64bit
   ida_ida.idainfo_is_auto_enabled
   ida_ida.idainfo_set_auto_enabled
   ida_ida.idainfo_is_be
   ida_ida.idainfo_set_be
   ida_ida.idainfo_is_dll
   ida_ida.idainfo_is_flat_off32
   ida_ida.idainfo_is_graph_view
   ida_ida.idainfo_set_graph_view
   ida_ida.idainfo_is_hard_float
   ida_ida.idainfo_is_kernel_mode
   ida_ida.idainfo_is_mem_aligned4
   ida_ida.idainfo_is_snapshot
   ida_ida.idainfo_is_wide_high_byte_first
   ida_ida.idainfo_set_wide_high_byte_first
   ida_ida.idainfo_like_binary
   ida_ida.idainfo_line_pref_with_seg
   ida_ida.idainfo_set_line_pref_with_seg
   ida_ida.idainfo_show_auto
   ida_ida.idainfo_set_show_auto
   ida_ida.idainfo_show_line_pref
   ida_ida.idainfo_set_show_line_pref
   ida_ida.idainfo_show_void
   ida_ida.idainfo_set_show_void
   ida_ida.idainfo_loading_idc
   ida_ida.idainfo_map_stkargs
   ida_ida.idainfo_pack_stkargs
   ida_ida.idainfo_readonly_idb
   ida_ida.idainfo_set_store_user_info
   ida_ida.idainfo_stack_ldbl
   ida_ida.idainfo_stack_varargs
   ida_ida.idainfo_use_allasm
   ida_ida.idainfo_use_gcc_layout
   ida_ida.macros_enabled
   ida_ida.should_create_stkvars
   ida_ida.should_trace_sp
   ida_ida.show_all_comments
   ida_ida.show_comments
   ida_ida.show_repeatables
   ida_ida.inf_get_comment
   ida_ida.inf_set_comment
   ida_ida.idainfo_comment_get
   ida_ida.idainfo_comment_set


Classes
-------

.. autoapisummary::

   ida_ida.compiler_info_t
   ida_ida.idainfo
   ida_ida.idbattr_valmap_t
   ida_ida.idbattr_info_t


Functions
---------

.. autoapisummary::

   ida_ida.is_filetype_like_binary
   ida_ida.getinf_str
   ida_ida.delinf
   ida_ida.inf_get_version
   ida_ida.inf_set_version
   ida_ida.inf_get_genflags
   ida_ida.inf_set_genflags
   ida_ida.inf_is_auto_enabled
   ida_ida.inf_set_auto_enabled
   ida_ida.inf_use_allasm
   ida_ida.inf_set_use_allasm
   ida_ida.inf_loading_idc
   ida_ida.inf_set_loading_idc
   ida_ida.inf_no_store_user_info
   ida_ida.inf_set_no_store_user_info
   ida_ida.inf_readonly_idb
   ida_ida.inf_set_readonly_idb
   ida_ida.inf_check_manual_ops
   ida_ida.inf_set_check_manual_ops
   ida_ida.inf_allow_non_matched_ops
   ida_ida.inf_set_allow_non_matched_ops
   ida_ida.inf_is_graph_view
   ida_ida.inf_set_graph_view
   ida_ida.inf_get_lflags
   ida_ida.inf_set_lflags
   ida_ida.inf_decode_fpp
   ida_ida.inf_set_decode_fpp
   ida_ida.inf_is_32bit_or_higher
   ida_ida.inf_is_32bit_exactly
   ida_ida.inf_set_32bit
   ida_ida.inf_is_16bit
   ida_ida.inf_is_64bit
   ida_ida.inf_set_64bit
   ida_ida.inf_is_ilp32
   ida_ida.inf_set_ilp32
   ida_ida.inf_is_dll
   ida_ida.inf_set_dll
   ida_ida.inf_is_flat_off32
   ida_ida.inf_set_flat_off32
   ida_ida.inf_is_be
   ida_ida.inf_set_be
   ida_ida.inf_is_wide_high_byte_first
   ida_ida.inf_set_wide_high_byte_first
   ida_ida.inf_dbg_no_store_path
   ida_ida.inf_set_dbg_no_store_path
   ida_ida.inf_is_snapshot
   ida_ida.inf_set_snapshot
   ida_ida.inf_pack_idb
   ida_ida.inf_set_pack_idb
   ida_ida.inf_compress_idb
   ida_ida.inf_set_compress_idb
   ida_ida.inf_is_kernel_mode
   ida_ida.inf_set_kernel_mode
   ida_ida.inf_get_app_bitness
   ida_ida.inf_set_app_bitness
   ida_ida.inf_get_database_change_count
   ida_ida.inf_set_database_change_count
   ida_ida.inf_get_filetype
   ida_ida.inf_set_filetype
   ida_ida.inf_get_ostype
   ida_ida.inf_set_ostype
   ida_ida.inf_get_apptype
   ida_ida.inf_set_apptype
   ida_ida.inf_get_asmtype
   ida_ida.inf_set_asmtype
   ida_ida.inf_get_specsegs
   ida_ida.inf_set_specsegs
   ida_ida.inf_get_af
   ida_ida.inf_set_af
   ida_ida.inf_trace_flow
   ida_ida.inf_set_trace_flow
   ida_ida.inf_mark_code
   ida_ida.inf_set_mark_code
   ida_ida.inf_create_jump_tables
   ida_ida.inf_set_create_jump_tables
   ida_ida.inf_noflow_to_data
   ida_ida.inf_set_noflow_to_data
   ida_ida.inf_create_all_xrefs
   ida_ida.inf_set_create_all_xrefs
   ida_ida.inf_del_no_xref_insns
   ida_ida.inf_set_del_no_xref_insns
   ida_ida.inf_create_func_from_ptr
   ida_ida.inf_set_create_func_from_ptr
   ida_ida.inf_create_func_from_call
   ida_ida.inf_set_create_func_from_call
   ida_ida.inf_create_func_tails
   ida_ida.inf_set_create_func_tails
   ida_ida.inf_should_create_stkvars
   ida_ida.inf_set_should_create_stkvars
   ida_ida.inf_propagate_stkargs
   ida_ida.inf_set_propagate_stkargs
   ida_ida.inf_propagate_regargs
   ida_ida.inf_set_propagate_regargs
   ida_ida.inf_should_trace_sp
   ida_ida.inf_set_should_trace_sp
   ida_ida.inf_full_sp_ana
   ida_ida.inf_set_full_sp_ana
   ida_ida.inf_noret_ana
   ida_ida.inf_set_noret_ana
   ida_ida.inf_guess_func_type
   ida_ida.inf_set_guess_func_type
   ida_ida.inf_truncate_on_del
   ida_ida.inf_set_truncate_on_del
   ida_ida.inf_create_strlit_on_xref
   ida_ida.inf_set_create_strlit_on_xref
   ida_ida.inf_check_unicode_strlits
   ida_ida.inf_set_check_unicode_strlits
   ida_ida.inf_create_off_using_fixup
   ida_ida.inf_set_create_off_using_fixup
   ida_ida.inf_create_off_on_dref
   ida_ida.inf_set_create_off_on_dref
   ida_ida.inf_op_offset
   ida_ida.inf_set_op_offset
   ida_ida.inf_data_offset
   ida_ida.inf_set_data_offset
   ida_ida.inf_use_flirt
   ida_ida.inf_set_use_flirt
   ida_ida.inf_append_sigcmt
   ida_ida.inf_set_append_sigcmt
   ida_ida.inf_allow_sigmulti
   ida_ida.inf_set_allow_sigmulti
   ida_ida.inf_hide_libfuncs
   ida_ida.inf_set_hide_libfuncs
   ida_ida.inf_rename_jumpfunc
   ida_ida.inf_set_rename_jumpfunc
   ida_ida.inf_rename_nullsub
   ida_ida.inf_set_rename_nullsub
   ida_ida.inf_coagulate_data
   ida_ida.inf_set_coagulate_data
   ida_ida.inf_coagulate_code
   ida_ida.inf_set_coagulate_code
   ida_ida.inf_final_pass
   ida_ida.inf_set_final_pass
   ida_ida.inf_get_af2
   ida_ida.inf_set_af2
   ida_ida.inf_handle_eh
   ida_ida.inf_set_handle_eh
   ida_ida.inf_handle_rtti
   ida_ida.inf_set_handle_rtti
   ida_ida.inf_macros_enabled
   ida_ida.inf_set_macros_enabled
   ida_ida.inf_merge_strlits
   ida_ida.inf_set_merge_strlits
   ida_ida.inf_get_baseaddr
   ida_ida.inf_set_baseaddr
   ida_ida.inf_get_start_ss
   ida_ida.inf_set_start_ss
   ida_ida.inf_get_start_cs
   ida_ida.inf_set_start_cs
   ida_ida.inf_get_start_ip
   ida_ida.inf_set_start_ip
   ida_ida.inf_get_start_ea
   ida_ida.inf_set_start_ea
   ida_ida.inf_get_start_sp
   ida_ida.inf_set_start_sp
   ida_ida.inf_get_main
   ida_ida.inf_set_main
   ida_ida.inf_get_min_ea
   ida_ida.inf_set_min_ea
   ida_ida.inf_get_max_ea
   ida_ida.inf_set_max_ea
   ida_ida.inf_get_omin_ea
   ida_ida.inf_set_omin_ea
   ida_ida.inf_get_omax_ea
   ida_ida.inf_set_omax_ea
   ida_ida.inf_get_lowoff
   ida_ida.inf_set_lowoff
   ida_ida.inf_get_highoff
   ida_ida.inf_set_highoff
   ida_ida.inf_get_maxref
   ida_ida.inf_set_maxref
   ida_ida.inf_get_netdelta
   ida_ida.inf_set_netdelta
   ida_ida.inf_get_xrefnum
   ida_ida.inf_set_xrefnum
   ida_ida.inf_get_type_xrefnum
   ida_ida.inf_set_type_xrefnum
   ida_ida.inf_get_refcmtnum
   ida_ida.inf_set_refcmtnum
   ida_ida.inf_get_xrefflag
   ida_ida.inf_set_xrefflag
   ida_ida.inf_show_xref_seg
   ida_ida.inf_set_show_xref_seg
   ida_ida.inf_show_xref_tmarks
   ida_ida.inf_set_show_xref_tmarks
   ida_ida.inf_show_xref_fncoff
   ida_ida.inf_set_show_xref_fncoff
   ida_ida.inf_show_xref_val
   ida_ida.inf_set_show_xref_val
   ida_ida.inf_get_max_autoname_len
   ida_ida.inf_set_max_autoname_len
   ida_ida.inf_get_nametype
   ida_ida.inf_set_nametype
   ida_ida.inf_get_short_demnames
   ida_ida.inf_set_short_demnames
   ida_ida.inf_get_long_demnames
   ida_ida.inf_set_long_demnames
   ida_ida.inf_get_demnames
   ida_ida.inf_set_demnames
   ida_ida.inf_get_listnames
   ida_ida.inf_set_listnames
   ida_ida.inf_get_indent
   ida_ida.inf_set_indent
   ida_ida.inf_get_cmt_indent
   ida_ida.inf_set_cmt_indent
   ida_ida.inf_get_margin
   ida_ida.inf_set_margin
   ida_ida.inf_get_lenxref
   ida_ida.inf_set_lenxref
   ida_ida.inf_get_outflags
   ida_ida.inf_set_outflags
   ida_ida.inf_show_void
   ida_ida.inf_set_show_void
   ida_ida.inf_show_auto
   ida_ida.inf_set_show_auto
   ida_ida.inf_gen_null
   ida_ida.inf_set_gen_null
   ida_ida.inf_show_line_pref
   ida_ida.inf_set_show_line_pref
   ida_ida.inf_line_pref_with_seg
   ida_ida.inf_set_line_pref_with_seg
   ida_ida.inf_gen_lzero
   ida_ida.inf_set_gen_lzero
   ida_ida.inf_gen_org
   ida_ida.inf_set_gen_org
   ida_ida.inf_gen_assume
   ida_ida.inf_set_gen_assume
   ida_ida.inf_gen_tryblks
   ida_ida.inf_set_gen_tryblks
   ida_ida.inf_get_cmtflg
   ida_ida.inf_set_cmtflg
   ida_ida.inf_show_repeatables
   ida_ida.inf_set_show_repeatables
   ida_ida.inf_show_all_comments
   ida_ida.inf_set_show_all_comments
   ida_ida.inf_hide_comments
   ida_ida.inf_set_hide_comments
   ida_ida.inf_show_src_linnum
   ida_ida.inf_set_show_src_linnum
   ida_ida.inf_test_mode
   ida_ida.inf_show_hidden_insns
   ida_ida.inf_set_show_hidden_insns
   ida_ida.inf_show_hidden_funcs
   ida_ida.inf_set_show_hidden_funcs
   ida_ida.inf_show_hidden_segms
   ida_ida.inf_set_show_hidden_segms
   ida_ida.inf_get_limiter
   ida_ida.inf_set_limiter
   ida_ida.inf_is_limiter_thin
   ida_ida.inf_set_limiter_thin
   ida_ida.inf_is_limiter_thick
   ida_ida.inf_set_limiter_thick
   ida_ida.inf_is_limiter_empty
   ida_ida.inf_set_limiter_empty
   ida_ida.inf_get_bin_prefix_size
   ida_ida.inf_set_bin_prefix_size
   ida_ida.inf_get_prefflag
   ida_ida.inf_set_prefflag
   ida_ida.inf_prefix_show_segaddr
   ida_ida.inf_set_prefix_show_segaddr
   ida_ida.inf_prefix_show_funcoff
   ida_ida.inf_set_prefix_show_funcoff
   ida_ida.inf_prefix_show_stack
   ida_ida.inf_set_prefix_show_stack
   ida_ida.inf_prefix_truncate_opcode_bytes
   ida_ida.inf_set_prefix_truncate_opcode_bytes
   ida_ida.inf_get_strlit_flags
   ida_ida.inf_set_strlit_flags
   ida_ida.inf_strlit_names
   ida_ida.inf_set_strlit_names
   ida_ida.inf_strlit_name_bit
   ida_ida.inf_set_strlit_name_bit
   ida_ida.inf_strlit_serial_names
   ida_ida.inf_set_strlit_serial_names
   ida_ida.inf_unicode_strlits
   ida_ida.inf_set_unicode_strlits
   ida_ida.inf_strlit_autocmt
   ida_ida.inf_set_strlit_autocmt
   ida_ida.inf_strlit_savecase
   ida_ida.inf_set_strlit_savecase
   ida_ida.inf_get_strlit_break
   ida_ida.inf_set_strlit_break
   ida_ida.inf_get_strlit_zeroes
   ida_ida.inf_set_strlit_zeroes
   ida_ida.inf_get_strtype
   ida_ida.inf_set_strtype
   ida_ida.inf_get_strlit_sernum
   ida_ida.inf_set_strlit_sernum
   ida_ida.inf_get_datatypes
   ida_ida.inf_set_datatypes
   ida_ida.inf_get_abibits
   ida_ida.inf_set_abibits
   ida_ida.inf_is_mem_aligned4
   ida_ida.inf_set_mem_aligned4
   ida_ida.inf_pack_stkargs
   ida_ida.inf_set_pack_stkargs
   ida_ida.inf_big_arg_align
   ida_ida.inf_set_big_arg_align
   ida_ida.inf_stack_ldbl
   ida_ida.inf_set_stack_ldbl
   ida_ida.inf_stack_varargs
   ida_ida.inf_set_stack_varargs
   ida_ida.inf_is_hard_float
   ida_ida.inf_set_hard_float
   ida_ida.inf_abi_set_by_user
   ida_ida.inf_set_abi_set_by_user
   ida_ida.inf_use_gcc_layout
   ida_ida.inf_set_use_gcc_layout
   ida_ida.inf_map_stkargs
   ida_ida.inf_set_map_stkargs
   ida_ida.inf_huge_arg_align
   ida_ida.inf_set_huge_arg_align
   ida_ida.inf_get_appcall_options
   ida_ida.inf_set_appcall_options
   ida_ida.inf_get_privrange_start_ea
   ida_ida.inf_set_privrange_start_ea
   ida_ida.inf_get_privrange_end_ea
   ida_ida.inf_set_privrange_end_ea
   ida_ida.inf_get_cc_id
   ida_ida.inf_set_cc_id
   ida_ida.inf_get_cc_cm
   ida_ida.inf_set_cc_cm
   ida_ida.inf_get_callcnv
   ida_ida.inf_set_callcnv
   ida_ida.inf_get_cc_size_i
   ida_ida.inf_set_cc_size_i
   ida_ida.inf_get_cc_size_b
   ida_ida.inf_set_cc_size_b
   ida_ida.inf_get_cc_size_e
   ida_ida.inf_set_cc_size_e
   ida_ida.inf_get_cc_defalign
   ida_ida.inf_set_cc_defalign
   ida_ida.inf_get_cc_size_s
   ida_ida.inf_set_cc_size_s
   ida_ida.inf_get_cc_size_l
   ida_ida.inf_set_cc_size_l
   ida_ida.inf_get_cc_size_ll
   ida_ida.inf_set_cc_size_ll
   ida_ida.inf_get_cc_size_ldbl
   ida_ida.inf_set_cc_size_ldbl
   ida_ida.inf_get_procname
   ida_ida.inf_set_procname
   ida_ida.inf_get_strlit_pref
   ida_ida.inf_set_strlit_pref
   ida_ida.inf_get_cc
   ida_ida.inf_set_cc
   ida_ida.inf_set_privrange
   ida_ida.inf_get_privrange
   ida_ida.inf_get_af_low
   ida_ida.inf_set_af_low
   ida_ida.inf_get_af_high
   ida_ida.inf_set_af_high
   ida_ida.inf_get_af2_low
   ida_ida.inf_set_af2_low
   ida_ida.inf_get_pack_mode
   ida_ida.inf_set_pack_mode
   ida_ida.inf_inc_database_change_count
   ida_ida.inf_get_demname_form
   ida_ida.inf_postinc_strlit_sernum
   ida_ida.inf_like_binary
   ida_ida.calc_default_idaplace_flags
   ida_ida.to_ea
   ida_ida.get_dbctx_id
   ida_ida.get_dbctx_qty
   ida_ida.switch_dbctx
   ida_ida.is_database_busy
   ida_ida.validate_idb
   ida_ida.move_privrange
   ida_ida.idainfo_is_32bit


Module Contents
---------------

.. py:data:: AF_FINAL

   Final pass of analysis.


.. py:data:: f_EXE_old

   MS DOS EXE File.


.. py:data:: f_COM_old

   MS DOS COM File.


.. py:data:: f_BIN

   Binary File.


.. py:data:: f_DRV

   MS DOS Driver.


.. py:data:: f_WIN

   New Executable (NE)


.. py:data:: f_HEX

   Intel Hex Object File.


.. py:data:: f_MEX

   MOS Technology Hex Object File.


.. py:data:: f_LX

   Linear Executable (LX)


.. py:data:: f_LE

   Linear Executable (LE)


.. py:data:: f_NLM

   Netware Loadable Module (NLM)


.. py:data:: f_COFF

   Common Object File Format (COFF)


.. py:data:: f_PE

   Portable Executable (PE)


.. py:data:: f_OMF

   Object Module Format.


.. py:data:: f_SREC

   Motorola SREC (S-record)


.. py:data:: f_ZIP

   ZIP file (this file is never loaded to IDA database)


.. py:data:: f_OMFLIB

   Library of OMF Modules.


.. py:data:: f_AR

   ar library


.. py:data:: f_LOADER

   file is loaded using LOADER DLL


.. py:data:: f_ELF

   Executable and Linkable Format (ELF)


.. py:data:: f_W32RUN

   Watcom DOS32 Extender (W32RUN)


.. py:data:: f_AOUT

   Linux a.out (AOUT)


.. py:data:: f_PRC

   PalmPilot program file.


.. py:data:: f_EXE

   MS DOS EXE File.


.. py:data:: f_COM

   MS DOS COM File.


.. py:data:: f_AIXAR

   AIX ar library.


.. py:data:: f_MACHO

   Mac OS X Mach-O.


.. py:data:: f_PSXOBJ

   Sony Playstation PSX object file.


.. py:data:: f_MD1IMG

   Mediatek Firmware Image.


.. py:function:: is_filetype_like_binary(ft: filetype_t) -> bool

   Is unstructured input file?


.. py:class:: compiler_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: id
      :type:  comp_t

      compiler id (see Compiler IDs)



   .. py:attribute:: cm
      :type:  cm_t

      memory model and calling convention (see CM) see also get_cc/set_cc 
              



   .. py:attribute:: size_i
      :type:  uchar

      sizeof(int)



   .. py:attribute:: size_b
      :type:  uchar

      sizeof(bool)



   .. py:attribute:: size_e
      :type:  uchar

      sizeof(enum)



   .. py:attribute:: defalign
      :type:  uchar

      default alignment for structures



   .. py:attribute:: size_s
      :type:  uchar

      short



   .. py:attribute:: size_l
      :type:  uchar

      long



   .. py:attribute:: size_ll
      :type:  uchar

      longlong



   .. py:attribute:: size_ldbl
      :type:  uchar

      longdouble (if different from processor_t::tbyte_size)



   .. py:method:: get_cc() -> callcnv_t


   .. py:method:: set_cc(cc: callcnv_t) -> None


.. py:data:: STT_CUR

   use current storage type (may be used only as a function argument)


.. py:data:: STT_VA

   regular storage: virtual arrays, an explicit flag for each byte


.. py:data:: STT_MM

   memory map: sparse storage. useful for huge objects


.. py:data:: STT_DBG

   memory map: temporary debugger storage. used internally


.. py:data:: IDAINFO_TAG_SIZE

   The database parameters. This structure is kept in the ida database. It contains the essential parameters for the current program 
           


.. py:data:: IDAINFO_PROCNAME_SIZE

.. py:data:: IDAINFO_STRLIT_PREF_SIZE

.. py:class:: idainfo(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: tag
      :type:  char [3]

      'IDA'



   .. py:attribute:: version
      :type:  ushort

      Version of database.



   .. py:attribute:: procname
      :type:  char [16]

      Name of the current processor (with \0)



   .. py:attribute:: s_genflags
      :type:  ushort

      General idainfo flags 
              



   .. py:attribute:: database_change_count
      :type:  int

      incremented after each byte and regular segment modifications 
              



   .. py:attribute:: filetype
      :type:  ushort

      The input file type.



   .. py:attribute:: ostype
      :type:  ushort

      OS type the program is for bit definitions in libfuncs.hpp 
              



   .. py:attribute:: apptype
      :type:  ushort

      Application type bit definitions in libfuncs.hpp 
              



   .. py:attribute:: asmtype
      :type:  uchar

      target assembler number



   .. py:attribute:: specsegs
      :type:  uchar

      What format do special segments use? 0-unspecified, 4-entries are 4 bytes, 8- entries are 8 bytes.



   .. py:attribute:: af
      :type:  int

      Analysis flags 
              



   .. py:attribute:: af2
      :type:  int

      Analysis flags 2 
              



   .. py:attribute:: baseaddr
      :type:  int

      remaining 28 bits are reserved

      base address of the program (paragraphs) 
              



   .. py:attribute:: start_ss
      :type:  sel_t

      selector of the initial stack segment



   .. py:attribute:: start_cs
      :type:  sel_t

      selector of the segment with the main entry point



   .. py:attribute:: start_ip
      :type:  ida_idaapi.ea_t

      IP register value at the start of program execution 
              



   .. py:attribute:: start_ea
      :type:  ida_idaapi.ea_t

      Linear address of program entry point.



   .. py:attribute:: start_sp
      :type:  ida_idaapi.ea_t

      SP register value at the start of program execution 
              



   .. py:attribute:: main
      :type:  ida_idaapi.ea_t

      address of main()



   .. py:attribute:: min_ea
      :type:  ida_idaapi.ea_t

      current limits of program



   .. py:attribute:: max_ea
      :type:  ida_idaapi.ea_t

      maxEA is excluded



   .. py:attribute:: omin_ea
      :type:  ida_idaapi.ea_t

      original minEA (is set after loading the input file)



   .. py:attribute:: omax_ea
      :type:  ida_idaapi.ea_t

      original maxEA (is set after loading the input file)



   .. py:attribute:: lowoff
      :type:  ida_idaapi.ea_t

      Low limit for offsets (used in calculation of 'void' operands) 
              



   .. py:attribute:: highoff
      :type:  ida_idaapi.ea_t

      High limit for offsets (used in calculation of 'void' operands) 
              



   .. py:attribute:: maxref
      :type:  int

      Max tail for references.



   .. py:attribute:: xrefnum
      :type:  uchar

      CROSS REFERENCES.

      Number of references to generate in the disassembly listing 0 - xrefs won't be generated at all 
              



   .. py:attribute:: type_xrefnum
      :type:  uchar

      Number of references to generate in the struct & enum windows 0 - xrefs won't be generated at all 
              



   .. py:attribute:: refcmtnum
      :type:  uchar

      Number of comment lines to generate for refs to string literals or demangled names 0 - such comments won't be generated at all 
              



   .. py:attribute:: s_xrefflag
      :type:  uchar

      Xref options 
              



   .. py:attribute:: max_autoname_len
      :type:  ushort

      NAMES.

      max autogenerated name length (without zero byte) 
              



   .. py:attribute:: nametype
      :type:  char

      Dummy names representation types 
              



   .. py:attribute:: short_demnames
      :type:  int

      short form of demangled names



   .. py:attribute:: long_demnames
      :type:  int

      long form of demangled names see demangle.h for definitions 
              



   .. py:attribute:: demnames
      :type:  uchar

      Demangled name flags 
              



   .. py:attribute:: listnames
      :type:  uchar

      Name list options 
              



   .. py:attribute:: indent
      :type:  uchar

      DISASSEMBLY LISTING DETAILS.

      Indentation for instructions 
              



   .. py:attribute:: cmt_indent
      :type:  uchar

      Indentation for comments.



   .. py:attribute:: margin
      :type:  ushort

      max length of data lines



   .. py:attribute:: lenxref
      :type:  ushort

      max length of line with xrefs



   .. py:attribute:: outflags
      :type:  int

      output flags 
              



   .. py:attribute:: s_cmtflg
      :type:  uchar

      Comment options 
              



   .. py:attribute:: s_limiter
      :type:  uchar

      Delimiter options 
              



   .. py:attribute:: bin_prefix_size
      :type:  short

      Number of instruction bytes (opcodes) to show in line prefix.



   .. py:attribute:: s_prefflag
      :type:  uchar

      Line prefix options 
              



   .. py:attribute:: strlit_flags
      :type:  uchar

      STRING LITERALS.

      string literal flags 
              



   .. py:attribute:: strlit_break
      :type:  uchar

      string literal line break symbol



   .. py:attribute:: strlit_zeroes
      :type:  char

      leading zeroes



   .. py:attribute:: strtype
      :type:  int

      current ascii string type see nalt.hpp for string types 
              



   .. py:attribute:: strlit_pref
      :type:  char [16]

      prefix for string literal names



   .. py:attribute:: strlit_sernum
      :type:  int

      serial number



   .. py:attribute:: datatypes
      :type:  int

      data types allowed in data carousel



   .. py:attribute:: cc
      :type:  compiler_info_t

      COMPILER.

      Target compiler 
              



   .. py:attribute:: abibits
      :type:  int

      ABI features. Depends on info returned by get_abi_name() Processor modules may modify them in set_compiler 
              



   .. py:attribute:: appcall_options
      :type:  int

      appcall options, see idd.hpp



   .. py:method:: get_abiname() -> str


   .. py:attribute:: abiname


   .. py:attribute:: lflags

      Misc. database flags 
              



   .. py:attribute:: minEA


   .. py:attribute:: maxEA


   .. py:attribute:: procName


.. py:data:: INFFL_AUTO

   Autoanalysis is enabled?


.. py:data:: INFFL_ALLASM

   may use constructs not supported by the target assembler 
           


.. py:data:: INFFL_LOADIDC

   loading an idc file that contains database info


.. py:data:: INFFL_NOUSER

   do not store user info in the database


.. py:data:: INFFL_READONLY

   (internal) temporary interdiction to modify the database


.. py:data:: INFFL_CHKOPS

   check manual operands? (unused)


.. py:data:: INFFL_NMOPS

   allow non-matched operands? (unused)


.. py:data:: INFFL_GRAPH_VIEW

   currently using graph options ( text_options_t::graph)


.. py:data:: LFLG_PC_FPP

   decode floating point processor instructions?


.. py:data:: LFLG_PC_FLAT

   32-bit program (or higher)?


.. py:data:: LFLG_64BIT

   64-bit program?


.. py:data:: LFLG_IS_DLL

   Is dynamic library?


.. py:data:: LFLG_FLAT_OFF32

   treat REF_OFF32 as 32-bit offset for 16bit segments (otherwise try SEG16:OFF16)


.. py:data:: LFLG_MSF

   Byte order: is MSB first?


.. py:data:: LFLG_WIDE_HBF

   Bit order of wide bytes: high byte first? (wide bytes: processor_t::dnbits > 8) 
           


.. py:data:: LFLG_DBG_NOPATH

   do not store input full path in debugger process options


.. py:data:: LFLG_SNAPSHOT

   memory snapshot was taken?


.. py:data:: LFLG_PACK

   pack the database?


.. py:data:: LFLG_COMPRESS

   compress the database?


.. py:data:: LFLG_KERNMODE

   is kernel mode binary?


.. py:data:: LFLG_ILP32

   64-bit instructions with 64-bit registers, but 32-bit pointers and address space. this bit is mutually exclusive with LFLG_64BIT 
           


.. py:data:: IDB_UNPACKED

   leave database components unpacked


.. py:data:: IDB_PACKED

   pack database components into .idb


.. py:data:: IDB_COMPRESSED

   compress & pack database components


.. py:data:: AF_CODE

   Trace execution flow.


.. py:data:: AF_MARKCODE

   Mark typical code sequences as code.


.. py:data:: AF_JUMPTBL

   Locate and create jump tables.


.. py:data:: AF_PURDAT

   Control flow to data segment is ignored.


.. py:data:: AF_USED

   Analyze and create all xrefs.


.. py:data:: AF_UNK

   Delete instructions with no xrefs.


.. py:data:: AF_PROCPTR

   Create function if data xref data->code32 exists.


.. py:data:: AF_PROC

   Create functions if call is present.


.. py:data:: AF_FTAIL

   Create function tails.


.. py:data:: AF_LVAR

   Create stack variables.


.. py:data:: AF_STKARG

   Propagate stack argument information.


.. py:data:: AF_REGARG

   Propagate register argument information.


.. py:data:: AF_TRACE

   Trace stack pointer.


.. py:data:: AF_VERSP

   Perform full SP-analysis. ( processor_t::verify_sp)


.. py:data:: AF_ANORET

   Perform 'no-return' analysis.


.. py:data:: AF_MEMFUNC

   Try to guess member function types.


.. py:data:: AF_TRFUNC

   Truncate functions upon code deletion.


.. py:data:: AF_STRLIT

   Create string literal if data xref exists.


.. py:data:: AF_CHKUNI

   Check for unicode strings.


.. py:data:: AF_FIXUP

   Create offsets and segments using fixup info.


.. py:data:: AF_DREFOFF

   Create offset if data xref to seg32 exists.


.. py:data:: AF_IMMOFF

   Convert 32bit instruction operand to offset.


.. py:data:: AF_DATOFF

   Automatically convert data to offsets.


.. py:data:: AF_FLIRT

   Use flirt signatures.


.. py:data:: AF_SIGCMT

   Append a signature name comment for recognized anonymous library functions.


.. py:data:: AF_SIGMLT

   Allow recognition of several copies of the same function.


.. py:data:: AF_HFLIRT

   Automatically hide library functions.


.. py:data:: AF_JFUNC

   Rename jump functions as j_...


.. py:data:: AF_NULLSUB

   Rename empty functions as nullsub_...


.. py:data:: AF_DODATA

   Coagulate data segs at the final pass.


.. py:data:: AF_DOCODE

   Coagulate code segs at the final pass.


.. py:data:: AF2_DOEH

   Handle EH information.


.. py:data:: AF2_DORTTI

   Handle RTTI information.


.. py:data:: AF2_MACRO

   Try to combine several instructions into a macro instruction 
           


.. py:data:: AF2_MERGESTR

   Merge string literals created using data xrefs 
           


.. py:data:: SW_SEGXRF

   show segments in xrefs?


.. py:data:: SW_XRFMRK

   show xref type marks?


.. py:data:: SW_XRFFNC

   show function offsets?


.. py:data:: SW_XRFVAL

   show xref values? (otherwise-"...")


.. py:data:: NM_REL_OFF

.. py:data:: NM_PTR_OFF

.. py:data:: NM_NAM_OFF

.. py:data:: NM_REL_EA

.. py:data:: NM_PTR_EA

.. py:data:: NM_NAM_EA

.. py:data:: NM_EA

.. py:data:: NM_EA4

.. py:data:: NM_EA8

.. py:data:: NM_SHORT

.. py:data:: NM_SERIAL

.. py:data:: DEMNAM_MASK

   mask for name form


.. py:data:: DEMNAM_CMNT

   display demangled names as comments


.. py:data:: DEMNAM_NAME

   display demangled names as regular names


.. py:data:: DEMNAM_NONE

   don't display demangled names


.. py:data:: DEMNAM_GCC3

   assume gcc3 names (valid for gnu compiler)


.. py:data:: DEMNAM_FIRST

   override type info


.. py:data:: LN_NORMAL

   include normal names


.. py:data:: LN_PUBLIC

   include public names


.. py:data:: LN_AUTO

   include autogenerated names


.. py:data:: LN_WEAK

   include weak names


.. py:data:: OFLG_SHOW_VOID

   Display void marks?


.. py:data:: OFLG_SHOW_AUTO

   Display autoanalysis indicator?


.. py:data:: OFLG_GEN_NULL

   Generate empty lines?


.. py:data:: OFLG_SHOW_PREF

   Show line prefixes?


.. py:data:: OFLG_PREF_SEG

   line prefixes with segment name?


.. py:data:: OFLG_LZERO

   generate leading zeroes in numbers


.. py:data:: OFLG_GEN_ORG

   Generate 'org' directives?


.. py:data:: OFLG_GEN_ASSUME

   Generate 'assume' directives?


.. py:data:: OFLG_GEN_TRYBLKS

   Generate try/catch directives?


.. py:data:: SCF_RPTCMT

   show repeatable comments?


.. py:data:: SCF_ALLCMT

   comment all lines?


.. py:data:: SCF_NOCMT

   no comments at all


.. py:data:: SCF_LINNUM

   show source line numbers


.. py:data:: SCF_TESTMODE

   testida.idc is running


.. py:data:: SCF_SHHID_ITEM

   show hidden instructions


.. py:data:: SCF_SHHID_FUNC

   show hidden functions


.. py:data:: SCF_SHHID_SEGM

   show hidden segments


.. py:data:: LMT_THIN

   thin borders


.. py:data:: LMT_THICK

   thick borders


.. py:data:: LMT_EMPTY

   empty lines at the end of basic blocks


.. py:data:: PREF_SEGADR

   show segment addresses?


.. py:data:: PREF_FNCOFF

   show function offsets?


.. py:data:: PREF_STACK

   show stack pointer?


.. py:data:: PREF_PFXTRUNC

   truncate instruction bytes if they would need more than 1 line


.. py:data:: STRF_GEN

   generate names?


.. py:data:: STRF_AUTO

   names have 'autogenerated' bit?


.. py:data:: STRF_SERIAL

   generate serial names?


.. py:data:: STRF_UNICODE

   unicode strings are present?


.. py:data:: STRF_COMMENT

   generate auto comment for string references?


.. py:data:: STRF_SAVECASE

   preserve case of strings for identifiers


.. py:data:: ABI_8ALIGN4

   4 byte alignment for 8byte scalars (__int64/double) inside structures?


.. py:data:: ABI_PACK_STKARGS

   do not align stack arguments to stack slots


.. py:data:: ABI_BIGARG_ALIGN

   use natural type alignment for argument if the alignment exceeds native word size. (e.g. __int64 argument should be 8byte aligned on some 32bit platforms) 
           


.. py:data:: ABI_STACK_LDBL

   long double arguments are passed on stack


.. py:data:: ABI_STACK_VARARGS

   varargs are always passed on stack (even when there are free registers)


.. py:data:: ABI_HARD_FLOAT

   use the floating-point register set


.. py:data:: ABI_SET_BY_USER

   compiler/abi were set by user flag and require SETCOMP_BY_USER flag to be changed


.. py:data:: ABI_GCC_LAYOUT

   use gcc layout for udts (used for mingw)


.. py:data:: ABI_MAP_STKARGS

   register arguments are mapped to stack area (and consume stack slots)


.. py:data:: ABI_HUGEARG_ALIGN

   use natural type alignment for an argument even if its alignment exceeds double native word size (the default is to use double word max). e.g. if this bit is set, __int128 has 16-byte alignment. this bit is not used by ida yet 
           


.. py:data:: INF_VERSION

.. py:data:: INF_PROCNAME

.. py:data:: INF_GENFLAGS

.. py:data:: INF_LFLAGS

.. py:data:: INF_DATABASE_CHANGE_COUNT

.. py:data:: INF_FILETYPE

.. py:data:: INF_OSTYPE

.. py:data:: INF_APPTYPE

.. py:data:: INF_ASMTYPE

.. py:data:: INF_SPECSEGS

.. py:data:: INF_AF

.. py:data:: INF_AF2

.. py:data:: INF_BASEADDR

.. py:data:: INF_START_SS

.. py:data:: INF_START_CS

.. py:data:: INF_START_IP

.. py:data:: INF_START_EA

.. py:data:: INF_START_SP

.. py:data:: INF_MAIN

.. py:data:: INF_MIN_EA

.. py:data:: INF_MAX_EA

.. py:data:: INF_OMIN_EA

.. py:data:: INF_OMAX_EA

.. py:data:: INF_LOWOFF

.. py:data:: INF_HIGHOFF

.. py:data:: INF_MAXREF

.. py:data:: INF_PRIVRANGE

.. py:data:: INF_PRIVRANGE_START_EA

.. py:data:: INF_PRIVRANGE_END_EA

.. py:data:: INF_NETDELTA

.. py:data:: INF_XREFNUM

.. py:data:: INF_TYPE_XREFNUM

.. py:data:: INF_REFCMTNUM

.. py:data:: INF_XREFFLAG

.. py:data:: INF_MAX_AUTONAME_LEN

.. py:data:: INF_NAMETYPE

.. py:data:: INF_SHORT_DEMNAMES

.. py:data:: INF_LONG_DEMNAMES

.. py:data:: INF_DEMNAMES

.. py:data:: INF_LISTNAMES

.. py:data:: INF_INDENT

.. py:data:: INF_CMT_INDENT

.. py:data:: INF_MARGIN

.. py:data:: INF_LENXREF

.. py:data:: INF_OUTFLAGS

.. py:data:: INF_CMTFLG

.. py:data:: INF_LIMITER

.. py:data:: INF_BIN_PREFIX_SIZE

.. py:data:: INF_PREFFLAG

.. py:data:: INF_STRLIT_FLAGS

.. py:data:: INF_STRLIT_BREAK

.. py:data:: INF_STRLIT_ZEROES

.. py:data:: INF_STRTYPE

.. py:data:: INF_STRLIT_PREF

.. py:data:: INF_STRLIT_SERNUM

.. py:data:: INF_DATATYPES

.. py:data:: INF_OBSOLETE_CC

.. py:data:: INF_CC_ID

.. py:data:: INF_CC_CM

.. py:data:: INF_CC_SIZE_I

.. py:data:: INF_CC_SIZE_B

.. py:data:: INF_CC_SIZE_E

.. py:data:: INF_CC_DEFALIGN

.. py:data:: INF_CC_SIZE_S

.. py:data:: INF_CC_SIZE_L

.. py:data:: INF_CC_SIZE_LL

.. py:data:: INF_CC_SIZE_LDBL

.. py:data:: INF_ABIBITS

.. py:data:: INF_APPCALL_OPTIONS

.. py:data:: INF_FILE_FORMAT_NAME

   file format name for loader modules


.. py:data:: INF_GROUPS

   segment group information (see init_groups())


.. py:data:: INF_H_PATH

   C header path.


.. py:data:: INF_C_MACROS

   C predefined macros.


.. py:data:: INF_INCLUDE

   assembler include file name


.. py:data:: INF_DUALOP_GRAPH

   Graph text representation options.


.. py:data:: INF_DUALOP_TEXT

   Text text representation options.


.. py:data:: INF_MD5

   MD5 of the input file.


.. py:data:: INF_IDA_VERSION

   version of ida which created the database


.. py:data:: INF_STR_ENCODINGS

   a list of encodings for the program strings


.. py:data:: INF_DBG_BINPATHS

   unused (20 indexes)


.. py:data:: INF_SHA256

   SHA256 of the input file.


.. py:data:: INF_ABINAME

   ABI name (processor specific)


.. py:data:: INF_ARCHIVE_PATH

   archive file path


.. py:data:: INF_PROBLEMS

   problem lists


.. py:data:: INF_SELECTORS

   2..63 are for selector_t blob (see init_selectors())


.. py:data:: INF_NOTEPAD

   notepad blob, occupies 1000 indexes (1MB of text)


.. py:data:: INF_SRCDBG_PATHS

   source debug paths, occupies 20 indexes


.. py:data:: INF_SRCDBG_UNDESIRED

   user-closed source files, occupies 20 indexes


.. py:data:: INF_INITIAL_VERSION

   initial version of database


.. py:data:: INF_CTIME

   database creation timestamp


.. py:data:: INF_ELAPSED

   seconds database stayed open


.. py:data:: INF_NOPENS

   how many times the database is opened


.. py:data:: INF_CRC32

   input file crc32


.. py:data:: INF_IMAGEBASE

   image base


.. py:data:: INF_IDSNODE

   ids modnode id (for import_module)


.. py:data:: INF_FSIZE

   input file size


.. py:data:: INF_OUTFILEENC

   output file encoding index


.. py:data:: INF_INPUT_FILE_PATH

.. py:data:: INF_COMPILER_INFO

.. py:data:: INF_CALLCNV

.. py:data:: INF_LAST

.. py:function:: getinf_str(tag: inftag_t) -> str

   Get program specific information (a non-scalar value) 
           
   :param tag: one of inftag_t constants
   :returns: number of bytes stored in the buffer (<0 - not defined)


.. py:function:: delinf(tag: inftag_t) -> bool

   Undefine a program specific information 
           
   :param tag: one of inftag_t constants
   :returns: success


.. py:function:: inf_get_version() -> ushort

.. py:function:: inf_set_version(_v: ushort) -> bool

.. py:function:: inf_get_genflags() -> ushort

.. py:function:: inf_set_genflags(_v: ushort) -> bool

.. py:function:: inf_is_auto_enabled() -> bool

.. py:function:: inf_set_auto_enabled(_v: bool = True) -> bool

.. py:function:: inf_use_allasm() -> bool

.. py:function:: inf_set_use_allasm(_v: bool = True) -> bool

.. py:function:: inf_loading_idc() -> bool

.. py:function:: inf_set_loading_idc(_v: bool = True) -> bool

.. py:function:: inf_no_store_user_info() -> bool

.. py:function:: inf_set_no_store_user_info(_v: bool = True) -> bool

.. py:function:: inf_readonly_idb() -> bool

.. py:function:: inf_set_readonly_idb(_v: bool = True) -> bool

.. py:function:: inf_check_manual_ops() -> bool

.. py:function:: inf_set_check_manual_ops(_v: bool = True) -> bool

.. py:function:: inf_allow_non_matched_ops() -> bool

.. py:function:: inf_set_allow_non_matched_ops(_v: bool = True) -> bool

.. py:function:: inf_is_graph_view() -> bool

.. py:function:: inf_set_graph_view(_v: bool = True) -> bool

.. py:function:: inf_get_lflags() -> int

.. py:function:: inf_set_lflags(_v: int) -> bool

.. py:function:: inf_decode_fpp() -> bool

.. py:function:: inf_set_decode_fpp(_v: bool = True) -> bool

.. py:function:: inf_is_32bit_or_higher() -> bool

.. py:function:: inf_is_32bit_exactly() -> bool

.. py:function:: inf_set_32bit(_v: bool = True) -> bool

.. py:function:: inf_is_16bit() -> bool

.. py:function:: inf_is_64bit() -> bool

.. py:function:: inf_set_64bit(_v: bool = True) -> bool

.. py:function:: inf_is_ilp32() -> bool

.. py:function:: inf_set_ilp32(_v: bool = True) -> bool

.. py:function:: inf_is_dll() -> bool

.. py:function:: inf_set_dll(_v: bool = True) -> bool

.. py:function:: inf_is_flat_off32() -> bool

.. py:function:: inf_set_flat_off32(_v: bool = True) -> bool

.. py:function:: inf_is_be() -> bool

.. py:function:: inf_set_be(_v: bool = True) -> bool

.. py:function:: inf_is_wide_high_byte_first() -> bool

.. py:function:: inf_set_wide_high_byte_first(_v: bool = True) -> bool

.. py:function:: inf_dbg_no_store_path() -> bool

.. py:function:: inf_set_dbg_no_store_path(_v: bool = True) -> bool

.. py:function:: inf_is_snapshot() -> bool

.. py:function:: inf_set_snapshot(_v: bool = True) -> bool

.. py:function:: inf_pack_idb() -> bool

.. py:function:: inf_set_pack_idb(_v: bool = True) -> bool

.. py:function:: inf_compress_idb() -> bool

.. py:function:: inf_set_compress_idb(_v: bool = True) -> bool

.. py:function:: inf_is_kernel_mode() -> bool

.. py:function:: inf_set_kernel_mode(_v: bool = True) -> bool

.. py:function:: inf_get_app_bitness() -> uint

.. py:function:: inf_set_app_bitness(bitness: uint) -> None

.. py:function:: inf_get_database_change_count() -> int

.. py:function:: inf_set_database_change_count(_v: int) -> bool

.. py:function:: inf_get_filetype() -> filetype_t

.. py:function:: inf_set_filetype(_v: filetype_t) -> bool

.. py:function:: inf_get_ostype() -> ushort

.. py:function:: inf_set_ostype(_v: ushort) -> bool

.. py:function:: inf_get_apptype() -> ushort

.. py:function:: inf_set_apptype(_v: ushort) -> bool

.. py:function:: inf_get_asmtype() -> uchar

.. py:function:: inf_set_asmtype(_v: uchar) -> bool

.. py:function:: inf_get_specsegs() -> uchar

.. py:function:: inf_set_specsegs(_v: uchar) -> bool

.. py:function:: inf_get_af() -> int

.. py:function:: inf_set_af(_v: int) -> bool

.. py:function:: inf_trace_flow() -> bool

.. py:function:: inf_set_trace_flow(_v: bool = True) -> bool

.. py:function:: inf_mark_code() -> bool

.. py:function:: inf_set_mark_code(_v: bool = True) -> bool

.. py:function:: inf_create_jump_tables() -> bool

.. py:function:: inf_set_create_jump_tables(_v: bool = True) -> bool

.. py:function:: inf_noflow_to_data() -> bool

.. py:function:: inf_set_noflow_to_data(_v: bool = True) -> bool

.. py:function:: inf_create_all_xrefs() -> bool

.. py:function:: inf_set_create_all_xrefs(_v: bool = True) -> bool

.. py:function:: inf_del_no_xref_insns() -> bool

.. py:function:: inf_set_del_no_xref_insns(_v: bool = True) -> bool

.. py:function:: inf_create_func_from_ptr() -> bool

.. py:function:: inf_set_create_func_from_ptr(_v: bool = True) -> bool

.. py:function:: inf_create_func_from_call() -> bool

.. py:function:: inf_set_create_func_from_call(_v: bool = True) -> bool

.. py:function:: inf_create_func_tails() -> bool

.. py:function:: inf_set_create_func_tails(_v: bool = True) -> bool

.. py:function:: inf_should_create_stkvars() -> bool

.. py:function:: inf_set_should_create_stkvars(_v: bool = True) -> bool

.. py:function:: inf_propagate_stkargs() -> bool

.. py:function:: inf_set_propagate_stkargs(_v: bool = True) -> bool

.. py:function:: inf_propagate_regargs() -> bool

.. py:function:: inf_set_propagate_regargs(_v: bool = True) -> bool

.. py:function:: inf_should_trace_sp() -> bool

.. py:function:: inf_set_should_trace_sp(_v: bool = True) -> bool

.. py:function:: inf_full_sp_ana() -> bool

.. py:function:: inf_set_full_sp_ana(_v: bool = True) -> bool

.. py:function:: inf_noret_ana() -> bool

.. py:function:: inf_set_noret_ana(_v: bool = True) -> bool

.. py:function:: inf_guess_func_type() -> bool

.. py:function:: inf_set_guess_func_type(_v: bool = True) -> bool

.. py:function:: inf_truncate_on_del() -> bool

.. py:function:: inf_set_truncate_on_del(_v: bool = True) -> bool

.. py:function:: inf_create_strlit_on_xref() -> bool

.. py:function:: inf_set_create_strlit_on_xref(_v: bool = True) -> bool

.. py:function:: inf_check_unicode_strlits() -> bool

.. py:function:: inf_set_check_unicode_strlits(_v: bool = True) -> bool

.. py:function:: inf_create_off_using_fixup() -> bool

.. py:function:: inf_set_create_off_using_fixup(_v: bool = True) -> bool

.. py:function:: inf_create_off_on_dref() -> bool

.. py:function:: inf_set_create_off_on_dref(_v: bool = True) -> bool

.. py:function:: inf_op_offset() -> bool

.. py:function:: inf_set_op_offset(_v: bool = True) -> bool

.. py:function:: inf_data_offset() -> bool

.. py:function:: inf_set_data_offset(_v: bool = True) -> bool

.. py:function:: inf_use_flirt() -> bool

.. py:function:: inf_set_use_flirt(_v: bool = True) -> bool

.. py:function:: inf_append_sigcmt() -> bool

.. py:function:: inf_set_append_sigcmt(_v: bool = True) -> bool

.. py:function:: inf_allow_sigmulti() -> bool

.. py:function:: inf_set_allow_sigmulti(_v: bool = True) -> bool

.. py:function:: inf_hide_libfuncs() -> bool

.. py:function:: inf_set_hide_libfuncs(_v: bool = True) -> bool

.. py:function:: inf_rename_jumpfunc() -> bool

.. py:function:: inf_set_rename_jumpfunc(_v: bool = True) -> bool

.. py:function:: inf_rename_nullsub() -> bool

.. py:function:: inf_set_rename_nullsub(_v: bool = True) -> bool

.. py:function:: inf_coagulate_data() -> bool

.. py:function:: inf_set_coagulate_data(_v: bool = True) -> bool

.. py:function:: inf_coagulate_code() -> bool

.. py:function:: inf_set_coagulate_code(_v: bool = True) -> bool

.. py:function:: inf_final_pass() -> bool

.. py:function:: inf_set_final_pass(_v: bool = True) -> bool

.. py:function:: inf_get_af2() -> int

.. py:function:: inf_set_af2(_v: int) -> bool

.. py:function:: inf_handle_eh() -> bool

.. py:function:: inf_set_handle_eh(_v: bool = True) -> bool

.. py:function:: inf_handle_rtti() -> bool

.. py:function:: inf_set_handle_rtti(_v: bool = True) -> bool

.. py:function:: inf_macros_enabled() -> bool

.. py:function:: inf_set_macros_enabled(_v: bool = True) -> bool

.. py:function:: inf_merge_strlits() -> bool

.. py:function:: inf_set_merge_strlits(_v: bool = True) -> bool

.. py:function:: inf_get_baseaddr() -> int

.. py:function:: inf_set_baseaddr(_v: int) -> bool

.. py:function:: inf_get_start_ss() -> sel_t

.. py:function:: inf_set_start_ss(_v: sel_t) -> bool

.. py:function:: inf_get_start_cs() -> sel_t

.. py:function:: inf_set_start_cs(_v: sel_t) -> bool

.. py:function:: inf_get_start_ip() -> ida_idaapi.ea_t

.. py:function:: inf_set_start_ip(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_start_ea() -> ida_idaapi.ea_t

.. py:function:: inf_set_start_ea(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_start_sp() -> ida_idaapi.ea_t

.. py:function:: inf_set_start_sp(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_main() -> ida_idaapi.ea_t

.. py:function:: inf_set_main(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_min_ea() -> ida_idaapi.ea_t

.. py:function:: inf_set_min_ea(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_max_ea() -> ida_idaapi.ea_t

.. py:function:: inf_set_max_ea(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_omin_ea() -> ida_idaapi.ea_t

.. py:function:: inf_set_omin_ea(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_omax_ea() -> ida_idaapi.ea_t

.. py:function:: inf_set_omax_ea(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_lowoff() -> ida_idaapi.ea_t

.. py:function:: inf_set_lowoff(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_highoff() -> ida_idaapi.ea_t

.. py:function:: inf_set_highoff(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_maxref() -> int

.. py:function:: inf_set_maxref(_v: int) -> bool

.. py:function:: inf_get_netdelta() -> int

.. py:function:: inf_set_netdelta(_v: int) -> bool

.. py:function:: inf_get_xrefnum() -> uchar

.. py:function:: inf_set_xrefnum(_v: uchar) -> bool

.. py:function:: inf_get_type_xrefnum() -> uchar

.. py:function:: inf_set_type_xrefnum(_v: uchar) -> bool

.. py:function:: inf_get_refcmtnum() -> uchar

.. py:function:: inf_set_refcmtnum(_v: uchar) -> bool

.. py:function:: inf_get_xrefflag() -> uchar

.. py:function:: inf_set_xrefflag(_v: uchar) -> bool

.. py:function:: inf_show_xref_seg() -> bool

.. py:function:: inf_set_show_xref_seg(_v: bool = True) -> bool

.. py:function:: inf_show_xref_tmarks() -> bool

.. py:function:: inf_set_show_xref_tmarks(_v: bool = True) -> bool

.. py:function:: inf_show_xref_fncoff() -> bool

.. py:function:: inf_set_show_xref_fncoff(_v: bool = True) -> bool

.. py:function:: inf_show_xref_val() -> bool

.. py:function:: inf_set_show_xref_val(_v: bool = True) -> bool

.. py:function:: inf_get_max_autoname_len() -> ushort

.. py:function:: inf_set_max_autoname_len(_v: ushort) -> bool

.. py:function:: inf_get_nametype() -> char

.. py:function:: inf_set_nametype(_v: char) -> bool

.. py:function:: inf_get_short_demnames() -> int

.. py:function:: inf_set_short_demnames(_v: int) -> bool

.. py:function:: inf_get_long_demnames() -> int

.. py:function:: inf_set_long_demnames(_v: int) -> bool

.. py:function:: inf_get_demnames() -> uchar

.. py:function:: inf_set_demnames(_v: uchar) -> bool

.. py:function:: inf_get_listnames() -> uchar

.. py:function:: inf_set_listnames(_v: uchar) -> bool

.. py:function:: inf_get_indent() -> uchar

.. py:function:: inf_set_indent(_v: uchar) -> bool

.. py:function:: inf_get_cmt_indent() -> uchar

.. py:function:: inf_set_cmt_indent(_v: uchar) -> bool

.. py:function:: inf_get_margin() -> ushort

.. py:function:: inf_set_margin(_v: ushort) -> bool

.. py:function:: inf_get_lenxref() -> ushort

.. py:function:: inf_set_lenxref(_v: ushort) -> bool

.. py:function:: inf_get_outflags() -> int

.. py:function:: inf_set_outflags(_v: int) -> bool

.. py:function:: inf_show_void() -> bool

.. py:function:: inf_set_show_void(_v: bool = True) -> bool

.. py:function:: inf_show_auto() -> bool

.. py:function:: inf_set_show_auto(_v: bool = True) -> bool

.. py:function:: inf_gen_null() -> bool

.. py:function:: inf_set_gen_null(_v: bool = True) -> bool

.. py:function:: inf_show_line_pref() -> bool

.. py:function:: inf_set_show_line_pref(_v: bool = True) -> bool

.. py:function:: inf_line_pref_with_seg() -> bool

.. py:function:: inf_set_line_pref_with_seg(_v: bool = True) -> bool

.. py:function:: inf_gen_lzero() -> bool

.. py:function:: inf_set_gen_lzero(_v: bool = True) -> bool

.. py:function:: inf_gen_org() -> bool

.. py:function:: inf_set_gen_org(_v: bool = True) -> bool

.. py:function:: inf_gen_assume() -> bool

.. py:function:: inf_set_gen_assume(_v: bool = True) -> bool

.. py:function:: inf_gen_tryblks() -> bool

.. py:function:: inf_set_gen_tryblks(_v: bool = True) -> bool

.. py:function:: inf_get_cmtflg() -> uchar

.. py:function:: inf_set_cmtflg(_v: uchar) -> bool

.. py:function:: inf_show_repeatables() -> bool

.. py:function:: inf_set_show_repeatables(_v: bool = True) -> bool

.. py:function:: inf_show_all_comments() -> bool

.. py:function:: inf_set_show_all_comments(_v: bool = True) -> bool

.. py:function:: inf_hide_comments() -> bool

.. py:function:: inf_set_hide_comments(_v: bool = True) -> bool

.. py:function:: inf_show_src_linnum() -> bool

.. py:function:: inf_set_show_src_linnum(_v: bool = True) -> bool

.. py:function:: inf_test_mode() -> bool

.. py:function:: inf_show_hidden_insns() -> bool

.. py:function:: inf_set_show_hidden_insns(_v: bool = True) -> bool

.. py:function:: inf_show_hidden_funcs() -> bool

.. py:function:: inf_set_show_hidden_funcs(_v: bool = True) -> bool

.. py:function:: inf_show_hidden_segms() -> bool

.. py:function:: inf_set_show_hidden_segms(_v: bool = True) -> bool

.. py:function:: inf_get_limiter() -> uchar

.. py:function:: inf_set_limiter(_v: uchar) -> bool

.. py:function:: inf_is_limiter_thin() -> bool

.. py:function:: inf_set_limiter_thin(_v: bool = True) -> bool

.. py:function:: inf_is_limiter_thick() -> bool

.. py:function:: inf_set_limiter_thick(_v: bool = True) -> bool

.. py:function:: inf_is_limiter_empty() -> bool

.. py:function:: inf_set_limiter_empty(_v: bool = True) -> bool

.. py:function:: inf_get_bin_prefix_size() -> short

.. py:function:: inf_set_bin_prefix_size(_v: short) -> bool

.. py:function:: inf_get_prefflag() -> uchar

.. py:function:: inf_set_prefflag(_v: uchar) -> bool

.. py:function:: inf_prefix_show_segaddr() -> bool

.. py:function:: inf_set_prefix_show_segaddr(_v: bool = True) -> bool

.. py:function:: inf_prefix_show_funcoff() -> bool

.. py:function:: inf_set_prefix_show_funcoff(_v: bool = True) -> bool

.. py:function:: inf_prefix_show_stack() -> bool

.. py:function:: inf_set_prefix_show_stack(_v: bool = True) -> bool

.. py:function:: inf_prefix_truncate_opcode_bytes() -> bool

.. py:function:: inf_set_prefix_truncate_opcode_bytes(_v: bool = True) -> bool

.. py:function:: inf_get_strlit_flags() -> uchar

.. py:function:: inf_set_strlit_flags(_v: uchar) -> bool

.. py:function:: inf_strlit_names() -> bool

.. py:function:: inf_set_strlit_names(_v: bool = True) -> bool

.. py:function:: inf_strlit_name_bit() -> bool

.. py:function:: inf_set_strlit_name_bit(_v: bool = True) -> bool

.. py:function:: inf_strlit_serial_names() -> bool

.. py:function:: inf_set_strlit_serial_names(_v: bool = True) -> bool

.. py:function:: inf_unicode_strlits() -> bool

.. py:function:: inf_set_unicode_strlits(_v: bool = True) -> bool

.. py:function:: inf_strlit_autocmt() -> bool

.. py:function:: inf_set_strlit_autocmt(_v: bool = True) -> bool

.. py:function:: inf_strlit_savecase() -> bool

.. py:function:: inf_set_strlit_savecase(_v: bool = True) -> bool

.. py:function:: inf_get_strlit_break() -> uchar

.. py:function:: inf_set_strlit_break(_v: uchar) -> bool

.. py:function:: inf_get_strlit_zeroes() -> char

.. py:function:: inf_set_strlit_zeroes(_v: char) -> bool

.. py:function:: inf_get_strtype() -> int

.. py:function:: inf_set_strtype(_v: int) -> bool

.. py:function:: inf_get_strlit_sernum() -> int

.. py:function:: inf_set_strlit_sernum(_v: int) -> bool

.. py:function:: inf_get_datatypes() -> int

.. py:function:: inf_set_datatypes(_v: int) -> bool

.. py:function:: inf_get_abibits() -> int

.. py:function:: inf_set_abibits(_v: int) -> bool

.. py:function:: inf_is_mem_aligned4() -> bool

.. py:function:: inf_set_mem_aligned4(_v: bool = True) -> bool

.. py:function:: inf_pack_stkargs(*args) -> bool

.. py:function:: inf_set_pack_stkargs(_v: bool = True) -> bool

.. py:function:: inf_big_arg_align(*args) -> bool

.. py:function:: inf_set_big_arg_align(_v: bool = True) -> bool

.. py:function:: inf_stack_ldbl() -> bool

.. py:function:: inf_set_stack_ldbl(_v: bool = True) -> bool

.. py:function:: inf_stack_varargs() -> bool

.. py:function:: inf_set_stack_varargs(_v: bool = True) -> bool

.. py:function:: inf_is_hard_float() -> bool

.. py:function:: inf_set_hard_float(_v: bool = True) -> bool

.. py:function:: inf_abi_set_by_user() -> bool

.. py:function:: inf_set_abi_set_by_user(_v: bool = True) -> bool

.. py:function:: inf_use_gcc_layout() -> bool

.. py:function:: inf_set_use_gcc_layout(_v: bool = True) -> bool

.. py:function:: inf_map_stkargs() -> bool

.. py:function:: inf_set_map_stkargs(_v: bool = True) -> bool

.. py:function:: inf_huge_arg_align(*args) -> bool

.. py:function:: inf_set_huge_arg_align(_v: bool = True) -> bool

.. py:function:: inf_get_appcall_options() -> int

.. py:function:: inf_set_appcall_options(_v: int) -> bool

.. py:function:: inf_get_privrange_start_ea() -> ida_idaapi.ea_t

.. py:function:: inf_set_privrange_start_ea(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_privrange_end_ea() -> ida_idaapi.ea_t

.. py:function:: inf_set_privrange_end_ea(_v: ida_idaapi.ea_t) -> bool

.. py:function:: inf_get_cc_id() -> comp_t

.. py:function:: inf_set_cc_id(_v: comp_t) -> bool

.. py:function:: inf_get_cc_cm() -> cm_t

.. py:function:: inf_set_cc_cm(_v: cm_t) -> bool

.. py:function:: inf_get_callcnv() -> callcnv_t

.. py:function:: inf_set_callcnv(_v: callcnv_t) -> bool

.. py:function:: inf_get_cc_size_i() -> uchar

.. py:function:: inf_set_cc_size_i(_v: uchar) -> bool

.. py:function:: inf_get_cc_size_b() -> uchar

.. py:function:: inf_set_cc_size_b(_v: uchar) -> bool

.. py:function:: inf_get_cc_size_e() -> uchar

.. py:function:: inf_set_cc_size_e(_v: uchar) -> bool

.. py:function:: inf_get_cc_defalign() -> uchar

.. py:function:: inf_set_cc_defalign(_v: uchar) -> bool

.. py:function:: inf_get_cc_size_s() -> uchar

.. py:function:: inf_set_cc_size_s(_v: uchar) -> bool

.. py:function:: inf_get_cc_size_l() -> uchar

.. py:function:: inf_set_cc_size_l(_v: uchar) -> bool

.. py:function:: inf_get_cc_size_ll() -> uchar

.. py:function:: inf_set_cc_size_ll(_v: uchar) -> bool

.. py:function:: inf_get_cc_size_ldbl() -> uchar

.. py:function:: inf_set_cc_size_ldbl(_v: uchar) -> bool

.. py:function:: inf_get_procname() -> str

.. py:function:: inf_set_procname(*args) -> bool

.. py:function:: inf_get_strlit_pref() -> str

.. py:function:: inf_set_strlit_pref(*args) -> bool

.. py:function:: inf_get_cc(out: compiler_info_t) -> bool

.. py:function:: inf_set_cc(_v: compiler_info_t) -> bool

.. py:function:: inf_set_privrange(_v: range_t) -> bool

.. py:function:: inf_get_privrange(*args) -> range_t

   This function has the following signatures:

       0. inf_get_privrange(out: range_t *) -> bool
       1. inf_get_privrange() -> range_t

   # 0: inf_get_privrange(out: range_t *) -> bool


   # 1: inf_get_privrange() -> range_t


.. py:function:: inf_get_af_low() -> ushort

   Get/set low/high 16bit halves of inf.af.


.. py:function:: inf_set_af_low(saf: ushort) -> None

.. py:function:: inf_get_af_high() -> ushort

.. py:function:: inf_set_af_high(saf2: ushort) -> None

.. py:function:: inf_get_af2_low() -> ushort

   Get/set low 16bit half of inf.af2.


.. py:function:: inf_set_af2_low(saf: ushort) -> None

.. py:function:: inf_get_pack_mode() -> int

.. py:function:: inf_set_pack_mode(pack_mode: int) -> int

.. py:function:: inf_inc_database_change_count(cnt: int = 1) -> None

.. py:function:: inf_get_demname_form() -> uchar

   Get DEMNAM_MASK bits of #demnames.


.. py:function:: inf_postinc_strlit_sernum(cnt: int = 1) -> int

.. py:function:: inf_like_binary() -> bool

.. py:data:: UA_MAXOP

   max number of operands allowed for an instruction


.. py:function:: calc_default_idaplace_flags() -> int

   Get default disassembly line options.


.. py:function:: to_ea(reg_cs: sel_t, reg_ip: int) -> ida_idaapi.ea_t

   Convert (sel,off) value to a linear address.


.. py:data:: IDB_EXT32

.. py:data:: IDB_EXT64

.. py:data:: IDB_EXT

.. py:function:: get_dbctx_id() -> ssize_t

   Get the current database context ID 
           
   :returns: the database context ID, or -1 if no current database


.. py:function:: get_dbctx_qty() -> size_t

   Get number of database contexts 
           
   :returns: number of database contexts


.. py:function:: switch_dbctx(idx: size_t) -> dbctx_t *

   Switch to the database with the provided context ID 
           
   :param idx: the index of the database to switch to
   :returns: the current dbctx_t instance or nullptr


.. py:function:: is_database_busy() -> bool

   Check if the database is busy (e.g. performing some critical operations and cannot be safely accessed) 
           


.. py:function:: validate_idb(vld_flags: int = 0) -> size_t

   Validate the database 
           
   :param vld_flags: combination of VLD_.. constants
   :returns: number of corrupted/fixed records


.. py:data:: VLD_AUTO_REPAIR

   automatically repair the database


.. py:data:: VLD_DIALOG

   ask user to repair (this bit is mutually exclusive with VLD_AUTO_REPAIR)


.. py:data:: VLD_SILENT

   no messages to the output window


.. py:function:: move_privrange(new_privrange_start: ida_idaapi.ea_t) -> bool

   Move privrange to the specified address 
           
   :param new_privrange_start: new start address of the privrange
   :returns: success


.. py:class:: idbattr_valmap_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: value
      :type:  uint64


   .. py:attribute:: valname
      :type:  str


.. py:class:: idbattr_info_t(name: str, offset: uintptr_t, width: size_t, bitmask: uint64 = 0, tag: uchar = 0, idi_flags: uint = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str

      human-readable name. if null, then the field will not be merged as part of INF. 
              



   .. py:attribute:: offset
      :type:  uintptr_t

      field position: offset within a structure (IDI_STRUCFLD) altval or supval index (IDI_NODEVAL) hashval name (IDI_ALTVAL/IDI_SUPVAL+IDI_HASH) 
              



   .. py:attribute:: width
      :type:  size_t

      field width in bytes



   .. py:attribute:: bitmask
      :type:  uint64

      mask for bitfields (0-not bitfield)



   .. py:attribute:: tag
      :type:  uchar

      tag of node value (if IDI_NODEVAL is set)



   .. py:attribute:: vmap
      :type:  idbattr_valmap_t const *

      array value=>name (terminated by empty element)



   .. py:attribute:: individual_node
      :type:  str

      individual node name (nullptr - use default)



   .. py:attribute:: idi_flags
      :type:  uint


   .. py:attribute:: maxsize
      :type:  int

      max bytes reserved for storage in netnode



   .. py:method:: is_node_altval() -> bool


   .. py:method:: is_node_supval() -> bool


   .. py:method:: is_node_valobj() -> bool


   .. py:method:: is_node_blob() -> bool


   .. py:method:: is_node_var() -> bool


   .. py:method:: is_struc_field() -> bool


   .. py:method:: is_cstr() -> bool


   .. py:method:: is_qstring() -> bool


   .. py:method:: is_bytearray() -> bool


   .. py:method:: is_buf_var() -> bool


   .. py:method:: is_decimal() -> bool


   .. py:method:: is_hexadecimal() -> bool


   .. py:method:: is_readonly_var() -> bool


   .. py:method:: is_incremented() -> bool


   .. py:method:: is_val_mapped() -> bool


   .. py:method:: is_hash() -> bool


   .. py:method:: use_hlpstruc() -> bool


   .. py:method:: is_bitmap() -> bool


   .. py:method:: is_onoff() -> bool


   .. py:method:: is_scalar_var() -> bool


   .. py:method:: is_bitfield() -> bool


   .. py:method:: is_boolean() -> bool


   .. py:method:: has_individual_node() -> bool


   .. py:method:: str_true() -> str


   .. py:method:: str_false() -> str


   .. py:method:: ridx() -> size_t


   .. py:method:: hashname() -> str


.. py:data:: IDI_STRUCFLD

   structure field (opposite to IDI_NODEVAL)


.. py:data:: IDI_ALTVAL

   netnode: altval


.. py:data:: IDI_SUPVAL

   netnode: supval


.. py:data:: IDI_VALOBJ

   netnode: valobj


.. py:data:: IDI_BLOB

   netnode: blob


.. py:data:: IDI_SCALAR

   scalar value (default)


.. py:data:: IDI_CSTR

   string


.. py:data:: IDI_QSTRING

   qstring


.. py:data:: IDI_BYTEARRAY

   byte array: binary representation


.. py:data:: IDI_EA_HEX

   default representation: hex or "BADADDR"


.. py:data:: IDI_DEC

   show as decimal


.. py:data:: IDI_HEX

   show as hexadecimal


.. py:data:: IDI_INC

   stored value is incremented (scalars only)


.. py:data:: IDI_MAP_VAL

   apply ea2node() to value


.. py:data:: IDI_HASH

   hashed node field, hash name in offset


.. py:data:: IDI_HLPSTRUC

   call helper for pointer to structure


.. py:data:: IDI_READONLY

   read-only field (cannot be modified)


.. py:data:: IDI_BITMAP

   bitmap field: interpret bitmask as bit number


.. py:data:: IDI_ONOFF

   show boolean as on/off (not true/false)


.. py:data:: IDI_NOMERGE

   field should not be merged as part of INF


.. py:data:: IDI_NODEVAL

.. py:data:: IDI_BUFVAR

.. py:data:: idainfo_big_arg_align

.. py:data:: idainfo_gen_null

.. py:data:: idainfo_set_gen_null

.. py:data:: idainfo_gen_lzero

.. py:data:: idainfo_set_gen_lzero

.. py:data:: idainfo_gen_tryblks

.. py:data:: idainfo_set_gen_tryblks

.. py:data:: idainfo_get_demname_form

.. py:data:: idainfo_get_pack_mode

.. py:data:: idainfo_set_pack_mode

.. py:function:: idainfo_is_32bit()

.. py:data:: idainfo_is_64bit

.. py:data:: idainfo_set_64bit

.. py:data:: idainfo_is_auto_enabled

.. py:data:: idainfo_set_auto_enabled

.. py:data:: idainfo_is_be

.. py:data:: idainfo_set_be

.. py:data:: idainfo_is_dll

.. py:data:: idainfo_is_flat_off32

.. py:data:: idainfo_is_graph_view

.. py:data:: idainfo_set_graph_view

.. py:data:: idainfo_is_hard_float

.. py:data:: idainfo_is_kernel_mode

.. py:data:: idainfo_is_mem_aligned4

.. py:data:: idainfo_is_snapshot

.. py:data:: idainfo_is_wide_high_byte_first

.. py:data:: idainfo_set_wide_high_byte_first

.. py:data:: idainfo_like_binary

.. py:data:: idainfo_line_pref_with_seg

.. py:data:: idainfo_set_line_pref_with_seg

.. py:data:: idainfo_show_auto

.. py:data:: idainfo_set_show_auto

.. py:data:: idainfo_show_line_pref

.. py:data:: idainfo_set_show_line_pref

.. py:data:: idainfo_show_void

.. py:data:: idainfo_set_show_void

.. py:data:: idainfo_loading_idc

.. py:data:: idainfo_map_stkargs

.. py:data:: idainfo_pack_stkargs

.. py:data:: idainfo_readonly_idb

.. py:data:: idainfo_set_store_user_info

.. py:data:: idainfo_stack_ldbl

.. py:data:: idainfo_stack_varargs

.. py:data:: idainfo_use_allasm

.. py:data:: idainfo_use_gcc_layout

.. py:data:: macros_enabled

.. py:data:: should_create_stkvars

.. py:data:: should_trace_sp

.. py:data:: show_all_comments

.. py:data:: show_comments

.. py:data:: show_repeatables

.. py:data:: inf_get_comment

.. py:data:: inf_set_comment

.. py:data:: idainfo_comment_get

.. py:data:: idainfo_comment_set


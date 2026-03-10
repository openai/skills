idc
===

.. py:module:: idc

.. autoapi-nested-parse::

   IDC compatibility module

   This file contains IDA built-in function declarations and internal bit
   definitions.  Each byte of the program has 32-bit flags (low 8 bits keep
   the byte value). These 32 bits are used in get_full_flags/get_flags functions.

   This file is subject to change without any notice.
   Future versions of IDA may use other definitions.



Attributes
----------

.. autoapisummary::

   idc.WORDMASK
   idc.BADADDR
   idc.BADSEL
   idc.SIZE_MAX
   idc.MS_VAL
   idc.FF_IVL
   idc.MS_CLS
   idc.FF_CODE
   idc.FF_DATA
   idc.FF_TAIL
   idc.FF_UNK
   idc.MS_COMM
   idc.FF_COMM
   idc.FF_REF
   idc.FF_LINE
   idc.FF_NAME
   idc.FF_LABL
   idc.FF_FLOW
   idc.FF_ANYNAME
   idc.MS_0TYPE
   idc.FF_0VOID
   idc.FF_0NUMH
   idc.FF_0NUMD
   idc.FF_0CHAR
   idc.FF_0SEG
   idc.FF_0OFF
   idc.FF_0NUMB
   idc.FF_0NUMO
   idc.FF_0ENUM
   idc.FF_0FOP
   idc.FF_0STRO
   idc.FF_0STK
   idc.MS_1TYPE
   idc.FF_1VOID
   idc.FF_1NUMH
   idc.FF_1NUMD
   idc.FF_1CHAR
   idc.FF_1SEG
   idc.FF_1OFF
   idc.FF_1NUMB
   idc.FF_1NUMO
   idc.FF_1ENUM
   idc.FF_1FOP
   idc.FF_1STRO
   idc.FF_1STK
   idc.DT_TYPE
   idc.FF_BYTE
   idc.FF_WORD
   idc.FF_DWORD
   idc.FF_QWORD
   idc.FF_TBYTE
   idc.FF_STRLIT
   idc.FF_STRUCT
   idc.FF_OWORD
   idc.FF_FLOAT
   idc.FF_DOUBLE
   idc.FF_PACKREAL
   idc.FF_ALIGN
   idc.MS_CODE
   idc.FF_FUNC
   idc.FF_IMMD
   idc.FF_JUMP
   idc.NEF_SEGS
   idc.NEF_RSCS
   idc.NEF_NAME
   idc.NEF_MAN
   idc.NEF_FILL
   idc.NEF_IMPS
   idc.NEF_FIRST
   idc.NEF_CODE
   idc.NEF_RELOAD
   idc.NEF_FLAT
   idc.IDCHK_OK
   idc.IDCHK_ARG
   idc.IDCHK_KEY
   idc.IDCHK_MAX
   idc.add_idc_hotkey
   idc.del_idc_hotkey
   idc.jumpto
   idc.auto_wait
   idc.DBFL_BAK
   idc.qexit
   idc.load_and_run_plugin
   idc.plan_to_apply_idasgn
   idc.create_insn
   idc.SN_CHECK
   idc.SN_NOCHECK
   idc.SN_PUBLIC
   idc.SN_NON_PUBLIC
   idc.SN_WEAK
   idc.SN_NON_WEAK
   idc.SN_AUTO
   idc.SN_NON_AUTO
   idc.SN_NOLIST
   idc.SN_NOWARN
   idc.SN_LOCAL
   idc.set_cmt
   idc.create_data
   idc.create_custom_data
   idc.create_align
   idc.del_items
   idc.DELIT_SIMPLE
   idc.DELIT_EXPAND
   idc.DELIT_DELNAMES
   idc.AP_ALLOWDUPS
   idc.AP_SIGNED
   idc.AP_INDEX
   idc.AP_ARRAY
   idc.AP_IDXBASEMASK
   idc.AP_IDXDEC
   idc.AP_IDXHEX
   idc.AP_IDXOCT
   idc.AP_IDXBIN
   idc.op_bin
   idc.op_oct
   idc.op_dec
   idc.op_hex
   idc.op_chr
   idc.OPND_OUTER
   idc.op_offset
   idc.REF_OFF8
   idc.REF_OFF16
   idc.REF_OFF32
   idc.REF_LOW8
   idc.REF_LOW16
   idc.REF_HIGH8
   idc.REF_HIGH16
   idc.REF_OFF64
   idc.REFINFO_RVA
   idc.REFINFO_PASTEND
   idc.REFINFO_NOBASE
   idc.REFINFO_SUBTRACT
   idc.REFINFO_SIGNEDOP
   idc.op_seg
   idc.op_num
   idc.op_flt
   idc.op_man
   idc.toggle_sign
   idc.op_enum
   idc.op_stkvar
   idc.E_PREV
   idc.E_NEXT
   idc.get_extra_cmt
   idc.update_extra_cmt
   idc.del_extra_cmt
   idc.set_manual_insn
   idc.get_manual_insn
   idc.patch_dbg_byte
   idc.patch_byte
   idc.patch_word
   idc.patch_dword
   idc.patch_qword
   idc.SR_inherit
   idc.SR_user
   idc.SR_auto
   idc.SR_autostart
   idc.auto_mark_range
   idc.auto_unmark
   idc.AU_UNK
   idc.AU_CODE
   idc.AU_PROC
   idc.AU_USED
   idc.AU_LIBF
   idc.AU_FINAL
   idc.OFILE_MAP
   idc.OFILE_EXE
   idc.OFILE_IDC
   idc.OFILE_LST
   idc.OFILE_ASM
   idc.OFILE_DIF
   idc.GENFLG_MAPSEG
   idc.GENFLG_MAPNAME
   idc.GENFLG_MAPDMNG
   idc.GENFLG_MAPLOC
   idc.GENFLG_IDCTYPE
   idc.GENFLG_ASMTYPE
   idc.GENFLG_GENHTML
   idc.GENFLG_ASMINC
   idc.CHART_PRINT_NAMES
   idc.CHART_GEN_GDL
   idc.CHART_WINGRAPH
   idc.CHART_NOLIBFUNCS
   idc.get_root_filename
   idc.get_input_file_path
   idc.set_root_filename
   idc.retrieve_input_file_md5
   idc.get_full_flags
   idc.get_db_byte
   idc.get_wide_byte
   idc.read_dbg_memory
   idc.get_original_byte
   idc.get_wide_word
   idc.get_wide_dword
   idc.get_qword
   idc.get_name_ea
   idc.get_screen_ea
   idc.next_addr
   idc.prev_addr
   idc.next_not_tail
   idc.prev_not_tail
   idc.get_item_head
   idc.get_item_end
   idc.GN_VISIBLE
   idc.GN_COLORED
   idc.GN_DEMANGLED
   idc.GN_STRICT
   idc.GN_SHORT
   idc.GN_LONG
   idc.GN_LOCAL
   idc.GN_ISRET
   idc.GN_NOT_ISRET
   idc.calc_gtn_flags
   idc.GENDSM_FORCE_CODE
   idc.GENDSM_MULTI_LINE
   idc.o_void
   idc.o_reg
   idc.o_mem
   idc.o_phrase
   idc.o_displ
   idc.o_imm
   idc.o_far
   idc.o_near
   idc.o_idpspec0
   idc.o_idpspec1
   idc.o_idpspec2
   idc.o_idpspec3
   idc.o_idpspec4
   idc.o_idpspec5
   idc.o_trreg
   idc.o_dbreg
   idc.o_crreg
   idc.o_fpreg
   idc.o_mmxreg
   idc.o_xmmreg
   idc.o_reglist
   idc.o_creglist
   idc.o_creg
   idc.o_fpreglist
   idc.o_text
   idc.o_cond
   idc.o_spr
   idc.o_twofpr
   idc.o_shmbme
   idc.o_crf
   idc.o_crb
   idc.o_dcr
   idc.GetCommentEx
   idc.get_cmt
   idc.get_forced_operand
   idc.BPU_1B
   idc.BPU_2B
   idc.BPU_4B
   idc.STRWIDTH_1B
   idc.STRWIDTH_2B
   idc.STRWIDTH_4B
   idc.STRWIDTH_MASK
   idc.STRLYT_TERMCHR
   idc.STRLYT_PASCAL1
   idc.STRLYT_PASCAL2
   idc.STRLYT_PASCAL4
   idc.STRLYT_MASK
   idc.STRLYT_SHIFT
   idc.STRTYPE_TERMCHR
   idc.STRTYPE_C
   idc.STRTYPE_C_16
   idc.STRTYPE_C_32
   idc.STRTYPE_PASCAL
   idc.STRTYPE_PASCAL_16
   idc.STRTYPE_LEN2
   idc.STRTYPE_LEN2_16
   idc.STRTYPE_LEN4
   idc.STRTYPE_LEN4_16
   idc.STRTYPE_C16
   idc.find_suspop
   idc.find_code
   idc.find_data
   idc.find_unknown
   idc.find_defined
   idc.find_imm
   idc.find_text
   idc.find_bytes
   idc.INF_VERSION
   idc.INF_PROCNAME
   idc.INF_GENFLAGS
   idc.INF_LFLAGS
   idc.INF_DATABASE_CHANGE_COUNT
   idc.INF_CHANGE_COUNTER
   idc.INF_FILETYPE
   idc.FT_EXE_OLD
   idc.FT_COM_OLD
   idc.FT_BIN
   idc.FT_DRV
   idc.FT_WIN
   idc.FT_HEX
   idc.FT_MEX
   idc.FT_LX
   idc.FT_LE
   idc.FT_NLM
   idc.FT_COFF
   idc.FT_PE
   idc.FT_OMF
   idc.FT_SREC
   idc.FT_ZIP
   idc.FT_OMFLIB
   idc.FT_AR
   idc.FT_LOADER
   idc.FT_ELF
   idc.FT_W32RUN
   idc.FT_AOUT
   idc.FT_PRC
   idc.FT_EXE
   idc.FT_COM
   idc.FT_AIXAR
   idc.FT_MACHO
   idc.INF_OSTYPE
   idc.OSTYPE_MSDOS
   idc.OSTYPE_WIN
   idc.OSTYPE_OS2
   idc.OSTYPE_NETW
   idc.INF_APPTYPE
   idc.APPT_CONSOLE
   idc.APPT_GRAPHIC
   idc.APPT_PROGRAM
   idc.APPT_LIBRARY
   idc.APPT_DRIVER
   idc.APPT_1THREAD
   idc.APPT_MTHREAD
   idc.APPT_16BIT
   idc.APPT_32BIT
   idc.INF_ASMTYPE
   idc.INF_SPECSEGS
   idc.INF_AF
   idc.INF_AF2
   idc.INF_BASEADDR
   idc.INF_START_SS
   idc.INF_START_CS
   idc.INF_START_IP
   idc.INF_START_EA
   idc.INF_START_SP
   idc.INF_MAIN
   idc.INF_MIN_EA
   idc.INF_MAX_EA
   idc.INF_OMIN_EA
   idc.INF_OMAX_EA
   idc.INF_LOWOFF
   idc.INF_LOW_OFF
   idc.INF_HIGHOFF
   idc.INF_HIGH_OFF
   idc.INF_MAXREF
   idc.INF_PRIVRANGE_START_EA
   idc.INF_START_PRIVRANGE
   idc.INF_PRIVRANGE_END_EA
   idc.INF_END_PRIVRANGE
   idc.INF_NETDELTA
   idc.INF_XREFNUM
   idc.INF_TYPE_XREFNUM
   idc.INF_TYPE_XREFS
   idc.INF_REFCMTNUM
   idc.INF_REFCMTS
   idc.INF_XREFFLAG
   idc.INF_XREFS
   idc.INF_MAX_AUTONAME_LEN
   idc.INF_NAMETYPE
   idc.INF_SHORT_DEMNAMES
   idc.INF_SHORT_DN
   idc.INF_LONG_DEMNAMES
   idc.INF_LONG_DN
   idc.INF_DEMNAMES
   idc.INF_LISTNAMES
   idc.INF_INDENT
   idc.INF_CMT_INDENT
   idc.INF_COMMENT
   idc.INF_MARGIN
   idc.INF_LENXREF
   idc.INF_OUTFLAGS
   idc.INF_CMTFLG
   idc.INF_CMTFLAG
   idc.INF_LIMITER
   idc.INF_BORDER
   idc.INF_BIN_PREFIX_SIZE
   idc.INF_BINPREF
   idc.INF_PREFFLAG
   idc.INF_STRLIT_FLAGS
   idc.INF_STRLIT_BREAK
   idc.INF_STRLIT_ZEROES
   idc.INF_STRTYPE
   idc.INF_STRLIT_PREF
   idc.INF_STRLIT_SERNUM
   idc.INF_DATATYPES
   idc.INF_CC_ID
   idc.COMP_MASK
   idc.COMP_UNK
   idc.COMP_MS
   idc.COMP_BC
   idc.COMP_WATCOM
   idc.COMP_GNU
   idc.COMP_VISAGE
   idc.COMP_BP
   idc.INF_CC_CM
   idc.INF_CC_SIZE_I
   idc.INF_CC_SIZE_B
   idc.INF_CC_SIZE_E
   idc.INF_CC_DEFALIGN
   idc.INF_CC_SIZE_S
   idc.INF_CC_SIZE_L
   idc.INF_CC_SIZE_LL
   idc.INF_CC_SIZE_LDBL
   idc.INF_COMPILER
   idc.INF_MODEL
   idc.INF_SIZEOF_INT
   idc.INF_SIZEOF_BOOL
   idc.INF_SIZEOF_ENUM
   idc.INF_SIZEOF_ALGN
   idc.INF_SIZEOF_SHORT
   idc.INF_SIZEOF_LONG
   idc.INF_SIZEOF_LLONG
   idc.INF_SIZEOF_LDBL
   idc.INF_ABIBITS
   idc.INF_APPCALL_OPTIONS
   idc.set_processor_type
   idc.SETPROC_IDB
   idc.SETPROC_LOADER
   idc.SETPROC_LOADER_NON_FATAL
   idc.SETPROC_USER
   idc.set_target_assembler
   idc.ask_seg
   idc.ask_yn
   idc.msg
   idc.warning
   idc.error
   idc.set_ida_state
   idc.IDA_STATUS_READY
   idc.IDA_STATUS_THINKING
   idc.IDA_STATUS_WAITING
   idc.IDA_STATUS_WORK
   idc.refresh_idaview_anyway
   idc.refresh_lists
   idc.set_selector
   idc.del_selector
   idc.ADDSEG_NOSREG
   idc.ADDSEG_OR_DIE
   idc.ADDSEG_NOTRUNC
   idc.ADDSEG_QUIET
   idc.ADDSEG_FILLGAP
   idc.ADDSEG_SPARSE
   idc.del_segm
   idc.SEGMOD_KILL
   idc.SEGMOD_KEEP
   idc.SEGMOD_SILENT
   idc.saAbs
   idc.saRelByte
   idc.saRelWord
   idc.saRelPara
   idc.saRelPage
   idc.saRelDble
   idc.saRel4K
   idc.saGroup
   idc.saRel32Bytes
   idc.saRel64Bytes
   idc.saRelQword
   idc.scPriv
   idc.scPub
   idc.scPub2
   idc.scStack
   idc.scCommon
   idc.scPub3
   idc.SEG_NORM
   idc.SEG_XTRN
   idc.SEG_CODE
   idc.SEG_DATA
   idc.SEG_IMP
   idc.SEG_GRP
   idc.SEG_NULL
   idc.SEG_UNDF
   idc.SEG_BSS
   idc.SEG_ABSSYM
   idc.SEG_COMM
   idc.SEG_IMEM
   idc.SEGATTR_START
   idc.SEGATTR_END
   idc.SEGATTR_ORGBASE
   idc.SEGATTR_ALIGN
   idc.SEGATTR_COMB
   idc.SEGATTR_PERM
   idc.SEGATTR_BITNESS
   idc.SEGATTR_FLAGS
   idc.SEGATTR_SEL
   idc.SEGATTR_ES
   idc.SEGATTR_CS
   idc.SEGATTR_SS
   idc.SEGATTR_DS
   idc.SEGATTR_FS
   idc.SEGATTR_GS
   idc.SEGATTR_TYPE
   idc.SEGATTR_COLOR
   idc.SEGATTR_START
   idc.SFL_COMORG
   idc.SFL_OBOK
   idc.SFL_HIDDEN
   idc.SFL_DEBUG
   idc.SFL_LOADER
   idc.SFL_HIDETYPE
   idc.MSF_SILENT
   idc.MSF_NOFIX
   idc.MSF_LDKEEP
   idc.MSF_FIXONCE
   idc.MOVE_SEGM_OK
   idc.MOVE_SEGM_PARAM
   idc.MOVE_SEGM_ROOM
   idc.MOVE_SEGM_IDP
   idc.MOVE_SEGM_CHUNK
   idc.MOVE_SEGM_LOADER
   idc.MOVE_SEGM_ODD
   idc.MOVE_SEGM_ORPHAN
   idc.MOVE_SEGM_DEBUG
   idc.MOVE_SEGM_SOURCEFILES
   idc.MOVE_SEGM_MAPPING
   idc.MOVE_SEGM_INVAL
   idc.rebase_program
   idc.set_storage_type
   idc.STT_VA
   idc.STT_MM
   idc.fl_CF
   idc.fl_CN
   idc.fl_JF
   idc.fl_JN
   idc.fl_F
   idc.XREF_USER
   idc.add_cref
   idc.del_cref
   idc.get_first_cref_from
   idc.get_next_cref_from
   idc.get_first_cref_to
   idc.get_next_cref_to
   idc.get_first_fcref_from
   idc.get_next_fcref_from
   idc.get_first_fcref_to
   idc.get_next_fcref_to
   idc.dr_O
   idc.dr_W
   idc.dr_R
   idc.dr_T
   idc.dr_I
   idc.add_dref
   idc.del_dref
   idc.get_first_dref_from
   idc.get_next_dref_from
   idc.get_first_dref_to
   idc.get_next_dref_to
   idc.add_func
   idc.del_func
   idc.set_func_end
   idc.FUNCATTR_START
   idc.FUNCATTR_END
   idc.FUNCATTR_FLAGS
   idc.FUNCATTR_FRAME
   idc.FUNCATTR_FRSIZE
   idc.FUNCATTR_FRREGS
   idc.FUNCATTR_ARGSIZE
   idc.FUNCATTR_FPD
   idc.FUNCATTR_COLOR
   idc.FUNCATTR_OWNER
   idc.FUNCATTR_REFQTY
   idc.FUNCATTR_START
   idc.FUNC_NORET
   idc.FUNC_FAR
   idc.FUNC_LIB
   idc.FUNC_STATIC
   idc.FUNC_FRAME
   idc.FUNC_USERFAR
   idc.FUNC_HIDDEN
   idc.FUNC_THUNK
   idc.FUNC_BOTTOMBP
   idc.FUNC_NORET_PENDING
   idc.FUNC_SP_READY
   idc.FUNC_PURGED_OK
   idc.FUNC_TAIL
   idc.FUNC_LUMINA
   idc.FUNC_OUTLINE
   idc.get_fchunk_referer
   idc.add_user_stkpnt
   idc.recalc_spd
   idc.get_entry_qty
   idc.add_entry
   idc.get_entry_ordinal
   idc.get_entry
   idc.get_entry_name
   idc.rename_entry
   idc.get_next_fixup_ea
   idc.get_prev_fixup_ea
   idc.FIXUP_OFF8
   idc.FIXUP_OFF16
   idc.FIXUP_SEG16
   idc.FIXUP_PTR32
   idc.FIXUP_OFF32
   idc.FIXUP_PTR48
   idc.FIXUP_HI8
   idc.FIXUP_HI16
   idc.FIXUP_LOW8
   idc.FIXUP_LOW16
   idc.FIXUP_OFF64
   idc.FIXUP_CUSTOM
   idc.FIXUPF_REL
   idc.FIXUPF_EXTDEF
   idc.FIXUPF_UNUSED
   idc.FIXUPF_CREATED
   idc.del_fixup
   idc.put_bookmark
   idc.get_bookmark
   idc.get_bookmark_desc
   idc.ENFL_REGEX
   idc.AR_LONG
   idc.AR_STR
   idc.add_sourcefile
   idc.get_sourcefile
   idc.del_sourcefile
   idc.set_source_linnum
   idc.get_source_linnum
   idc.del_source_linnum
   idc.SizeOf
   idc.TINFO_GUESSED
   idc.TINFO_DEFINITE
   idc.TINFO_DELAYFUNC
   idc.PT_SIL
   idc.PT_NDC
   idc.PT_TYP
   idc.PT_VAR
   idc.PT_PACKMASK
   idc.PT_HIGH
   idc.PT_LOWER
   idc.PT_REPLACE
   idc.PT_RAWARGS
   idc.PT_SILENT
   idc.PT_PAKDEF
   idc.PT_PAK1
   idc.PT_PAK2
   idc.PT_PAK4
   idc.PT_PAK8
   idc.PT_PAK16
   idc.PT_FILE
   idc.PT_STANDALONE
   idc.PDF_INCL_DEPS
   idc.PDF_DEF_FWD
   idc.PDF_DEF_BASE
   idc.PDF_HEADER_CMT
   idc.PRTYPE_1LINE
   idc.PRTYPE_MULTI
   idc.PRTYPE_TYPE
   idc.PRTYPE_PRAGMA
   idc.PRTYPE_SEMI
   idc.PRTYPE_CPP
   idc.PRTYPE_DEF
   idc.PRTYPE_NOARGS
   idc.PRTYPE_NOARRS
   idc.PRTYPE_NORES
   idc.PRTYPE_RESTORE
   idc.PRTYPE_NOREGEX
   idc.PRTYPE_COLORED
   idc.PRTYPE_METHODS
   idc.PRTYPE_1LINCMT
   idc.add_hidden_range
   idc.del_hidden_range
   idc.load_debugger
   idc.start_process
   idc.exit_process
   idc.suspend_process
   idc.get_processes
   idc.attach_process
   idc.detach_process
   idc.get_thread_qty
   idc.getn_thread
   idc.get_current_thread
   idc.getn_thread_name
   idc.select_thread
   idc.suspend_thread
   idc.resume_thread
   idc.step_into
   idc.step_over
   idc.run_to
   idc.step_until_ret
   idc.wait_for_next_event
   idc.WFNE_ANY
   idc.WFNE_SUSP
   idc.WFNE_SILENT
   idc.WFNE_CONT
   idc.WFNE_NOWAIT
   idc.NOTASK
   idc.DBG_ERROR
   idc.DBG_TIMEOUT
   idc.PROCESS_STARTED
   idc.PROCESS_EXITED
   idc.THREAD_STARTED
   idc.THREAD_EXITED
   idc.BREAKPOINT
   idc.STEP
   idc.EXCEPTION
   idc.LIB_LOADED
   idc.LIB_UNLOADED
   idc.INFORMATION
   idc.PROCESS_ATTACHED
   idc.PROCESS_DETACHED
   idc.PROCESS_SUSPENDED
   idc.refresh_debugger_memory
   idc.take_memory_snapshot
   idc.get_process_state
   idc.DSTATE_SUSP
   idc.DSTATE_NOTASK
   idc.DSTATE_RUN
   idc.DSTATE_RUN_WAIT_ATTACH
   idc.DSTATE_RUN_WAIT_END
   idc.set_debugger_options
   idc.DOPT_SEGM_MSGS
   idc.DOPT_START_BPT
   idc.DOPT_THREAD_MSGS
   idc.DOPT_THREAD_BPT
   idc.DOPT_BPT_MSGS
   idc.DOPT_LIB_MSGS
   idc.DOPT_LIB_BPT
   idc.DOPT_INFO_MSGS
   idc.DOPT_INFO_BPT
   idc.DOPT_REAL_MEMORY
   idc.DOPT_REDO_STACK
   idc.DOPT_ENTRY_BPT
   idc.DOPT_EXCDLG
   idc.EXCDLG_NEVER
   idc.EXCDLG_UNKNOWN
   idc.EXCDLG_ALWAYS
   idc.DOPT_LOAD_DINFO
   idc.get_debugger_event_cond
   idc.set_debugger_event_cond
   idc.set_remote_debugger
   idc.define_exception
   idc.EXC_BREAK
   idc.EXC_HANDLE
   idc.get_reg_value
   idc.get_bpt_qty
   idc.BPTATTR_EA
   idc.BPTATTR_SIZE
   idc.BPTATTR_TYPE
   idc.BPT_WRITE
   idc.BPT_RDWR
   idc.BPT_SOFT
   idc.BPT_EXEC
   idc.BPT_DEFAULT
   idc.BPTATTR_COUNT
   idc.BPTATTR_FLAGS
   idc.BPT_BRK
   idc.BPT_TRACE
   idc.BPT_UPDMEM
   idc.BPT_ENABLED
   idc.BPT_LOWCND
   idc.BPT_TRACEON
   idc.BPT_TRACE_INSN
   idc.BPT_TRACE_FUNC
   idc.BPT_TRACE_BBLK
   idc.BPTATTR_COND
   idc.BPTATTR_PID
   idc.BPTATTR_TID
   idc.BPLT_ABS
   idc.BPLT_REL
   idc.BPLT_SYM
   idc.add_bpt
   idc.del_bpt
   idc.enable_bpt
   idc.check_bpt
   idc.BPTCK_NONE
   idc.BPTCK_NO
   idc.BPTCK_YES
   idc.BPTCK_ACT
   idc.TRACE_STEP
   idc.TRACE_INSN
   idc.TRACE_FUNC
   idc.get_step_trace_options
   idc.set_step_trace_options
   idc.ST_OVER_DEBUG_SEG
   idc.ST_OVER_LIB_FUNC
   idc.ST_ALREADY_LOGGED
   idc.ST_SKIP_LOOPS
   idc.load_trace_file
   idc.save_trace_file
   idc.is_valid_trace_file
   idc.diff_trace_file
   idc.get_trace_file_desc
   idc.set_trace_file_desc
   idc.get_tev_qty
   idc.get_tev_ea
   idc.TEV_NONE
   idc.TEV_INSN
   idc.TEV_CALL
   idc.TEV_RET
   idc.TEV_BPT
   idc.TEV_MEM
   idc.TEV_EVENT
   idc.get_tev_type
   idc.get_tev_tid
   idc.get_tev_reg
   idc.get_tev_mem_qty
   idc.get_tev_mem
   idc.get_tev_mem_ea
   idc.get_call_tev_callee
   idc.get_ret_tev_return
   idc.get_bpt_tev_ea
   idc.CIC_ITEM
   idc.CIC_FUNC
   idc.CIC_SEGM
   idc.DEFCOLOR
   idc.ARGV


Exceptions
----------

.. autoapisummary::

   idc.DeprecatedIDCError


Functions
---------

.. autoapisummary::

   idc.has_value
   idc.byte_value
   idc.is_loaded
   idc.is_code
   idc.is_data
   idc.is_tail
   idc.is_unknown
   idc.is_head
   idc.is_flow
   idc.isExtra
   idc.isRef
   idc.hasName
   idc.hasUserName
   idc.is_defarg0
   idc.is_defarg1
   idc.isDec0
   idc.isDec1
   idc.isHex0
   idc.isHex1
   idc.isOct0
   idc.isOct1
   idc.isBin0
   idc.isBin1
   idc.is_off0
   idc.is_off1
   idc.is_char0
   idc.is_char1
   idc.is_seg0
   idc.is_seg1
   idc.is_enum0
   idc.is_enum1
   idc.is_manual0
   idc.is_manual1
   idc.is_stroff0
   idc.is_stroff1
   idc.is_stkvar0
   idc.is_stkvar1
   idc.is_byte
   idc.is_word
   idc.is_dword
   idc.is_qword
   idc.is_oword
   idc.is_tbyte
   idc.is_float
   idc.is_double
   idc.is_pack_real
   idc.is_strlit
   idc.is_struct
   idc.is_align
   idc.value_is_string
   idc.value_is_long
   idc.value_is_float
   idc.value_is_func
   idc.value_is_pvoid
   idc.value_is_int64
   idc.to_ea
   idc.form
   idc.substr
   idc.strstr
   idc.strlen
   idc.xtol
   idc.atoa
   idc.ltoa
   idc.atol
   idc.rotate_left
   idc.rotate_dword
   idc.rotate_word
   idc.rotate_byte
   idc.eval_idc
   idc.EVAL_FAILURE
   idc.save_database
   idc.validate_idb_names
   idc.call_system
   idc.qsleep
   idc.delete_all_segments
   idc.plan_and_wait
   idc.set_name
   idc.make_array
   idc.create_strlit
   idc.create_byte
   idc.create_word
   idc.create_dword
   idc.create_qword
   idc.create_oword
   idc.create_yword
   idc.create_float
   idc.create_double
   idc.create_pack_real
   idc.create_tbyte
   idc.create_struct
   idc.define_local_var
   idc.set_array_params
   idc.op_plain_offset
   idc.toggle_bnot
   idc.op_stroff
   idc.op_offset_high16
   idc.MakeVar
   idc.split_sreg_range
   idc.AutoMark
   idc.gen_file
   idc.gen_flow_graph
   idc.gen_simple_call_chart
   idc.idadir
   idc.get_idb_path
   idc.get_bytes
   idc.read_dbg_byte
   idc.read_dbg_word
   idc.read_dbg_dword
   idc.read_dbg_qword
   idc.write_dbg_memory
   idc.GetFloat
   idc.GetDouble
   idc.get_name_ea_simple
   idc.get_segm_by_sel
   idc.get_curline
   idc.read_selection_start
   idc.read_selection_end
   idc.get_sreg
   idc.next_head
   idc.prev_head
   idc.get_item_size
   idc.func_contains
   idc.get_name
   idc.demangle_name
   idc.generate_disasm_line
   idc.GetDisasm
   idc.print_insn_mnem
   idc.print_operand
   idc.get_operand_type
   idc.get_operand_value
   idc.get_strlit_contents
   idc.get_str_type
   idc.process_config_line
   idc.get_inf_attr
   idc.set_inf_attr
   idc.SetPrcsr
   idc.get_processor_name
   idc.batch
   idc.process_ui_action
   idc.sel2para
   idc.find_selector
   idc.get_first_seg
   idc.get_next_seg
   idc.get_segm_start
   idc.get_segm_end
   idc.get_segm_name
   idc.add_segm_ex
   idc.AddSeg
   idc.set_segment_bounds
   idc.set_segm_name
   idc.set_segm_class
   idc.set_segm_alignment
   idc.set_segm_combination
   idc.set_segm_addressing
   idc.selector_by_name
   idc.set_default_sreg_value
   idc.set_segm_type
   idc.get_segm_attr
   idc.set_segm_attr
   idc.move_segm
   idc.get_xref_type
   idc.fopen
   idc.fclose
   idc.filelength
   idc.fseek
   idc.ftell
   idc.LoadFile
   idc.loadfile
   idc.SaveFile
   idc.savefile
   idc.fgetc
   idc.fputc
   idc.fprintf
   idc.readshort
   idc.readlong
   idc.writeshort
   idc.writelong
   idc.readstr
   idc.writestr
   idc.get_next_func
   idc.get_prev_func
   idc.get_func_attr
   idc.set_func_attr
   idc.get_func_flags
   idc.set_func_flags
   idc.get_func_name
   idc.get_func_cmt
   idc.set_func_cmt
   idc.choose_func
   idc.get_func_off_str
   idc.find_func_end
   idc.get_frame_id
   idc.get_frame_lvar_size
   idc.get_frame_regs_size
   idc.get_frame_args_size
   idc.get_frame_size
   idc.set_frame_size
   idc.get_spd
   idc.get_sp_delta
   idc.get_fchunk_attr
   idc.set_fchunk_attr
   idc.get_next_fchunk
   idc.get_prev_fchunk
   idc.append_func_tail
   idc.remove_fchunk
   idc.set_tail_owner
   idc.first_func_chunk
   idc.next_func_chunk
   idc.add_auto_stkpnt
   idc.del_stkpnt
   idc.get_min_spd_ea
   idc.get_fixup_target_type
   idc.get_fixup_target_flags
   idc.get_fixup_target_sel
   idc.get_fixup_target_off
   idc.get_fixup_target_dis
   idc.set_fixup
   idc.get_struc_id
   idc.get_struc_name
   idc.get_struc_cmt
   idc.get_struc_size
   idc.get_member_qty
   idc.get_member_by_idx
   idc.is_member_id
   idc.get_member_id
   idc.get_member_offset
   idc.get_member_name
   idc.get_member_cmt
   idc.get_member_size
   idc.get_member_strid
   idc.is_union
   idc.add_struc
   idc.del_struc
   idc.set_struc_name
   idc.set_struc_cmt
   idc.add_struc_member
   idc.del_struc_member
   idc.set_member_name
   idc.set_member_type
   idc.set_member_cmt
   idc.expand_struc
   idc.get_enum
   idc.get_enum_name
   idc.get_enum_cmt
   idc.get_enum_size
   idc.get_enum_width
   idc.get_enum_flag
   idc.get_enum_member_by_name
   idc.get_enum_member_enum
   idc.get_enum_member
   idc.get_first_bmask
   idc.get_last_bmask
   idc.get_next_bmask
   idc.get_prev_bmask
   idc.get_bmask_name
   idc.get_bmask_cmt
   idc.set_bmask_name
   idc.set_bmask_cmt
   idc.get_first_enum_member
   idc.get_last_enum_member
   idc.get_next_enum_member
   idc.get_prev_enum_member
   idc.get_enum_member_name
   idc.get_enum_member_cmt
   idc.get_enum_member_value
   idc.get_enum_member_bmask
   idc.add_enum
   idc.del_enum
   idc.set_enum_name
   idc.set_enum_flag
   idc.set_enum_width
   idc.is_bf
   idc.set_enum_bf
   idc.set_enum_cmt
   idc.add_enum_member
   idc.del_enum_member
   idc.set_enum_member_name
   idc.set_enum_member_cmt
   idc.create_array
   idc.get_array_id
   idc.rename_array
   idc.delete_array
   idc.set_array_long
   idc.set_array_string
   idc.get_array_element
   idc.del_array_element
   idc.get_first_index
   idc.get_last_index
   idc.get_next_index
   idc.get_prev_index
   idc.set_hash_long
   idc.get_hash_long
   idc.set_hash_string
   idc.get_hash_string
   idc.del_hash_string
   idc.get_first_hash_key
   idc.get_last_hash_key
   idc.get_next_hash_key
   idc.get_prev_hash_key
   idc.add_default_til
   idc.import_type
   idc.get_type
   idc.sizeof
   idc.get_tinfo
   idc.get_local_tinfo
   idc.guess_type
   idc.apply_type
   idc.SetType
   idc.parse_decl
   idc.parse_decls
   idc.print_decls
   idc.get_ordinal_limit
   idc.set_local_type
   idc.GetLocalType
   idc.get_numbered_type_name
   idc.update_hidden_range
   idc.get_first_module
   idc.get_next_module
   idc.get_module_name
   idc.get_module_size
   idc.resume_process
   idc.send_dbg_command
   idc.get_event_id
   idc.get_event_pid
   idc.get_event_tid
   idc.get_event_ea
   idc.is_event_handled
   idc.get_event_module_name
   idc.get_event_module_base
   idc.get_event_module_size
   idc.get_event_exit_code
   idc.get_event_info
   idc.get_event_bpt_hea
   idc.get_event_exc_code
   idc.get_event_exc_ea
   idc.can_exc_continue
   idc.get_event_exc_info
   idc.set_reg_value
   idc.get_bpt_ea
   idc.get_bpt_attr
   idc.set_bpt_attr
   idc.set_bpt_cond
   idc.enable_tracing
   idc.clear_trace
   idc.get_color
   idc.set_color
   idc.force_bl_jump
   idc.force_bl_call
   idc.set_flag
   idc.here
   idc.is_mapped


Module Contents
---------------

.. py:data:: WORDMASK
   :value: 18446744073709551615


.. py:exception:: DeprecatedIDCError

   Bases: :py:obj:`Exception`


   Exception for deprecated function calls


.. py:data:: BADADDR

.. py:data:: BADSEL

.. py:data:: SIZE_MAX

.. py:data:: MS_VAL

.. py:data:: FF_IVL

.. py:function:: has_value(F)

.. py:function:: byte_value(F)

   Get byte value from flags
   Get value of byte provided that the byte is initialized.
   This macro works ok only for 8-bit byte machines.


.. py:function:: is_loaded(ea)

   Is the byte initialized?


.. py:data:: MS_CLS

.. py:data:: FF_CODE

.. py:data:: FF_DATA

.. py:data:: FF_TAIL

.. py:data:: FF_UNK

.. py:function:: is_code(F)

.. py:function:: is_data(F)

.. py:function:: is_tail(F)

.. py:function:: is_unknown(F)

.. py:function:: is_head(F)

.. py:data:: MS_COMM

.. py:data:: FF_COMM

.. py:data:: FF_REF

.. py:data:: FF_LINE

.. py:data:: FF_NAME

.. py:data:: FF_LABL

.. py:data:: FF_FLOW

.. py:data:: FF_ANYNAME

.. py:function:: is_flow(F)

.. py:function:: isExtra(F)

.. py:function:: isRef(F)

.. py:function:: hasName(F)

.. py:function:: hasUserName(F)

.. py:data:: MS_0TYPE

.. py:data:: FF_0VOID

.. py:data:: FF_0NUMH

.. py:data:: FF_0NUMD

.. py:data:: FF_0CHAR

.. py:data:: FF_0SEG

.. py:data:: FF_0OFF

.. py:data:: FF_0NUMB

.. py:data:: FF_0NUMO

.. py:data:: FF_0ENUM

.. py:data:: FF_0FOP

.. py:data:: FF_0STRO

.. py:data:: FF_0STK

.. py:data:: MS_1TYPE

.. py:data:: FF_1VOID

.. py:data:: FF_1NUMH

.. py:data:: FF_1NUMD

.. py:data:: FF_1CHAR

.. py:data:: FF_1SEG

.. py:data:: FF_1OFF

.. py:data:: FF_1NUMB

.. py:data:: FF_1NUMO

.. py:data:: FF_1ENUM

.. py:data:: FF_1FOP

.. py:data:: FF_1STRO

.. py:data:: FF_1STK

.. py:function:: is_defarg0(F)

.. py:function:: is_defarg1(F)

.. py:function:: isDec0(F)

.. py:function:: isDec1(F)

.. py:function:: isHex0(F)

.. py:function:: isHex1(F)

.. py:function:: isOct0(F)

.. py:function:: isOct1(F)

.. py:function:: isBin0(F)

.. py:function:: isBin1(F)

.. py:function:: is_off0(F)

.. py:function:: is_off1(F)

.. py:function:: is_char0(F)

.. py:function:: is_char1(F)

.. py:function:: is_seg0(F)

.. py:function:: is_seg1(F)

.. py:function:: is_enum0(F)

.. py:function:: is_enum1(F)

.. py:function:: is_manual0(F)

.. py:function:: is_manual1(F)

.. py:function:: is_stroff0(F)

.. py:function:: is_stroff1(F)

.. py:function:: is_stkvar0(F)

.. py:function:: is_stkvar1(F)

.. py:data:: DT_TYPE

.. py:data:: FF_BYTE

.. py:data:: FF_WORD

.. py:data:: FF_DWORD

.. py:data:: FF_QWORD

.. py:data:: FF_TBYTE

.. py:data:: FF_STRLIT

.. py:data:: FF_STRUCT

.. py:data:: FF_OWORD

.. py:data:: FF_FLOAT

.. py:data:: FF_DOUBLE

.. py:data:: FF_PACKREAL

.. py:data:: FF_ALIGN

.. py:function:: is_byte(F)

.. py:function:: is_word(F)

.. py:function:: is_dword(F)

.. py:function:: is_qword(F)

.. py:function:: is_oword(F)

.. py:function:: is_tbyte(F)

.. py:function:: is_float(F)

.. py:function:: is_double(F)

.. py:function:: is_pack_real(F)

.. py:function:: is_strlit(F)

.. py:function:: is_struct(F)

.. py:function:: is_align(F)

.. py:data:: MS_CODE

.. py:data:: FF_FUNC

.. py:data:: FF_IMMD

.. py:data:: FF_JUMP

.. py:data:: NEF_SEGS

.. py:data:: NEF_RSCS

.. py:data:: NEF_NAME

.. py:data:: NEF_MAN

.. py:data:: NEF_FILL

.. py:data:: NEF_IMPS

.. py:data:: NEF_FIRST

.. py:data:: NEF_CODE

.. py:data:: NEF_RELOAD

.. py:data:: NEF_FLAT

.. py:function:: value_is_string(var)

.. py:function:: value_is_long(var)

.. py:function:: value_is_float(var)

.. py:function:: value_is_func(var)

.. py:function:: value_is_pvoid(var)

.. py:function:: value_is_int64(var)

.. py:function:: to_ea(seg, off)

   Return value of expression: ((seg<<4) + off)


.. py:function:: form(format, *args)

.. py:function:: substr(s, x1, x2)

.. py:function:: strstr(s1, s2)

.. py:function:: strlen(s)

.. py:function:: xtol(s)

.. py:function:: atoa(ea)

   Convert address value to a string
   Return address in the form 'seg000:1234'
   (the same as in line prefixes)

   :param ea: address to format


.. py:function:: ltoa(n, radix)

.. py:function:: atol(s)

.. py:function:: rotate_left(value, count, nbits, offset)

   Rotate a value to the left (or right)

   :param value: value to rotate
   :param count: number of times to rotate. negative counter means
                 rotate to the right
   :param nbits: number of bits to rotate
   :param offset: offset of the first bit to rotate

   :returns: the value with the specified field rotated
            all other bits are not modified


.. py:function:: rotate_dword(x, count)

.. py:function:: rotate_word(x, count)

.. py:function:: rotate_byte(x, count)

.. py:data:: IDCHK_OK
   :value: 0


.. py:data:: IDCHK_ARG
   :value: -1


.. py:data:: IDCHK_KEY
   :value: -2


.. py:data:: IDCHK_MAX
   :value: -3


.. py:data:: add_idc_hotkey

.. py:data:: del_idc_hotkey

.. py:data:: jumpto

.. py:data:: auto_wait

.. py:function:: eval_idc(expr)

   Evaluate an IDC expression

   :param expr: an expression

   :returns: the expression value. If there are problems, the returned value will be "IDC_FAILURE: xxx"
            where xxx is the error description

   NOTE: Python implementation evaluates IDC only, while IDC can call other registered languages


.. py:function:: EVAL_FAILURE(code)

   Check the result of eval_idc() for evaluation failures

   :param code: result of eval_idc()

   :returns: True if there was an evaluation error


.. py:function:: save_database(idbname, flags=0)

   Save current database to the specified idb file

   :param idbname: name of the idb file. if empty, the current idb
                   file will be used.
   :param flags: combination of ida_loader.DBFL_... bits or 0


.. py:data:: DBFL_BAK

.. py:function:: validate_idb_names(do_repair=0)

   check consistency of IDB name records
   :param do_repair: try to repair netnode header it TRUE
   :returns: number of inconsistent name records


.. py:data:: qexit

.. py:function:: call_system(command)

   Execute an OS command.

   :param command: command line to execute

   :returns: error code from OS

   NOTE: IDA will wait for the started program to finish.
   In order to start the command in parallel, use OS methods.
   For example, you may start another program in parallel using
   "start" command.


.. py:function:: qsleep(milliseconds)

   qsleep the specified number of milliseconds
   This function suspends IDA for the specified amount of time

   :param milliseconds: time to sleep


.. py:data:: load_and_run_plugin

.. py:data:: plan_to_apply_idasgn

.. py:function:: delete_all_segments()

   Delete all segments, instructions, comments, i.e. everything
   except values of bytes.


.. py:data:: create_insn

.. py:function:: plan_and_wait(sEA, eEA, final_pass=True)

   Perform full analysis of the range

   :param sEA: starting linear address
   :param eEA: ending linear address (excluded)
   :param final_pass: make the final pass over the specified range

   :returns: 1-ok, 0-Ctrl-Break was pressed.


.. py:function:: set_name(ea, name, flags=ida_name.SN_CHECK)

   Rename an address

   :param ea: linear address
   :param name: new name of address. If name == "", then delete old name
   :param flags: combination of SN_... constants

   :returns: 1-ok, 0-failure


.. py:data:: SN_CHECK

.. py:data:: SN_NOCHECK

.. py:data:: SN_PUBLIC

.. py:data:: SN_NON_PUBLIC

.. py:data:: SN_WEAK

.. py:data:: SN_NON_WEAK

.. py:data:: SN_AUTO

.. py:data:: SN_NON_AUTO

.. py:data:: SN_NOLIST

.. py:data:: SN_NOWARN

.. py:data:: SN_LOCAL

.. py:data:: set_cmt

.. py:function:: make_array(ea, nitems)

   Create an array.

   :param ea: linear address
   :param nitems: size of array in items

   NOTE: This function will create an array of the items with the same type as
   the type of the item at 'ea'. If the byte at 'ea' is undefined, then
   this function will create an array of bytes.


.. py:function:: create_strlit(ea, endea)

   Create a string.

   This function creates a string (the string type is determined by the
   value of get_inf_attr(INF_STRTYPE))

   :param ea: linear address
   :param endea: ending address of the string (excluded)
       if endea == BADADDR, then length of string will be calculated
       by the kernel

   :returns: 1-ok, 0-failure

   NOTE: The type of an existing string is returned by get_str_type()


.. py:data:: create_data

.. py:function:: create_byte(ea)

   Convert the current item to a byte

   :param ea: linear address

   :returns: 1-ok, 0-failure


.. py:function:: create_word(ea)

   Convert the current item to a word (2 bytes)

   :param ea: linear address

   :returns: 1-ok, 0-failure


.. py:function:: create_dword(ea)

   Convert the current item to a double word (4 bytes)

   :param ea: linear address

   :returns: 1-ok, 0-failure


.. py:function:: create_qword(ea)

   Convert the current item to a quadro word (8 bytes)

   :param ea: linear address

   :returns: 1-ok, 0-failure


.. py:function:: create_oword(ea)

   Convert the current item to an octa word (16 bytes/128 bits)

   :param ea: linear address

   :returns: 1-ok, 0-failure


.. py:function:: create_yword(ea)

   Convert the current item to a ymm word (32 bytes/256 bits)

   :param ea: linear address

   :returns: 1-ok, 0-failure


.. py:function:: create_float(ea)

   Convert the current item to a floating point (4 bytes)

   :param ea: linear address

   :returns: 1-ok, 0-failure


.. py:function:: create_double(ea)

   Convert the current item to a double floating point (8 bytes)

   :param ea: linear address

   :returns: 1-ok, 0-failure


.. py:function:: create_pack_real(ea)

   Convert the current item to a packed real (10 or 12 bytes)

   :param ea: linear address

   :returns: 1-ok, 0-failure


.. py:function:: create_tbyte(ea)

   Convert the current item to a tbyte (10 or 12 bytes)

   :param ea: linear address

   :returns: 1-ok, 0-failure


.. py:function:: create_struct(ea, size, strname)

   Convert the current item to a structure instance

   :param ea: linear address
   :param size: structure size in bytes. -1 means that the size
       will be calculated automatically
   :param strname: name of a structure type

   :returns: 1-ok, 0-failure


.. py:data:: create_custom_data

.. py:data:: create_align

.. py:function:: define_local_var(start, end, location, name)

   Create a local variable

   :param start: start of address range for the local variable
   :param end: end of address range for the local variable
   :param location: the variable location in the "[bp+xx]" form where xx is
                    a number. The location can also be specified as a
                    register name.
   :param name: name of the local variable

   :returns: 1-ok, 0-failure

   NOTE: For the stack variables the end address is ignored.
         If there is no function at 'start' then this function will fail.


.. py:data:: del_items

.. py:data:: DELIT_SIMPLE

.. py:data:: DELIT_EXPAND

.. py:data:: DELIT_DELNAMES

.. py:function:: set_array_params(ea, flags, litems, align)

   Set array representation format

   :param ea: linear address
   :param flags: combination of AP_... constants or 0
   :param litems: number of items per line. 0 means auto
   :param align: element alignment
                 - -1: do not align
                 - 0:  automatic alignment
                 - other values: element width

   :returns: 1-ok, 0-failure


.. py:data:: AP_ALLOWDUPS
   :value: 1


.. py:data:: AP_SIGNED
   :value: 2


.. py:data:: AP_INDEX
   :value: 4


.. py:data:: AP_ARRAY
   :value: 8


.. py:data:: AP_IDXBASEMASK
   :value: 240


.. py:data:: AP_IDXDEC
   :value: 0


.. py:data:: AP_IDXHEX
   :value: 16


.. py:data:: AP_IDXOCT
   :value: 32


.. py:data:: AP_IDXBIN
   :value: 48


.. py:data:: op_bin

.. py:data:: op_oct

.. py:data:: op_dec

.. py:data:: op_hex

.. py:data:: op_chr

.. py:function:: op_plain_offset(ea, n, base)

   Convert operand to an offset
   (for the explanations of 'ea' and 'n' please see op_bin())

   Example:
   ========

       seg000:2000 dw      1234h

       and there is a segment at paragraph 0x1000 and there is a data item
       within the segment at 0x1234:

       seg000:1234 MyString        db 'Hello, world!',0

       Then you need to specify a linear address of the segment base to
       create a proper offset:

       op_plain_offset(["seg000",0x2000],0,0x10000);

       and you will have:

       seg000:2000 dw      offset MyString

   Motorola 680x0 processor have a concept of "outer offsets".
   If you want to create an outer offset, you need to combine number
   of the operand with the following bit:

   Please note that the outer offsets are meaningful only for
   Motorola 680x0.

   :param ea: linear address
   :param n: number of operand
       - 0 - the first operand
       - 1 - the second, third and all other operands
       - -1 - all operands
   :param base: base of the offset as a linear address
       If base == BADADDR then the current operand becomes non-offset


.. py:data:: OPND_OUTER

.. py:data:: op_offset

.. py:data:: REF_OFF8

.. py:data:: REF_OFF16

.. py:data:: REF_OFF32

.. py:data:: REF_LOW8

.. py:data:: REF_LOW16

.. py:data:: REF_HIGH8

.. py:data:: REF_HIGH16

.. py:data:: REF_OFF64

.. py:data:: REFINFO_RVA
   :value: 16


.. py:data:: REFINFO_PASTEND
   :value: 32


.. py:data:: REFINFO_NOBASE
   :value: 128


.. py:data:: REFINFO_SUBTRACT
   :value: 256


.. py:data:: REFINFO_SIGNEDOP
   :value: 512


.. py:data:: op_seg

.. py:data:: op_num

.. py:data:: op_flt

.. py:data:: op_man

.. py:data:: toggle_sign

.. py:function:: toggle_bnot(ea, n)

   Toggle the bitwise not operator for the operand

   :param ea: linear address
   :param n: number of operand
       - 0 - the first operand
       - 1 - the second, third and all other operands
       - -1 - all operands


.. py:data:: op_enum

.. py:function:: op_stroff(ea, n, strid, delta)

   Convert operand to an offset in a structure

   :param ea: linear address
   :param n: number of operand
       - 0 - the first operand
       - 1 - the second, third and all other operands
       - -1 - all operands
   :param strid: id of a structure type
   :param delta: struct offset delta. usually 0. denotes the difference
                   between the structure base and the pointer into the structure.



.. py:data:: op_stkvar

.. py:function:: op_offset_high16(ea, n, target)

   Convert operand to a high offset
   High offset is the upper 16bits of an offset.
   This type is used by TMS320C6 processors (and probably by other
   RISC processors too)

   :param ea: linear address
   :param n: number of operand
       - 0 - the first operand
       - 1 - the second, third and all other operands
       - -1 - all operands
   :param target: the full value (all 32bits) of the offset


.. py:function:: MakeVar(ea)

.. py:data:: E_PREV

.. py:data:: E_NEXT

.. py:data:: get_extra_cmt

.. py:data:: update_extra_cmt

.. py:data:: del_extra_cmt

.. py:data:: set_manual_insn

.. py:data:: get_manual_insn

.. py:data:: patch_dbg_byte

.. py:data:: patch_byte

.. py:data:: patch_word

.. py:data:: patch_dword

.. py:data:: patch_qword

.. py:data:: SR_inherit
   :value: 1


.. py:data:: SR_user
   :value: 2


.. py:data:: SR_auto
   :value: 3


.. py:data:: SR_autostart
   :value: 4


.. py:function:: split_sreg_range(ea, reg, value, tag=SR_user)

   Set value of a segment register.

   :param ea: linear address
   :param reg: name of a register, like "cs", "ds", "es", etc.
   :param value: new value of the segment register.
   :param tag: of SR_... constants

   NOTE: IDA keeps tracks of all the points where segment register change their
         values. This function allows you to specify the correct value of a segment
         register if IDA is not able to find the correct value.


.. py:data:: auto_mark_range

.. py:data:: auto_unmark

.. py:function:: AutoMark(ea, qtype)

   Plan to analyze an address


.. py:data:: AU_UNK

.. py:data:: AU_CODE

.. py:data:: AU_PROC

.. py:data:: AU_USED

.. py:data:: AU_LIBF

.. py:data:: AU_FINAL

.. py:function:: gen_file(filetype, path, ea1, ea2, flags)

   Generate an output file

   :param filetype:  type of output file. One of OFILE_... symbols. See below.
   :param path:  the output file path (will be overwritten!)
   :param ea1:   start address. For some file types this argument is ignored
   :param ea2:   end address. For some file types this argument is ignored
   :param flags: bit combination of GENFLG_...

   :returns: number of the generated lines.
               -1 if an error occurred
               OFILE_EXE: 0-can't generate exe file, 1-ok


.. py:data:: OFILE_MAP

.. py:data:: OFILE_EXE

.. py:data:: OFILE_IDC

.. py:data:: OFILE_LST

.. py:data:: OFILE_ASM

.. py:data:: OFILE_DIF

.. py:data:: GENFLG_MAPSEG

.. py:data:: GENFLG_MAPNAME

.. py:data:: GENFLG_MAPDMNG

.. py:data:: GENFLG_MAPLOC

.. py:data:: GENFLG_IDCTYPE

.. py:data:: GENFLG_ASMTYPE

.. py:data:: GENFLG_GENHTML

.. py:data:: GENFLG_ASMINC

.. py:function:: gen_flow_graph(outfile, title, ea1, ea2, flags)

   Generate a flow chart GDL file

   :param outfile: output file name. GDL extension will be used
   :param title: graph title
   :param ea1: beginning of the range to flow chart
   :param ea2: end of the range to flow chart.
   :param flags: combination of CHART_... constants

   NOTE: If ea2 == BADADDR then ea1 is treated as an address within a function.
          That function will be flow charted.


.. py:data:: CHART_PRINT_NAMES
   :value: 4096


.. py:data:: CHART_GEN_GDL
   :value: 16384


.. py:data:: CHART_WINGRAPH
   :value: 32768


.. py:data:: CHART_NOLIBFUNCS
   :value: 1024


.. py:function:: gen_simple_call_chart(outfile, title, flags)

   Generate a function call graph GDL file

   :param outfile: output file name. GDL extension will be used
   :param title:   graph title
   :param flags:   combination of CHART_GEN_GDL, CHART_WINGRAPH, CHART_NOLIBFUNCS


.. py:function:: idadir()

   Get IDA directory

   This function returns the directory where IDA.EXE resides


.. py:data:: get_root_filename

.. py:data:: get_input_file_path

.. py:data:: set_root_filename

.. py:function:: get_idb_path()

   Get IDB full path

   This function returns full path of the current IDB database


.. py:data:: retrieve_input_file_md5

.. py:data:: get_full_flags

.. py:data:: get_db_byte

.. py:function:: get_bytes(ea, size, use_dbg=False)

   Return the specified number of bytes of the program

   :param ea: linear address

   :param size: size of buffer in normal 8-bit bytes

   :param use_dbg: if True, use debugger memory, otherwise just the database

   :returns: None on failure
            otherwise a string containing the read bytes


.. py:data:: get_wide_byte

.. py:function:: read_dbg_byte(ea)

   Get value of program byte using the debugger memory

   :param ea: linear address
   :returns: The value or None on failure.


.. py:function:: read_dbg_word(ea)

   Get value of program word using the debugger memory

   :param ea: linear address
   :returns: The value or None on failure.


.. py:function:: read_dbg_dword(ea)

   Get value of program double-word using the debugger memory

   :param ea: linear address
   :returns: The value or None on failure.


.. py:function:: read_dbg_qword(ea)

   Get value of program quadro-word using the debugger memory

   :param ea: linear address
   :returns: The value or None on failure.


.. py:data:: read_dbg_memory

.. py:function:: write_dbg_memory(ea, data)

   Write to debugger memory.

   :param ea: linear address
   :param data: string to write
   :returns: number of written bytes (-1 - network/debugger error)

   Thread-safe function (may be called only from the main thread and debthread)


.. py:data:: get_original_byte

.. py:data:: get_wide_word

.. py:data:: get_wide_dword

.. py:data:: get_qword

.. py:function:: GetFloat(ea)

   Get value of a floating point number (4 bytes)
   This function assumes number stored using IEEE format
   and in the same endianness as integers.

   :param ea: linear address

   :returns: float


.. py:function:: GetDouble(ea)

   Get value of a floating point number (8 bytes)
   This function assumes number stored using IEEE format
   and in the same endianness as integers.

   :param ea: linear address

   :returns: double


.. py:function:: get_name_ea_simple(name)

   Get linear address of a name

   :param name: name of program byte

   :returns: address of the name
            BADADDR - No such name


.. py:data:: get_name_ea

.. py:function:: get_segm_by_sel(base)

   Get segment by segment base

   :param base: segment base paragraph or selector

   :returns: linear address of the start of the segment or BADADDR
            if no such segment


.. py:data:: get_screen_ea

.. py:function:: get_curline()

   Get the disassembly line at the cursor

   :returns: string


.. py:function:: read_selection_start()

   Get start address of the selected range
   returns BADADDR - the user has not selected an range


.. py:function:: read_selection_end()

   Get end address of the selected range

   :returns: BADADDR - the user has not selected an range


.. py:function:: get_sreg(ea, reg)

   Get value of segment register at the specified address

   :param ea: linear address
   :param reg: name of segment register

   :returns: the value of the segment register or -1 on error

   NOTE: The segment registers in 32bit program usually contain selectors,
          so to get paragraph pointed to by the segment register you need to
          call sel2para() function.


.. py:data:: next_addr

.. py:data:: prev_addr

.. py:function:: next_head(ea, maxea=BADADDR)

   Get next defined item (instruction or data) in the program

   :param ea: linear address to start search from
   :param maxea: the search will stop at the address
       maxea is not included in the search range

   :returns: BADADDR - no (more) defined items


.. py:function:: prev_head(ea, minea=0)

   Get previous defined item (instruction or data) in the program

   :param ea: linear address to start search from
   :param minea: the search will stop at the address
           minea is included in the search range

   :returns: BADADDR - no (more) defined items


.. py:data:: next_not_tail

.. py:data:: prev_not_tail

.. py:data:: get_item_head

.. py:data:: get_item_end

.. py:function:: get_item_size(ea)

   Get size of instruction or data item in bytes

   :param ea: linear address

   :returns: 1..n


.. py:function:: func_contains(func_ea, ea)

   Does the given function contain the given address?

   :param func_ea: any address belonging to the function
   :param ea: linear address

   :returns:  success


.. py:data:: GN_VISIBLE

.. py:data:: GN_COLORED

.. py:data:: GN_DEMANGLED

.. py:data:: GN_STRICT

.. py:data:: GN_SHORT

.. py:data:: GN_LONG

.. py:data:: GN_LOCAL

.. py:data:: GN_ISRET

.. py:data:: GN_NOT_ISRET

.. py:data:: calc_gtn_flags

.. py:function:: get_name(ea, gtn_flags=0)

   Get name at the specified address

   :param ea: linear address
   :param gtn_flags: how exactly the name should be retrieved.
                     combination of GN_ bits

   :returns: "" - byte has no name


.. py:function:: demangle_name(name, disable_mask)

   demangle_name a name

   :param name: name to demangle
   :param disable_mask: a mask that tells how to demangle the name
           it is a good idea to get this mask using
           get_inf_attr(INF_SHORT_DN) or get_inf_attr(INF_LONG_DN)

   :returns: a demangled name
       If the input name cannot be demangled, returns None


.. py:function:: generate_disasm_line(ea, flags)

   Get disassembly line

   :param ea: linear address of instruction

   :param flags: combination of the GENDSM_ flags, or 0

   :returns: "" - could not decode instruction at the specified location

   NOTE: this function may not return exactly the same mnemonics
          as you see on the screen.


.. py:data:: GENDSM_FORCE_CODE

.. py:data:: GENDSM_MULTI_LINE

.. py:function:: GetDisasm(ea)

   Get disassembly line

   :param ea: linear address of instruction

   :returns: "" - could not decode instruction at the specified location

   NOTE: this function may not return exactly the same mnemonics
          as you see on the screen.


.. py:function:: print_insn_mnem(ea)

   Get instruction mnemonics

   :param ea: linear address of instruction

   :returns: "" - no instruction at the specified location

   NOTE: this function may not return exactly the same mnemonics
   as you see on the screen.


.. py:function:: print_operand(ea, n)

   Get operand of an instruction or data

   :param ea: linear address of the item
   :param n: number of operand:
       0 - the first operand
       1 - the second operand

   :returns: the current text representation of operand or ""


.. py:function:: get_operand_type(ea, n)

   Get type of instruction operand

   :param ea: linear address of instruction
   :param n: number of operand:
       0 - the first operand
       1 - the second operand

   :returns: any of o_* constants or -1 on error


.. py:data:: o_void

.. py:data:: o_reg

.. py:data:: o_mem

.. py:data:: o_phrase

.. py:data:: o_displ

.. py:data:: o_imm

.. py:data:: o_far

.. py:data:: o_near

.. py:data:: o_idpspec0

.. py:data:: o_idpspec1

.. py:data:: o_idpspec2

.. py:data:: o_idpspec3

.. py:data:: o_idpspec4

.. py:data:: o_idpspec5

.. py:data:: o_trreg

.. py:data:: o_dbreg

.. py:data:: o_crreg

.. py:data:: o_fpreg

.. py:data:: o_mmxreg

.. py:data:: o_xmmreg

.. py:data:: o_reglist

.. py:data:: o_creglist

.. py:data:: o_creg

.. py:data:: o_fpreglist

.. py:data:: o_text

.. py:data:: o_cond

.. py:data:: o_spr

.. py:data:: o_twofpr

.. py:data:: o_shmbme

.. py:data:: o_crf

.. py:data:: o_crb

.. py:data:: o_dcr

.. py:function:: get_operand_value(ea, n)

   Get number used in the operand

   This function returns an immediate number used in the operand

   :param ea: linear address of instruction
   :param n: the operand number

   :returns: value
       operand is an immediate value  => immediate value
       operand has a displacement     => displacement
       operand is a direct memory ref => memory address
       operand is a register          => register number
       operand is a register phrase   => phrase number
       otherwise                      => -1


.. py:data:: GetCommentEx

.. py:data:: get_cmt

.. py:data:: get_forced_operand

.. py:data:: BPU_1B

.. py:data:: BPU_2B

.. py:data:: BPU_4B

.. py:data:: STRWIDTH_1B

.. py:data:: STRWIDTH_2B

.. py:data:: STRWIDTH_4B

.. py:data:: STRWIDTH_MASK

.. py:data:: STRLYT_TERMCHR

.. py:data:: STRLYT_PASCAL1

.. py:data:: STRLYT_PASCAL2

.. py:data:: STRLYT_PASCAL4

.. py:data:: STRLYT_MASK

.. py:data:: STRLYT_SHIFT

.. py:data:: STRTYPE_TERMCHR

.. py:data:: STRTYPE_C

.. py:data:: STRTYPE_C_16

.. py:data:: STRTYPE_C_32

.. py:data:: STRTYPE_PASCAL

.. py:data:: STRTYPE_PASCAL_16

.. py:data:: STRTYPE_LEN2

.. py:data:: STRTYPE_LEN2_16

.. py:data:: STRTYPE_LEN4

.. py:data:: STRTYPE_LEN4_16

.. py:data:: STRTYPE_C16

.. py:function:: get_strlit_contents(ea, length=-1, strtype=STRTYPE_C)

   Get string contents
   :param ea: linear address
   :param length: string length. -1 means to calculate the max string length
   :param strtype: the string type (one of STRTYPE_... constants)

   :returns: string contents or empty string


.. py:function:: get_str_type(ea)

   Get string type

   :param ea: linear address

   :returns: One of STRTYPE_... constants


.. py:data:: find_suspop

.. py:data:: find_code

.. py:data:: find_data

.. py:data:: find_unknown

.. py:data:: find_defined

.. py:data:: find_imm

.. py:data:: find_text

.. py:data:: find_bytes

.. py:function:: process_config_line(directive)

   Obsolete. Please use ida_idp.process_config_directive().


.. py:data:: INF_VERSION
   :value: 0


.. py:data:: INF_PROCNAME
   :value: 1


.. py:data:: INF_GENFLAGS
   :value: 2


.. py:data:: INF_LFLAGS
   :value: 3


.. py:data:: INF_DATABASE_CHANGE_COUNT
   :value: 4


.. py:data:: INF_CHANGE_COUNTER
   :value: 4


.. py:data:: INF_FILETYPE
   :value: 5


.. py:data:: FT_EXE_OLD
   :value: 0


.. py:data:: FT_COM_OLD
   :value: 1


.. py:data:: FT_BIN
   :value: 2


.. py:data:: FT_DRV
   :value: 3


.. py:data:: FT_WIN
   :value: 4


.. py:data:: FT_HEX
   :value: 5


.. py:data:: FT_MEX
   :value: 6


.. py:data:: FT_LX
   :value: 7


.. py:data:: FT_LE
   :value: 8


.. py:data:: FT_NLM
   :value: 9


.. py:data:: FT_COFF
   :value: 10


.. py:data:: FT_PE
   :value: 11


.. py:data:: FT_OMF
   :value: 12


.. py:data:: FT_SREC
   :value: 13


.. py:data:: FT_ZIP
   :value: 14


.. py:data:: FT_OMFLIB
   :value: 15


.. py:data:: FT_AR
   :value: 16


.. py:data:: FT_LOADER
   :value: 17


.. py:data:: FT_ELF
   :value: 18


.. py:data:: FT_W32RUN
   :value: 19


.. py:data:: FT_AOUT
   :value: 20


.. py:data:: FT_PRC
   :value: 21


.. py:data:: FT_EXE
   :value: 22


.. py:data:: FT_COM
   :value: 23


.. py:data:: FT_AIXAR
   :value: 24


.. py:data:: FT_MACHO
   :value: 25


.. py:data:: INF_OSTYPE
   :value: 6


.. py:data:: OSTYPE_MSDOS
   :value: 1


.. py:data:: OSTYPE_WIN
   :value: 2


.. py:data:: OSTYPE_OS2
   :value: 4


.. py:data:: OSTYPE_NETW
   :value: 8


.. py:data:: INF_APPTYPE
   :value: 7


.. py:data:: APPT_CONSOLE
   :value: 1


.. py:data:: APPT_GRAPHIC
   :value: 2


.. py:data:: APPT_PROGRAM
   :value: 4


.. py:data:: APPT_LIBRARY
   :value: 8


.. py:data:: APPT_DRIVER
   :value: 16


.. py:data:: APPT_1THREAD
   :value: 32


.. py:data:: APPT_MTHREAD
   :value: 64


.. py:data:: APPT_16BIT
   :value: 128


.. py:data:: APPT_32BIT
   :value: 256


.. py:data:: INF_ASMTYPE
   :value: 8


.. py:data:: INF_SPECSEGS
   :value: 9


.. py:data:: INF_AF
   :value: 10


.. py:data:: INF_AF2
   :value: 11


.. py:data:: INF_BASEADDR
   :value: 12


.. py:data:: INF_START_SS
   :value: 13


.. py:data:: INF_START_CS
   :value: 14


.. py:data:: INF_START_IP
   :value: 15


.. py:data:: INF_START_EA
   :value: 16


.. py:data:: INF_START_SP
   :value: 17


.. py:data:: INF_MAIN
   :value: 18


.. py:data:: INF_MIN_EA
   :value: 19


.. py:data:: INF_MAX_EA
   :value: 20


.. py:data:: INF_OMIN_EA
   :value: 21


.. py:data:: INF_OMAX_EA
   :value: 22


.. py:data:: INF_LOWOFF
   :value: 23


.. py:data:: INF_LOW_OFF
   :value: 23


.. py:data:: INF_HIGHOFF
   :value: 24


.. py:data:: INF_HIGH_OFF
   :value: 24


.. py:data:: INF_MAXREF
   :value: 25


.. py:data:: INF_PRIVRANGE_START_EA
   :value: 27


.. py:data:: INF_START_PRIVRANGE
   :value: 27


.. py:data:: INF_PRIVRANGE_END_EA
   :value: 28


.. py:data:: INF_END_PRIVRANGE
   :value: 28


.. py:data:: INF_NETDELTA
   :value: 29


.. py:data:: INF_XREFNUM
   :value: 30


.. py:data:: INF_TYPE_XREFNUM
   :value: 31


.. py:data:: INF_TYPE_XREFS
   :value: 31


.. py:data:: INF_REFCMTNUM
   :value: 32


.. py:data:: INF_REFCMTS
   :value: 32


.. py:data:: INF_XREFFLAG
   :value: 33


.. py:data:: INF_XREFS
   :value: 33


.. py:data:: INF_MAX_AUTONAME_LEN
   :value: 34


.. py:data:: INF_NAMETYPE
   :value: 35


.. py:data:: INF_SHORT_DEMNAMES
   :value: 36


.. py:data:: INF_SHORT_DN
   :value: 36


.. py:data:: INF_LONG_DEMNAMES
   :value: 37


.. py:data:: INF_LONG_DN
   :value: 37


.. py:data:: INF_DEMNAMES
   :value: 38


.. py:data:: INF_LISTNAMES
   :value: 39


.. py:data:: INF_INDENT
   :value: 40


.. py:data:: INF_CMT_INDENT
   :value: 41


.. py:data:: INF_COMMENT
   :value: 41


.. py:data:: INF_MARGIN
   :value: 42


.. py:data:: INF_LENXREF
   :value: 43


.. py:data:: INF_OUTFLAGS
   :value: 44


.. py:data:: INF_CMTFLG
   :value: 45


.. py:data:: INF_CMTFLAG
   :value: 45


.. py:data:: INF_LIMITER
   :value: 46


.. py:data:: INF_BORDER
   :value: 46


.. py:data:: INF_BIN_PREFIX_SIZE
   :value: 47


.. py:data:: INF_BINPREF
   :value: 47


.. py:data:: INF_PREFFLAG
   :value: 48


.. py:data:: INF_STRLIT_FLAGS
   :value: 49


.. py:data:: INF_STRLIT_BREAK
   :value: 50


.. py:data:: INF_STRLIT_ZEROES
   :value: 51


.. py:data:: INF_STRTYPE
   :value: 52


.. py:data:: INF_STRLIT_PREF
   :value: 53


.. py:data:: INF_STRLIT_SERNUM
   :value: 54


.. py:data:: INF_DATATYPES
   :value: 55


.. py:data:: INF_CC_ID
   :value: 57


.. py:data:: COMP_MASK
   :value: 15


.. py:data:: COMP_UNK
   :value: 0


.. py:data:: COMP_MS
   :value: 1


.. py:data:: COMP_BC
   :value: 2


.. py:data:: COMP_WATCOM
   :value: 3


.. py:data:: COMP_GNU
   :value: 6


.. py:data:: COMP_VISAGE
   :value: 7


.. py:data:: COMP_BP
   :value: 8


.. py:data:: INF_CC_CM
   :value: 58


.. py:data:: INF_CC_SIZE_I
   :value: 59


.. py:data:: INF_CC_SIZE_B
   :value: 60


.. py:data:: INF_CC_SIZE_E
   :value: 61


.. py:data:: INF_CC_DEFALIGN
   :value: 62


.. py:data:: INF_CC_SIZE_S
   :value: 63


.. py:data:: INF_CC_SIZE_L
   :value: 64


.. py:data:: INF_CC_SIZE_LL
   :value: 65


.. py:data:: INF_CC_SIZE_LDBL
   :value: 66


.. py:data:: INF_COMPILER
   :value: 57


.. py:data:: INF_MODEL
   :value: 58


.. py:data:: INF_SIZEOF_INT
   :value: 59


.. py:data:: INF_SIZEOF_BOOL
   :value: 60


.. py:data:: INF_SIZEOF_ENUM
   :value: 61


.. py:data:: INF_SIZEOF_ALGN
   :value: 62


.. py:data:: INF_SIZEOF_SHORT
   :value: 63


.. py:data:: INF_SIZEOF_LONG
   :value: 64


.. py:data:: INF_SIZEOF_LLONG
   :value: 65


.. py:data:: INF_SIZEOF_LDBL
   :value: 66


.. py:data:: INF_ABIBITS
   :value: 67


.. py:data:: INF_APPCALL_OPTIONS
   :value: 68


.. py:function:: get_inf_attr(attr)

   Deprecated. Please ida_ida.inf_get_* instead.


.. py:function:: set_inf_attr(attr, value)

   Deprecated. Please ida_ida.inf_set_* instead.


.. py:data:: set_processor_type

.. py:data:: SETPROC_IDB

.. py:data:: SETPROC_LOADER

.. py:data:: SETPROC_LOADER_NON_FATAL

.. py:data:: SETPROC_USER

.. py:function:: SetPrcsr(processor)

.. py:function:: get_processor_name()

   Get name of the current processor
   :returns: processor name


.. py:data:: set_target_assembler

.. py:function:: batch(batch)

   Enable/disable batch mode of operation

   :param batch: batch mode
           0 - ida will display dialog boxes and wait for the user input
           1 - ida will not display dialog boxes, warnings, etc.

   :returns: old balue of batch flag


.. py:function:: process_ui_action(name, flags=0)

   Invokes an IDA UI action by name

   :param name: Command name
   :param flags: Reserved. Must be zero
   :returns: Boolean


.. py:data:: ask_seg

.. py:data:: ask_yn

.. py:data:: msg

.. py:data:: warning

.. py:data:: error

.. py:data:: set_ida_state

.. py:data:: IDA_STATUS_READY
   :value: 0


.. py:data:: IDA_STATUS_THINKING
   :value: 1


.. py:data:: IDA_STATUS_WAITING
   :value: 2


.. py:data:: IDA_STATUS_WORK
   :value: 3


.. py:data:: refresh_idaview_anyway

.. py:data:: refresh_lists

.. py:function:: sel2para(sel)

   Get a selector value

   :param sel: the selector number

   :returns: selector value if found
            otherwise the input value (sel)

   NOTE: selector values are always in paragraphs


.. py:function:: find_selector(val)

   Find a selector which has the specified value

   :param val: value to search for

   :returns: the selector number if found,
            otherwise the input value (val & 0xFFFF)

   NOTE: selector values are always in paragraphs


.. py:data:: set_selector

.. py:data:: del_selector

.. py:function:: get_first_seg()

   Get first segment

   :returns: address of the start of the first segment
       BADADDR - no segments are defined


.. py:function:: get_next_seg(ea)

   Get next segment

   :param ea: linear address

   :returns: start of the next segment
            BADADDR - no next segment


.. py:function:: get_segm_start(ea)

   Get start address of a segment

   :param ea: any address in the segment

   :returns: start of segment
            BADADDR - the specified address doesn't belong to any segment


.. py:function:: get_segm_end(ea)

   Get end address of a segment

   :param ea: any address in the segment

   :returns: end of segment (an address past end of the segment)
            BADADDR - the specified address doesn't belong to any segment


.. py:function:: get_segm_name(ea)

   Get name of a segment

   :param ea: any address in the segment

   :returns: "" - no segment at the specified address


.. py:function:: add_segm_ex(startea, endea, base, use32, align, comb, flags)

   Create a new segment

   :param startea: linear address of the start of the segment
   :param endea: linear address of the end of the segment
              this address will not belong to the segment
              'endea' should be higher than 'startea'
   :param base: base paragraph or selector of the segment.
              a paragraph is 16byte memory chunk.
              If a selector value is specified, the selector should be
              already defined.
   :param use32: 0: 16bit segment, 1: 32bit segment, 2: 64bit segment
   :param align: segment alignment. see below for alignment values
   :param comb: segment combination. see below for combination values.
   :param flags: combination of ADDSEG_... bits

   :returns: 0-failed, 1-ok


.. py:data:: ADDSEG_NOSREG

.. py:data:: ADDSEG_OR_DIE

.. py:data:: ADDSEG_NOTRUNC

.. py:data:: ADDSEG_QUIET

.. py:data:: ADDSEG_FILLGAP

.. py:data:: ADDSEG_SPARSE

.. py:function:: AddSeg(startea, endea, base, use32, align, comb)

.. py:data:: del_segm

.. py:data:: SEGMOD_KILL

.. py:data:: SEGMOD_KEEP

.. py:data:: SEGMOD_SILENT

.. py:function:: set_segment_bounds(ea, startea, endea, flags)

   Change segment boundaries

   :param ea: any address in the segment
   :param startea: new start address of the segment
   :param endea: new end address of the segment
   :param flags: combination of SEGMOD_... flags

   :returns: boolean success


.. py:function:: set_segm_name(ea, name)

   Change name of the segment

   :param ea: any address in the segment
   :param name: new name of the segment

   :returns: success (boolean)


.. py:function:: set_segm_class(ea, segclass)

   Change class of the segment

   :param ea: any address in the segment
   :param segclass: new class of the segment

   :returns: success (boolean)


.. py:function:: set_segm_alignment(ea, alignment)

   Change alignment of the segment

   :param ea: any address in the segment
   :param alignment: new alignment of the segment (one of the sa... constants)

   :returns: success (boolean)


.. py:data:: saAbs

.. py:data:: saRelByte

.. py:data:: saRelWord

.. py:data:: saRelPara

.. py:data:: saRelPage

.. py:data:: saRelDble

.. py:data:: saRel4K

.. py:data:: saGroup

.. py:data:: saRel32Bytes

.. py:data:: saRel64Bytes

.. py:data:: saRelQword

.. py:function:: set_segm_combination(segea, comb)

   Change combination of the segment

   :param segea: any address in the segment
   :param comb: new combination of the segment (one of the sc... constants)

   :returns: success (boolean)


.. py:data:: scPriv

.. py:data:: scPub

.. py:data:: scPub2

.. py:data:: scStack

.. py:data:: scCommon

.. py:data:: scPub3

.. py:function:: set_segm_addressing(ea, bitness)

   Change segment addressing

   :param ea: any address in the segment
   :param bitness: 0: 16bit, 1: 32bit, 2: 64bit

   :returns: success (boolean)


.. py:function:: selector_by_name(segname)

   Get segment selector by name

   :param segname: name of segment

   :returns: segment selector or BADADDR


.. py:function:: set_default_sreg_value(ea, reg, value)

   Set default segment register value for a segment

   :param ea: any address in the segment
              if no segment is present at the specified address
              then all segments will be affected
   :param reg: name of segment register
   :param value: default value of the segment register. -1-undefined.


.. py:function:: set_segm_type(segea, segtype)

   Set segment type

   :param segea: any address within segment
   :param segtype: new segment type:

   :returns: !=0 - ok


.. py:data:: SEG_NORM

.. py:data:: SEG_XTRN

.. py:data:: SEG_CODE

.. py:data:: SEG_DATA

.. py:data:: SEG_IMP

.. py:data:: SEG_GRP

.. py:data:: SEG_NULL

.. py:data:: SEG_UNDF

.. py:data:: SEG_BSS

.. py:data:: SEG_ABSSYM

.. py:data:: SEG_COMM

.. py:data:: SEG_IMEM

.. py:function:: get_segm_attr(segea, attr)

   Get segment attribute

   :param segea: any address within segment
   :param attr: one of SEGATTR_... constants


.. py:function:: set_segm_attr(segea, attr, value)

   Set segment attribute

   :param segea: any address within segment
   :param attr: one of SEGATTR_... constants

   NOTE: Please note that not all segment attributes are modifiable.
          Also some of them should be modified using special functions
          like set_segm_addressing, etc.


.. py:data:: SEGATTR_START
   :value: 0


.. py:data:: SEGATTR_END
   :value: 4


.. py:data:: SEGATTR_ORGBASE
   :value: 16


.. py:data:: SEGATTR_ALIGN
   :value: 20


.. py:data:: SEGATTR_COMB
   :value: 21


.. py:data:: SEGATTR_PERM
   :value: 22


.. py:data:: SEGATTR_BITNESS
   :value: 23


.. py:data:: SEGATTR_FLAGS
   :value: 24


.. py:data:: SEGATTR_SEL
   :value: 28


.. py:data:: SEGATTR_ES
   :value: 32


.. py:data:: SEGATTR_CS
   :value: 36


.. py:data:: SEGATTR_SS
   :value: 40


.. py:data:: SEGATTR_DS
   :value: 44


.. py:data:: SEGATTR_FS
   :value: 48


.. py:data:: SEGATTR_GS
   :value: 52


.. py:data:: SEGATTR_TYPE
   :value: 96


.. py:data:: SEGATTR_COLOR
   :value: 100


.. py:data:: SEGATTR_START
   :value: 0


.. py:data:: SFL_COMORG
   :value: 1


.. py:data:: SFL_OBOK
   :value: 2


.. py:data:: SFL_HIDDEN
   :value: 4


.. py:data:: SFL_DEBUG
   :value: 8


.. py:data:: SFL_LOADER
   :value: 16


.. py:data:: SFL_HIDETYPE
   :value: 32


.. py:function:: move_segm(ea, to, flags)

   Move a segment to a new address
   This function moves all information to the new address
   It fixes up address sensitive information in the kernel
   The total effect is equal to reloading the segment to the target address

   :param ea: any address within the segment to move
   :param to: new segment start address
   :param flags: combination MFS_... constants

   :returns: MOVE_SEGM_... error code


.. py:data:: MSF_SILENT
   :value: 1


.. py:data:: MSF_NOFIX
   :value: 2


.. py:data:: MSF_LDKEEP
   :value: 4


.. py:data:: MSF_FIXONCE
   :value: 8


.. py:data:: MOVE_SEGM_OK
   :value: 0


.. py:data:: MOVE_SEGM_PARAM
   :value: -1


.. py:data:: MOVE_SEGM_ROOM
   :value: -2


.. py:data:: MOVE_SEGM_IDP
   :value: -3


.. py:data:: MOVE_SEGM_CHUNK
   :value: -4


.. py:data:: MOVE_SEGM_LOADER
   :value: -5


.. py:data:: MOVE_SEGM_ODD
   :value: -6


.. py:data:: MOVE_SEGM_ORPHAN

.. py:data:: MOVE_SEGM_DEBUG

.. py:data:: MOVE_SEGM_SOURCEFILES

.. py:data:: MOVE_SEGM_MAPPING

.. py:data:: MOVE_SEGM_INVAL

.. py:data:: rebase_program

.. py:data:: set_storage_type

.. py:data:: STT_VA
   :value: 0


.. py:data:: STT_MM
   :value: 1


.. py:data:: fl_CF
   :value: 16


.. py:data:: fl_CN
   :value: 17


.. py:data:: fl_JF
   :value: 18


.. py:data:: fl_JN
   :value: 19


.. py:data:: fl_F
   :value: 21


.. py:data:: XREF_USER
   :value: 32


.. py:data:: add_cref

.. py:data:: del_cref

.. py:data:: get_first_cref_from

.. py:data:: get_next_cref_from

.. py:data:: get_first_cref_to

.. py:data:: get_next_cref_to

.. py:data:: get_first_fcref_from

.. py:data:: get_next_fcref_from

.. py:data:: get_first_fcref_to

.. py:data:: get_next_fcref_to

.. py:data:: dr_O

.. py:data:: dr_W

.. py:data:: dr_R

.. py:data:: dr_T

.. py:data:: dr_I

.. py:data:: add_dref

.. py:data:: del_dref

.. py:data:: get_first_dref_from

.. py:data:: get_next_dref_from

.. py:data:: get_first_dref_to

.. py:data:: get_next_dref_to

.. py:function:: get_xref_type()

   Return type of the last xref obtained by
   [RD]first/next[B0] functions.

   :returns: constants fl_* or dr_*


.. py:function:: fopen(f, mode)

.. py:function:: fclose(handle)

.. py:function:: filelength(handle)

.. py:function:: fseek(handle, offset, origin)

.. py:function:: ftell(handle)

.. py:function:: LoadFile(filepath, pos, ea, size)

   Load file into IDA database

   :param filepath: path to input file
   :param pos: position in the file
   :param ea: linear address to load
   :param size: number of bytes to load

   :returns: 0 - error, 1 - ok


.. py:function:: loadfile(filepath, pos, ea, size)

.. py:function:: SaveFile(filepath, pos, ea, size)

   Save from IDA database to file

   :param filepath: path to output file
   :param pos: position in the file
   :param ea: linear address to save from
   :param size: number of bytes to save

   :returns: 0 - error, 1 - ok


.. py:function:: savefile(filepath, pos, ea, size)

.. py:function:: fgetc(handle)

.. py:function:: fputc(byte, handle)

.. py:function:: fprintf(handle, format, *args)

.. py:function:: readshort(handle, mostfirst)

.. py:function:: readlong(handle, mostfirst)

.. py:function:: writeshort(handle, word, mostfirst)

.. py:function:: writelong(handle, dword, mostfirst)

.. py:function:: readstr(handle)

.. py:function:: writestr(handle, s)

.. py:data:: add_func

.. py:data:: del_func

.. py:data:: set_func_end

.. py:function:: get_next_func(ea)

   Find next function

   :param ea: any address belonging to the function

   :returns:        BADADDR - no more functions
           otherwise returns the next function start address


.. py:function:: get_prev_func(ea)

   Find previous function

   :param ea: any address belonging to the function

   :returns: BADADDR - no more functions
           otherwise returns the previous function start address


.. py:function:: get_func_attr(ea, attr)

   Get a function attribute

   :param ea: any address belonging to the function
   :param attr: one of FUNCATTR_... constants

   :returns: BADADDR - error otherwise returns the attribute value


.. py:function:: set_func_attr(ea, attr, value)

   Set a function attribute

   :param ea: any address belonging to the function
   :param attr: one of FUNCATTR_... constants
   :param value: new value of the attribute

   :returns: 1-ok, 0-failed


.. py:data:: FUNCATTR_START
   :value: 0


.. py:data:: FUNCATTR_END
   :value: 4


.. py:data:: FUNCATTR_FLAGS
   :value: 8


.. py:data:: FUNCATTR_FRAME
   :value: 16


.. py:data:: FUNCATTR_FRSIZE
   :value: 20


.. py:data:: FUNCATTR_FRREGS
   :value: 24


.. py:data:: FUNCATTR_ARGSIZE
   :value: 28


.. py:data:: FUNCATTR_FPD
   :value: 32


.. py:data:: FUNCATTR_COLOR
   :value: 36


.. py:data:: FUNCATTR_OWNER
   :value: 16


.. py:data:: FUNCATTR_REFQTY
   :value: 20


.. py:data:: FUNCATTR_START
   :value: 0


.. py:function:: get_func_flags(ea)

   Retrieve function flags

   :param ea: any address belonging to the function

   :returns: -1 - function doesn't exist otherwise returns the flags


.. py:data:: FUNC_NORET

.. py:data:: FUNC_FAR

.. py:data:: FUNC_LIB

.. py:data:: FUNC_STATIC

.. py:data:: FUNC_FRAME

.. py:data:: FUNC_USERFAR

.. py:data:: FUNC_HIDDEN

.. py:data:: FUNC_THUNK

.. py:data:: FUNC_BOTTOMBP

.. py:data:: FUNC_NORET_PENDING

.. py:data:: FUNC_SP_READY

.. py:data:: FUNC_PURGED_OK

.. py:data:: FUNC_TAIL

.. py:data:: FUNC_LUMINA

.. py:data:: FUNC_OUTLINE

.. py:function:: set_func_flags(ea, flags)

   Change function flags

   :param ea: any address belonging to the function
   :param flags: see get_func_flags() for explanations

   :returns: !=0 - ok


.. py:function:: get_func_name(ea)

   Retrieve function name

   :param ea: any address belonging to the function

   :returns: null string - function doesn't exist
           otherwise returns function name


.. py:function:: get_func_cmt(ea, repeatable)

   Retrieve function comment

   :param ea: any address belonging to the function
   :param repeatable: 1: get repeatable comment
           0: get regular comment

   :returns: function comment string


.. py:function:: set_func_cmt(ea, cmt, repeatable)

   Set function comment

   :param ea: any address belonging to the function
   :param cmt: a function comment line
   :param repeatable: 1: get repeatable comment
           0: get regular comment


.. py:function:: choose_func(title)

   Ask the user to select a function

   Arguments:

   :param title: title of the dialog box

   :returns: -1 - user refused to select a function
            otherwise returns the selected function start address


.. py:function:: get_func_off_str(ea)

   Convert address to 'funcname+offset' string

   :param ea: address to convert

   :returns: if the address belongs to a function then return a string
            formed as 'name+offset' where 'name' is a function name
            'offset' is offset within the function else return null string


.. py:function:: find_func_end(ea)

   Determine a new function boundaries

   :param ea: starting address of a new function

   :returns: if a function already exists, then return its end address.
           If a function end cannot be determined, the return BADADDR
           otherwise return the end address of the new function


.. py:function:: get_frame_id(ea)

   Get ID of function frame structure

   :param ea: any address belonging to the function

   :returns: ID of function frame or None In order to access stack variables
            you need to use structure member manipulaion functions with the
            obtained ID.


.. py:function:: get_frame_lvar_size(ea)

   Get size of local variables in function frame

   :param ea: any address belonging to the function

   :returns: Size of local variables in bytes.
            If the function doesn't have a frame, return 0
            If the function doesn't exist, return None


.. py:function:: get_frame_regs_size(ea)

   Get size of saved registers in function frame

   :param ea: any address belonging to the function

   :returns: Size of saved registers in bytes.
            If the function doesn't have a frame, return 0
            This value is used as offset for BP (if FUNC_FRAME is set)
            If the function doesn't exist, return None


.. py:function:: get_frame_args_size(ea)

   Get size of arguments in function frame which are purged upon return

   :param ea: any address belonging to the function

   :returns: Size of function arguments in bytes.
            If the function doesn't have a frame, return 0
            If the function doesn't exist, return -1


.. py:function:: get_frame_size(ea)

   Get full size of function frame

   :param ea: any address belonging to the function
   :returns: Size of function frame in bytes.
               This function takes into account size of local
               variables + size of saved registers + size of
               return address + size of function arguments
               If the function doesn't have a frame, return size of
               function return address in the stack.
               If the function doesn't exist, return 0


.. py:function:: set_frame_size(ea, lvsize, frregs, argsize)

   Make function frame

   :param ea: any address belonging to the function
   :param lvsize: size of function local variables
   :param frregs: size of saved registers
   :param argsize: size of function arguments

   :returns: ID of function frame or -1
            If the function did not have a frame, the frame
            will be created. Otherwise the frame will be modified


.. py:function:: get_spd(ea)

   Get current delta for the stack pointer

   :param ea: end address of the instruction
              i.e.the last address of the instruction+1

   :returns: The difference between the original SP upon
            entering the function and SP for the specified address


.. py:function:: get_sp_delta(ea)

   Get modification of SP made by the instruction

   :param ea: end address of the instruction
              i.e.the last address of the instruction+1

   :returns: Get modification of SP made at the specified location
            If the specified location doesn't contain a SP change point, return 0
            Otherwise return delta of SP modification


.. py:function:: get_fchunk_attr(ea, attr)

   Get a function chunk attribute

   :param ea: any address in the chunk
   :param attr: one of: FUNCATTR_START, FUNCATTR_END, FUNCATTR_OWNER, FUNCATTR_REFQTY

   :returns: desired attribute or -1


.. py:function:: set_fchunk_attr(ea, attr, value)

   Set a function chunk attribute

   :param ea: any address in the chunk
   :param attr: only FUNCATTR_START, FUNCATTR_END, FUNCATTR_OWNER
   :param value: desired value

   :returns: 0 if failed, 1 if success


.. py:data:: get_fchunk_referer

.. py:function:: get_next_fchunk(ea)

   Get next function chunk

   :param ea: any address

   :returns:  the starting address of the next function chunk or BADADDR

   NOTE: This function enumerates all chunks of all functions in the database


.. py:function:: get_prev_fchunk(ea)

   Get previous function chunk

   :param ea: any address

   :returns: the starting address of the function chunk or BADADDR

   NOTE: This function enumerates all chunks of all functions in the database


.. py:function:: append_func_tail(funcea, ea1, ea2)

   Append a function chunk to the function

   :param funcea: any address in the function
   :param ea1: start of function tail
   :param ea2: end of function tail
   :returns: 0 if failed, 1 if success

   NOTE: If a chunk exists at the specified addresses, it must have exactly
          the specified boundaries


.. py:function:: remove_fchunk(funcea, tailea)

   Remove a function chunk from the function

   :param funcea: any address in the function
   :param tailea: any address in the function chunk to remove

   :returns: 0 if failed, 1 if success


.. py:function:: set_tail_owner(tailea, funcea)

   Change the function chunk owner

   :param tailea: any address in the function chunk
   :param funcea: the starting address of the new owner

   :returns: False if failed, True if success

   NOTE: The new owner must already have the chunk appended before the call


.. py:function:: first_func_chunk(funcea)

   Get the first function chunk of the specified function

   :param funcea: any address in the function

   :returns: the function entry point or BADADDR

   NOTE: This function returns the first (main) chunk of the specified function


.. py:function:: next_func_chunk(funcea, tailea)

   Get the next function chunk of the specified function

   :param funcea: any address in the function
   :param tailea: any address in the current chunk

   :returns: the starting address of the next function chunk or BADADDR

   NOTE: This function returns the next chunk of the specified function


.. py:function:: add_auto_stkpnt(func_ea, ea, delta)

   Add automatic SP register change point
   :param func_ea: function start
   :param ea: linear address where SP changes
              usually this is the end of the instruction which
              modifies the stack pointer (insn.ea+insn.size)
   :param delta: difference between old and new values of SP
   :returns: 1-ok, 0-failed


.. py:data:: add_user_stkpnt

.. py:function:: del_stkpnt(func_ea, ea)

   Delete SP register change point

   :param func_ea: function start
   :param ea: linear address
   :returns: 1-ok, 0-failed


.. py:function:: get_min_spd_ea(func_ea)

   Return the address with the minimal spd (stack pointer delta)
   If there are no SP change points, then return BADADDR.

   :param func_ea: function start
   :returns: BADDADDR - no such function


.. py:data:: recalc_spd

.. py:data:: get_entry_qty

.. py:data:: add_entry

.. py:data:: get_entry_ordinal

.. py:data:: get_entry

.. py:data:: get_entry_name

.. py:data:: rename_entry

.. py:data:: get_next_fixup_ea

.. py:data:: get_prev_fixup_ea

.. py:function:: get_fixup_target_type(ea)

   Get fixup target type

   :param ea: address to get information about

   :returns: 0 - no fixup at the specified address
                otherwise returns fixup type


.. py:data:: FIXUP_OFF8
   :value: 13


.. py:data:: FIXUP_OFF16
   :value: 1


.. py:data:: FIXUP_SEG16
   :value: 2


.. py:data:: FIXUP_PTR32
   :value: 3


.. py:data:: FIXUP_OFF32
   :value: 4


.. py:data:: FIXUP_PTR48
   :value: 5


.. py:data:: FIXUP_HI8
   :value: 6


.. py:data:: FIXUP_HI16
   :value: 7


.. py:data:: FIXUP_LOW8
   :value: 8


.. py:data:: FIXUP_LOW16
   :value: 9


.. py:data:: FIXUP_OFF64
   :value: 12


.. py:data:: FIXUP_CUSTOM
   :value: 32768


.. py:function:: get_fixup_target_flags(ea)

   Get fixup target flags

   :param ea: address to get information about

   :returns: 0 - no fixup at the specified address
                otherwise returns fixup target flags


.. py:data:: FIXUPF_REL
   :value: 1


.. py:data:: FIXUPF_EXTDEF
   :value: 2


.. py:data:: FIXUPF_UNUSED
   :value: 4


.. py:data:: FIXUPF_CREATED
   :value: 8


.. py:function:: get_fixup_target_sel(ea)

   Get fixup target selector

   :param ea: address to get information about

   :returns: BADSEL - no fixup at the specified address
                     otherwise returns fixup target selector


.. py:function:: get_fixup_target_off(ea)

   Get fixup target offset

   :param ea: address to get information about

   :returns: BADADDR - no fixup at the specified address
                      otherwise returns fixup target offset


.. py:function:: get_fixup_target_dis(ea)

   Get fixup target displacement

   :param ea: address to get information about

   :returns: 0 - no fixup at the specified address
                otherwise returns fixup target displacement


.. py:function:: set_fixup(ea, fixuptype, fixupflags, targetsel, targetoff, displ)

   Set fixup information

   :param ea: address to set fixup information about
   :param fixuptype:  fixup type. see get_fixup_target_type()
                      for possible fixup types.
   :param fixupflags: fixup flags. see get_fixup_target_flags()
                      for possible fixup types.
   :param targetsel:  target selector
   :param targetoff:  target offset
   :param displ:      displacement

   :returns:        none


.. py:data:: del_fixup

.. py:data:: put_bookmark

.. py:data:: get_bookmark

.. py:data:: get_bookmark_desc

.. py:function:: get_struc_id(name)

.. py:function:: get_struc_name(tid)

.. py:function:: get_struc_cmt(tid)

.. py:function:: get_struc_size(tid)

.. py:function:: get_member_qty(sid)

   Get number of members of a structure

   :param sid: structure type ID

   :returns: -1 if bad structure type ID is passed otherwise
            returns number of members.


.. py:function:: get_member_by_idx(sid, idx)

   Get member ID by member ordinal number

   :param sid: structure type ID
   :param idx: member ordinal number

   :returns: -1 if bad structure type ID is passed or there is
            no member with the specified index
            otherwise returns the member ID.


.. py:function:: is_member_id(sid)

   Is a member id?

   :param sid: structure type ID

   :returns: True there is structure member with the specified ID
            False otherwise


.. py:function:: get_member_id(sid, member_offset)

   :param sid: structure type ID
   :param member_offset:. The offset can be
   any offset in the member. For example,
   is a member is 4 bytes long and starts
   at offset 2, then 2,3,4,5 denote
   the same structure member.

   :returns: -1 if bad structure type ID is passed or there is
   no member at the specified offset.
   otherwise returns the member id.


.. py:function:: get_member_offset(sid, member_name)

   Get offset of a member of a structure by the member name

   :param sid: structure type ID
   :param member_name: name of structure member

   :returns: -1 if bad structure type ID is passed
            or no such member in the structure
            otherwise returns offset of the specified member.

   NOTE: Union members are, in IDA's internals, located
          at subsequent byte offsets: member 0 -> offset 0x0,
          member 1 -> offset 0x1, etc...


.. py:function:: get_member_name(sid, member_offset)

   Get name of a member of a structure

   :param sid: structure type ID
   :param member_offset: member offset. The offset can be
                         any offset in the member. For example,
                         is a member is 4 bytes long and starts
                         at offset 2, then 2,3,4,5 denote
                         the same structure member.

   :returns: None if bad structure type ID is passed
            or no such member in the structure
            otherwise returns name of the specified member.


.. py:function:: get_member_cmt(sid, member_offset, repeatable=True)

   Get comment of a member

   :param sid: structure type ID
   :param member_offset: member offset. The offset can be
                         any offset in the member. For example,
                         is a member is 4 bytes long and starts
                         at offset 2, then 2,3,4,5 denote
                         the same structure member.
   :param repeatable: is not used anymore

   :returns: None if bad structure type ID is passed
            or no such member in the structure
            otherwise returns comment of the specified member.


.. py:function:: get_member_size(sid, member_offset)

   Get size of a member

   :param sid: structure type ID
   :param member_offset: member offset. The offset can be
                         any offset in the member. For example,
                         is a member is 4 bytes long and starts
                         at offset 2, then 2,3,4,5 denote
                         the same structure member.

   :returns: None if bad structure type ID is passed,
            or no such member in the structure
            otherwise returns size of the specified
            member in bytes.


.. py:function:: get_member_strid(sid, member_offset)

   Get structure id of a member

   :param sid: structure type ID
   :param member_offset: member offset. The offset can be
                         any offset in the member. For example,
                         is a member is 4 bytes long and starts
                         at offset 2, then 2,3,4,5 denote
                         the same structure member.
   :returns: -1 if bad structure type ID is passed
            or no such member in the structure
            otherwise returns structure id of the member.
            If the current member is not a structure, returns -1.


.. py:function:: is_union(sid)

   Is a structure a union?

   :param sid: structure type ID

   :returns: True: yes, this is a union id
            False: no

   NOTE: Unions are a special kind of structures


.. py:function:: add_struc(index, name, is_union)

   Define a new structure type

   :param index: -1
   :param name: name of the new structure type.
   :param is_union: 0: structure
                    1: union

   :returns: -1 if can't define structure type because of
            bad structure name: the name is ill-formed or is
            already used in the program.
            otherwise returns ID of the new structure type


.. py:function:: del_struc(sid)

   Delete a structure type

   :param sid: structure type ID

   :returns: 0 if bad structure type ID is passed
            1 otherwise the structure type is deleted. All data
            and other structure types referencing to the
            deleted structure type will be displayed as array
            of bytes.


.. py:function:: set_struc_name(sid, name)

.. py:function:: set_struc_cmt(sid, cmt, repeatable=True)

.. py:function:: add_struc_member(sid, name, offset, flag, typeid, nbytes, target=-1, tdelta=0, reftype=REF_OFF32)

   Add structure member

   :param sid: structure type ID
   :param name: name of the new member
   :param offset: offset of the new member
                  -1 means to add at the end of the structure
   :param flag: type of the new member. Should be one of
                FF_BYTE..FF_PACKREAL (see above) combined with FF_DATA
   :param typeid: if is_struct(flag) then typeid specifies the structure id for the member
                  if is_off0(flag) then typeid specifies the offset base.
                  if is_strlit(flag) then typeid specifies the string type (STRTYPE_...).
                  if is_stroff(flag) then typeid specifies the structure id
                  if is_enum(flag) then typeid specifies the enum id
                  if is_custom(flags) then typeid specifies the dtid and fid: dtid|(fid<<16)
                  Otherwise typeid should be -1.
   :param nbytes: number of bytes in the new member

   :param target: target address of the offset expr. You may specify it as
                  -1, ida will calculate it itself
   :param tdelta: offset target delta. usually 0
   :param reftype: see REF_... definitions

   NOTE: The remaining arguments are allowed only if is_off0(flag) and you want
          to specify a complex offset expression

   :returns: 0 - ok, otherwise error code (one of typeinf.TERR_*)



.. py:function:: del_struc_member(sid, member_offset)

   Delete structure member

   :param sid: structure type ID
   :param member_offset: offset of the member

   :returns: != 0 - ok.

   NOTE: IDA allows 'holes' between members of a
          structure. It treats these 'holes'
          as unnamed arrays of bytes.


.. py:function:: set_member_name(sid, member_offset, name)

   Change structure member name

   :param sid: structure type ID
   :param member_offset: offset of the member
   :param name: new name of the member

   :returns: != 0 - ok.


.. py:function:: set_member_type(sid, member_offset, flag, typeid, nitems, target=-1, tdelta=0, reftype=REF_OFF32)

   Change structure member type

   :param sid: structure type ID
   :param member_offset: offset of the member
   :param flag: new type of the member. Should be one of
                FF_BYTE..FF_PACKREAL (see above) combined with FF_DATA
   :param typeid: if is_struct(flag) then typeid specifies the structure id for the member
                  if is_off0(flag) then typeid specifies the offset base.
                  if is_strlit(flag) then typeid specifies the string type (STRTYPE_...).
                  if is_stroff(flag) then typeid specifies the structure id
                  if is_enum(flag) then typeid specifies the enum id
                  if is_custom(flags) then typeid specifies the dtid and fid: dtid|(fid<<16)
                  Otherwise typeid should be -1.
   :param nitems: number of items in the member

   :param target: target address of the offset expr. You may specify it as
                  -1, ida will calculate it itself
   :param tdelta: offset target delta. usually 0
   :param reftype: see REF_... definitions

   NOTE: The remaining arguments are allowed only if is_off0(flag) and you want
          to specify a complex offset expression

   :returns: !=0 - ok.


.. py:function:: set_member_cmt(sid, member_offset, comment, repeatable)

   Change structure member comment

   :param sid: structure type ID
   :param member_offset: offset of the member
   :param comment: new comment of the structure member
   :param repeatable: 1: change repeatable comment
                      0: change regular comment

   :returns: != 0 - ok


.. py:function:: expand_struc(sid, offset, delta, recalc=True)

   Expand or shrink a structure type
   :param id: structure type ID
   :param offset: offset in the structure
   :param delta: how many bytes to add or remove
   :param recalc: is not used anymore
   :returns: True if ok, False on error


.. py:data:: ENFL_REGEX
   :value: 1


.. py:function:: get_enum(name)

   Get enum by name

   :param name: enum type name

   :returns: enum type TID or BADADDR


.. py:function:: get_enum_name(enum_id, flags=0)

   Get name of enum

   :param enum_id: enum TID
   :param flags: use ENFL_REGEX to beautify the name

   :returns: enum name or None


.. py:function:: get_enum_cmt(enum_id)

   Get enum comment

   :param enum_id: enum TID

   :returns: enum comment


.. py:function:: get_enum_size(enum_id)

   Get the number of the members of the enum

   :param enum_id: enum TID

   :returns: number of members


.. py:function:: get_enum_width(enum_id)

   Get the width of a enum element
   allowed values: 0 (unspecified),1,2,4,8,16,32,64

   :param enum_id: enum TID

   :returns: enum width or -1 in case of error


.. py:function:: get_enum_flag(enum_id)

   Get flags determining the representation of the enum.
   (currently they define the numeric base: octal, decimal, hex, bin) and signness.

   :param enum_id: enum TID

   :returns: flag of 0


.. py:function:: get_enum_member_by_name(name)

   Get a reference to an enum member by its name

   :param name: enum member name

   :returns: enum member TID or BADADDR


.. py:function:: get_enum_member_enum(const_id)

   Get the parent enum of an enum member

   :param const_id: id of const

   :returns: enum TID or BADADDR


.. py:function:: get_enum_member(enum_id, value, serial, bmask)

   Get id of constant

   :param enum_id: id of enum
   :param value: value of constant
   :param serial: serial number of the constant in the
             enumeration. See op_enum() for details.
   :param bmask: bitmask of the constant
             ordinary enums accept only -1 as a bitmask

   :returns: id of constant or -1 if error


.. py:function:: get_first_bmask(enum_id)

   Get first bitmask in the enum

   :param enum_id: id of enum

   :returns: id of constant or -1 if error


.. py:function:: get_last_bmask(enum_id)

   Get last bitmask in the enum

   :param enum_id: id of enum

   :returns: id of constant or -1 if error


.. py:function:: get_next_bmask(enum_id, bmask)

   Get next bitmask in the enum

   :param enum_id: id of enum
   :param bmask

   :returns: id of constant or -1 if error


.. py:function:: get_prev_bmask(enum_id, bmask)

   Get prev bitmask in the enum

   :param enum_id: id of enum
   :param bmask

   :returns: id of constant or -1 if error


.. py:function:: get_bmask_name(enum_id, bmask)

   Get bitmask name (only for bitfields)

   :param enum_id: id of enum
   :param bmask: bitmask of the constant

   :returns: name of bitmask or None


.. py:function:: get_bmask_cmt(enum_id, bmask, repeatable)

   Get bitmask comment (only for bitfields)

   :param enum_id: id of enum
   :param bmask: bitmask of the constant
   :param repeatable: type of comment, 0-regular, 1-repeatable

   :returns: comment attached to bitmask or None


.. py:function:: set_bmask_name(enum_id, bmask, name)

   Set bitmask name (only for bitfields)

   :param enum_id: id of enum
   :param bmask: bitmask of the constant
   :param name: name of bitmask

   :returns: True-ok, False-failed


.. py:function:: set_bmask_cmt(enum_id, bmask, cmt, repeatable)

   Set bitmask comment (only for bitfields)

   :param enum_id: id of enum
   :param bmask: bitmask of the constant
   :param cmt: comment
   repeatable - is not used anymore

   :returns: 1-ok, 0-failed


.. py:function:: get_first_enum_member(enum_id, bmask=-1)

   Get first constant in the enum

   :param enum_id: id of enum
   :param bmask: bitmask of the constant (ordinary enums accept only -1 as a bitmask)

   :returns: value of constant or -1 if no constants are defined
            All constants are sorted by their values as unsigned longs.


.. py:function:: get_last_enum_member(enum_id, bmask=-1)

   Get last constant in the enum

   :param enum_id: id of enum
   :param bmask: bitmask of the constant (ordinary enums accept only -1 as a bitmask)

   :returns: value of constant or -1 if no constants are defined
            All constants are sorted by their values
            as unsigned longs.


.. py:function:: get_next_enum_member(enum_id, value, bmask=-1)

   Get next constant in the enum

   :param enum_id: id of enum
   :param bmask: bitmask of the constant ordinary enums accept only -1 as a bitmask
   :param value: value of the current constant

   :returns: value of a constant with value higher than the specified
            value. -1 if no such constants exist.
            All constants are sorted by their values as unsigned longs.


.. py:function:: get_prev_enum_member(enum_id, value, bmask=-1)

   Get prev constant in the enum

   :param enum_id: id of enum
   :param bmask  : bitmask of the constant
             ordinary enums accept only -1 as a bitmask
   :param value: value of the current constant

   :returns: value of a constant with value lower than the specified
       value. -1 if no such constants exist.
       All constants are sorted by their values as unsigned longs.


.. py:function:: get_enum_member_name(const_id)

   Get name of a constant

   :param const_id: id of const

   Returns: name of constant


.. py:function:: get_enum_member_cmt(const_id, repeatable=True)

   Get comment of a constant

   :param const_id: id of const
   :param repeatable: not used anymore

   :returns: comment string


.. py:function:: get_enum_member_value(const_id)

   Get value of an enum member

   :param const_id: id of const

   :returns: member value or None


.. py:function:: get_enum_member_bmask(const_id)

   Get bitmask of an enum member

   :param const_id: id of const

   :returns: member value or None


.. py:function:: add_enum(idx, name, flag)

   Add a new enum type

   :param idx: is not used anymore
   :param name: name of the enum.
   :param flag: flags for representation of numeric constants
                in the definition of enum.

   :returns: id of new enum or BADADDR


.. py:function:: del_enum(enum_id)

   Delete an enum type

   :param enum_id: id of enum

   :returns: success


.. py:function:: set_enum_name(enum_id, name)

   Set name of enum type

   :param enum_id: id of enum
   :param name: new enum name

   :returns: 1-ok, 0-failed


.. py:function:: set_enum_flag(enum_id, flag)

   Set enum constant representation flags

   :param enum_id: enum TID
   :param flag

   :returns: success


.. py:function:: set_enum_width(enum_id, nbytes)

   Set the width of enum base type

   :param enum_id: enum TID
   :param nbytes: width of enum base type, allowed values: 0 (unspecified),1,2,4,8,16,32,64

   :returns: success


.. py:function:: is_bf(enum_id)

   Is enum a bitmask ?

   :param enum_id: enum TID

   :returns: if it is a bitmask enum return True, otherwise False


.. py:function:: set_enum_bf(enum_id, bf)

   Set or clear the 'bitmask' attribute of an enum

   :param enum_id: enum TID
   :param bf: bitmask enum or not

   :returns: success


.. py:function:: set_enum_cmt(enum_id, cmt, repeatable)

   Set comment for enum type

   :param enum_id: enum TID
   :param cmt: comment
   :param repeatable: is comment repeatable ?

   :returns: 1-ok, 0-failed


.. py:function:: add_enum_member(enum_id, name, value, bmask=-1)

   Add a member of enum - a symbolic constant

   :param enum_id: id of enum
   :param name: name of symbolic constant. Must be unique in the program.
   :param value: value of symbolic constant.
   :param bmask: bitmask of the constant
       ordinary enums accept only -1 as a bitmask
       all bits set in value should be set in bmask too

   :returns: 0-ok, otherwise error code (one of ENUM_MEMBER_ERROR_*)


.. py:function:: del_enum_member(enum_id, value, serial, bmask=-1)

   Delete a member of enum - a symbolic constant

   :param enum_id: id of enum
   :param value: value of symbolic constant.
   :param serial: serial number of the constant in the
       enumeration. See op_enum() for for details.
   :param bmask: bitmask of the constant ordinary enums accept
       only -1 as a bitmask

   :returns: 1-ok, 0-failed


.. py:function:: set_enum_member_name(const_id, name)

   Set name of enum member

   :param const_id: enum constant TID
   :param name: new member name

   :returns: 1-ok, 0-failed


.. py:function:: set_enum_member_cmt(const_id, cmt, repeatable=False)

   Set comment for enum member

   :param const_id: enum constant TID
   :param cmt: comment
   :param repeatable: is not used anymore

   :returns: 1-ok, 0-failed


.. py:data:: AR_LONG

   Array of longs


.. py:data:: AR_STR

   Array of strings


.. py:function:: create_array(name)

   Create array.

   :param name: The array name.

   :returns: -1 in case of failure, a valid array_id otherwise.


.. py:function:: get_array_id(name)

   Get array array_id, by name.

   :param name: The array name.

   :returns: -1 in case of failure (i.e., no array with that
            name exists), a valid array_id otherwise.


.. py:function:: rename_array(array_id, newname)

   Rename array, by its ID.

   :param id: The ID of the array to rename.
   :param newname: The new name of the array.

   :returns: 1 in case of success, 0 otherwise


.. py:function:: delete_array(array_id)

   Delete array, by its ID.

   :param array_id: The ID of the array to delete.


.. py:function:: set_array_long(array_id, idx, value)

   Sets the long value of an array element.

   :param array_id: The array ID.
   :param idx: Index of an element.
   :param value: 32bit or 64bit value to store in the array

   :returns: 1 in case of success, 0 otherwise


.. py:function:: set_array_string(array_id, idx, value)

   Sets the string value of an array element.

   :param array_id: The array ID.
   :param idx: Index of an element.
   :param value: String value to store in the array

   :returns: 1 in case of success, 0 otherwise


.. py:function:: get_array_element(tag, array_id, idx)

   Get value of array element.

   :param tag: Tag of array, specifies one of two array types: AR_LONG, AR_STR
   :param array_id: The array ID.
   :param idx: Index of an element.

   :returns: Value of the specified array element. Note that
            this function may return char or long result. Unexistent
            array elements give zero as a result.


.. py:function:: del_array_element(tag, array_id, idx)

   Delete an array element.

   :param tag: Tag of array, specifies one of two array types: AR_LONG, AR_STR
   :param array_id: The array ID.
   :param idx: Index of an element.

   :returns: 1 in case of success, 0 otherwise.


.. py:function:: get_first_index(tag, array_id)

   Get index of the first existing array element.

   :param tag: Tag of array, specifies one of two array types: AR_LONG, AR_STR
   :param array_id: The array ID.

   :returns: -1 if the array is empty, otherwise index of first array
            element of given type.


.. py:function:: get_last_index(tag, array_id)

   Get index of last existing array element.

   :param tag: Tag of array, specifies one of two array types: AR_LONG, AR_STR
   :param array_id: The array ID.

   :returns: -1 if the array is empty, otherwise index of first array
            element of given type.


.. py:function:: get_next_index(tag, array_id, idx)

   Get index of the next existing array element.

   :param tag: Tag of array, specifies one of two array types: AR_LONG, AR_STR
   :param array_id: The array ID.
   :param idx: Index of the current element.

   :returns: -1 if no more elements, otherwise returns index of the
            next array element of given type.


.. py:function:: get_prev_index(tag, array_id, idx)

   Get index of the previous existing array element.

   :param tag: Tag of array, specifies one of two array types: AR_LONG, AR_STR
   :param array_id: The array ID.
   :param idx: Index of the current element.

   :returns: -1 if no more elements, otherwise returns index of the
            previous array element of given type.


.. py:function:: set_hash_long(hash_id, key, value)

   Sets the long value of a hash element.

   :param hash_id: The hash ID.
   :param key: Key of an element.
   :param value: 32bit or 64bit value to store in the hash

   :returns: 1 in case of success, 0 otherwise


.. py:function:: get_hash_long(hash_id, key)

   Gets the long value of a hash element.

   :param hash_id: The hash ID.
   :param key: Key of an element.

   :returns: the 32bit or 64bit value of the element, or 0 if no such
            element.


.. py:function:: set_hash_string(hash_id, key, value)

   Sets the string value of a hash element.

   :param hash_id: The hash ID.
   :param key: Key of an element.
   :param value: string value to store in the hash

   :returns: 1 in case of success, 0 otherwise


.. py:function:: get_hash_string(hash_id, key)

   Gets the string value of a hash element.

   :param hash_id: The hash ID.
   :param key: Key of an element.

   :returns: the string value of the element, or None if no such
            element.


.. py:function:: del_hash_string(hash_id, key)

   Delete a hash element.

   :param hash_id: The hash ID.
   :param key: Key of an element

   :returns: 1 upon success, 0 otherwise.


.. py:function:: get_first_hash_key(hash_id)

   Get the first key in the hash.

   :param hash_id: The hash ID.

   :returns: the key, 0 otherwise.


.. py:function:: get_last_hash_key(hash_id)

   Get the last key in the hash.

   :param hash_id: The hash ID.

   :returns: the key, 0 otherwise.


.. py:function:: get_next_hash_key(hash_id, key)

   Get the next key in the hash.

   :param hash_id: The hash ID.
   :param key: The current key.

   :returns: the next key, 0 otherwise


.. py:function:: get_prev_hash_key(hash_id, key)

   Get the previous key in the hash.

   :param hash_id: The hash ID.
   :param key: The current key.

   :returns: the previous key, 0 otherwise


.. py:data:: add_sourcefile

.. py:data:: get_sourcefile

.. py:data:: del_sourcefile

.. py:data:: set_source_linnum

.. py:data:: get_source_linnum

.. py:data:: del_source_linnum

.. py:function:: add_default_til(name)

   Load a type library

   :param name: name of type library.
   :returns: 1-ok, 0-failed.


.. py:function:: import_type(idx, type_name)

   Copy information from type library to database
   Copy structure, union, or enum definition from the type library
   to the IDA database.

   :param idx: -1, ignored
   :param type_name: name of type to copy

   :returns: BADNODE-failed, otherwise the type id (structure id or enum id)


.. py:function:: get_type(ea)

   Get type of function/variable

   :param ea: the address of the object

   :returns: type string or None if failed


.. py:function:: sizeof(typestr)

   Returns the size of the type. It is equivalent to IDC's sizeof().
   :param typestr: can be specified as a typeinfo tuple (e.g. the result of get_tinfo()),
           serialized type byte string,
           or a string with C declaration (e.g. "int")
   :returns: -1 if typestring is not valid or has no size. otherwise size of the type


.. py:data:: SizeOf

.. py:function:: get_tinfo(ea)

   Get type information of function/variable as 'typeinfo' object

   :param ea: the address of the object
   :returns: None on failure, or (type, fields) tuple.


.. py:function:: get_local_tinfo(ordinal)

   Get local type information as 'typeinfo' object

   :param ordinal:  slot number (1...NumberOfLocalTypes)
   :returns: None on failure, or (type, fields) tuple.


.. py:function:: guess_type(ea)

   Guess type of function/variable

   :param ea: the address of the object, can be the structure member id too

   :returns: type string or None if failed


.. py:data:: TINFO_GUESSED
   :value: 0


.. py:data:: TINFO_DEFINITE
   :value: 1


.. py:data:: TINFO_DELAYFUNC
   :value: 2


.. py:function:: apply_type(ea, py_type, flags=TINFO_DEFINITE)

   Apply the specified type to the address

   :param ea: the address of the object
   :param py_type: typeinfo tuple (type, fields) as get_tinfo() returns
                or tuple (name, type, fields) as parse_decl() returns
                or None
               if specified as None, then the
               item associated with 'ea' will be deleted.
   :param flags: combination of TINFO_... constants or 0
   :returns: Boolean


.. py:data:: PT_SIL

.. py:data:: PT_NDC

.. py:data:: PT_TYP

.. py:data:: PT_VAR

.. py:data:: PT_PACKMASK

.. py:data:: PT_HIGH

.. py:data:: PT_LOWER

.. py:data:: PT_REPLACE

.. py:data:: PT_RAWARGS

.. py:data:: PT_SILENT

.. py:data:: PT_PAKDEF
   :value: 0


.. py:data:: PT_PAK1
   :value: 16


.. py:data:: PT_PAK2
   :value: 32


.. py:data:: PT_PAK4
   :value: 48


.. py:data:: PT_PAK8
   :value: 64


.. py:data:: PT_PAK16
   :value: 80


.. py:data:: PT_FILE
   :value: 65536


.. py:data:: PT_STANDALONE

.. py:function:: SetType(ea, newtype)

   Set type of function/variable

   :param ea: the address of the object
   :param newtype: the type string in C declaration form.
               Must contain the closing ';'
               if specified as an empty string, then the
               item associated with 'ea' will be deleted.

   :returns: 1-ok, 0-failed.


.. py:function:: parse_decl(inputtype, flags)

   Parse type declaration

   :param inputtype: file name or C declarations (depending on the flags)
   :param flags: combination of PT_... constants or 0

   :returns: None on failure or (name, type, fields) tuple


.. py:function:: parse_decls(inputtype, flags=0)

   Parse type declarations

   :param inputtype: file name or C declarations (depending on the flags)
   :param flags: combination of PT_... constants or 0

   :returns: number of parsing errors (0 no errors)


.. py:function:: print_decls(ordinals, flags)

   Print types in a format suitable for use in a header file

   :param ordinals: comma-separated list of type ordinals
   :param flags: combination of PDF_... constants or 0

   :returns: string containing the type definitions


.. py:data:: PDF_INCL_DEPS
   :value: 1


.. py:data:: PDF_DEF_FWD
   :value: 2


.. py:data:: PDF_DEF_BASE
   :value: 4


.. py:data:: PDF_HEADER_CMT
   :value: 8


.. py:function:: get_ordinal_limit()

   Get number of local types + 1

   :returns: value >= 1. 1 means that there are no local types.


.. py:function:: set_local_type(ordinal, input, flags)

   Parse one type declaration and store it in the specified slot

   :param ordinal:  slot number (1...NumberOfLocalTypes)
                    -1 means allocate new slot or reuse the slot
                    of the existing named type
   :param input:  C declaration. Empty input empties the slot
   :param flags:  combination of PT_... constants or 0

   :returns: slot number or 0 if error


.. py:function:: GetLocalType(ordinal, flags)

   Retrieve a local type declaration
   :param flags: any of PRTYPE_* constants
   :returns: local type as a C declaration or ""


.. py:data:: PRTYPE_1LINE
   :value: 0


.. py:data:: PRTYPE_MULTI
   :value: 1


.. py:data:: PRTYPE_TYPE
   :value: 2


.. py:data:: PRTYPE_PRAGMA
   :value: 4


.. py:data:: PRTYPE_SEMI
   :value: 8


.. py:data:: PRTYPE_CPP
   :value: 16


.. py:data:: PRTYPE_DEF
   :value: 32


.. py:data:: PRTYPE_NOARGS
   :value: 64


.. py:data:: PRTYPE_NOARRS
   :value: 128


.. py:data:: PRTYPE_NORES
   :value: 256


.. py:data:: PRTYPE_RESTORE
   :value: 512


.. py:data:: PRTYPE_NOREGEX
   :value: 1024


.. py:data:: PRTYPE_COLORED
   :value: 2048


.. py:data:: PRTYPE_METHODS
   :value: 4096


.. py:data:: PRTYPE_1LINCMT
   :value: 8192


.. py:function:: get_numbered_type_name(ordinal)

   Retrieve a local type name

   :param ordinal:  slot number (1...NumberOfLocalTypes)

   returns: local type name or None


.. py:data:: add_hidden_range

.. py:function:: update_hidden_range(ea, visible)

   Set hidden range state

   :param ea:      any address belonging to the hidden range
   :param visible: new state of the range

   :returns: != 0 - ok


.. py:data:: del_hidden_range

.. py:data:: load_debugger

.. py:data:: start_process

.. py:data:: exit_process

.. py:data:: suspend_process

.. py:data:: get_processes

.. py:data:: attach_process

.. py:data:: detach_process

.. py:data:: get_thread_qty

.. py:data:: getn_thread

.. py:data:: get_current_thread

.. py:data:: getn_thread_name

.. py:data:: select_thread

.. py:data:: suspend_thread

.. py:data:: resume_thread

.. py:function:: get_first_module()

   Enumerate process modules

   :returns: first module's base address or None on failure


.. py:function:: get_next_module(base)

   Enumerate process modules

   :param base: previous module's base address

   :returns: next module's base address or None on failure


.. py:function:: get_module_name(base)

   Get process module name

   :param base: the base address of the module

   :returns: required info or None


.. py:function:: get_module_size(base)

   Get process module size

   :param base: the base address of the module

   :returns: required info or -1


.. py:data:: step_into

.. py:data:: step_over

.. py:data:: run_to

.. py:data:: step_until_ret

.. py:data:: wait_for_next_event

.. py:function:: resume_process()

.. py:function:: send_dbg_command(cmd)

   Sends a command to the debugger module and returns the output string.
   An exception will be raised if the debugger is not running or the current debugger does not export
   the 'send_dbg_command' IDC command.


.. py:data:: WFNE_ANY
   :value: 1


.. py:data:: WFNE_SUSP
   :value: 2


.. py:data:: WFNE_SILENT
   :value: 4


.. py:data:: WFNE_CONT
   :value: 8


.. py:data:: WFNE_NOWAIT
   :value: 16


.. py:data:: NOTASK
   :value: -2


.. py:data:: DBG_ERROR
   :value: -1


.. py:data:: DBG_TIMEOUT
   :value: 0


.. py:data:: PROCESS_STARTED
   :value: 1


.. py:data:: PROCESS_EXITED
   :value: 2


.. py:data:: THREAD_STARTED
   :value: 4


.. py:data:: THREAD_EXITED
   :value: 8


.. py:data:: BREAKPOINT
   :value: 16


.. py:data:: STEP
   :value: 32


.. py:data:: EXCEPTION
   :value: 64


.. py:data:: LIB_LOADED
   :value: 128


.. py:data:: LIB_UNLOADED
   :value: 256


.. py:data:: INFORMATION
   :value: 512


.. py:data:: PROCESS_ATTACHED
   :value: 1024


.. py:data:: PROCESS_DETACHED
   :value: 2048


.. py:data:: PROCESS_SUSPENDED
   :value: 4096


.. py:data:: refresh_debugger_memory

.. py:data:: take_memory_snapshot

.. py:data:: get_process_state

.. py:data:: DSTATE_SUSP
   :value: -1


.. py:data:: DSTATE_NOTASK
   :value: 0


.. py:data:: DSTATE_RUN
   :value: 1


.. py:data:: DSTATE_RUN_WAIT_ATTACH
   :value: 2


.. py:data:: DSTATE_RUN_WAIT_END
   :value: 3


   Get various information about the current debug event
   These functions are valid only when the current event exists
   (the process is in the suspended state)


.. py:function:: get_event_id()

   Get ID of debug event

   :returns: event ID


.. py:function:: get_event_pid()

   Get process ID for debug event

   :returns: process ID


.. py:function:: get_event_tid()

   Get type ID for debug event

   :returns: type ID


.. py:function:: get_event_ea()

   Get ea for debug event

   :returns: ea


.. py:function:: is_event_handled()

   Is the debug event handled?

   :returns: boolean


.. py:function:: get_event_module_name()

   Get module name for debug event

   :returns: module name


.. py:function:: get_event_module_base()

   Get module base for debug event

   :returns: module base


.. py:function:: get_event_module_size()

   Get module size for debug event

   :returns: module size


.. py:function:: get_event_exit_code()

   Get exit code for debug event

   :returns: exit code for PROCESS_EXITED, THREAD_EXITED events


.. py:function:: get_event_info()

   Get debug event info

   :returns: event info: for THREAD_STARTED (thread name)
                        for LIB_UNLOADED (unloaded library name)
                        for INFORMATION (message to display)


.. py:function:: get_event_bpt_hea()

   Get hardware address for BREAKPOINT event

   :returns: hardware address


.. py:function:: get_event_exc_code()

   Get exception code for EXCEPTION event

   :returns: exception code


.. py:function:: get_event_exc_ea()

   Get address for EXCEPTION event

   :returns: adress of exception


.. py:function:: can_exc_continue()

   Can it continue after EXCEPTION event?

   :returns: boolean


.. py:function:: get_event_exc_info()

   Get info for EXCEPTION event

   :returns: info string


.. py:data:: set_debugger_options

.. py:data:: DOPT_SEGM_MSGS
   :value: 1


.. py:data:: DOPT_START_BPT
   :value: 2


.. py:data:: DOPT_THREAD_MSGS
   :value: 4


.. py:data:: DOPT_THREAD_BPT
   :value: 8


.. py:data:: DOPT_BPT_MSGS
   :value: 16


.. py:data:: DOPT_LIB_MSGS
   :value: 64


.. py:data:: DOPT_LIB_BPT
   :value: 128


.. py:data:: DOPT_INFO_MSGS
   :value: 256


.. py:data:: DOPT_INFO_BPT
   :value: 512


.. py:data:: DOPT_REAL_MEMORY
   :value: 1024


.. py:data:: DOPT_REDO_STACK
   :value: 2048


.. py:data:: DOPT_ENTRY_BPT
   :value: 4096


.. py:data:: DOPT_EXCDLG
   :value: 24576


.. py:data:: EXCDLG_NEVER
   :value: 0


.. py:data:: EXCDLG_UNKNOWN
   :value: 8192


.. py:data:: EXCDLG_ALWAYS
   :value: 24576


.. py:data:: DOPT_LOAD_DINFO
   :value: 32768


.. py:data:: get_debugger_event_cond

.. py:data:: set_debugger_event_cond

.. py:data:: set_remote_debugger

.. py:data:: define_exception

.. py:data:: EXC_BREAK
   :value: 1


.. py:data:: EXC_HANDLE
   :value: 2


.. py:data:: get_reg_value

.. py:function:: set_reg_value(value, name)

   Set register value

   :param name: the register name
   :param value: new register value

   NOTE: The debugger should be running
          It is not necessary to use this function to set register values.
          A register name in the left side of an assignment will do too.


.. py:data:: get_bpt_qty

.. py:function:: get_bpt_ea(n)

   Get breakpoint address

   :param n: number of breakpoint, is in range 0..get_bpt_qty()-1

   :returns: address of the breakpoint or BADADDR


.. py:function:: get_bpt_attr(ea, bptattr)

   Get the characteristics of a breakpoint

   :param ea: any address in the breakpoint range
   :param bptattr: the desired attribute code, one of BPTATTR_... constants

   :returns: the desired attribute value or -1


.. py:data:: BPTATTR_EA
   :value: 1


.. py:data:: BPTATTR_SIZE
   :value: 2


.. py:data:: BPTATTR_TYPE
   :value: 3


.. py:data:: BPT_WRITE
   :value: 1


.. py:data:: BPT_RDWR
   :value: 3


.. py:data:: BPT_SOFT
   :value: 4


.. py:data:: BPT_EXEC
   :value: 8


.. py:data:: BPT_DEFAULT
   :value: 12


.. py:data:: BPTATTR_COUNT
   :value: 4


.. py:data:: BPTATTR_FLAGS
   :value: 5


.. py:data:: BPT_BRK
   :value: 1


.. py:data:: BPT_TRACE
   :value: 2


.. py:data:: BPT_UPDMEM
   :value: 4


.. py:data:: BPT_ENABLED
   :value: 8


.. py:data:: BPT_LOWCND
   :value: 16


.. py:data:: BPT_TRACEON
   :value: 32


.. py:data:: BPT_TRACE_INSN
   :value: 64


.. py:data:: BPT_TRACE_FUNC
   :value: 128


.. py:data:: BPT_TRACE_BBLK
   :value: 256


.. py:data:: BPTATTR_COND
   :value: 6


.. py:data:: BPTATTR_PID
   :value: 7


.. py:data:: BPTATTR_TID
   :value: 8


.. py:data:: BPLT_ABS
   :value: 0


.. py:data:: BPLT_REL
   :value: 1


.. py:data:: BPLT_SYM
   :value: 2


.. py:function:: set_bpt_attr(address, bptattr, value)

       modifiable characteristics of a breakpoint

   :param address: any address in the breakpoint range
   :param bptattr: the attribute code, one of BPTATTR_* constants
                   BPTATTR_CND is not allowed, see set_bpt_cond()
   :param value: the attribute value

   :returns: success


.. py:function:: set_bpt_cond(ea, cnd, is_lowcnd=0)

   Set breakpoint condition

   :param ea: any address in the breakpoint range
   :param cnd: breakpoint condition
   :param is_lowcnd: 0 - regular condition, 1 - low level condition

   :returns: success


.. py:data:: add_bpt

.. py:data:: del_bpt

.. py:data:: enable_bpt

.. py:data:: check_bpt

.. py:data:: BPTCK_NONE
   :value: -1


.. py:data:: BPTCK_NO
   :value: 0


.. py:data:: BPTCK_YES
   :value: 1


.. py:data:: BPTCK_ACT
   :value: 2


.. py:function:: enable_tracing(trace_level, enable)

   Enable step tracing

   :param trace_level:  what kind of trace to modify
   :param enable: 0: turn off, 1: turn on

   :returns: success


.. py:data:: TRACE_STEP
   :value: 0


.. py:data:: TRACE_INSN
   :value: 1


.. py:data:: TRACE_FUNC
   :value: 2


.. py:data:: get_step_trace_options

.. py:data:: set_step_trace_options

.. py:data:: ST_OVER_DEBUG_SEG
   :value: 1


.. py:data:: ST_OVER_LIB_FUNC
   :value: 2


.. py:data:: ST_ALREADY_LOGGED
   :value: 4


.. py:data:: ST_SKIP_LOOPS
   :value: 8


.. py:data:: load_trace_file

.. py:data:: save_trace_file

.. py:data:: is_valid_trace_file

.. py:data:: diff_trace_file

.. py:function:: clear_trace(filename)

   Clear the current trace buffer


.. py:data:: get_trace_file_desc

.. py:data:: set_trace_file_desc

.. py:data:: get_tev_qty

.. py:data:: get_tev_ea

.. py:data:: TEV_NONE
   :value: 0


.. py:data:: TEV_INSN
   :value: 1


.. py:data:: TEV_CALL
   :value: 2


.. py:data:: TEV_RET
   :value: 3


.. py:data:: TEV_BPT
   :value: 4


.. py:data:: TEV_MEM
   :value: 5


.. py:data:: TEV_EVENT
   :value: 6


.. py:data:: get_tev_type

.. py:data:: get_tev_tid

.. py:data:: get_tev_reg

.. py:data:: get_tev_mem_qty

.. py:data:: get_tev_mem

.. py:data:: get_tev_mem_ea

.. py:data:: get_call_tev_callee

.. py:data:: get_ret_tev_return

.. py:data:: get_bpt_tev_ea

.. py:function:: get_color(ea, what)

   Get item color

   :param ea: address of the item
   :param what: type of the item (one of  CIC_* constants)

   :returns: color code in RGB (hex 0xBBGGRR)


.. py:data:: CIC_ITEM
   :value: 1


.. py:data:: CIC_FUNC
   :value: 2


.. py:data:: CIC_SEGM
   :value: 3


.. py:data:: DEFCOLOR
   :value: 4294967295


.. py:function:: set_color(ea, what, color)

   Set item color

   :param ea: address of the item
   :param what: type of the item (one of CIC_* constants)
   :param color: new color code in RGB (hex 0xBBGGRR)

   :returns: success (True or False)


.. py:function:: force_bl_jump(ea)

   Some ARM compilers in Thumb mode use BL (branch-and-link)
   instead of B (branch) for long jumps, since BL has more range.
   By default, IDA tries to determine if BL is a jump or a call.
   You can override IDA's decision using commands in Edit/Other menu
   (Force BL call/Force BL jump) or the following two functions.

   Force BL instruction to be a jump

   :param ea: address of the BL instruction

   :returns: 1-ok, 0-failed


.. py:function:: force_bl_call(ea)

   Force BL instruction to be a call

   :param ea: address of the BL instruction

   :returns: 1-ok, 0-failed


.. py:function:: set_flag(off, bit, value)

.. py:function:: here()

.. py:function:: is_mapped(ea)

.. py:data:: ARGV
   :value: []


   The command line arguments passed to IDA via the -S switch.



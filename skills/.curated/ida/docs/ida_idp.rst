ida_idp
=======

.. py:module:: ida_idp

.. autoapi-nested-parse::

   Contains definition of the interface to IDP modules.

   The interface consists of two structures:
   * definition of target assembler: ::ash
   * definition of current processor: ::ph


   These structures contain information about target processor and assembler features.
   It also defines two groups of kernel events:
   * processor_t::event_t processor related events
   * idb_event:event_code_t database related events


   The processor related events are used to communicate with the processor module. The database related events are used to inform any interested parties, like plugins or processor modules, about the changes in the database. 
       



Attributes
----------

.. autoapisummary::

   ida_idp.IDP_INTERFACE_VERSION
   ida_idp.CF_STOP
   ida_idp.CF_CALL
   ida_idp.CF_CHG1
   ida_idp.CF_CHG2
   ida_idp.CF_CHG3
   ida_idp.CF_CHG4
   ida_idp.CF_CHG5
   ida_idp.CF_CHG6
   ida_idp.CF_USE1
   ida_idp.CF_USE2
   ida_idp.CF_USE3
   ida_idp.CF_USE4
   ida_idp.CF_USE5
   ida_idp.CF_USE6
   ida_idp.CF_JUMP
   ida_idp.CF_SHFT
   ida_idp.CF_HLL
   ida_idp.CF_CHG7
   ida_idp.CF_CHG8
   ida_idp.CF_USE7
   ida_idp.CF_USE8
   ida_idp.IRI_EXTENDED
   ida_idp.IRI_RET_LITERALLY
   ida_idp.IRI_SKIP_RETTARGET
   ida_idp.IRI_STRICT
   ida_idp.AS_OFFST
   ida_idp.AS_COLON
   ida_idp.AS_UDATA
   ida_idp.AS_2CHRE
   ida_idp.AS_NCHRE
   ida_idp.AS_N2CHR
   ida_idp.AS_1TEXT
   ida_idp.AS_NHIAS
   ida_idp.AS_NCMAS
   ida_idp.AS_HEXFM
   ida_idp.ASH_HEXF0
   ida_idp.ASH_HEXF1
   ida_idp.ASH_HEXF2
   ida_idp.ASH_HEXF3
   ida_idp.ASH_HEXF4
   ida_idp.ASH_HEXF5
   ida_idp.AS_DECFM
   ida_idp.ASD_DECF0
   ida_idp.ASD_DECF1
   ida_idp.ASD_DECF2
   ida_idp.ASD_DECF3
   ida_idp.AS_OCTFM
   ida_idp.ASO_OCTF0
   ida_idp.ASO_OCTF1
   ida_idp.ASO_OCTF2
   ida_idp.ASO_OCTF3
   ida_idp.ASO_OCTF4
   ida_idp.ASO_OCTF5
   ida_idp.ASO_OCTF6
   ida_idp.ASO_OCTF7
   ida_idp.AS_BINFM
   ida_idp.ASB_BINF0
   ida_idp.ASB_BINF1
   ida_idp.ASB_BINF2
   ida_idp.ASB_BINF3
   ida_idp.ASB_BINF4
   ida_idp.ASB_BINF5
   ida_idp.AS_UNEQU
   ida_idp.AS_ONEDUP
   ida_idp.AS_NOXRF
   ida_idp.AS_XTRNTYPE
   ida_idp.AS_RELSUP
   ida_idp.AS_LALIGN
   ida_idp.AS_NOCODECLN
   ida_idp.AS_NOSPACE
   ida_idp.AS_ALIGN2
   ida_idp.AS_ASCIIC
   ida_idp.AS_ASCIIZ
   ida_idp.AS2_BRACE
   ida_idp.AS2_STRINV
   ida_idp.AS2_BYTE1CHAR
   ida_idp.AS2_IDEALDSCR
   ida_idp.AS2_TERSESTR
   ida_idp.AS2_COLONSUF
   ida_idp.AS2_YWORD
   ida_idp.AS2_ZWORD
   ida_idp.HKCB_GLOBAL
   ida_idp.PLFM_386
   ida_idp.PLFM_Z80
   ida_idp.PLFM_I860
   ida_idp.PLFM_8051
   ida_idp.PLFM_TMS
   ida_idp.PLFM_6502
   ida_idp.PLFM_PDP
   ida_idp.PLFM_68K
   ida_idp.PLFM_JAVA
   ida_idp.PLFM_6800
   ida_idp.PLFM_ST7
   ida_idp.PLFM_MC6812
   ida_idp.PLFM_MIPS
   ida_idp.PLFM_ARM
   ida_idp.PLFM_TMSC6
   ida_idp.PLFM_PPC
   ida_idp.PLFM_80196
   ida_idp.PLFM_Z8
   ida_idp.PLFM_SH
   ida_idp.PLFM_NET
   ida_idp.PLFM_AVR
   ida_idp.PLFM_H8
   ida_idp.PLFM_PIC
   ida_idp.PLFM_SPARC
   ida_idp.PLFM_ALPHA
   ida_idp.PLFM_HPPA
   ida_idp.PLFM_H8500
   ida_idp.PLFM_TRICORE
   ida_idp.PLFM_DSP56K
   ida_idp.PLFM_C166
   ida_idp.PLFM_ST20
   ida_idp.PLFM_IA64
   ida_idp.PLFM_I960
   ida_idp.PLFM_F2MC
   ida_idp.PLFM_TMS320C54
   ida_idp.PLFM_TMS320C55
   ida_idp.PLFM_TRIMEDIA
   ida_idp.PLFM_M32R
   ida_idp.PLFM_NEC_78K0
   ida_idp.PLFM_NEC_78K0S
   ida_idp.PLFM_M740
   ida_idp.PLFM_M7700
   ida_idp.PLFM_ST9
   ida_idp.PLFM_FR
   ida_idp.PLFM_MC6816
   ida_idp.PLFM_M7900
   ida_idp.PLFM_TMS320C3
   ida_idp.PLFM_KR1878
   ida_idp.PLFM_AD218X
   ida_idp.PLFM_OAKDSP
   ida_idp.PLFM_TLCS900
   ida_idp.PLFM_C39
   ida_idp.PLFM_CR16
   ida_idp.PLFM_MN102L00
   ida_idp.PLFM_TMS320C1X
   ida_idp.PLFM_NEC_V850X
   ida_idp.PLFM_SCR_ADPT
   ida_idp.PLFM_EBC
   ida_idp.PLFM_MSP430
   ida_idp.PLFM_SPU
   ida_idp.PLFM_DALVIK
   ida_idp.PLFM_65C816
   ida_idp.PLFM_M16C
   ida_idp.PLFM_ARC
   ida_idp.PLFM_UNSP
   ida_idp.PLFM_TMS320C28
   ida_idp.PLFM_DSP96K
   ida_idp.PLFM_SPC700
   ida_idp.PLFM_AD2106X
   ida_idp.PLFM_PIC16
   ida_idp.PLFM_S390
   ida_idp.PLFM_XTENSA
   ida_idp.PLFM_RISCV
   ida_idp.PLFM_RL78
   ida_idp.PLFM_RX
   ida_idp.PLFM_WASM
   ida_idp.PR_SEGS
   ida_idp.PR_USE32
   ida_idp.PR_DEFSEG32
   ida_idp.PR_RNAMESOK
   ida_idp.PR_ADJSEGS
   ida_idp.PR_DEFNUM
   ida_idp.PRN_HEX
   ida_idp.PRN_OCT
   ida_idp.PRN_DEC
   ida_idp.PRN_BIN
   ida_idp.PR_WORD_INS
   ida_idp.PR_NOCHANGE
   ida_idp.PR_ASSEMBLE
   ida_idp.PR_ALIGN
   ida_idp.PR_TYPEINFO
   ida_idp.PR_USE64
   ida_idp.PR_SGROTHER
   ida_idp.PR_STACK_UP
   ida_idp.PR_BINMEM
   ida_idp.PR_SEGTRANS
   ida_idp.PR_CHK_XREF
   ida_idp.PR_NO_SEGMOVE
   ida_idp.PR_USE_ARG_TYPES
   ida_idp.PR_SCALE_STKVARS
   ida_idp.PR_DELAYED
   ida_idp.PR_ALIGN_INSN
   ida_idp.PR_PURGING
   ida_idp.PR_CNDINSNS
   ida_idp.PR_USE_TBYTE
   ida_idp.PR_DEFSEG64
   ida_idp.PR_OUTER
   ida_idp.PR2_MAPPINGS
   ida_idp.PR2_IDP_OPTS
   ida_idp.PR2_CODE16_BIT
   ida_idp.PR2_MACRO
   ida_idp.PR2_USE_CALCREL
   ida_idp.PR2_REL_BITS
   ida_idp.PR2_FORCE_16BIT
   ida_idp.OP_FP_BASED
   ida_idp.OP_SP_BASED
   ida_idp.OP_SP_ADD
   ida_idp.OP_SP_SUB
   ida_idp.CUSTOM_INSN_ITYPE
   ida_idp.REG_SPOIL
   ida_idp.NO_ACCESS
   ida_idp.WRITE_ACCESS
   ida_idp.READ_ACCESS
   ida_idp.RW_ACCESS
   ida_idp.SETPROC_IDB
   ida_idp.SETPROC_LOADER
   ida_idp.SETPROC_LOADER_NON_FATAL
   ida_idp.SETPROC_USER
   ida_idp.LTC_NONE
   ida_idp.LTC_ADDED
   ida_idp.LTC_DELETED
   ida_idp.LTC_EDITED
   ida_idp.LTC_ALIASED
   ida_idp.LTC_COMPILER
   ida_idp.LTC_TIL_LOADED
   ida_idp.LTC_TIL_UNLOADED
   ida_idp.LTC_TIL_COMPACTED
   ida_idp.closebase
   ida_idp.savebase
   ida_idp.upgraded
   ida_idp.auto_empty
   ida_idp.auto_empty_finally
   ida_idp.determined_main
   ida_idp.extlang_changed
   ida_idp.idasgn_loaded
   ida_idp.kernel_config_loaded
   ida_idp.loader_finished
   ida_idp.flow_chart_created
   ida_idp.compiler_changed
   ida_idp.changing_ti
   ida_idp.ti_changed
   ida_idp.changing_op_ti
   ida_idp.op_ti_changed
   ida_idp.changing_op_type
   ida_idp.op_type_changed
   ida_idp.segm_added
   ida_idp.deleting_segm
   ida_idp.segm_deleted
   ida_idp.changing_segm_start
   ida_idp.segm_start_changed
   ida_idp.changing_segm_end
   ida_idp.segm_end_changed
   ida_idp.changing_segm_name
   ida_idp.segm_name_changed
   ida_idp.changing_segm_class
   ida_idp.segm_class_changed
   ida_idp.segm_attrs_updated
   ida_idp.segm_moved
   ida_idp.allsegs_moved
   ida_idp.func_added
   ida_idp.func_updated
   ida_idp.set_func_start
   ida_idp.set_func_end
   ida_idp.deleting_func
   ida_idp.frame_deleted
   ida_idp.thunk_func_created
   ida_idp.func_tail_appended
   ida_idp.deleting_func_tail
   ida_idp.func_tail_deleted
   ida_idp.tail_owner_changed
   ida_idp.func_noret_changed
   ida_idp.stkpnts_changed
   ida_idp.updating_tryblks
   ida_idp.tryblks_updated
   ida_idp.deleting_tryblks
   ida_idp.sgr_changed
   ida_idp.make_code
   ida_idp.make_data
   ida_idp.destroyed_items
   ida_idp.renamed
   ida_idp.byte_patched
   ida_idp.changing_cmt
   ida_idp.cmt_changed
   ida_idp.changing_range_cmt
   ida_idp.range_cmt_changed
   ida_idp.extra_cmt_changed
   ida_idp.item_color_changed
   ida_idp.callee_addr_changed
   ida_idp.bookmark_changed
   ida_idp.sgr_deleted
   ida_idp.adding_segm
   ida_idp.func_deleted
   ida_idp.dirtree_mkdir
   ida_idp.dirtree_rmdir
   ida_idp.dirtree_link
   ida_idp.dirtree_move
   ida_idp.dirtree_rank
   ida_idp.dirtree_rminode
   ida_idp.dirtree_segm_moved
   ida_idp.local_types_changed
   ida_idp.lt_udm_created
   ida_idp.lt_udm_deleted
   ida_idp.lt_udm_renamed
   ida_idp.lt_udm_changed
   ida_idp.lt_udt_expanded
   ida_idp.frame_created
   ida_idp.frame_udm_created
   ida_idp.frame_udm_deleted
   ida_idp.frame_udm_renamed
   ida_idp.frame_udm_changed
   ida_idp.frame_expanded
   ida_idp.idasgn_matched_ea
   ida_idp.lt_edm_created
   ida_idp.lt_edm_deleted
   ida_idp.lt_edm_renamed
   ida_idp.lt_edm_changed
   ida_idp.local_type_renamed
   ida_idp.IDPOPT_CST
   ida_idp.IDPOPT_JVL
   ida_idp.IDPOPT_PRI_DEFAULT
   ida_idp.IDPOPT_PRI_HIGH
   ida_idp.IDPOPT_NUM_INT
   ida_idp.IDPOPT_NUM_CHAR
   ida_idp.IDPOPT_NUM_SHORT
   ida_idp.IDPOPT_NUM_RANGE
   ida_idp.IDPOPT_NUM_UNS
   ida_idp.IDPOPT_BIT_UINT
   ida_idp.IDPOPT_BIT_UCHAR
   ida_idp.IDPOPT_BIT_USHORT
   ida_idp.IDPOPT_BIT_BOOL
   ida_idp.IDPOPT_STR_QSTRING
   ida_idp.IDPOPT_STR_LONG
   ida_idp.IDPOPT_I64_RANGE
   ida_idp.IDPOPT_I64_UNS
   ida_idp.IDPOPT_CST_PARAMS
   ida_idp.IDPOPT_MBROFF
   ida_idp.cik_string
   ida_idp.cik_filename
   ida_idp.cik_path
   ida_idp.REAL_ERROR_FORMAT
   ida_idp.REAL_ERROR_RANGE
   ida_idp.REAL_ERROR_BADDATA
   ida_idp.IDPOPT_STR
   ida_idp.IDPOPT_NUM
   ida_idp.IDPOPT_BIT
   ida_idp.IDPOPT_FLT
   ida_idp.IDPOPT_I64
   ida_idp.IDPOPT_OK
   ida_idp.IDPOPT_BADKEY
   ida_idp.IDPOPT_BADTYPE
   ida_idp.IDPOPT_BADVALUE
   ida_idp.ph


Classes
-------

.. autoapisummary::

   ida_idp.reg_access_vec_t
   ida_idp.asm_t
   ida_idp.reg_info_t
   ida_idp.reg_access_t
   ida_idp.reg_accesses_t
   ida_idp.num_range_t
   ida_idp.params_t
   ida_idp.IDP_Hooks
   ida_idp.processor_t
   ida_idp.IDB_Hooks


Functions
---------

.. autoapisummary::

   ida_idp.has_cf_chg
   ida_idp.has_cf_use
   ida_idp.has_insn_feature
   ida_idp.is_call_insn
   ida_idp.is_ret_insn
   ida_idp.is_indirect_jump_insn
   ida_idp.is_basic_block_end
   ida_idp.get_ph
   ida_idp.get_ash
   ida_idp.str2reg
   ida_idp.is_align_insn
   ida_idp.get_reg_name
   ida_idp.parse_reg_name
   ida_idp.set_processor_type
   ida_idp.get_idp_name
   ida_idp.set_target_assembler
   ida_idp.gen_idb_event
   ida_idp.register_cfgopts
   ida_idp.get_config_value
   ida_idp.cfg_get_cc_parm
   ida_idp.cfg_get_cc_header_path
   ida_idp.cfg_get_cc_predefined_macros
   ida_idp.process_config_directive
   ida_idp.AssembleLine
   ida_idp.assemble
   ida_idp.ph_get_id
   ida_idp.ph_get_version
   ida_idp.ph_get_flag
   ida_idp.ph_get_cnbits
   ida_idp.ph_get_dnbits
   ida_idp.ph_get_reg_first_sreg
   ida_idp.ph_get_reg_last_sreg
   ida_idp.ph_get_segreg_size
   ida_idp.ph_get_reg_code_sreg
   ida_idp.ph_get_reg_data_sreg
   ida_idp.ph_get_icode_return
   ida_idp.ph_get_instruc_start
   ida_idp.ph_get_instruc_end
   ida_idp.ph_get_tbyte_size
   ida_idp.ph_get_instruc
   ida_idp.ph_get_regnames
   ida_idp.ph_get_operand_info
   ida_idp.ph_calcrel
   ida_idp.ph_find_reg_value
   ida_idp.ph_find_op_value
   ida_idp.ph_get_reg_accesses
   ida_idp.ph_get_abi_info
   ida_idp.get_idp_notifier_addr
   ida_idp.get_idp_notifier_ud_addr
   ida_idp.delay_slot_insn
   ida_idp.get_reg_info
   ida_idp.sizeof_ldbl
   ida_idp.str2sreg
   ida_idp.get_idb_notifier_addr
   ida_idp.get_idb_notifier_ud_addr


Module Contents
---------------

.. py:class:: reg_access_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> reg_access_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> reg_access_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: reg_access_vec_t) -> None


   .. py:method:: extract() -> reg_access_t *


   .. py:method:: inject(s: reg_access_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< reg_access_t >::const_iterator


   .. py:method:: end(*args) -> qvector< reg_access_t >::const_iterator


   .. py:method:: insert(it: reg_access_t, x: reg_access_t) -> qvector< reg_access_t >::iterator


   .. py:method:: erase(*args) -> qvector< reg_access_t >::iterator


   .. py:method:: find(*args) -> qvector< reg_access_t >::const_iterator


   .. py:method:: has(x: reg_access_t) -> bool


   .. py:method:: add_unique(x: reg_access_t) -> bool


   .. py:method:: append(x: reg_access_t) -> None


   .. py:method:: extend(x: reg_access_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:data:: IDP_INTERFACE_VERSION

   The interface version number. 
           


.. py:data:: CF_STOP

   Instruction doesn't pass execution to the next instruction 
           


.. py:data:: CF_CALL

   CALL instruction (should make a procedure here)


.. py:data:: CF_CHG1

   The instruction modifies the first operand.


.. py:data:: CF_CHG2

   The instruction modifies the second operand.


.. py:data:: CF_CHG3

   The instruction modifies the third operand.


.. py:data:: CF_CHG4

   The instruction modifies the fourth operand.


.. py:data:: CF_CHG5

   The instruction modifies the fifth operand.


.. py:data:: CF_CHG6

   The instruction modifies the sixth operand.


.. py:data:: CF_USE1

   The instruction uses value of the first operand.


.. py:data:: CF_USE2

   The instruction uses value of the second operand.


.. py:data:: CF_USE3

   The instruction uses value of the third operand.


.. py:data:: CF_USE4

   The instruction uses value of the fourth operand.


.. py:data:: CF_USE5

   The instruction uses value of the fifth operand.


.. py:data:: CF_USE6

   The instruction uses value of the sixth operand.


.. py:data:: CF_JUMP

   The instruction passes execution using indirect jump or call (thus needs additional analysis) 
           


.. py:data:: CF_SHFT

   Bit-shift instruction (shl,shr...)


.. py:data:: CF_HLL

   Instruction may be present in a high level language function 
           


.. py:data:: CF_CHG7

   The instruction modifies the seventh operand.


.. py:data:: CF_CHG8

   The instruction modifies the eighth operand.


.. py:data:: CF_USE7

   The instruction uses value of the seventh operand.


.. py:data:: CF_USE8

   The instruction uses value of the eighth operand.


.. py:function:: has_cf_chg(feature: int, opnum: uint) -> bool

   Does an instruction with the specified feature modify the i-th operand?


.. py:function:: has_cf_use(feature: int, opnum: uint) -> bool

   Does an instruction with the specified feature use a value of the i-th operand?


.. py:function:: has_insn_feature(icode: uint16, bit: int) -> bool

   Does the specified instruction have the specified feature?


.. py:function:: is_call_insn(insn: insn_t const &) -> bool

   Is the instruction a "call"?


.. py:data:: IRI_EXTENDED

   Is the instruction a "return"?

   include instructions like "leave" that begin the function epilog 
           


.. py:data:: IRI_RET_LITERALLY

   report only 'ret' instructions


.. py:data:: IRI_SKIP_RETTARGET

   exclude 'ret' instructions that have special targets (see set_ret_target in PC) 
           


.. py:data:: IRI_STRICT

.. py:function:: is_ret_insn(*args) -> bool

.. py:function:: is_indirect_jump_insn(insn: insn_t const &) -> bool

   Is the instruction an indirect jump?


.. py:function:: is_basic_block_end(insn: insn_t const &, call_insn_stops_block: bool) -> bool

   Is the instruction the end of a basic block?


.. py:class:: asm_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: flag
      :type:  int

      Assembler feature bits 
              



   .. py:attribute:: uflag
      :type:  uint16

      user defined flags (local only for IDP) you may define and use your own bits 
              



   .. py:attribute:: name
      :type:  str

      Assembler name (displayed in menus)



   .. py:attribute:: help
      :type:  help_t

      Help screen number, 0 - no help.



   .. py:attribute:: header
      :type:  char const *const *

      array of automatically generated header lines they appear at the start of disassembled text 
              



   .. py:attribute:: origin
      :type:  str

      org directive



   .. py:attribute:: end
      :type:  str

      end directive



   .. py:attribute:: cmnt
      :type:  str

      comment string (see also cmnt2)



   .. py:attribute:: ascsep
      :type:  char

      string literal delimiter



   .. py:attribute:: accsep
      :type:  char

      char constant delimiter



   .. py:attribute:: esccodes
      :type:  str

      special chars that cannot appear as is in string and char literals 
              



   .. py:attribute:: a_ascii
      :type:  str

      string literal directive



   .. py:attribute:: a_byte
      :type:  str

      byte directive



   .. py:attribute:: a_word
      :type:  str

      word directive



   .. py:attribute:: a_dword
      :type:  str

      nullptr if not allowed



   .. py:attribute:: a_qword
      :type:  str

      nullptr if not allowed



   .. py:attribute:: a_oword
      :type:  str

      nullptr if not allowed



   .. py:attribute:: a_float
      :type:  str

      float; 4bytes; nullptr if not allowed



   .. py:attribute:: a_double
      :type:  str

      double; 8bytes; nullptr if not allowed



   .. py:attribute:: a_tbyte
      :type:  str

      long double; nullptr if not allowed



   .. py:attribute:: a_packreal
      :type:  str

      packed decimal real nullptr if not allowed



   .. py:attribute:: a_dups
      :type:  str

      array keyword. the following sequences may appear:
      * #h header
      * #d size
      * #v value
      * #s(b,w,l,q,f,d,o) size specifiers for byte,word, dword,qword, float,double,oword 


              



   .. py:attribute:: a_bss
      :type:  str

      uninitialized data directive should include 's' for the size of data 
              



   .. py:attribute:: a_equ
      :type:  str

      'equ' Used if AS_UNEQU is set



   .. py:attribute:: a_seg
      :type:  str

      'seg ' prefix (example: push seg seg001)



   .. py:attribute:: a_curip
      :type:  str

      current IP (instruction pointer) symbol in assembler



   .. py:attribute:: a_public
      :type:  str

      "public" name keyword. nullptr-use default, ""-do not generate



   .. py:attribute:: a_weak
      :type:  str

      "weak" name keyword. nullptr-use default, ""-do not generate



   .. py:attribute:: a_extrn
      :type:  str

      "extern" name keyword



   .. py:attribute:: a_comdef
      :type:  str

      "comm" (communal variable)



   .. py:attribute:: a_align
      :type:  str

      "align" keyword



   .. py:attribute:: lbrace
      :type:  char

      left brace used in complex expressions



   .. py:attribute:: rbrace
      :type:  char

      right brace used in complex expressions



   .. py:attribute:: a_mod
      :type:  str

      % mod assembler time operation



   .. py:attribute:: a_band
      :type:  str

      & bit and assembler time operation



   .. py:attribute:: a_bor
      :type:  str

      | bit or assembler time operation



   .. py:attribute:: a_xor
      :type:  str

      ^ bit xor assembler time operation



   .. py:attribute:: a_bnot
      :type:  str

      ~ bit not assembler time operation



   .. py:attribute:: a_shl
      :type:  str

      << shift left assembler time operation



   .. py:attribute:: a_shr
      :type:  str

      >> shift right assembler time operation



   .. py:attribute:: a_sizeof_fmt
      :type:  str

      size of type (format string)



   .. py:attribute:: flag2
      :type:  int

      Secondary assembler feature bits 
              



   .. py:attribute:: cmnt2
      :type:  str

      comment close string (usually nullptr) this is used to denote a string which closes comments, for example, if the comments are represented with (* ... *) then cmnt = "(*" and cmnt2 = "*)" 
              



   .. py:attribute:: low8
      :type:  str

      low8 operation, should contain s for the operand



   .. py:attribute:: high8
      :type:  str

      high8



   .. py:attribute:: low16
      :type:  str

      low16



   .. py:attribute:: high16
      :type:  str

      high16



   .. py:attribute:: a_include_fmt
      :type:  str

      the include directive (format string)



   .. py:attribute:: a_vstruc_fmt
      :type:  str

      if a named item is a structure and displayed in the verbose (multiline) form then display the name as printf(a_strucname_fmt, typename) (for asms with type checking, e.g. tasm ideal) 
              



   .. py:attribute:: a_rva
      :type:  str

      'rva' keyword for image based offsets (see REFINFO_RVAOFF) 
              



   .. py:attribute:: a_yword
      :type:  str

      32-byte (256-bit) data; nullptr if not allowed requires AS2_YWORD 
              



   .. py:attribute:: a_zword
      :type:  str

      64-byte (512-bit) data; nullptr if not allowed requires AS2_ZWORD 
              



.. py:data:: AS_OFFST

   offsets are 'offset xxx' ?


.. py:data:: AS_COLON

   create colons after data names ?


.. py:data:: AS_UDATA

   can use '?' in data directives


.. py:data:: AS_2CHRE

   double char constants are: "xy


.. py:data:: AS_NCHRE

   char constants are: 'x


.. py:data:: AS_N2CHR

   can't have 2 byte char consts


.. py:data:: AS_1TEXT

   1 text per line, no bytes


.. py:data:: AS_NHIAS

   no characters with high bit


.. py:data:: AS_NCMAS

   no commas in ascii directives


.. py:data:: AS_HEXFM

   mask - hex number format


.. py:data:: ASH_HEXF0

   34h


.. py:data:: ASH_HEXF1

   h'34


.. py:data:: ASH_HEXF2

   34


.. py:data:: ASH_HEXF3

   0x34


.. py:data:: ASH_HEXF4

   $34


.. py:data:: ASH_HEXF5

   <^R > (radix)


.. py:data:: AS_DECFM

   mask - decimal number format


.. py:data:: ASD_DECF0

   34


.. py:data:: ASD_DECF1

   #34


.. py:data:: ASD_DECF2

   34.


.. py:data:: ASD_DECF3

   .34


.. py:data:: AS_OCTFM

   mask - octal number format


.. py:data:: ASO_OCTF0

   123o


.. py:data:: ASO_OCTF1

   0123


.. py:data:: ASO_OCTF2

   123


.. py:data:: ASO_OCTF3

   @123


.. py:data:: ASO_OCTF4

   o'123


.. py:data:: ASO_OCTF5

   123q


.. py:data:: ASO_OCTF6

   ~123


.. py:data:: ASO_OCTF7

   q'123


.. py:data:: AS_BINFM

   mask - binary number format


.. py:data:: ASB_BINF0

   010101b


.. py:data:: ASB_BINF1

   ^B010101


.. py:data:: ASB_BINF2

   %010101


.. py:data:: ASB_BINF3

   0b1010101


.. py:data:: ASB_BINF4

   b'1010101


.. py:data:: ASB_BINF5

   b'1010101'


.. py:data:: AS_UNEQU

   replace undefined data items with EQU (for ANTA's A80)


.. py:data:: AS_ONEDUP

   One array definition per line.


.. py:data:: AS_NOXRF

   Disable xrefs during the output file generation.


.. py:data:: AS_XTRNTYPE

   Assembler understands type of extern symbols as ":type" suffix.


.. py:data:: AS_RELSUP

   Checkarg: 'and','or','xor' operations with addresses are possible.


.. py:data:: AS_LALIGN

   Labels at "align" keyword are supported.


.. py:data:: AS_NOCODECLN

   don't create colons after code names


.. py:data:: AS_NOSPACE

   No spaces in expressions.


.. py:data:: AS_ALIGN2

   .align directive expects an exponent rather than a power of 2 (.align 5 means to align at 32byte boundary) 
           


.. py:data:: AS_ASCIIC

   ascii directive accepts C-like escape sequences (\n,\x01 and similar) 
           


.. py:data:: AS_ASCIIZ

   ascii directive inserts implicit zero byte at the end


.. py:data:: AS2_BRACE

   Use braces for all expressions.


.. py:data:: AS2_STRINV

   Invert meaning of idainfo::wide_high_byte_first for text strings (for processors with bytes bigger than 8 bits) 
           


.. py:data:: AS2_BYTE1CHAR

   One symbol per processor byte. Meaningful only for wide byte processors 
           


.. py:data:: AS2_IDEALDSCR

   Description of struc/union is in the 'reverse' form (keyword before name), the same as in borland tasm ideal 
           


.. py:data:: AS2_TERSESTR

   'terse' structure initialization form; NAME<fld,fld,...> is supported 
           


.. py:data:: AS2_COLONSUF

   addresses may have ":xx" suffix; this suffix must be ignored when extracting the address under the cursor 
           


.. py:data:: AS2_YWORD

   a_yword field is present and valid


.. py:data:: AS2_ZWORD

   a_zword field is present and valid


.. py:data:: HKCB_GLOBAL

   is global event listener? if true, the listener will survive database closing and opening. it will stay in the memory until explicitly unhooked. otherwise the kernel will delete it as soon as the owner is unloaded. should be used only with PLUGIN_FIX plugins. 
           


.. py:data:: PLFM_386

   Intel 80x86.


.. py:data:: PLFM_Z80

   8085, Z80


.. py:data:: PLFM_I860

   Intel 860.


.. py:data:: PLFM_8051

   8051


.. py:data:: PLFM_TMS

   Texas Instruments TMS320C5x.


.. py:data:: PLFM_6502

   6502


.. py:data:: PLFM_PDP

   PDP11.


.. py:data:: PLFM_68K

   Motorola 680x0.


.. py:data:: PLFM_JAVA

   Java.


.. py:data:: PLFM_6800

   Motorola 68xx.


.. py:data:: PLFM_ST7

   SGS-Thomson ST7.


.. py:data:: PLFM_MC6812

   Motorola 68HC12.


.. py:data:: PLFM_MIPS

   MIPS.


.. py:data:: PLFM_ARM

   Advanced RISC Machines.


.. py:data:: PLFM_TMSC6

   Texas Instruments TMS320C6x.


.. py:data:: PLFM_PPC

   PowerPC.


.. py:data:: PLFM_80196

   Intel 80196.


.. py:data:: PLFM_Z8

   Z8.


.. py:data:: PLFM_SH

   Renesas (formerly Hitachi) SuperH.


.. py:data:: PLFM_NET

   Microsoft Visual Studio.Net.


.. py:data:: PLFM_AVR

   Atmel 8-bit RISC processor(s)


.. py:data:: PLFM_H8

   Hitachi H8/300, H8/2000.


.. py:data:: PLFM_PIC

   Microchip's PIC.


.. py:data:: PLFM_SPARC

   SPARC.


.. py:data:: PLFM_ALPHA

   DEC Alpha.


.. py:data:: PLFM_HPPA

   Hewlett-Packard PA-RISC.


.. py:data:: PLFM_H8500

   Hitachi H8/500.


.. py:data:: PLFM_TRICORE

   Tasking Tricore.


.. py:data:: PLFM_DSP56K

   Motorola DSP5600x.


.. py:data:: PLFM_C166

   Siemens C166 family.


.. py:data:: PLFM_ST20

   SGS-Thomson ST20.


.. py:data:: PLFM_IA64

   Intel Itanium IA64.


.. py:data:: PLFM_I960

   Intel 960.


.. py:data:: PLFM_F2MC

   Fujistu F2MC-16.


.. py:data:: PLFM_TMS320C54

   Texas Instruments TMS320C54xx.


.. py:data:: PLFM_TMS320C55

   Texas Instruments TMS320C55xx.


.. py:data:: PLFM_TRIMEDIA

   Trimedia.


.. py:data:: PLFM_M32R

   Mitsubishi 32bit RISC.


.. py:data:: PLFM_NEC_78K0

   NEC 78K0.


.. py:data:: PLFM_NEC_78K0S

   NEC 78K0S.


.. py:data:: PLFM_M740

   Mitsubishi 8bit.


.. py:data:: PLFM_M7700

   Mitsubishi 16bit.


.. py:data:: PLFM_ST9

   ST9+.


.. py:data:: PLFM_FR

   Fujitsu FR Family.


.. py:data:: PLFM_MC6816

   Motorola 68HC16.


.. py:data:: PLFM_M7900

   Mitsubishi 7900.


.. py:data:: PLFM_TMS320C3

   Texas Instruments TMS320C3.


.. py:data:: PLFM_KR1878

   Angstrem KR1878.


.. py:data:: PLFM_AD218X

   Analog Devices ADSP 218X.


.. py:data:: PLFM_OAKDSP

   Atmel OAK DSP.


.. py:data:: PLFM_TLCS900

   Toshiba TLCS-900.


.. py:data:: PLFM_C39

   Rockwell C39.


.. py:data:: PLFM_CR16

   NSC CR16.


.. py:data:: PLFM_MN102L00

   Panasonic MN10200.


.. py:data:: PLFM_TMS320C1X

   Texas Instruments TMS320C1x.


.. py:data:: PLFM_NEC_V850X

   NEC V850 and V850ES/E1/E2.


.. py:data:: PLFM_SCR_ADPT

   Processor module adapter for processor modules written in scripting languages.


.. py:data:: PLFM_EBC

   EFI Bytecode.


.. py:data:: PLFM_MSP430

   Texas Instruments MSP430.


.. py:data:: PLFM_SPU

   Cell Broadband Engine Synergistic Processor Unit.


.. py:data:: PLFM_DALVIK

   Android Dalvik Virtual Machine.


.. py:data:: PLFM_65C816

   65802/65816


.. py:data:: PLFM_M16C

   Renesas M16C.


.. py:data:: PLFM_ARC

   Argonaut RISC Core.


.. py:data:: PLFM_UNSP

   SunPlus unSP.


.. py:data:: PLFM_TMS320C28

   Texas Instruments TMS320C28x.


.. py:data:: PLFM_DSP96K

   Motorola DSP96000.


.. py:data:: PLFM_SPC700

   Sony SPC700.


.. py:data:: PLFM_AD2106X

   Analog Devices ADSP 2106X.


.. py:data:: PLFM_PIC16

   Microchip's 16-bit PIC.


.. py:data:: PLFM_S390

   IBM's S390.


.. py:data:: PLFM_XTENSA

   Tensilica Xtensa.


.. py:data:: PLFM_RISCV

   RISC-V.


.. py:data:: PLFM_RL78

   Renesas RL78.


.. py:data:: PLFM_RX

   Renesas RX.


.. py:data:: PLFM_WASM

   WASM.


.. py:data:: PR_SEGS

   has segment registers?


.. py:data:: PR_USE32

   supports 32-bit addressing?


.. py:data:: PR_DEFSEG32

   segments are 32-bit by default


.. py:data:: PR_RNAMESOK

   allow user register names for location names


.. py:data:: PR_ADJSEGS

   IDA may adjust segments' starting/ending addresses.


.. py:data:: PR_DEFNUM

   mask - default number representation


.. py:data:: PRN_HEX

   hex


.. py:data:: PRN_OCT

   octal


.. py:data:: PRN_DEC

   decimal


.. py:data:: PRN_BIN

   binary


.. py:data:: PR_WORD_INS

   instruction codes are grouped 2bytes in binary line prefix


.. py:data:: PR_NOCHANGE

   The user can't change segments and code/data attributes (display only) 
           


.. py:data:: PR_ASSEMBLE

   Module has a built-in assembler and will react to ev_assemble.


.. py:data:: PR_ALIGN

   All data items should be aligned properly.


.. py:data:: PR_TYPEINFO

   the processor module fully supports type information callbacks; without full support, function argument locations and other things will probably be wrong. 
           


.. py:data:: PR_USE64

   supports 64-bit addressing?


.. py:data:: PR_SGROTHER

   the segment registers don't contain the segment selectors.


.. py:data:: PR_STACK_UP

   the stack grows up


.. py:data:: PR_BINMEM

   the processor module provides correct segmentation for binary files (i.e. it creates additional segments). The kernel will not ask the user to specify the RAM/ROM sizes 
           


.. py:data:: PR_SEGTRANS

   the processor module supports the segment translation feature (meaning it calculates the code addresses using the map_code_ea() function) 
           


.. py:data:: PR_CHK_XREF

   don't allow near xrefs between segments with different bases


.. py:data:: PR_NO_SEGMOVE

   the processor module doesn't support move_segm() (i.e. the user can't move segments) 
           


.. py:data:: PR_USE_ARG_TYPES

   use processor_t::use_arg_types callback


.. py:data:: PR_SCALE_STKVARS

   use processor_t::get_stkvar_scale callback


.. py:data:: PR_DELAYED

   has delayed jumps and calls. If this flag is set, processor_t::is_basic_block_end, processor_t::delay_slot_insn should be implemented 
           


.. py:data:: PR_ALIGN_INSN

   allow ida to create alignment instructions arbitrarily. Since these instructions might lead to other wrong instructions and spoil the listing, IDA does not create them by default anymore 
           


.. py:data:: PR_PURGING

   there are calling conventions which may purge bytes from the stack


.. py:data:: PR_CNDINSNS

   has conditional instructions


.. py:data:: PR_USE_TBYTE

   BTMT_SPECFLT means _TBYTE type


.. py:data:: PR_DEFSEG64

   segments are 64-bit by default


.. py:data:: PR_OUTER

   has outer operands (currently only mc68k)


.. py:data:: PR2_MAPPINGS

   the processor module uses memory mapping


.. py:data:: PR2_IDP_OPTS

   the module has processor-specific configuration options


.. py:data:: PR2_CODE16_BIT

   low bit of code addresses has special meaning e.g. ARM Thumb, MIPS16 
           


.. py:data:: PR2_MACRO

   processor supports macro instructions


.. py:data:: PR2_USE_CALCREL

   (Lumina) the module supports calcrel info


.. py:data:: PR2_REL_BITS

   (Lumina) calcrel info has bits granularity, not bytes - construction flag only


.. py:data:: PR2_FORCE_16BIT

   use 16-bit basic types despite of 32-bit segments (used by c166)


.. py:data:: OP_FP_BASED

   operand is FP based


.. py:data:: OP_SP_BASED

   operand is SP based


.. py:data:: OP_SP_ADD

   operand value is added to the pointer


.. py:data:: OP_SP_SUB

   operand value is subtracted from the pointer


.. py:data:: CUSTOM_INSN_ITYPE

   Custom instruction codes defined by processor extension plugins must be greater than or equal to this 
           


.. py:data:: REG_SPOIL

   processor_t::use_regarg_type uses this bit in the return value to indicate that the register value has been spoiled 
           


.. py:function:: get_ph() -> processor_t *

.. py:function:: get_ash() -> asm_t *

.. py:function:: str2reg(p: str) -> int

   Get any register number (-1 on error)


.. py:function:: is_align_insn(ea: ida_idaapi.ea_t) -> int

   If the instruction at 'ea' looks like an alignment instruction, return its length in bytes. Otherwise return 0. 
           


.. py:function:: get_reg_name(reg: int, width: size_t, reghi: int = -1) -> str

   Get text representation of a register. For most processors this function will just return processor_t::reg_names[reg]. If the processor module has implemented processor_t::get_reg_name, it will be used instead 
           
   :param reg: internal register number as defined in the processor module
   :param width: register width in bytes
   :param reghi: if specified, then this function will return the register pair
   :returns: length of register name in bytes or -1 if failure


.. py:class:: reg_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: reg
      :type:  int

      register number



   .. py:attribute:: size
      :type:  int

      register size



   .. py:method:: compare(r: reg_info_t) -> int


.. py:function:: parse_reg_name(ri: reg_info_t, regname: str) -> bool

   Get register info by name. 
           
   :param ri: result
   :param regname: name of register
   :returns: success


.. py:data:: NO_ACCESS

.. py:data:: WRITE_ACCESS

.. py:data:: READ_ACCESS

.. py:data:: RW_ACCESS

.. py:class:: reg_access_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: regnum
      :type:  int

      register number (only entire registers)



   .. py:attribute:: range
      :type:  bitrange_t

      bitrange inside the register



   .. py:attribute:: access_type
      :type:  access_type_t


   .. py:attribute:: opnum
      :type:  uchar

      operand number



   .. py:method:: have_common_bits(r: reg_access_t) -> bool


.. py:class:: reg_accesses_t

   Bases: :py:obj:`reg_access_vec_t`


   .. py:attribute:: thisown


.. py:data:: SETPROC_IDB

   set processor type for old idb


.. py:data:: SETPROC_LOADER

   set processor type for new idb; if the user has specified a compatible processor, return success without changing it. if failure, call loader_failure() 
             


.. py:data:: SETPROC_LOADER_NON_FATAL

   the same as SETPROC_LOADER but non-fatal failures.


.. py:data:: SETPROC_USER

   set user-specified processor used for -p and manual processor change at later time 
             


.. py:function:: set_processor_type(procname: str, level: setproc_level_t) -> bool

   Set target processor type. Once a processor module is loaded, it cannot be replaced until we close the idb. 
           
   :param procname: name of processor type (one of names present in processor_t::psnames)
   :param level: SETPROC_
   :returns: success


.. py:function:: get_idp_name() -> str

   Get name of the current processor module. The name is derived from the file name. For example, for IBM PC the module is named "pc.w32" (windows version), then the module name is "PC" (uppercase). If no processor module is loaded, this function will return nullptr 
           


.. py:function:: set_target_assembler(asmnum: int) -> bool

   Set target assembler. 
           
   :param asmnum: number of assembler in the current processor module
   :returns: success


.. py:data:: LTC_NONE

   no event (internal use)


.. py:data:: LTC_ADDED

   added a local type


.. py:data:: LTC_DELETED

   deleted a local type


.. py:data:: LTC_EDITED

   edited a local type


.. py:data:: LTC_ALIASED

   added a type alias


.. py:data:: LTC_COMPILER

   changed the compiler and calling convention


.. py:data:: LTC_TIL_LOADED

   loaded a til file


.. py:data:: LTC_TIL_UNLOADED

   unloaded a til file


.. py:data:: LTC_TIL_COMPACTED

   numbered types have been compacted compact_numbered_types()


.. py:data:: closebase

.. py:data:: savebase

.. py:data:: upgraded

.. py:data:: auto_empty

.. py:data:: auto_empty_finally

.. py:data:: determined_main

.. py:data:: extlang_changed

.. py:data:: idasgn_loaded

.. py:data:: kernel_config_loaded

.. py:data:: loader_finished

.. py:data:: flow_chart_created

.. py:data:: compiler_changed

.. py:data:: changing_ti

.. py:data:: ti_changed

.. py:data:: changing_op_ti

.. py:data:: op_ti_changed

.. py:data:: changing_op_type

.. py:data:: op_type_changed

.. py:data:: segm_added

.. py:data:: deleting_segm

.. py:data:: segm_deleted

.. py:data:: changing_segm_start

.. py:data:: segm_start_changed

.. py:data:: changing_segm_end

.. py:data:: segm_end_changed

.. py:data:: changing_segm_name

.. py:data:: segm_name_changed

.. py:data:: changing_segm_class

.. py:data:: segm_class_changed

.. py:data:: segm_attrs_updated

.. py:data:: segm_moved

.. py:data:: allsegs_moved

.. py:data:: func_added

.. py:data:: func_updated

.. py:data:: set_func_start

.. py:data:: set_func_end

.. py:data:: deleting_func

.. py:data:: frame_deleted

.. py:data:: thunk_func_created

.. py:data:: func_tail_appended

.. py:data:: deleting_func_tail

.. py:data:: func_tail_deleted

.. py:data:: tail_owner_changed

.. py:data:: func_noret_changed

.. py:data:: stkpnts_changed

.. py:data:: updating_tryblks

.. py:data:: tryblks_updated

.. py:data:: deleting_tryblks

.. py:data:: sgr_changed

.. py:data:: make_code

.. py:data:: make_data

.. py:data:: destroyed_items

.. py:data:: renamed

.. py:data:: byte_patched

.. py:data:: changing_cmt

.. py:data:: cmt_changed

.. py:data:: changing_range_cmt

.. py:data:: range_cmt_changed

.. py:data:: extra_cmt_changed

.. py:data:: item_color_changed

.. py:data:: callee_addr_changed

.. py:data:: bookmark_changed

.. py:data:: sgr_deleted

.. py:data:: adding_segm

.. py:data:: func_deleted

.. py:data:: dirtree_mkdir

.. py:data:: dirtree_rmdir

.. py:data:: dirtree_link

.. py:data:: dirtree_move

.. py:data:: dirtree_rank

.. py:data:: dirtree_rminode

.. py:data:: dirtree_segm_moved

.. py:data:: local_types_changed

.. py:data:: lt_udm_created

.. py:data:: lt_udm_deleted

.. py:data:: lt_udm_renamed

.. py:data:: lt_udm_changed

.. py:data:: lt_udt_expanded

.. py:data:: frame_created

.. py:data:: frame_udm_created

.. py:data:: frame_udm_deleted

.. py:data:: frame_udm_renamed

.. py:data:: frame_udm_changed

.. py:data:: frame_expanded

.. py:data:: idasgn_matched_ea

.. py:data:: lt_edm_created

.. py:data:: lt_edm_deleted

.. py:data:: lt_edm_renamed

.. py:data:: lt_edm_changed

.. py:data:: local_type_renamed

.. py:function:: gen_idb_event(*args) -> None

   the kernel will use this function to generate idb_events


.. py:data:: IDPOPT_CST

.. py:data:: IDPOPT_JVL

.. py:data:: IDPOPT_PRI_DEFAULT

.. py:data:: IDPOPT_PRI_HIGH

.. py:data:: IDPOPT_NUM_INT

.. py:data:: IDPOPT_NUM_CHAR

.. py:data:: IDPOPT_NUM_SHORT

.. py:data:: IDPOPT_NUM_RANGE

.. py:data:: IDPOPT_NUM_UNS

.. py:data:: IDPOPT_BIT_UINT

.. py:data:: IDPOPT_BIT_UCHAR

.. py:data:: IDPOPT_BIT_USHORT

.. py:data:: IDPOPT_BIT_BOOL

.. py:data:: IDPOPT_STR_QSTRING

.. py:data:: IDPOPT_STR_LONG

.. py:data:: IDPOPT_I64_RANGE

.. py:data:: IDPOPT_I64_UNS

.. py:data:: IDPOPT_CST_PARAMS

.. py:data:: IDPOPT_MBROFF

.. py:class:: num_range_t(_min: int64, _max: int64)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: minval
      :type:  int64


   .. py:attribute:: maxval
      :type:  int64


.. py:class:: params_t(_p1: int64, _p2: int64)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: p1
      :type:  int64


   .. py:attribute:: p2
      :type:  int64


.. py:data:: cik_string

.. py:data:: cik_filename

.. py:data:: cik_path

.. py:function:: register_cfgopts(opts: cfgopt_t const [], nopts: size_t, cb: config_changed_cb_t * = None, obj: void * = None) -> bool

.. py:function:: get_config_value(key: str) -> jvalue_t *

.. py:function:: cfg_get_cc_parm(compid: comp_t, name: str) -> str

.. py:function:: cfg_get_cc_header_path(compid: comp_t) -> str

.. py:function:: cfg_get_cc_predefined_macros(compid: comp_t) -> str

.. py:function:: process_config_directive(directive: str, priority: int = 2) -> None

.. py:function:: AssembleLine(ea, cs, ip, use32, line)

   Assemble an instruction to a string (display a warning if an error is found)

   :param ea: linear address of instruction
   :param cs:  cs of instruction
   :param ip:  ip of instruction
   :param use32: is 32bit segment
   :param line: line to assemble
   :returns: a string containing the assembled instruction, or None on failure


.. py:function:: assemble(ea, cs, ip, use32, line)

   Assemble an instruction into the database (display a warning if an error is found)

   :param ea: linear address of instruction
   :param cs: cs of instruction
   :param ip: ip of instruction
   :param use32: is 32bit segment?
   :param line: line to assemble

   :returns: Boolean. True on success.


.. py:function:: ph_get_id()

   Returns the 'ph.id' field


.. py:function:: ph_get_version()

   Returns the 'ph.version'


.. py:function:: ph_get_flag()

   Returns the 'ph.flag'


.. py:function:: ph_get_cnbits()

   Returns the 'ph.cnbits'


.. py:function:: ph_get_dnbits()

   Returns the 'ph.dnbits'


.. py:function:: ph_get_reg_first_sreg()

   Returns the 'ph.reg_first_sreg'


.. py:function:: ph_get_reg_last_sreg()

   Returns the 'ph.reg_last_sreg'


.. py:function:: ph_get_segreg_size()

   Returns the 'ph.segreg_size'


.. py:function:: ph_get_reg_code_sreg()

   Returns the 'ph.reg_code_sreg'


.. py:function:: ph_get_reg_data_sreg()

   Returns the 'ph.reg_data_sreg'


.. py:function:: ph_get_icode_return()

   Returns the 'ph.icode_return'


.. py:function:: ph_get_instruc_start()

   Returns the 'ph.instruc_start'


.. py:function:: ph_get_instruc_end()

   Returns the 'ph.instruc_end'


.. py:function:: ph_get_tbyte_size()

   Returns the 'ph.tbyte_size' field as defined in he processor module


.. py:function:: ph_get_instruc()

   Returns a list of tuples (instruction_name, instruction_feature) containing the
   instructions list as defined in he processor module


.. py:function:: ph_get_regnames()

   Returns the list of register names as defined in the processor module


.. py:function:: ph_get_operand_info(ea: ida_idaapi.ea_t, n: int) -> Union[Tuple[int, ida_idaapi.ea_t, int, int, int], None]

   Returns the operand information given an ea and operand number.

   :param ea: address
   :param n: operand number

   :returns: Returns an idd_opinfo_t as a tuple: (modified, ea, reg_ival, regidx, value_size).
             Please refer to idd_opinfo_t structure in the SDK.


.. py:function:: ph_calcrel(ea: ida_idaapi.ea_t) -> bytevec_t *, size_t *

.. py:function:: ph_find_reg_value(insn: insn_t const &, reg: int) -> uint64 *

.. py:function:: ph_find_op_value(insn: insn_t const &, op: int) -> uint64 *

.. py:function:: ph_get_reg_accesses(accvec: reg_accesses_t, insn: insn_t const &, flags: int) -> ssize_t

.. py:function:: ph_get_abi_info(comp: comp_t) -> qstrvec_t *, qstrvec_t *

.. py:class:: IDP_Hooks(_flags: int = 0, _hkcb_flags: int = 1)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: hook() -> bool


   .. py:method:: unhook() -> bool


   .. py:method:: ev_init(idp_modname: str) -> int

      The IDP module is just loaded. 
                
      :param idp_modname: (const char *) processor module name
      :returns: <0: on failure



   .. py:method:: ev_term() -> int

      The IDP module is being unloaded.



   .. py:method:: ev_newprc(pnum: int, keep_cfg: bool) -> int

      Before changing processor type. 
                
      :param pnum: (int) processor number in the array of processor names
      :param keep_cfg: (bool) true: do not modify kernel configuration
      :returns: 1: ok
      :returns: <0: prohibit



   .. py:method:: ev_newasm(asmnum: int) -> int

      Before setting a new assembler. 
                
      :param asmnum: (int) See also ev_asm_installed



   .. py:method:: ev_newfile(fname: char *) -> int

      A new file has been loaded. 
                
      :param fname: (char *) input file name



   .. py:method:: ev_oldfile(fname: char *) -> int

      An old file has been loaded. 
                
      :param fname: (char *) input file name



   .. py:method:: ev_newbinary(filename: char *, fileoff: qoff64_t, basepara: ida_idaapi.ea_t, binoff: ida_idaapi.ea_t, nbytes: uint64) -> int

      IDA is about to load a binary file. 
                
      :param filename: (char *) binary file name
      :param fileoff: (qoff64_t) offset in the file
      :param basepara: (::ea_t) base loading paragraph
      :param binoff: (::ea_t) loader offset
      :param nbytes: (::uint64) number of bytes to load



   .. py:method:: ev_endbinary(ok: bool) -> int

      IDA has loaded a binary file. 
                
      :param ok: (bool) file loaded successfully?



   .. py:method:: ev_set_idp_options(keyword: str, value_type: int, value: void const *, idb_loaded: bool) -> int

      Set IDP-specific configuration option Also see set_options_t in config.hpp 
                
      :param keyword: (const char *)
      :param value_type: (int)
      :param value: (const void *)
      :param idb_loaded: (bool) true if the ev_oldfile/ev_newfile events have been generated
      :returns: 1: ok
      :returns: 0: not implemented
      :returns: -1: error (and message in errbuf)



   .. py:method:: ev_set_proc_options(options: str, confidence: int) -> int

      Called if the user specified an option string in the command line: -p<processor name>:<options>. Can be used for setting a processor subtype. Also called if option string is passed to set_processor_type() and IDC's SetProcessorType(). 
                
      :param options: (const char *)
      :param confidence: (int) 0: loader's suggestion 1: user's decision
      :returns: <0: if bad option string



   .. py:method:: ev_ana_insn(out: insn_t *) -> bool

      Analyze one instruction and fill 'out' structure. This function shouldn't change the database, flags or anything else. All these actions should be performed only by emu_insn() function. insn_t::ea contains address of instruction to analyze. 
                
      :param out: (insn_t *)
      :returns: length of the instruction in bytes, 0 if instruction can't be decoded.
      :returns: 0: if instruction can't be decoded.



   .. py:method:: ev_emu_insn(insn: insn_t const *) -> bool

      Emulate instruction, create cross-references, plan to analyze subsequent instructions, modify flags etc. Upon entrance to this function, all information about the instruction is in 'insn' structure. 
                
      :param insn: (const insn_t *)
      :returns: 1: ok
      :returns: -1: the kernel will delete the instruction



   .. py:method:: ev_out_header(outctx: outctx_t *) -> int

      Function to produce start of disassembled text 
                
      :param outctx: (outctx_t *)
      :returns: void: 



   .. py:method:: ev_out_footer(outctx: outctx_t *) -> int

      Function to produce end of disassembled text 
                
      :param outctx: (outctx_t *)
      :returns: void: 



   .. py:method:: ev_out_segstart(outctx: outctx_t *, seg: segment_t *) -> int

      Function to produce start of segment 
                
      :param outctx: (outctx_t *)
      :param seg: (segment_t *)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_out_segend(outctx: outctx_t *, seg: segment_t *) -> int

      Function to produce end of segment 
                
      :param outctx: (outctx_t *)
      :param seg: (segment_t *)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_out_assumes(outctx: outctx_t *) -> int

      Function to produce assume directives when segment register value changes. 
                
      :param outctx: (outctx_t *)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_out_insn(outctx: outctx_t *) -> bool

      Generate text representation of an instruction in 'ctx.insn' outctx_t provides functions to output the generated text. This function shouldn't change the database, flags or anything else. All these actions should be performed only by emu_insn() function. 
                
      :param outctx: (outctx_t *)
      :returns: void: 



   .. py:method:: ev_out_mnem(outctx: outctx_t *) -> int

      Generate instruction mnemonics. This callback should append the colored mnemonics to ctx.outbuf Optional notification, if absent, out_mnem will be called. 
                
      :param outctx: (outctx_t *)
      :returns: 1: if appended the mnemonics
      :returns: 0: not implemented



   .. py:method:: ev_out_operand(outctx: outctx_t *, op: op_t const *) -> bool

      Generate text representation of an instruction operand outctx_t provides functions to output the generated text. All these actions should be performed only by emu_insn() function. 
                
      :param outctx: (outctx_t *)
      :param op: (const op_t *)
      :returns: 1: ok
      :returns: -1: operand is hidden



   .. py:method:: ev_out_data(outctx: outctx_t *, analyze_only: bool) -> int

      Generate text representation of data items This function may change the database and create cross-references if analyze_only is set 
                
      :param outctx: (outctx_t *)
      :param analyze_only: (bool)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_out_label(outctx: outctx_t *, colored_name: str) -> int

      The kernel is going to generate an instruction label line or a function header. 
                
      :param outctx: (outctx_t *)
      :param colored_name: (const char *)
      :returns: <0: if the kernel should not generate the label
      :returns: 0: not implemented or continue



   .. py:method:: ev_out_special_item(outctx: outctx_t *, segtype: uchar) -> int

      Generate text representation of an item in a special segment i.e. absolute symbols, externs, communal definitions etc 
                
      :param outctx: (outctx_t *)
      :param segtype: (uchar)
      :returns: 1: ok
      :returns: 0: not implemented
      :returns: -1: overflow



   .. py:method:: ev_gen_regvar_def(outctx: outctx_t *, v: regvar_t *) -> int

      Generate register variable definition line. 
                
      :param outctx: (outctx_t *)
      :param v: (regvar_t *)
      :returns: >0: ok, generated the definition text
      :returns: 0: not implemented



   .. py:method:: ev_gen_src_file_lnnum(outctx: outctx_t *, file: str, lnnum: size_t) -> int

      Callback: generate analog of: 
           #line  123
          


                
      :param outctx: (outctx_t *) output context
      :param file: (const char *) source file (may be nullptr)
      :param lnnum: (size_t) line number
      :returns: 1: directive has been generated
      :returns: 0: not implemented



   .. py:method:: ev_creating_segm(seg: segment_t *) -> int

      A new segment is about to be created. 
                
      :param seg: (segment_t *)
      :returns: 1: ok
      :returns: <0: segment should not be created



   .. py:method:: ev_moving_segm(seg: segment_t *, to: ida_idaapi.ea_t, flags: int) -> int

      May the kernel move the segment? 
                
      :param seg: (segment_t *) segment to move
      :param to: (::ea_t) new segment start address
      :param flags: (int) combination of Move segment flags
      :returns: 0: yes
      :returns: <0: the kernel should stop



   .. py:method:: ev_coagulate(start_ea: ida_idaapi.ea_t) -> int

      Try to define some unexplored bytes. This notification will be called if the kernel tried all possibilities and could not find anything more useful than to convert to array of bytes. The module can help the kernel and convert the bytes into something more useful. 
                
      :param start_ea: (::ea_t)
      :returns: number of converted bytes



   .. py:method:: ev_undefine(ea: ida_idaapi.ea_t) -> int

      An item in the database (insn or data) is being deleted. 
                
      :param ea: (ea_t)
      :returns: 1: do not delete srranges at the item end
      :returns: 0: srranges can be deleted



   .. py:method:: ev_treat_hindering_item(hindering_item_ea: ida_idaapi.ea_t, new_item_flags: flags64_t, new_item_ea: ida_idaapi.ea_t, new_item_length: asize_t) -> int

      An item hinders creation of another item. 
                
      :param hindering_item_ea: (::ea_t)
      :param new_item_flags: (flags64_t) (0 for code)
      :param new_item_ea: (::ea_t)
      :param new_item_length: (::asize_t)
      :returns: 0: no reaction
      :returns: !=0: the kernel may delete the hindering item



   .. py:method:: ev_rename(ea: ida_idaapi.ea_t, new_name: str) -> int

      The kernel is going to rename a byte. 
                
      :param ea: (::ea_t)
      :param new_name: (const char *)
      :returns: <0: if the kernel should not rename it.
      :returns: 2: to inhibit the notification. I.e., the kernel should not rename, but 'set_name()' should return 'true'. also see renamed the return value is ignored when kernel is going to delete name



   .. py:method:: ev_is_far_jump(icode: int) -> int

      is indirect far jump or call instruction? meaningful only if the processor has 'near' and 'far' reference types 
                
      :param icode: (int)
      :returns: 0: not implemented
      :returns: 1: yes
      :returns: -1: no



   .. py:method:: ev_is_sane_insn(insn: insn_t const *, no_crefs: int) -> int

      Is the instruction sane for the current file type?. 
                
      :param insn: (const insn_t*) the instruction
      :param no_crefs: (int) 1: the instruction has no code refs to it. ida just tries to convert unexplored bytes to an instruction (but there is no other reason to convert them into an instruction) 0: the instruction is created because of some coderef, user request or another weighty reason.
      :returns: >=0: ok
      :returns: <0: no, the instruction isn't likely to appear in the program



   .. py:method:: ev_is_cond_insn(insn: insn_t const *) -> int

      Is conditional instruction? 
                
      :param insn: (const insn_t *) instruction address
      :returns: 1: yes
      :returns: -1: no
      :returns: 0: not implemented or not instruction



   .. py:method:: ev_is_call_insn(insn: insn_t const *) -> int

      Is the instruction a "call"? 
                
      :param insn: (const insn_t *) instruction
      :returns: 0: unknown
      :returns: <0: no
      :returns: 1: yes



   .. py:method:: ev_is_ret_insn(insn: insn_t const *, flags: uchar) -> int

      Is the instruction a "return"? 
                
      :param insn: (const insn_t *) instruction
      :param flags: (uchar), combination of IRI_... flags (see above)
      :returns: 0: unknown
      :returns: <0: no
      :returns: 1: yes



   .. py:method:: ev_may_be_func(insn: insn_t const *, state: int) -> int

      Can a function start here? 
                
      :param insn: (const insn_t*) the instruction
      :param state: (int) autoanalysis phase 0: creating functions 1: creating chunks
      :returns: probability 1..100



   .. py:method:: ev_is_basic_block_end(insn: insn_t const *, call_insn_stops_block: bool) -> int

      Is the current instruction end of a basic block?. This function should be defined for processors with delayed jump slots. 
                
      :param insn: (const insn_t*) the instruction
      :param call_insn_stops_block: (bool)
      :returns: 0: unknown
      :returns: <0: no
      :returns: 1: yes



   .. py:method:: ev_is_indirect_jump(insn: insn_t const *) -> int

      Determine if instruction is an indirect jump. If CF_JUMP bit cannot describe all jump types jumps, please define this callback. 
                
      :param insn: (const insn_t*) the instruction
      :returns: 0: use CF_JUMP
      :returns: 1: no
      :returns: 2: yes



   .. py:method:: ev_is_insn_table_jump() -> int

      Reserved.



   .. py:method:: ev_is_switch(si: switch_info_t, insn: insn_t const *) -> int

      Find 'switch' idiom or override processor module's decision. It will be called for instructions marked with CF_JUMP. 
                
      :param si: (switch_info_t *), out
      :param insn: (const insn_t *) instruction possibly belonging to a switch
      :returns: 1: switch is found, 'si' is filled. IDA will create the switch using the filled 'si'
      :returns: -1: no switch found. This value forbids switch creation by the processor module
      :returns: 0: not implemented



   .. py:method:: ev_calc_switch_cases(casevec: casevec_t *, targets: eavec_t *, insn_ea: ida_idaapi.ea_t, si: switch_info_t) -> int

      Calculate case values and targets for a custom jump table. 
                
      :param casevec: (::casevec_t *) vector of case values (may be nullptr)
      :param targets: (eavec_t *) corresponding target addresses (my be nullptr)
      :param insn_ea: (::ea_t) address of the 'indirect jump' instruction
      :param si: (switch_info_t *) switch information
      :returns: 1: ok
      :returns: <=0: failed



   .. py:method:: ev_create_switch_xrefs(jumpea: ida_idaapi.ea_t, si: switch_info_t) -> int

      Create xrefs for a custom jump table. 
                
      :param jumpea: (::ea_t) address of the jump insn
      :param si: (const switch_info_t *) switch information
      :returns: must return 1 Must be implemented if module uses custom jump tables, SWI_CUSTOM



   .. py:method:: ev_is_align_insn(ea: ida_idaapi.ea_t) -> int

      Is the instruction created only for alignment purposes?. Do not directly call this function, use is_align_insn() 
                
      :param ea: (ea_t) - instruction address
      :returns: number: of bytes in the instruction



   .. py:method:: ev_is_alloca_probe(ea: ida_idaapi.ea_t) -> int

      Does the function at 'ea' behave as __alloca_probe? 
                
      :param ea: (::ea_t)
      :returns: 1: yes
      :returns: 0: no



   .. py:method:: ev_delay_slot_insn(ea: ida_idaapi.ea_t, bexec: bool, fexec: bool) -> PyObject *

      Get delay slot instruction 
                
      :param ea: (::ea_t *) in: instruction address in question, out: (if the answer is positive) if the delay slot contains valid insn: the address of the delay slot insn else: BADADDR (invalid insn, e.g. a branch)
      :param bexec: (bool *) execute slot if jumping, initially set to 'true'
      :param fexec: (bool *) execute slot if not jumping, initally set to 'true'
      :returns: 1: positive answer
      :returns: <=0: ordinary insn



   .. py:method:: ev_is_sp_based(mode: int *, insn: insn_t const *, op: op_t const *) -> int

      Check whether the operand is relative to stack pointer or frame pointer This event is used to determine how to output a stack variable If not implemented, then all operands are sp based by default. Implement this event only if some stack references use frame pointer instead of stack pointer. 
                
      :param mode: (int *) out, combination of SP/FP operand flags
      :param insn: (const insn_t *)
      :param op: (const op_t *)
      :returns: 0: not implemented
      :returns: 1: ok



   .. py:method:: ev_can_have_type(op: op_t const *) -> int

      Can the operand have a type as offset, segment, decimal, etc? (for example, a register AX can't have a type, meaning that the user can't change its representation. see bytes.hpp for information about types and flags) 
                
      :param op: (const op_t *)
      :returns: 0: unknown
      :returns: <0: no
      :returns: 1: yes



   .. py:method:: ev_cmp_operands(op1: op_t const *, op2: op_t const *) -> int

      Compare instruction operands 
                
      :param op1: (const op_t*)
      :param op2: (const op_t*)
      :returns: 1: equal
      :returns: -1: not equal
      :returns: 0: not implemented



   .. py:method:: ev_adjust_refinfo(ri: refinfo_t, ea: ida_idaapi.ea_t, n: int, fd: fixup_data_t const *) -> int

      Called from apply_fixup before converting operand to reference. Can be used for changing the reference info. (e.g. the PPC module adds REFINFO_NOBASE for some references) 
                
      :param ri: (refinfo_t *)
      :param ea: (::ea_t) instruction address
      :param n: (int) operand number
      :param fd: (const fixup_data_t *)
      :returns: <0: do not create an offset
      :returns: 0: not implemented or refinfo adjusted



   .. py:method:: ev_get_operand_string(insn: insn_t const *, opnum: int) -> PyObject *

      Request text string for operand (cli, java, ...). 
                
      :param insn: (const insn_t*) the instruction
      :param opnum: (int) operand number, -1 means any string operand
      :returns: 0: no string (or empty string)
      :returns: >0: original string length without terminating zero



   .. py:method:: ev_get_reg_name(reg: int, width: size_t, reghi: int) -> PyObject *

      Generate text representation of a register. Most processor modules do not need to implement this callback. It is useful only if processor_t::reg_names[reg] does not provide the correct register name. 
                
      :param reg: (int) internal register number as defined in the processor module
      :param width: (size_t) register width in bytes
      :param reghi: (int) if not -1 then this function will return the register pair
      :returns: -1: if error
      :returns: strlen(buf): if success



   .. py:method:: ev_str2reg(regname: str) -> int

      Convert a register name to a register number. The register number is the register index in the processor_t::reg_names array Most processor modules do not need to implement this callback It is useful only if processor_t::reg_names[reg] does not provide the correct register names 
                
      :param regname: (const char *)
      :returns: register: number + 1
      :returns: 0: not implemented or could not be decoded



   .. py:method:: ev_get_autocmt(insn: insn_t const *) -> PyObject *

      Callback: get dynamic auto comment. Will be called if the autocomments are enabled and the comment retrieved from ida.int starts with '$!'. 'insn' contains valid info. 
                
      :param insn: (const insn_t*) the instruction
      :returns: 1: new comment has been generated
      :returns: 0: callback has not been handled. the buffer must not be changed in this case



   .. py:method:: ev_get_bg_color(color: bgcolor_t *, ea: ida_idaapi.ea_t) -> int

      Get item background color. Plugins can hook this callback to color disassembly lines dynamically 
                
      :param color: (bgcolor_t *), out
      :param ea: (::ea_t)
      :returns: 0: not implemented
      :returns: 1: color set



   .. py:method:: ev_is_jump_func(pfn: func_t *, jump_target: ea_t *, func_pointer: ea_t *) -> int

      Is the function a trivial "jump" function?. 
                
      :param pfn: (func_t *)
      :param jump_target: (::ea_t *)
      :param func_pointer: (::ea_t *)
      :returns: <0: no
      :returns: 0: don't know
      :returns: 1: yes, see 'jump_target' and 'func_pointer'



   .. py:method:: ev_func_bounds(possible_return_code: int *, pfn: func_t *, max_func_end_ea: ida_idaapi.ea_t) -> int

      find_func_bounds() finished its work. The module may fine tune the function bounds 
                
      :param possible_return_code: (int *), in/out
      :param pfn: (func_t *)
      :param max_func_end_ea: (::ea_t) (from the kernel's point of view)
      :returns: void: 



   .. py:method:: ev_verify_sp(pfn: func_t *) -> int

      All function instructions have been analyzed. Now the processor module can analyze the stack pointer for the whole function 
                
      :param pfn: (func_t *)
      :returns: 0: ok
      :returns: <0: bad stack pointer



   .. py:method:: ev_verify_noreturn(pfn: func_t *) -> int

      The kernel wants to set 'noreturn' flags for a function. 
                
      :param pfn: (func_t *)
      :returns: 0: ok. any other value: do not set 'noreturn' flag



   .. py:method:: ev_create_func_frame(pfn: func_t *) -> int

      Create a function frame for a newly created function Set up frame size, its attributes etc 
                
      :param pfn: (func_t *)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_get_frame_retsize(frsize: int *, pfn: func_t const *) -> int

      Get size of function return address in bytes If this event is not implemented, the kernel will assume
      * 8 bytes for 64-bit function
      * 4 bytes for 32-bit function
      * 2 bytes otherwise



      :param frsize: (int *) frame size (out)
      :param pfn: (const func_t *), can't be nullptr
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_get_stkvar_scale_factor() -> int

      Should stack variable references be multiplied by a coefficient before being used in the stack frame?. Currently used by TMS320C55 because the references into the stack should be multiplied by 2 
                
      :returns: scaling factor
      :returns: 0: not implemented



   .. py:method:: ev_demangle_name(name: str, disable_mask: int, demreq: int) -> PyObject *

      Demangle a C++ (or another language) name into a user-readable string. This event is called by demangle_name() 
                
      :param name: (const char *) mangled name
      :param disable_mask: (uint32) flags to inhibit parts of output or compiler info/other (see MNG_)
      :param demreq: (demreq_type_t) operation to perform
      :returns: 1: if success
      :returns: 0: not implemented



   .. py:method:: ev_add_cref(_from: ida_idaapi.ea_t, to: ida_idaapi.ea_t, type: cref_t) -> int

      A code reference is being created. 
                
      :param to: (::ea_t)
      :param type: (cref_t)
      :returns: <0: cancel cref creation
      :returns: 0: not implemented or continue



   .. py:method:: ev_add_dref(_from: ida_idaapi.ea_t, to: ida_idaapi.ea_t, type: dref_t) -> int

      A data reference is being created. 
                
      :param to: (::ea_t)
      :param type: (dref_t)
      :returns: <0: cancel dref creation
      :returns: 0: not implemented or continue



   .. py:method:: ev_del_cref(_from: ida_idaapi.ea_t, to: ida_idaapi.ea_t, expand: bool) -> int

      A code reference is being deleted. 
                
      :param to: (::ea_t)
      :param expand: (bool)
      :returns: <0: cancel cref deletion
      :returns: 0: not implemented or continue



   .. py:method:: ev_del_dref(_from: ida_idaapi.ea_t, to: ida_idaapi.ea_t) -> int

      A data reference is being deleted. 
                
      :param to: (::ea_t)
      :returns: <0: cancel dref deletion
      :returns: 0: not implemented or continue



   .. py:method:: ev_coagulate_dref(_from: ida_idaapi.ea_t, to: ida_idaapi.ea_t, may_define: bool, code_ea: ea_t *) -> int

      Data reference is being analyzed. plugin may correct 'code_ea' (e.g. for thumb mode refs, we clear the last bit) 
                
      :param to: (::ea_t)
      :param may_define: (bool)
      :param code_ea: (::ea_t *)
      :returns: <0: failed dref analysis, >0 done dref analysis
      :returns: 0: not implemented or continue



   .. py:method:: ev_may_show_sreg(current_ea: ida_idaapi.ea_t) -> int

      The kernel wants to display the segment registers in the messages window. 
                
      :param current_ea: (::ea_t)
      :returns: <0: if the kernel should not show the segment registers. (assuming that the module has done it)
      :returns: 0: not implemented



   .. py:method:: ev_auto_queue_empty(type: atype_t) -> int

      One analysis queue is empty. 
                
      :param type: (atype_t)
      :returns: void: see also idb_event::auto_empty_finally



   .. py:method:: ev_validate_flirt_func(start_ea: ida_idaapi.ea_t, funcname: str) -> int

      Flirt has recognized a library function. This callback can be used by a plugin or proc module to intercept it and validate such a function. 
                
      :param start_ea: (::ea_t)
      :param funcname: (const char *)
      :returns: -1: do not create a function,
      :returns: 0: function is validated



   .. py:method:: ev_adjust_libfunc_ea(sig: idasgn_t const *, libfun: libfunc_t const *, ea: ea_t *) -> int

      Called when a signature module has been matched against bytes in the database. This is used to compute the offset at which a particular module's libfunc should be applied. 
                
      :param sig: (const idasgn_t *)
      :param libfun: (const libfunc_t *)
      :param ea: (::ea_t *)
      :returns: 1: the ea_t pointed to by the third argument was modified.
      :returns: <=0: not modified. use default algorithm.



   .. py:method:: ev_assemble(ea: ida_idaapi.ea_t, cs: ida_idaapi.ea_t, ip: ida_idaapi.ea_t, use32: bool, line: str) -> PyObject *

      Assemble an instruction. (display a warning if an error is found). 
                
      :param ea: (::ea_t) linear address of instruction
      :param cs: (::ea_t) cs of instruction
      :param ip: (::ea_t) ip of instruction
      :param use32: (bool) is 32bit segment?
      :param line: (const char *) line to assemble
      :returns: size of the instruction in bytes



   .. py:method:: ev_extract_address(out_ea: ea_t *, screen_ea: ida_idaapi.ea_t, string: str, position: size_t) -> int

      Extract address from a string. 
                
      :param out_ea: (ea_t *), out
      :param screen_ea: (ea_t)
      :param string: (const char *)
      :param position: (size_t)
      :returns: 1: ok
      :returns: 0: kernel should use the standard algorithm
      :returns: -1: error



   .. py:method:: ev_realcvt(m: void *, e: fpvalue_t *, swt: uint16) -> int

      Floating point -> IEEE conversion 
                
      :param m: (void *) ptr to processor-specific floating point value
      :param e: (fpvalue_t *) IDA representation of a floating point value
      :param swt: (uint16) operation (see realcvt() in ieee.h)
      :returns: 0: not implemented



   .. py:method:: ev_gen_asm_or_lst(starting: bool, fp: FILE *, is_asm: bool, flags: int, outline: html_line_cb_t **) -> int

      Callback: generating asm or lst file. The kernel calls this callback twice, at the beginning and at the end of listing generation. The processor module can intercept this event and adjust its output 
                
      :param starting: (bool) beginning listing generation
      :param fp: (FILE *) output file
      :param is_asm: (bool) true:assembler, false:listing
      :param flags: (int) flags passed to gen_file()
      :param outline: (html_line_cb_t **) ptr to ptr to outline callback. if this callback is defined for this code, it will be used by the kernel to output the generated lines
      :returns: void: 



   .. py:method:: ev_gen_map_file(nlines: int *, fp: FILE *) -> int

      Generate map file. If not implemented the kernel itself will create the map file. 
                
      :param nlines: (int *) number of lines in map file (-1 means write error)
      :param fp: (FILE *) output file
      :returns: 0: not implemented
      :returns: 1: ok
      :returns: -1: write error



   .. py:method:: ev_create_flat_group(image_base: ida_idaapi.ea_t, bitness: int, dataseg_sel: sel_t) -> int

      Create special segment representing the flat group. 
                
      :param image_base: (::ea_t)
      :param bitness: (int)
      :param dataseg_sel: (::sel_t) return value is ignored



   .. py:method:: ev_getreg(regval: uval_t *, regnum: int) -> int

      IBM PC only internal request, should never be used for other purpose Get register value by internal index 
                
      :param regval: (uval_t *), out
      :param regnum: (int)
      :returns: 1: ok
      :returns: 0: not implemented
      :returns: -1: failed (undefined value or bad regnum)



   .. py:method:: ev_analyze_prolog(ea: ida_idaapi.ea_t) -> int

      Analyzes function prolog, epilog, and updates purge, and function attributes 
                
      :param ea: (::ea_t) start of function
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_calc_spdelta(spdelta: sval_t *, insn: insn_t const *) -> int

      Calculate amount of change to sp for the given insn. This event is required to decompile code snippets. 
                
      :param spdelta: (sval_t *)
      :param insn: (const insn_t *)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_calcrel() -> int

      Reserved.



   .. py:method:: ev_find_reg_value(pinsn: insn_t const *, reg: int) -> PyObject *

      Find register value via a register tracker. The returned value in 'out' is valid before executing the instruction. 
                
      :param pinsn: (const insn_t *) instruction
      :param reg: (int) register index
      :returns: 1: if implemented, and value was found
      :returns: 0: not implemented, -1 decoding failed, or no value found



   .. py:method:: ev_find_op_value(pinsn: insn_t const *, opn: int) -> PyObject *

      Find operand value via a register tracker. The returned value in 'out' is valid before executing the instruction. 
                
      :param pinsn: (const insn_t *) instruction
      :param opn: (int) operand index
      :returns: 1: if implemented, and value was found
      :returns: 0: not implemented, -1 decoding failed, or no value found



   .. py:method:: ev_replaying_undo(action_name: str, vec: undo_records_t const *, is_undo: bool) -> int

      Replaying an undo/redo buffer 
                
      :param action_name: (const char *) action that we perform undo/redo for. may be nullptr for intermediary buffers.
      :param vec: (const undo_records_t *)
      :param is_undo: (bool) true if performing undo, false if performing redo This event may be generated multiple times per undo/redo



   .. py:method:: ev_ending_undo(action_name: str, is_undo: bool) -> int

      Ended undoing/redoing an action 
                
      :param action_name: (const char *) action that we finished undoing/redoing. is not nullptr.
      :param is_undo: (bool) true if performing undo, false if performing redo



   .. py:method:: ev_set_code16_mode(ea: ida_idaapi.ea_t, code16: bool) -> int

      Some processors have ISA 16-bit mode e.g. ARM Thumb mode, PPC VLE, MIPS16 Set ISA 16-bit mode 
                
      :param ea: (ea_t) address to set new ISA mode
      :param code16: (bool) true for 16-bit mode, false for 32-bit mode



   .. py:method:: ev_get_code16_mode(ea: ida_idaapi.ea_t) -> int

      Get ISA 16-bit mode 
                
      :param ea: (ea_t) address to get the ISA mode
      :returns: 1: 16-bit mode
      :returns: 0: not implemented or 32-bit mode



   .. py:method:: ev_get_procmod() -> int

      Get pointer to the processor module object. All processor modules must implement this. The pointer is returned as size_t. 
                



   .. py:method:: ev_asm_installed(asmnum: int) -> int

      After setting a new assembler 
                
      :param asmnum: (int) See also ev_newasm



   .. py:method:: ev_get_reg_accesses(accvec: reg_accesses_t, insn: insn_t const *, flags: int) -> int

      Get info about the registers that are used/changed by an instruction. 
                
      :param accvec: (reg_accesses_t*) out: info about accessed registers
      :param insn: (const insn_t *) instruction in question
      :param flags: (int) reserved, must be 0
      :returns: -1: if accvec is nullptr
      :returns: 1: found the requested access (and filled accvec)
      :returns: 0: not implemented



   .. py:method:: ev_is_control_flow_guard(p_reg: int *, insn: insn_t const *) -> int

      Detect if an instruction is a "thunk call" to a flow guard function (equivalent to call reg/return/nop) 
                
      :param p_reg: (int *) indirect register number, may be -1
      :param insn: (const insn_t *) call/jump instruction
      :returns: -1: no thunk detected
      :returns: 1: indirect call
      :returns: 2: security check routine call (NOP)
      :returns: 3: return thunk
      :returns: 0: not implemented



   .. py:method:: ev_create_merge_handlers(md: merge_data_t *) -> int

      Create merge handlers, if needed 
                
      :param md: (merge_data_t *) This event is generated immediately after opening idbs.
      :returns: must be 0



   .. py:method:: ev_privrange_changed(old_privrange: range_t, delta: adiff_t) -> int

      Privrange interval has been moved to a new location. Most common actions to be done by module in this case: fix indices of netnodes used by module 
                
      :param old_privrange: (const range_t *) - old privrange interval
      :param delta: (::adiff_t)
      :returns: 0: Ok
      :returns: -1: error (and message in errbuf)



   .. py:method:: ev_cvt64_supval(node: nodeidx_t, tag: uchar, idx: nodeidx_t, data: uchar const *) -> int

      perform 32-64 conversion for a netnode array element 
                
      :param node: (::nodeidx_t)
      :param tag: (uchar)
      :param idx: (::nodeidx_t)
      :param data: (const uchar *)
      :returns: 0: nothing was done
      :returns: 1: converted successfully
      :returns: -1: error (and message in errbuf)



   .. py:method:: ev_cvt64_hashval(node: nodeidx_t, tag: uchar, name: str, data: uchar const *) -> int

      perform 32-64 conversion for a hash value 
                
      :param node: (::nodeidx_t)
      :param tag: (uchar)
      :param name: (const ::char *)
      :param data: (const uchar *)
      :returns: 0: nothing was done
      :returns: 1: converted successfully
      :returns: -1: error (and message in errbuf)



   .. py:method:: ev_gen_stkvar_def(outctx: outctx_t *, stkvar: udm_t, v: int, tid: tid_t) -> int

      Generate stack variable definition line Default line is varname = type ptr value, where 'type' is one of byte,word,dword,qword,tbyte 
                
      :param outctx: (outctx_t *)
      :param stkvar: (const udm_t *)
      :param v: (sval_t)
      :param tid: (tid_t) stkvar TID
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_is_addr_insn(type: int *, insn: insn_t const *) -> int

      Does the instruction calculate some address using an immediate operand? e.g. in PC such operand may be o_displ: 'lea eax, [esi+4]' 
                
      :param type: (int *) pointer to the returned instruction type:
      * 0 the "add" instruction (the immediate operand is a relative value)
      * 1 the "move" instruction (the immediate operand is an absolute value)
      * 2 the "sub" instruction (the immediate operand is a relative value)
      :param insn: (const insn_t *) instruction
      :returns: >0 the operand number+1
      :returns: 0: not implemented



   .. py:method:: ev_next_exec_insn(target: ea_t *, ea: ida_idaapi.ea_t, tid: int, getreg: processor_t::regval_getter_t *, regvalues: regval_t) -> int

      Get next address to be executed This function must return the next address to be executed. If the instruction following the current one is executed, then it must return BADADDR Usually the instructions to consider are: jumps, branches, calls, returns. This function is essential if the 'single step' is not supported in hardware. 
                
      :param target: (::ea_t *), out: pointer to the answer
      :param ea: (::ea_t) instruction address
      :param tid: (int) current therad id
      :param getreg: (::processor_t::regval_getter_t *) function to get register values
      :param regvalues: (const regval_t *) register values array
      :returns: 0: unimplemented
      :returns: 1: implemented



   .. py:method:: ev_calc_step_over(target: ea_t *, ip: ida_idaapi.ea_t) -> int

      Calculate the address of the instruction which will be executed after "step over". The kernel will put a breakpoint there. If the step over is equal to step into or we cannot calculate the address, return BADADDR. 
                
      :param target: (::ea_t *) pointer to the answer
      :param ip: (::ea_t) instruction address
      :returns: 0: unimplemented
      :returns: 1: implemented



   .. py:method:: ev_calc_next_eas(res: eavec_t *, insn: insn_t const *, over: bool) -> int

      Calculate list of addresses the instruction in 'insn' may pass control to. This callback is required for source level debugging. 
                
      :param res: (eavec_t *), out: array for the results.
      :param insn: (const insn_t*) the instruction
      :param over: (bool) calculate for step over (ignore call targets)
      :returns: <0: incalculable (indirect jumps, for example)
      :returns: >=0: number of addresses of called functions in the array. They must be put at the beginning of the array (0 if over=true)



   .. py:method:: ev_get_macro_insn_head(head: ea_t *, ip: ida_idaapi.ea_t) -> int

      Calculate the start of a macro instruction. This notification is called if IP points to the middle of an instruction 
                
      :param head: (::ea_t *), out: answer, BADADDR means normal instruction
      :param ip: (::ea_t) instruction address
      :returns: 0: unimplemented
      :returns: 1: implemented



   .. py:method:: ev_get_dbr_opnum(opnum: int *, insn: insn_t const *) -> int

      Get the number of the operand to be displayed in the debugger reference view (text mode). 
                
      :param opnum: (int *) operand number (out, -1 means no such operand)
      :param insn: (const insn_t*) the instruction
      :returns: 0: unimplemented
      :returns: 1: implemented



   .. py:method:: ev_insn_reads_tbit(insn: insn_t const *, getreg: processor_t::regval_getter_t *, regvalues: regval_t) -> int

      Check if insn will read the TF bit. 
                
      :param insn: (const insn_t*) the instruction
      :param getreg: (::processor_t::regval_getter_t *) function to get register values
      :param regvalues: (const regval_t *) register values array
      :returns: 2: yes, will generate 'step' exception
      :returns: 1: yes, will store the TF bit in memory
      :returns: 0: no



   .. py:method:: ev_clean_tbit(ea: ida_idaapi.ea_t, getreg: processor_t::regval_getter_t *, regvalues: regval_t) -> int

      Clear the TF bit after an insn like pushf stored it in memory. 
                
      :param ea: (::ea_t) instruction address
      :param getreg: (::processor_t::regval_getter_t *) function to get register values
      :param regvalues: (const regval_t *) register values array
      :returns: 1: ok
      :returns: 0: failed



   .. py:method:: ev_get_reg_info(main_regname: char const **, bitrange: bitrange_t, regname: str) -> int

      Get register information by its name. example: "ah" returns:
      * main_regname="eax"
      * bitrange_t = { offset==8, nbits==8 }


      This callback may be unimplemented if the register names are all present in processor_t::reg_names and they all have the same size 
                
      :param main_regname: (const char **), out
      :param bitrange: (bitrange_t *), out: position and size of the value within 'main_regname' (empty bitrange == whole register)
      :param regname: (const char *)
      :returns: 1: ok
      :returns: -1: failed (not found)
      :returns: 0: unimplemented



   .. py:method:: ev_update_call_stack(stack: call_stack_t, tid: int, getreg: processor_t::regval_getter_t *, regvalues: regval_t) -> int

      Calculate the call stack trace for the given thread. This callback is invoked when the process is suspended and should fill the 'trace' object with the information about the current call stack. Note that this callback is NOT invoked if the current debugger backend implements stack tracing via debugger_t::event_t::ev_update_call_stack. The debugger-specific algorithm takes priority. Implementing this callback in the processor module is useful when multiple debugging platforms follow similar patterns, and thus the same processor-specific algorithm can be used for different platforms. 
                
      :param stack: (call_stack_t *) result
      :param tid: (int) thread id
      :param getreg: (::processor_t::regval_getter_t *) function to get register values
      :param regvalues: (const regval_t *) register values array
      :returns: 1: ok
      :returns: -1: failed
      :returns: 0: unimplemented



   .. py:method:: ev_setup_til() -> int

      Setup default type libraries. (called after loading a new file into the database). The processor module may load tils, setup memory model and perform other actions required to set up the type system. This is an optional callback. 
                
      :returns: void: 



   .. py:method:: ev_get_abi_info(comp: comp_t) -> int

      Get all possible ABI names and optional extensions for given compiler abiname/option is a string entirely consisting of letters, digits and underscore 
                
      :param comp: (comp_t) - compiler ID
      :returns: 0: not implemented
      :returns: 1: ok



   .. py:method:: ev_max_ptr_size() -> int

      Get maximal size of a pointer in bytes. 
                
      :returns: max possible size of a pointer



   .. py:method:: ev_get_default_enum_size() -> int

      Get default enum size. Not generated anymore. inf_get_cc_size_e() is used instead 
                



   .. py:method:: ev_get_cc_regs(regs: callregs_t, cc: callcnv_t) -> int

      Get register allocation convention for given calling convention 
                
      :param regs: (callregs_t *), out
      :param cc: (::callcnv_t)
      :returns: 1: 
      :returns: 0: not implemented



   .. py:method:: ev_get_simd_types(out: simd_info_vec_t *, simd_attrs: simd_info_t, argloc: argloc_t, create_tifs: bool) -> int

      Get SIMD-related types according to given attributes ant/or argument location 
                
      :param out: (::simd_info_vec_t *)
      :param simd_attrs: (const simd_info_t *), may be nullptr
      :param argloc: (const argloc_t *), may be nullptr
      :param create_tifs: (bool) return valid tinfo_t objects, create if neccessary
      :returns: number: of found types
      :returns: -1: error If name==nullptr, initialize all SIMD types



   .. py:method:: ev_calc_cdecl_purged_bytes(ea: ida_idaapi.ea_t) -> int

      Calculate number of purged bytes after call. 
                
      :param ea: (::ea_t) address of the call instruction
      :returns: number of purged bytes (usually add sp, N)



   .. py:method:: ev_calc_purged_bytes(p_purged_bytes: int *, fti: func_type_data_t) -> int

      Calculate number of purged bytes by the given function type. 
                
      :param p_purged_bytes: (int *) ptr to output
      :param fti: (const func_type_data_t *) func type details
      :returns: 1: 
      :returns: 0: not implemented



   .. py:method:: ev_calc_retloc(retloc: argloc_t, rettype: tinfo_t, cc: callcnv_t) -> int

      Calculate return value location. 
                
      :param retloc: (argloc_t *)
      :param rettype: (const tinfo_t *)
      :param cc: (::callcnv_t)
      :returns: 0: not implemented
      :returns: 1: ok,
      :returns: -1: error



   .. py:method:: ev_calc_arglocs(fti: func_type_data_t) -> int

      Calculate function argument locations. This callback should fill retloc, all arglocs, and stkargs. This callback is never called for CM_CC_SPECIAL functions. 
                
      :param fti: (func_type_data_t *) points to the func type info
      :returns: 0: not implemented
      :returns: 1: ok
      :returns: -1: error



   .. py:method:: ev_calc_varglocs(ftd: func_type_data_t, aux_regs: regobjs_t, aux_stkargs: relobj_t, nfixed: int) -> int

      Calculate locations of the arguments that correspond to '...'. 
                
      :param ftd: (func_type_data_t *), inout: info about all arguments (including varargs)
      :param aux_regs: (regobjs_t *) buffer for hidden register arguments, may be nullptr
      :param aux_stkargs: (relobj_t *) buffer for hidden stack arguments, may be nullptr
      :param nfixed: (int) number of fixed arguments
      :returns: 0: not implemented
      :returns: 1: ok
      :returns: -1: error On some platforms variadic calls require passing additional information: for example, number of floating variadic arguments must be passed in rax on gcc-x64. The locations and values that constitute this additional information are returned in the buffers pointed by aux_regs and aux_stkargs



   .. py:method:: ev_adjust_argloc(argloc: argloc_t, optional_type: tinfo_t, size: int) -> int

      Adjust argloc according to its type/size and platform endianess 
                
      :param argloc: (argloc_t *), inout
      :param size: (int) 'size' makes no sense if type != nullptr (type->get_size() should be used instead)
      :returns: 0: not implemented
      :returns: 1: ok
      :returns: -1: error



   .. py:method:: ev_lower_func_type(argnums: intvec_t *, fti: func_type_data_t) -> int

      Get function arguments which should be converted to pointers when lowering function prototype. The processor module can also modify 'fti' in order to make non-standard conversion of some arguments. 
                
      :param argnums: (intvec_t *), out - numbers of arguments to be converted to pointers in acsending order
      :param fti: (func_type_data_t *), inout func type details
      :returns: 0: not implemented
      :returns: 1: argnums was filled
      :returns: 2: argnums was filled and made substantial changes to fti argnums[0] can contain a special negative value indicating that the return value should be passed as a hidden 'retstr' argument: -1 this argument is passed as the first one and the function returns a pointer to the argument, -2 this argument is passed as the last one and the function returns a pointer to the argument, -3 this argument is passed as the first one and the function returns 'void'.



   .. py:method:: ev_equal_reglocs(a1: argloc_t, a2: argloc_t) -> int

      Are 2 register arglocs the same?. We need this callback for the pc module. 
                
      :param a1: (argloc_t *)
      :param a2: (argloc_t *)
      :returns: 1: yes
      :returns: -1: no
      :returns: 0: not implemented



   .. py:method:: ev_use_stkarg_type(ea: ida_idaapi.ea_t, arg: funcarg_t) -> int

      Use information about a stack argument. 
                
      :param ea: (::ea_t) address of the push instruction which pushes the function argument into the stack
      :param arg: (const funcarg_t *) argument info
      :returns: 1: ok
      :returns: <=0: failed, the kernel will create a comment with the argument name or type for the instruction



   .. py:method:: ev_use_regarg_type(ea: ida_idaapi.ea_t, rargs: funcargvec_t const *) -> PyObject *

      Use information about register argument. 
                
      :param ea: (::ea_t) address of the instruction
      :param rargs: (const funcargvec_t *) vector of register arguments (including regs extracted from scattered arguments)
      :returns: 1: 
      :returns: 0: not implemented



   .. py:method:: ev_use_arg_types(ea: ida_idaapi.ea_t, fti: func_type_data_t, rargs: funcargvec_t *) -> int

      Use information about callee arguments. 
                
      :param ea: (::ea_t) address of the call instruction
      :param fti: (func_type_data_t *) info about function type
      :param rargs: (funcargvec_t *) array of register arguments
      :returns: 1: (and removes handled arguments from fti and rargs)
      :returns: 0: not implemented



   .. py:method:: ev_arg_addrs_ready(caller: ida_idaapi.ea_t, n: int, tif: tinfo_t, addrs: ea_t *) -> int

      Argument address info is ready. 
                
      :param caller: (::ea_t)
      :param n: (int) number of formal arguments
      :param tif: (tinfo_t *) call prototype
      :param addrs: (::ea_t *) argument intilization addresses
      :returns: <0: do not save into idb; other values mean "ok to save"



   .. py:method:: ev_decorate_name(name: str, mangle: bool, cc: int, optional_type: tinfo_t) -> PyObject *

      Decorate/undecorate a C symbol name. 
                
      :param name: (const char *) name of symbol
      :param mangle: (bool) true-mangle, false-unmangle
      :param cc: (::callcnv_t) calling convention
      :returns: 1: if success
      :returns: 0: not implemented or failed



   .. py:method:: ev_arch_changed() -> int

      The loader is done parsing arch-related information, which the processor module might want to use to finish its initialization. 
                
      :returns: 1: if success
      :returns: 0: not implemented or failed



   .. py:method:: ev_get_stkarg_area_info(out: stkarg_area_info_t, cc: callcnv_t) -> int

      Get some metrics of the stack argument area. 
                
      :param out: (stkarg_area_info_t *) ptr to stkarg_area_info_t
      :param cc: (::callcnv_t) calling convention
      :returns: 1: if success
      :returns: 0: not implemented



   .. py:method:: ev_last_cb_before_loader() -> int


   .. py:method:: ev_loader() -> int

      This code and higher ones are reserved for the loaders. The arguments and the return values are defined by the loaders 
                



.. py:function:: get_idp_notifier_addr(arg1: PyObject *) -> PyObject *

.. py:function:: get_idp_notifier_ud_addr(hooks: IDP_Hooks) -> PyObject *

.. py:function:: delay_slot_insn(ea: ea_t *, bexec: bool *, fexec: bool *) -> bool

.. py:function:: get_reg_info(regname: str, bitrange: bitrange_t) -> str

.. py:function:: sizeof_ldbl() -> size_t

.. py:data:: REAL_ERROR_FORMAT
   :value: -1


.. py:data:: REAL_ERROR_RANGE
   :value: -2


.. py:data:: REAL_ERROR_BADDATA
   :value: -3


.. py:data:: IDPOPT_STR
   :value: 1


.. py:data:: IDPOPT_NUM
   :value: 2


.. py:data:: IDPOPT_BIT
   :value: 3


.. py:data:: IDPOPT_FLT
   :value: 4


.. py:data:: IDPOPT_I64
   :value: 5


.. py:data:: IDPOPT_OK
   :value: 0


.. py:data:: IDPOPT_BADKEY
   :value: 1


.. py:data:: IDPOPT_BADTYPE
   :value: 2


.. py:data:: IDPOPT_BADVALUE
   :value: 3


.. py:class:: processor_t

   Bases: :py:obj:`IDP_Hooks`


   .. py:attribute:: idb_hooks


   .. py:method:: get_idpdesc()

      This function must be present and should return the list of
      short processor names similar to the one in ph.psnames.
      This method can be overridden to return to the kernel a different IDP description.



   .. py:method:: get_auxpref(insn)

      This function returns insn.auxpref value



   .. py:method:: ev_newprc(*args)

      Before changing processor type. 
                
      :param pnum: (int) processor number in the array of processor names
      :param keep_cfg: (bool) true: do not modify kernel configuration
      :returns: 1: ok
      :returns: <0: prohibit



   .. py:method:: ev_newfile(*args)

      A new file has been loaded. 
                
      :param fname: (char *) input file name



   .. py:method:: ev_oldfile(*args)

      An old file has been loaded. 
                
      :param fname: (char *) input file name



   .. py:method:: ev_newbinary(*args)

      IDA is about to load a binary file. 
                
      :param filename: (char *) binary file name
      :param fileoff: (qoff64_t) offset in the file
      :param basepara: (::ea_t) base loading paragraph
      :param binoff: (::ea_t) loader offset
      :param nbytes: (::uint64) number of bytes to load



   .. py:method:: ev_endbinary(*args)

      IDA has loaded a binary file. 
                
      :param ok: (bool) file loaded successfully?



   .. py:method:: ev_set_idp_options(keyword, value_type, value, idb_loaded)

      Set IDP-specific configuration option Also see set_options_t in config.hpp 
                
      :param keyword: (const char *)
      :param value_type: (int)
      :param value: (const void *)
      :param idb_loaded: (bool) true if the ev_oldfile/ev_newfile events have been generated
      :returns: 1: ok
      :returns: 0: not implemented
      :returns: -1: error (and message in errbuf)



   .. py:method:: ev_set_proc_options(*args)

      Called if the user specified an option string in the command line: -p<processor name>:<options>. Can be used for setting a processor subtype. Also called if option string is passed to set_processor_type() and IDC's SetProcessorType(). 
                
      :param options: (const char *)
      :param confidence: (int) 0: loader's suggestion 1: user's decision
      :returns: <0: if bad option string



   .. py:method:: ev_ana_insn(*args)

      Analyze one instruction and fill 'out' structure. This function shouldn't change the database, flags or anything else. All these actions should be performed only by emu_insn() function. insn_t::ea contains address of instruction to analyze. 
                
      :param out: (insn_t *)
      :returns: length of the instruction in bytes, 0 if instruction can't be decoded.
      :returns: 0: if instruction can't be decoded.



   .. py:method:: ev_emu_insn(*args)

      Emulate instruction, create cross-references, plan to analyze subsequent instructions, modify flags etc. Upon entrance to this function, all information about the instruction is in 'insn' structure. 
                
      :param insn: (const insn_t *)
      :returns: 1: ok
      :returns: -1: the kernel will delete the instruction



   .. py:method:: ev_out_header(*args)

      Function to produce start of disassembled text 
                
      :param outctx: (outctx_t *)
      :returns: void: 



   .. py:method:: ev_out_footer(*args)

      Function to produce end of disassembled text 
                
      :param outctx: (outctx_t *)
      :returns: void: 



   .. py:method:: ev_out_segstart(ctx, s)

      Function to produce start of segment 
                
      :param outctx: (outctx_t *)
      :param seg: (segment_t *)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_out_segend(ctx, s)

      Function to produce end of segment 
                
      :param outctx: (outctx_t *)
      :param seg: (segment_t *)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_out_assumes(*args)

      Function to produce assume directives when segment register value changes. 
                
      :param outctx: (outctx_t *)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_out_insn(*args)

      Generate text representation of an instruction in 'ctx.insn' outctx_t provides functions to output the generated text. This function shouldn't change the database, flags or anything else. All these actions should be performed only by emu_insn() function. 
                
      :param outctx: (outctx_t *)
      :returns: void: 



   .. py:method:: ev_out_mnem(*args)

      Generate instruction mnemonics. This callback should append the colored mnemonics to ctx.outbuf Optional notification, if absent, out_mnem will be called. 
                
      :param outctx: (outctx_t *)
      :returns: 1: if appended the mnemonics
      :returns: 0: not implemented



   .. py:method:: ev_out_operand(*args)

      Generate text representation of an instruction operand outctx_t provides functions to output the generated text. All these actions should be performed only by emu_insn() function. 
                
      :param outctx: (outctx_t *)
      :param op: (const op_t *)
      :returns: 1: ok
      :returns: -1: operand is hidden



   .. py:method:: ev_out_data(*args)

      Generate text representation of data items This function may change the database and create cross-references if analyze_only is set 
                
      :param outctx: (outctx_t *)
      :param analyze_only: (bool)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_out_label(*args)

      The kernel is going to generate an instruction label line or a function header. 
                
      :param outctx: (outctx_t *)
      :param colored_name: (const char *)
      :returns: <0: if the kernel should not generate the label
      :returns: 0: not implemented or continue



   .. py:method:: ev_out_special_item(*args)

      Generate text representation of an item in a special segment i.e. absolute symbols, externs, communal definitions etc 
                
      :param outctx: (outctx_t *)
      :param segtype: (uchar)
      :returns: 1: ok
      :returns: 0: not implemented
      :returns: -1: overflow



   .. py:method:: ev_gen_regvar_def(ctx, v)

      Generate register variable definition line. 
                
      :param outctx: (outctx_t *)
      :param v: (regvar_t *)
      :returns: >0: ok, generated the definition text
      :returns: 0: not implemented



   .. py:method:: ev_gen_src_file_lnnum(*args)

      Callback: generate analog of: 
           #line  123
          


                
      :param outctx: (outctx_t *) output context
      :param file: (const char *) source file (may be nullptr)
      :param lnnum: (size_t) line number
      :returns: 1: directive has been generated
      :returns: 0: not implemented



   .. py:method:: ev_creating_segm(s)

      A new segment is about to be created. 
                
      :param seg: (segment_t *)
      :returns: 1: ok
      :returns: <0: segment should not be created



   .. py:method:: ev_moving_segm(s, to_ea, flags)

      May the kernel move the segment? 
                
      :param seg: (segment_t *) segment to move
      :param to: (::ea_t) new segment start address
      :param flags: (int) combination of Move segment flags
      :returns: 0: yes
      :returns: <0: the kernel should stop



   .. py:method:: ev_coagulate(*args)

      Try to define some unexplored bytes. This notification will be called if the kernel tried all possibilities and could not find anything more useful than to convert to array of bytes. The module can help the kernel and convert the bytes into something more useful. 
                
      :param start_ea: (::ea_t)
      :returns: number of converted bytes



   .. py:method:: ev_undefine(*args)

      An item in the database (insn or data) is being deleted. 
                
      :param ea: (ea_t)
      :returns: 1: do not delete srranges at the item end
      :returns: 0: srranges can be deleted



   .. py:method:: ev_treat_hindering_item(*args)

      An item hinders creation of another item. 
                
      :param hindering_item_ea: (::ea_t)
      :param new_item_flags: (flags64_t) (0 for code)
      :param new_item_ea: (::ea_t)
      :param new_item_length: (::asize_t)
      :returns: 0: no reaction
      :returns: !=0: the kernel may delete the hindering item



   .. py:method:: ev_rename(*args)

      The kernel is going to rename a byte. 
                
      :param ea: (::ea_t)
      :param new_name: (const char *)
      :returns: <0: if the kernel should not rename it.
      :returns: 2: to inhibit the notification. I.e., the kernel should not rename, but 'set_name()' should return 'true'. also see renamed the return value is ignored when kernel is going to delete name



   .. py:method:: ev_is_far_jump(*args)

      is indirect far jump or call instruction? meaningful only if the processor has 'near' and 'far' reference types 
                
      :param icode: (int)
      :returns: 0: not implemented
      :returns: 1: yes
      :returns: -1: no



   .. py:method:: ev_is_sane_insn(*args)

      Is the instruction sane for the current file type?. 
                
      :param insn: (const insn_t*) the instruction
      :param no_crefs: (int) 1: the instruction has no code refs to it. ida just tries to convert unexplored bytes to an instruction (but there is no other reason to convert them into an instruction) 0: the instruction is created because of some coderef, user request or another weighty reason.
      :returns: >=0: ok
      :returns: <0: no, the instruction isn't likely to appear in the program



   .. py:method:: ev_is_call_insn(*args)

      Is the instruction a "call"? 
                
      :param insn: (const insn_t *) instruction
      :returns: 0: unknown
      :returns: <0: no
      :returns: 1: yes



   .. py:method:: ev_is_ret_insn(*args)

      Is the instruction a "return"? 
                
      :param insn: (const insn_t *) instruction
      :param flags: (uchar), combination of IRI_... flags (see above)
      :returns: 0: unknown
      :returns: <0: no
      :returns: 1: yes



   .. py:method:: ev_may_be_func(*args)

      Can a function start here? 
                
      :param insn: (const insn_t*) the instruction
      :param state: (int) autoanalysis phase 0: creating functions 1: creating chunks
      :returns: probability 1..100



   .. py:method:: ev_is_basic_block_end(*args)

      Is the current instruction end of a basic block?. This function should be defined for processors with delayed jump slots. 
                
      :param insn: (const insn_t*) the instruction
      :param call_insn_stops_block: (bool)
      :returns: 0: unknown
      :returns: <0: no
      :returns: 1: yes



   .. py:method:: ev_is_indirect_jump(*args)

      Determine if instruction is an indirect jump. If CF_JUMP bit cannot describe all jump types jumps, please define this callback. 
                
      :param insn: (const insn_t*) the instruction
      :returns: 0: use CF_JUMP
      :returns: 1: no
      :returns: 2: yes



   .. py:method:: ev_is_insn_table_jump(*args)

      Reserved.



   .. py:method:: ev_is_switch(*args)

      Find 'switch' idiom or override processor module's decision. It will be called for instructions marked with CF_JUMP. 
                
      :param si: (switch_info_t *), out
      :param insn: (const insn_t *) instruction possibly belonging to a switch
      :returns: 1: switch is found, 'si' is filled. IDA will create the switch using the filled 'si'
      :returns: -1: no switch found. This value forbids switch creation by the processor module
      :returns: 0: not implemented



   .. py:method:: ev_create_switch_xrefs(*args)

      Create xrefs for a custom jump table. 
                
      :param jumpea: (::ea_t) address of the jump insn
      :param si: (const switch_info_t *) switch information
      :returns: must return 1 Must be implemented if module uses custom jump tables, SWI_CUSTOM



   .. py:method:: ev_is_align_insn(*args)

      Is the instruction created only for alignment purposes?. Do not directly call this function, use is_align_insn() 
                
      :param ea: (ea_t) - instruction address
      :returns: number: of bytes in the instruction



   .. py:method:: ev_is_alloca_probe(*args)

      Does the function at 'ea' behave as __alloca_probe? 
                
      :param ea: (::ea_t)
      :returns: 1: yes
      :returns: 0: no



   .. py:method:: ev_is_sp_based(mode, insn, op)

      Check whether the operand is relative to stack pointer or frame pointer This event is used to determine how to output a stack variable If not implemented, then all operands are sp based by default. Implement this event only if some stack references use frame pointer instead of stack pointer. 
                
      :param mode: (int *) out, combination of SP/FP operand flags
      :param insn: (const insn_t *)
      :param op: (const op_t *)
      :returns: 0: not implemented
      :returns: 1: ok



   .. py:method:: ev_can_have_type(*args)

      Can the operand have a type as offset, segment, decimal, etc? (for example, a register AX can't have a type, meaning that the user can't change its representation. see bytes.hpp for information about types and flags) 
                
      :param op: (const op_t *)
      :returns: 0: unknown
      :returns: <0: no
      :returns: 1: yes



   .. py:method:: ev_cmp_operands(*args)

      Compare instruction operands 
                
      :param op1: (const op_t*)
      :param op2: (const op_t*)
      :returns: 1: equal
      :returns: -1: not equal
      :returns: 0: not implemented



   .. py:method:: ev_get_operand_string(buf, insn, opnum)

      Request text string for operand (cli, java, ...). 
                
      :param insn: (const insn_t*) the instruction
      :param opnum: (int) operand number, -1 means any string operand
      :returns: 0: no string (or empty string)
      :returns: >0: original string length without terminating zero



   .. py:method:: ev_str2reg(*args)

      Convert a register name to a register number. The register number is the register index in the processor_t::reg_names array Most processor modules do not need to implement this callback It is useful only if processor_t::reg_names[reg] does not provide the correct register names 
                
      :param regname: (const char *)
      :returns: register: number + 1
      :returns: 0: not implemented or could not be decoded



   .. py:method:: ev_get_autocmt(*args)

      Callback: get dynamic auto comment. Will be called if the autocomments are enabled and the comment retrieved from ida.int starts with '$!'. 'insn' contains valid info. 
                
      :param insn: (const insn_t*) the instruction
      :returns: 1: new comment has been generated
      :returns: 0: callback has not been handled. the buffer must not be changed in this case



   .. py:method:: ev_func_bounds(_possible_return_code, pfn, max_func_end_ea)

      find_func_bounds() finished its work. The module may fine tune the function bounds 
                
      :param possible_return_code: (int *), in/out
      :param pfn: (func_t *)
      :param max_func_end_ea: (::ea_t) (from the kernel's point of view)
      :returns: void: 



   .. py:method:: ev_verify_sp(pfn)

      All function instructions have been analyzed. Now the processor module can analyze the stack pointer for the whole function 
                
      :param pfn: (func_t *)
      :returns: 0: ok
      :returns: <0: bad stack pointer



   .. py:method:: ev_verify_noreturn(pfn)

      The kernel wants to set 'noreturn' flags for a function. 
                
      :param pfn: (func_t *)
      :returns: 0: ok. any other value: do not set 'noreturn' flag



   .. py:method:: ev_create_func_frame(pfn)

      Create a function frame for a newly created function Set up frame size, its attributes etc 
                
      :param pfn: (func_t *)
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_get_frame_retsize(frsize, pfn)

      Get size of function return address in bytes If this event is not implemented, the kernel will assume
      * 8 bytes for 64-bit function
      * 4 bytes for 32-bit function
      * 2 bytes otherwise



      :param frsize: (int *) frame size (out)
      :param pfn: (const func_t *), can't be nullptr
      :returns: 1: ok
      :returns: 0: not implemented



   .. py:method:: ev_coagulate_dref(from_ea, to_ea, may_define, _code_ea)

      Data reference is being analyzed. plugin may correct 'code_ea' (e.g. for thumb mode refs, we clear the last bit) 
                
      :param to: (::ea_t)
      :param may_define: (bool)
      :param code_ea: (::ea_t *)
      :returns: <0: failed dref analysis, >0 done dref analysis
      :returns: 0: not implemented or continue



   .. py:method:: ev_may_show_sreg(*args)

      The kernel wants to display the segment registers in the messages window. 
                
      :param current_ea: (::ea_t)
      :returns: <0: if the kernel should not show the segment registers. (assuming that the module has done it)
      :returns: 0: not implemented



   .. py:method:: ev_auto_queue_empty(*args)

      One analysis queue is empty. 
                
      :param type: (atype_t)
      :returns: void: see also idb_event::auto_empty_finally



   .. py:method:: ev_validate_flirt_func(*args)

      Flirt has recognized a library function. This callback can be used by a plugin or proc module to intercept it and validate such a function. 
                
      :param start_ea: (::ea_t)
      :param funcname: (const char *)
      :returns: -1: do not create a function,
      :returns: 0: function is validated



   .. py:method:: ev_assemble(*args)

      Assemble an instruction. (display a warning if an error is found). 
                
      :param ea: (::ea_t) linear address of instruction
      :param cs: (::ea_t) cs of instruction
      :param ip: (::ea_t) ip of instruction
      :param use32: (bool) is 32bit segment?
      :param line: (const char *) line to assemble
      :returns: size of the instruction in bytes



   .. py:method:: ev_gen_map_file(nlines, fp)

      Generate map file. If not implemented the kernel itself will create the map file. 
                
      :param nlines: (int *) number of lines in map file (-1 means write error)
      :param fp: (FILE *) output file
      :returns: 0: not implemented
      :returns: 1: ok
      :returns: -1: write error



   .. py:method:: ev_calc_step_over(target, ip)

      Calculate the address of the instruction which will be executed after "step over". The kernel will put a breakpoint there. If the step over is equal to step into or we cannot calculate the address, return BADADDR. 
                
      :param target: (::ea_t *) pointer to the answer
      :param ip: (::ea_t) instruction address
      :returns: 0: unimplemented
      :returns: 1: implemented



   .. py:method:: closebase(*args)


   .. py:method:: savebase(*args)


   .. py:method:: auto_empty(*args)


   .. py:method:: auto_empty_finally(*args)


   .. py:method:: determined_main(*args)


   .. py:method:: idasgn_loaded(*args)


   .. py:method:: kernel_config_loaded(*args)


   .. py:method:: compiler_changed(*args)


   .. py:method:: segm_moved(from_ea, to_ea, size, changed_netmap)


   .. py:method:: func_added(pfn)


   .. py:method:: set_func_start(*args)


   .. py:method:: set_func_end(*args)


   .. py:method:: deleting_func(pfn)


   .. py:method:: sgr_changed(*args)


   .. py:method:: make_code(*args)


   .. py:method:: make_data(*args)


   .. py:method:: renamed(*args)


.. py:function:: str2sreg(name: str)

   get segment register number from its name or -1


.. py:data:: ph

.. py:class:: IDB_Hooks(_flags: int = 0, _hkcb_flags: int = 1)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: hook() -> bool


   .. py:method:: unhook() -> bool


   .. py:method:: closebase() -> None

      The database will be closed now.



   .. py:method:: savebase() -> None

      The database is being saved.



   .. py:method:: upgraded(_from: int) -> None

      The database has been upgraded and the receiver can upgrade its info as well 
                



   .. py:method:: auto_empty() -> None

      Info: all analysis queues are empty. This callback is called once when the initial analysis is finished. If the queue is not empty upon the return from this callback, it will be called later again. 
                



   .. py:method:: auto_empty_finally() -> None

      Info: all analysis queues are empty definitively. This callback is called only once. 
                



   .. py:method:: determined_main(main: ida_idaapi.ea_t) -> None

      The main() function has been determined. 
                
      :param main: (::ea_t) address of the main() function



   .. py:method:: extlang_changed(kind: int, el: extlang_t *, idx: int) -> None

      The list of extlangs or the default extlang was changed. 
                
      :param kind: (int) 0: extlang installed 1: extlang removed 2: default extlang changed
      :param el: (extlang_t *) pointer to the extlang affected
      :param idx: (int) extlang index



   .. py:method:: idasgn_loaded(short_sig_name: str) -> None

      FLIRT signature has been loaded for normal processing (not for recognition of startup sequences). 
                
      :param short_sig_name: (const char *)



   .. py:method:: kernel_config_loaded(pass_number: int) -> None

      This event is issued when ida.cfg is parsed. 
                
      :param pass_number: (int)



   .. py:method:: loader_finished(li: linput_t *, neflags: uint16, filetypename: str) -> None

      External file loader finished its work. Use this event to augment the existing loader functionality. 
                
      :param li: (linput_t *)
      :param neflags: (uint16) Load file flags
      :param filetypename: (const char *)



   .. py:method:: flow_chart_created(fc: qflow_chart_t) -> None

      Gui has retrieved a function flow chart. Plugins may modify the flow chart in this callback. 
                
      :param fc: (qflow_chart_t *)



   .. py:method:: compiler_changed(adjust_inf_fields: bool) -> None

      The kernel has changed the compiler information. ( idainfo::cc structure; get_abi_name) 
                
      :param adjust_inf_fields: (::bool) may change inf fields?



   .. py:method:: changing_ti(ea: ida_idaapi.ea_t, new_type: type_t const *, new_fnames: p_list const *) -> None

      An item typestring (c/c++ prototype) is to be changed. 
                
      :param ea: (::ea_t)
      :param new_type: (const type_t *)
      :param new_fnames: (const p_list *)



   .. py:method:: ti_changed(ea: ida_idaapi.ea_t, type: type_t const *, fnames: p_list const *) -> None

      An item typestring (c/c++ prototype) has been changed. 
                
      :param ea: (::ea_t)
      :param type: (const type_t *)
      :param fnames: (const p_list *)



   .. py:method:: changing_op_ti(ea: ida_idaapi.ea_t, n: int, new_type: type_t const *, new_fnames: p_list const *) -> None

      An operand typestring (c/c++ prototype) is to be changed. 
                
      :param ea: (::ea_t)
      :param n: (int)
      :param new_type: (const type_t *)
      :param new_fnames: (const p_list *)



   .. py:method:: op_ti_changed(ea: ida_idaapi.ea_t, n: int, type: type_t const *, fnames: p_list const *) -> None

      An operand typestring (c/c++ prototype) has been changed. 
                
      :param ea: (::ea_t)
      :param n: (int)
      :param type: (const type_t *)
      :param fnames: (const p_list *)



   .. py:method:: changing_op_type(ea: ida_idaapi.ea_t, n: int, opinfo: opinfo_t) -> None

      An operand type (offset, hex, etc...) is to be changed. 
                
      :param ea: (::ea_t)
      :param n: (int) eventually or'ed with OPND_OUTER or OPND_ALL
      :param opinfo: (const opinfo_t *) additional operand info



   .. py:method:: op_type_changed(ea: ida_idaapi.ea_t, n: int) -> None

      An operand type (offset, hex, etc...) has been set or deleted. 
                
      :param ea: (::ea_t)
      :param n: (int) eventually or'ed with OPND_OUTER or OPND_ALL



   .. py:method:: segm_added(s: segment_t *) -> None

      A new segment has been created. 
                
      :param s: (segment_t *) See also adding_segm



   .. py:method:: deleting_segm(start_ea: ida_idaapi.ea_t) -> None

      A segment is to be deleted. 
                
      :param start_ea: (::ea_t)



   .. py:method:: segm_deleted(start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t, flags: int) -> None

      A segment has been deleted. 
                
      :param start_ea: (::ea_t)
      :param end_ea: (::ea_t)
      :param flags: (int)



   .. py:method:: changing_segm_start(s: segment_t *, new_start: ida_idaapi.ea_t, segmod_flags: int) -> None

      Segment start address is to be changed. 
                
      :param s: (segment_t *)
      :param new_start: (::ea_t)
      :param segmod_flags: (int)



   .. py:method:: segm_start_changed(s: segment_t *, oldstart: ida_idaapi.ea_t) -> None

      Segment start address has been changed. 
                
      :param s: (segment_t *)
      :param oldstart: (::ea_t)



   .. py:method:: changing_segm_end(s: segment_t *, new_end: ida_idaapi.ea_t, segmod_flags: int) -> None

      Segment end address is to be changed. 
                
      :param s: (segment_t *)
      :param new_end: (::ea_t)
      :param segmod_flags: (int)



   .. py:method:: segm_end_changed(s: segment_t *, oldend: ida_idaapi.ea_t) -> None

      Segment end address has been changed. 
                
      :param s: (segment_t *)
      :param oldend: (::ea_t)



   .. py:method:: changing_segm_name(s: segment_t *, oldname: str) -> None

      Segment name is being changed. 
                
      :param s: (segment_t *)
      :param oldname: (const char *)



   .. py:method:: segm_name_changed(s: segment_t *, name: str) -> None

      Segment name has been changed. 
                
      :param s: (segment_t *)
      :param name: (const char *)



   .. py:method:: changing_segm_class(s: segment_t *) -> None

      Segment class is being changed. 
                
      :param s: (segment_t *)



   .. py:method:: segm_class_changed(s: segment_t *, sclass: str) -> None

      Segment class has been changed. 
                
      :param s: (segment_t *)
      :param sclass: (const char *)



   .. py:method:: segm_attrs_updated(s: segment_t *) -> None

      Segment attributes has been changed. 
                
      :param s: (segment_t *) This event is generated for secondary segment attributes (examples: color, permissions, etc)



   .. py:method:: segm_moved(_from: ida_idaapi.ea_t, to: ida_idaapi.ea_t, size: asize_t, changed_netmap: bool) -> None

      Segment has been moved. 
                
      :param to: (::ea_t)
      :param size: (::asize_t)
      :param changed_netmap: (bool) See also idb_event::allsegs_moved



   .. py:method:: allsegs_moved(info: segm_move_infos_t *) -> None

      Program rebasing is complete. This event is generated after series of segm_moved events 
                
      :param info: (segm_move_infos_t *)



   .. py:method:: func_added(pfn: func_t *) -> None

      The kernel has added a function. 
                
      :param pfn: (func_t *)



   .. py:method:: func_updated(pfn: func_t *) -> None

      The kernel has updated a function. 
                
      :param pfn: (func_t *)



   .. py:method:: set_func_start(pfn: func_t *, new_start: ida_idaapi.ea_t) -> None

      Function chunk start address will be changed. 
                
      :param pfn: (func_t *)
      :param new_start: (::ea_t)



   .. py:method:: set_func_end(pfn: func_t *, new_end: ida_idaapi.ea_t) -> None

      Function chunk end address will be changed. 
                
      :param pfn: (func_t *)
      :param new_end: (::ea_t)



   .. py:method:: deleting_func(pfn: func_t *) -> None

      The kernel is about to delete a function. 
                
      :param pfn: (func_t *)



   .. py:method:: frame_deleted(pfn: func_t *) -> None

      The kernel has deleted a function frame. 
                
      :param pfn: (func_t *) idb_event::frame_created



   .. py:method:: thunk_func_created(pfn: func_t *) -> None

      A thunk bit has been set for a function. 
                
      :param pfn: (func_t *)



   .. py:method:: func_tail_appended(pfn: func_t *, tail: func_t *) -> None

      A function tail chunk has been appended. 
                
      :param pfn: (func_t *)
      :param tail: (func_t *)



   .. py:method:: deleting_func_tail(pfn: func_t *, tail: range_t) -> None

      A function tail chunk is to be removed. 
                
      :param pfn: (func_t *)
      :param tail: (const range_t *)



   .. py:method:: func_tail_deleted(pfn: func_t *, tail_ea: ida_idaapi.ea_t) -> None

      A function tail chunk has been removed. 
                
      :param pfn: (func_t *)
      :param tail_ea: (::ea_t)



   .. py:method:: tail_owner_changed(tail: func_t *, owner_func: ida_idaapi.ea_t, old_owner: ida_idaapi.ea_t) -> None

      A tail chunk owner has been changed. 
                
      :param tail: (func_t *)
      :param owner_func: (::ea_t)
      :param old_owner: (::ea_t)



   .. py:method:: func_noret_changed(pfn: func_t *) -> None

      FUNC_NORET bit has been changed. 
                
      :param pfn: (func_t *)



   .. py:method:: stkpnts_changed(pfn: func_t *) -> None

      Stack change points have been modified. 
                
      :param pfn: (func_t *)



   .. py:method:: updating_tryblks(tbv: tryblks_t const *) -> None

      About to update tryblk information 
                
      :param tbv: (const ::tryblks_t *)



   .. py:method:: tryblks_updated(tbv: tryblks_t const *) -> None

      Updated tryblk information 
                
      :param tbv: (const ::tryblks_t *)



   .. py:method:: deleting_tryblks(range: range_t) -> None

      About to delete tryblk information in given range 
                
      :param range: (const range_t *)



   .. py:method:: sgr_changed(start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t, regnum: int, value: sel_t, old_value: sel_t, tag: uchar) -> None

      The kernel has changed a segment register value. 
                
      :param start_ea: (::ea_t)
      :param end_ea: (::ea_t)
      :param regnum: (int)
      :param value: (::sel_t)
      :param old_value: (::sel_t)
      :param tag: (uchar) Segment register range tags



   .. py:method:: make_code(insn: insn_t const *) -> None

      An instruction is being created. 
                
      :param insn: (const insn_t*)



   .. py:method:: make_data(ea: ida_idaapi.ea_t, flags: flags64_t, tid: tid_t, len: asize_t) -> None

      A data item is being created. 
                
      :param ea: (::ea_t)
      :param flags: (flags64_t)
      :param tid: (tid_t)
      :param len: (::asize_t)



   .. py:method:: destroyed_items(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, will_disable_range: bool) -> None

      Instructions/data have been destroyed in [ea1,ea2). 
                
      :param ea1: (::ea_t)
      :param ea2: (::ea_t)
      :param will_disable_range: (bool)



   .. py:method:: renamed(ea: ida_idaapi.ea_t, new_name: str, local_name: bool, old_name: str) -> None

      The kernel has renamed a byte. See also the rename event 
                
      :param ea: (::ea_t)
      :param new_name: (const char *) can be nullptr
      :param local_name: (bool)
      :param old_name: (const char *) can be nullptr



   .. py:method:: byte_patched(ea: ida_idaapi.ea_t, old_value: int) -> None

      A byte has been patched. 
                
      :param ea: (::ea_t)
      :param old_value: (uint32)



   .. py:method:: changing_cmt(ea: ida_idaapi.ea_t, repeatable_cmt: bool, newcmt: str) -> None

      An item comment is to be changed. 
                
      :param ea: (::ea_t)
      :param repeatable_cmt: (bool)
      :param newcmt: (const char *)



   .. py:method:: cmt_changed(ea: ida_idaapi.ea_t, repeatable_cmt: bool) -> None

      An item comment has been changed. 
                
      :param ea: (::ea_t)
      :param repeatable_cmt: (bool)



   .. py:method:: changing_range_cmt(kind: range_kind_t, a: range_t, cmt: str, repeatable: bool) -> None

      Range comment is to be changed. 
                
      :param kind: (range_kind_t)
      :param a: (const range_t *)
      :param cmt: (const char *)
      :param repeatable: (bool)



   .. py:method:: range_cmt_changed(kind: range_kind_t, a: range_t, cmt: str, repeatable: bool) -> None

      Range comment has been changed. 
                
      :param kind: (range_kind_t)
      :param a: (const range_t *)
      :param cmt: (const char *)
      :param repeatable: (bool)



   .. py:method:: extra_cmt_changed(ea: ida_idaapi.ea_t, line_idx: int, cmt: str) -> None

      An extra comment has been changed. 
                
      :param ea: (::ea_t)
      :param line_idx: (int)
      :param cmt: (const char *)



   .. py:method:: item_color_changed(ea: ida_idaapi.ea_t, color: bgcolor_t) -> None

      An item color has been changed. 
                
      :param ea: (::ea_t)
      :param color: (bgcolor_t) if color==DEFCOLOR, the the color is deleted.



   .. py:method:: callee_addr_changed(ea: ida_idaapi.ea_t, callee: ida_idaapi.ea_t) -> None

      Callee address has been updated by the user. 
                
      :param ea: (::ea_t)
      :param callee: (::ea_t)



   .. py:method:: bookmark_changed(index: int, pos: lochist_entry_t const *, desc: str, operation: int) -> None

      Boomarked position changed. 
                
      :param index: (uint32)
      :param pos: (::const lochist_entry_t *)
      :param desc: (::const char *)
      :param operation: (int) 0-added, 1-updated, 2-deleted if desc==nullptr, then the bookmark was deleted.



   .. py:method:: sgr_deleted(start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t, regnum: int) -> None

      The kernel has deleted a segment register value. 
                
      :param start_ea: (::ea_t)
      :param end_ea: (::ea_t)
      :param regnum: (int)



   .. py:method:: adding_segm(s: segment_t *) -> None

      A segment is being created. 
                
      :param s: (segment_t *)



   .. py:method:: func_deleted(func_ea: ida_idaapi.ea_t) -> None

      A function has been deleted. 
                
      :param func_ea: (::ea_t)



   .. py:method:: dirtree_mkdir(dt: dirtree_t *, path: str) -> None

      Dirtree: a directory has been created. 
                
      :param dt: (dirtree_t *)
      :param path: (::const char *)



   .. py:method:: dirtree_rmdir(dt: dirtree_t *, path: str) -> None

      Dirtree: a directory has been deleted. 
                
      :param dt: (dirtree_t *)
      :param path: (::const char *)



   .. py:method:: dirtree_link(dt: dirtree_t *, path: str, link: bool) -> None

      Dirtree: an item has been linked/unlinked. 
                
      :param dt: (dirtree_t *)
      :param path: (::const char *)
      :param link: (::bool)



   .. py:method:: dirtree_move(dt: dirtree_t *, _from: str, to: str) -> None

      Dirtree: a directory or item has been moved. 
                
      :param dt: (dirtree_t *)
      :param to: (::const char *)



   .. py:method:: dirtree_rank(dt: dirtree_t *, path: str, rank: size_t) -> None

      Dirtree: a directory or item rank has been changed. 
                
      :param dt: (dirtree_t *)
      :param path: (::const char *)
      :param rank: (::size_t)



   .. py:method:: dirtree_rminode(dt: dirtree_t *, inode: inode_t) -> None

      Dirtree: an inode became unavailable. 
                
      :param dt: (dirtree_t *)
      :param inode: (inode_t)



   .. py:method:: dirtree_segm_moved(dt: dirtree_t *) -> None

      Dirtree: inodes were changed due to a segment movement or a program rebasing 
                
      :param dt: (dirtree_t *)



   .. py:method:: local_types_changed(ltc: local_type_change_t, ordinal: int, name: str) -> None

      Local types have been changed 
                
      :param ltc: (local_type_change_t)
      :param ordinal: (uint32) 0 means ordinal is unknown
      :param name: (const char *) nullptr means name is unknown



   .. py:method:: lt_udm_created(udtname: str, udm: udm_t) -> None

      local type udt member has been added 
                
      :param udtname: (::const char *)
      :param udm: (::const udm_t *)



   .. py:method:: lt_udm_deleted(udtname: str, udm_tid: tid_t, udm: udm_t) -> None

      local type udt member has been deleted 
                
      :param udtname: (::const char *)
      :param udm_tid: (tid_t)
      :param udm: (::const udm_t *)



   .. py:method:: lt_udm_renamed(udtname: str, udm: udm_t, oldname: str) -> None

      local type udt member has been renamed 
                
      :param udtname: (::const char *)
      :param udm: (::const udm_t *)
      :param oldname: (::const char *)



   .. py:method:: lt_udm_changed(udtname: str, udm_tid: tid_t, udmold: udm_t, udmnew: udm_t) -> None

      local type udt member has been changed 
                
      :param udtname: (::const char *)
      :param udm_tid: (tid_t)
      :param udmold: (::const udm_t *)
      :param udmnew: (::const udm_t *)



   .. py:method:: lt_udt_expanded(udtname: str, udm_tid: tid_t, delta: adiff_t) -> None

      A structure type has been expanded/shrank. 
                
      :param udtname: (::const char *)
      :param udm_tid: (tid_t) the gap was added/removed before this member
      :param delta: (::adiff_t) number of added/removed bytes



   .. py:method:: frame_created(func_ea: ida_idaapi.ea_t) -> None

      A function frame has been created. 
                
      :param func_ea: (::ea_t) idb_event::frame_deleted



   .. py:method:: frame_udm_created(func_ea: ida_idaapi.ea_t, udm: udm_t) -> None

      Frame member has been added. 
                
      :param func_ea: (::ea_t)
      :param udm: (::const udm_t *)



   .. py:method:: frame_udm_deleted(func_ea: ida_idaapi.ea_t, udm_tid: tid_t, udm: udm_t) -> None

      Frame member has been deleted. 
                
      :param func_ea: (::ea_t)
      :param udm_tid: (tid_t)
      :param udm: (::const udm_t *)



   .. py:method:: frame_udm_renamed(func_ea: ida_idaapi.ea_t, udm: udm_t, oldname: str) -> None

      Frame member has been renamed. 
                
      :param func_ea: (::ea_t)
      :param udm: (::const udm_t *)
      :param oldname: (::const char *)



   .. py:method:: frame_udm_changed(func_ea: ida_idaapi.ea_t, udm_tid: tid_t, udmold: udm_t, udmnew: udm_t) -> None

      Frame member has been changed. 
                
      :param func_ea: (::ea_t)
      :param udm_tid: (tid_t)
      :param udmold: (::const udm_t *)
      :param udmnew: (::const udm_t *)



   .. py:method:: frame_expanded(func_ea: ida_idaapi.ea_t, udm_tid: tid_t, delta: adiff_t) -> None

      A frame type has been expanded/shrank. 
                
      :param func_ea: (::ea_t)
      :param udm_tid: (tid_t) the gap was added/removed before this member
      :param delta: (::adiff_t) number of added/removed bytes



   .. py:method:: idasgn_matched_ea(ea: ida_idaapi.ea_t, name: str, lib_name: str) -> None

      A FLIRT match has been found 
                
      :param ea: (::ea_t) the matching address
      :param name: (::const char *) the matched name
      :param lib_name: (::const char *) library name extracted from signature file



   .. py:method:: lt_edm_created(enumname: str, edm: edm_t) -> None

      local type enum member has been added 
                
      :param enumname: (::const char *)
      :param edm: (::const edm_t *)



   .. py:method:: lt_edm_deleted(enumname: str, edm_tid: tid_t, edm: edm_t) -> None

      local type enum member has been deleted 
                
      :param enumname: (::const char *)
      :param edm_tid: (tid_t)
      :param edm: (::const edm_t *)



   .. py:method:: lt_edm_renamed(enumname: str, edm: edm_t, oldname: str) -> None

      local type enum member has been renamed 
                
      :param enumname: (::const char *)
      :param edm: (::const edm_t *)
      :param oldname: (::const char *)



   .. py:method:: lt_edm_changed(enumname: str, edm_tid: tid_t, edmold: edm_t, edmnew: edm_t) -> None

      local type enum member has been changed 
                
      :param enumname: (::const char *)
      :param edm_tid: (tid_t)
      :param edmold: (::const edm_t *)
      :param edmnew: (::const edm_t *)



   .. py:method:: local_type_renamed(ordinal: int, oldname: str, newname: str) -> None

      Local type has been renamed 
                
      :param ordinal: (uint32) 0 means ordinal is unknown
      :param oldname: (const char *) nullptr means name is unknown
      :param newname: (const char *) nullptr means name is unknown



.. py:function:: get_idb_notifier_addr(arg1: PyObject *) -> PyObject *

.. py:function:: get_idb_notifier_ud_addr(hooks: IDB_Hooks) -> PyObject *


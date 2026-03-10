ida_hexrays
===========

.. py:module:: ida_hexrays

.. autoapi-nested-parse::

   There are 2 representations of the binary code in the decompiler:

   Hex-Rays Decompiler project Copyright (c) 1990-2025 Hex-Rays ALL RIGHTS RESERVED.

   * microcode: processor instructions are translated into it and then the decompiler optimizes and transforms it
   * ctree: ctree is built from the optimized microcode and represents AST-like tree with C statements and expressions. It can be printed as C code.


   Microcode is represented by the following classes:
   * mba_t keeps general info about the decompiled code and array of basic blocks. usually mba_t is named 'mba'
   * mblock_t a basic block. includes list of instructions
   * minsn_t an instruction. contains 3 operands: left, right, and destination
   * mop_t an operand. depending on its type may hold various info like a number, register, stack variable, etc.
   * mlist_t list of memory or register locations; can hold vast areas of memory and multiple registers. this class is used very extensively in the decompiler. it may represent list of locations accessed by an instruction or even an entire basic block. it is also used as argument of many functions. for example, there is a function that searches for an instruction that refers to a mlist_t.


   See [https://hex-rays.com/blog/microcode-in-pictures](https://hex-rays.com/blog/microcode-in-pictures) for a few pictures.
   Ctree is represented by:
   * cfunc_t keeps general info about the decompiled code, including a pointer to mba_t. deleting cfunc_t will delete mba_t too (however, decompiler returns cfuncptr_t, which is a reference counting object and deletes the underlying function as soon as all references to it go out of scope). cfunc_t has 'body', which represents the decompiled function body as cinsn_t.
   * cinsn_t a C statement. can be a compound statement or any other legal C statements (like if, for, while, return, expression-statement, etc). depending on the statement type has pointers to additional info. for example, the 'if' statement has poiner to cif_t, which holds the 'if' condition, 'then' branch, and optionally 'else' branch. Please note that despite of the name cinsn_t we say "statements", not "instructions". For us instructions are part of microcode, not ctree.
   * cexpr_t a C expression. is used as part of a C statement, when necessary. cexpr_t has 'type' field, which keeps the expression type.
   * citem_t a base class for cinsn_t and cexpr_t, holds common info like the address, label, and opcode.
   * cnumber_t a constant 64-bit number. in addition to its value also holds information how to represent it: decimal, hex, or as a symbolic constant (enum member). please note that numbers are represented by another class (mnumber_t) in microcode.


   See [https://hex-rays.com/blog/hex-rays-decompiler-primer](https://hex-rays.com/blog/hex-rays-decompiler-primer) for more pictures and more details.
   Both microcode and ctree use the following class:
   * lvar_t a local variable. may represent a stack or register variable. a variable has a name, type, location, etc. the list of variables is stored in mba->vars.
   * lvar_locator_t holds a variable location (vdloc_t) and its definition address.
   * vdloc_t describes a variable location, like a register number, a stack offset, or, in complex cases, can be a mix of register and stack locations. very similar to argloc_t, which is used in ida. the differences between argloc_t and vdloc_t are:
   * vdloc_t never uses ARGLOC_REG2
   * vdloc_t uses micro register numbers instead of processor register numbers
   * the stack offsets are never negative in vdloc_t, while in argloc_t there can be negative offsets




   The above are the most important classes in this header file. There are many auxiliary classes, please see their definitions in the header file.
   See also the description of Virtual Machine used by Microcode. 
       



Attributes
----------

.. autoapisummary::

   ida_hexrays.MAX_SUPPORTED_STACK_SIZE
   ida_hexrays.MAX_VLR_SIZE
   ida_hexrays.CMP_NZ
   ida_hexrays.CMP_Z
   ida_hexrays.CMP_AE
   ida_hexrays.CMP_B
   ida_hexrays.CMP_A
   ida_hexrays.CMP_BE
   ida_hexrays.CMP_GT
   ida_hexrays.CMP_GE
   ida_hexrays.CMP_LT
   ida_hexrays.CMP_LE
   ida_hexrays.cvar
   ida_hexrays.MAX_VLR_VALUE
   ida_hexrays.MAX_VLR_SVALUE
   ida_hexrays.MIN_VLR_SVALUE
   ida_hexrays.MERR_OK
   ida_hexrays.MERR_BLOCK
   ida_hexrays.MERR_INTERR
   ida_hexrays.MERR_INSN
   ida_hexrays.MERR_MEM
   ida_hexrays.MERR_BADBLK
   ida_hexrays.MERR_BADSP
   ida_hexrays.MERR_PROLOG
   ida_hexrays.MERR_SWITCH
   ida_hexrays.MERR_EXCEPTION
   ida_hexrays.MERR_HUGESTACK
   ida_hexrays.MERR_LVARS
   ida_hexrays.MERR_BITNESS
   ida_hexrays.MERR_BADCALL
   ida_hexrays.MERR_BADFRAME
   ida_hexrays.MERR_UNKTYPE
   ida_hexrays.MERR_BADIDB
   ida_hexrays.MERR_SIZEOF
   ida_hexrays.MERR_REDO
   ida_hexrays.MERR_CANCELED
   ida_hexrays.MERR_RECDEPTH
   ida_hexrays.MERR_OVERLAP
   ida_hexrays.MERR_PARTINIT
   ida_hexrays.MERR_COMPLEX
   ida_hexrays.MERR_LICENSE
   ida_hexrays.MERR_ONLY32
   ida_hexrays.MERR_ONLY64
   ida_hexrays.MERR_BUSY
   ida_hexrays.MERR_FARPTR
   ida_hexrays.MERR_EXTERN
   ida_hexrays.MERR_FUNCSIZE
   ida_hexrays.MERR_BADRANGES
   ida_hexrays.MERR_BADARCH
   ida_hexrays.MERR_DSLOT
   ida_hexrays.MERR_STOP
   ida_hexrays.MERR_CLOUD
   ida_hexrays.MERR_EMULATOR
   ida_hexrays.MERR_MAX_ERR
   ida_hexrays.MERR_LOOP
   ida_hexrays.m_nop
   ida_hexrays.m_stx
   ida_hexrays.m_ldx
   ida_hexrays.m_ldc
   ida_hexrays.m_mov
   ida_hexrays.m_neg
   ida_hexrays.m_lnot
   ida_hexrays.m_bnot
   ida_hexrays.m_xds
   ida_hexrays.m_xdu
   ida_hexrays.m_low
   ida_hexrays.m_high
   ida_hexrays.m_add
   ida_hexrays.m_sub
   ida_hexrays.m_mul
   ida_hexrays.m_udiv
   ida_hexrays.m_sdiv
   ida_hexrays.m_umod
   ida_hexrays.m_smod
   ida_hexrays.m_or
   ida_hexrays.m_and
   ida_hexrays.m_xor
   ida_hexrays.m_shl
   ida_hexrays.m_shr
   ida_hexrays.m_sar
   ida_hexrays.m_cfadd
   ida_hexrays.m_ofadd
   ida_hexrays.m_cfshl
   ida_hexrays.m_cfshr
   ida_hexrays.m_sets
   ida_hexrays.m_seto
   ida_hexrays.m_setp
   ida_hexrays.m_setnz
   ida_hexrays.m_setz
   ida_hexrays.m_setae
   ida_hexrays.m_setb
   ida_hexrays.m_seta
   ida_hexrays.m_setbe
   ida_hexrays.m_setg
   ida_hexrays.m_setge
   ida_hexrays.m_setl
   ida_hexrays.m_setle
   ida_hexrays.m_jcnd
   ida_hexrays.m_jnz
   ida_hexrays.m_jz
   ida_hexrays.m_jae
   ida_hexrays.m_jb
   ida_hexrays.m_ja
   ida_hexrays.m_jbe
   ida_hexrays.m_jg
   ida_hexrays.m_jge
   ida_hexrays.m_jl
   ida_hexrays.m_jle
   ida_hexrays.m_jtbl
   ida_hexrays.m_ijmp
   ida_hexrays.m_goto
   ida_hexrays.m_call
   ida_hexrays.m_icall
   ida_hexrays.m_ret
   ida_hexrays.m_push
   ida_hexrays.m_pop
   ida_hexrays.m_und
   ida_hexrays.m_ext
   ida_hexrays.m_f2i
   ida_hexrays.m_f2u
   ida_hexrays.m_i2f
   ida_hexrays.m_u2f
   ida_hexrays.m_f2f
   ida_hexrays.m_fneg
   ida_hexrays.m_fadd
   ida_hexrays.m_fsub
   ida_hexrays.m_fmul
   ida_hexrays.m_fdiv
   ida_hexrays.MUST_ACCESS
   ida_hexrays.MAY_ACCESS
   ida_hexrays.MAYMUST_ACCESS_MASK
   ida_hexrays.ONE_ACCESS_TYPE
   ida_hexrays.INCLUDE_SPOILED_REGS
   ida_hexrays.EXCLUDE_PASS_REGS
   ida_hexrays.FULL_XDSU
   ida_hexrays.WITH_ASSERTS
   ida_hexrays.EXCLUDE_VOLATILE
   ida_hexrays.INCLUDE_UNUSED_SRC
   ida_hexrays.INCLUDE_DEAD_RETREGS
   ida_hexrays.INCLUDE_RESTRICTED
   ida_hexrays.CALL_SPOILS_ONLY_ARGS
   ida_hexrays.mr_none
   ida_hexrays.mr_cf
   ida_hexrays.mr_zf
   ida_hexrays.mr_sf
   ida_hexrays.mr_of
   ida_hexrays.mr_pf
   ida_hexrays.cc_count
   ida_hexrays.mr_cc
   ida_hexrays.mr_first
   ida_hexrays.NF_FIXED
   ida_hexrays.NF_NEGDONE
   ida_hexrays.NF_BINVDONE
   ida_hexrays.NF_NEGATE
   ida_hexrays.NF_BITNOT
   ida_hexrays.NF_VALID
   ida_hexrays.GUESSED_NONE
   ida_hexrays.GUESSED_WEAK
   ida_hexrays.GUESSED_FUNC
   ida_hexrays.GUESSED_DATA
   ida_hexrays.TS_NOELL
   ida_hexrays.TS_SHRINK
   ida_hexrays.TS_DONTREF
   ida_hexrays.TS_MASK
   ida_hexrays.SVW_INT
   ida_hexrays.SVW_FLOAT
   ida_hexrays.SVW_SOFT
   ida_hexrays.LVINF_KEEP
   ida_hexrays.LVINF_SPLIT
   ida_hexrays.LVINF_NOPTR
   ida_hexrays.LVINF_NOMAP
   ida_hexrays.LVINF_UNUSED
   ida_hexrays.ULV_PRECISE_DEFEA
   ida_hexrays.MLI_NAME
   ida_hexrays.MLI_TYPE
   ida_hexrays.MLI_CMT
   ida_hexrays.MLI_SET_FLAGS
   ida_hexrays.MLI_CLR_FLAGS
   ida_hexrays.bitset_width
   ida_hexrays.bitset_align
   ida_hexrays.bitset_shift
   ida_hexrays.mop_z
   ida_hexrays.mop_r
   ida_hexrays.mop_n
   ida_hexrays.mop_str
   ida_hexrays.mop_d
   ida_hexrays.mop_S
   ida_hexrays.mop_v
   ida_hexrays.mop_b
   ida_hexrays.mop_f
   ida_hexrays.mop_l
   ida_hexrays.mop_a
   ida_hexrays.mop_h
   ida_hexrays.mop_c
   ida_hexrays.mop_fn
   ida_hexrays.mop_p
   ida_hexrays.mop_sc
   ida_hexrays.NOSIZE
   ida_hexrays.SHINS_NUMADDR
   ida_hexrays.SHINS_VALNUM
   ida_hexrays.SHINS_SHORT
   ida_hexrays.SHINS_LDXEA
   ida_hexrays.NO_SIDEFF
   ida_hexrays.WITH_SIDEFF
   ida_hexrays.ONLY_SIDEFF
   ida_hexrays.ANY_REGSIZE
   ida_hexrays.ANY_FPSIZE
   ida_hexrays.OPROP_IMPDONE
   ida_hexrays.OPROP_UDT
   ida_hexrays.OPROP_FLOAT
   ida_hexrays.OPROP_CCFLAGS
   ida_hexrays.OPROP_UDEFVAL
   ida_hexrays.OPROP_LOWADDR
   ida_hexrays.OPROP_ABI
   ida_hexrays.ROLE_UNK
   ida_hexrays.ROLE_EMPTY
   ida_hexrays.ROLE_MEMSET
   ida_hexrays.ROLE_MEMSET32
   ida_hexrays.ROLE_MEMSET64
   ida_hexrays.ROLE_MEMCPY
   ida_hexrays.ROLE_STRCPY
   ida_hexrays.ROLE_STRLEN
   ida_hexrays.ROLE_STRCAT
   ida_hexrays.ROLE_TAIL
   ida_hexrays.ROLE_BUG
   ida_hexrays.ROLE_ALLOCA
   ida_hexrays.ROLE_BSWAP
   ida_hexrays.ROLE_PRESENT
   ida_hexrays.ROLE_CONTAINING_RECORD
   ida_hexrays.ROLE_FASTFAIL
   ida_hexrays.ROLE_READFLAGS
   ida_hexrays.ROLE_IS_MUL_OK
   ida_hexrays.ROLE_SATURATED_MUL
   ida_hexrays.ROLE_BITTEST
   ida_hexrays.ROLE_BITTESTANDSET
   ida_hexrays.ROLE_BITTESTANDRESET
   ida_hexrays.ROLE_BITTESTANDCOMPLEMENT
   ida_hexrays.ROLE_VA_ARG
   ida_hexrays.ROLE_VA_COPY
   ida_hexrays.ROLE_VA_START
   ida_hexrays.ROLE_VA_END
   ida_hexrays.ROLE_ROL
   ida_hexrays.ROLE_ROR
   ida_hexrays.ROLE_CFSUB3
   ida_hexrays.ROLE_OFSUB3
   ida_hexrays.ROLE_ABS
   ida_hexrays.ROLE_3WAYCMP0
   ida_hexrays.ROLE_3WAYCMP1
   ida_hexrays.ROLE_WMEMCPY
   ida_hexrays.ROLE_WMEMSET
   ida_hexrays.ROLE_WCSCPY
   ida_hexrays.ROLE_WCSLEN
   ida_hexrays.ROLE_WCSCAT
   ida_hexrays.ROLE_SSE_CMP4
   ida_hexrays.ROLE_SSE_CMP8
   ida_hexrays.FUNC_NAME_MEMCPY
   ida_hexrays.FUNC_NAME_WMEMCPY
   ida_hexrays.FUNC_NAME_MEMSET
   ida_hexrays.FUNC_NAME_WMEMSET
   ida_hexrays.FUNC_NAME_MEMSET32
   ida_hexrays.FUNC_NAME_MEMSET64
   ida_hexrays.FUNC_NAME_STRCPY
   ida_hexrays.FUNC_NAME_WCSCPY
   ida_hexrays.FUNC_NAME_STRLEN
   ida_hexrays.FUNC_NAME_WCSLEN
   ida_hexrays.FUNC_NAME_STRCAT
   ida_hexrays.FUNC_NAME_WCSCAT
   ida_hexrays.FUNC_NAME_TAIL
   ida_hexrays.FUNC_NAME_VA_ARG
   ida_hexrays.FUNC_NAME_EMPTY
   ida_hexrays.FUNC_NAME_PRESENT
   ida_hexrays.FUNC_NAME_CONTAINING_RECORD
   ida_hexrays.FUNC_NAME_MORESTACK
   ida_hexrays.FCI_PROP
   ida_hexrays.FCI_DEAD
   ida_hexrays.FCI_FINAL
   ida_hexrays.FCI_NORET
   ida_hexrays.FCI_PURE
   ida_hexrays.FCI_NOSIDE
   ida_hexrays.FCI_SPLOK
   ida_hexrays.FCI_HASCALL
   ida_hexrays.FCI_HASFMT
   ida_hexrays.FCI_EXPLOCS
   ida_hexrays.CHF_INITED
   ida_hexrays.CHF_REPLACED
   ida_hexrays.CHF_OVER
   ida_hexrays.CHF_FAKE
   ida_hexrays.CHF_PASSTHRU
   ida_hexrays.CHF_TERM
   ida_hexrays.SIZEOF_BLOCK_CHAINS
   ida_hexrays.GCA_EMPTY
   ida_hexrays.GCA_SPEC
   ida_hexrays.GCA_ALLOC
   ida_hexrays.GCA_NALLOC
   ida_hexrays.GCA_OFIRST
   ida_hexrays.GCA_OLAST
   ida_hexrays.IPROP_OPTIONAL
   ida_hexrays.IPROP_PERSIST
   ida_hexrays.IPROP_WILDMATCH
   ida_hexrays.IPROP_CLNPOP
   ida_hexrays.IPROP_FPINSN
   ida_hexrays.IPROP_FARCALL
   ida_hexrays.IPROP_TAILCALL
   ida_hexrays.IPROP_ASSERT
   ida_hexrays.IPROP_SPLIT
   ida_hexrays.IPROP_SPLIT1
   ida_hexrays.IPROP_SPLIT2
   ida_hexrays.IPROP_SPLIT4
   ida_hexrays.IPROP_SPLIT8
   ida_hexrays.IPROP_COMBINED
   ida_hexrays.IPROP_EXTSTX
   ida_hexrays.IPROP_IGNLOWSRC
   ida_hexrays.IPROP_INV_JX
   ida_hexrays.IPROP_WAS_NORET
   ida_hexrays.IPROP_MULTI_MOV
   ida_hexrays.IPROP_DONT_PROP
   ida_hexrays.IPROP_DONT_COMB
   ida_hexrays.IPROP_MBARRIER
   ida_hexrays.IPROP_UNMERGED
   ida_hexrays.IPROP_UNPAIRED
   ida_hexrays.OPTI_ADDREXPRS
   ida_hexrays.OPTI_MINSTKREF
   ida_hexrays.OPTI_COMBINSNS
   ida_hexrays.OPTI_NO_LDXOPT
   ida_hexrays.OPTI_NO_VALRNG
   ida_hexrays.EQ_IGNSIZE
   ida_hexrays.EQ_IGNCODE
   ida_hexrays.EQ_CMPDEST
   ida_hexrays.EQ_OPTINSN
   ida_hexrays.NORET_IGNORE_WAS_NORET_ICALL
   ida_hexrays.NORET_FORBID_ANALYSIS
   ida_hexrays.BLT_NONE
   ida_hexrays.BLT_STOP
   ida_hexrays.BLT_0WAY
   ida_hexrays.BLT_1WAY
   ida_hexrays.BLT_2WAY
   ida_hexrays.BLT_NWAY
   ida_hexrays.BLT_XTRN
   ida_hexrays.MBL_PRIV
   ida_hexrays.MBL_NONFAKE
   ida_hexrays.MBL_FAKE
   ida_hexrays.MBL_GOTO
   ida_hexrays.MBL_TCAL
   ida_hexrays.MBL_PUSH
   ida_hexrays.MBL_DMT64
   ida_hexrays.MBL_COMB
   ida_hexrays.MBL_PROP
   ida_hexrays.MBL_DEAD
   ida_hexrays.MBL_LIST
   ida_hexrays.MBL_INCONST
   ida_hexrays.MBL_CALL
   ida_hexrays.MBL_BACKPROP
   ida_hexrays.MBL_NORET
   ida_hexrays.MBL_DSLOT
   ida_hexrays.MBL_VALRANGES
   ida_hexrays.MBL_KEEP
   ida_hexrays.MBL_INLINED
   ida_hexrays.MBL_EXTFRAME
   ida_hexrays.FD_BACKWARD
   ida_hexrays.FD_FORWARD
   ida_hexrays.FD_USE
   ida_hexrays.FD_DEF
   ida_hexrays.FD_DIRTY
   ida_hexrays.VR_AT_START
   ida_hexrays.VR_AT_END
   ida_hexrays.VR_EXACT
   ida_hexrays.WARN_VARARG_REGS
   ida_hexrays.WARN_ILL_PURGED
   ida_hexrays.WARN_ILL_FUNCTYPE
   ida_hexrays.WARN_VARARG_TCAL
   ida_hexrays.WARN_VARARG_NOSTK
   ida_hexrays.WARN_VARARG_MANY
   ida_hexrays.WARN_ADDR_OUTARGS
   ida_hexrays.WARN_DEP_UNK_CALLS
   ida_hexrays.WARN_ILL_ELLIPSIS
   ida_hexrays.WARN_GUESSED_TYPE
   ida_hexrays.WARN_EXP_LINVAR
   ida_hexrays.WARN_WIDEN_CHAINS
   ida_hexrays.WARN_BAD_PURGED
   ida_hexrays.WARN_CBUILD_LOOPS
   ida_hexrays.WARN_NO_SAVE_REST
   ida_hexrays.WARN_ODD_INPUT_REG
   ida_hexrays.WARN_ODD_ADDR_USE
   ida_hexrays.WARN_MUST_RET_FP
   ida_hexrays.WARN_ILL_FPU_STACK
   ida_hexrays.WARN_SELFREF_PROP
   ida_hexrays.WARN_WOULD_OVERLAP
   ida_hexrays.WARN_ARRAY_INARG
   ida_hexrays.WARN_MAX_ARGS
   ida_hexrays.WARN_BAD_FIELD_TYPE
   ida_hexrays.WARN_WRITE_CONST
   ida_hexrays.WARN_BAD_RETVAR
   ida_hexrays.WARN_FRAG_LVAR
   ida_hexrays.WARN_HUGE_STKOFF
   ida_hexrays.WARN_UNINITED_REG
   ida_hexrays.WARN_FIXED_INSN
   ida_hexrays.WARN_WRONG_VA_OFF
   ida_hexrays.WARN_CR_NOFIELD
   ida_hexrays.WARN_CR_BADOFF
   ida_hexrays.WARN_BAD_STROFF
   ida_hexrays.WARN_BAD_VARSIZE
   ida_hexrays.WARN_UNSUPP_REG
   ida_hexrays.WARN_UNALIGNED_ARG
   ida_hexrays.WARN_BAD_STD_TYPE
   ida_hexrays.WARN_BAD_CALL_SP
   ida_hexrays.WARN_MISSED_SWITCH
   ida_hexrays.WARN_BAD_SP
   ida_hexrays.WARN_BAD_STKPNT
   ida_hexrays.WARN_UNDEF_LVAR
   ida_hexrays.WARN_JUMPOUT
   ida_hexrays.WARN_BAD_VALRNG
   ida_hexrays.WARN_BAD_SHADOW
   ida_hexrays.WARN_OPT_VALRNG
   ida_hexrays.WARN_RET_LOCREF
   ida_hexrays.WARN_BAD_MAPDST
   ida_hexrays.WARN_BAD_INSN
   ida_hexrays.WARN_ODD_ABI
   ida_hexrays.WARN_UNBALANCED_STACK
   ida_hexrays.WARN_OPT_VALRNG2
   ida_hexrays.WARN_OPT_VALRNG3
   ida_hexrays.WARN_OPT_USELESS_JCND
   ida_hexrays.WARN_SUBFRAME_OVERFLOW
   ida_hexrays.WARN_OPT_VALRNG4
   ida_hexrays.WARN_MAX
   ida_hexrays.MMAT_ZERO
   ida_hexrays.MMAT_GENERATED
   ida_hexrays.MMAT_PREOPTIMIZED
   ida_hexrays.MMAT_LOCOPT
   ida_hexrays.MMAT_CALLS
   ida_hexrays.MMAT_GLBOPT1
   ida_hexrays.MMAT_GLBOPT2
   ida_hexrays.MMAT_GLBOPT3
   ida_hexrays.MMAT_LVARS
   ida_hexrays.MMIDX_GLBLOW
   ida_hexrays.MMIDX_LVARS
   ida_hexrays.MMIDX_RETADDR
   ida_hexrays.MMIDX_SHADOW
   ida_hexrays.MMIDX_ARGS
   ida_hexrays.MMIDX_GLBHIGH
   ida_hexrays.MBA_PRCDEFS
   ida_hexrays.MBA_NOFUNC
   ida_hexrays.MBA_PATTERN
   ida_hexrays.MBA_LOADED
   ida_hexrays.MBA_RETFP
   ida_hexrays.MBA_SPLINFO
   ida_hexrays.MBA_PASSREGS
   ida_hexrays.MBA_THUNK
   ida_hexrays.MBA_CMNSTK
   ida_hexrays.MBA_PREOPT
   ida_hexrays.MBA_CMBBLK
   ida_hexrays.MBA_ASRTOK
   ida_hexrays.MBA_CALLS
   ida_hexrays.MBA_ASRPROP
   ida_hexrays.MBA_SAVRST
   ida_hexrays.MBA_RETREF
   ida_hexrays.MBA_GLBOPT
   ida_hexrays.MBA_LVARS0
   ida_hexrays.MBA_LVARS1
   ida_hexrays.MBA_DELPAIRS
   ida_hexrays.MBA_CHVARS
   ida_hexrays.MBA_SHORT
   ida_hexrays.MBA_COLGDL
   ida_hexrays.MBA_INSGDL
   ida_hexrays.MBA_NICE
   ida_hexrays.MBA_REFINE
   ida_hexrays.MBA_WINGR32
   ida_hexrays.MBA_NUMADDR
   ida_hexrays.MBA_VALNUM
   ida_hexrays.MBA_INITIAL_FLAGS
   ida_hexrays.MBA2_LVARNAMES_OK
   ida_hexrays.MBA2_LVARS_RENAMED
   ida_hexrays.MBA2_OVER_CHAINS
   ida_hexrays.MBA2_VALRNG_DONE
   ida_hexrays.MBA2_IS_CTR
   ida_hexrays.MBA2_IS_DTR
   ida_hexrays.MBA2_ARGIDX_OK
   ida_hexrays.MBA2_NO_DUP_CALLS
   ida_hexrays.MBA2_NO_DUP_LVARS
   ida_hexrays.MBA2_UNDEF_RETVAR
   ida_hexrays.MBA2_ARGIDX_SORTED
   ida_hexrays.MBA2_CODE16_BIT
   ida_hexrays.MBA2_STACK_RETVAL
   ida_hexrays.MBA2_HAS_OUTLINES
   ida_hexrays.MBA2_NO_FRAME
   ida_hexrays.MBA2_PROP_COMPLEX
   ida_hexrays.MBA2_DONT_VERIFY
   ida_hexrays.MBA2_INITIAL_FLAGS
   ida_hexrays.MBA2_ALL_FLAGS
   ida_hexrays.NALT_VD
   ida_hexrays.LOCOPT_ALL
   ida_hexrays.LOCOPT_REFINE
   ida_hexrays.LOCOPT_REFINE2
   ida_hexrays.ACFL_LOCOPT
   ida_hexrays.ACFL_BLKOPT
   ida_hexrays.ACFL_GLBPROP
   ida_hexrays.ACFL_GLBDEL
   ida_hexrays.ACFL_GUESS
   ida_hexrays.CPBLK_FAST
   ida_hexrays.CPBLK_MINREF
   ida_hexrays.CPBLK_OPTJMP
   ida_hexrays.INLINE_EXTFRAME
   ida_hexrays.INLINE_DONTCOPY
   ida_hexrays.GC_REGS_AND_STKVARS
   ida_hexrays.GC_ASR
   ida_hexrays.GC_XDSU
   ida_hexrays.GC_END
   ida_hexrays.GC_DIRTY_ALL
   ida_hexrays.OPF_REUSE
   ida_hexrays.OPF_NEW_WINDOW
   ida_hexrays.OPF_REUSE_ACTIVE
   ida_hexrays.OPF_NO_WAIT
   ida_hexrays.OPF_WINDOW_MGMT_MASK
   ida_hexrays.VDRUN_NEWFILE
   ida_hexrays.VDRUN_APPEND
   ida_hexrays.VDRUN_ONLYNEW
   ida_hexrays.VDRUN_SILENT
   ida_hexrays.VDRUN_SENDIDB
   ida_hexrays.VDRUN_MAYSTOP
   ida_hexrays.VDRUN_CMDLINE
   ida_hexrays.VDRUN_STATS
   ida_hexrays.VDRUN_LUMINA
   ida_hexrays.VDRUN_PERF
   ida_hexrays.GCO_STK
   ida_hexrays.GCO_REG
   ida_hexrays.GCO_USE
   ida_hexrays.GCO_DEF
   ida_hexrays.cot_empty
   ida_hexrays.cot_comma
   ida_hexrays.cot_asg
   ida_hexrays.cot_asgbor
   ida_hexrays.cot_asgxor
   ida_hexrays.cot_asgband
   ida_hexrays.cot_asgadd
   ida_hexrays.cot_asgsub
   ida_hexrays.cot_asgmul
   ida_hexrays.cot_asgsshr
   ida_hexrays.cot_asgushr
   ida_hexrays.cot_asgshl
   ida_hexrays.cot_asgsdiv
   ida_hexrays.cot_asgudiv
   ida_hexrays.cot_asgsmod
   ida_hexrays.cot_asgumod
   ida_hexrays.cot_tern
   ida_hexrays.cot_lor
   ida_hexrays.cot_land
   ida_hexrays.cot_bor
   ida_hexrays.cot_xor
   ida_hexrays.cot_band
   ida_hexrays.cot_eq
   ida_hexrays.cot_ne
   ida_hexrays.cot_sge
   ida_hexrays.cot_uge
   ida_hexrays.cot_sle
   ida_hexrays.cot_ule
   ida_hexrays.cot_sgt
   ida_hexrays.cot_ugt
   ida_hexrays.cot_slt
   ida_hexrays.cot_ult
   ida_hexrays.cot_sshr
   ida_hexrays.cot_ushr
   ida_hexrays.cot_shl
   ida_hexrays.cot_add
   ida_hexrays.cot_sub
   ida_hexrays.cot_mul
   ida_hexrays.cot_sdiv
   ida_hexrays.cot_udiv
   ida_hexrays.cot_smod
   ida_hexrays.cot_umod
   ida_hexrays.cot_fadd
   ida_hexrays.cot_fsub
   ida_hexrays.cot_fmul
   ida_hexrays.cot_fdiv
   ida_hexrays.cot_fneg
   ida_hexrays.cot_neg
   ida_hexrays.cot_cast
   ida_hexrays.cot_lnot
   ida_hexrays.cot_bnot
   ida_hexrays.cot_ptr
   ida_hexrays.cot_ref
   ida_hexrays.cot_postinc
   ida_hexrays.cot_postdec
   ida_hexrays.cot_preinc
   ida_hexrays.cot_predec
   ida_hexrays.cot_call
   ida_hexrays.cot_idx
   ida_hexrays.cot_memref
   ida_hexrays.cot_memptr
   ida_hexrays.cot_num
   ida_hexrays.cot_fnum
   ida_hexrays.cot_str
   ida_hexrays.cot_obj
   ida_hexrays.cot_var
   ida_hexrays.cot_insn
   ida_hexrays.cot_sizeof
   ida_hexrays.cot_helper
   ida_hexrays.cot_type
   ida_hexrays.cot_last
   ida_hexrays.cit_empty
   ida_hexrays.cit_block
   ida_hexrays.cit_expr
   ida_hexrays.cit_if
   ida_hexrays.cit_for
   ida_hexrays.cit_while
   ida_hexrays.cit_do
   ida_hexrays.cit_switch
   ida_hexrays.cit_break
   ida_hexrays.cit_continue
   ida_hexrays.cit_return
   ida_hexrays.cit_goto
   ida_hexrays.cit_asm
   ida_hexrays.cit_try
   ida_hexrays.cit_throw
   ida_hexrays.cit_end
   ida_hexrays.CMAT_ZERO
   ida_hexrays.CMAT_BUILT
   ida_hexrays.CMAT_TRANS1
   ida_hexrays.CMAT_NICE
   ida_hexrays.CMAT_TRANS2
   ida_hexrays.CMAT_CPA
   ida_hexrays.CMAT_TRANS3
   ida_hexrays.CMAT_CASTED
   ida_hexrays.CMAT_FINAL
   ida_hexrays.ITP_EMPTY
   ida_hexrays.ITP_ARG1
   ida_hexrays.ITP_ARG64
   ida_hexrays.ITP_BRACE1
   ida_hexrays.ITP_INNER_LAST
   ida_hexrays.ITP_ASM
   ida_hexrays.ITP_ELSE
   ida_hexrays.ITP_DO
   ida_hexrays.ITP_SEMI
   ida_hexrays.ITP_CURLY1
   ida_hexrays.ITP_CURLY2
   ida_hexrays.ITP_BRACE2
   ida_hexrays.ITP_COLON
   ida_hexrays.ITP_BLOCK1
   ida_hexrays.ITP_BLOCK2
   ida_hexrays.ITP_TRY
   ida_hexrays.ITP_CASE
   ida_hexrays.ITP_SIGN
   ida_hexrays.RETRIEVE_ONCE
   ida_hexrays.RETRIEVE_ALWAYS
   ida_hexrays.EXFL_CPADONE
   ida_hexrays.EXFL_LVALUE
   ida_hexrays.EXFL_FPOP
   ida_hexrays.EXFL_ALONE
   ida_hexrays.EXFL_CSTR
   ida_hexrays.EXFL_PARTIAL
   ida_hexrays.EXFL_UNDEF
   ida_hexrays.EXFL_JUMPOUT
   ida_hexrays.EXFL_VFTABLE
   ida_hexrays.EXFL_ALL
   ida_hexrays.CALC_CURLY_BRACES
   ida_hexrays.NO_CURLY_BRACES
   ida_hexrays.USE_CURLY_BRACES
   ida_hexrays.CFL_FINAL
   ida_hexrays.CFL_HELPER
   ida_hexrays.CFL_NORET
   ida_hexrays.CV_FAST
   ida_hexrays.CV_PRUNE
   ida_hexrays.CV_PARENTS
   ida_hexrays.CV_POST
   ida_hexrays.CV_RESTART
   ida_hexrays.CV_INSNS
   ida_hexrays.ANCHOR_INDEX
   ida_hexrays.ANCHOR_MASK
   ida_hexrays.ANCHOR_CITEM
   ida_hexrays.ANCHOR_LVAR
   ida_hexrays.ANCHOR_ITP
   ida_hexrays.ANCHOR_BLKCMT
   ida_hexrays.VDI_NONE
   ida_hexrays.VDI_EXPR
   ida_hexrays.VDI_LVAR
   ida_hexrays.VDI_FUNC
   ida_hexrays.VDI_TAIL
   ida_hexrays.GLN_CURRENT
   ida_hexrays.GLN_GOTO_TARGET
   ida_hexrays.GLN_ALL
   ida_hexrays.FORBID_UNUSED_LABELS
   ida_hexrays.ALLOW_UNUSED_LABELS
   ida_hexrays.CIT_COLLAPSED
   ida_hexrays.CFS_BOUNDS
   ida_hexrays.CFS_TEXT
   ida_hexrays.CFS_LVARS_HIDDEN
   ida_hexrays.CFS_LOCKED
   ida_hexrays.DECOMP_NO_WAIT
   ida_hexrays.DECOMP_NO_CACHE
   ida_hexrays.DECOMP_NO_FRAME
   ida_hexrays.DECOMP_WARNINGS
   ida_hexrays.DECOMP_ALL_BLKS
   ida_hexrays.DECOMP_NO_HIDE
   ida_hexrays.DECOMP_GXREFS_DEFLT
   ida_hexrays.DECOMP_GXREFS_NOUPD
   ida_hexrays.DECOMP_GXREFS_FORCE
   ida_hexrays.DECOMP_VOID_MBA
   ida_hexrays.DECOMP_OUTLINE
   ida_hexrays.hxe_flowchart
   ida_hexrays.hxe_stkpnts
   ida_hexrays.hxe_prolog
   ida_hexrays.hxe_microcode
   ida_hexrays.hxe_preoptimized
   ida_hexrays.hxe_locopt
   ida_hexrays.hxe_prealloc
   ida_hexrays.hxe_glbopt
   ida_hexrays.hxe_pre_structural
   ida_hexrays.hxe_structural
   ida_hexrays.hxe_maturity
   ida_hexrays.hxe_interr
   ida_hexrays.hxe_combine
   ida_hexrays.hxe_print_func
   ida_hexrays.hxe_func_printed
   ida_hexrays.hxe_resolve_stkaddrs
   ida_hexrays.hxe_build_callinfo
   ida_hexrays.hxe_callinfo_built
   ida_hexrays.hxe_calls_done
   ida_hexrays.hxe_begin_inlining
   ida_hexrays.hxe_inlining_func
   ida_hexrays.hxe_inlined_func
   ida_hexrays.hxe_collect_warnings
   ida_hexrays.hxe_open_pseudocode
   ida_hexrays.hxe_switch_pseudocode
   ida_hexrays.hxe_refresh_pseudocode
   ida_hexrays.hxe_close_pseudocode
   ida_hexrays.hxe_keyboard
   ida_hexrays.hxe_right_click
   ida_hexrays.hxe_double_click
   ida_hexrays.hxe_curpos
   ida_hexrays.hxe_create_hint
   ida_hexrays.hxe_text_ready
   ida_hexrays.hxe_populating_popup
   ida_hexrays.lxe_lvar_name_changed
   ida_hexrays.lxe_lvar_type_changed
   ida_hexrays.lxe_lvar_cmt_changed
   ida_hexrays.lxe_lvar_mapping_changed
   ida_hexrays.hxe_cmt_changed
   ida_hexrays.hxe_mba_maturity
   ida_hexrays.USE_KEYBOARD
   ida_hexrays.USE_MOUSE
   ida_hexrays.HEXRAYS_API_MAGIC
   ida_hexrays.CMT_NONE
   ida_hexrays.CMT_TAIL
   ida_hexrays.CMT_BLOCK1
   ida_hexrays.CMT_BLOCK2
   ida_hexrays.CMT_LVAR
   ida_hexrays.CMT_FUNC
   ida_hexrays.CMT_ALL
   ida_hexrays.VDUI_VISIBLE
   ida_hexrays.VDUI_VALID
   ida_hexrays.hx_user_numforms_begin
   ida_hexrays.hx_user_numforms_end
   ida_hexrays.hx_user_numforms_next
   ida_hexrays.hx_user_numforms_prev
   ida_hexrays.hx_user_numforms_first
   ida_hexrays.hx_user_numforms_second
   ida_hexrays.hx_user_numforms_find
   ida_hexrays.hx_user_numforms_insert
   ida_hexrays.hx_user_numforms_erase
   ida_hexrays.hx_user_numforms_clear
   ida_hexrays.hx_user_numforms_size
   ida_hexrays.hx_user_numforms_free
   ida_hexrays.hx_user_numforms_new
   ida_hexrays.hx_lvar_mapping_begin
   ida_hexrays.hx_lvar_mapping_end
   ida_hexrays.hx_lvar_mapping_next
   ida_hexrays.hx_lvar_mapping_prev
   ida_hexrays.hx_lvar_mapping_first
   ida_hexrays.hx_lvar_mapping_second
   ida_hexrays.hx_lvar_mapping_find
   ida_hexrays.hx_lvar_mapping_insert
   ida_hexrays.hx_lvar_mapping_erase
   ida_hexrays.hx_lvar_mapping_clear
   ida_hexrays.hx_lvar_mapping_size
   ida_hexrays.hx_lvar_mapping_free
   ida_hexrays.hx_lvar_mapping_new
   ida_hexrays.hx_udcall_map_begin
   ida_hexrays.hx_udcall_map_end
   ida_hexrays.hx_udcall_map_next
   ida_hexrays.hx_udcall_map_prev
   ida_hexrays.hx_udcall_map_first
   ida_hexrays.hx_udcall_map_second
   ida_hexrays.hx_udcall_map_find
   ida_hexrays.hx_udcall_map_insert
   ida_hexrays.hx_udcall_map_erase
   ida_hexrays.hx_udcall_map_clear
   ida_hexrays.hx_udcall_map_size
   ida_hexrays.hx_udcall_map_free
   ida_hexrays.hx_udcall_map_new
   ida_hexrays.hx_user_cmts_begin
   ida_hexrays.hx_user_cmts_end
   ida_hexrays.hx_user_cmts_next
   ida_hexrays.hx_user_cmts_prev
   ida_hexrays.hx_user_cmts_first
   ida_hexrays.hx_user_cmts_second
   ida_hexrays.hx_user_cmts_find
   ida_hexrays.hx_user_cmts_insert
   ida_hexrays.hx_user_cmts_erase
   ida_hexrays.hx_user_cmts_clear
   ida_hexrays.hx_user_cmts_size
   ida_hexrays.hx_user_cmts_free
   ida_hexrays.hx_user_cmts_new
   ida_hexrays.hx_user_iflags_begin
   ida_hexrays.hx_user_iflags_end
   ida_hexrays.hx_user_iflags_next
   ida_hexrays.hx_user_iflags_prev
   ida_hexrays.hx_user_iflags_first
   ida_hexrays.hx_user_iflags_second
   ida_hexrays.hx_user_iflags_find
   ida_hexrays.hx_user_iflags_insert
   ida_hexrays.hx_user_iflags_erase
   ida_hexrays.hx_user_iflags_clear
   ida_hexrays.hx_user_iflags_size
   ida_hexrays.hx_user_iflags_free
   ida_hexrays.hx_user_iflags_new
   ida_hexrays.hx_user_unions_begin
   ida_hexrays.hx_user_unions_end
   ida_hexrays.hx_user_unions_next
   ida_hexrays.hx_user_unions_prev
   ida_hexrays.hx_user_unions_first
   ida_hexrays.hx_user_unions_second
   ida_hexrays.hx_user_unions_find
   ida_hexrays.hx_user_unions_insert
   ida_hexrays.hx_user_unions_erase
   ida_hexrays.hx_user_unions_clear
   ida_hexrays.hx_user_unions_size
   ida_hexrays.hx_user_unions_free
   ida_hexrays.hx_user_unions_new
   ida_hexrays.hx_user_labels_begin
   ida_hexrays.hx_user_labels_end
   ida_hexrays.hx_user_labels_next
   ida_hexrays.hx_user_labels_prev
   ida_hexrays.hx_user_labels_first
   ida_hexrays.hx_user_labels_second
   ida_hexrays.hx_user_labels_find
   ida_hexrays.hx_user_labels_insert
   ida_hexrays.hx_user_labels_erase
   ida_hexrays.hx_user_labels_clear
   ida_hexrays.hx_user_labels_size
   ida_hexrays.hx_user_labels_free
   ida_hexrays.hx_user_labels_new
   ida_hexrays.hx_eamap_begin
   ida_hexrays.hx_eamap_end
   ida_hexrays.hx_eamap_next
   ida_hexrays.hx_eamap_prev
   ida_hexrays.hx_eamap_first
   ida_hexrays.hx_eamap_second
   ida_hexrays.hx_eamap_find
   ida_hexrays.hx_eamap_insert
   ida_hexrays.hx_eamap_erase
   ida_hexrays.hx_eamap_clear
   ida_hexrays.hx_eamap_size
   ida_hexrays.hx_eamap_free
   ida_hexrays.hx_eamap_new
   ida_hexrays.hx_boundaries_begin
   ida_hexrays.hx_boundaries_end
   ida_hexrays.hx_boundaries_next
   ida_hexrays.hx_boundaries_prev
   ida_hexrays.hx_boundaries_first
   ida_hexrays.hx_boundaries_second
   ida_hexrays.hx_boundaries_find
   ida_hexrays.hx_boundaries_insert
   ida_hexrays.hx_boundaries_erase
   ida_hexrays.hx_boundaries_clear
   ida_hexrays.hx_boundaries_size
   ida_hexrays.hx_boundaries_free
   ida_hexrays.hx_boundaries_new
   ida_hexrays.hx_block_chains_begin
   ida_hexrays.hx_block_chains_end
   ida_hexrays.hx_block_chains_next
   ida_hexrays.hx_block_chains_prev
   ida_hexrays.hx_block_chains_get
   ida_hexrays.hx_block_chains_find
   ida_hexrays.hx_block_chains_insert
   ida_hexrays.hx_block_chains_erase
   ida_hexrays.hx_block_chains_clear
   ida_hexrays.hx_block_chains_size
   ida_hexrays.hx_block_chains_free
   ida_hexrays.hx_block_chains_new
   ida_hexrays.hx_hexrays_alloc
   ida_hexrays.hx_hexrays_free
   ida_hexrays.hx_valrng_t_clear
   ida_hexrays.hx_valrng_t_copy
   ida_hexrays.hx_valrng_t_assign
   ida_hexrays.hx_valrng_t_compare
   ida_hexrays.hx_valrng_t_set_eq
   ida_hexrays.hx_valrng_t_set_cmp
   ida_hexrays.hx_valrng_t_reduce_size
   ida_hexrays.hx_valrng_t_intersect_with
   ida_hexrays.hx_valrng_t_unite_with
   ida_hexrays.hx_valrng_t_inverse
   ida_hexrays.hx_valrng_t_has
   ida_hexrays.hx_valrng_t_print
   ida_hexrays.hx_valrng_t_dstr
   ida_hexrays.hx_valrng_t_cvt_to_single_value
   ida_hexrays.hx_valrng_t_cvt_to_cmp
   ida_hexrays.hx_get_merror_desc
   ida_hexrays.hx_must_mcode_close_block
   ida_hexrays.hx_is_mcode_propagatable
   ida_hexrays.hx_negate_mcode_relation
   ida_hexrays.hx_swap_mcode_relation
   ida_hexrays.hx_get_signed_mcode
   ida_hexrays.hx_get_unsigned_mcode
   ida_hexrays.hx_mcode_modifies_d
   ida_hexrays.hx_operand_locator_t_compare
   ida_hexrays.hx_vd_printer_t_print
   ida_hexrays.hx_file_printer_t_print
   ida_hexrays.hx_qstring_printer_t_print
   ida_hexrays.hx_dstr
   ida_hexrays.hx_is_type_correct
   ida_hexrays.hx_is_small_udt
   ida_hexrays.hx_is_nonbool_type
   ida_hexrays.hx_is_bool_type
   ida_hexrays.hx_partial_type_num
   ida_hexrays.hx_get_float_type
   ida_hexrays.hx_get_int_type_by_width_and_sign
   ida_hexrays.hx_get_unk_type
   ida_hexrays.hx_dummy_ptrtype
   ida_hexrays.hx_get_member_type
   ida_hexrays.hx_make_pointer
   ida_hexrays.hx_create_typedef
   ida_hexrays.hx_get_type
   ida_hexrays.hx_set_type
   ida_hexrays.hx_vdloc_t_dstr
   ida_hexrays.hx_vdloc_t_compare
   ida_hexrays.hx_vdloc_t_is_aliasable
   ida_hexrays.hx_print_vdloc
   ida_hexrays.hx_arglocs_overlap
   ida_hexrays.hx_lvar_locator_t_compare
   ida_hexrays.hx_lvar_locator_t_dstr
   ida_hexrays.hx_lvar_t_dstr
   ida_hexrays.hx_lvar_t_is_promoted_arg
   ida_hexrays.hx_lvar_t_accepts_type
   ida_hexrays.hx_lvar_t_set_lvar_type
   ida_hexrays.hx_lvar_t_set_width
   ida_hexrays.hx_lvar_t_append_list
   ida_hexrays.hx_lvar_t_append_list_
   ida_hexrays.hx_lvars_t_find_stkvar
   ida_hexrays.hx_lvars_t_find
   ida_hexrays.hx_lvars_t_find_lvar
   ida_hexrays.hx_restore_user_lvar_settings
   ida_hexrays.hx_save_user_lvar_settings
   ida_hexrays.hx_modify_user_lvars
   ida_hexrays.hx_modify_user_lvar_info
   ida_hexrays.hx_locate_lvar
   ida_hexrays.hx_restore_user_defined_calls
   ida_hexrays.hx_save_user_defined_calls
   ida_hexrays.hx_parse_user_call
   ida_hexrays.hx_convert_to_user_call
   ida_hexrays.hx_install_microcode_filter
   ida_hexrays.hx_udc_filter_t_cleanup
   ida_hexrays.hx_udc_filter_t_init
   ida_hexrays.hx_udc_filter_t_apply
   ida_hexrays.hx_bitset_t_bitset_t
   ida_hexrays.hx_bitset_t_copy
   ida_hexrays.hx_bitset_t_add
   ida_hexrays.hx_bitset_t_add_
   ida_hexrays.hx_bitset_t_add__
   ida_hexrays.hx_bitset_t_sub
   ida_hexrays.hx_bitset_t_sub_
   ida_hexrays.hx_bitset_t_sub__
   ida_hexrays.hx_bitset_t_cut_at
   ida_hexrays.hx_bitset_t_shift_down
   ida_hexrays.hx_bitset_t_has
   ida_hexrays.hx_bitset_t_has_all
   ida_hexrays.hx_bitset_t_has_any
   ida_hexrays.hx_bitset_t_dstr
   ida_hexrays.hx_bitset_t_empty
   ida_hexrays.hx_bitset_t_count
   ida_hexrays.hx_bitset_t_count_
   ida_hexrays.hx_bitset_t_last
   ida_hexrays.hx_bitset_t_fill_with_ones
   ida_hexrays.hx_bitset_t_fill_gaps
   ida_hexrays.hx_bitset_t_has_common
   ida_hexrays.hx_bitset_t_intersect
   ida_hexrays.hx_bitset_t_is_subset_of
   ida_hexrays.hx_bitset_t_compare
   ida_hexrays.hx_bitset_t_goup
   ida_hexrays.hx_ivl_t_dstr
   ida_hexrays.hx_ivl_t_compare
   ida_hexrays.hx_ivlset_t_add
   ida_hexrays.hx_ivlset_t_add_
   ida_hexrays.hx_ivlset_t_addmasked
   ida_hexrays.hx_ivlset_t_sub
   ida_hexrays.hx_ivlset_t_sub_
   ida_hexrays.hx_ivlset_t_has_common
   ida_hexrays.hx_ivlset_t_print
   ida_hexrays.hx_ivlset_t_dstr
   ida_hexrays.hx_ivlset_t_count
   ida_hexrays.hx_ivlset_t_has_common_
   ida_hexrays.hx_ivlset_t_contains
   ida_hexrays.hx_ivlset_t_includes
   ida_hexrays.hx_ivlset_t_intersect
   ida_hexrays.hx_ivlset_t_compare
   ida_hexrays.hx_rlist_t_print
   ida_hexrays.hx_rlist_t_dstr
   ida_hexrays.hx_mlist_t_addmem
   ida_hexrays.hx_mlist_t_print
   ida_hexrays.hx_mlist_t_dstr
   ida_hexrays.hx_mlist_t_compare
   ida_hexrays.hx_get_temp_regs
   ida_hexrays.hx_is_kreg
   ida_hexrays.hx_reg2mreg
   ida_hexrays.hx_mreg2reg
   ida_hexrays.hx_get_mreg_name
   ida_hexrays.hx_install_optinsn_handler
   ida_hexrays.hx_remove_optinsn_handler
   ida_hexrays.hx_install_optblock_handler
   ida_hexrays.hx_remove_optblock_handler
   ida_hexrays.hx_simple_graph_t_compute_dominators
   ida_hexrays.hx_simple_graph_t_compute_immediate_dominators
   ida_hexrays.hx_simple_graph_t_depth_first_preorder
   ida_hexrays.hx_simple_graph_t_depth_first_postorder
   ida_hexrays.hx_simple_graph_t_goup
   ida_hexrays.hx_mutable_graph_t_resize
   ida_hexrays.hx_mutable_graph_t_goup
   ida_hexrays.hx_mutable_graph_t_del_edge
   ida_hexrays.hx_lvar_ref_t_compare
   ida_hexrays.hx_lvar_ref_t_var
   ida_hexrays.hx_stkvar_ref_t_compare
   ida_hexrays.hx_stkvar_ref_t_get_stkvar
   ida_hexrays.hx_fnumber_t_print
   ida_hexrays.hx_fnumber_t_dstr
   ida_hexrays.hx_mop_t_copy
   ida_hexrays.hx_mop_t_assign
   ida_hexrays.hx_mop_t_swap
   ida_hexrays.hx_mop_t_erase
   ida_hexrays.hx_mop_t_print
   ida_hexrays.hx_mop_t_dstr
   ida_hexrays.hx_mop_t_create_from_mlist
   ida_hexrays.hx_mop_t_create_from_ivlset
   ida_hexrays.hx_mop_t_create_from_vdloc
   ida_hexrays.hx_mop_t_create_from_scattered_vdloc
   ida_hexrays.hx_mop_t_create_from_insn
   ida_hexrays.hx_mop_t_make_number
   ida_hexrays.hx_mop_t_make_fpnum
   ida_hexrays.hx_mop_t__make_gvar
   ida_hexrays.hx_mop_t_make_gvar
   ida_hexrays.hx_mop_t_make_reg_pair
   ida_hexrays.hx_mop_t_make_helper
   ida_hexrays.hx_mop_t_is_bit_reg
   ida_hexrays.hx_mop_t_may_use_aliased_memory
   ida_hexrays.hx_mop_t_is01
   ida_hexrays.hx_mop_t_is_sign_extended_from
   ida_hexrays.hx_mop_t_is_zero_extended_from
   ida_hexrays.hx_mop_t_equal_mops
   ida_hexrays.hx_mop_t_lexcompare
   ida_hexrays.hx_mop_t_for_all_ops
   ida_hexrays.hx_mop_t_for_all_scattered_submops
   ida_hexrays.hx_mop_t_is_constant
   ida_hexrays.hx_mop_t_get_stkoff
   ida_hexrays.hx_mop_t_make_low_half
   ida_hexrays.hx_mop_t_make_high_half
   ida_hexrays.hx_mop_t_make_first_half
   ida_hexrays.hx_mop_t_make_second_half
   ida_hexrays.hx_mop_t_shift_mop
   ida_hexrays.hx_mop_t_change_size
   ida_hexrays.hx_mop_t_preserve_side_effects
   ida_hexrays.hx_mop_t_apply_ld_mcode
   ida_hexrays.hx_mcallarg_t_print
   ida_hexrays.hx_mcallarg_t_dstr
   ida_hexrays.hx_mcallarg_t_set_regarg
   ida_hexrays.hx_mcallinfo_t_lexcompare
   ida_hexrays.hx_mcallinfo_t_set_type
   ida_hexrays.hx_mcallinfo_t_get_type
   ida_hexrays.hx_mcallinfo_t_print
   ida_hexrays.hx_mcallinfo_t_dstr
   ida_hexrays.hx_mcases_t_compare
   ida_hexrays.hx_mcases_t_print
   ida_hexrays.hx_mcases_t_dstr
   ida_hexrays.hx_vivl_t_extend_to_cover
   ida_hexrays.hx_vivl_t_intersect
   ida_hexrays.hx_vivl_t_print
   ida_hexrays.hx_vivl_t_dstr
   ida_hexrays.hx_chain_t_print
   ida_hexrays.hx_chain_t_dstr
   ida_hexrays.hx_chain_t_append_list
   ida_hexrays.hx_chain_t_append_list_
   ida_hexrays.hx_block_chains_t_get_chain
   ida_hexrays.hx_block_chains_t_print
   ida_hexrays.hx_block_chains_t_dstr
   ida_hexrays.hx_graph_chains_t_for_all_chains
   ida_hexrays.hx_graph_chains_t_release
   ida_hexrays.hx_minsn_t_init
   ida_hexrays.hx_minsn_t_copy
   ida_hexrays.hx_minsn_t_set_combined
   ida_hexrays.hx_minsn_t_swap
   ida_hexrays.hx_minsn_t_print
   ida_hexrays.hx_minsn_t_dstr
   ida_hexrays.hx_minsn_t_setaddr
   ida_hexrays.hx_minsn_t_optimize_subtree
   ida_hexrays.hx_minsn_t_for_all_ops
   ida_hexrays.hx_minsn_t_for_all_insns
   ida_hexrays.hx_minsn_t__make_nop
   ida_hexrays.hx_minsn_t_equal_insns
   ida_hexrays.hx_minsn_t_lexcompare
   ida_hexrays.hx_minsn_t_is_noret_call
   ida_hexrays.hx_minsn_t_is_helper
   ida_hexrays.hx_minsn_t_find_call
   ida_hexrays.hx_minsn_t_has_side_effects
   ida_hexrays.hx_minsn_t_find_opcode
   ida_hexrays.hx_minsn_t_find_ins_op
   ida_hexrays.hx_minsn_t_find_num_op
   ida_hexrays.hx_minsn_t_modifies_d
   ida_hexrays.hx_minsn_t_is_between
   ida_hexrays.hx_minsn_t_may_use_aliased_memory
   ida_hexrays.hx_minsn_t_serialize
   ida_hexrays.hx_minsn_t_deserialize
   ida_hexrays.hx_getf_reginsn
   ida_hexrays.hx_getb_reginsn
   ida_hexrays.hx_mblock_t_init
   ida_hexrays.hx_mblock_t_print
   ida_hexrays.hx_mblock_t_dump
   ida_hexrays.hx_mblock_t_vdump_block
   ida_hexrays.hx_mblock_t_insert_into_block
   ida_hexrays.hx_mblock_t_remove_from_block
   ida_hexrays.hx_mblock_t_for_all_insns
   ida_hexrays.hx_mblock_t_for_all_ops
   ida_hexrays.hx_mblock_t_for_all_uses
   ida_hexrays.hx_mblock_t_optimize_insn
   ida_hexrays.hx_mblock_t_optimize_block
   ida_hexrays.hx_mblock_t_build_lists
   ida_hexrays.hx_mblock_t_optimize_useless_jump
   ida_hexrays.hx_mblock_t_append_use_list
   ida_hexrays.hx_mblock_t_append_def_list
   ida_hexrays.hx_mblock_t_build_use_list
   ida_hexrays.hx_mblock_t_build_def_list
   ida_hexrays.hx_mblock_t_find_first_use
   ida_hexrays.hx_mblock_t_find_redefinition
   ida_hexrays.hx_mblock_t_is_rhs_redefined
   ida_hexrays.hx_mblock_t_find_access
   ida_hexrays.hx_mblock_t_get_valranges
   ida_hexrays.hx_mblock_t_get_valranges_
   ida_hexrays.hx_mblock_t_get_reginsn_qty
   ida_hexrays.hx_mba_ranges_t_range_contains
   ida_hexrays.hx_mba_t_stkoff_vd2ida
   ida_hexrays.hx_mba_t_stkoff_ida2vd
   ida_hexrays.hx_mba_t_idaloc2vd
   ida_hexrays.hx_mba_t_idaloc2vd_
   ida_hexrays.hx_mba_t_vd2idaloc
   ida_hexrays.hx_mba_t_vd2idaloc_
   ida_hexrays.hx_mba_t_term
   ida_hexrays.hx_mba_t_get_curfunc
   ida_hexrays.hx_mba_t_set_maturity
   ida_hexrays.hx_mba_t_optimize_local
   ida_hexrays.hx_mba_t_build_graph
   ida_hexrays.hx_mba_t_get_graph
   ida_hexrays.hx_mba_t_analyze_calls
   ida_hexrays.hx_mba_t_optimize_global
   ida_hexrays.hx_mba_t_alloc_lvars
   ida_hexrays.hx_mba_t_dump
   ida_hexrays.hx_mba_t_vdump_mba
   ida_hexrays.hx_mba_t_print
   ida_hexrays.hx_mba_t_verify
   ida_hexrays.hx_mba_t_mark_chains_dirty
   ida_hexrays.hx_mba_t_insert_block
   ida_hexrays.hx_mba_t_remove_block
   ida_hexrays.hx_mba_t_copy_block
   ida_hexrays.hx_mba_t_remove_empty_and_unreachable_blocks
   ida_hexrays.hx_mba_t_merge_blocks
   ida_hexrays.hx_mba_t_for_all_ops
   ida_hexrays.hx_mba_t_for_all_insns
   ida_hexrays.hx_mba_t_for_all_topinsns
   ida_hexrays.hx_mba_t_find_mop
   ida_hexrays.hx_mba_t_create_helper_call
   ida_hexrays.hx_mba_t_get_func_output_lists
   ida_hexrays.hx_mba_t_arg
   ida_hexrays.hx_mba_t_alloc_fict_ea
   ida_hexrays.hx_mba_t_map_fict_ea
   ida_hexrays.hx_mba_t_serialize
   ida_hexrays.hx_mba_t_deserialize
   ida_hexrays.hx_mba_t_save_snapshot
   ida_hexrays.hx_mba_t_alloc_kreg
   ida_hexrays.hx_mba_t_free_kreg
   ida_hexrays.hx_mba_t_inline_func
   ida_hexrays.hx_mba_t_locate_stkpnt
   ida_hexrays.hx_mba_t_set_lvar_name
   ida_hexrays.hx_mbl_graph_t_is_accessed_globally
   ida_hexrays.hx_mbl_graph_t_get_ud
   ida_hexrays.hx_mbl_graph_t_get_du
   ida_hexrays.hx_cdg_insn_iterator_t_next
   ida_hexrays.hx_codegen_t_clear
   ida_hexrays.hx_codegen_t_emit
   ida_hexrays.hx_codegen_t_emit_
   ida_hexrays.hx_change_hexrays_config
   ida_hexrays.hx_get_hexrays_version
   ida_hexrays.hx_open_pseudocode
   ida_hexrays.hx_close_pseudocode
   ida_hexrays.hx_get_widget_vdui
   ida_hexrays.hx_decompile_many
   ida_hexrays.hx_hexrays_failure_t_desc
   ida_hexrays.hx_send_database
   ida_hexrays.hx_gco_info_t_append_to_list
   ida_hexrays.hx_get_current_operand
   ida_hexrays.hx_remitem
   ida_hexrays.hx_negated_relation
   ida_hexrays.hx_swapped_relation
   ida_hexrays.hx_get_op_signness
   ida_hexrays.hx_asgop
   ida_hexrays.hx_asgop_revert
   ida_hexrays.hx_cnumber_t_print
   ida_hexrays.hx_cnumber_t_value
   ida_hexrays.hx_cnumber_t_assign
   ida_hexrays.hx_cnumber_t_compare
   ida_hexrays.hx_var_ref_t_compare
   ida_hexrays.hx_ctree_visitor_t_apply_to
   ida_hexrays.hx_ctree_visitor_t_apply_to_exprs
   ida_hexrays.hx_ctree_parentee_t_recalc_parent_types
   ida_hexrays.hx_cfunc_parentee_t_calc_rvalue_type
   ida_hexrays.hx_citem_locator_t_compare
   ida_hexrays.hx_citem_t_contains_expr
   ida_hexrays.hx_citem_t_contains_label
   ida_hexrays.hx_citem_t_find_parent_of
   ida_hexrays.hx_citem_t_find_closest_addr
   ida_hexrays.hx_cexpr_t_assign
   ida_hexrays.hx_cexpr_t_compare
   ida_hexrays.hx_cexpr_t_replace_by
   ida_hexrays.hx_cexpr_t_cleanup
   ida_hexrays.hx_cexpr_t_put_number
   ida_hexrays.hx_cexpr_t_print1
   ida_hexrays.hx_cexpr_t_calc_type
   ida_hexrays.hx_cexpr_t_equal_effect
   ida_hexrays.hx_cexpr_t_is_child_of
   ida_hexrays.hx_cexpr_t_contains_operator
   ida_hexrays.hx_cexpr_t_get_high_nbit_bound
   ida_hexrays.hx_cexpr_t_get_low_nbit_bound
   ida_hexrays.hx_cexpr_t_requires_lvalue
   ida_hexrays.hx_cexpr_t_has_side_effects
   ida_hexrays.hx_cexpr_t_maybe_ptr
   ida_hexrays.hx_cexpr_t_dstr
   ida_hexrays.hx_cif_t_assign
   ida_hexrays.hx_cif_t_compare
   ida_hexrays.hx_cloop_t_assign
   ida_hexrays.hx_cfor_t_compare
   ida_hexrays.hx_cwhile_t_compare
   ida_hexrays.hx_cdo_t_compare
   ida_hexrays.hx_creturn_t_compare
   ida_hexrays.hx_cthrow_t_compare
   ida_hexrays.hx_cgoto_t_compare
   ida_hexrays.hx_casm_t_compare
   ida_hexrays.hx_cinsn_t_assign
   ida_hexrays.hx_cinsn_t_compare
   ida_hexrays.hx_cinsn_t_replace_by
   ida_hexrays.hx_cinsn_t_cleanup
   ida_hexrays.hx_cinsn_t_new_insn
   ida_hexrays.hx_cinsn_t_create_if
   ida_hexrays.hx_cinsn_t_print
   ida_hexrays.hx_cinsn_t_print1
   ida_hexrays.hx_cinsn_t_is_ordinary_flow
   ida_hexrays.hx_cinsn_t_contains_insn
   ida_hexrays.hx_cinsn_t_collect_free_breaks
   ida_hexrays.hx_cinsn_t_collect_free_continues
   ida_hexrays.hx_cinsn_t_dstr
   ida_hexrays.hx_cblock_t_compare
   ida_hexrays.hx_carglist_t_compare
   ida_hexrays.hx_ccase_t_compare
   ida_hexrays.hx_ccases_t_compare
   ida_hexrays.hx_cswitch_t_compare
   ida_hexrays.hx_ccatch_t_compare
   ida_hexrays.hx_ctry_t_compare
   ida_hexrays.hx_ctree_item_t_get_udm
   ida_hexrays.hx_ctree_item_t_get_edm
   ida_hexrays.hx_ctree_item_t_get_lvar
   ida_hexrays.hx_ctree_item_t_get_ea
   ida_hexrays.hx_ctree_item_t_get_label_num
   ida_hexrays.hx_ctree_item_t_print
   ida_hexrays.hx_ctree_item_t_dstr
   ida_hexrays.hx_lnot
   ida_hexrays.hx_new_block
   ida_hexrays.hx_vcreate_helper
   ida_hexrays.hx_vcall_helper
   ida_hexrays.hx_make_num
   ida_hexrays.hx_make_ref
   ida_hexrays.hx_dereference
   ida_hexrays.hx_save_user_labels
   ida_hexrays.hx_save_user_cmts
   ida_hexrays.hx_save_user_numforms
   ida_hexrays.hx_save_user_iflags
   ida_hexrays.hx_save_user_unions
   ida_hexrays.hx_restore_user_labels
   ida_hexrays.hx_restore_user_cmts
   ida_hexrays.hx_restore_user_numforms
   ida_hexrays.hx_restore_user_iflags
   ida_hexrays.hx_restore_user_unions
   ida_hexrays.hx_cfunc_t_build_c_tree
   ida_hexrays.hx_cfunc_t_verify
   ida_hexrays.hx_cfunc_t_print_dcl
   ida_hexrays.hx_cfunc_t_print_func
   ida_hexrays.hx_cfunc_t_get_func_type
   ida_hexrays.hx_cfunc_t_get_lvars
   ida_hexrays.hx_cfunc_t_get_stkoff_delta
   ida_hexrays.hx_cfunc_t_find_label
   ida_hexrays.hx_cfunc_t_remove_unused_labels
   ida_hexrays.hx_cfunc_t_get_user_cmt
   ida_hexrays.hx_cfunc_t_set_user_cmt
   ida_hexrays.hx_cfunc_t_get_user_iflags
   ida_hexrays.hx_cfunc_t_set_user_iflags
   ida_hexrays.hx_cfunc_t_has_orphan_cmts
   ida_hexrays.hx_cfunc_t_del_orphan_cmts
   ida_hexrays.hx_cfunc_t_get_user_union_selection
   ida_hexrays.hx_cfunc_t_set_user_union_selection
   ida_hexrays.hx_cfunc_t_save_user_labels
   ida_hexrays.hx_cfunc_t_save_user_cmts
   ida_hexrays.hx_cfunc_t_save_user_numforms
   ida_hexrays.hx_cfunc_t_save_user_iflags
   ida_hexrays.hx_cfunc_t_save_user_unions
   ida_hexrays.hx_cfunc_t_get_line_item
   ida_hexrays.hx_cfunc_t_get_warnings
   ida_hexrays.hx_cfunc_t_get_eamap
   ida_hexrays.hx_cfunc_t_get_boundaries
   ida_hexrays.hx_cfunc_t_get_pseudocode
   ida_hexrays.hx_cfunc_t_refresh_func_ctext
   ida_hexrays.hx_cfunc_t_gather_derefs
   ida_hexrays.hx_cfunc_t_find_item_coords
   ida_hexrays.hx_cfunc_t_cleanup
   ida_hexrays.hx_close_hexrays_waitbox
   ida_hexrays.hx_decompile
   ida_hexrays.hx_gen_microcode
   ida_hexrays.hx_create_cfunc
   ida_hexrays.hx_mark_cfunc_dirty
   ida_hexrays.hx_clear_cached_cfuncs
   ida_hexrays.hx_has_cached_cfunc
   ida_hexrays.hx_get_ctype_name
   ida_hexrays.hx_create_field_name
   ida_hexrays.hx_install_hexrays_callback
   ida_hexrays.hx_remove_hexrays_callback
   ida_hexrays.hx_vdui_t_set_locked
   ida_hexrays.hx_vdui_t_refresh_view
   ida_hexrays.hx_vdui_t_refresh_ctext
   ida_hexrays.hx_vdui_t_switch_to
   ida_hexrays.hx_vdui_t_get_number
   ida_hexrays.hx_vdui_t_get_current_label
   ida_hexrays.hx_vdui_t_clear
   ida_hexrays.hx_vdui_t_refresh_cpos
   ida_hexrays.hx_vdui_t_get_current_item
   ida_hexrays.hx_vdui_t_ui_rename_lvar
   ida_hexrays.hx_vdui_t_rename_lvar
   ida_hexrays.hx_vdui_t_ui_set_call_type
   ida_hexrays.hx_vdui_t_ui_set_lvar_type
   ida_hexrays.hx_vdui_t_set_lvar_type
   ida_hexrays.hx_vdui_t_set_noptr_lvar
   ida_hexrays.hx_vdui_t_ui_edit_lvar_cmt
   ida_hexrays.hx_vdui_t_set_lvar_cmt
   ida_hexrays.hx_vdui_t_ui_map_lvar
   ida_hexrays.hx_vdui_t_ui_unmap_lvar
   ida_hexrays.hx_vdui_t_map_lvar
   ida_hexrays.hx_vdui_t_set_udm_type
   ida_hexrays.hx_vdui_t_rename_udm
   ida_hexrays.hx_vdui_t_set_global_type
   ida_hexrays.hx_vdui_t_rename_global
   ida_hexrays.hx_vdui_t_rename_label
   ida_hexrays.hx_vdui_t_jump_enter
   ida_hexrays.hx_vdui_t_ctree_to_disasm
   ida_hexrays.hx_vdui_t_calc_cmt_type
   ida_hexrays.hx_vdui_t_edit_cmt
   ida_hexrays.hx_vdui_t_edit_func_cmt
   ida_hexrays.hx_vdui_t_del_orphan_cmts
   ida_hexrays.hx_vdui_t_set_num_radix
   ida_hexrays.hx_vdui_t_set_num_enum
   ida_hexrays.hx_vdui_t_set_num_stroff
   ida_hexrays.hx_vdui_t_invert_sign
   ida_hexrays.hx_vdui_t_invert_bits
   ida_hexrays.hx_vdui_t_collapse_item
   ida_hexrays.hx_vdui_t_collapse_lvars
   ida_hexrays.hx_vdui_t_split_item
   ida_hexrays.hx_select_udt_by_offset
   ida_hexrays.hx_catchexpr_t_compare
   ida_hexrays.hx_mba_t_split_block
   ida_hexrays.hx_mba_t_remove_blocks
   ida_hexrays.hx_cfunc_t_recalc_item_addresses
   ida_hexrays.hx_int64_emulator_t_mop_value
   ida_hexrays.hx_int64_emulator_t_minsn_value
   ida_hexrays.is_allowed_on_small_struni
   ida_hexrays.is_small_struni
   ida_hexrays.mbl_array_t


Exceptions
----------

.. autoapisummary::

   ida_hexrays.DecompilationFailure


Classes
-------

.. autoapisummary::

   ida_hexrays.array_of_bitsets
   ida_hexrays.mopvec_t
   ida_hexrays.mcallargs_t
   ida_hexrays.block_chains_vec_t
   ida_hexrays.user_numforms_t
   ida_hexrays.lvar_mapping_t
   ida_hexrays.hexwarns_t
   ida_hexrays.ctree_items_t
   ida_hexrays.user_labels_t
   ida_hexrays.user_cmts_t
   ida_hexrays.user_iflags_t
   ida_hexrays.user_unions_t
   ida_hexrays.cinsnptrvec_t
   ida_hexrays.eamap_t
   ida_hexrays.boundaries_t
   ida_hexrays.cfuncptr_t
   ida_hexrays.qvector_history_t
   ida_hexrays.history_t
   ida_hexrays.cinsn_list_t_iterator
   ida_hexrays.cinsn_list_t
   ida_hexrays.qvector_lvar_t
   ida_hexrays.qvector_carg_t
   ida_hexrays.qvector_ccase_t
   ida_hexrays.qvector_catchexprs_t
   ida_hexrays.qvector_ccatchvec_t
   ida_hexrays.cblock_posvec_t
   ida_hexrays.lvar_saved_infos_t
   ida_hexrays.ui_stroff_ops_t
   ida_hexrays.Hexrays_Hooks
   ida_hexrays.uval_ivl_t
   ida_hexrays.uval_ivl_ivlset_t
   ida_hexrays.array_of_ivlsets
   ida_hexrays.valrng_t
   ida_hexrays.operand_locator_t
   ida_hexrays.number_format_t
   ida_hexrays.vd_printer_t
   ida_hexrays.vc_printer_t
   ida_hexrays.qstring_printer_t
   ida_hexrays.vdloc_t
   ida_hexrays.lvar_locator_t
   ida_hexrays.lvar_t
   ida_hexrays.lvars_t
   ida_hexrays.lvar_saved_info_t
   ida_hexrays.lvar_uservec_t
   ida_hexrays.user_lvar_modifier_t
   ida_hexrays.udcall_t
   ida_hexrays.microcode_filter_t
   ida_hexrays.udc_filter_t
   ida_hexrays.bitset_t
   ida_hexrays.iterator
   ida_hexrays.node_bitset_t
   ida_hexrays.array_of_node_bitset_t
   ida_hexrays.ivl_t
   ida_hexrays.ivl_with_name_t
   ida_hexrays.ivlset_t
   ida_hexrays.rlist_t
   ida_hexrays.mlist_t
   ida_hexrays.optinsn_t
   ida_hexrays.optblock_t
   ida_hexrays.simple_graph_t
   ida_hexrays.op_parent_info_t
   ida_hexrays.minsn_visitor_t
   ida_hexrays.mop_visitor_t
   ida_hexrays.scif_visitor_t
   ida_hexrays.mlist_mop_visitor_t
   ida_hexrays.lvar_ref_t
   ida_hexrays.stkvar_ref_t
   ida_hexrays.scif_t
   ida_hexrays.mnumber_t
   ida_hexrays.fnumber_t
   ida_hexrays.mop_t
   ida_hexrays.mop_pair_t
   ida_hexrays.mop_addr_t
   ida_hexrays.mcallarg_t
   ida_hexrays.mcallinfo_t
   ida_hexrays.mcases_t
   ida_hexrays.voff_t
   ida_hexrays.vivl_t
   ida_hexrays.chain_t
   ida_hexrays.block_chains_t
   ida_hexrays.chain_visitor_t
   ida_hexrays.graph_chains_t
   ida_hexrays.minsn_t
   ida_hexrays.intval64_t
   ida_hexrays.int64_emulator_t
   ida_hexrays.mblock_t
   ida_hexrays.hexwarn_t
   ida_hexrays.mba_ranges_t
   ida_hexrays.mba_range_iterator_t
   ida_hexrays.mba_t
   ida_hexrays.chain_keeper_t
   ida_hexrays.mbl_graph_t
   ida_hexrays.cdg_insn_iterator_t
   ida_hexrays.codegen_t
   ida_hexrays.hexrays_failure_t
   ida_hexrays.vd_failure_t
   ida_hexrays.vd_interr_t
   ida_hexrays.gco_info_t
   ida_hexrays.cnumber_t
   ida_hexrays.var_ref_t
   ida_hexrays.treeloc_t
   ida_hexrays.citem_cmt_t
   ida_hexrays.citem_locator_t
   ida_hexrays.bit_bound_t
   ida_hexrays.citem_t
   ida_hexrays.cexpr_t
   ida_hexrays.ceinsn_t
   ida_hexrays.cif_t
   ida_hexrays.cloop_t
   ida_hexrays.cfor_t
   ida_hexrays.cwhile_t
   ida_hexrays.cdo_t
   ida_hexrays.creturn_t
   ida_hexrays.cgoto_t
   ida_hexrays.casm_t
   ida_hexrays.cinsn_t
   ida_hexrays.cblock_t
   ida_hexrays.carg_t
   ida_hexrays.carglist_t
   ida_hexrays.ccase_t
   ida_hexrays.ccases_t
   ida_hexrays.cswitch_t
   ida_hexrays.catchexpr_t
   ida_hexrays.ccatch_t
   ida_hexrays.ctry_t
   ida_hexrays.cthrow_t
   ida_hexrays.cblock_pos_t
   ida_hexrays.ctree_visitor_t
   ida_hexrays.ctree_parentee_t
   ida_hexrays.cfunc_parentee_t
   ida_hexrays.ctree_anchor_t
   ida_hexrays.ctree_item_t
   ida_hexrays.cfunc_t
   ida_hexrays.ctext_position_t
   ida_hexrays.history_item_t
   ida_hexrays.vdui_t
   ida_hexrays.ui_stroff_op_t
   ida_hexrays.ui_stroff_applicator_t
   ida_hexrays.user_numforms_iterator_t
   ida_hexrays.lvar_mapping_iterator_t
   ida_hexrays.udcall_map_iterator_t
   ida_hexrays.user_cmts_iterator_t
   ida_hexrays.user_iflags_iterator_t
   ida_hexrays.user_unions_iterator_t
   ida_hexrays.user_labels_iterator_t
   ida_hexrays.eamap_iterator_t
   ida_hexrays.boundaries_iterator_t
   ida_hexrays.block_chains_iterator_t


Functions
---------

.. autoapisummary::

   ida_hexrays.user_iflags_second
   ida_hexrays.qswap
   ida_hexrays.debug_hexrays_ctree
   ida_hexrays.init_hexrays_plugin
   ida_hexrays.get_widget_vdui
   ida_hexrays.boundaries_find
   ida_hexrays.boundaries_insert
   ida_hexrays.term_hexrays_plugin
   ida_hexrays.hexrays_alloc
   ida_hexrays.hexrays_free
   ida_hexrays.max_vlr_value
   ida_hexrays.min_vlr_svalue
   ida_hexrays.max_vlr_svalue
   ida_hexrays.is_unsigned_cmpop
   ida_hexrays.is_signed_cmpop
   ida_hexrays.is_cmpop_with_eq
   ida_hexrays.is_cmpop_without_eq
   ida_hexrays.is_may_access
   ida_hexrays.get_merror_desc
   ida_hexrays.must_mcode_close_block
   ida_hexrays.is_mcode_propagatable
   ida_hexrays.is_mcode_addsub
   ida_hexrays.is_mcode_xdsu
   ida_hexrays.is_mcode_set
   ida_hexrays.is_mcode_set1
   ida_hexrays.is_mcode_j1
   ida_hexrays.is_mcode_jcond
   ida_hexrays.is_mcode_convertible_to_jmp
   ida_hexrays.is_mcode_convertible_to_set
   ida_hexrays.is_mcode_call
   ida_hexrays.is_mcode_fpu
   ida_hexrays.is_mcode_commutative
   ida_hexrays.is_mcode_shift
   ida_hexrays.is_mcode_divmod
   ida_hexrays.has_mcode_seloff
   ida_hexrays.set2jcnd
   ida_hexrays.jcnd2set
   ida_hexrays.negate_mcode_relation
   ida_hexrays.swap_mcode_relation
   ida_hexrays.get_signed_mcode
   ida_hexrays.get_unsigned_mcode
   ida_hexrays.is_signed_mcode
   ida_hexrays.is_unsigned_mcode
   ida_hexrays.mcode_modifies_d
   ida_hexrays.dstr
   ida_hexrays.is_type_correct
   ida_hexrays.is_small_udt
   ida_hexrays.is_nonbool_type
   ida_hexrays.is_bool_type
   ida_hexrays.is_ptr_or_array
   ida_hexrays.is_paf
   ida_hexrays.is_inplace_def
   ida_hexrays.partial_type_num
   ida_hexrays.get_float_type
   ida_hexrays.get_int_type_by_width_and_sign
   ida_hexrays.get_unk_type
   ida_hexrays.dummy_ptrtype
   ida_hexrays.make_pointer
   ida_hexrays.create_typedef
   ida_hexrays.get_type
   ida_hexrays.set_type
   ida_hexrays.print_vdloc
   ida_hexrays.arglocs_overlap
   ida_hexrays.restore_user_lvar_settings
   ida_hexrays.save_user_lvar_settings
   ida_hexrays.modify_user_lvars
   ida_hexrays.modify_user_lvar_info
   ida_hexrays.locate_lvar
   ida_hexrays.rename_lvar
   ida_hexrays.restore_user_defined_calls
   ida_hexrays.save_user_defined_calls
   ida_hexrays.parse_user_call
   ida_hexrays.convert_to_user_call
   ida_hexrays.install_microcode_filter
   ida_hexrays.get_temp_regs
   ida_hexrays.is_kreg
   ida_hexrays.reg2mreg
   ida_hexrays.mreg2reg
   ida_hexrays.get_mreg_name
   ida_hexrays.lexcompare
   ida_hexrays.getf_reginsn
   ida_hexrays.getb_reginsn
   ida_hexrays.change_hexrays_config
   ida_hexrays.get_hexrays_version
   ida_hexrays.open_pseudocode
   ida_hexrays.close_pseudocode
   ida_hexrays.decompile_many
   ida_hexrays.send_database
   ida_hexrays.get_current_operand
   ida_hexrays.remitem
   ida_hexrays.negated_relation
   ida_hexrays.swapped_relation
   ida_hexrays.get_op_signness
   ida_hexrays.asgop
   ida_hexrays.asgop_revert
   ida_hexrays.op_uses_x
   ida_hexrays.op_uses_y
   ida_hexrays.op_uses_z
   ida_hexrays.is_binary
   ida_hexrays.is_unary
   ida_hexrays.is_relational
   ida_hexrays.is_assignment
   ida_hexrays.accepts_udts
   ida_hexrays.is_prepost
   ida_hexrays.is_commutative
   ida_hexrays.is_additive
   ida_hexrays.is_multiplicative
   ida_hexrays.is_bitop
   ida_hexrays.is_logical
   ida_hexrays.is_loop
   ida_hexrays.is_break_consumer
   ida_hexrays.is_lvalue
   ida_hexrays.accepts_small_udts
   ida_hexrays.save_user_labels
   ida_hexrays.save_user_cmts
   ida_hexrays.save_user_numforms
   ida_hexrays.save_user_iflags
   ida_hexrays.save_user_unions
   ida_hexrays.restore_user_labels
   ida_hexrays.restore_user_cmts
   ida_hexrays.restore_user_numforms
   ida_hexrays.restore_user_iflags
   ida_hexrays.restore_user_unions
   ida_hexrays.close_hexrays_waitbox
   ida_hexrays.decompile
   ida_hexrays.decompile_func
   ida_hexrays.gen_microcode
   ida_hexrays.create_empty_mba
   ida_hexrays.create_cfunc
   ida_hexrays.mark_cfunc_dirty
   ida_hexrays.clear_cached_cfuncs
   ida_hexrays.has_cached_cfunc
   ida_hexrays.get_ctype_name
   ida_hexrays.create_field_name
   ida_hexrays.select_udt_by_offset
   ida_hexrays.user_numforms_first
   ida_hexrays.user_numforms_second
   ida_hexrays.user_numforms_find
   ida_hexrays.user_numforms_insert
   ida_hexrays.user_numforms_begin
   ida_hexrays.user_numforms_end
   ida_hexrays.user_numforms_next
   ida_hexrays.user_numforms_prev
   ida_hexrays.user_numforms_erase
   ida_hexrays.user_numforms_clear
   ida_hexrays.user_numforms_size
   ida_hexrays.user_numforms_free
   ida_hexrays.user_numforms_new
   ida_hexrays.lvar_mapping_first
   ida_hexrays.lvar_mapping_second
   ida_hexrays.lvar_mapping_find
   ida_hexrays.lvar_mapping_insert
   ida_hexrays.lvar_mapping_begin
   ida_hexrays.lvar_mapping_end
   ida_hexrays.lvar_mapping_next
   ida_hexrays.lvar_mapping_prev
   ida_hexrays.lvar_mapping_erase
   ida_hexrays.lvar_mapping_clear
   ida_hexrays.lvar_mapping_size
   ida_hexrays.lvar_mapping_free
   ida_hexrays.lvar_mapping_new
   ida_hexrays.udcall_map_first
   ida_hexrays.udcall_map_second
   ida_hexrays.udcall_map_find
   ida_hexrays.udcall_map_insert
   ida_hexrays.udcall_map_begin
   ida_hexrays.udcall_map_end
   ida_hexrays.udcall_map_next
   ida_hexrays.udcall_map_prev
   ida_hexrays.udcall_map_erase
   ida_hexrays.udcall_map_clear
   ida_hexrays.udcall_map_size
   ida_hexrays.udcall_map_free
   ida_hexrays.udcall_map_new
   ida_hexrays.user_cmts_first
   ida_hexrays.user_cmts_second
   ida_hexrays.user_cmts_find
   ida_hexrays.user_cmts_insert
   ida_hexrays.user_cmts_begin
   ida_hexrays.user_cmts_end
   ida_hexrays.user_cmts_next
   ida_hexrays.user_cmts_prev
   ida_hexrays.user_cmts_erase
   ida_hexrays.user_cmts_clear
   ida_hexrays.user_cmts_size
   ida_hexrays.user_cmts_free
   ida_hexrays.user_cmts_new
   ida_hexrays.user_iflags_first
   ida_hexrays.user_iflags_find
   ida_hexrays.user_iflags_insert
   ida_hexrays.user_iflags_begin
   ida_hexrays.user_iflags_end
   ida_hexrays.user_iflags_next
   ida_hexrays.user_iflags_prev
   ida_hexrays.user_iflags_erase
   ida_hexrays.user_iflags_clear
   ida_hexrays.user_iflags_size
   ida_hexrays.user_iflags_free
   ida_hexrays.user_iflags_new
   ida_hexrays.user_unions_first
   ida_hexrays.user_unions_second
   ida_hexrays.user_unions_find
   ida_hexrays.user_unions_insert
   ida_hexrays.user_unions_begin
   ida_hexrays.user_unions_end
   ida_hexrays.user_unions_next
   ida_hexrays.user_unions_prev
   ida_hexrays.user_unions_erase
   ida_hexrays.user_unions_clear
   ida_hexrays.user_unions_size
   ida_hexrays.user_unions_free
   ida_hexrays.user_unions_new
   ida_hexrays.user_labels_first
   ida_hexrays.user_labels_second
   ida_hexrays.user_labels_find
   ida_hexrays.user_labels_insert
   ida_hexrays.user_labels_begin
   ida_hexrays.user_labels_end
   ida_hexrays.user_labels_next
   ida_hexrays.user_labels_prev
   ida_hexrays.user_labels_erase
   ida_hexrays.user_labels_clear
   ida_hexrays.user_labels_size
   ida_hexrays.user_labels_free
   ida_hexrays.user_labels_new
   ida_hexrays.eamap_first
   ida_hexrays.eamap_second
   ida_hexrays.eamap_find
   ida_hexrays.eamap_insert
   ida_hexrays.eamap_begin
   ida_hexrays.eamap_end
   ida_hexrays.eamap_next
   ida_hexrays.eamap_prev
   ida_hexrays.eamap_erase
   ida_hexrays.eamap_clear
   ida_hexrays.eamap_size
   ida_hexrays.eamap_free
   ida_hexrays.eamap_new
   ida_hexrays.boundaries_first
   ida_hexrays.boundaries_second
   ida_hexrays.boundaries_begin
   ida_hexrays.boundaries_end
   ida_hexrays.boundaries_next
   ida_hexrays.boundaries_prev
   ida_hexrays.boundaries_erase
   ida_hexrays.boundaries_clear
   ida_hexrays.boundaries_size
   ida_hexrays.boundaries_free
   ida_hexrays.boundaries_new
   ida_hexrays.block_chains_get
   ida_hexrays.block_chains_find
   ida_hexrays.block_chains_insert
   ida_hexrays.block_chains_begin
   ida_hexrays.block_chains_end
   ida_hexrays.block_chains_next
   ida_hexrays.block_chains_prev
   ida_hexrays.block_chains_erase
   ida_hexrays.block_chains_clear
   ida_hexrays.block_chains_size
   ida_hexrays.block_chains_free
   ida_hexrays.block_chains_new
   ida_hexrays.decompile
   ida_hexrays.citem_to_specific_type
   ida_hexrays.property_op_to_typename
   ida_hexrays.cexpr_operands
   ida_hexrays.cinsn_details
   ida_hexrays.cfunc_type
   ida_hexrays.lnot
   ida_hexrays.make_ref
   ida_hexrays.dereference
   ida_hexrays.call_helper
   ida_hexrays.new_block
   ida_hexrays.make_num
   ida_hexrays.create_helper
   ida_hexrays.install_hexrays_callback
   ida_hexrays.remove_hexrays_callback


Module Contents
---------------

.. py:class:: array_of_bitsets(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> bitset_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> bitset_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: array_of_bitsets) -> None


   .. py:method:: extract() -> bitset_t *


   .. py:method:: inject(s: bitset_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< bitset_t >::const_iterator


   .. py:method:: end(*args) -> qvector< bitset_t >::const_iterator


   .. py:method:: insert(it: bitset_t, x: bitset_t) -> qvector< bitset_t >::iterator


   .. py:method:: erase(*args) -> qvector< bitset_t >::iterator


   .. py:method:: find(*args) -> qvector< bitset_t >::const_iterator


   .. py:method:: has(x: bitset_t) -> bool


   .. py:method:: add_unique(x: bitset_t) -> bool


   .. py:method:: append(x: bitset_t) -> None


   .. py:method:: extend(x: array_of_bitsets) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: mopvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> mop_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> mop_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: mopvec_t) -> None


   .. py:method:: extract() -> mop_t *


   .. py:method:: inject(s: mop_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< mop_t >::const_iterator


   .. py:method:: end(*args) -> qvector< mop_t >::const_iterator


   .. py:method:: insert(it: mop_t, x: mop_t) -> qvector< mop_t >::iterator


   .. py:method:: erase(*args) -> qvector< mop_t >::iterator


   .. py:method:: find(*args) -> qvector< mop_t >::const_iterator


   .. py:method:: has(x: mop_t) -> bool


   .. py:method:: add_unique(x: mop_t) -> bool


   .. py:method:: append(x: mop_t) -> None


   .. py:method:: extend(x: mopvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: mcallargs_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> mcallarg_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> mcallarg_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: mcallargs_t) -> None


   .. py:method:: extract() -> mcallarg_t *


   .. py:method:: inject(s: mcallarg_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< mcallarg_t >::const_iterator


   .. py:method:: end(*args) -> qvector< mcallarg_t >::const_iterator


   .. py:method:: insert(it: mcallarg_t, x: mcallarg_t) -> qvector< mcallarg_t >::iterator


   .. py:method:: erase(*args) -> qvector< mcallarg_t >::iterator


   .. py:method:: find(*args) -> qvector< mcallarg_t >::const_iterator


   .. py:method:: has(x: mcallarg_t) -> bool


   .. py:method:: add_unique(x: mcallarg_t) -> bool


   .. py:method:: append(x: mcallarg_t) -> None


   .. py:method:: extend(x: mcallargs_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: block_chains_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> block_chains_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> block_chains_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: block_chains_vec_t) -> None


   .. py:method:: extract() -> block_chains_t *


   .. py:method:: inject(s: block_chains_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< block_chains_t >::const_iterator


   .. py:method:: end(*args) -> qvector< block_chains_t >::const_iterator


   .. py:method:: insert(it: block_chains_t, x: block_chains_t) -> qvector< block_chains_t >::iterator


   .. py:method:: erase(*args) -> qvector< block_chains_t >::iterator


   .. py:method:: append(x: block_chains_t) -> None


   .. py:method:: extend(x: block_chains_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: user_numforms_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: at(_Keyval: operand_locator_t) -> number_format_t &


   .. py:method:: size() -> size_t


.. py:class:: lvar_mapping_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: at(_Keyval: lvar_locator_t) -> lvar_locator_t &


   .. py:method:: size() -> size_t


.. py:class:: hexwarns_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> hexwarn_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> hexwarn_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: hexwarns_t) -> None


   .. py:method:: extract() -> hexwarn_t *


   .. py:method:: inject(s: hexwarn_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< hexwarn_t >::const_iterator


   .. py:method:: end(*args) -> qvector< hexwarn_t >::const_iterator


   .. py:method:: insert(it: hexwarn_t, x: hexwarn_t) -> qvector< hexwarn_t >::iterator


   .. py:method:: erase(*args) -> qvector< hexwarn_t >::iterator


   .. py:method:: find(*args) -> qvector< hexwarn_t >::const_iterator


   .. py:method:: has(x: hexwarn_t) -> bool


   .. py:method:: add_unique(x: hexwarn_t) -> bool


   .. py:method:: append(x: hexwarn_t) -> None


   .. py:method:: extend(x: hexwarns_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: ctree_items_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> citem_t *&


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> citem_t *const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: ctree_items_t) -> None


   .. py:method:: extract() -> citem_t **


   .. py:method:: inject(s: citem_t **, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< citem_t * >::const_iterator


   .. py:method:: end(*args) -> qvector< citem_t * >::const_iterator


   .. py:method:: insert(it: qvector< citem_t * >::iterator, x: citem_t) -> qvector< citem_t * >::iterator


   .. py:method:: erase(*args) -> qvector< citem_t * >::iterator


   .. py:method:: find(*args) -> qvector< citem_t * >::const_iterator


   .. py:method:: has(x: citem_t) -> bool


   .. py:method:: add_unique(x: citem_t) -> bool


   .. py:method:: append(x: citem_t) -> None


   .. py:method:: extend(x: ctree_items_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: user_labels_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: at(_Keyval: int const &) -> _qstring< char > &


   .. py:method:: size() -> size_t


.. py:class:: user_cmts_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: at(_Keyval: treeloc_t) -> citem_cmt_t &


   .. py:method:: size() -> size_t


.. py:class:: user_iflags_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: at(_Keyval: citem_locator_t) -> int &


   .. py:method:: size() -> size_t


.. py:class:: user_unions_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: at(_Keyval: unsigned long long const &) -> qvector< int > &


   .. py:method:: size() -> size_t


.. py:class:: cinsnptrvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> cinsn_t *&


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> cinsn_t *const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: cinsnptrvec_t) -> None


   .. py:method:: extract() -> cinsn_t **


   .. py:method:: inject(s: cinsn_t **, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< cinsn_t * >::const_iterator


   .. py:method:: end(*args) -> qvector< cinsn_t * >::const_iterator


   .. py:method:: insert(it: qvector< cinsn_t * >::iterator, x: cinsn_t) -> qvector< cinsn_t * >::iterator


   .. py:method:: erase(*args) -> qvector< cinsn_t * >::iterator


   .. py:method:: find(*args) -> qvector< cinsn_t * >::const_iterator


   .. py:method:: has(x: cinsn_t) -> bool


   .. py:method:: add_unique(x: cinsn_t) -> bool


   .. py:method:: append(x: cinsn_t) -> None


   .. py:method:: extend(x: cinsnptrvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: eamap_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: at(_Keyval: unsigned long long const &) -> cinsnptrvec_t &


   .. py:method:: size() -> size_t


.. py:class:: boundaries_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: at(_Keyval: cinsn_t) -> rangeset_t &


   .. py:method:: size() -> size_t


.. py:function:: user_iflags_second(p: user_iflags_iterator_t) -> int32 const &

   Get reference to the current map value.


.. py:class:: cfuncptr_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: reset() -> None


   .. py:attribute:: entry_ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: mba
      :type:  mba_t *


   .. py:attribute:: body
      :type:  cinsn_t


   .. py:attribute:: argidx
      :type:  intvec_t &


   .. py:attribute:: maturity
      :type:  ctree_maturity_t


   .. py:attribute:: user_labels
      :type:  user_labels_t *


   .. py:attribute:: user_cmts
      :type:  user_cmts_t *


   .. py:attribute:: numforms
      :type:  user_numforms_t *


   .. py:attribute:: user_iflags
      :type:  user_iflags_t *


   .. py:attribute:: user_unions
      :type:  user_unions_t *


   .. py:attribute:: refcnt
      :type:  int


   .. py:attribute:: statebits
      :type:  int


   .. py:attribute:: hdrlines
      :type:  int


   .. py:attribute:: treeitems
      :type:  citem_pointers_t


   .. py:method:: release() -> None


   .. py:method:: build_c_tree() -> None


   .. py:method:: verify(aul: allow_unused_labels_t, even_without_debugger: bool) -> None


   .. py:method:: print_dcl() -> None


   .. py:method:: print_func(vp: vc_printer_t) -> None


   .. py:method:: get_func_type(type: tinfo_t) -> bool


   .. py:method:: get_lvars() -> lvars_t *


   .. py:method:: get_stkoff_delta() -> int


   .. py:method:: find_label(label: int) -> citem_t *


   .. py:method:: remove_unused_labels() -> None


   .. py:method:: get_user_cmt(loc: treeloc_t, rt: cmt_retrieval_type_t) -> str


   .. py:method:: set_user_cmt(loc: treeloc_t, cmt: str) -> None


   .. py:method:: get_user_iflags(loc: citem_locator_t) -> int


   .. py:method:: set_user_iflags(loc: citem_locator_t, iflags: int) -> None


   .. py:method:: has_orphan_cmts() -> bool


   .. py:method:: del_orphan_cmts() -> int


   .. py:method:: get_user_union_selection(ea: ida_idaapi.ea_t, path: intvec_t) -> bool


   .. py:method:: set_user_union_selection(ea: ida_idaapi.ea_t, path: intvec_t) -> None


   .. py:method:: save_user_labels() -> None

      Save user defined labels into the database. 
              



   .. py:method:: save_user_cmts() -> None

      Save user defined comments into the database. 
              



   .. py:method:: save_user_numforms() -> None

      Save user defined number formats into the database. 
              



   .. py:method:: save_user_iflags() -> None

      Save user defined citem iflags into the database. 
              



   .. py:method:: save_user_unions() -> None

      Save user defined union field selections into the database. 
              



   .. py:method:: get_line_item(line: str, x: int, is_ctree_line: bool, phead: ctree_item_t, pitem: ctree_item_t, ptail: ctree_item_t) -> bool


   .. py:method:: get_warnings() -> hexwarns_t &


   .. py:method:: get_eamap() -> eamap_t &


   .. py:method:: get_boundaries() -> boundaries_t &


   .. py:method:: get_pseudocode() -> strvec_t const &


   .. py:method:: refresh_func_ctext() -> None


   .. py:method:: recalc_item_addresses() -> None


   .. py:method:: gather_derefs(ci: ctree_item_t, udm: udt_type_data_t = None) -> bool


   .. py:method:: find_item_coords(*args)

      This method has the following signatures:

          1. find_item_coords(item: citem_t) -> Tuple[int, int]
          2. find_item_coords(item: citem_t, x: int_pointer, y: int_pointer) -> bool

      NOTE: The second form is retained for backward-compatibility,
      but we strongly recommend using the first.

      :param item: The item to find coordinates for in the pseudocode listing



   .. py:method:: locked() -> bool


.. py:class:: qvector_history_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> history_item_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> history_item_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: qvector_history_t) -> None


   .. py:method:: extract() -> history_item_t *


   .. py:method:: inject(s: history_item_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< history_item_t >::const_iterator


   .. py:method:: end(*args) -> qvector< history_item_t >::const_iterator


   .. py:method:: insert(it: history_item_t, x: history_item_t) -> qvector< history_item_t >::iterator


   .. py:method:: erase(*args) -> qvector< history_item_t >::iterator


   .. py:method:: find(*args) -> qvector< history_item_t >::const_iterator


   .. py:method:: has(x: history_item_t) -> bool


   .. py:method:: add_unique(x: history_item_t) -> bool


   .. py:method:: append(x: history_item_t) -> None


   .. py:method:: extend(x: qvector_history_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: history_t

   Bases: :py:obj:`qvector_history_t`


   .. py:attribute:: thisown


   .. py:method:: pop() -> history_item_t


   .. py:method:: top(*args) -> history_item_t &


   .. py:method:: push(v: history_item_t) -> None


.. py:class:: cinsn_list_t_iterator

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: cur
      :type:  cinsn_t const &


   .. py:attribute:: next


.. py:class:: cinsn_list_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: swap(x: cinsn_list_t) -> None


   .. py:method:: empty() -> bool


   .. py:method:: size() -> size_t


   .. py:method:: front(*args) -> cinsn_t const &


   .. py:method:: back(*args) -> cinsn_t const &


   .. py:method:: rbegin(*args) -> qlist< cinsn_t >::const_reverse_iterator


   .. py:method:: rend(*args) -> qlist< cinsn_t >::const_reverse_iterator


   .. py:method:: push_front(x: cinsn_t) -> None


   .. py:method:: push_back(*args) -> cinsn_t &


   .. py:method:: clear() -> None


   .. py:method:: pop_front() -> None


   .. py:method:: pop_back() -> None


   .. py:method:: splice(pos: qlist< cinsn_t >::iterator, other: cinsn_list_t, first: qlist< cinsn_t >::iterator, last: qlist< cinsn_t >::iterator) -> None


   .. py:method:: remove(v: cinsn_t) -> bool


   .. py:method:: find(item)


   .. py:method:: index(item)


   .. py:method:: at(index)


   .. py:method:: begin() -> cinsn_list_t_iterator


   .. py:method:: end() -> cinsn_list_t_iterator


   .. py:method:: insert(*args) -> cinsn_list_t_iterator


   .. py:method:: erase(p: cinsn_list_t_iterator) -> None


.. py:class:: qvector_lvar_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> lvar_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> lvar_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: qvector_lvar_t) -> None


   .. py:method:: extract() -> lvar_t *


   .. py:method:: inject(s: lvar_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< lvar_t >::const_iterator


   .. py:method:: end(*args) -> qvector< lvar_t >::const_iterator


   .. py:method:: insert(it: lvar_t, x: lvar_t) -> qvector< lvar_t >::iterator


   .. py:method:: erase(*args) -> qvector< lvar_t >::iterator


   .. py:method:: find(*args) -> qvector< lvar_t >::const_iterator


   .. py:method:: has(x: lvar_t) -> bool


   .. py:method:: add_unique(x: lvar_t) -> bool


   .. py:method:: append(x: lvar_t) -> None


   .. py:method:: extend(x: qvector_lvar_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: qvector_carg_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> carg_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> carg_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: qvector_carg_t) -> None


   .. py:method:: extract() -> carg_t *


   .. py:method:: inject(s: carg_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< carg_t >::const_iterator


   .. py:method:: end(*args) -> qvector< carg_t >::const_iterator


   .. py:method:: insert(it: carg_t, x: carg_t) -> qvector< carg_t >::iterator


   .. py:method:: erase(*args) -> qvector< carg_t >::iterator


   .. py:method:: find(*args) -> qvector< carg_t >::const_iterator


   .. py:method:: has(x: carg_t) -> bool


   .. py:method:: add_unique(x: carg_t) -> bool


   .. py:method:: append(x: carg_t) -> None


   .. py:method:: extend(x: qvector_carg_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: qvector_ccase_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> ccase_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> ccase_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: qvector_ccase_t) -> None


   .. py:method:: extract() -> ccase_t *


   .. py:method:: inject(s: ccase_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< ccase_t >::const_iterator


   .. py:method:: end(*args) -> qvector< ccase_t >::const_iterator


   .. py:method:: insert(it: ccase_t, x: ccase_t) -> qvector< ccase_t >::iterator


   .. py:method:: erase(*args) -> qvector< ccase_t >::iterator


   .. py:method:: find(*args) -> qvector< ccase_t >::const_iterator


   .. py:method:: has(x: ccase_t) -> bool


   .. py:method:: add_unique(x: ccase_t) -> bool


   .. py:method:: append(x: ccase_t) -> None


   .. py:method:: extend(x: qvector_ccase_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: qvector_catchexprs_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> catchexpr_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> catchexpr_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: qvector_catchexprs_t) -> None


   .. py:method:: extract() -> catchexpr_t *


   .. py:method:: inject(s: catchexpr_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< catchexpr_t >::const_iterator


   .. py:method:: end(*args) -> qvector< catchexpr_t >::const_iterator


   .. py:method:: insert(it: catchexpr_t, x: catchexpr_t) -> qvector< catchexpr_t >::iterator


   .. py:method:: erase(*args) -> qvector< catchexpr_t >::iterator


   .. py:method:: find(*args) -> qvector< catchexpr_t >::const_iterator


   .. py:method:: has(x: catchexpr_t) -> bool


   .. py:method:: add_unique(x: catchexpr_t) -> bool


   .. py:method:: append(x: catchexpr_t) -> None


   .. py:method:: extend(x: qvector_catchexprs_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: qvector_ccatchvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> ccatch_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> ccatch_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: qvector_ccatchvec_t) -> None


   .. py:method:: extract() -> ccatch_t *


   .. py:method:: inject(s: ccatch_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< ccatch_t >::const_iterator


   .. py:method:: end(*args) -> qvector< ccatch_t >::const_iterator


   .. py:method:: insert(it: ccatch_t, x: ccatch_t) -> qvector< ccatch_t >::iterator


   .. py:method:: erase(*args) -> qvector< ccatch_t >::iterator


   .. py:method:: find(*args) -> qvector< ccatch_t >::const_iterator


   .. py:method:: has(x: ccatch_t) -> bool


   .. py:method:: add_unique(x: ccatch_t) -> bool


   .. py:method:: append(x: ccatch_t) -> None


   .. py:method:: extend(x: qvector_ccatchvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: cblock_posvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> cblock_pos_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> cblock_pos_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: cblock_posvec_t) -> None


   .. py:method:: extract() -> cblock_pos_t *


   .. py:method:: inject(s: cblock_pos_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< cblock_pos_t >::const_iterator


   .. py:method:: end(*args) -> qvector< cblock_pos_t >::const_iterator


   .. py:method:: insert(it: cblock_pos_t, x: cblock_pos_t) -> qvector< cblock_pos_t >::iterator


   .. py:method:: erase(*args) -> qvector< cblock_pos_t >::iterator


   .. py:method:: append(x: cblock_pos_t) -> None


   .. py:method:: extend(x: cblock_posvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: lvar_saved_infos_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> lvar_saved_info_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> lvar_saved_info_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: lvar_saved_infos_t) -> None


   .. py:method:: extract() -> lvar_saved_info_t *


   .. py:method:: inject(s: lvar_saved_info_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< lvar_saved_info_t >::const_iterator


   .. py:method:: end(*args) -> qvector< lvar_saved_info_t >::const_iterator


   .. py:method:: insert(it: lvar_saved_info_t, x: lvar_saved_info_t) -> qvector< lvar_saved_info_t >::iterator


   .. py:method:: erase(*args) -> qvector< lvar_saved_info_t >::iterator


   .. py:method:: find(*args) -> qvector< lvar_saved_info_t >::const_iterator


   .. py:method:: has(x: lvar_saved_info_t) -> bool


   .. py:method:: add_unique(x: lvar_saved_info_t) -> bool


   .. py:method:: append(x: lvar_saved_info_t) -> None


   .. py:method:: extend(x: lvar_saved_infos_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: ui_stroff_ops_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> ui_stroff_op_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> ui_stroff_op_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: ui_stroff_ops_t) -> None


   .. py:method:: extract() -> ui_stroff_op_t *


   .. py:method:: inject(s: ui_stroff_op_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< ui_stroff_op_t >::const_iterator


   .. py:method:: end(*args) -> qvector< ui_stroff_op_t >::const_iterator


   .. py:method:: insert(it: ui_stroff_op_t, x: ui_stroff_op_t) -> qvector< ui_stroff_op_t >::iterator


   .. py:method:: erase(*args) -> qvector< ui_stroff_op_t >::iterator


   .. py:method:: find(*args) -> qvector< ui_stroff_op_t >::const_iterator


   .. py:method:: has(x: ui_stroff_op_t) -> bool


   .. py:method:: add_unique(x: ui_stroff_op_t) -> bool


   .. py:method:: append(x: ui_stroff_op_t) -> None


   .. py:method:: extend(x: ui_stroff_ops_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:function:: qswap(a: cinsn_t, b: cinsn_t) -> None

.. py:function:: debug_hexrays_ctree(level: int, msg: str) -> None

.. py:function:: init_hexrays_plugin(flags: int = 0) -> bool

   Check that your plugin is compatible with hex-rays decompiler. This function must be called before calling any other decompiler function. 
           
   :param flags: reserved, must be 0
   :returns: true if the decompiler exists and is compatible with your plugin


.. py:function:: get_widget_vdui(f: TWidget *) -> vdui_t *

   Get the vdui_t instance associated to the TWidget 
           
   :param f: pointer to window
   :returns: a vdui_t *, or nullptr


.. py:function:: boundaries_find(map: boundaries_t, key: cinsn_t) -> boundaries_iterator_t

   Find the specified key in boundaries_t.


.. py:function:: boundaries_insert(map: boundaries_t, key: cinsn_t, val: rangeset_t) -> boundaries_iterator_t

   Insert new (cinsn_t *, rangeset_t) pair into boundaries_t.


.. py:function:: term_hexrays_plugin() -> None

   Stop working with hex-rays decompiler.


.. py:class:: Hexrays_Hooks(_flags: int = 0, _hkcb_flags: int = 1)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: hook() -> bool


   .. py:method:: unhook() -> bool


   .. py:method:: flowchart(fc: qflow_chart_t, mba: mba_t, reachable_blocks: bitset_t, decomp_flags: int) -> int

      Flowchart has been generated. 
                
      :param fc: (qflow_chart_t *)
      :param mba: (mba_t *)
      :param reachable_blocks: (bitset_t *)
      :param decomp_flags: (int)
      :returns: Microcode error code



   .. py:method:: stkpnts(mba: mba_t, _sps: stkpnts_t *) -> int

      SP change points have been calculated. 
                
      :param mba: (mba_t *)
      :returns: Microcode error code This event is generated for each inlined range as well.



   .. py:method:: prolog(mba: mba_t, fc: qflow_chart_t, reachable_blocks: bitset_t, decomp_flags: int) -> int

      Prolog analysis has been finished. 
                
      :param mba: (mba_t *)
      :param fc: (qflow_chart_t *)
      :param reachable_blocks: (const bitset_t *)
      :param decomp_flags: (int)
      :returns: Microcode error code This event is generated for each inlined range as well.



   .. py:method:: microcode(mba: mba_t) -> int

      Microcode has been generated. 
                
      :param mba: (mba_t *)
      :returns: Microcode error code



   .. py:method:: preoptimized(mba: mba_t) -> int

      Microcode has been preoptimized. 
                
      :param mba: (mba_t *)
      :returns: Microcode error code



   .. py:method:: locopt(mba: mba_t) -> int

      Basic block level optimization has been finished. 
                
      :param mba: (mba_t *)
      :returns: Microcode error code



   .. py:method:: prealloc(mba: mba_t) -> int

      Local variables: preallocation step begins. 
                
      :param mba: (mba_t *) This event may occur several times. Should return: 1 if modified microcode Negative values are Microcode error code



   .. py:method:: glbopt(mba: mba_t) -> int

      Global optimization has been finished. If microcode is modified, MERR_LOOP must be returned. It will cause a complete restart of the optimization. 
                
      :param mba: (mba_t *)
      :returns: Microcode error code



   .. py:method:: pre_structural(ct: control_graph_t *, cfunc: cfunc_t, g: simple_graph_t) -> int

      Structure analysis is starting. 
                
      :param ct: (control_graph_t *) in/out: control graph
      :param cfunc: (cfunc_t *) in: the current function
      :param g: (const simple_graph_t *) in: control flow graph
      :returns: Microcode error code; MERR_BLOCK means that the analysis has been performed by a plugin



   .. py:method:: structural(ct: control_graph_t *) -> int

      Structural analysis has been finished. 
                
      :param ct: (control_graph_t *)



   .. py:method:: maturity(cfunc: cfunc_t, new_maturity: ctree_maturity_t) -> int

      Ctree maturity level is being changed. 
                
      :param cfunc: (cfunc_t *)
      :param new_maturity: (ctree_maturity_t)



   .. py:method:: interr(errcode: int) -> int

      Internal error has occurred. 
                
      :param errcode: (int )



   .. py:method:: combine(blk: mblock_t, insn: minsn_t) -> int

      Trying to combine instructions of basic block. 
                
      :param blk: (mblock_t *)
      :param insn: (minsn_t *) Should return: 1 if combined the current instruction with a preceding one -1 if the instruction should not be combined 0 else



   .. py:method:: print_func(cfunc: cfunc_t, vp: vc_printer_t) -> int

      Printing ctree and generating text. 
                
      :param cfunc: (cfunc_t *)
      :param vp: (vc_printer_t *) Returns: 1 if text has been generated by the plugin It is forbidden to modify ctree at this event.



   .. py:method:: func_printed(cfunc: cfunc_t) -> int

      Function text has been generated. Plugins may modify the text in cfunc_t::sv. However, it is too late to modify the ctree or microcode. The text uses regular color codes (see lines.hpp) COLOR_ADDR is used to store pointers to ctree items. 
                
      :param cfunc: (cfunc_t *)



   .. py:method:: resolve_stkaddrs(mba: mba_t) -> int

      The optimizer is about to resolve stack addresses. 
                
      :param mba: (mba_t *)



   .. py:method:: build_callinfo(blk: mblock_t, type: tinfo_t) -> PyObject *

      Analyzing a call instruction. 
                
      :param blk: (mblock_t *) blk->tail is the call.
      :param type: (tinfo_t *) buffer for the output type.



   .. py:method:: callinfo_built(blk: mblock_t) -> int

      A call instruction has been anallyzed. 
                
      :param blk: (mblock_t *) blk->tail is the call.



   .. py:method:: calls_done(mba: mba_t) -> int

      All calls have been analyzed. 
                
      :param mba: (mba_t *) This event is generated immediately after analyzing all calls, before any optimizitions, call unmerging and block merging.



   .. py:method:: begin_inlining(cdg: codegen_t, decomp_flags: int) -> int

      Starting to inline outlined functions. 
                
      :param cdg: (codegen_t *)
      :param decomp_flags: (int)
      :returns: Microcode error code This is an opportunity to inline other ranges.



   .. py:method:: inlining_func(cdg: codegen_t, blk: int, mbr: mba_ranges_t) -> int

      A set of ranges is going to be inlined. 
                
      :param cdg: (codegen_t *)
      :param blk: (int) the block containing call/jump to inline
      :param mbr: (mba_ranges_t *) the range to inline



   .. py:method:: inlined_func(cdg: codegen_t, blk: int, mbr: mba_ranges_t, i1: int, i2: int) -> int

      A set of ranges got inlined. 
                
      :param cdg: (codegen_t *)
      :param blk: (int) the block containing call/jump to inline
      :param mbr: (mba_ranges_t *) the range to inline
      :param i1: (int) blknum of the first inlined block
      :param i2: (int) blknum of the last inlined block (excluded)



   .. py:method:: collect_warnings(cfunc: cfunc_t) -> int

      Collect warning messages from plugins. These warnings will be displayed at the function header, after the user-defined comments. 
                
      :param cfunc: (cfunc_t *)



   .. py:method:: open_pseudocode(vu: vdui_t) -> int

      New pseudocode view has been opened. 
                
      :param vu: (vdui_t *)



   .. py:method:: switch_pseudocode(vu: vdui_t) -> int

      Existing pseudocode view has been reloaded with a new function. Its text has not been refreshed yet, only cfunc and mba pointers are ready. 
                
      :param vu: (vdui_t *)



   .. py:method:: refresh_pseudocode(vu: vdui_t) -> int

      Existing pseudocode text has been refreshed. Adding/removing pseudocode lines is forbidden in this event. 
                
      :param vu: (vdui_t *) See also hxe_text_ready, which happens earlier



   .. py:method:: close_pseudocode(vu: vdui_t) -> int

      Pseudocode view is being closed. 
                
      :param vu: (vdui_t *)



   .. py:method:: keyboard(vu: vdui_t, key_code: int, shift_state: int) -> int

      Keyboard has been hit. 
                
      :param vu: (vdui_t *)
      :param key_code: (int) VK_...
      :param shift_state: (int) Should return: 1 if the event has been handled



   .. py:method:: right_click(vu: vdui_t) -> int

      Mouse right click. Use hxe_populating_popup instead, in case you want to add items in the popup menu. 
                
      :param vu: (vdui_t *)



   .. py:method:: double_click(vu: vdui_t, shift_state: int) -> int

      Mouse double click. 
                
      :param vu: (vdui_t *)
      :param shift_state: (int) Should return: 1 if the event has been handled



   .. py:method:: curpos(vu: vdui_t) -> int

      Current cursor position has been changed. (for example, by left-clicking or using keyboard)

                
      :param vu: (vdui_t *)



   .. py:method:: create_hint(vu: vdui_t) -> PyObject *

      Create a hint for the current item. 
                
      :param vu: (vdui_t *)
      :returns: 0: continue collecting hints with other subscribers
      :returns: 1: stop collecting hints



   .. py:method:: text_ready(vu: vdui_t) -> int

      Decompiled text is ready. 
                
      :param vu: (vdui_t *) This event can be used to modify the output text (sv). Obsolete. Please use hxe_func_printed instead.



   .. py:method:: populating_popup(widget: TWidget *, popup_handle: TPopupMenu *, vu: vdui_t) -> int

      Populating popup menu. We can add menu items now. 
                
      :param widget: (TWidget *)
      :param popup_handle: (TPopupMenu *)
      :param vu: (vdui_t *)



   .. py:method:: lvar_name_changed(vu: vdui_t, v: lvar_t, name: str, is_user_name: bool) -> int

      Local variable got renamed. 
                
      :param vu: (vdui_t *)
      :param v: (lvar_t *)
      :param name: (const char *)
      :param is_user_name: (bool) Please note that it is possible to read/write user settings for lvars directly from the idb.



   .. py:method:: lvar_type_changed(vu: vdui_t, v: lvar_t, tinfo: tinfo_t) -> int

      Local variable type got changed. 
                
      :param vu: (vdui_t *)
      :param v: (lvar_t *)
      :param tinfo: (const tinfo_t *) Please note that it is possible to read/write user settings for lvars directly from the idb.



   .. py:method:: lvar_cmt_changed(vu: vdui_t, v: lvar_t, cmt: str) -> int

      Local variable comment got changed. 
                
      :param vu: (vdui_t *)
      :param v: (lvar_t *)
      :param cmt: (const char *) Please note that it is possible to read/write user settings for lvars directly from the idb.



   .. py:method:: lvar_mapping_changed(vu: vdui_t, frm: lvar_t, to: lvar_t) -> int

      Local variable mapping got changed. 
                
      :param vu: (vdui_t *)
      :param to: (lvar_t *) Please note that it is possible to read/write user settings for lvars directly from the idb.



   .. py:method:: cmt_changed(cfunc: cfunc_t, loc: treeloc_t, cmt: str) -> int

      Comment got changed. 
                
      :param cfunc: (cfunc_t *)
      :param loc: (const treeloc_t *)
      :param cmt: (const char *)



   .. py:method:: mba_maturity(mba: mba_t, reqmat: mba_maturity_t) -> int

      Maturity level of an MBA was changed. 
                
      :param mba: (mba_t *)
      :param reqmat: (mba_maturity_t) requested maturity level
      :returns: Microcode error code



.. py:class:: uval_ivl_t(_off: unsigned long long, _size: unsigned long long)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: off
      :type:  unsigned long long


   .. py:attribute:: size
      :type:  unsigned long long


   .. py:method:: valid() -> bool


   .. py:method:: end() -> unsigned long long


   .. py:method:: last() -> unsigned long long


.. py:class:: uval_ivl_ivlset_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: swap(r: uval_ivl_ivlset_t) -> None


   .. py:method:: getivl(idx: int) -> ivl_t const &


   .. py:method:: lastivl() -> ivl_t const &


   .. py:method:: nivls() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: clear() -> None


   .. py:method:: qclear() -> None


   .. py:method:: all_values() -> bool


   .. py:method:: set_all_values() -> None


   .. py:method:: single_value(*args) -> bool


   .. py:method:: begin(*args) -> ivlset_tpl< ivl_t,unsigned long long >::iterator


   .. py:method:: end(*args) -> ivlset_tpl< ivl_t,unsigned long long >::iterator


.. py:class:: array_of_ivlsets(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> ivlset_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> ivlset_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: array_of_ivlsets) -> None


   .. py:method:: extract() -> ivlset_t *


   .. py:method:: inject(s: ivlset_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< ivlset_t >::const_iterator


   .. py:method:: end(*args) -> qvector< ivlset_t >::const_iterator


   .. py:method:: insert(it: ivlset_t, x: ivlset_t) -> qvector< ivlset_t >::iterator


   .. py:method:: erase(*args) -> qvector< ivlset_t >::iterator


   .. py:method:: find(*args) -> qvector< ivlset_t >::const_iterator


   .. py:method:: has(x: ivlset_t) -> bool


   .. py:method:: add_unique(x: ivlset_t) -> bool


   .. py:method:: append(x: ivlset_t) -> None


   .. py:method:: extend(x: array_of_ivlsets) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:data:: MAX_SUPPORTED_STACK_SIZE

.. py:function:: hexrays_alloc(size: size_t) -> void *

.. py:function:: hexrays_free(ptr: void *) -> None

.. py:data:: MAX_VLR_SIZE

.. py:function:: max_vlr_value(size: int) -> uvlr_t

.. py:function:: min_vlr_svalue(size: int) -> uvlr_t

.. py:function:: max_vlr_svalue(size: int) -> uvlr_t

.. py:data:: CMP_NZ

.. py:data:: CMP_Z

.. py:data:: CMP_AE

.. py:data:: CMP_B

.. py:data:: CMP_A

.. py:data:: CMP_BE

.. py:data:: CMP_GT

.. py:data:: CMP_GE

.. py:data:: CMP_LT

.. py:data:: CMP_LE

.. py:function:: is_unsigned_cmpop(cmpop: cmpop_t) -> bool

.. py:function:: is_signed_cmpop(cmpop: cmpop_t) -> bool

.. py:function:: is_cmpop_with_eq(cmpop: cmpop_t) -> bool

.. py:function:: is_cmpop_without_eq(cmpop: cmpop_t) -> bool

.. py:class:: valrng_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: swap(r: valrng_t) -> None


   .. py:method:: compare(r: valrng_t) -> int


   .. py:method:: set_none() -> None


   .. py:method:: set_all() -> None


   .. py:method:: set_unk() -> None


   .. py:method:: set_eq(v: uvlr_t) -> None


   .. py:method:: set_cmp(cmp: cmpop_t, _value: uvlr_t) -> None


   .. py:method:: reduce_size(new_size: int) -> bool


   .. py:method:: intersect_with(r: valrng_t) -> bool


   .. py:method:: unite_with(r: valrng_t) -> bool


   .. py:method:: inverse() -> None


   .. py:method:: empty() -> bool


   .. py:method:: all_values() -> bool


   .. py:method:: is_unknown() -> bool


   .. py:method:: has(v: uvlr_t) -> bool


   .. py:method:: dstr() -> str


   .. py:method:: cvt_to_single_value() -> bool


   .. py:method:: cvt_to_cmp() -> bool


   .. py:method:: get_size() -> int


   .. py:method:: max_value() -> uvlr_t


   .. py:method:: min_svalue() -> uvlr_t


   .. py:method:: max_svalue() -> uvlr_t


.. py:data:: cvar

.. py:data:: MAX_VLR_VALUE

.. py:data:: MAX_VLR_SVALUE

.. py:data:: MIN_VLR_SVALUE

.. py:function:: is_may_access(maymust: maymust_t) -> bool

.. py:data:: MERR_OK

   ok


.. py:data:: MERR_BLOCK

   no error, switch to new block


.. py:data:: MERR_INTERR

   internal error


.. py:data:: MERR_INSN

   cannot convert to microcode


.. py:data:: MERR_MEM

   not enough memory


.. py:data:: MERR_BADBLK

   bad block found


.. py:data:: MERR_BADSP

   positive sp value has been found


.. py:data:: MERR_PROLOG

   prolog analysis failed


.. py:data:: MERR_SWITCH

   wrong switch idiom


.. py:data:: MERR_EXCEPTION

   exception analysis failed


.. py:data:: MERR_HUGESTACK

   stack frame is too big


.. py:data:: MERR_LVARS

   local variable allocation failed


.. py:data:: MERR_BITNESS

   16-bit functions cannot be decompiled


.. py:data:: MERR_BADCALL

   could not determine call arguments


.. py:data:: MERR_BADFRAME

   function frame is wrong


.. py:data:: MERR_UNKTYPE

   undefined type s (currently unused error code)


.. py:data:: MERR_BADIDB

   inconsistent database information


.. py:data:: MERR_SIZEOF

   wrong basic type sizes in compiler settings


.. py:data:: MERR_REDO

   redecompilation has been requested


.. py:data:: MERR_CANCELED

   decompilation has been cancelled


.. py:data:: MERR_RECDEPTH

   max recursion depth reached during lvar allocation


.. py:data:: MERR_OVERLAP

   variables would overlap: s


.. py:data:: MERR_PARTINIT

   partially initialized variable s


.. py:data:: MERR_COMPLEX

   too complex function


.. py:data:: MERR_LICENSE

   no license available


.. py:data:: MERR_ONLY32

   only 32-bit functions can be decompiled for the current database


.. py:data:: MERR_ONLY64

   only 64-bit functions can be decompiled for the current database


.. py:data:: MERR_BUSY

   already decompiling a function


.. py:data:: MERR_FARPTR

   far memory model is supported only for pc


.. py:data:: MERR_EXTERN

   special segments cannot be decompiled


.. py:data:: MERR_FUNCSIZE

   too big function


.. py:data:: MERR_BADRANGES

   bad input ranges


.. py:data:: MERR_BADARCH

   current architecture is not supported


.. py:data:: MERR_DSLOT

   bad instruction in the delay slot


.. py:data:: MERR_STOP

   no error, stop the analysis


.. py:data:: MERR_CLOUD

   cloud: s


.. py:data:: MERR_EMULATOR

   emulator: s


.. py:data:: MERR_MAX_ERR

.. py:data:: MERR_LOOP

   internal code: redo last loop (never reported)


.. py:function:: get_merror_desc(code: merror_t, mba: mba_t) -> str

   Get textual description of an error code 
           
   :param code: Microcode error code
   :param mba: the microcode array
   :returns: the error address


.. py:data:: m_nop

.. py:data:: m_stx

.. py:data:: m_ldx

.. py:data:: m_ldc

.. py:data:: m_mov

.. py:data:: m_neg

.. py:data:: m_lnot

.. py:data:: m_bnot

.. py:data:: m_xds

.. py:data:: m_xdu

.. py:data:: m_low

.. py:data:: m_high

.. py:data:: m_add

.. py:data:: m_sub

.. py:data:: m_mul

.. py:data:: m_udiv

.. py:data:: m_sdiv

.. py:data:: m_umod

.. py:data:: m_smod

.. py:data:: m_or

.. py:data:: m_and

.. py:data:: m_xor

.. py:data:: m_shl

.. py:data:: m_shr

.. py:data:: m_sar

.. py:data:: m_cfadd

.. py:data:: m_ofadd

.. py:data:: m_cfshl

.. py:data:: m_cfshr

.. py:data:: m_sets

.. py:data:: m_seto

.. py:data:: m_setp

.. py:data:: m_setnz

.. py:data:: m_setz

.. py:data:: m_setae

.. py:data:: m_setb

.. py:data:: m_seta

.. py:data:: m_setbe

.. py:data:: m_setg

.. py:data:: m_setge

.. py:data:: m_setl

.. py:data:: m_setle

.. py:data:: m_jcnd

.. py:data:: m_jnz

.. py:data:: m_jz

.. py:data:: m_jae

.. py:data:: m_jb

.. py:data:: m_ja

.. py:data:: m_jbe

.. py:data:: m_jg

.. py:data:: m_jge

.. py:data:: m_jl

.. py:data:: m_jle

.. py:data:: m_jtbl

.. py:data:: m_ijmp

.. py:data:: m_goto

.. py:data:: m_call

.. py:data:: m_icall

.. py:data:: m_ret

.. py:data:: m_push

.. py:data:: m_pop

.. py:data:: m_und

.. py:data:: m_ext

.. py:data:: m_f2i

.. py:data:: m_f2u

.. py:data:: m_i2f

.. py:data:: m_u2f

.. py:data:: m_f2f

.. py:data:: m_fneg

.. py:data:: m_fadd

.. py:data:: m_fsub

.. py:data:: m_fmul

.. py:data:: m_fdiv

.. py:function:: must_mcode_close_block(mcode: mcode_t, including_calls: bool) -> bool

   Must an instruction with the given opcode be the last one in a block? Such opcodes are called closing opcodes. 
           
   :param mcode: instruction opcode
   :param including_calls: should m_call/m_icall be considered as the closing opcodes? If this function returns true, the opcode cannot appear in the middle of a block. Calls are a special case: unknown calls (is_unknown_call) are considered as closing opcodes.


.. py:function:: is_mcode_propagatable(mcode: mcode_t) -> bool

   May opcode be propagated? Such opcodes can be used in sub-instructions (nested instructions) There is a handful of non-propagatable opcodes, like jumps, ret, nop, etc All other regular opcodes are propagatable and may appear in a nested instruction. 
           


.. py:function:: is_mcode_addsub(mcode: mcode_t) -> bool

.. py:function:: is_mcode_xdsu(mcode: mcode_t) -> bool

.. py:function:: is_mcode_set(mcode: mcode_t) -> bool

.. py:function:: is_mcode_set1(mcode: mcode_t) -> bool

.. py:function:: is_mcode_j1(mcode: mcode_t) -> bool

.. py:function:: is_mcode_jcond(mcode: mcode_t) -> bool

.. py:function:: is_mcode_convertible_to_jmp(mcode: mcode_t) -> bool

.. py:function:: is_mcode_convertible_to_set(mcode: mcode_t) -> bool

.. py:function:: is_mcode_call(mcode: mcode_t) -> bool

.. py:function:: is_mcode_fpu(mcode: mcode_t) -> bool

.. py:function:: is_mcode_commutative(mcode: mcode_t) -> bool

.. py:function:: is_mcode_shift(mcode: mcode_t) -> bool

.. py:function:: is_mcode_divmod(op: mcode_t) -> bool

.. py:function:: has_mcode_seloff(op: mcode_t) -> bool

.. py:function:: set2jcnd(code: mcode_t) -> mcode_t

.. py:function:: jcnd2set(code: mcode_t) -> mcode_t

.. py:function:: negate_mcode_relation(code: mcode_t) -> mcode_t

.. py:function:: swap_mcode_relation(code: mcode_t) -> mcode_t

.. py:function:: get_signed_mcode(code: mcode_t) -> mcode_t

.. py:function:: get_unsigned_mcode(code: mcode_t) -> mcode_t

.. py:function:: is_signed_mcode(code: mcode_t) -> bool

.. py:function:: is_unsigned_mcode(code: mcode_t) -> bool

.. py:function:: mcode_modifies_d(mcode: mcode_t) -> bool

.. py:class:: operand_locator_t(_ea: ida_idaapi.ea_t, _opnum: int)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      address of the original processor instruction



   .. py:attribute:: opnum
      :type:  int

      operand number in the instruction



   .. py:method:: compare(r: operand_locator_t) -> int


.. py:data:: MUST_ACCESS

.. py:data:: MAY_ACCESS

.. py:data:: MAYMUST_ACCESS_MASK

.. py:data:: ONE_ACCESS_TYPE

.. py:data:: INCLUDE_SPOILED_REGS

.. py:data:: EXCLUDE_PASS_REGS

.. py:data:: FULL_XDSU

.. py:data:: WITH_ASSERTS

.. py:data:: EXCLUDE_VOLATILE

.. py:data:: INCLUDE_UNUSED_SRC

.. py:data:: INCLUDE_DEAD_RETREGS

.. py:data:: INCLUDE_RESTRICTED

.. py:data:: CALL_SPOILS_ONLY_ARGS

.. py:data:: mr_none

.. py:data:: mr_cf

.. py:data:: mr_zf

.. py:data:: mr_sf

.. py:data:: mr_of

.. py:data:: mr_pf

.. py:data:: cc_count

.. py:data:: mr_cc

.. py:data:: mr_first

.. py:class:: number_format_t(_opnum: int = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: flags32
      :type:  flags_t

      low 32bit of flags (for compatibility)



   .. py:attribute:: opnum
      :type:  char

      operand number: 0..UA_MAXOP



   .. py:attribute:: props
      :type:  char

      properties: combination of NF_ bits (Number format property bits) 
              



   .. py:attribute:: serial
      :type:  uchar

      for enums: constant serial number



   .. py:attribute:: org_nbytes
      :type:  char

      original number size in bytes



   .. py:attribute:: type_name
      :type:  str

      for stroffs: structure for offsetof()
      for enums: enum name 
              



   .. py:attribute:: flags
      :type:  flags64_t

      ida flags, which describe number radix, enum, etc 
              



   .. py:method:: get_radix() -> int

      Get number radix 
              
      :returns: 2,8,10, or 16



   .. py:method:: is_fixed() -> bool

      Is number representation fixed? Fixed representation cannot be modified by the decompiler 
              



   .. py:method:: is_hex() -> bool

      Is a hexadecimal number?



   .. py:method:: is_dec() -> bool

      Is a decimal number?



   .. py:method:: is_oct() -> bool

      Is a octal number?



   .. py:method:: is_enum() -> bool

      Is a symbolic constant?



   .. py:method:: is_char() -> bool

      Is a character constant?



   .. py:method:: is_stroff() -> bool

      Is a structure field offset?



   .. py:method:: is_numop() -> bool

      Is a number?



   .. py:method:: needs_to_be_inverted() -> bool

      Does the number need to be negated or bitwise negated? Returns true if the user requested a negation but it is not done yet 
              



   .. py:method:: has_unmutable_type() -> bool


.. py:data:: NF_FIXED

   number format has been defined by the user


.. py:data:: NF_NEGDONE

   temporary internal bit: negation has been performed


.. py:data:: NF_BINVDONE

   temporary internal bit: inverting bits is done


.. py:data:: NF_NEGATE

   The user asked to negate the constant.


.. py:data:: NF_BITNOT

   The user asked to invert bits of the constant.


.. py:data:: NF_VALID

   internal bit: stroff or enum is valid for enums: this bit is set immediately for stroffs: this bit is set at the end of decompilation 
           


.. py:class:: vd_printer_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: tmpbuf
      :type:  str


   .. py:attribute:: hdrlines
      :type:  int

      number of header lines (prototype+typedef+lvars) valid at the end of print process 
              



.. py:class:: vc_printer_t(f: cfunc_t)

   Bases: :py:obj:`vd_printer_t`


   .. py:attribute:: thisown


   .. py:attribute:: func
      :type:  cfunc_t const *

      cfunc_t to generate text for



   .. py:attribute:: lastchar
      :type:  char

      internal: last printed character 
              



   .. py:method:: oneliner() -> bool

      Are we generating one-line text representation? 
              
      :returns: `true` if the output will occupy one line without line breaks



.. py:class:: qstring_printer_t(f: cfunc_t, tags: bool)

   Bases: :py:obj:`vc_printer_t`


   .. py:attribute:: thisown


   .. py:attribute:: with_tags
      :type:  bool

      Generate output with color tags.



   .. py:attribute:: s
      :type:  str

      Reference to the output string 
              



   .. py:method:: get_s() -> str


.. py:function:: dstr(tif: tinfo_t) -> str

   Print the specified type info. This function can be used from a debugger by typing "tif->dstr()" 
           


.. py:function:: is_type_correct(ptr: type_t const *) -> bool

   Verify a type string. 
           
   :returns: true if type string is correct


.. py:function:: is_small_udt(tif: tinfo_t) -> bool

   Is a small structure or union? 
           
   :returns: true if the type is a small UDT (user defined type). Small UDTs fit into a register (or pair or registers) as a rule.


.. py:function:: is_nonbool_type(type: tinfo_t) -> bool

   Is definitely a non-boolean type? 
           
   :returns: true if the type is a non-boolean type (non bool and well defined)


.. py:function:: is_bool_type(type: tinfo_t) -> bool

   Is a boolean type? 
           
   :returns: true if the type is a boolean type


.. py:function:: is_ptr_or_array(t: type_t) -> bool

   Is a pointer or array type?


.. py:function:: is_paf(t: type_t) -> bool

   Is a pointer, array, or function type?


.. py:function:: is_inplace_def(type: tinfo_t) -> bool

   Is struct/union/enum definition (not declaration)?


.. py:function:: partial_type_num(type: tinfo_t) -> int

   Calculate number of partial subtypes. 
           
   :returns: number of partial subtypes. The bigger is this number, the uglier is the type.


.. py:function:: get_float_type(width: int) -> tinfo_t

   Get a type of a floating point value with the specified width 
           
   :param width: width of the desired type
   :returns: type info object


.. py:function:: get_int_type_by_width_and_sign(srcwidth: int, sign: type_sign_t) -> tinfo_t

   Create a type info by width and sign. Returns a simple type (examples: int, short) with the given width and sign. 
           
   :param srcwidth: size of the type in bytes
   :param sign: sign of the type


.. py:function:: get_unk_type(size: int) -> tinfo_t

   Create a partial type info by width. Returns a partially defined type (examples: _DWORD, _BYTE) with the given width. 
           
   :param size: size of the type in bytes


.. py:function:: dummy_ptrtype(ptrsize: int, isfp: bool) -> tinfo_t

   Generate a dummy pointer type 
           
   :param ptrsize: size of pointed object
   :param isfp: is floating point object?


.. py:function:: make_pointer(type: tinfo_t) -> tinfo_t

   Create a pointer type. This function performs the following conversion: "type" -> "type*" 
           
   :param type: object type.
   :returns: "type*". for example, if 'char' is passed as the argument,


.. py:function:: create_typedef(*args) -> tinfo_t

   This function has the following signatures:

       0. create_typedef(name: str) -> tinfo_t
       1. create_typedef(n: int) -> tinfo_t

   # 0: create_typedef(name: str) -> tinfo_t

   Create a reference to a named type. 
           
   :returns: type which refers to the specified name. For example, if name is "DWORD", the type info which refers to "DWORD" is created.

   # 1: create_typedef(n: int) -> tinfo_t

   Create a reference to an ordinal type. 
           
   :returns: type which refers to the specified ordinal. For example, if n is 1, the type info which refers to ordinal type 1 is created.


.. py:data:: GUESSED_NONE

.. py:data:: GUESSED_WEAK

.. py:data:: GUESSED_FUNC

.. py:data:: GUESSED_DATA

.. py:data:: TS_NOELL

.. py:data:: TS_SHRINK

.. py:data:: TS_DONTREF

.. py:data:: TS_MASK

.. py:function:: get_type(id: int, tif: tinfo_t, guess: type_source_t) -> bool

   Get a global type. Global types are types of addressable objects and struct/union/enum types 
           
   :param id: address or id of the object
   :param tif: buffer for the answer
   :param guess: what kind of types to consider
   :returns: success


.. py:function:: set_type(id: int, tif: tinfo_t, source: type_source_t, force: bool = False) -> bool

   Set a global type. 
           
   :param id: address or id of the object
   :param tif: new type info
   :param source: where the type comes from
   :param force: true means to set the type as is, false means to merge the new type with the possibly existing old type info.
   :returns: success


.. py:class:: vdloc_t

   Bases: :py:obj:`ida_typeinf.argloc_t`


   .. py:attribute:: thisown


   .. py:method:: reg1() -> int

      Get the register info. Use when atype() == ALOC_REG1 or ALOC_REG2 
              



   .. py:method:: set_reg1(r1: int) -> None

      Set register location.



   .. py:method:: compare(r: vdloc_t) -> int


   .. py:method:: is_aliasable(mb: mba_t, size: int) -> bool


.. py:function:: print_vdloc(loc: vdloc_t, nbytes: int) -> str

   Print vdloc. Since vdloc does not always carry the size info, we pass it as NBYTES.. 
           


.. py:function:: arglocs_overlap(loc1: vdloc_t, w1: size_t, loc2: vdloc_t, w2: size_t) -> bool

   Do two arglocs overlap?


.. py:class:: lvar_locator_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: location
      :type:  vdloc_t

      Variable location.



   .. py:attribute:: defea
      :type:  ida_idaapi.ea_t

      Definition address. Usually, this is the address of the instruction that initializes the variable. In some cases it can be a fictional address. 
              



   .. py:method:: get_stkoff() -> int

      Get offset of the varialbe in the stack frame. 
              
      :returns: a non-negative value for stack variables. The value is an offset from the bottom of the stack frame in terms of vd-offsets. negative values mean error (not a stack variable)



   .. py:method:: is_reg1() -> bool

      Is variable located on one register?



   .. py:method:: is_reg2() -> bool

      Is variable located on two registers?



   .. py:method:: is_reg_var() -> bool

      Is variable located on register(s)?



   .. py:method:: is_stk_var() -> bool

      Is variable located on the stack?



   .. py:method:: is_scattered() -> bool

      Is variable scattered?



   .. py:method:: get_reg1() -> mreg_t

      Get the register number of the variable.



   .. py:method:: get_reg2() -> mreg_t

      Get the number of the second register (works only for ALOC_REG2 lvars)



   .. py:method:: get_scattered() -> scattered_aloc_t &

      Get information about scattered variable.



   .. py:method:: compare(r: lvar_locator_t) -> int


.. py:class:: lvar_t(*args, **kwargs)

   Bases: :py:obj:`lvar_locator_t`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str

      variable name. use mba_t::set_nice_lvar_name() and mba_t::set_user_lvar_name() to modify it 
              



   .. py:attribute:: cmt
      :type:  str

      variable comment string



   .. py:attribute:: tif
      :type:  tinfo_t

      variable type



   .. py:attribute:: width
      :type:  int

      variable size in bytes



   .. py:attribute:: defblk
      :type:  int

      first block defining the variable. 0 for args, -1 if unknown 
              



   .. py:attribute:: divisor
      :type:  uint64

      max known divisor of the variable



   .. py:method:: used() -> bool

      Is the variable used in the code?



   .. py:method:: typed() -> bool

      Has the variable a type?



   .. py:method:: mreg_done() -> bool

      Have corresponding microregs been replaced by references to this variable?



   .. py:method:: has_nice_name() -> bool

      Does the variable have a nice name?



   .. py:method:: is_unknown_width() -> bool

      Do we know the width of the variable?



   .. py:method:: has_user_info() -> bool

      Has any user-defined information?



   .. py:method:: has_user_name() -> bool

      Has user-defined name?



   .. py:method:: has_user_type() -> bool

      Has user-defined type?



   .. py:method:: is_result_var() -> bool

      Is the function result?



   .. py:method:: is_arg_var() -> bool

      Is the function argument?



   .. py:method:: is_fake_var() -> bool

      Is fake return variable?



   .. py:method:: is_overlapped_var() -> bool

      Is overlapped variable?



   .. py:method:: is_floating_var() -> bool

      Used by a fpu insn?



   .. py:method:: is_spoiled_var() -> bool

      Is spoiled var? (meaningful only during lvar allocation)



   .. py:method:: is_noptr_var() -> bool

      Variable type should not be a pointer.



   .. py:method:: is_mapdst_var() -> bool

      Other variable(s) map to this var?



   .. py:method:: is_thisarg() -> bool

      Is 'this' argument of a C++ member function?



   .. py:method:: is_split_var() -> bool

      Is a split variable?



   .. py:method:: has_regname() -> bool

      Has a register name? (like _RAX)



   .. py:method:: in_asm() -> bool

      Is variable used in an instruction translated into __asm?



   .. py:method:: is_dummy_arg() -> bool

      Is a dummy argument (added to fill a hole in the argument list)



   .. py:method:: is_notarg() -> bool

      Is a local variable? (local variable cannot be an input argument)



   .. py:method:: is_automapped() -> bool

      Was the variable automatically mapped to another variable?



   .. py:method:: is_used_byref() -> bool

      Was the address of the variable taken?



   .. py:method:: is_decl_unused() -> bool

      Was declared as __unused by the user? See CVAR_UNUSED.



   .. py:method:: is_shared() -> bool

      Is lvar mapped to several chains.



   .. py:method:: was_scattered_arg() -> bool

      Was lvar transformed from a scattered argument?



   .. py:method:: set_used() -> None


   .. py:method:: clear_used() -> None


   .. py:method:: set_typed() -> None


   .. py:method:: set_non_typed() -> None


   .. py:method:: clr_user_info() -> None


   .. py:method:: set_user_name() -> None


   .. py:method:: set_user_type() -> None


   .. py:method:: clr_user_type() -> None


   .. py:method:: clr_user_name() -> None


   .. py:method:: set_mreg_done() -> None


   .. py:method:: clr_mreg_done() -> None


   .. py:method:: set_unknown_width() -> None


   .. py:method:: clr_unknown_width() -> None


   .. py:method:: set_arg_var() -> None


   .. py:method:: clr_arg_var() -> None


   .. py:method:: set_fake_var() -> None


   .. py:method:: clr_fake_var() -> None


   .. py:method:: set_overlapped_var() -> None


   .. py:method:: clr_overlapped_var() -> None


   .. py:method:: set_floating_var() -> None


   .. py:method:: clr_floating_var() -> None


   .. py:method:: set_spoiled_var() -> None


   .. py:method:: clr_spoiled_var() -> None


   .. py:method:: set_mapdst_var() -> None


   .. py:method:: clr_mapdst_var() -> None


   .. py:method:: set_noptr_var() -> None


   .. py:method:: clr_noptr_var() -> None


   .. py:method:: set_thisarg() -> None


   .. py:method:: clr_thisarg() -> None


   .. py:method:: set_split_var() -> None


   .. py:method:: clr_split_var() -> None


   .. py:method:: set_dummy_arg() -> None


   .. py:method:: clr_dummy_arg() -> None


   .. py:method:: set_notarg() -> None


   .. py:method:: clr_notarg() -> None


   .. py:method:: set_automapped() -> None


   .. py:method:: clr_automapped() -> None


   .. py:method:: set_used_byref() -> None


   .. py:method:: clr_used_byref() -> None


   .. py:method:: set_decl_unused() -> None


   .. py:method:: clr_decl_unused() -> None


   .. py:method:: set_shared() -> None


   .. py:method:: clr_shared() -> None


   .. py:method:: set_scattered_arg() -> None


   .. py:method:: clr_scattered_arg() -> None


   .. py:method:: has_common(v: lvar_t) -> bool

      Do variables overlap?



   .. py:method:: has_common_bit(loc: vdloc_t, width2: asize_t) -> bool

      Does the variable overlap with the specified location?



   .. py:method:: type() -> tinfo_t &

      Get variable type.



   .. py:method:: accepts_type(t: tinfo_t, may_change_thisarg: bool = False) -> bool

      Check if the variable accept the specified type. Some types are forbidden (void, function types, wrong arrays, etc) 
              



   .. py:method:: set_lvar_type(t: tinfo_t, may_fail: bool = False) -> bool

      Set variable type Note: this function does not modify the idb, only the lvar instance in the memory. For permanent changes see modify_user_lvars() Also, the variable type is not considered as final by the decompiler and may be modified later by the type derivation. In some cases set_final_var_type() may work better, but it does not do persistent changes to the database neither. 
              
      :param t: new type
      :param may_fail: if false and type is bad, interr
      :returns: success



   .. py:method:: set_final_lvar_type(t: tinfo_t) -> None

      Set final variable type.



   .. py:method:: set_width(w: int, svw_flags: int = 0) -> bool

      Change the variable width. We call the variable size 'width', it is represents the number of bytes. This function may change the variable type using set_lvar_type(). 
              
      :param w: new width
      :param svw_flags: combination of SVW_... bits
      :returns: success



   .. py:method:: append_list(mba: mba_t, lst: mlist_t, pad_if_scattered: bool = False) -> None

      Append local variable to mlist. 
              
      :param mba: ptr to the current mba_t
      :param lst: list to append to
      :param pad_if_scattered: if true, append padding bytes in case of scattered lvar



   .. py:method:: is_aliasable(mba: mba_t) -> bool

      Is the variable aliasable? 
              
      :param mba: ptr to the current mba_t Aliasable variables may be modified indirectly (through a pointer)



.. py:data:: SVW_INT

.. py:data:: SVW_FLOAT

.. py:data:: SVW_SOFT

.. py:class:: lvars_t

   Bases: :py:obj:`qvector_lvar_t`


   .. py:attribute:: thisown


   .. py:method:: find_input_lvar(argloc: vdloc_t, _size: int) -> int

      Find an input variable at the specified location. 
              
      :param argloc: variable location
      :param _size: variable size in bytes
      :returns: -1 if failed, otherwise an index into 'vars'



   .. py:method:: find_input_reg(reg: int, _size: int = 1) -> int

      Find an input register variable. 
              
      :param reg: register to find
      :param _size: variable size in bytes
      :returns: -1 if failed, otherwise an index into 'vars'



   .. py:method:: find_stkvar(spoff: int, width: int) -> int

      Find a stack variable at the specified location. 
              
      :param spoff: offset from the minimal sp
      :param width: variable size in bytes
      :returns: -1 if failed, otherwise an index into 'vars'



   .. py:method:: find(ll: lvar_locator_t) -> lvar_t *

      Find a variable at the specified location. 
              
      :param ll: variable location
      :returns: pointer to variable or nullptr



   .. py:method:: find_lvar(location: vdloc_t, width: int, defblk: int = -1) -> int

      Find a variable at the specified location. 
              
      :param location: variable location
      :param width: variable size in bytes
      :param defblk: definition block of the lvar. -1 means any block
      :returns: -1 if failed, otherwise an index into 'vars'



.. py:class:: lvar_saved_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ll
      :type:  lvar_locator_t

      Variable locator.



   .. py:attribute:: name
      :type:  str

      Name.



   .. py:attribute:: type
      :type:  tinfo_t

      Type.



   .. py:attribute:: cmt
      :type:  str

      Comment.



   .. py:attribute:: size
      :type:  ssize_t

      Type size (if not initialized then -1)



   .. py:attribute:: flags
      :type:  int

      saved user lvar info property bits 
              



   .. py:method:: has_info() -> bool


   .. py:method:: is_kept() -> bool


   .. py:method:: clear_keep() -> None


   .. py:method:: set_keep() -> None


   .. py:method:: is_split_lvar() -> bool


   .. py:method:: set_split_lvar() -> None


   .. py:method:: clr_split_lvar() -> None


   .. py:method:: is_noptr_lvar() -> bool


   .. py:method:: set_noptr_lvar() -> None


   .. py:method:: clr_noptr_lvar() -> None


   .. py:method:: is_nomap_lvar() -> bool


   .. py:method:: set_nomap_lvar() -> None


   .. py:method:: clr_nomap_lvar() -> None


   .. py:method:: is_unused_lvar() -> bool


   .. py:method:: set_unused_lvar() -> None


   .. py:method:: clr_unused_lvar() -> None


.. py:data:: LVINF_KEEP

   preserve saved user settings regardless of vars for example, if a var loses all its user-defined attributes or even gets destroyed, keep its lvar_saved_info_t. this is used for ephemeral variables that get destroyed by macro recognition. 
           


.. py:data:: LVINF_SPLIT

   split allocation of a new variable. forces the decompiler to create a new variable at ll.defea 
           


.. py:data:: LVINF_NOPTR

   variable type should not be a pointer


.. py:data:: LVINF_NOMAP

   forbid automatic mapping of the variable


.. py:data:: LVINF_UNUSED

   unused argument, corresponds to CVAR_UNUSED


.. py:class:: lvar_uservec_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: lvvec
      :type:  lvar_saved_infos_t

      User-specified names, types, comments for lvars. Variables without user-specified info are not present in this vector. 
              



   .. py:attribute:: lmaps
      :type:  lvar_mapping_t

      Local variable mapping (used for merging variables)



   .. py:attribute:: stkoff_delta
      :type:  int

      Delta to add to IDA stack offset to calculate Hex-Rays stack offsets. Should be set by the caller before calling save_user_lvar_settings(); 
              



   .. py:attribute:: ulv_flags
      :type:  int

      Various flags. Possible values are from lvar_uservec_t property bits.



   .. py:method:: swap(r: lvar_uservec_t) -> None


   .. py:method:: clear() -> None


   .. py:method:: empty() -> bool


   .. py:method:: find_info(vloc: lvar_locator_t) -> lvar_saved_info_t *

      find saved user settings for given var



   .. py:method:: keep_info(v: lvar_t) -> None

      Preserve user settings for given var.



.. py:data:: ULV_PRECISE_DEFEA

   Use precise defea's for lvar locations.


.. py:function:: restore_user_lvar_settings(lvinf: lvar_uservec_t, func_ea: ida_idaapi.ea_t) -> bool

   Restore user defined local variable settings in the database. 
           
   :param lvinf: ptr to output buffer
   :param func_ea: entry address of the function
   :returns: success


.. py:function:: save_user_lvar_settings(func_ea: ida_idaapi.ea_t, lvinf: lvar_uservec_t) -> None

   Save user defined local variable settings into the database. 
           
   :param func_ea: entry address of the function
   :param lvinf: user-specified info about local variables


.. py:class:: user_lvar_modifier_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: modify_lvars(lvinf: lvar_uservec_t) -> bool

      Modify lvar settings. Returns: true-modified 
              



.. py:function:: modify_user_lvars(entry_ea: ida_idaapi.ea_t, mlv: user_lvar_modifier_t) -> bool

   Modify saved local variable settings. 
           
   :param entry_ea: function start address
   :param mlv: local variable modifier
   :returns: true if modified variables


.. py:function:: modify_user_lvar_info(func_ea: ida_idaapi.ea_t, mli_flags: uint, info: lvar_saved_info_t) -> bool

   Modify saved local variable settings of one variable. 
           
   :param func_ea: function start address
   :param mli_flags: bits that specify which attrs defined by INFO are to be set
   :param info: local variable info attrs
   :returns: true if modified, false if invalid MLI_FLAGS passed


.. py:data:: MLI_NAME

   apply lvar name


.. py:data:: MLI_TYPE

   apply lvar type


.. py:data:: MLI_CMT

   apply lvar comment


.. py:data:: MLI_SET_FLAGS

   set LVINF_... bits


.. py:data:: MLI_CLR_FLAGS

   clear LVINF_... bits


.. py:function:: locate_lvar(out: lvar_locator_t, func_ea: ida_idaapi.ea_t, varname: str) -> bool

   Find a variable by name. 
           
   :param out: output buffer for the variable locator
   :param func_ea: function start address
   :param varname: variable name
   :returns: success Since VARNAME is not always enough to find the variable, it may decompile the function.


.. py:function:: rename_lvar(func_ea: ida_idaapi.ea_t, oldname: str, newname: str) -> bool

   Rename a local variable. 
           
   :param func_ea: function start address
   :param oldname: old name of the variable
   :param newname: new name of the variable
   :returns: success This is a convenience function. For bulk renaming consider using modify_user_lvars.


.. py:class:: udcall_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str


   .. py:attribute:: tif
      :type:  tinfo_t


   .. py:method:: compare(r: udcall_t) -> int


   .. py:method:: empty() -> bool


.. py:function:: restore_user_defined_calls(udcalls: udcall_map_t *, func_ea: ida_idaapi.ea_t) -> bool

   Restore user defined function calls from the database. 
           
   :param udcalls: ptr to output buffer
   :param func_ea: entry address of the function
   :returns: success


.. py:function:: save_user_defined_calls(func_ea: ida_idaapi.ea_t, udcalls: udcall_map_t const &) -> None

   Save user defined local function calls into the database. 
           
   :param func_ea: entry address of the function
   :param udcalls: user-specified info about user defined function calls


.. py:function:: parse_user_call(udc: udcall_t, decl: str, silent: bool) -> bool

   Convert function type declaration into internal structure 
           
   :param udc: - pointer to output structure
   :param decl: - function type declaration
   :param silent: - if TRUE: do not show warning in case of incorrect type
   :returns: success


.. py:function:: convert_to_user_call(udc: udcall_t, cdg: codegen_t) -> merror_t

   try to generate user-defined call for an instruction 
           
   :returns: Microcode error code code: MERR_OK - user-defined call generated else - error (MERR_INSN == inacceptable udc.tif)


.. py:class:: microcode_filter_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: match(cdg: codegen_t) -> bool

      check if the filter object is to be applied 
              
      :returns: success



   .. py:method:: apply(cdg: codegen_t) -> merror_t

      generate microcode for an instruction 
              
      :returns: MERR_... code: MERR_OK - user-defined microcode generated, go to the next instruction MERR_INSN - not generated - the caller should try the standard way else - error



.. py:function:: install_microcode_filter(filter: microcode_filter_t, install: bool = True) -> bool

   register/unregister non-standard microcode generator 
           
   :param filter: - microcode generator object
   :param install: - TRUE - register the object, FALSE - unregister
   :returns: success


.. py:class:: udc_filter_t

   Bases: :py:obj:`microcode_filter_t`


   .. py:attribute:: thisown


   .. py:method:: cleanup() -> None

      Cleanup the filter This function properly clears type information associated to this filter. 
              



   .. py:method:: match(cdg: codegen_t) -> bool

      return true if the filter object should be applied to given instruction



   .. py:method:: apply(cdg: codegen_t) -> merror_t

      generate microcode for an instruction 
              
      :returns: MERR_... code: MERR_OK - user-defined microcode generated, go to the next instruction MERR_INSN - not generated - the caller should try the standard way else - error



   .. py:method:: empty() -> bool


   .. py:method:: install() -> None


   .. py:method:: remove() -> bool


   .. py:method:: init(decl: str) -> bool


.. py:class:: bitset_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: swap(r: bitset_t) -> None


   .. py:method:: copy(m: bitset_t) -> bitset_t &


   .. py:method:: add(*args) -> bool

      This function has the following signatures:

          0. add(bit: int) -> bool
          1. add(bit: int, width: int) -> bool
          2. add(ml: const bitset_t &) -> bool

      # 0: add(bit: int) -> bool


      # 1: add(bit: int, width: int) -> bool


      # 2: add(ml: const bitset_t &) -> bool



   .. py:method:: sub(*args) -> bool

      This function has the following signatures:

          0. sub(bit: int) -> bool
          1. sub(bit: int, width: int) -> bool
          2. sub(ml: const bitset_t &) -> bool

      # 0: sub(bit: int) -> bool


      # 1: sub(bit: int, width: int) -> bool


      # 2: sub(ml: const bitset_t &) -> bool



   .. py:method:: cut_at(maxbit: int) -> bool


   .. py:method:: shift_down(shift: int) -> None


   .. py:method:: has(bit: int) -> bool


   .. py:method:: has_all(bit: int, width: int) -> bool


   .. py:method:: has_any(bit: int, width: int) -> bool


   .. py:method:: dstr() -> str


   .. py:method:: empty() -> bool


   .. py:method:: count(*args) -> int

      This function has the following signatures:

          0. count() -> int
          1. count(bit: int) -> int

      # 0: count() -> int


      # 1: count(bit: int) -> int



   .. py:method:: last() -> int


   .. py:method:: clear() -> None


   .. py:method:: fill_with_ones(maxbit: int) -> None


   .. py:method:: has_common(ml: bitset_t) -> bool


   .. py:method:: intersect(ml: bitset_t) -> bool


   .. py:method:: is_subset_of(ml: bitset_t) -> bool


   .. py:method:: includes(ml: bitset_t) -> bool


   .. py:method:: compare(r: bitset_t) -> int


   .. py:method:: itat(n: int) -> bitset_t::iterator


   .. py:method:: begin() -> bitset_t::iterator


   .. py:method:: end() -> bitset_t::iterator


   .. py:method:: front() -> int


   .. py:method:: back() -> int


   .. py:method:: inc(p: iterator, n: int = 1) -> None


   .. py:method:: itv(it: iterator) -> int


.. py:data:: bitset_width

.. py:data:: bitset_align

.. py:data:: bitset_shift

.. py:class:: iterator(n: int = -1)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


.. py:class:: node_bitset_t(*args)

   Bases: :py:obj:`bitset_t`


   .. py:attribute:: thisown


.. py:class:: array_of_node_bitset_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


.. py:class:: ivl_t(_off: int = 0, _size: int = 0)

   Bases: :py:obj:`uval_ivl_t`


   .. py:attribute:: thisown


   .. py:method:: empty() -> bool


   .. py:method:: clear() -> None


   .. py:method:: dstr() -> str


   .. py:method:: extend_to_cover(r: ivl_t) -> bool


   .. py:method:: intersect(r: ivl_t) -> None


   .. py:method:: overlap(ivl: ivl_t) -> bool


   .. py:method:: includes(ivl: ivl_t) -> bool


   .. py:method:: contains(off2: int) -> bool


   .. py:method:: compare(r: ivl_t) -> int


.. py:class:: ivl_with_name_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ivl
      :type:  ivl_t


   .. py:attribute:: whole
      :type:  str


   .. py:attribute:: part
      :type:  str


.. py:class:: ivlset_t(*args)

   Bases: :py:obj:`uval_ivl_ivlset_t`


   .. py:attribute:: thisown


   .. py:method:: add(*args) -> bool

      This function has the following signatures:

          0. add(ivl: const ivl_t &) -> bool
          1. add(ea: ida_idaapi.ea_t, size: asize_t) -> bool
          2. add(ivs: const ivlset_t &) -> bool

      # 0: add(ivl: const ivl_t &) -> bool


      # 1: add(ea: ida_idaapi.ea_t, size: asize_t) -> bool


      # 2: add(ivs: const ivlset_t &) -> bool



   .. py:method:: addmasked(ivs: ivlset_t, mask: ivl_t) -> bool


   .. py:method:: sub(*args) -> bool

      This function has the following signatures:

          0. sub(ivl: const ivl_t &) -> bool
          1. sub(ea: ida_idaapi.ea_t, size: asize_t) -> bool
          2. sub(ivs: const ivlset_t &) -> bool

      # 0: sub(ivl: const ivl_t &) -> bool


      # 1: sub(ea: ida_idaapi.ea_t, size: asize_t) -> bool


      # 2: sub(ivs: const ivlset_t &) -> bool



   .. py:method:: dstr() -> str


   .. py:method:: count() -> asize_t


   .. py:method:: has_common(*args) -> bool

      This function has the following signatures:

          0. has_common(ivl: const ivl_t &, strict: bool=false) -> bool
          1. has_common(ivs: const ivlset_t &) -> bool

      # 0: has_common(ivl: const ivl_t &, strict: bool=false) -> bool


      # 1: has_common(ivs: const ivlset_t &) -> bool



   .. py:method:: contains(off: int) -> bool


   .. py:method:: includes(ivs: ivlset_t) -> bool


   .. py:method:: intersect(ivs: ivlset_t) -> bool


   .. py:method:: compare(r: ivlset_t) -> int


.. py:class:: rlist_t(*args)

   Bases: :py:obj:`bitset_t`


   .. py:attribute:: thisown


   .. py:method:: dstr() -> str


.. py:class:: mlist_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: reg
      :type:  rlist_t


   .. py:attribute:: mem
      :type:  ivlset_t


   .. py:method:: swap(r: mlist_t) -> None


   .. py:method:: addmem(ea: ida_idaapi.ea_t, size: asize_t) -> bool


   .. py:method:: add(*args) -> bool

      This function has the following signatures:

          0. add(r: mreg_t, size: int) -> bool
          1. add(r: const rlist_t &) -> bool
          2. add(ivl: const ivl_t &) -> bool
          3. add(lst: const mlist_t &) -> bool

      # 0: add(r: mreg_t, size: int) -> bool


      # 1: add(r: const rlist_t &) -> bool


      # 2: add(ivl: const ivl_t &) -> bool


      # 3: add(lst: const mlist_t &) -> bool



   .. py:method:: sub(*args) -> bool

      This function has the following signatures:

          0. sub(r: mreg_t, size: int) -> bool
          1. sub(ivl: const ivl_t &) -> bool
          2. sub(lst: const mlist_t &) -> bool

      # 0: sub(r: mreg_t, size: int) -> bool


      # 1: sub(ivl: const ivl_t &) -> bool


      # 2: sub(lst: const mlist_t &) -> bool



   .. py:method:: count() -> asize_t


   .. py:method:: dstr() -> str


   .. py:method:: empty() -> bool


   .. py:method:: clear() -> None


   .. py:method:: has(r: mreg_t) -> bool


   .. py:method:: has_all(r: mreg_t, size: int) -> bool


   .. py:method:: has_any(r: mreg_t, size: int) -> bool


   .. py:method:: has_memory() -> bool


   .. py:method:: has_common(lst: mlist_t) -> bool


   .. py:method:: includes(lst: mlist_t) -> bool


   .. py:method:: intersect(lst: mlist_t) -> bool


   .. py:method:: is_subset_of(lst: mlist_t) -> bool


   .. py:method:: compare(r: mlist_t) -> int


.. py:function:: get_temp_regs() -> mlist_t const &

   Get list of temporary registers. Tempregs are temporary registers that are used during code generation. They do not map to regular processor registers. They are used only to store temporary values during execution of one instruction. Tempregs may not be used to pass a value from one block to another. In other words, at the end of a block all tempregs must be dead. 
           


.. py:function:: is_kreg(r: mreg_t) -> bool

   Is a kernel register? Kernel registers are temporary registers that can be used freely. They may be used to store values that cross instruction or basic block boundaries. Kernel registers do not map to regular processor registers. See also mba_t::alloc_kreg() 
           


.. py:function:: reg2mreg(reg: int) -> mreg_t

   Map a processor register to a microregister. 
           
   :param reg: processor register number
   :returns: microregister register id or mr_none


.. py:function:: mreg2reg(reg: mreg_t, width: int) -> int

   Map a microregister to a processor register. 
           
   :param reg: microregister number
   :param width: size of microregister in bytes
   :returns: processor register id or -1


.. py:function:: get_mreg_name(reg: mreg_t, width: int, ud: void * = None) -> str

   Get the microregister name. 
           
   :param reg: microregister number
   :param width: size of microregister in bytes. may be bigger than the real register size.
   :param ud: reserved, must be nullptr
   :returns: width of the printed register. this value may be less than the WIDTH argument.


.. py:class:: optinsn_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: func(blk: mblock_t, ins: minsn_t, optflags: int) -> int

      Optimize an instruction. 
              
      :param blk: current basic block. maybe nullptr, which means that the instruction must be optimized without context
      :param ins: instruction to optimize; it is always a top-level instruction. the callback may not delete the instruction but may convert it into nop (see mblock_t::make_nop). to optimize sub-instructions, visit them using minsn_visitor_t. sub-instructions may not be converted into nop but can be converted to "mov x,x". for example: add x,0,x => mov x,x this callback may change other instructions in the block, but should do this with care, e.g. to no break the propagation algorithm if called with OPTI_NO_LDXOPT.
      :param optflags: combination of optimization flags bits
      :returns: number of changes made to the instruction. if after this call the instruction's use/def lists have changed, you must mark the block level lists as dirty (see mark_lists_dirty)



   .. py:method:: install() -> None


   .. py:method:: remove() -> bool


.. py:class:: optblock_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: func(blk: mblock_t) -> int

      Optimize a block. This function usually performs the optimizations that require analyzing the entire block and/or its neighbors. For example it can recognize patterns and perform conversions like: b0: b0: ... ... jnz x, 0, @b2 => jnz x, 0, @b2 b1: b1: add x, 0, y mov x, y ... ... 
              
      :param blk: Basic block to optimize as a whole.
      :returns: number of changes made to the block. See also mark_lists_dirty.



   .. py:method:: install() -> None


   .. py:method:: remove() -> bool


.. py:class:: simple_graph_t(*args, **kwargs)

   Bases: :py:obj:`ida_gdl.gdl_graph_t`


   .. py:attribute:: thisown


   .. py:attribute:: title
      :type:  str


   .. py:attribute:: colored_gdl_edges
      :type:  bool


   .. py:method:: compute_dominators(domin: array_of_node_bitset_t, post: bool = False) -> None


   .. py:method:: compute_immediate_dominators(domin: array_of_node_bitset_t, idomin: intvec_t, post: bool = False) -> None


   .. py:method:: depth_first_preorder(pre: node_ordering_t) -> int


   .. py:method:: depth_first_postorder(post: node_ordering_t) -> int


   .. py:method:: begin() -> simple_graph_t::iterator


   .. py:method:: end() -> simple_graph_t::iterator


   .. py:method:: front() -> int


   .. py:method:: inc(p: simple_graph_t::iterator &, n: int = 1) -> None


   .. py:method:: goup(node: int) -> int


.. py:class:: op_parent_info_t(_mba: mba_t = None, _blk: mblock_t = None, _topins: minsn_t = None)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: mba
      :type:  mba_t *


   .. py:attribute:: blk
      :type:  mblock_t *


   .. py:attribute:: topins
      :type:  minsn_t *


   .. py:attribute:: curins
      :type:  minsn_t *


.. py:class:: minsn_visitor_t(_mba: mba_t = None, _blk: mblock_t = None, _topins: minsn_t = None)

   Bases: :py:obj:`op_parent_info_t`


   .. py:attribute:: thisown


   .. py:method:: visit_minsn() -> int


.. py:class:: mop_visitor_t(_mba: mba_t = None, _blk: mblock_t = None, _topins: minsn_t = None)

   Bases: :py:obj:`op_parent_info_t`


   .. py:attribute:: thisown


   .. py:attribute:: prune
      :type:  bool

      Should skip sub-operands of the current operand? visit_mop() may set 'prune=true' for that. 
              



   .. py:method:: visit_mop(op: mop_t, type: tinfo_t, is_target: bool) -> int


.. py:class:: scif_visitor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: visit_scif_mop(r: mop_t, off: int) -> int


.. py:class:: mlist_mop_visitor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: topins
      :type:  minsn_t *


   .. py:attribute:: curins
      :type:  minsn_t *


   .. py:attribute:: changed
      :type:  bool


   .. py:attribute:: list
      :type:  mlist_t *


   .. py:attribute:: prune
      :type:  bool

      Should skip sub-operands of the current operand? visit_mop() may set 'prune=true' for that. 
              



   .. py:method:: visit_mop(op: mop_t) -> int


.. py:class:: lvar_ref_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: mba
      :type:  mba_t *const

      Pointer to the parent mba_t object. Since we need to access the 'mba->vars' array in order to retrieve the referenced variable, we keep a pointer to mba_t here. Note: this means this class and consequently mop_t, minsn_t, mblock_t are specific to a mba_t object and cannot migrate between them. fortunately this is not something we need to do. second, lvar_ref_t's appear only after MMAT_LVARS. 
              



   .. py:attribute:: off
      :type:  int

      offset from the beginning of the variable



   .. py:attribute:: idx
      :type:  int

      index into mba->vars



   .. py:method:: compare(r: lvar_ref_t) -> int


   .. py:method:: swap(r: lvar_ref_t) -> None


   .. py:method:: var() -> lvar_t &

      Retrieve the referenced variable.



.. py:data:: mop_z

   none


.. py:data:: mop_r

   register (they exist until MMAT_LVARS)


.. py:data:: mop_n

   immediate number constant


.. py:data:: mop_str

   immediate string constant (user representation)


.. py:data:: mop_d

   result of another instruction


.. py:data:: mop_S

   local stack variable (they exist until MMAT_LVARS)


.. py:data:: mop_v

   global variable


.. py:data:: mop_b

   micro basic block (mblock_t)


.. py:data:: mop_f

   list of arguments


.. py:data:: mop_l

   local variable


.. py:data:: mop_a

   mop_addr_t: address of operand (mop_l, mop_v, mop_S, mop_r)


.. py:data:: mop_h

   helper function


.. py:data:: mop_c

   mcases


.. py:data:: mop_fn

   floating point constant


.. py:data:: mop_p

   operand pair


.. py:data:: mop_sc

   scattered


.. py:data:: NOSIZE

   wrong or unexisting operand size


.. py:class:: stkvar_ref_t(m: mba_t, o: int)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: mba
      :type:  mba_t *const

      Pointer to the parent mba_t object. We need it in order to retrieve the referenced stack variable. See notes for lvar_ref_t::mba. 
              



   .. py:attribute:: off
      :type:  int

      Offset to the stack variable from the bottom of the stack frame. It is called 'decompiler stkoff' and it is different from IDA stkoff. See a note and a picture about 'decompiler stkoff' below. 
              



   .. py:method:: compare(r: stkvar_ref_t) -> int


   .. py:method:: swap(r: stkvar_ref_t) -> None


   .. py:method:: get_stkvar(udm: udm_t = None, p_idaoff: uval_t * = None) -> ssize_t

      Retrieve the referenced stack variable. 
              
      :param udm: stkvar, may be nullptr
      :param p_idaoff: if specified, will hold IDA stkoff after the call.
      :returns: index of stkvar in the frame or -1



.. py:class:: scif_t(_mba: mba_t, tif: tinfo_t, n: str = None)

   Bases: :py:obj:`vdloc_t`


   .. py:attribute:: thisown


   .. py:attribute:: mba
      :type:  mba_t *

      Pointer to the parent mba_t object. Some operations may convert a scattered operand into something simpler, (a stack operand, for example). We will need to create stkvar_ref_t at that moment, this is why we need this pointer. See notes for lvar_ref_t::mba. 
              



   .. py:attribute:: name
      :type:  str

      Usually scattered operands are created from a function prototype, which has the name information. We preserve it and use it to name the corresponding local variable. 
              



   .. py:attribute:: type
      :type:  tinfo_t

      Scattered operands always have type info assigned to them because without it we won't be able to manipulte them. 
              



.. py:class:: mnumber_t(*args)

   Bases: :py:obj:`operand_locator_t`


   .. py:attribute:: thisown


   .. py:attribute:: value
      :type:  uint64


   .. py:attribute:: org_value
      :type:  uint64


   .. py:method:: compare(r: mnumber_t) -> int


   .. py:method:: update_value(val64: uint64) -> None


.. py:class:: fnumber_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: fnum
      :type:  fpvalue_t

      Internal representation of the number.



   .. py:attribute:: nbytes
      :type:  int

      Original size of the constant in bytes.



   .. py:method:: dereference_uint16() -> uint16 *


   .. py:method:: dereference_const_uint16() -> uint16 const *


   .. py:method:: compare(r: fnumber_t) -> int


   .. py:method:: calc_max_exp() -> int


   .. py:method:: is_nan() -> bool


.. py:data:: SHINS_NUMADDR

   display definition addresses for numbers


.. py:data:: SHINS_VALNUM

   display value numbers


.. py:data:: SHINS_SHORT

   do not display use-def chains and other attrs


.. py:data:: SHINS_LDXEA

   display address of ldx expressions (not used)


.. py:data:: NO_SIDEFF

   change operand size but ignore side effects if you decide to keep the changed operand, handle_new_size() must be called 
             


.. py:data:: WITH_SIDEFF

   change operand size and handle side effects


.. py:data:: ONLY_SIDEFF

   only handle side effects


.. py:data:: ANY_REGSIZE

   any register size is permitted


.. py:data:: ANY_FPSIZE

   any size of floating operand is permitted


.. py:class:: mop_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: t
      :type:  mopt_t

      Operand type.



   .. py:attribute:: oprops
      :type:  uint8

      Operand properties.



   .. py:attribute:: valnum
      :type:  uint16

      Value number. Zero means unknown. Operands with the same value number are equal. 
              



   .. py:attribute:: size
      :type:  int

      Operand size. Usually it is 1,2,4,8 or NOSIZE but for UDTs other sizes are permitted 
              



   .. py:method:: set_impptr_done() -> None


   .. py:method:: set_udt() -> None


   .. py:method:: set_undef_val() -> None


   .. py:method:: set_lowaddr() -> None


   .. py:method:: set_for_abi() -> None


   .. py:method:: is_impptr_done() -> bool


   .. py:method:: is_udt() -> bool


   .. py:method:: probably_floating() -> bool


   .. py:method:: is_undef_val() -> bool


   .. py:method:: is_lowaddr() -> bool


   .. py:method:: is_for_abi() -> bool


   .. py:method:: is_ccflags() -> bool


   .. py:method:: is_pcval() -> bool


   .. py:method:: is_glbaddr_from_fixup() -> bool


   .. py:method:: assign(rop: mop_t) -> mop_t &


   .. py:method:: zero() -> None


   .. py:method:: swap(rop: mop_t) -> None


   .. py:method:: erase() -> None


   .. py:method:: erase_but_keep_size() -> None


   .. py:method:: dstr() -> str


   .. py:method:: create_from_mlist(mba: mba_t, lst: mlist_t, fullsize: int) -> bool

      Create operand from mlist_t. Example: if LST contains 4 bits for R0.4, our operand will be (t=mop_r, r=R0, size=4) 
              
      :param mba: pointer to microcode
      :param lst: list of locations
      :param fullsize: mba->fullsize
      :returns: success



   .. py:method:: create_from_ivlset(mba: mba_t, ivs: ivlset_t, fullsize: int) -> bool

      Create operand from ivlset_t. Example: if IVS contains [glbvar..glbvar+4), our operand will be (t=mop_v, g=&glbvar, size=4) 
              
      :param mba: pointer to microcode
      :param ivs: set of memory intervals
      :param fullsize: mba->fullsize
      :returns: success



   .. py:method:: create_from_vdloc(mba: mba_t, loc: vdloc_t, _size: int) -> None

      Create operand from vdloc_t. Example: if LOC contains (type=ALOC_REG1, r=R0), our operand will be (t=mop_r, r=R0, size=_SIZE) 
              
      :param mba: pointer to microcode
      :param loc: location
      :param _size: operand size Note: this function cannot handle scattered locations.
      :returns: success



   .. py:method:: create_from_scattered_vdloc(mba: mba_t, name: str, type: tinfo_t, loc: vdloc_t) -> None

      Create operand from scattered vdloc_t. Example: if LOC is (ALOC_DIST, {EAX.4, EDX.4}) and TYPE is _LARGE_INTEGER, our operand will be (t=mop_sc, scif={EAX.4, EDX.4}) 
              
      :param mba: pointer to microcode
      :param name: name of the operand, if available
      :param type: type of the operand, must be present
      :param loc: a scattered location
      :returns: success



   .. py:method:: create_from_insn(m: minsn_t) -> None

      Create operand from an instruction. This function creates a nested instruction that can be used as an operand. Example: if m="add x,y,z", our operand will be (t=mop_d,d=m). The destination operand of 'add' (z) is lost. 
              
      :param m: instruction to embed into operand. may not be nullptr.



   .. py:method:: make_number(*args) -> None

      Create an integer constant operand. 
              
      :param _value: value to store in the operand
      :param _size: size of the value in bytes (1,2,4,8)
      :param _ea: address of the processor instruction that made the value
      :param opnum: operand number of the processor instruction



   .. py:method:: make_fpnum(bytes: void const *) -> bool

      Create a floating point constant operand. 
              
      :param bytes: pointer to the floating point value as used by the current processor (e.g. for x86 it must be in IEEE 754)
      :returns: success



   .. py:method:: make_reg(*args) -> None

      This function has the following signatures:

          0. make_reg(reg: mreg_t) -> None
          1. make_reg(reg: mreg_t, _size: int) -> None

      # 0: make_reg(reg: mreg_t) -> None

      Create a register operand.


      # 1: make_reg(reg: mreg_t, _size: int) -> None



   .. py:method:: make_gvar(ea: ida_idaapi.ea_t) -> None

      Create a global variable operand.



   .. py:method:: make_stkvar(mba: mba_t, off: int) -> None


   .. py:method:: make_reg_pair(loreg: int, hireg: int, halfsize: int) -> None

      Create pair of registers. 
              
      :param loreg: register holding the low part of the value
      :param hireg: register holding the high part of the value
      :param halfsize: the size of each of loreg/hireg



   .. py:method:: make_insn(ins: minsn_t) -> None

      Create a nested instruction.



   .. py:method:: make_blkref(blknum: int) -> None

      Create a global variable operand.



   .. py:method:: make_helper(name: str) -> None

      Create a helper operand. A helper operand usually keeps a built-in function name like "va_start" It is essentially just an arbitrary identifier without any additional info. 
              



   .. py:method:: empty() -> bool


   .. py:method:: is_glbvar() -> bool

      Is a global variable?



   .. py:method:: is_stkvar() -> bool

      Is a stack variable?



   .. py:method:: is_reg(*args) -> bool

      This function has the following signatures:

          0. is_reg() -> bool
          1. is_reg(_r: mreg_t) -> bool
          2. is_reg(_r: mreg_t, _size: int) -> bool

      # 0: is_reg() -> bool

      Is a register operand? See also get_mreg_name() 
              

      # 1: is_reg(_r: mreg_t) -> bool

      Is the specified register?


      # 2: is_reg(_r: mreg_t, _size: int) -> bool

      Is the specified register of the specified size?



   .. py:method:: is_arglist() -> bool

      Is a list of arguments?



   .. py:method:: is_cc() -> bool

      Is a condition code?



   .. py:method:: is_bit_reg(*args) -> bool

      This function has the following signatures:

          0. is_bit_reg() -> bool
          1. is_bit_reg(reg: mreg_t) -> bool

      # 0: is_bit_reg() -> bool


      # 1: is_bit_reg(reg: mreg_t) -> bool

      Is a bit register? This includes condition codes and eventually other bit registers 
              



   .. py:method:: is_kreg() -> bool

      Is a kernel register?



   .. py:method:: is_mblock(*args) -> bool

      This function has the following signatures:

          0. is_mblock() -> bool
          1. is_mblock(serial: int) -> bool

      # 0: is_mblock() -> bool

      Is a block reference?


      # 1: is_mblock(serial: int) -> bool

      Is a block reference to the specified block?



   .. py:method:: is_scattered() -> bool

      Is a scattered operand?



   .. py:method:: is_glbaddr(*args) -> bool

      This function has the following signatures:

          0. is_glbaddr() -> bool
          1. is_glbaddr(ea: ida_idaapi.ea_t) -> bool

      # 0: is_glbaddr() -> bool

      Is address of a global memory cell?


      # 1: is_glbaddr(ea: ida_idaapi.ea_t) -> bool

      Is address of the specified global memory cell?



   .. py:method:: is_stkaddr() -> bool

      Is address of a stack variable?



   .. py:method:: is_insn(*args) -> bool

      This function has the following signatures:

          0. is_insn() -> bool
          1. is_insn(code: mcode_t) -> bool

      # 0: is_insn() -> bool

      Is a sub-instruction?


      # 1: is_insn(code: mcode_t) -> bool

      Is a sub-instruction with the specified opcode?



   .. py:method:: has_side_effects(include_ldx_and_divs: bool = False) -> bool

      Has any side effects? 
              
      :param include_ldx_and_divs: consider ldx/div/mod as having side effects?



   .. py:method:: may_use_aliased_memory() -> bool

      Is it possible for the operand to use aliased memory?



   .. py:method:: is01() -> bool

      Are the possible values of the operand only 0 and 1? This function returns true for 0/1 constants, bit registers, the result of 'set' insns, etc. 
              



   .. py:method:: is_sign_extended_from(nbytes: int) -> bool

      Does the high part of the operand consist of the sign bytes? 
              
      :param nbytes: number of bytes that were sign extended. the remaining size-nbytes high bytes must be sign bytes Example: is_sign_extended_from(xds.4(op.1), 1) -> true because the high 3 bytes are certainly sign bits



   .. py:method:: is_zero_extended_from(nbytes: int) -> bool

      Does the high part of the operand consist of zero bytes? 
              
      :param nbytes: number of bytes that were zero extended. the remaining size-nbytes high bytes must be zero Example: is_zero_extended_from(xdu.8(op.1), 2) -> true because the high 6 bytes are certainly zero



   .. py:method:: is_extended_from(nbytes: int, is_signed: bool) -> bool

      Does the high part of the operand consist of zero or sign bytes?



   .. py:method:: equal_mops(rop: mop_t, eqflags: int) -> bool

      Compare operands. This is the main comparison function for operands. 
              
      :param rop: operand to compare with
      :param eqflags: combination of comparison bits bits



   .. py:method:: lexcompare(rop: mop_t) -> int


   .. py:method:: for_all_ops(mv: mop_visitor_t, type: tinfo_t = None, is_target: bool = False) -> int

      Visit the operand and all its sub-operands. This function visits the current operand as well. 
              
      :param mv: visitor object
      :param type: operand type
      :param is_target: is a destination operand?



   .. py:method:: for_all_scattered_submops(sv: scif_visitor_t) -> int

      Visit all sub-operands of a scattered operand. This function does not visit the current operand, only its sub-operands. All sub-operands are synthetic and are destroyed after the visitor. This function works only with scattered operands. 
              
      :param sv: visitor object



   .. py:method:: value(is_signed: bool) -> uint64

      Retrieve value of a constant integer operand. These functions can be called only for mop_n operands. See is_constant() that can be called on any operand. 
              



   .. py:method:: signed_value() -> int64


   .. py:method:: unsigned_value() -> uint64


   .. py:method:: update_numop_value(val: uint64) -> None


   .. py:method:: is_constant(is_signed: bool = True) -> bool

      Retrieve value of a constant integer operand. 
              
      :param is_signed: should treat the value as signed
      :returns: true if the operand is mop_n



   .. py:method:: is_equal_to(n: uint64, is_signed: bool = True) -> bool


   .. py:method:: is_zero() -> bool


   .. py:method:: is_one() -> bool


   .. py:method:: is_positive_constant() -> bool


   .. py:method:: is_negative_constant() -> bool


   .. py:method:: get_stkvar(udm: udm_t = None, p_idaoff: uval_t * = None) -> ssize_t

      Retrieve the referenced stack variable. 
              
      :param udm: stkvar, may be nullptr
      :param p_idaoff: if specified, will hold IDA stkoff after the call.
      :returns: index of stkvar in the frame or -1



   .. py:method:: get_stkoff(p_vdoff: sval_t *) -> bool

      Get the referenced stack offset. This function can also handle mop_sc if it is entirely mapped into a continuous stack region. 
              
      :param p_vdoff: the output buffer
      :returns: success



   .. py:method:: get_insn(code: mcode_t) -> minsn_t *

      Get subinstruction of the operand. If the operand has a subinstruction with the specified opcode, return it. 
              
      :param code: desired opcode
      :returns: pointer to the instruction or nullptr



   .. py:method:: make_low_half(width: int) -> bool

      Make the low part of the operand. This function takes into account the memory endianness (byte sex) 
              
      :param width: the desired size of the operand part in bytes
      :returns: success



   .. py:method:: make_high_half(width: int) -> bool

      Make the high part of the operand. This function takes into account the memory endianness (byte sex) 
              
      :param width: the desired size of the operand part in bytes
      :returns: success



   .. py:method:: make_first_half(width: int) -> bool

      Make the first part of the operand. This function does not care about the memory endianness 
              
      :param width: the desired size of the operand part in bytes
      :returns: success



   .. py:method:: make_second_half(width: int) -> bool

      Make the second part of the operand. This function does not care about the memory endianness 
              
      :param width: the desired size of the operand part in bytes
      :returns: success



   .. py:method:: shift_mop(offset: int) -> bool

      Shift the operand. This function shifts only the beginning of the operand. The operand size will be changed. Examples: shift_mop(AH.1, -1) -> AX.2 shift_mop(qword_00000008.8, 4) -> dword_0000000C.4 shift_mop(xdu.8(op.4), 4) -> #0.4 shift_mop(#0x12345678.4, 3) -> #12.1 
              
      :param offset: shift count (the number of bytes to shift)
      :returns: success



   .. py:method:: change_size(nsize: int, sideff: side_effect_t = WITH_SIDEFF) -> bool

      Change the operand size. Examples: change_size(AL.1, 2) -> AX.2 change_size(qword_00000008.8, 4) -> dword_00000008.4 change_size(xdu.8(op.4), 4) -> op.4 change_size(#0x12345678.4, 1) -> #0x78.1 
              
      :param nsize: new operand size
      :param sideff: may modify the database because of the size change?
      :returns: success



   .. py:method:: double_size(sideff: side_effect_t = WITH_SIDEFF) -> bool


   .. py:method:: preserve_side_effects(blk: mblock_t, top: minsn_t, moved_calls: bool * = None) -> bool

      Move subinstructions with side effects out of the operand. If we decide to delete an instruction operand, it is a good idea to call this function. Alternatively we should skip such operands by calling mop_t::has_side_effects() For example, if we transform: jnz x, x, @blk => goto @blk then we must call this function before deleting the X operands. 
              
      :param blk: current block
      :param top: top level instruction that contains our operand
      :param moved_calls: pointer to the boolean that will track if all side effects get handled correctly. must be false initially.
      :returns: false failed to preserve a side effect, it is not safe to delete the operand true no side effects or successfully preserved them



   .. py:method:: apply_ld_mcode(mcode: mcode_t, ea: ida_idaapi.ea_t, newsize: int) -> None

      Apply a unary opcode to the operand. 
              
      :param mcode: opcode to apply. it must accept 'l' and 'd' operands but not 'r'. examples: m_low/m_high/m_xds/m_xdu
      :param ea: value of minsn_t::ea for the newly created insruction
      :param newsize: new operand size Example: apply_ld_mcode(m_low) will convert op => low(op)



   .. py:method:: apply_xdu(ea: ida_idaapi.ea_t, newsize: int) -> None


   .. py:method:: apply_xds(ea: ida_idaapi.ea_t, newsize: int) -> None


   .. py:attribute:: obj_id


   .. py:method:: replace_by(o)


   .. py:attribute:: meminfo


   .. py:property:: nnn


   .. py:property:: d


   .. py:property:: s


   .. py:property:: f


   .. py:property:: l


   .. py:property:: a


   .. py:property:: c


   .. py:property:: fpc


   .. py:property:: pair


   .. py:property:: scif


   .. py:property:: r


   .. py:property:: g


   .. py:property:: b


   .. py:property:: cstr


   .. py:property:: helper


.. py:data:: OPROP_IMPDONE

   imported operand (a pointer) has been dereferenced


.. py:data:: OPROP_UDT

   a struct or union


.. py:data:: OPROP_FLOAT

   possibly floating value


.. py:data:: OPROP_CCFLAGS

   mop_n: a pc-relative value mop_a: an address obtained from a relocation else: value of a condition code register (like mr_cc) 
           


.. py:data:: OPROP_UDEFVAL

   uses undefined value


.. py:data:: OPROP_LOWADDR

   a low address offset


.. py:data:: OPROP_ABI

   is used to organize arg/retval of a call such operands should be combined more carefully than others at least on BE platforms 
           


.. py:function:: lexcompare(a: mop_t, b: mop_t) -> int

.. py:class:: mop_pair_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: lop
      :type:  mop_t

      low operand



   .. py:attribute:: hop
      :type:  mop_t

      high operand



.. py:class:: mop_addr_t(*args)

   Bases: :py:obj:`mop_t`


   .. py:attribute:: thisown


   .. py:attribute:: insize
      :type:  int


   .. py:attribute:: outsize
      :type:  int


   .. py:method:: lexcompare(ra: mop_addr_t) -> int


.. py:class:: mcallarg_t(*args)

   Bases: :py:obj:`mop_t`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      address where the argument was initialized. BADADDR means unknown. 
              



   .. py:attribute:: type
      :type:  tinfo_t

      formal argument type



   .. py:attribute:: name
      :type:  str

      formal argument name



   .. py:attribute:: argloc
      :type:  argloc_t

      ida argloc



   .. py:attribute:: flags
      :type:  int

      FAI_...



   .. py:method:: copy_mop(op: mop_t) -> None


   .. py:method:: dstr() -> str


   .. py:method:: set_regarg(*args) -> None

      This function has the following signatures:

          0. set_regarg(mr: mreg_t, sz: int, tif: const tinfo_t &) -> None
          1. set_regarg(mr: mreg_t, tif: const tinfo_t &) -> None
          2. set_regarg(mr: mreg_t, dt: char, sign: type_sign_t=type_unsigned) -> None

      # 0: set_regarg(mr: mreg_t, sz: int, tif: const tinfo_t &) -> None


      # 1: set_regarg(mr: mreg_t, tif: const tinfo_t &) -> None


      # 2: set_regarg(mr: mreg_t, dt: char, sign: type_sign_t=type_unsigned) -> None



   .. py:method:: make_int(val: int, val_ea: ida_idaapi.ea_t, opno: int = 0) -> None


   .. py:method:: make_uint(val: int, val_ea: ida_idaapi.ea_t, opno: int = 0) -> None


.. py:data:: ROLE_UNK

   unknown function role


.. py:data:: ROLE_EMPTY

   empty, does not do anything (maybe spoils regs)


.. py:data:: ROLE_MEMSET

   memset(void *dst, uchar value, size_t count);


.. py:data:: ROLE_MEMSET32

   memset32(void *dst, uint32 value, size_t count);


.. py:data:: ROLE_MEMSET64

   memset64(void *dst, uint64 value, size_t count);


.. py:data:: ROLE_MEMCPY

   memcpy(void *dst, const void *src, size_t count);


.. py:data:: ROLE_STRCPY

   strcpy(char *dst, const char *src);


.. py:data:: ROLE_STRLEN

   strlen(const char *src);


.. py:data:: ROLE_STRCAT

   strcat(char *dst, const char *src);


.. py:data:: ROLE_TAIL

   char *tail(const char *str);


.. py:data:: ROLE_BUG

   BUG() helper macro: never returns, causes exception.


.. py:data:: ROLE_ALLOCA

   alloca() function


.. py:data:: ROLE_BSWAP

   bswap() function (any size)


.. py:data:: ROLE_PRESENT

   present() function (used in patterns)


.. py:data:: ROLE_CONTAINING_RECORD

   CONTAINING_RECORD() macro.


.. py:data:: ROLE_FASTFAIL

   __fastfail()


.. py:data:: ROLE_READFLAGS

   __readeflags, __readcallersflags


.. py:data:: ROLE_IS_MUL_OK

   is_mul_ok


.. py:data:: ROLE_SATURATED_MUL

   saturated_mul


.. py:data:: ROLE_BITTEST

   [lock] bt


.. py:data:: ROLE_BITTESTANDSET

   [lock] bts


.. py:data:: ROLE_BITTESTANDRESET

   [lock] btr


.. py:data:: ROLE_BITTESTANDCOMPLEMENT

   [lock] btc


.. py:data:: ROLE_VA_ARG

   va_arg() macro


.. py:data:: ROLE_VA_COPY

   va_copy() function


.. py:data:: ROLE_VA_START

   va_start() function


.. py:data:: ROLE_VA_END

   va_end() function


.. py:data:: ROLE_ROL

   rotate left


.. py:data:: ROLE_ROR

   rotate right


.. py:data:: ROLE_CFSUB3

   carry flag after subtract with carry


.. py:data:: ROLE_OFSUB3

   overflow flag after subtract with carry


.. py:data:: ROLE_ABS

   integer absolute value


.. py:data:: ROLE_3WAYCMP0

   3-way compare helper, returns -1/0/1


.. py:data:: ROLE_3WAYCMP1

   3-way compare helper, returns 0/1/2


.. py:data:: ROLE_WMEMCPY

   wchar_t *wmemcpy(wchar_t *dst, const wchar_t *src, size_t n)


.. py:data:: ROLE_WMEMSET

   wchar_t *wmemset(wchar_t *dst, wchar_t wc, size_t n)


.. py:data:: ROLE_WCSCPY

   wchar_t *wcscpy(wchar_t *dst, const wchar_t *src);


.. py:data:: ROLE_WCSLEN

   size_t wcslen(const wchar_t *s)


.. py:data:: ROLE_WCSCAT

   wchar_t *wcscat(wchar_t *dst, const wchar_t *src)


.. py:data:: ROLE_SSE_CMP4

   e.g. _mm_cmpgt_ss


.. py:data:: ROLE_SSE_CMP8

   e.g. _mm_cmpgt_sd


.. py:data:: FUNC_NAME_MEMCPY

.. py:data:: FUNC_NAME_WMEMCPY

.. py:data:: FUNC_NAME_MEMSET

.. py:data:: FUNC_NAME_WMEMSET

.. py:data:: FUNC_NAME_MEMSET32

.. py:data:: FUNC_NAME_MEMSET64

.. py:data:: FUNC_NAME_STRCPY

.. py:data:: FUNC_NAME_WCSCPY

.. py:data:: FUNC_NAME_STRLEN

.. py:data:: FUNC_NAME_WCSLEN

.. py:data:: FUNC_NAME_STRCAT

.. py:data:: FUNC_NAME_WCSCAT

.. py:data:: FUNC_NAME_TAIL

.. py:data:: FUNC_NAME_VA_ARG

.. py:data:: FUNC_NAME_EMPTY

.. py:data:: FUNC_NAME_PRESENT

.. py:data:: FUNC_NAME_CONTAINING_RECORD

.. py:data:: FUNC_NAME_MORESTACK

.. py:class:: mcallinfo_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: callee
      :type:  ida_idaapi.ea_t

      address of the called function, if known



   .. py:attribute:: solid_args
      :type:  int

      number of solid args. there may be variadic args in addtion 
              



   .. py:attribute:: call_spd
      :type:  int

      sp value at call insn



   .. py:attribute:: stkargs_top
      :type:  int

      first offset past stack arguments



   .. py:attribute:: cc
      :type:  callcnv_t

      calling convention



   .. py:attribute:: args
      :type:  mcallargs_t

      call arguments



   .. py:attribute:: retregs
      :type:  mopvec_t

      return register(s) (e.g., AX, AX:DX, etc.) this vector is built from return_regs 
              



   .. py:attribute:: return_type
      :type:  tinfo_t

      type of the returned value



   .. py:attribute:: return_argloc
      :type:  argloc_t

      location of the returned value



   .. py:attribute:: return_regs
      :type:  mlist_t

      list of values returned by the function



   .. py:attribute:: spoiled
      :type:  mlist_t

      list of spoiled locations (includes return_regs)



   .. py:attribute:: pass_regs
      :type:  mlist_t

      passthrough registers: registers that depend on input values (subset of spoiled) 
              



   .. py:attribute:: visible_memory
      :type:  ivlset_t

      what memory is visible to the call?



   .. py:attribute:: dead_regs
      :type:  mlist_t

      registers defined by the function but never used. upon propagation we do the following:
      * dead_regs += return_regs
      * retregs.clear() since the call is propagated 


              



   .. py:attribute:: flags
      :type:  int

      combination of Call properties... bits 
              



   .. py:attribute:: role
      :type:  funcrole_t

      function role



   .. py:attribute:: fti_attrs
      :type:  type_attrs_t

      extended function attributes



   .. py:method:: lexcompare(f: mcallinfo_t) -> int


   .. py:method:: set_type(type: tinfo_t) -> bool


   .. py:method:: get_type() -> tinfo_t


   .. py:method:: is_vararg() -> bool


   .. py:method:: dstr() -> str


.. py:data:: FCI_PROP

   call has been propagated


.. py:data:: FCI_DEAD

   some return registers were determined dead


.. py:data:: FCI_FINAL

   call type is final, should not be changed


.. py:data:: FCI_NORET

   call does not return


.. py:data:: FCI_PURE

   pure function


.. py:data:: FCI_NOSIDE

   call does not have side effects


.. py:data:: FCI_SPLOK

   spoiled/visible_memory lists have been optimized. for some functions we can reduce them as soon as information about the arguments becomes available. in order not to try optimize them again we use this bit. 
           


.. py:data:: FCI_HASCALL

   A function is an synthetic helper combined from several instructions and at least one of them was a call to a real functions 
           


.. py:data:: FCI_HASFMT

   A variadic function with recognized printf- or scanf-style format string 
           


.. py:data:: FCI_EXPLOCS

   all arglocs are specified explicitly


.. py:class:: mcases_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: values
      :type:  casevec_t

      expression values for each target



   .. py:attribute:: targets
      :type:  intvec_t

      target block numbers



   .. py:method:: swap(r: mcases_t) -> None


   .. py:method:: compare(r: mcases_t) -> int


   .. py:method:: empty() -> bool


   .. py:method:: size() -> size_t


   .. py:method:: resize(s: int) -> None


   .. py:method:: dstr() -> str


.. py:class:: voff_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: off
      :type:  int

      register number or stack offset



   .. py:attribute:: type
      :type:  mopt_t

      mop_r - register, mop_S - stack, mop_z - undefined



   .. py:method:: set(_type: mopt_t, _off: int) -> None


   .. py:method:: set_stkoff(stkoff: int) -> None


   .. py:method:: set_reg(mreg: mreg_t) -> None


   .. py:method:: undef() -> None


   .. py:method:: defined() -> bool


   .. py:method:: is_reg() -> bool


   .. py:method:: is_stkoff() -> bool


   .. py:method:: get_reg() -> mreg_t


   .. py:method:: get_stkoff() -> int


   .. py:method:: inc(delta: int) -> None


   .. py:method:: add(width: int) -> voff_t


   .. py:method:: diff(r: voff_t) -> int


   .. py:method:: compare(r: voff_t) -> int


.. py:class:: vivl_t(*args)

   Bases: :py:obj:`voff_t`


   .. py:attribute:: thisown


   .. py:attribute:: size
      :type:  int

      Interval size in bytes.



   .. py:method:: set(*args) -> None

      This function has the following signatures:

          0. set(_type: mopt_t, _off: int, _size: int=0) -> None
          1. set(voff: const voff_t &, _size: int) -> None

      # 0: set(_type: mopt_t, _off: int, _size: int=0) -> None


      # 1: set(voff: const voff_t &, _size: int) -> None



   .. py:method:: set_stkoff(stkoff: int, sz: int = 0) -> None


   .. py:method:: set_reg(mreg: mreg_t, sz: int = 0) -> None


   .. py:method:: extend_to_cover(r: vivl_t) -> bool

      Extend a value interval using another value interval of the same type 
              
      :returns: success



   .. py:method:: intersect(r: vivl_t) -> int

      Intersect value intervals the same type 
              
      :returns: size of the resulting intersection



   .. py:method:: overlap(r: vivl_t) -> bool

      Do two value intervals overlap?



   .. py:method:: includes(r: vivl_t) -> bool

      Does our value interval include another?



   .. py:method:: contains(voff2: voff_t) -> bool

      Does our value interval contain the specified value offset?



   .. py:method:: compare(r: vivl_t) -> int


   .. py:method:: dstr() -> str


.. py:class:: chain_t(*args)

   Bases: :py:obj:`ida_pro.intvec_t`


   .. py:attribute:: thisown


   .. py:attribute:: width
      :type:  int

      size of the value in bytes



   .. py:attribute:: varnum
      :type:  int

      allocated variable index (-1 - not allocated yet)



   .. py:attribute:: flags
      :type:  uchar

      combination Chain properties bits 
              



   .. py:method:: set_value(r: chain_t) -> None


   .. py:method:: key() -> voff_t const &


   .. py:method:: is_inited() -> bool


   .. py:method:: is_reg() -> bool


   .. py:method:: is_stkoff() -> bool


   .. py:method:: is_replaced() -> bool


   .. py:method:: is_overlapped() -> bool


   .. py:method:: is_fake() -> bool


   .. py:method:: is_passreg() -> bool


   .. py:method:: is_term() -> bool


   .. py:method:: set_inited(b: bool) -> None


   .. py:method:: set_replaced(b: bool) -> None


   .. py:method:: set_overlapped(b: bool) -> None


   .. py:method:: set_term(b: bool) -> None


   .. py:method:: get_reg() -> mreg_t


   .. py:method:: get_stkoff() -> int


   .. py:method:: overlap(r: chain_t) -> bool


   .. py:method:: includes(r: chain_t) -> bool


   .. py:method:: endoff() -> voff_t const


   .. py:method:: dstr() -> str


   .. py:method:: append_list(mba: mba_t, list: mlist_t) -> None

      Append the contents of the chain to the specified list of locations.



   .. py:method:: clear_varnum() -> None


.. py:data:: CHF_INITED

   is chain initialized? (valid only after lvar allocation)


.. py:data:: CHF_REPLACED

   chain operands have been replaced?


.. py:data:: CHF_OVER

   overlapped chain


.. py:data:: CHF_FAKE

   fake chain created by widen_chains()


.. py:data:: CHF_PASSTHRU

   pass-thru chain, must use the input variable to the block


.. py:data:: CHF_TERM

   terminating chain; the variable does not survive across the block


.. py:data:: SIZEOF_BLOCK_CHAINS

.. py:class:: block_chains_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: get_reg_chain(reg: mreg_t, width: int = 1) -> chain_t *

      Get chain for the specified register 
              
      :param reg: register number
      :param width: size of register in bytes



   .. py:method:: get_stk_chain(off: int, width: int = 1) -> chain_t *

      Get chain for the specified stack offset 
              
      :param off: stack offset
      :param width: size of stack value in bytes



   .. py:method:: get_chain(*args) -> chain_t *

      This function has the following signatures:

          0. get_chain(k: const voff_t &, width: int=1) -> const chain_t *
          1. get_chain(k: const voff_t &, width: int=1) -> chain_t *
          2. get_chain(ch: const chain_t &) -> const chain_t *
          3. get_chain(ch: const chain_t &) -> chain_t *

      # 0: get_chain(k: const voff_t &, width: int=1) -> const chain_t *

      Get chain for the specified value offset. 
              

      # 1: get_chain(k: const voff_t &, width: int=1) -> chain_t *


      # 2: get_chain(ch: const chain_t &) -> const chain_t *

      Get chain similar to the specified chain 
              

      # 3: get_chain(ch: const chain_t &) -> chain_t *



   .. py:method:: dstr() -> str


.. py:class:: chain_visitor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: parent
      :type:  block_chains_t *

      parent of the current chain



   .. py:method:: visit_chain(nblock: int, ch: chain_t) -> int


.. py:class:: graph_chains_t

   Bases: :py:obj:`block_chains_vec_t`


   .. py:attribute:: thisown


   .. py:method:: for_all_chains(cv: chain_visitor_t, gca_flags: int) -> int

      Visit all chains 
              
      :param cv: chain visitor
      :param gca_flags: combination of GCA_ bits



   .. py:method:: is_locked() -> bool

      Are the chains locked? It is a good idea to lock the chains before using them. This ensures that they won't be recalculated and reallocated during the use. See the chain_keeper_t class for that. 
              



   .. py:method:: acquire() -> None

      Lock the chains.



   .. py:method:: release() -> None

      Unlock the chains.



   .. py:method:: swap(r: graph_chains_t) -> None


.. py:data:: GCA_EMPTY

   include empty chains


.. py:data:: GCA_SPEC

   include chains for special registers


.. py:data:: GCA_ALLOC

   enumerate only allocated chains


.. py:data:: GCA_NALLOC

   enumerate only non-allocated chains


.. py:data:: GCA_OFIRST

   consider only chains of the first block


.. py:data:: GCA_OLAST

   consider only chains of the last block


.. py:class:: minsn_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: opcode
      :type:  mcode_t

      instruction opcode



   .. py:attribute:: iprops
      :type:  int

      combination of instruction property bits bits



   .. py:attribute:: next
      :type:  minsn_t *

      next insn in doubly linked list. check also nexti()



   .. py:attribute:: prev
      :type:  minsn_t *

      prev insn in doubly linked list. check also previ()



   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      instruction address



   .. py:attribute:: l
      :type:  mop_t

      left operand



   .. py:attribute:: r
      :type:  mop_t

      right operand



   .. py:attribute:: d
      :type:  mop_t

      destination operand



   .. py:method:: is_optional() -> bool


   .. py:method:: is_combined() -> bool


   .. py:method:: is_farcall() -> bool


   .. py:method:: is_cleaning_pop() -> bool


   .. py:method:: is_extstx() -> bool


   .. py:method:: is_tailcall() -> bool


   .. py:method:: is_fpinsn() -> bool


   .. py:method:: is_assert() -> bool


   .. py:method:: is_persistent() -> bool


   .. py:method:: is_wild_match() -> bool


   .. py:method:: is_propagatable() -> bool


   .. py:method:: is_ignlowsrc() -> bool


   .. py:method:: is_inverted_jx() -> bool


   .. py:method:: was_noret_icall() -> bool


   .. py:method:: is_multimov() -> bool


   .. py:method:: is_combinable() -> bool


   .. py:method:: was_split() -> bool


   .. py:method:: is_mbarrier() -> bool


   .. py:method:: was_unmerged() -> bool


   .. py:method:: was_unpaired() -> bool


   .. py:method:: set_optional() -> None


   .. py:method:: clr_combined() -> None


   .. py:method:: set_farcall() -> None


   .. py:method:: set_cleaning_pop() -> None


   .. py:method:: set_extstx() -> None


   .. py:method:: set_tailcall() -> None


   .. py:method:: clr_tailcall() -> None


   .. py:method:: set_fpinsn() -> None


   .. py:method:: clr_fpinsn() -> None


   .. py:method:: set_assert() -> None


   .. py:method:: clr_assert() -> None


   .. py:method:: set_persistent() -> None


   .. py:method:: set_wild_match() -> None


   .. py:method:: clr_propagatable() -> None


   .. py:method:: set_ignlowsrc() -> None


   .. py:method:: clr_ignlowsrc() -> None


   .. py:method:: set_inverted_jx() -> None


   .. py:method:: set_noret_icall() -> None


   .. py:method:: clr_noret_icall() -> None


   .. py:method:: set_multimov() -> None


   .. py:method:: clr_multimov() -> None


   .. py:method:: set_combinable() -> None


   .. py:method:: clr_combinable() -> None


   .. py:method:: set_mbarrier() -> None


   .. py:method:: set_unmerged() -> None


   .. py:method:: set_split_size(s: int) -> None


   .. py:method:: get_split_size() -> int


   .. py:method:: swap(m: minsn_t) -> None

      Swap two instructions. The prev/next fields are not modified by this function because it would corrupt the doubly linked list. 
              



   .. py:method:: dstr() -> str

      Get displayable text without tags in a static buffer.



   .. py:method:: setaddr(new_ea: ida_idaapi.ea_t) -> None

      Change the instruction address. This function modifies subinstructions as well. 
              



   .. py:method:: optimize_solo(optflags: int = 0) -> int

      Optimize one instruction without context. This function does not have access to the instruction context (the previous and next instructions in the list, the block number, etc). It performs only basic optimizations that are available without this info. 
              
      :param optflags: combination of optimization flags bits
      :returns: number of changes, 0-unchanged See also mblock_t::optimize_insn()



   .. py:method:: optimize_subtree(blk: mblock_t, top: minsn_t, parent: minsn_t, converted_call: ea_t *, optflags: int = 2) -> int

      Optimize instruction in its context. Do not use this function, use mblock_t::optimize() 
              



   .. py:method:: for_all_ops(mv: mop_visitor_t) -> int

      Visit all instruction operands. This function visits subinstruction operands as well. 
              
      :param mv: operand visitor
      :returns: non-zero value returned by mv.visit_mop() or zero



   .. py:method:: for_all_insns(mv: minsn_visitor_t) -> int

      Visit all instructions. This function visits the instruction itself and all its subinstructions. 
              
      :param mv: instruction visitor
      :returns: non-zero value returned by mv.visit_mop() or zero



   .. py:method:: equal_insns(m: minsn_t, eqflags: int) -> bool

      Compare instructions. This is the main comparison function for instructions. 
              
      :param m: instruction to compare with
      :param eqflags: combination of comparison bits bits



   .. py:method:: lexcompare(ri: minsn_t) -> int


   .. py:method:: is_noret_call(flags: int = 0) -> bool

      Is a non-returing call? 
              
      :param flags: combination of NORET_... bits



   .. py:method:: is_unknown_call() -> bool

      Is an unknown call? Unknown calls are calls without the argument list (mcallinfo_t). Usually the argument lists are determined by mba_t::analyze_calls(). Unknown calls exist until the MMAT_CALLS maturity level. See also mblock_t::is_call_block 
              



   .. py:method:: is_helper(name: str) -> bool

      Is a helper call with the specified name? Helper calls usually have well-known function names (see Well known function names) but they may have any other name. The decompiler does not assume any special meaning for non-well-known names. 
              



   .. py:method:: find_call(with_helpers: bool = False) -> minsn_t *

      Find a call instruction. Check for the current instruction and its subinstructions. 
              
      :param with_helpers: consider helper calls as well?



   .. py:method:: contains_call(with_helpers: bool = False) -> bool

      Does the instruction contain a call?



   .. py:method:: has_side_effects(include_ldx_and_divs: bool = False) -> bool

      Does the instruction have a side effect? 
              
      :param include_ldx_and_divs: consider ldx/div/mod as having side effects? stx is always considered as having side effects. Apart from ldx/std only call may have side effects.



   .. py:method:: get_role() -> funcrole_t

      Get the function role of a call.



   .. py:method:: is_memcpy() -> bool


   .. py:method:: is_memset() -> bool


   .. py:method:: is_alloca() -> bool


   .. py:method:: is_bswap() -> bool


   .. py:method:: is_readflags() -> bool


   .. py:method:: contains_opcode(mcode: mcode_t) -> bool

      Does the instruction have the specified opcode? This function searches subinstructions as well. 
              
      :param mcode: opcode to search for.



   .. py:method:: find_opcode(mcode: mcode_t) -> minsn_t *

      Find a (sub)insruction with the specified opcode. 
              
      :param mcode: opcode to search for.



   .. py:method:: find_ins_op(op: mcode_t = m_nop) -> minsn_t *

      Find an operand that is a subinsruction with the specified opcode. This function checks only the 'l' and 'r' operands of the current insn. 
              
      :param op: opcode to search for
      :returns: &l or &r or nullptr



   .. py:method:: find_num_op() -> mop_t *

      Find a numeric operand of the current instruction. This function checks only the 'l' and 'r' operands of the current insn. 
              
      :returns: &l or &r or nullptr



   .. py:method:: is_mov() -> bool


   .. py:method:: is_like_move() -> bool


   .. py:method:: modifies_d() -> bool

      Does the instruction modify its 'd' operand? Some instructions (e.g. m_stx) do not modify the 'd' operand. 
              



   .. py:method:: modifies_pair_mop() -> bool


   .. py:method:: is_between(m1: minsn_t, m2: minsn_t) -> bool

      Is the instruction in the specified range of instructions? 
              
      :param m1: beginning of the range in the doubly linked list
      :param m2: end of the range in the doubly linked list (excluded, may be nullptr) This function assumes that m1 and m2 belong to the same basic block and they are top level instructions.



   .. py:method:: is_after(m: minsn_t) -> bool

      Is the instruction after the specified one? 
              
      :param m: the instruction to compare against in the list



   .. py:method:: may_use_aliased_memory() -> bool

      Is it possible for the instruction to use aliased memory?



   .. py:method:: serialize(b: bytevec_t *) -> int

      Serialize an instruction 
              
      :param b: the output buffer
      :returns: the serialization format that was used to store info



   .. py:method:: deserialize(bytes: uchar const *, format_version: int) -> bool

      Deserialize an instruction 
              
      :param bytes: pointer to serialized data
      :param format_version: serialization format version. this value is returned by minsn_t::serialize()
      :returns: success



   .. py:attribute:: obj_id


   .. py:method:: replace_by(o)


   .. py:attribute:: meminfo


.. py:data:: IPROP_OPTIONAL

   optional instruction


.. py:data:: IPROP_PERSIST

   persistent insn; they are not destroyed


.. py:data:: IPROP_WILDMATCH

   match multiple insns


.. py:data:: IPROP_CLNPOP

   the purpose of the instruction is to clean stack (e.g. "pop ecx" is often used for that) 
           


.. py:data:: IPROP_FPINSN

   floating point insn


.. py:data:: IPROP_FARCALL

   call of a far function using push cs/call sequence


.. py:data:: IPROP_TAILCALL

   tail call


.. py:data:: IPROP_ASSERT

   assertion: usually mov #val, op. assertions are used to help the optimizer. assertions are ignored when generating ctree 
           


.. py:data:: IPROP_SPLIT

   the instruction has been split:


.. py:data:: IPROP_SPLIT1

   into 1 byte


.. py:data:: IPROP_SPLIT2

   into 2 bytes


.. py:data:: IPROP_SPLIT4

   into 4 bytes


.. py:data:: IPROP_SPLIT8

   into 8 bytes


.. py:data:: IPROP_COMBINED

   insn has been modified because of a partial reference


.. py:data:: IPROP_EXTSTX

   this is m_ext propagated into m_stx


.. py:data:: IPROP_IGNLOWSRC

   low part of the instruction source operand has been created artificially (this bit is used only for 'and x, 80...') 
           


.. py:data:: IPROP_INV_JX

   inverted conditional jump


.. py:data:: IPROP_WAS_NORET

   was noret icall


.. py:data:: IPROP_MULTI_MOV

   bits that can be set by plugins:

   the minsn was generated as part of insn that moves multiple registers (example: STM on ARM may transfer multiple registers) 
           


.. py:data:: IPROP_DONT_PROP

   may not propagate


.. py:data:: IPROP_DONT_COMB

   may not combine this instruction with others


.. py:data:: IPROP_MBARRIER

   this instruction acts as a memory barrier (instructions accessing memory may not be reordered past it) 
           


.. py:data:: IPROP_UNMERGED

   'goto' instruction was transformed info 'call'


.. py:data:: IPROP_UNPAIRED

   instruction is a result of del_dest_pairs() transformation


.. py:data:: OPTI_ADDREXPRS

   optimize all address expressions (&x+N; &x-&y)


.. py:data:: OPTI_MINSTKREF

   may update minstkref


.. py:data:: OPTI_COMBINSNS

   may combine insns (only for optimize_insn)


.. py:data:: OPTI_NO_LDXOPT

   the function is called after the propagation attempt, we do not optimize low/high(ldx) in this case 
           


.. py:data:: OPTI_NO_VALRNG

   forbid using valranges


.. py:data:: EQ_IGNSIZE

   ignore source operand sizes


.. py:data:: EQ_IGNCODE

   ignore instruction opcodes


.. py:data:: EQ_CMPDEST

   compare instruction destinations


.. py:data:: EQ_OPTINSN

   optimize mop_d operands


.. py:data:: NORET_IGNORE_WAS_NORET_ICALL

.. py:data:: NORET_FORBID_ANALYSIS

.. py:function:: getf_reginsn(ins: minsn_t) -> minsn_t *

   Skip assertions forward.


.. py:function:: getb_reginsn(ins: minsn_t) -> minsn_t *

   Skip assertions backward.


.. py:class:: intval64_t(v: uint64 = 0, _s: int = 1)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: val
      :type:  uint64


   .. py:attribute:: size
      :type:  int


   .. py:method:: sval() -> int64


   .. py:method:: uval() -> uint64


   .. py:method:: sext(target_sz: int) -> intval64_t


   .. py:method:: zext(target_sz: int) -> intval64_t


   .. py:method:: low(target_sz: int) -> intval64_t


   .. py:method:: high(target_sz: int) -> intval64_t


   .. py:method:: sdiv(o: intval64_t) -> intval64_t


   .. py:method:: smod(o: intval64_t) -> intval64_t


   .. py:method:: sar(o: intval64_t) -> intval64_t


.. py:class:: int64_emulator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: get_mop_value(mop: mop_t) -> intval64_t


   .. py:method:: mop_value(mop: mop_t) -> intval64_t


   .. py:method:: minsn_value(insn: minsn_t) -> intval64_t


.. py:data:: BLT_NONE

   unknown block type


.. py:data:: BLT_STOP

   stops execution regularly (must be the last block)


.. py:data:: BLT_0WAY

   does not have successors (tail is a noret function)


.. py:data:: BLT_1WAY

   passes execution to one block (regular or goto block)


.. py:data:: BLT_2WAY

   passes execution to two blocks (conditional jump)


.. py:data:: BLT_NWAY

   passes execution to many blocks (switch idiom)


.. py:data:: BLT_XTRN

   external block (out of function address)


.. py:class:: mblock_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: nextb
      :type:  mblock_t *

      next block in the doubly linked list



   .. py:attribute:: prevb
      :type:  mblock_t *

      previous block in the doubly linked list



   .. py:attribute:: flags
      :type:  int

      combination of Basic block properties bits 
              



   .. py:attribute:: start
      :type:  ida_idaapi.ea_t

      start address



   .. py:attribute:: end
      :type:  ida_idaapi.ea_t

      end address note: we cannot rely on start/end addresses very much because instructions are propagated between blocks 
              



   .. py:attribute:: head
      :type:  minsn_t *

      pointer to the first instruction of the block



   .. py:attribute:: tail
      :type:  minsn_t *

      pointer to the last instruction of the block



   .. py:attribute:: mba
      :type:  mba_t *

      the parent micro block array



   .. py:attribute:: serial
      :type:  int

      block number



   .. py:attribute:: type
      :type:  mblock_type_t

      block type (BLT_NONE - not computed yet)



   .. py:attribute:: dead_at_start
      :type:  mlist_t

      data that is dead at the block entry



   .. py:attribute:: mustbuse
      :type:  mlist_t

      data that must be used by the block



   .. py:attribute:: maybuse
      :type:  mlist_t

      data that may be used by the block



   .. py:attribute:: mustbdef
      :type:  mlist_t

      data that must be defined by the block



   .. py:attribute:: maybdef
      :type:  mlist_t

      data that may be defined by the block



   .. py:attribute:: dnu
      :type:  mlist_t

      data that is defined but not used in the block



   .. py:attribute:: maxbsp
      :type:  int

      maximal sp value in the block (0...stacksize)



   .. py:attribute:: minbstkref
      :type:  int

      lowest stack location accessible with indirect addressing (offset from the stack bottom) initially it is 0 (not computed) 
              



   .. py:attribute:: minbargref
      :type:  int

      the same for arguments



   .. py:attribute:: predset
      :type:  intvec_t

      control flow graph: list of our predecessors use npred() and pred() to access it 
              



   .. py:attribute:: succset
      :type:  intvec_t

      control flow graph: list of our successors use nsucc() and succ() to access it 
              



   .. py:method:: mark_lists_dirty() -> None


   .. py:method:: request_propagation() -> None


   .. py:method:: needs_propagation() -> bool


   .. py:method:: request_demote64() -> None


   .. py:method:: lists_dirty() -> bool


   .. py:method:: lists_ready() -> bool


   .. py:method:: make_lists_ready() -> int


   .. py:method:: npred() -> int

      Get number of block predecessors.



   .. py:method:: nsucc() -> int

      Get number of block successors.



   .. py:method:: pred(n: int) -> int


   .. py:method:: succ(n: int) -> int


   .. py:method:: empty() -> bool


   .. py:method:: dump() -> None

      Dump block info. This function is useful for debugging, see mba_t::dump for info 
              



   .. py:method:: dump_block(title: str) -> None


   .. py:method:: insert_into_block(nm: minsn_t, om: minsn_t) -> minsn_t *

      Insert instruction into the doubly linked list 
              
      :param nm: new instruction
      :param om: existing instruction, part of the doubly linked list if nullptr, then the instruction will be inserted at the beginning of the list NM will be inserted immediately after OM
      :returns: pointer to NM



   .. py:method:: remove_from_block(m: minsn_t) -> minsn_t *

      Remove instruction from the doubly linked list 
              
      :param m: instruction to remove The removed instruction is not deleted, the caller gets its ownership
      :returns: pointer to the next instruction



   .. py:method:: for_all_insns(mv: minsn_visitor_t) -> int

      Visit all instructions. This function visits subinstructions too. 
              
      :param mv: instruction visitor
      :returns: zero or the value returned by mv.visit_insn() See also mba_t::for_all_topinsns()



   .. py:method:: for_all_ops(mv: mop_visitor_t) -> int

      Visit all operands. This function visit subinstruction operands too. 
              
      :param mv: operand visitor
      :returns: zero or the value returned by mv.visit_mop()



   .. py:method:: for_all_uses(list: mlist_t, i1: minsn_t, i2: minsn_t, mmv: mlist_mop_visitor_t) -> int

      Visit all operands that use LIST. 
              
      :param list: ptr to the list of locations. it may be modified: parts that get redefined by the instructions in [i1,i2) will be deleted.
      :param i1: starting instruction. must be a top level insn.
      :param i2: ending instruction (excluded). must be a top level insn.
      :param mmv: operand visitor
      :returns: zero or the value returned by mmv.visit_mop()



   .. py:method:: optimize_insn(*args) -> int

      Optimize one instruction in the context of the block. 
              
      :param m: pointer to a top level instruction
      :param optflags: combination of optimization flags bits
      :returns: number of changes made to the block This function may change other instructions in the block too. However, it will not destroy top level instructions (it may convert them to nop's). This function performs only intrablock modifications. See also minsn_t::optimize_solo()



   .. py:method:: optimize_block() -> int

      Optimize a basic block. Usually there is no need to call this function explicitly because the decompiler will call it itself if optinsn_t::func or optblock_t::func return non-zero. 
              
      :returns: number of changes made to the block



   .. py:method:: build_lists(kill_deads: bool) -> int

      Build def-use lists and eliminate deads. 
              
      :param kill_deads: do delete dead instructions?
      :returns: the number of eliminated instructions Better mblock_t::call make_lists_ready() rather than this function.



   .. py:method:: optimize_useless_jump() -> int

      Remove a jump at the end of the block if it is useless. This function preserves any side effects when removing a useless jump. Both conditional and unconditional jumps are handled (and jtbl too). This function deletes useless jumps, not only replaces them with a nop. (please note that \optimize_insn does not handle useless jumps). 
              
      :returns: number of changes made to the block



   .. py:method:: append_use_list(*args) -> None

      Append use-list of an operand. This function calculates list of locations that may or must be used by the operand and appends it to LIST. 
              
      :param list: ptr to the output buffer. we will append to it.
      :param op: operand to calculate the use list of
      :param maymust: should we calculate 'may-use' or 'must-use' list? see maymust_t for more details.
      :param mask: if only part of the operand should be considered, a bitmask can be used to specify which part. example: op=AX,mask=0xFF means that we will consider only AL.



   .. py:method:: append_def_list(list: mlist_t, op: mop_t, maymust: maymust_t) -> None

      Append def-list of an operand. This function calculates list of locations that may or must be modified by the operand and appends it to LIST. 
              
      :param list: ptr to the output buffer. we will append to it.
      :param op: operand to calculate the def list of
      :param maymust: should we calculate 'may-def' or 'must-def' list? see maymust_t for more details.



   .. py:method:: build_use_list(ins: minsn_t, maymust: maymust_t) -> mlist_t

      Build use-list of an instruction. This function calculates list of locations that may or must be used by the instruction. Examples: "ldx ds.2, eax.4, ebx.4", may-list: all aliasable memory "ldx ds.2, eax.4, ebx.4", must-list: empty Since LDX uses EAX for indirect access, it may access any aliasable memory. On the other hand, we cannot tell for sure which memory cells will be accessed, this is why the must-list is empty. 
              
      :param ins: instruction to calculate the use list of
      :param maymust: should we calculate 'may-use' or 'must-use' list? see maymust_t for more details.
      :returns: the calculated use-list



   .. py:method:: build_def_list(ins: minsn_t, maymust: maymust_t) -> mlist_t

      Build def-list of an instruction. This function calculates list of locations that may or must be modified by the instruction. Examples: "stx ebx.4, ds.2, eax.4", may-list: all aliasable memory "stx ebx.4, ds.2, eax.4", must-list: empty Since STX uses EAX for indirect access, it may modify any aliasable memory. On the other hand, we cannot tell for sure which memory cells will be modified, this is why the must-list is empty. 
              
      :param ins: instruction to calculate the def list of
      :param maymust: should we calculate 'may-def' or 'must-def' list? see maymust_t for more details.
      :returns: the calculated def-list



   .. py:method:: is_used(*args) -> bool

      Is the list used by the specified instruction range? 
              
      :param list: list of locations. LIST may be modified by the function: redefined locations will be removed from it.
      :param i1: starting instruction of the range (must be a top level insn)
      :param i2: end instruction of the range (must be a top level insn) i2 is excluded from the range. it can be specified as nullptr. i1 and i2 must belong to the same block.
      :param maymust: should we search in 'may-access' or 'must-access' mode?



   .. py:method:: find_first_use(*args) -> minsn_t *

      This function has the following signatures:

          0. find_first_use(list: mlist_t *, i1: const minsn_t *, i2: const minsn_t *, maymust: maymust_t=MAY_ACCESS) -> const minsn_t *
          1. find_first_use(list: mlist_t *, i1: minsn_t *, i2: const minsn_t *, maymust: maymust_t=MAY_ACCESS) -> minsn_t *

      # 0: find_first_use(list: mlist_t *, i1: const minsn_t *, i2: const minsn_t *, maymust: maymust_t=MAY_ACCESS) -> const minsn_t *

      Find the first insn that uses the specified list in the insn range. 
              
      :returns: pointer to such instruction or nullptr. Upon return LIST will contain only locations not redefined by insns [i1..result]

      # 1: find_first_use(list: mlist_t *, i1: minsn_t *, i2: const minsn_t *, maymust: maymust_t=MAY_ACCESS) -> minsn_t *



   .. py:method:: is_redefined(*args) -> bool

      Is the list redefined by the specified instructions? 
              
      :param list: list of locations to check.
      :param i1: starting instruction of the range (must be a top level insn)
      :param i2: end instruction of the range (must be a top level insn) i2 is excluded from the range. it can be specified as nullptr. i1 and i2 must belong to the same block.
      :param maymust: should we search in 'may-access' or 'must-access' mode?



   .. py:method:: find_redefinition(*args) -> minsn_t *

      This function has the following signatures:

          0. find_redefinition(list: const mlist_t &, i1: const minsn_t *, i2: const minsn_t *, maymust: maymust_t=MAY_ACCESS) -> const minsn_t *
          1. find_redefinition(list: const mlist_t &, i1: minsn_t *, i2: const minsn_t *, maymust: maymust_t=MAY_ACCESS) -> minsn_t *

      # 0: find_redefinition(list: const mlist_t &, i1: const minsn_t *, i2: const minsn_t *, maymust: maymust_t=MAY_ACCESS) -> const minsn_t *

      Find the first insn that redefines any part of the list in the insn range. 
              
      :returns: pointer to such instruction or nullptr.

      # 1: find_redefinition(list: const mlist_t &, i1: minsn_t *, i2: const minsn_t *, maymust: maymust_t=MAY_ACCESS) -> minsn_t *



   .. py:method:: is_rhs_redefined(ins: minsn_t, i1: minsn_t, i2: minsn_t) -> bool

      Is the right hand side of the instruction redefined the insn range? "right hand side" corresponds to the source operands of the instruction. 
              
      :param ins: instruction to consider
      :param i1: starting instruction of the range (must be a top level insn)
      :param i2: end instruction of the range (must be a top level insn) i2 is excluded from the range. it can be specified as nullptr. i1 and i2 must belong to the same block.



   .. py:method:: find_access(op: mop_t, parent: minsn_t **, mend: minsn_t, fdflags: int) -> minsn_t *

      Find the instruction that accesses the specified operand. This function search inside one block. 
              
      :param op: operand to search for
      :param parent: ptr to ptr to a top level instruction. in: denotes the beginning of the search range. out: denotes the parent of the found instruction.
      :param mend: end instruction of the range (must be a top level insn) mend is excluded from the range. it can be specified as nullptr. parent and mend must belong to the same block.
      :param fdflags: combination of bits for mblock_t::find_access bits
      :returns: the instruction that accesses the operand. this instruction may be a sub-instruction. to find out the top level instruction, check out *parent. nullptr means 'not found'.



   .. py:method:: find_def(op: mop_t, p_i1: minsn_t **, i2: minsn_t, fdflags: int) -> minsn_t *


   .. py:method:: find_use(op: mop_t, p_i1: minsn_t **, i2: minsn_t, fdflags: int) -> minsn_t *


   .. py:method:: get_valranges(*args) -> bool

      This function has the following signatures:

          0. get_valranges(res: valrng_t *, vivl: const vivl_t &, vrflags: int) -> bool
          1. get_valranges(res: valrng_t *, vivl: const vivl_t &, m: const minsn_t *, vrflags: int) -> bool

      # 0: get_valranges(res: valrng_t *, vivl: const vivl_t &, vrflags: int) -> bool

      Find possible values for a block. 
              

      # 1: get_valranges(res: valrng_t *, vivl: const vivl_t &, m: const minsn_t *, vrflags: int) -> bool

      Find possible values for an instruction. 
              



   .. py:method:: make_nop(m: minsn_t) -> None

      Erase the instruction (convert it to nop) and mark the lists dirty. This is the recommended function to use because it also marks the block use-def lists dirty. 
              



   .. py:method:: get_reginsn_qty() -> size_t

      Calculate number of regular instructions in the block. Assertions are skipped by this function. 
              
      :returns: Number of non-assertion instructions in the block.



   .. py:method:: is_call_block() -> bool


   .. py:method:: is_unknown_call() -> bool


   .. py:method:: is_nway() -> bool


   .. py:method:: is_branch() -> bool


   .. py:method:: is_simple_goto_block() -> bool


   .. py:method:: is_simple_jcnd_block() -> bool


   .. py:method:: preds()

      Iterates the list of predecessor blocks



   .. py:method:: succs()

      Iterates the list of successor blocks



.. py:data:: MBL_PRIV

   private block - no instructions except the specified are accepted (used in patterns) 
           


.. py:data:: MBL_NONFAKE

   regular block


.. py:data:: MBL_FAKE

   fake block


.. py:data:: MBL_GOTO

   this block is a goto target


.. py:data:: MBL_TCAL

   aritifical call block for tail calls


.. py:data:: MBL_PUSH

   needs "convert push/pop instructions"


.. py:data:: MBL_DMT64

   needs "demote 64bits"


.. py:data:: MBL_COMB

   needs "combine" pass


.. py:data:: MBL_PROP

   needs 'propagation' pass


.. py:data:: MBL_DEAD

   needs "eliminate deads" pass


.. py:data:: MBL_LIST

   use/def lists are ready (not dirty)


.. py:data:: MBL_INCONST

   inconsistent lists: we are building them


.. py:data:: MBL_CALL

   call information has been built


.. py:data:: MBL_BACKPROP

   performed backprop_cc


.. py:data:: MBL_NORET

   dead end block: doesn't return execution control


.. py:data:: MBL_DSLOT

   block for delay slot


.. py:data:: MBL_VALRANGES

   should optimize using value ranges


.. py:data:: MBL_KEEP

   do not remove even if unreachable


.. py:data:: MBL_INLINED

   block was inlined, not originally part of mbr


.. py:data:: MBL_EXTFRAME

   an inlined block with an external frame


.. py:data:: FD_BACKWARD

   search direction


.. py:data:: FD_FORWARD

   search direction


.. py:data:: FD_USE

   look for use


.. py:data:: FD_DEF

   look for definition


.. py:data:: FD_DIRTY

   ignore possible implicit definitions by function calls and indirect memory access 
           


.. py:data:: VR_AT_START

   get value ranges before the instruction or at the block start (if M is nullptr) 
           


.. py:data:: VR_AT_END

   get value ranges after the instruction or at the block end, just after the last instruction (if M is nullptr) 
           


.. py:data:: VR_EXACT

   find exact match. if not set, the returned valrng size will be >= vivl.size 
           


.. py:data:: WARN_VARARG_REGS

   0 cannot handle register arguments in vararg function, discarded them


.. py:data:: WARN_ILL_PURGED

   1 odd caller purged bytes d, correcting


.. py:data:: WARN_ILL_FUNCTYPE

   2 invalid function type 's' has been ignored


.. py:data:: WARN_VARARG_TCAL

   3 cannot handle tail call to vararg


.. py:data:: WARN_VARARG_NOSTK

   4 call vararg without local stack


.. py:data:: WARN_VARARG_MANY

   5 too many varargs, some ignored


.. py:data:: WARN_ADDR_OUTARGS

   6 cannot handle address arithmetics in outgoing argument area of stack frame - unused


.. py:data:: WARN_DEP_UNK_CALLS

   7 found interdependent unknown calls


.. py:data:: WARN_ILL_ELLIPSIS

   8 erroneously detected ellipsis type has been ignored


.. py:data:: WARN_GUESSED_TYPE

   9 using guessed type s;


.. py:data:: WARN_EXP_LINVAR

   10 failed to expand a linear variable


.. py:data:: WARN_WIDEN_CHAINS

   11 failed to widen chains


.. py:data:: WARN_BAD_PURGED

   12 inconsistent function type and number of purged bytes


.. py:data:: WARN_CBUILD_LOOPS

   13 too many cbuild loops


.. py:data:: WARN_NO_SAVE_REST

   14 could not find valid save-restore pair for s


.. py:data:: WARN_ODD_INPUT_REG

   15 odd input register s


.. py:data:: WARN_ODD_ADDR_USE

   16 odd use of a variable address


.. py:data:: WARN_MUST_RET_FP

   17 function return type is incorrect (must be floating point)


.. py:data:: WARN_ILL_FPU_STACK

   18 inconsistent fpu stack


.. py:data:: WARN_SELFREF_PROP

   19 self-referencing variable has been detected


.. py:data:: WARN_WOULD_OVERLAP

   20 variables would overlap: s


.. py:data:: WARN_ARRAY_INARG

   21 array has been used for an input argument


.. py:data:: WARN_MAX_ARGS

   22 too many input arguments, some ignored


.. py:data:: WARN_BAD_FIELD_TYPE

   23 incorrect structure member type for s::s, ignored


.. py:data:: WARN_WRITE_CONST

   24 write access to const memory at a has been detected


.. py:data:: WARN_BAD_RETVAR

   25 wrong return variable


.. py:data:: WARN_FRAG_LVAR

   26 fragmented variable at s may be wrong


.. py:data:: WARN_HUGE_STKOFF

   27 exceedingly huge offset into the stack frame


.. py:data:: WARN_UNINITED_REG

   28 reference to an uninitialized register has been removed: s


.. py:data:: WARN_FIXED_INSN

   29 fixed broken insn


.. py:data:: WARN_WRONG_VA_OFF

   30 wrong offset of va_list variable


.. py:data:: WARN_CR_NOFIELD

   31 CONTAINING_RECORD: no field 's' in struct 's' at d


.. py:data:: WARN_CR_BADOFF

   32 CONTAINING_RECORD: too small offset d for struct 's'


.. py:data:: WARN_BAD_STROFF

   33 user specified stroff has not been processed: s


.. py:data:: WARN_BAD_VARSIZE

   34 inconsistent variable size for 's'


.. py:data:: WARN_UNSUPP_REG

   35 unsupported processor register 's'


.. py:data:: WARN_UNALIGNED_ARG

   36 unaligned function argument 's'


.. py:data:: WARN_BAD_STD_TYPE

   37 corrupted or unexisting local type 's'


.. py:data:: WARN_BAD_CALL_SP

   38 bad sp value at call


.. py:data:: WARN_MISSED_SWITCH

   39 wrong markup of switch jump, skipped it


.. py:data:: WARN_BAD_SP

   40 positive sp value a has been found


.. py:data:: WARN_BAD_STKPNT

   41 wrong sp change point


.. py:data:: WARN_UNDEF_LVAR

   42 variable 's' is possibly undefined


.. py:data:: WARN_JUMPOUT

   43 control flows out of bounds


.. py:data:: WARN_BAD_VALRNG

   44 values range analysis failed


.. py:data:: WARN_BAD_SHADOW

   45 ignored the value written to the shadow area of the succeeding call


.. py:data:: WARN_OPT_VALRNG

   46 conditional instruction was optimized away because s


.. py:data:: WARN_RET_LOCREF

   47 returning address of temporary local variable 's'


.. py:data:: WARN_BAD_MAPDST

   48 too short map destination 's' for variable 's'


.. py:data:: WARN_BAD_INSN

   49 bad instruction


.. py:data:: WARN_ODD_ABI

   50 encountered odd instruction for the current ABI


.. py:data:: WARN_UNBALANCED_STACK

   51 unbalanced stack, ignored a potential tail call


.. py:data:: WARN_OPT_VALRNG2

   52 mask 0xX is shortened because s <= 0xX"


.. py:data:: WARN_OPT_VALRNG3

   53 masking with 0XX was optimized away because s <= 0xX


.. py:data:: WARN_OPT_USELESS_JCND

   54 simplified comparisons for 's': s became s


.. py:data:: WARN_SUBFRAME_OVERFLOW

   55 call arguments overflow the function chunk frame


.. py:data:: WARN_OPT_VALRNG4

   56 the cases s were optimized away because s


.. py:data:: WARN_MAX

   may be used in notes as a placeholder when the warning id is not available 
             


.. py:class:: hexwarn_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      Address where the warning occurred.



   .. py:attribute:: id
      :type:  warnid_t

      Warning id.



   .. py:attribute:: text
      :type:  str

      Fully formatted text of the warning.



   .. py:method:: compare(r: hexwarn_t) -> int


.. py:data:: MMAT_ZERO

   microcode does not exist


.. py:data:: MMAT_GENERATED

   generated microcode


.. py:data:: MMAT_PREOPTIMIZED

   preoptimized pass is complete


.. py:data:: MMAT_LOCOPT

   local optimization of each basic block is complete. control flow graph is ready too. 
             


.. py:data:: MMAT_CALLS

   detected call arguments. see also hxe_calls_done


.. py:data:: MMAT_GLBOPT1

   performed the first pass of global optimization


.. py:data:: MMAT_GLBOPT2

   most global optimization passes are done


.. py:data:: MMAT_GLBOPT3

   completed all global optimization. microcode is fixed now.


.. py:data:: MMAT_LVARS

   allocated local variables


.. py:data:: MMIDX_GLBLOW

   global memory: low part


.. py:data:: MMIDX_LVARS

   stack: local variables


.. py:data:: MMIDX_RETADDR

   stack: return address


.. py:data:: MMIDX_SHADOW

   stack: shadow arguments


.. py:data:: MMIDX_ARGS

   stack: regular stack arguments


.. py:data:: MMIDX_GLBHIGH

   global memory: high part


.. py:class:: mba_ranges_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: pfn
      :type:  func_t *

      function to decompile. if not null, then function mode.



   .. py:attribute:: ranges
      :type:  rangevec_t

      snippet mode: ranges to decompile. function mode: list of outlined ranges 
              



   .. py:method:: start() -> ida_idaapi.ea_t


   .. py:method:: empty() -> bool


   .. py:method:: clear() -> None


   .. py:method:: is_snippet() -> bool


   .. py:method:: is_fragmented() -> bool


.. py:class:: mba_range_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: rii
      :type:  range_chunk_iterator_t


   .. py:attribute:: fii
      :type:  func_tail_iterator_t


   .. py:method:: is_snippet() -> bool


   .. py:method:: set(mbr: mba_ranges_t) -> bool


   .. py:method:: next() -> bool


   .. py:method:: chunk() -> range_t const &


.. py:class:: mba_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: precise_defeas() -> bool


   .. py:method:: optimized() -> bool


   .. py:method:: short_display() -> bool


   .. py:method:: show_reduction() -> bool


   .. py:method:: graph_insns() -> bool


   .. py:method:: loaded_gdl() -> bool


   .. py:method:: should_beautify() -> bool


   .. py:method:: rtype_refined() -> bool


   .. py:method:: may_refine_rettype() -> bool


   .. py:method:: use_wingraph32() -> bool


   .. py:method:: display_numaddrs() -> bool


   .. py:method:: display_valnums() -> bool


   .. py:method:: is_pattern() -> bool


   .. py:method:: is_thunk() -> bool


   .. py:method:: saverest_done() -> bool


   .. py:method:: callinfo_built() -> bool


   .. py:method:: really_alloc() -> bool


   .. py:method:: lvars_allocated() -> bool


   .. py:method:: chain_varnums_ok() -> bool


   .. py:method:: returns_fpval() -> bool


   .. py:method:: has_passregs() -> bool


   .. py:method:: generated_asserts() -> bool


   .. py:method:: propagated_asserts() -> bool


   .. py:method:: deleted_pairs() -> bool


   .. py:method:: common_stkvars_stkargs() -> bool


   .. py:method:: lvar_names_ok() -> bool


   .. py:method:: lvars_renamed() -> bool


   .. py:method:: has_over_chains() -> bool


   .. py:method:: valranges_done() -> bool


   .. py:method:: argidx_ok() -> bool


   .. py:method:: argidx_sorted() -> bool


   .. py:method:: code16_bit_removed() -> bool


   .. py:method:: has_stack_retval() -> bool


   .. py:method:: has_outlines() -> bool


   .. py:method:: is_ctr() -> bool


   .. py:method:: is_dtr() -> bool


   .. py:method:: is_cdtr() -> bool


   .. py:method:: prop_complex() -> bool


   .. py:method:: get_mba_flags() -> int


   .. py:method:: get_mba_flags2() -> int


   .. py:method:: set_mba_flags(f: int) -> None


   .. py:method:: clr_mba_flags(f: int) -> None


   .. py:method:: set_mba_flags2(f: int) -> None


   .. py:method:: clr_mba_flags2(f: int) -> None


   .. py:method:: clr_cdtr() -> None


   .. py:method:: calc_shins_flags() -> int


   .. py:method:: stkoff_vd2ida(off: int) -> int


   .. py:method:: stkoff_ida2vd(off: int) -> int


   .. py:method:: argbase() -> int


   .. py:method:: idaloc2vd(loc: argloc_t, width: int) -> vdloc_t


   .. py:method:: vd2idaloc(*args) -> argloc_t

      This function has the following signatures:

          0. vd2idaloc(loc: const vdloc_t &, width: int) -> argloc_t
          1. vd2idaloc(loc: const vdloc_t &, width: int, spd: int) -> argloc_t

      # 0: vd2idaloc(loc: const vdloc_t &, width: int) -> argloc_t


      # 1: vd2idaloc(loc: const vdloc_t &, width: int, spd: int) -> argloc_t



   .. py:method:: is_stkarg(v: lvar_t) -> bool


   .. py:method:: get_ida_argloc(v: lvar_t) -> argloc_t


   .. py:attribute:: mbr
      :type:  mba_ranges_t


   .. py:attribute:: entry_ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: last_prolog_ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: first_epilog_ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: qty
      :type:  int

      number of basic blocks



   .. py:attribute:: npurged
      :type:  int

      -1 - unknown



   .. py:attribute:: cc
      :type:  callcnv_t

      calling convention



   .. py:attribute:: tmpstk_size
      :type:  int

      size of the temporary stack part (which dynamically changes with push/pops) 
              



   .. py:attribute:: frsize
      :type:  int

      size of local stkvars range in the stack frame



   .. py:attribute:: frregs
      :type:  int

      size of saved registers range in the stack frame



   .. py:attribute:: fpd
      :type:  int

      frame pointer delta



   .. py:attribute:: pfn_flags
      :type:  int

      copy of func_t::flags



   .. py:attribute:: retsize
      :type:  int

      size of return address in the stack frame



   .. py:attribute:: shadow_args
      :type:  int

      size of shadow argument area



   .. py:attribute:: fullsize
      :type:  int

      Full stack size including incoming args.



   .. py:attribute:: stacksize
      :type:  int

      The maximal size of the function stack including bytes allocated for outgoing call arguments (up to retaddr) 
              



   .. py:attribute:: inargoff
      :type:  int

      offset of the first stack argument; after fix_scattered_movs() INARGOFF may be less than STACKSIZE 
              



   .. py:attribute:: minstkref
      :type:  int

      The lowest stack location whose address was taken.



   .. py:attribute:: minstkref_ea
      :type:  ida_idaapi.ea_t

      address with lowest minstkref (for debugging)



   .. py:attribute:: minargref
      :type:  int

      The lowest stack argument location whose address was taken This location and locations above it can be aliased It controls locations >= inargoff-shadow_args 
              



   .. py:attribute:: spd_adjust
      :type:  int

      If sp>0, the max positive sp value.



   .. py:attribute:: gotoff_stkvars
      :type:  ivlset_t

      stkvars that hold .got offsets. considered to be unaliasable



   .. py:attribute:: restricted_memory
      :type:  ivlset_t


   .. py:attribute:: aliased_memory
      :type:  ivlset_t

      aliased_memory+restricted_memory=ALLMEM



   .. py:attribute:: nodel_memory
      :type:  mlist_t

      global dead elimination may not delete references to this area



   .. py:attribute:: consumed_argregs
      :type:  rlist_t

      registers converted into stack arguments, should not be used as arguments



   .. py:attribute:: maturity
      :type:  mba_maturity_t

      current maturity level



   .. py:attribute:: reqmat
      :type:  mba_maturity_t

      required maturity level



   .. py:attribute:: final_type
      :type:  bool

      is the function type final? (specified by the user)



   .. py:attribute:: idb_type
      :type:  tinfo_t

      function type as retrieved from the database



   .. py:attribute:: idb_spoiled
      :type:  reginfovec_t

      MBA_SPLINFO && final_type: info in ida format.



   .. py:attribute:: spoiled_list
      :type:  mlist_t

      MBA_SPLINFO && !final_type: info in vd format.



   .. py:attribute:: fti_flags
      :type:  int

      FTI_... constants for the current function.



   .. py:attribute:: label
      :type:  str

      name of the function or pattern (colored)



   .. py:attribute:: vars
      :type:  lvars_t

      local variables



   .. py:attribute:: argidx
      :type:  intvec_t

      input arguments (indexes into 'vars')



   .. py:attribute:: retvaridx
      :type:  int

      index of variable holding the return value -1 means none 
              



   .. py:attribute:: error_ea
      :type:  ida_idaapi.ea_t

      during microcode generation holds ins.ea



   .. py:attribute:: error_strarg
      :type:  str


   .. py:attribute:: blocks
      :type:  mblock_t *

      double linked list of blocks



   .. py:attribute:: natural
      :type:  mblock_t **

      natural order of blocks



   .. py:attribute:: std_ivls
      :type:  ivl_with_name_t [6]

      we treat memory as consisting of 6 parts see memreg_index_t 
              



   .. py:attribute:: notes
      :type:  hexwarns_t


   .. py:attribute:: occurred_warns
      :type:  uchar [32]


   .. py:method:: write_to_const_detected() -> bool


   .. py:method:: bad_call_sp_detected() -> bool


   .. py:method:: regargs_is_not_aligned() -> bool


   .. py:method:: has_bad_sp() -> bool


   .. py:method:: term() -> None


   .. py:method:: get_curfunc() -> func_t *


   .. py:method:: use_frame() -> bool


   .. py:method:: is_snippet() -> bool


   .. py:method:: set_maturity(mat: mba_maturity_t) -> merror_t

      Set maturity level. 
              
      :param mat: new maturity level
      :returns: error code Plugins may use this function to skip some parts of the analysis. The maturity level cannot be decreased.



   .. py:method:: optimize_local(locopt_bits: int) -> int

      Optimize each basic block locally 
              
      :param locopt_bits: combination of Bits for optimize_local() bits
      :returns: number of changes. 0 means nothing changed This function is called by the decompiler, usually there is no need to call it explicitly.



   .. py:method:: build_graph() -> merror_t

      Build control flow graph. This function may be called only once. It calculates the type of each basic block and the adjacency list. optimize_local() calls this function if necessary. You need to call this function only before MMAT_LOCOPT. 
              
      :returns: error code



   .. py:method:: get_graph() -> mbl_graph_t *

      Get control graph. Call build_graph() if you need the graph before MMAT_LOCOPT. 
              



   .. py:method:: analyze_calls(acflags: int) -> int

      Analyze calls and determine calling conventions. 
              
      :param acflags: permitted actions that are necessary for successful detection of calling conventions. See Bits for analyze_calls()
      :returns: number of calls. -1 means error.



   .. py:method:: optimize_global() -> merror_t

      Optimize microcode globally. This function applies various optimization methods until we reach the fixed point. After that it preallocates lvars unless reqmat forbids it. 
              
      :returns: error code



   .. py:method:: alloc_lvars() -> None

      Allocate local variables. Must be called only immediately after optimize_global(), with no modifications to the microcode. Converts registers, stack variables, and similar operands into mop_l. This call will not fail because all necessary checks were performed in optimize_global(). After this call the microcode reaches its final state. 
              



   .. py:method:: dump() -> None

      Dump microcode to a file. The file will be created in the directory pointed by IDA_DUMPDIR envvar. Dump will be created only if IDA is run under debugger. 
              



   .. py:method:: dump_mba(_verify: bool, title: str) -> None


   .. py:method:: verify(always: bool) -> None

      Verify microcode consistency. 
              
      :param always: if false, the check will be performed only if ida runs under debugger If any inconsistency is discovered, an internal error will be generated. We strongly recommend you to call this function before returing control to the decompiler from your callbacks, in the case if you modified the microcode. If the microcode is inconsistent, this function will generate an internal error. We provide the source code of this function in the plugins/hexrays_sdk/verifier directory for your reference.



   .. py:method:: mark_chains_dirty() -> None

      Mark the microcode use-def chains dirty. Call this function is any inter-block data dependencies got changed because of your modifications to the microcode. Failing to do so may cause an internal error. 
              



   .. py:method:: get_mblock(n: uint) -> mblock_t *

      Get basic block by its serial number.



   .. py:method:: insert_block(bblk: int) -> mblock_t *

      Insert a block in the middle of the mbl array. The very first block of microcode must be empty, it is the entry block. The very last block of microcode must be BLT_STOP, it is the exit block. Therefore inserting a new block before the entry point or after the exit block is not a good idea. 
              
      :param bblk: the new block will be inserted before BBLK
      :returns: ptr to the new block



   .. py:method:: split_block(blk: mblock_t, start_insn: minsn_t) -> mblock_t *

      Split a block: insert a new one after the block, move some instructions to new block 
              
      :param blk: block to be split
      :param start_insn: all instructions to be moved to new block: starting with this one up to the end
      :returns: ptr to the new block



   .. py:method:: remove_block(blk: mblock_t) -> bool

      Delete a block. 
              
      :param blk: block to delete
      :returns: true if at least one of the other blocks became empty or unreachable



   .. py:method:: remove_blocks(start_blk: int, end_blk: int) -> bool


   .. py:method:: copy_block(blk: mblock_t, new_serial: int, cpblk_flags: int = 3) -> mblock_t *

      Make a copy of a block. This function makes a simple copy of the block. It does not fix the predecessor and successor lists, they must be fixed if necessary. 
              
      :param blk: block to copy
      :param new_serial: position of the copied block
      :param cpblk_flags: combination of Batch decompilation bits... bits
      :returns: pointer to the new copy



   .. py:method:: remove_empty_and_unreachable_blocks() -> bool

      Delete all empty and unreachable blocks. Blocks marked with MBL_KEEP won't be deleted. 
              



   .. py:method:: merge_blocks() -> bool

      Merge blocks. This function merges blocks constituting linear flow. It calls remove_empty_and_unreachable_blocks() as well. 
              
      :returns: true if changed any blocks



   .. py:method:: for_all_ops(mv: mop_visitor_t) -> int

      Visit all operands of all instructions. 
              
      :param mv: operand visitor
      :returns: non-zero value returned by mv.visit_mop() or zero



   .. py:method:: for_all_insns(mv: minsn_visitor_t) -> int

      Visit all instructions. This function visits all instruction and subinstructions. 
              
      :param mv: instruction visitor
      :returns: non-zero value returned by mv.visit_mop() or zero



   .. py:method:: for_all_topinsns(mv: minsn_visitor_t) -> int

      Visit all top level instructions. 
              
      :param mv: instruction visitor
      :returns: non-zero value returned by mv.visit_mop() or zero



   .. py:method:: find_mop(ctx: op_parent_info_t, ea: ida_idaapi.ea_t, is_dest: bool, list: mlist_t) -> mop_t *

      Find an operand in the microcode. This function tries to find the operand that matches LIST. Any operand that overlaps with LIST is considered as a match. 
              
      :param ctx: context information for the result
      :param ea: desired address of the operand. BADADDR means to accept any address.
      :param is_dest: search for destination operand? this argument may be ignored if the exact match could not be found
      :param list: list of locations the correspond to the operand
      :returns: pointer to the operand or nullptr.



   .. py:method:: create_helper_call(ea: ida_idaapi.ea_t, helper: str, rettype: tinfo_t = None, callargs: mcallargs_t = None, out: mop_t = None) -> minsn_t *

      Create a call of a helper function. 
              
      :param ea: The desired address of the instruction
      :param helper: The helper name
      :param rettype: The return type (nullptr or empty type means 'void')
      :param callargs: The helper arguments (nullptr-no arguments)
      :param out: The operand where the call result should be stored. If this argument is not nullptr, "mov helper_call(), out" will be generated. Otherwise "call helper()" will be generated. Note: the size of this operand must be equal to the RETTYPE size
      :returns: pointer to the created instruction or nullptr if error



   .. py:method:: get_func_output_lists(*args) -> None

      Prepare the lists of registers & memory that are defined/killed by a function 
              
      :param return_regs: defined regs to return (eax,edx)
      :param spoiled: spoiled regs (flags,ecx,mem)
      :param type: the function type
      :param call_ea: the call insn address (if known)
      :param tail_call: is it the tail call?



   .. py:method:: arg(n: int) -> lvar_t &

      Get input argument of the decompiled function. 
              
      :param n: argument number (0..nargs-1)



   .. py:method:: alloc_fict_ea(real_ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

      Allocate a fictional address. This function can be used to allocate a new unique address for a new instruction, if re-using any existing address leads to conflicts. For example, if the last instruction of the function modifies R0 and falls through to the next function, it will be a tail call: LDM R0!, {R4,R7} end of the function start of another function In this case R0 generates two different lvars at the same address:
      * one modified by LDM
      * another that represents the return value from the tail call


      Another example: a third-party plugin makes a copy of an instruction. This may lead to the generation of two variables at the same address. Example 3: fictional addresses can be used for new instructions created while modifying the microcode. This function can be used to allocate a new unique address for a new instruction or a variable. The fictional address is selected from an unallocated address range. 
              
      :param real_ea: real instruction address (BADADDR is ok too)
      :returns: a unique fictional address



   .. py:method:: map_fict_ea(fict_ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

      Resolve a fictional address. This function provides a reverse of the mapping made by alloc_fict_ea(). 
              
      :param fict_ea: fictional definition address
      :returns: the real instruction address



   .. py:method:: get_std_region(idx: memreg_index_t) -> ivl_t const &

      Get information about various memory regions. We map the stack frame to the global memory, to some unused range. 
              



   .. py:method:: get_lvars_region() -> ivl_t const &


   .. py:method:: get_shadow_region() -> ivl_t const &


   .. py:method:: get_args_region() -> ivl_t const &


   .. py:method:: get_stack_region() -> ivl_t


   .. py:method:: serialize() -> None

      Serialize mbl array into a sequence of bytes.



   .. py:method:: deserialize(bytes: uchar const *) -> mba_t *
      :staticmethod:


      Deserialize a byte sequence into mbl array. 
              
      :param bytes: pointer to the beginning of the byte sequence.
      :returns: new mbl array



   .. py:method:: save_snapshot(description: str) -> None

      Create and save microcode snapshot.



   .. py:method:: alloc_kreg(size: size_t, check_size: bool = True) -> mreg_t

      Allocate a kernel register. 
              
      :param size: size of the register in bytes
      :param check_size: if true, only the sizes that correspond to a size of a basic type will be accepted.
      :returns: allocated register. mr_none means failure.



   .. py:method:: free_kreg(reg: mreg_t, size: size_t) -> None

      Free a kernel register. If wrong arguments are passed, this function will generate an internal error. 
              
      :param reg: a previously allocated kernel register
      :param size: size of the register in bytes



   .. py:method:: inline_func(cdg: codegen_t, blknum: int, ranges: mba_ranges_t, decomp_flags: int = 0, inline_flags: int = 0) -> merror_t

      Inline a range. This function may be called only during the initial microcode generation phase. 
              
      :param cdg: the codegenerator object
      :param blknum: the block contaning the call/jump instruction to inline
      :param ranges: the set of ranges to inline. in the case of multiple calls to inline_func(), ranges will be compared using their start addresses. if two ranges have the same address, they will be considered the same.
      :param decomp_flags: combination of decompile() flags bits
      :param inline_flags: combination of inline_func() flags bits
      :returns: error code



   .. py:method:: locate_stkpnt(ea: ida_idaapi.ea_t) -> stkpnt_t const *


   .. py:method:: set_lvar_name(v: lvar_t, name: str, flagbits: int) -> bool


   .. py:method:: set_nice_lvar_name(v: lvar_t, name: str) -> bool


   .. py:method:: set_user_lvar_name(v: lvar_t, name: str) -> bool


   .. py:attribute:: idb_node


.. py:data:: MBA_PRCDEFS

   use precise defeas for chain-allocated lvars


.. py:data:: MBA_NOFUNC

   function is not present, addresses might be wrong


.. py:data:: MBA_PATTERN

   microcode pattern, callinfo is present


.. py:data:: MBA_LOADED

   loaded gdl, no instructions (debugging)


.. py:data:: MBA_RETFP

   function returns floating point value


.. py:data:: MBA_SPLINFO

   (final_type ? idb_spoiled : spoiled_regs) is valid


.. py:data:: MBA_PASSREGS

   has mcallinfo_t::pass_regs


.. py:data:: MBA_THUNK

   thunk function


.. py:data:: MBA_CMNSTK

   stkvars+stkargs should be considered as one area


.. py:data:: MBA_PREOPT

   preoptimization stage complete


.. py:data:: MBA_CMBBLK

   request to combine blocks


.. py:data:: MBA_ASRTOK

   assertions have been generated


.. py:data:: MBA_CALLS

   callinfo has been built


.. py:data:: MBA_ASRPROP

   assertion have been propagated


.. py:data:: MBA_SAVRST

   save-restore analysis has been performed


.. py:data:: MBA_RETREF

   return type has been refined


.. py:data:: MBA_GLBOPT

   microcode has been optimized globally


.. py:data:: MBA_LVARS0

   lvar pre-allocation has been performed


.. py:data:: MBA_LVARS1

   lvar real allocation has been performed


.. py:data:: MBA_DELPAIRS

   pairs have been deleted once


.. py:data:: MBA_CHVARS

   can verify chain varnums


.. py:data:: MBA_SHORT

   use short display


.. py:data:: MBA_COLGDL

   display graph after each reduction


.. py:data:: MBA_INSGDL

   display instruction in graphs


.. py:data:: MBA_NICE

   apply transformations to c code


.. py:data:: MBA_REFINE

   may refine return value size


.. py:data:: MBA_WINGR32

   use wingraph32


.. py:data:: MBA_NUMADDR

   display definition addresses for numbers


.. py:data:: MBA_VALNUM

   display value numbers


.. py:data:: MBA_INITIAL_FLAGS

.. py:data:: MBA2_LVARNAMES_OK

   may verify lvar_names?


.. py:data:: MBA2_LVARS_RENAMED

   accept empty names now?


.. py:data:: MBA2_OVER_CHAINS

   has overlapped chains?


.. py:data:: MBA2_VALRNG_DONE

   calculated valranges?


.. py:data:: MBA2_IS_CTR

   is constructor?


.. py:data:: MBA2_IS_DTR

   is destructor?


.. py:data:: MBA2_ARGIDX_OK

   may verify input argument list?


.. py:data:: MBA2_NO_DUP_CALLS

   forbid multiple calls with the same ea


.. py:data:: MBA2_NO_DUP_LVARS

   forbid multiple lvars with the same ea


.. py:data:: MBA2_UNDEF_RETVAR

   return value is undefined


.. py:data:: MBA2_ARGIDX_SORTED

   args finally sorted according to ABI (e.g. reverse stkarg order in Borland) 
           


.. py:data:: MBA2_CODE16_BIT

   the code16 bit got removed


.. py:data:: MBA2_STACK_RETVAL

   the return value (or its part) is on the stack


.. py:data:: MBA2_HAS_OUTLINES

   calls to outlined code have been inlined


.. py:data:: MBA2_NO_FRAME

   do not use function frame info (only snippet mode)


.. py:data:: MBA2_PROP_COMPLEX

   allow propagation of more complex variable definitions


.. py:data:: MBA2_DONT_VERIFY

   Do not verify microcode. This flag is recomended to be set only when debugging decompiler plugins 
           


.. py:data:: MBA2_INITIAL_FLAGS

.. py:data:: MBA2_ALL_FLAGS

.. py:data:: NALT_VD

   this index is not used by ida


.. py:data:: LOCOPT_ALL

   redo optimization for all blocks. if this bit is not set, only dirty blocks will be optimized 
           


.. py:data:: LOCOPT_REFINE

   refine return type, ok to fail


.. py:data:: LOCOPT_REFINE2

   refine return type, try harder


.. py:data:: ACFL_LOCOPT

   perform local propagation (requires ACFL_BLKOPT)


.. py:data:: ACFL_BLKOPT

   perform interblock transformations


.. py:data:: ACFL_GLBPROP

   perform global propagation


.. py:data:: ACFL_GLBDEL

   perform dead code eliminition


.. py:data:: ACFL_GUESS

   may guess calling conventions


.. py:data:: CPBLK_FAST

   do not update minbstkref and minbargref


.. py:data:: CPBLK_MINREF

   update minbstkref and minbargref


.. py:data:: CPBLK_OPTJMP

   del the jump insn at the end of the block if it becomes useless 
           


.. py:data:: INLINE_EXTFRAME

   Inlined function has its own (external) frame.


.. py:data:: INLINE_DONTCOPY

   Do not reuse old inlined copy even if it exists.


.. py:class:: chain_keeper_t(_gc: graph_chains_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: front() -> block_chains_t &


   .. py:method:: back() -> block_chains_t &


   .. py:method:: for_all_chains(cv: chain_visitor_t, gca: int) -> int


.. py:data:: GC_REGS_AND_STKVARS

   registers and stkvars (restricted memory only)


.. py:data:: GC_ASR

   all the above and assertions


.. py:data:: GC_XDSU

   only registers calculated with FULL_XDSU


.. py:data:: GC_END

   number of chain types


.. py:data:: GC_DIRTY_ALL

   bitmask to represent all chains


.. py:class:: mbl_graph_t(*args, **kwargs)

   Bases: :py:obj:`simple_graph_t`


   .. py:attribute:: thisown


   .. py:method:: is_ud_chain_dirty(gctype: gctype_t) -> bool

      Is the use-def chain of the specified kind dirty?



   .. py:method:: is_du_chain_dirty(gctype: gctype_t) -> bool

      Is the def-use chain of the specified kind dirty?



   .. py:method:: get_chain_stamp() -> int


   .. py:method:: get_ud(gctype: gctype_t) -> graph_chains_t *

      Get use-def chains.



   .. py:method:: get_du(gctype: gctype_t) -> graph_chains_t *

      Get def-use chains.



   .. py:method:: is_redefined_globally(*args) -> bool

      Is LIST redefined in the graph?



   .. py:method:: is_used_globally(*args) -> bool

      Is LIST used in the graph?



   .. py:method:: get_mblock(n: int) -> mblock_t *


.. py:class:: cdg_insn_iterator_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: mba
      :type:  mba_t const *


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: end
      :type:  ida_idaapi.ea_t


   .. py:attribute:: dslot
      :type:  ida_idaapi.ea_t


   .. py:attribute:: dslot_insn
      :type:  insn_t


   .. py:attribute:: severed_branch
      :type:  ida_idaapi.ea_t


   .. py:attribute:: is_likely_dslot
      :type:  bool


   .. py:method:: ok() -> bool


   .. py:method:: has_dslot() -> bool


   .. py:method:: dslot_with_xrefs() -> bool


   .. py:method:: is_severed_dslot() -> bool


   .. py:method:: start(rng: range_t) -> None


   .. py:method:: next(ins: insn_t *) -> merror_t


.. py:class:: codegen_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: mba
      :type:  mba_t *


   .. py:attribute:: mb
      :type:  mblock_t *


   .. py:attribute:: insn
      :type:  insn_t


   .. py:attribute:: ignore_micro
      :type:  char


   .. py:attribute:: ii
      :type:  cdg_insn_iterator_t


   .. py:method:: clear() -> None


   .. py:method:: analyze_prolog(fc: qflow_chart_t, reachable: bitset_t) -> merror_t

      Analyze prolog/epilog of the function to decompile. If prolog is found, allocate and fill 'mba->pi' structure. 
              
      :param fc: flow chart
      :param reachable: bitmap of reachable blocks
      :returns: error code



   .. py:method:: gen_micro() -> merror_t

      Generate microcode for one instruction. The instruction is in INSN 
              
      :returns: MERR_OK - all ok MERR_BLOCK - all ok, need to switch to new block MERR_BADBLK - delete current block and continue other error codes are fatal



   .. py:method:: load_operand(opnum: int, flags: int = 0) -> mreg_t

      Generate microcode to load one operand. 
              
      :param opnum: number of INSN operand
      :param flags: reserved for future use
      :returns: register containing the operand.



   .. py:method:: microgen_completed() -> None

      This method is called when the microcode generation is done.



   .. py:method:: prepare_gen_micro() -> merror_t

      Setup internal data to handle new instruction. This method should be called before calling gen_micro(). Usually gen_micro() is called by the decompiler. You have to call this function explicitly only if you yourself call gen_micro(). The instruction is in INSN 
              
      :returns: MERR_OK - all ok other error codes are fatal



   .. py:method:: load_effective_address(n: int, flags: int = 0) -> mreg_t

      Generate microcode to calculate the address of a memory operand. 
              
      :param n: - number of INSN operand
      :param flags: - reserved for future use
      :returns: register containing the operand address. mr_none - failed (not a memory operand)



   .. py:method:: store_operand(n: int, mop: mop_t, flags: int = 0, outins: minsn_t ** = None) -> bool

      Generate microcode to store an operand. In case of success an arbitrary number of instructions can be generated (and even no instruction if the source and target are the same) 
              
      :param n: - number of target INSN operand
      :param mop: - operand to be stored
      :param flags: - reserved for future use
      :param outins: - (OUT) the last generated instruction
      :returns: success



   .. py:method:: emit_micro_mvm(code: mcode_t, dtype: op_dtype_t, l: int, r: int, d: int, offsize: int) -> minsn_t *

      Emit one microinstruction. This variant takes a data type not a size. 
              



   .. py:method:: emit(*args) -> minsn_t *

      This function has the following signatures:

          0. emit(code: mcode_t, width: int, l: int, r: int, d: int, offsize: int) -> minsn_t *
          1. emit(code: mcode_t, l: const mop_t *, r: const mop_t *, d: const mop_t *) -> minsn_t *

      # 0: emit(code: mcode_t, width: int, l: int, r: int, d: int, offsize: int) -> minsn_t *

      Emit one microinstruction. The L, R, D arguments usually mean the register number. However, they depend on CODE. For example:
      * for m_goto and m_jcnd L is the target address
      * for m_ldc L is the constant value to load



      :returns: created microinstruction. can be nullptr if the instruction got immediately optimized away.

      # 1: emit(code: mcode_t, l: const mop_t *, r: const mop_t *, d: const mop_t *) -> minsn_t *

      Emit one microinstruction. This variant accepts pointers to operands. It is more difficult to use but permits to create virtually any instruction. Operands may be nullptr when it makes sense. 
              



.. py:function:: change_hexrays_config(directive: str) -> bool

   Parse DIRECTIVE and update the current configuration variables. For the syntax see hexrays.cfg 
           


.. py:function:: get_hexrays_version() -> str

   Get decompiler version. The returned string is of the form <major>.<minor>.<revision>.<build-date> 
           
   :returns: pointer to version string. For example: "2.0.0.140605"


.. py:data:: OPF_REUSE

   reuse existing window


.. py:data:: OPF_NEW_WINDOW

   open new window


.. py:data:: OPF_REUSE_ACTIVE

   reuse existing window, only if the currently active widget is a pseudocode view 
           


.. py:data:: OPF_NO_WAIT

   do not display waitbox if decompilation happens


.. py:data:: OPF_WINDOW_MGMT_MASK

.. py:function:: open_pseudocode(ea: ida_idaapi.ea_t, flags: int) -> vdui_t *

   Open pseudocode window. The specified function is decompiled and the pseudocode window is opened. 
           
   :param ea: function to decompile
   :param flags: a combination of OPF_ flags
   :returns: false if failed


.. py:function:: close_pseudocode(f: TWidget *) -> bool

   Close pseudocode window. 
           
   :param f: pointer to window
   :returns: false if failed


.. py:data:: VDRUN_NEWFILE

   Create a new file or overwrite existing file.


.. py:data:: VDRUN_APPEND

   Create a new file or append to existing file.


.. py:data:: VDRUN_ONLYNEW

   Fail if output file already exists.


.. py:data:: VDRUN_SILENT

   Silent decompilation.


.. py:data:: VDRUN_SENDIDB

   Send problematic databases to hex-rays.com.


.. py:data:: VDRUN_MAYSTOP

   The user can cancel decompilation.


.. py:data:: VDRUN_CMDLINE

   Called from ida's command line.


.. py:data:: VDRUN_STATS

   Print statistics into vd_stats.txt.


.. py:data:: VDRUN_LUMINA

   Use lumina server.


.. py:data:: VDRUN_PERF

   Print performance stats to ida.log.


.. py:function:: decompile_many(outfile: str, funcaddrs: uint64vec_t, flags: int) -> bool

   Batch decompilation. Decompile all or the specified functions 
           
   :param outfile: name of the output file
   :param funcaddrs: list of functions to decompile. If nullptr or empty, then decompile all nonlib functions
   :param flags: Batch decompilation bits
   :returns: true if no internal error occurred and the user has not cancelled decompilation


.. py:class:: hexrays_failure_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: code
      :type:  merror_t

      Microcode error code



   .. py:attribute:: errea
      :type:  ida_idaapi.ea_t

      associated address



   .. py:attribute:: str
      :type:  hexrays_failure_t.str

      string information



   .. py:method:: desc() -> str


.. py:class:: vd_failure_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: hf
      :type:  hexrays_failure_t


   .. py:method:: desc() -> str


.. py:class:: vd_interr_t(ea: ida_idaapi.ea_t, buf: str)

   Bases: :py:obj:`vd_failure_t`


   .. py:attribute:: thisown


.. py:function:: send_database(err: hexrays_failure_t, silent: bool) -> None

   Send the database to Hex-Rays. This function sends the current database to the Hex-Rays server. The database is sent in the compressed form over an encrypted (SSL) connection. 
           
   :param err: failure description object. Empty hexrays_failure_t object can be used if error information is not available.
   :param silent: if false, a dialog box will be displayed before sending the database.


.. py:class:: gco_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str

      register or stkvar name



   .. py:attribute:: stkoff
      :type:  int

      if stkvar, stack offset



   .. py:attribute:: regnum
      :type:  int

      if register, the register id



   .. py:attribute:: size
      :type:  int

      operand size



   .. py:attribute:: flags
      :type:  int


   .. py:method:: is_reg() -> bool


   .. py:method:: is_use() -> bool


   .. py:method:: is_def() -> bool


   .. py:method:: append_to_list(list: mlist_t, mba: mba_t) -> bool

      Append operand info to LIST. This function converts IDA register number or stack offset to a decompiler list. 
              
      :param list: list to append to
      :param mba: microcode object



   .. py:method:: cvt_to_ivl() -> vivl_t

      Convert operand info to VIVL. The returned VIVL can be used, for example, in a call of get_valranges(). 
              



.. py:data:: GCO_STK

   a stack variable


.. py:data:: GCO_REG

   is register? otherwise a stack variable


.. py:data:: GCO_USE

   is source operand?


.. py:data:: GCO_DEF

   is destination operand?


.. py:function:: get_current_operand(out: gco_info_t) -> bool

   Get the instruction operand under the cursor. This function determines the operand that is under the cursor in the active disassembly listing. If the operand refers to a register or stack variable, it returns true. 
           


.. py:function:: remitem(e: citem_t) -> None

.. py:data:: cot_empty

.. py:data:: cot_comma

   x, y


.. py:data:: cot_asg

   x = y


.. py:data:: cot_asgbor

   x |= y


.. py:data:: cot_asgxor

   x ^= y


.. py:data:: cot_asgband

   x &= y


.. py:data:: cot_asgadd

   x += y


.. py:data:: cot_asgsub

   x -= y


.. py:data:: cot_asgmul

   x *= y


.. py:data:: cot_asgsshr

   x >>= y signed


.. py:data:: cot_asgushr

   x >>= y unsigned


.. py:data:: cot_asgshl

   x <<= y


.. py:data:: cot_asgsdiv

   x /= y signed


.. py:data:: cot_asgudiv

   x /= y unsigned


.. py:data:: cot_asgsmod

   x %= y signed


.. py:data:: cot_asgumod

   x %= y unsigned


.. py:data:: cot_tern

   x ? y : z


.. py:data:: cot_lor

   x || y


.. py:data:: cot_land

   x && y


.. py:data:: cot_bor

   x | y


.. py:data:: cot_xor

   x ^ y


.. py:data:: cot_band

   x & y


.. py:data:: cot_eq

   x == y int or fpu (see EXFL_FPOP)


.. py:data:: cot_ne

   x != y int or fpu (see EXFL_FPOP)


.. py:data:: cot_sge

   x >= y signed or fpu (see EXFL_FPOP)


.. py:data:: cot_uge

   x >= y unsigned


.. py:data:: cot_sle

   x <= y signed or fpu (see EXFL_FPOP)


.. py:data:: cot_ule

   x <= y unsigned


.. py:data:: cot_sgt

   x > y signed or fpu (see EXFL_FPOP)


.. py:data:: cot_ugt

   x > y unsigned


.. py:data:: cot_slt

   x < y signed or fpu (see EXFL_FPOP)


.. py:data:: cot_ult

   x < y unsigned


.. py:data:: cot_sshr

   x >> y signed


.. py:data:: cot_ushr

   x >> y unsigned


.. py:data:: cot_shl

   x << y


.. py:data:: cot_add

   x + y


.. py:data:: cot_sub

   x - y


.. py:data:: cot_mul

   x * y


.. py:data:: cot_sdiv

   x / y signed


.. py:data:: cot_udiv

   x / y unsigned


.. py:data:: cot_smod

   x % y signed


.. py:data:: cot_umod

   x % y unsigned


.. py:data:: cot_fadd

   x + y fp


.. py:data:: cot_fsub

   x - y fp


.. py:data:: cot_fmul

   x * y fp


.. py:data:: cot_fdiv

   x / y fp


.. py:data:: cot_fneg

   -x fp


.. py:data:: cot_neg

   -x


.. py:data:: cot_cast

   (type)x


.. py:data:: cot_lnot

   !x


.. py:data:: cot_bnot

   ~x


.. py:data:: cot_ptr

   *x, access size in 'ptrsize'


.. py:data:: cot_ref

   &x


.. py:data:: cot_postinc

   x++


.. py:data:: cot_postdec

   x-


.. py:data:: cot_preinc

   ++x


.. py:data:: cot_predec

   -x


.. py:data:: cot_call

   x(...)


.. py:data:: cot_idx

   x[y]


.. py:data:: cot_memref

   x.m


.. py:data:: cot_memptr

   x->m, access size in 'ptrsize'


.. py:data:: cot_num

   n


.. py:data:: cot_fnum

   fpc


.. py:data:: cot_str

   string constant (user representation)


.. py:data:: cot_obj

   obj_ea


.. py:data:: cot_var

   v


.. py:data:: cot_insn

   instruction in expression, internal representation only


.. py:data:: cot_sizeof

   sizeof(x)


.. py:data:: cot_helper

   arbitrary name


.. py:data:: cot_type

   arbitrary type


.. py:data:: cot_last

.. py:data:: cit_empty

   instruction types start here


.. py:data:: cit_block

   block-statement: { ... }


.. py:data:: cit_expr

   expression-statement: expr;


.. py:data:: cit_if

   if-statement


.. py:data:: cit_for

   for-statement


.. py:data:: cit_while

   while-statement


.. py:data:: cit_do

   do-statement


.. py:data:: cit_switch

   switch-statement


.. py:data:: cit_break

   break-statement


.. py:data:: cit_continue

   continue-statement


.. py:data:: cit_return

   return-statement


.. py:data:: cit_goto

   goto-statement


.. py:data:: cit_asm

   asm-statement


.. py:data:: cit_try

   C++ try-statement.


.. py:data:: cit_throw

   C++ throw-statement.


.. py:data:: cit_end

.. py:function:: negated_relation(op: ctype_t) -> ctype_t

   Negate a comparison operator. For example, cot_sge becomes cot_slt.


.. py:function:: swapped_relation(op: ctype_t) -> ctype_t

   Swap a comparison operator. For example, cot_sge becomes cot_sle.


.. py:function:: get_op_signness(op: ctype_t) -> type_sign_t

   Get operator sign. Meaningful for sign-dependent operators, like cot_sdiv.


.. py:function:: asgop(cop: ctype_t) -> ctype_t

   Convert plain operator into assignment operator. For example, cot_add returns cot_asgadd.


.. py:function:: asgop_revert(cop: ctype_t) -> ctype_t

   Convert assignment operator into plain operator. For example, cot_asgadd returns cot_add 
           
   :returns: cot_empty is the input operator is not an assignment operator.


.. py:function:: op_uses_x(op: ctype_t) -> bool

   Does operator use the 'x' field of cexpr_t?


.. py:function:: op_uses_y(op: ctype_t) -> bool

   Does operator use the 'y' field of cexpr_t?


.. py:function:: op_uses_z(op: ctype_t) -> bool

   Does operator use the 'z' field of cexpr_t?


.. py:function:: is_binary(op: ctype_t) -> bool

   Is binary operator?


.. py:function:: is_unary(op: ctype_t) -> bool

   Is unary operator?


.. py:function:: is_relational(op: ctype_t) -> bool

   Is comparison operator?


.. py:function:: is_assignment(op: ctype_t) -> bool

   Is assignment operator?


.. py:function:: accepts_udts(op: ctype_t) -> bool

.. py:function:: is_prepost(op: ctype_t) -> bool

   Is pre/post increment/decrement operator?


.. py:function:: is_commutative(op: ctype_t) -> bool

   Is commutative operator?


.. py:function:: is_additive(op: ctype_t) -> bool

   Is additive operator?


.. py:function:: is_multiplicative(op: ctype_t) -> bool

   Is multiplicative operator?


.. py:function:: is_bitop(op: ctype_t) -> bool

   Is bit related operator?


.. py:function:: is_logical(op: ctype_t) -> bool

   Is logical operator?


.. py:function:: is_loop(op: ctype_t) -> bool

   Is loop statement code?


.. py:function:: is_break_consumer(op: ctype_t) -> bool

   Does a break statement influence the specified statement code?


.. py:function:: is_lvalue(op: ctype_t) -> bool

   Is Lvalue operator?


.. py:function:: accepts_small_udts(op: ctype_t) -> bool

   Is the operator allowed on small structure or union?


.. py:class:: cnumber_t(_opnum: int = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: nf
      :type:  number_format_t

      how to represent it



   .. py:method:: value(type: tinfo_t) -> uint64

      Get value. This function will properly extend the number sign to 64bits depending on the type sign. 
              



   .. py:method:: assign(v: uint64, nbytes: int, sign: type_sign_t) -> None

      Assign new value 
              
      :param v: new value
      :param nbytes: size of the new value in bytes
      :param sign: sign of the value



   .. py:method:: compare(r: cnumber_t) -> int


.. py:class:: var_ref_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: mba
      :type:  mba_t *

      pointer to the underlying micro array



   .. py:attribute:: idx
      :type:  int

      index into lvars_t



   .. py:method:: getv() -> lvar_t &


   .. py:method:: compare(r: var_ref_t) -> int


.. py:data:: CMAT_ZERO

   does not exist


.. py:data:: CMAT_BUILT

   just generated


.. py:data:: CMAT_TRANS1

   applied first wave of transformations


.. py:data:: CMAT_NICE

   nicefied expressions


.. py:data:: CMAT_TRANS2

   applied second wave of transformations


.. py:data:: CMAT_CPA

   corrected pointer arithmetic


.. py:data:: CMAT_TRANS3

   applied third wave of transformations


.. py:data:: CMAT_CASTED

   added necessary casts


.. py:data:: CMAT_FINAL

   ready-to-use


.. py:data:: ITP_EMPTY

   nothing


.. py:data:: ITP_ARG1

   , (64 entries are reserved for 64 call arguments)


.. py:data:: ITP_ARG64

.. py:data:: ITP_BRACE1

.. py:data:: ITP_INNER_LAST

.. py:data:: ITP_ASM

   __asm-line


.. py:data:: ITP_ELSE

   else-line


.. py:data:: ITP_DO

   do-line


.. py:data:: ITP_SEMI

   semicolon


.. py:data:: ITP_CURLY1

   {


.. py:data:: ITP_CURLY2

   }


.. py:data:: ITP_BRACE2

   )


.. py:data:: ITP_COLON

   : (label)


.. py:data:: ITP_BLOCK1

   opening block comment. this comment is printed before the item (other comments are indented and printed after the item) 
             


.. py:data:: ITP_BLOCK2

   closing block comment.


.. py:data:: ITP_TRY

   C++ try statement.


.. py:data:: ITP_CASE

   bit for switch cases


.. py:data:: ITP_SIGN

   if this bit is set too, then we have a negative case value


.. py:class:: treeloc_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: itp
      :type:  item_preciser_t


.. py:data:: RETRIEVE_ONCE

   Retrieve comment if it has not been used yet.


.. py:data:: RETRIEVE_ALWAYS

   Retrieve comment even if it has been used.


.. py:class:: citem_cmt_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: used
      :type:  bool

      the comment has been retrieved?



   .. py:method:: c_str() -> str


.. py:class:: citem_locator_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      citem address



   .. py:attribute:: op
      :type:  ctype_t

      citem operation



   .. py:method:: compare(r: citem_locator_t) -> int


.. py:class:: bit_bound_t(n: int = 0, s: int = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: nbits
      :type:  int16


   .. py:attribute:: sbits
      :type:  int16


.. py:class:: citem_t(o: ctype_t = cot_empty)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      address that corresponds to the item. may be BADADDR



   .. py:attribute:: label_num
      :type:  int

      label number. -1 means no label. items of the expression types (cot_...) should not have labels at the final maturity level, but at the intermediate levels any ctree item may have a label. Labels must be unique. Usually they correspond to the basic block numbers. 
              



   .. py:attribute:: index
      :type:  int

      an index in cfunc_t::treeitems. meaningful only after print_func() 
              



   .. py:method:: swap(r: citem_t) -> None

      Swap two citem_t.



   .. py:method:: is_expr() -> bool

      Is an expression?



   .. py:method:: contains_expr(e: cexpr_t) -> bool

      Does the item contain an expression?



   .. py:method:: contains_label() -> bool

      Does the item contain a label?



   .. py:method:: find_parent_of(item: citem_t) -> citem_t *

      Find parent of the specified item. 
              
      :param item: Item to find the parent of. The search will be performed among the children of the item pointed by `this`.
      :returns: nullptr if not found



   .. py:method:: find_closest_addr(_ea: ida_idaapi.ea_t) -> citem_t *


   .. py:method:: print1(func: cfunc_t) -> None

      Print item into one line. 
              
      :param func: parent function. This argument is used to find out the referenced variable names.
      :returns: length of the generated text.



   .. py:attribute:: cinsn
      :type:  cinsn_t *const


   .. py:attribute:: cexpr
      :type:  cexpr_t *const


   .. py:attribute:: op

      item type



   .. py:attribute:: obj_id


   .. py:method:: replace_by(o)


   .. py:attribute:: meminfo


.. py:class:: cexpr_t(*args)

   Bases: :py:obj:`citem_t`


   .. py:attribute:: thisown


   .. py:attribute:: type
      :type:  tinfo_t

      expression type. must be carefully maintained



   .. py:attribute:: exflags
      :type:  int

      Expression attributes 
              



   .. py:method:: cpadone() -> bool

      Pointer arithmetic correction done for this expression?



   .. py:method:: is_odd_lvalue() -> bool


   .. py:method:: is_fpop() -> bool


   .. py:method:: is_cstr() -> bool


   .. py:method:: is_undef_val() -> bool


   .. py:method:: is_jumpout() -> bool


   .. py:method:: is_vftable() -> bool


   .. py:method:: set_cpadone() -> None


   .. py:method:: set_vftable() -> None


   .. py:method:: swap(r: cexpr_t) -> None

      Swap two citem_t.



   .. py:method:: assign(r: cexpr_t) -> cexpr_t &


   .. py:method:: compare(r: cexpr_t) -> int


   .. py:method:: cleanup() -> None

      Cleanup the expression. This function properly deletes all children and sets the item type to cot_empty. 
              



   .. py:method:: put_number(*args) -> None

      Assign a number to the expression. 
              
      :param func: current function
      :param value: number value
      :param nbytes: size of the number in bytes
      :param sign: number sign



   .. py:method:: print1(func: cfunc_t) -> None

      Print expression into one line. 
              
      :param func: parent function. This argument is used to find out the referenced variable names.



   .. py:method:: calc_type(recursive: bool) -> None

      Calculate the type of the expression. Use this function to calculate the expression type when a new expression is built 
              
      :param recursive: if true, types of all children expression will be calculated before calculating our type



   .. py:method:: equal_effect(r: cexpr_t) -> bool

      Compare two expressions. This function tries to compare two expressions in an 'intelligent' manner. For example, it knows about commutitive operators and can ignore useless casts. 
              
      :param r: the expression to compare against the current expression
      :returns: true expressions can be considered equal



   .. py:method:: is_child_of(parent: citem_t) -> bool

      Verify if the specified item is our parent. 
              
      :param parent: possible parent item
      :returns: true if the specified item is our parent



   .. py:method:: contains_operator(needed_op: ctype_t, times: int = 1) -> bool

      Check if the expression contains the specified operator. 
              
      :param needed_op: operator code to search for
      :param times: how many times the operator code should be present
      :returns: true if the expression has at least TIMES children with NEEDED_OP



   .. py:method:: contains_comma(times: int = 1) -> bool

      Does the expression contain a comma operator?



   .. py:method:: contains_insn(times: int = 1) -> bool

      Does the expression contain an embedded statement operator?



   .. py:method:: contains_insn_or_label() -> bool

      Does the expression contain an embedded statement operator or a label?



   .. py:method:: contains_comma_or_insn_or_label(maxcommas: int = 1) -> bool

      Does the expression contain a comma operator or an embedded statement operator or a label?



   .. py:method:: is_nice_expr() -> bool

      Is nice expression? Nice expressions do not contain comma operators, embedded statements, or labels. 
              



   .. py:method:: is_nice_cond() -> bool

      Is nice condition?. Nice condition is a nice expression of the boolean type. 
              



   .. py:method:: is_call_object_of(parent: citem_t) -> bool

      Is call object? 
              
      :returns: true if our expression is the call object of the specified parent expression.



   .. py:method:: is_call_arg_of(parent: citem_t) -> bool

      Is call argument? 
              
      :returns: true if our expression is a call argument of the specified parent expression.



   .. py:method:: get_type_sign() -> type_sign_t

      Get expression sign.



   .. py:method:: is_type_unsigned() -> bool

      Is expression unsigned?



   .. py:method:: is_type_signed() -> bool

      Is expression signed?



   .. py:method:: get_high_nbit_bound() -> bit_bound_t

      Get max number of bits that can really be used by the expression. For example, x % 16 can yield only 4 non-zero bits, higher bits are zero 
              



   .. py:method:: get_low_nbit_bound() -> int

      Get min number of bits that are certainly required to represent the expression. For example, constant 16 always uses 5 bits: 10000. 
              



   .. py:method:: requires_lvalue(child: cexpr_t) -> bool

      Check if the expression requires an lvalue. 
              
      :param child: The function will check if this child of our expression must be an lvalue.
      :returns: true if child must be an lvalue.



   .. py:method:: has_side_effects() -> bool

      Check if the expression has side effects. Calls, pre/post inc/dec, and assignments have side effects. 
              



   .. py:method:: numval() -> uint64

      Get numeric value of the expression. This function can be called only on cot_num expressions! 
              



   .. py:method:: is_const_value(_v: uint64) -> bool

      Check if the expression is a number with the specified value.



   .. py:method:: is_negative_const() -> bool

      Check if the expression is a negative number.



   .. py:method:: is_non_negative_const() -> bool

      Check if the expression is a non-negative number.



   .. py:method:: is_non_zero_const() -> bool

      Check if the expression is a non-zero number.



   .. py:method:: is_zero_const() -> bool

      Check if the expression is a zero.



   .. py:method:: get_const_value() -> bool

      Get expression value. 
              
      :returns: true if the expression is a number.



   .. py:method:: maybe_ptr() -> bool

      May the expression be a pointer?



   .. py:method:: get_ptr_or_array() -> cexpr_t *

      Find pointer or array child.



   .. py:method:: find_op(_op: ctype_t) -> cexpr_t *

      Find the child with the specified operator.



   .. py:method:: find_num_op() -> cexpr_t *

      Find the operand with a numeric value.



   .. py:method:: theother(what: cexpr_t) -> cexpr_t *

      Get the other operand. This function returns the other operand (not the specified one) for binary expressions. 
              



   .. py:method:: get_1num_op(o1: cexpr_t **, o2: cexpr_t **) -> bool

      Get pointers to operands. at last one operand should be a number o1 will be pointer to the number 
              



   .. py:method:: dstr() -> str


   .. py:method:: get_v() -> var_ref_t *


   .. py:method:: set_v(v: var_ref_t) -> None


   .. py:attribute:: v

      used for cot_var



   .. py:property:: n


   .. py:property:: fpc


   .. py:property:: x


   .. py:property:: y


   .. py:property:: z


   .. py:property:: a


   .. py:property:: insn


   .. py:property:: m


   .. py:property:: ptrsize


   .. py:property:: obj_ea


   .. py:property:: refwidth


   .. py:property:: helper


   .. py:property:: string


.. py:data:: EXFL_CPADONE

   pointer arithmetic correction done


.. py:data:: EXFL_LVALUE

   expression is lvalue even if it doesn't look like it


.. py:data:: EXFL_FPOP

   floating point operation


.. py:data:: EXFL_ALONE

   standalone helper


.. py:data:: EXFL_CSTR

   string literal


.. py:data:: EXFL_PARTIAL

   type of the expression is considered partial


.. py:data:: EXFL_UNDEF

   expression uses undefined value


.. py:data:: EXFL_JUMPOUT

   jump out-of-function


.. py:data:: EXFL_VFTABLE

   is ptr to vftable (used for cot_memptr, cot_memref)


.. py:data:: EXFL_ALL

   all currently defined bits


.. py:class:: ceinsn_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: expr
      :type:  cexpr_t

      Expression of the statement.



.. py:data:: CALC_CURLY_BRACES

   print curly braces if necessary


.. py:data:: NO_CURLY_BRACES

   don't print curly braces


.. py:data:: USE_CURLY_BRACES

   print curly braces without any checks


.. py:class:: cif_t(*args)

   Bases: :py:obj:`ceinsn_t`


   .. py:attribute:: thisown


   .. py:attribute:: ithen
      :type:  cinsn_t *

      Then-branch of the if-statement.



   .. py:attribute:: ielse
      :type:  cinsn_t *

      Else-branch of the if-statement. May be nullptr.



   .. py:method:: assign(r: cif_t) -> cif_t &


   .. py:method:: compare(r: cif_t) -> int


   .. py:method:: cleanup() -> None


.. py:class:: cloop_t(*args)

   Bases: :py:obj:`ceinsn_t`


   .. py:attribute:: thisown


   .. py:attribute:: body
      :type:  cinsn_t *


   .. py:method:: assign(r: cloop_t) -> cloop_t &


   .. py:method:: cleanup() -> None


.. py:class:: cfor_t

   Bases: :py:obj:`cloop_t`


   .. py:attribute:: thisown


   .. py:attribute:: init
      :type:  cexpr_t

      Initialization expression.



   .. py:attribute:: step
      :type:  cexpr_t

      Step expression.



   .. py:method:: compare(r: cfor_t) -> int


.. py:class:: cwhile_t

   Bases: :py:obj:`cloop_t`


   .. py:attribute:: thisown


   .. py:method:: compare(r: cwhile_t) -> int


.. py:class:: cdo_t

   Bases: :py:obj:`cloop_t`


   .. py:attribute:: thisown


   .. py:method:: compare(r: cdo_t) -> int


.. py:class:: creturn_t

   Bases: :py:obj:`ceinsn_t`


   .. py:attribute:: thisown


   .. py:method:: compare(r: creturn_t) -> int


.. py:class:: cgoto_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: label_num
      :type:  int

      Target label number.



   .. py:method:: compare(r: cgoto_t) -> int


.. py:class:: casm_t(*args)

   Bases: :py:obj:`ida_pro.eavec_t`


   .. py:attribute:: thisown


   .. py:method:: compare(r: casm_t) -> int


   .. py:method:: one_insn() -> bool


.. py:class:: cinsn_t(*args)

   Bases: :py:obj:`citem_t`


   .. py:attribute:: thisown


   .. py:attribute:: ctry
      :type:  ctry_t *

      details of try-statement



   .. py:attribute:: cthrow
      :type:  cthrow_t *

      details of throw-statement



   .. py:method:: swap(r: cinsn_t) -> None

      Swap two citem_t.



   .. py:method:: assign(r: cinsn_t) -> cinsn_t &


   .. py:method:: compare(r: cinsn_t) -> int


   .. py:method:: cleanup() -> None

      Cleanup the statement. This function properly deletes all children and sets the item type to cit_empty. 
              



   .. py:method:: zero() -> None

      Overwrite with zeroes without cleaning memory or deleting children.



   .. py:method:: new_insn(insn_ea: ida_idaapi.ea_t) -> cinsn_t &

      Create a new statement. The current statement must be a block. The new statement will be appended to it. 
              
      :param insn_ea: statement address



   .. py:method:: create_if(cnd: cexpr_t) -> cif_t &

      Create a new if-statement. The current statement must be a block. The new statement will be appended to it. 
              
      :param cnd: if condition. It will be deleted after being copied.



   .. py:method:: print1(func: cfunc_t) -> None

      Print the statement into one line. Currently this function is not available. 
              
      :param func: parent function. This argument is used to find out the referenced variable names.



   .. py:method:: is_ordinary_flow() -> bool

      Check if the statement passes execution to the next statement. 
              
      :returns: false if the statement breaks the control flow (like goto, return, etc)



   .. py:method:: contains_insn(type: ctype_t, times: int = 1) -> bool

      Check if the statement contains a statement of the specified type. 
              
      :param type: statement opcode to look for
      :param times: how many times TYPE should be present
      :returns: true if the statement has at least TIMES children with opcode == TYPE



   .. py:method:: collect_free_breaks(breaks: cinsnptrvec_t) -> bool

      Collect free `break` statements. This function finds all free `break` statements within the current statement. A `break` statement is free if it does not have a loop or switch parent that that is also within the current statement. 
              
      :param breaks: pointer to the variable where the vector of all found free `break` statements is returned. This argument can be nullptr.
      :returns: true if some free `break` statements have been found



   .. py:method:: collect_free_continues(continues: cinsnptrvec_t) -> bool

      Collect free `continue` statements. This function finds all free `continue` statements within the current statement. A `continue` statement is free if it does not have a loop parent that that is also within the current statement. 
              
      :param continues: pointer to the variable where the vector of all found free `continue` statements is returned. This argument can be nullptr.
      :returns: true if some free `continue` statements have been found



   .. py:method:: contains_free_break() -> bool

      Check if the statement has free `break` statements.



   .. py:method:: contains_free_continue() -> bool

      Check if the statement has free `continue` statements.



   .. py:method:: dstr() -> str


   .. py:method:: insn_is_epilog(insn: cinsn_t) -> bool
      :staticmethod:



   .. py:method:: is_epilog()


   .. py:property:: cblock


   .. py:property:: cexpr


   .. py:property:: cif


   .. py:property:: cfor


   .. py:property:: cwhile


   .. py:property:: cdo


   .. py:property:: cswitch


   .. py:property:: creturn


   .. py:property:: cgoto


   .. py:property:: casm


.. py:class:: cblock_t

   Bases: :py:obj:`cinsn_list_t`


   .. py:attribute:: thisown


   .. py:method:: compare(r: cblock_t) -> int


.. py:class:: carg_t

   Bases: :py:obj:`cexpr_t`


   .. py:attribute:: thisown


   .. py:attribute:: is_vararg
      :type:  bool

      is a vararg (matches ...)



   .. py:attribute:: formal_type
      :type:  tinfo_t

      formal parameter type (if known)



   .. py:method:: consume_cexpr(e: cexpr_t) -> None


   .. py:method:: compare(r: carg_t) -> int


.. py:class:: carglist_t(*args)

   Bases: :py:obj:`qvector_carg_t`


   .. py:attribute:: thisown


   .. py:attribute:: functype
      :type:  tinfo_t

      function object type



   .. py:attribute:: flags
      :type:  int

      call flags



   .. py:method:: compare(r: carglist_t) -> int


.. py:data:: CFL_FINAL

   call type is final, should not be changed


.. py:data:: CFL_HELPER

   created from a decompiler helper function


.. py:data:: CFL_NORET

   call does not return


.. py:class:: ccase_t

   Bases: :py:obj:`cinsn_t`


   .. py:attribute:: thisown


   .. py:attribute:: values
      :type:  uint64vec_t

      List of case values. if empty, then 'default' case 
              



   .. py:method:: compare(r: ccase_t) -> int


   .. py:method:: size() -> size_t


   .. py:method:: value(i: int) -> uint64 const &


.. py:class:: ccases_t

   Bases: :py:obj:`qvector_ccase_t`


   .. py:attribute:: thisown


   .. py:method:: compare(r: ccases_t) -> int


.. py:class:: cswitch_t

   Bases: :py:obj:`ceinsn_t`


   .. py:attribute:: thisown


   .. py:attribute:: mvnf
      :type:  cnumber_t

      Maximal switch value and number format.



   .. py:attribute:: cases
      :type:  ccases_t

      Switch cases: values and instructions.



   .. py:method:: compare(r: cswitch_t) -> int


.. py:class:: catchexpr_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: obj
      :type:  cexpr_t

      the caught object. if obj.op==cot_empty, no object. ideally, obj.op==cot_var 
              



   .. py:attribute:: fake_type
      :type:  str

      if not empty, type of the caught object. ideally, obj.type should be enough. however, in some cases the detailed type info is not available. 
              



   .. py:method:: compare(r: catchexpr_t) -> int


   .. py:method:: swap(r: catchexpr_t) -> None


   .. py:method:: is_catch_all() -> bool


.. py:class:: ccatch_t(*args, **kwargs)

   Bases: :py:obj:`cblock_t`


   .. py:attribute:: thisown


   .. py:attribute:: exprs
      :type:  catchexprs_t


   .. py:method:: compare(r: ccatch_t) -> int


   .. py:method:: is_catch_all() -> bool


   .. py:method:: swap(r: ccatch_t) -> None


.. py:class:: ctry_t(*args, **kwargs)

   Bases: :py:obj:`cblock_t`


   .. py:attribute:: thisown


   .. py:attribute:: catchs
      :type:  ccatchvec_t

      "catch all", if present, must be the last element. wind-statements must have "catch all" and nothing else. 
              



   .. py:attribute:: old_state
      :type:  size_t

      old state number (internal, MSVC related)



   .. py:attribute:: new_state
      :type:  size_t

      new state number (internal, MSVC related)



   .. py:attribute:: is_wind
      :type:  bool

      Is C++ wind statement? (not part of the C++ language) MSVC generates code like the following to keep track of constructed objects and destroy them upon an exception. Example:
      // an object is constructed at this point __wind { // some other code that may throw an exception } __unwind { // this code is executed only if there was an exception // in the __wind block. normally here we destroy the object // after that the exception is passed to the // exception handler, regular control flow is interrupted here. } // regular logic continues here, if there were no exceptions // also the object's destructor is called 
              



   .. py:method:: compare(r: ctry_t) -> int


.. py:class:: cthrow_t

   Bases: :py:obj:`ceinsn_t`


   .. py:attribute:: thisown


   .. py:method:: compare(r: cthrow_t) -> int


.. py:class:: cblock_pos_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: blk
      :type:  cblock_t *


   .. py:attribute:: p
      :type:  cblock_t::iterator


   .. py:method:: is_first_insn() -> bool


   .. py:method:: insn() -> cinsn_t *


   .. py:method:: prev_insn() -> cinsn_t *


.. py:class:: ctree_visitor_t(_flags: int)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: cv_flags
      :type:  int

      Ctree visitor property bits 
              



   .. py:method:: maintain_parents() -> bool

      Should the parent information by maintained?



   .. py:method:: must_prune() -> bool

      Should the traversal skip the children of the current item?



   .. py:method:: must_restart() -> bool

      Should the traversal restart?



   .. py:method:: is_postorder() -> bool

      Should the leave...() functions be called?



   .. py:method:: only_insns() -> bool

      Should all expressions be automatically pruned?



   .. py:method:: prune_now() -> None

      Prune children. This function may be called by a visitor() to skip all children of the current item. 
              



   .. py:method:: clr_prune() -> None

      Do not prune children. This is an internal function, no need to call it.



   .. py:method:: set_restart() -> None

      Restart the travesal. Meaningful only in apply_to_exprs()



   .. py:method:: clr_restart() -> None

      Do not restart. This is an internal function, no need to call it.



   .. py:attribute:: parents
      :type:  parents_t

      Vector of parents of the current item.



   .. py:attribute:: bposvec
      :type:  cblock_posvec_t

      Vector of block positions. Only cit_block and cit_try parents have the corresponding element in this vector. 
              



   .. py:method:: apply_to(item: citem_t, parent: citem_t) -> int

      Traverse ctree. The traversal will start at the specified item and continue until of one the visit_...() functions return a non-zero value. 
              
      :param item: root of the ctree to traverse
      :param parent: parent of the specified item. can be specified as nullptr.
      :returns: 0 or a non-zero value returned by a visit_...() function



   .. py:method:: apply_to_exprs(item: citem_t, parent: citem_t) -> int

      Traverse only expressions. The traversal will start at the specified item and continue until of one the visit_...() functions return a non-zero value. 
              
      :param item: root of the ctree to traverse
      :param parent: parent of the specified item. can be specified as nullptr.
      :returns: 0 or a non-zero value returned by a visit_...() function



   .. py:method:: parent_item() -> citem_t *

      Get parent of the current item as an item (statement or expression)



   .. py:method:: parent_expr() -> cexpr_t *

      Get parent of the current item as an expression.



   .. py:method:: parent_insn() -> cinsn_t *

      Get parent of the current item as a statement.



   .. py:method:: visit_insn(arg0: cinsn_t) -> int

      Visit a statement. This is a visitor function which should be overridden by a derived class to do some useful work. This visitor performs pre-order traserval, i.e. an item is visited before its children. 
              
      :returns: 0 to continue the traversal, nonzero to stop.



   .. py:method:: visit_expr(arg0: cexpr_t) -> int

      Visit an expression. This is a visitor function which should be overridden by a derived class to do some useful work. This visitor performs pre-order traserval, i.e. an item is visited before its children. 
              
      :returns: 0 to continue the traversal, nonzero to stop.



   .. py:method:: leave_insn(arg0: cinsn_t) -> int

      Visit a statement after having visited its children. This is a visitor function which should be overridden by a derived class to do some useful work. This visitor performs post-order traserval, i.e. an item is visited after its children. 
              
      :returns: 0 to continue the traversal, nonzero to stop.



   .. py:method:: leave_expr(arg0: cexpr_t) -> int

      Visit an expression after having visited its children. This is a visitor function which should be overridden by a derived class to do some useful work. This visitor performs post-order traserval, i.e. an item is visited after its children. 
              
      :returns: 0 to continue the traversal, nonzero to stop.



.. py:data:: CV_FAST

   do not maintain parent information


.. py:data:: CV_PRUNE

   this bit is set by visit...() to prune the walk


.. py:data:: CV_PARENTS

   maintain parent information


.. py:data:: CV_POST

   call the leave...() functions


.. py:data:: CV_RESTART

   restart enumeration at the top expr (apply_to_exprs)


.. py:data:: CV_INSNS

   visit only statements, prune all expressions do not use before the final ctree maturity because expressions may contain statements at intermediate stages (see cot_insn). Otherwise you risk missing statements embedded into expressions. 
           


.. py:class:: ctree_parentee_t(post: bool = False)

   Bases: :py:obj:`ctree_visitor_t`


   .. py:attribute:: thisown


   .. py:method:: recalc_parent_types() -> bool

      Recalculate type of parent nodes. If a node type has been changed, the visitor must recalculate all parent types, otherwise the ctree becomes inconsistent. If during this recalculation a parent node is added/deleted, this function returns true. In this case the traversal must be stopped because the information about parent nodes is stale. 
              
      :returns: false-ok to continue the traversal, true-must stop.



.. py:class:: cfunc_parentee_t(f: cfunc_t, post: bool = False)

   Bases: :py:obj:`ctree_parentee_t`


   .. py:attribute:: thisown


   .. py:attribute:: func
      :type:  cfunc_t *

      Pointer to current function.



   .. py:method:: calc_rvalue_type(target: tinfo_t, e: cexpr_t) -> bool

      Calculate rvalue type. This function tries to determine the type of the specified item based on its context. For example, if the current expression is the right side of an assignment operator, the type of its left side will be returned. This function can be used to determine the 'best' type of the specified expression. 
              
      :param target: 'best' type of the expression will be returned here
      :param e: expression to determine the desired type
      :returns: false if failed



.. py:class:: ctree_anchor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: value
      :type:  int


   .. py:method:: get_index() -> int


   .. py:method:: get_itp() -> item_preciser_t


   .. py:method:: is_valid_anchor() -> bool


   .. py:method:: is_citem_anchor() -> bool


   .. py:method:: is_lvar_anchor() -> bool


   .. py:method:: is_itp_anchor() -> bool


   .. py:method:: is_blkcmt_anchor() -> bool


.. py:data:: ANCHOR_INDEX

.. py:data:: ANCHOR_MASK

.. py:data:: ANCHOR_CITEM

   c-tree item


.. py:data:: ANCHOR_LVAR

   declaration of local variable


.. py:data:: ANCHOR_ITP

   item type preciser


.. py:data:: ANCHOR_BLKCMT

   block comment (for ctree items)


.. py:data:: VDI_NONE

   undefined


.. py:data:: VDI_EXPR

   c-tree item


.. py:data:: VDI_LVAR

   declaration of local variable


.. py:data:: VDI_FUNC

   the function itself (the very first line with the function prototype)


.. py:data:: VDI_TAIL

   cursor is at (beyond) the line end (commentable line)


.. py:class:: ctree_item_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: citype
      :type:  cursor_item_type_t

      Item type.



   .. py:attribute:: it
      :type:  citem_t *


   .. py:attribute:: e
      :type:  cexpr_t *

      VDI_EXPR: Expression.



   .. py:attribute:: i
      :type:  cinsn_t *

      VDI_EXPR: Statement.



   .. py:attribute:: l
      :type:  lvar_t *

      VDI_LVAR: Local variable.



   .. py:attribute:: f
      :type:  cfunc_t *

      VDI_FUNC: Function.



   .. py:method:: get_udm(udm: udm_t = None, parent: tinfo_t = None, p_offset: uint64 * = None) -> int

      Get type of a structure field. If the current item is a structure/union field, this function will return information about it. 
              
      :param udm: pointer to buffer for the udt member info.
      :param parent: pointer to buffer for the struct/union type.
      :param p_offset: pointer to the offset in bits inside udt.
      :returns: member index or -1 if failed Both output parameters can be nullptr.



   .. py:method:: get_edm(parent: tinfo_t) -> int

      Get type of an enum member. If the current item is a symbolic constant, this function will return information about it. 
              
      :param parent: pointer to buffer for the enum type.
      :returns: member index or -1 if failed



   .. py:method:: get_lvar() -> lvar_t *

      Get pointer to local variable. If the current item is a local variable, this function will return pointer to its definition. 
              
      :returns: nullptr if failed



   .. py:method:: get_ea() -> ida_idaapi.ea_t

      Get address of the current item. Each ctree item has an address. 
              
      :returns: BADADDR if failed



   .. py:method:: get_label_num(gln_flags: int) -> int

      Get label number of the current item. 
              
      :param gln_flags: Combination of get_label_num control bits
      :returns: -1 if failed or no label



   .. py:method:: is_citem() -> bool

      Is the current item is a ctree item?



   .. py:method:: dstr() -> str


   .. py:attribute:: loc
      :type:  treeloc_t *const

      VDI_TAIL: Line tail.



.. py:data:: GLN_CURRENT

   get label of the current item


.. py:data:: GLN_GOTO_TARGET

   get goto target


.. py:data:: GLN_ALL

   get both


.. py:data:: FORBID_UNUSED_LABELS

   Unused labels cause interr.


.. py:data:: ALLOW_UNUSED_LABELS

   Unused labels are permitted.


.. py:function:: save_user_labels(func_ea: ida_idaapi.ea_t, user_labels: user_labels_t, func: cfunc_t = None) -> None

   Save user defined labels into the database. 
           
   :param func_ea: the entry address of the function, ignored if FUNC != nullptr
   :param user_labels: collection of user defined labels
   :param func: pointer to current function, if FUNC != nullptr, then save labels using a more stable method that preserves them even when the decompiler output drastically changes


.. py:function:: save_user_cmts(func_ea: ida_idaapi.ea_t, user_cmts: user_cmts_t) -> None

   Save user defined comments into the database. 
           
   :param func_ea: the entry address of the function
   :param user_cmts: collection of user defined comments


.. py:function:: save_user_numforms(func_ea: ida_idaapi.ea_t, numforms: user_numforms_t) -> None

   Save user defined number formats into the database. 
           
   :param func_ea: the entry address of the function
   :param numforms: collection of user defined comments


.. py:function:: save_user_iflags(func_ea: ida_idaapi.ea_t, iflags: user_iflags_t) -> None

   Save user defined citem iflags into the database. 
           
   :param func_ea: the entry address of the function
   :param iflags: collection of user defined citem iflags


.. py:function:: save_user_unions(func_ea: ida_idaapi.ea_t, unions: user_unions_t) -> None

   Save user defined union field selections into the database. 
           
   :param func_ea: the entry address of the function
   :param unions: collection of union field selections


.. py:function:: restore_user_labels(func_ea: ida_idaapi.ea_t, func: cfunc_t = None) -> user_labels_t *

   Restore user defined labels from the database. 
           
   :param func_ea: the entry address of the function, ignored if FUNC != nullptr
   :param func: pointer to current function
   :returns: collection of user defined labels. The returned object must be deleted by the caller using delete_user_labels()


.. py:function:: restore_user_cmts(func_ea: ida_idaapi.ea_t) -> user_cmts_t *

   Restore user defined comments from the database. 
           
   :param func_ea: the entry address of the function
   :returns: collection of user defined comments. The returned object must be deleted by the caller using delete_user_cmts()


.. py:function:: restore_user_numforms(func_ea: ida_idaapi.ea_t) -> user_numforms_t *

   Restore user defined number formats from the database. 
           
   :param func_ea: the entry address of the function
   :returns: collection of user defined number formats. The returned object must be deleted by the caller using delete_user_numforms()


.. py:function:: restore_user_iflags(func_ea: ida_idaapi.ea_t) -> user_iflags_t *

   Restore user defined citem iflags from the database. 
           
   :param func_ea: the entry address of the function
   :returns: collection of user defined iflags. The returned object must be deleted by the caller using delete_user_iflags()


.. py:function:: restore_user_unions(func_ea: ida_idaapi.ea_t) -> user_unions_t *

   Restore user defined union field selections from the database. 
           
   :param func_ea: the entry address of the function
   :returns: collection of union field selections The returned object must be deleted by the caller using delete_user_unions()


.. py:class:: cfunc_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: entry_ea
      :type:  ida_idaapi.ea_t

      function entry address



   .. py:attribute:: mba
      :type:  mba_t *

      underlying microcode



   .. py:attribute:: body
      :type:  cinsn_t

      function body, must be a block



   .. py:attribute:: argidx
      :type:  intvec_t &

      list of arguments (indexes into vars)



   .. py:attribute:: maturity
      :type:  ctree_maturity_t

      maturity level



   .. py:attribute:: user_labels
      :type:  user_labels_t *

      user-defined labels.



   .. py:attribute:: user_cmts
      :type:  user_cmts_t *

      user-defined comments.



   .. py:attribute:: numforms
      :type:  user_numforms_t *

      user-defined number formats.



   .. py:attribute:: user_iflags
      :type:  user_iflags_t *

      user-defined item flags ctree item iflags bits



   .. py:attribute:: user_unions
      :type:  user_unions_t *

      user-defined union field selections. 
              



   .. py:attribute:: refcnt
      :type:  int

      reference count to this object. use cfuncptr_t



   .. py:attribute:: statebits
      :type:  int

      current cfunc_t state. see cfunc state bits 
              



   .. py:attribute:: hdrlines
      :type:  int

      number of lines in the declaration area



   .. py:attribute:: treeitems
      :type:  citem_pointers_t

      vector of pointers to citem_t objects (nodes constituting the ctree)



   .. py:method:: release() -> None


   .. py:method:: build_c_tree() -> None

      Generate the function body. This function (re)generates the function body from the underlying microcode. 
              



   .. py:method:: verify(aul: allow_unused_labels_t, even_without_debugger: bool) -> None

      Verify the ctree. This function verifies the ctree. If the ctree is malformed, an internal error is generated. Use it to verify the ctree after your modifications. 
              
      :param aul: Are unused labels acceptable?
      :param even_without_debugger: if false and there is no debugger, the verification will be skipped



   .. py:method:: print_dcl() -> None

      Print function prototype. 
              



   .. py:method:: print_func(vp: vc_printer_t) -> None

      Print function text. 
              
      :param vp: printer helper class to receive the generated text.



   .. py:method:: get_func_type(type: tinfo_t) -> bool

      Get the function type. 
              
      :param type: variable where the function type is returned
      :returns: false if failure



   .. py:method:: get_lvars() -> lvars_t *

      Get vector of local variables. 
              
      :returns: pointer to the vector of local variables. If you modify this vector, the ctree must be regenerated in order to have correct cast operators. Use build_c_tree() for that. Removing lvars should be done carefully: all references in ctree and microcode must be corrected after that.



   .. py:method:: get_stkoff_delta() -> int

      Get stack offset delta. The local variable stack offsets retrieved by v.location.stkoff() should be adjusted before being used as stack frame offsets in IDA. 
              
      :returns: the delta to apply. example: ida_stkoff = v.location.stkoff() - f->get_stkoff_delta()



   .. py:method:: find_label(label: int) -> citem_t *

      Find the label. 
              
      :returns: pointer to the ctree item with the specified label number.



   .. py:method:: remove_unused_labels() -> None

      Remove unused labels. This function checks what labels are really used by the function and removes the unused ones. You must call it after deleting a goto statement. 
              



   .. py:method:: get_user_cmt(loc: treeloc_t, rt: cmt_retrieval_type_t) -> str

      Retrieve a user defined comment. 
              
      :param loc: ctree location
      :param rt: should already retrieved comments retrieved again?
      :returns: pointer to the comment string or nullptr



   .. py:method:: set_user_cmt(loc: treeloc_t, cmt: str) -> None

      Set a user defined comment. This function stores the specified comment in the cfunc_t structure. The save_user_cmts() function must be called after it. 
              
      :param loc: ctree location
      :param cmt: new comment. if empty or nullptr, then an existing comment is deleted.



   .. py:method:: get_user_iflags(loc: citem_locator_t) -> int

      Retrieve citem iflags. 
              
      :param loc: citem locator
      :returns: ctree item iflags bits or 0



   .. py:method:: set_user_iflags(loc: citem_locator_t, iflags: int) -> None

      Set citem iflags. 
              
      :param loc: citem locator
      :param iflags: new iflags



   .. py:method:: has_orphan_cmts() -> bool

      Check if there are orphan comments.



   .. py:method:: del_orphan_cmts() -> int

      Delete all orphan comments. The save_user_cmts() function must be called after this call. 
              



   .. py:method:: get_user_union_selection(ea: ida_idaapi.ea_t, path: intvec_t) -> bool

      Retrieve a user defined union field selection. 
              
      :param ea: address
      :param path: out: path describing the union selection.
      :returns: pointer to the path or nullptr



   .. py:method:: set_user_union_selection(ea: ida_idaapi.ea_t, path: intvec_t) -> None

      Set a union field selection. The save_user_unions() function must be called after calling this function. 
              
      :param ea: address
      :param path: in: path describing the union selection.



   .. py:method:: save_user_labels() -> None

      Save user-defined labels into the database.



   .. py:method:: save_user_cmts() -> None

      Save user-defined comments into the database.



   .. py:method:: save_user_numforms() -> None

      Save user-defined number formats into the database.



   .. py:method:: save_user_iflags() -> None

      Save user-defined iflags into the database.



   .. py:method:: save_user_unions() -> None

      Save user-defined union field selections into the database.



   .. py:method:: get_line_item(line: str, x: int, is_ctree_line: bool, phead: ctree_item_t, pitem: ctree_item_t, ptail: ctree_item_t) -> bool

      Get ctree item for the specified cursor position. 
              
      :param line: line of decompilation text (element of sv)
      :param x: x cursor coordinate in the line
      :param is_ctree_line: does the line belong to statement area? (if not, it is assumed to belong to the declaration area)
      :param phead: ptr to the first item on the line (used to attach block comments). May be nullptr
      :param pitem: ptr to the current item. May be nullptr
      :param ptail: ptr to the last item on the line (used to attach indented comments). May be nullptr
      :returns: false if failed to get the current item



   .. py:method:: get_warnings() -> hexwarns_t &

      Get information about decompilation warnings. 
              
      :returns: reference to the vector of warnings



   .. py:method:: get_eamap() -> eamap_t &

      Get pointer to ea->insn map. This function initializes eamap if not done yet. 
              



   .. py:method:: get_boundaries() -> boundaries_t &

      Get pointer to map of instruction boundaries. This function initializes the boundary map if not done yet. 
              



   .. py:method:: get_pseudocode() -> strvec_t const &

      Get pointer to decompilation output: the pseudocode. This function generates pseudocode if not done yet. 
              



   .. py:method:: refresh_func_ctext() -> None

      Refresh ctext after a ctree modification. This function informs the decompiler that ctree (body) have been modified and ctext (sv) does not correspond to it anymore. It also refreshes the pseudocode windows if there is any. 
              



   .. py:method:: recalc_item_addresses() -> None

      Recalculate item adresses. This function may be required after shuffling ctree items. For example, when adding or removing statements of a block, or changing 'if' statements. 
              



   .. py:method:: gather_derefs(ci: ctree_item_t, udm: udt_type_data_t = None) -> bool


   .. py:method:: locked() -> bool


   .. py:method:: find_item_coords(*args)

      This method has the following signatures:

          1. find_item_coords(item: citem_t) -> Tuple[int, int]
          2. find_item_coords(item: citem_t, x: int_pointer, y: int_pointer) -> bool

      NOTE: The second form is retained for backward-compatibility,
      but we strongly recommend using the first.

      :param item: The item to find coordinates for in the pseudocode listing



.. py:data:: CIT_COLLAPSED

   display ctree item in collapsed form


.. py:data:: CFS_BOUNDS

   'eamap' and 'boundaries' are ready


.. py:data:: CFS_TEXT

   'sv' is ready (and hdrlines)


.. py:data:: CFS_LVARS_HIDDEN

   local variable definitions are collapsed


.. py:data:: CFS_LOCKED

   cfunc is temporarily locked


.. py:data:: DECOMP_NO_WAIT

   do not display waitbox


.. py:data:: DECOMP_NO_CACHE

   do not use decompilation cache (snippets are never cached)


.. py:data:: DECOMP_NO_FRAME

   do not use function frame info (only snippet mode)


.. py:data:: DECOMP_WARNINGS

   display warnings in the output window


.. py:data:: DECOMP_ALL_BLKS

   generate microcode for unreachable blocks


.. py:data:: DECOMP_NO_HIDE

   do not close display waitbox. see close_hexrays_waitbox()


.. py:data:: DECOMP_GXREFS_DEFLT

   the default behavior: do not update the global xrefs cache upon decompile() call, but when the pseudocode text is generated (e.g., through cfunc_t.get_pseudocode()) 
           


.. py:data:: DECOMP_GXREFS_NOUPD

   do not update the global xrefs cache


.. py:data:: DECOMP_GXREFS_FORCE

   update the global xrefs cache immediately


.. py:data:: DECOMP_VOID_MBA

   return empty mba object (to be used with gen_microcode)


.. py:data:: DECOMP_OUTLINE

   generate code for an outline


.. py:function:: close_hexrays_waitbox() -> None

   Close the waitbox displayed by the decompiler. Useful if DECOMP_NO_HIDE was used during decompilation. 
           


.. py:function:: decompile(mbr: mba_ranges_t, hf: hexrays_failure_t = None, decomp_flags: int = 0) -> cfuncptr_t

   Decompile a snippet or a function. 
           
   :param mbr: what to decompile
   :param hf: extended error information (if failed)
   :param decomp_flags: bitwise combination of decompile() flags... bits
   :returns: pointer to the decompilation result (a reference counted pointer). nullptr if failed.


.. py:function:: decompile_func(pfn: func_t *, hf: hexrays_failure_t = None, decomp_flags: int = 0) -> cfuncptr_t

   Decompile a function. Multiple decompilations of the same function return the same object. 
           
   :param pfn: pointer to function to decompile
   :param hf: extended error information (if failed)
   :param decomp_flags: bitwise combination of decompile() flags... bits
   :returns: pointer to the decompilation result (a reference counted pointer). nullptr if failed.


.. py:function:: gen_microcode(mbr: mba_ranges_t, hf: hexrays_failure_t = None, retlist: mlist_t = None, decomp_flags: int = 0, reqmat: mba_maturity_t = MMAT_GLBOPT3) -> mba_t *

   Generate microcode of an arbitrary code snippet 
           
   :param mbr: snippet ranges
   :param hf: extended error information (if failed)
   :param retlist: list of registers the snippet returns
   :param decomp_flags: bitwise combination of decompile() flags... bits
   :param reqmat: required microcode maturity
   :returns: pointer to the microcode, nullptr if failed.


.. py:function:: create_empty_mba(mbr: mba_ranges_t, hf: hexrays_failure_t = None) -> mba_t *

   Create an empty microcode object.


.. py:function:: create_cfunc(mba: mba_t) -> cfuncptr_t

   Create a new cfunc_t object. 
           
   :param mba: microcode object. After creating the cfunc object it takes the ownership of MBA.


.. py:function:: mark_cfunc_dirty(ea: ida_idaapi.ea_t, close_views: bool = False) -> bool

   Flush the cached decompilation results. Erases a cache entry for the specified function. 
           
   :param ea: function to erase from the cache
   :param close_views: close pseudocode windows that show the function
   :returns: if a cache entry existed.


.. py:function:: clear_cached_cfuncs() -> None

   Flush all cached decompilation results.


.. py:function:: has_cached_cfunc(ea: ida_idaapi.ea_t) -> bool

   Do we have a cached decompilation result for 'ea'?


.. py:function:: get_ctype_name(op: ctype_t) -> str

.. py:function:: create_field_name(*args) -> str

.. py:data:: hxe_flowchart

   Flowchart has been generated. 
             


.. py:data:: hxe_stkpnts

   SP change points have been calculated. 
             


.. py:data:: hxe_prolog

   Prolog analysis has been finished. 
             


.. py:data:: hxe_microcode

   Microcode has been generated. 
             


.. py:data:: hxe_preoptimized

   Microcode has been preoptimized. 
             


.. py:data:: hxe_locopt

   Basic block level optimization has been finished. 
             


.. py:data:: hxe_prealloc

   Local variables: preallocation step begins. 
             


.. py:data:: hxe_glbopt

   Global optimization has been finished. If microcode is modified, MERR_LOOP must be returned. It will cause a complete restart of the optimization. 
             


.. py:data:: hxe_pre_structural

   Structure analysis is starting. 
             


.. py:data:: hxe_structural

   Structural analysis has been finished. 
             


.. py:data:: hxe_maturity

   Ctree maturity level is being changed. 
             


.. py:data:: hxe_interr

   Internal error has occurred. 
             


.. py:data:: hxe_combine

   Trying to combine instructions of basic block. 
             


.. py:data:: hxe_print_func

   Printing ctree and generating text. 
             


.. py:data:: hxe_func_printed

   Function text has been generated. Plugins may modify the text in cfunc_t::sv. However, it is too late to modify the ctree or microcode. The text uses regular color codes (see lines.hpp) COLOR_ADDR is used to store pointers to ctree items. 
             


.. py:data:: hxe_resolve_stkaddrs

   The optimizer is about to resolve stack addresses. 
             


.. py:data:: hxe_build_callinfo

   Analyzing a call instruction. 
             


.. py:data:: hxe_callinfo_built

   A call instruction has been anallyzed. 
             


.. py:data:: hxe_calls_done

   All calls have been analyzed. 
             


.. py:data:: hxe_begin_inlining

   Starting to inline outlined functions. 
             


.. py:data:: hxe_inlining_func

   A set of ranges is going to be inlined. 
             


.. py:data:: hxe_inlined_func

   A set of ranges got inlined. 
             


.. py:data:: hxe_collect_warnings

   Collect warning messages from plugins. These warnings will be displayed at the function header, after the user-defined comments. 
             


.. py:data:: hxe_open_pseudocode

   New pseudocode view has been opened. 
             


.. py:data:: hxe_switch_pseudocode

   Existing pseudocode view has been reloaded with a new function. Its text has not been refreshed yet, only cfunc and mba pointers are ready. 
             


.. py:data:: hxe_refresh_pseudocode

   Existing pseudocode text has been refreshed. Adding/removing pseudocode lines is forbidden in this event. 
             


.. py:data:: hxe_close_pseudocode

   Pseudocode view is being closed. 
             


.. py:data:: hxe_keyboard

   Keyboard has been hit. 
             


.. py:data:: hxe_right_click

   Mouse right click. Use hxe_populating_popup instead, in case you want to add items in the popup menu. 
             


.. py:data:: hxe_double_click

   Mouse double click. 
             


.. py:data:: hxe_curpos

   Current cursor position has been changed. (for example, by left-clicking or using keyboard)

             


.. py:data:: hxe_create_hint

   Create a hint for the current item. 
             


.. py:data:: hxe_text_ready

   Decompiled text is ready. 
             


.. py:data:: hxe_populating_popup

   Populating popup menu. We can add menu items now. 
             


.. py:data:: lxe_lvar_name_changed

   Local variable got renamed. 
             


.. py:data:: lxe_lvar_type_changed

   Local variable type got changed. 
             


.. py:data:: lxe_lvar_cmt_changed

   Local variable comment got changed. 
             


.. py:data:: lxe_lvar_mapping_changed

   Local variable mapping got changed. 
             


.. py:data:: hxe_cmt_changed

   Comment got changed. 
             


.. py:data:: hxe_mba_maturity

   Maturity level of an MBA was changed. 
             


.. py:data:: USE_KEYBOARD

   Keyboard.


.. py:data:: USE_MOUSE

   Mouse.


.. py:class:: ctext_position_t(_lnnum: int = -1, _x: int = 0, _y: int = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: lnnum
      :type:  int

      Line number.



   .. py:attribute:: x
      :type:  int

      x coordinate of the cursor within the window



   .. py:attribute:: y
      :type:  int

      y coordinate of the cursor within the window 
              



   .. py:method:: in_ctree(hdrlines: int) -> bool

      Is the cursor in the variable/type declaration area? 
              
      :param hdrlines: Number of lines of the declaration area



   .. py:method:: compare(r: ctext_position_t) -> int


.. py:data:: HEXRAYS_API_MAGIC

.. py:class:: history_item_t(*args)

   Bases: :py:obj:`ctext_position_t`


   .. py:attribute:: thisown


   .. py:attribute:: func_ea
      :type:  ida_idaapi.ea_t

      The entry address of the decompiled function.



   .. py:attribute:: curr_ea
      :type:  ida_idaapi.ea_t

      Current address.



   .. py:attribute:: end
      :type:  ida_idaapi.ea_t

      BADADDR-decompile a function; otherwise end of the range.



.. py:class:: vdui_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: flags
      :type:  int

      Properties of pseudocode window 
              



   .. py:method:: visible() -> bool

      Is the pseudocode window visible? if not, it might be invisible or destroyed 
              



   .. py:method:: valid() -> bool

      Does the pseudocode window contain valid code? It can become invalid if the function type gets changed in IDA. 
              



   .. py:method:: locked() -> bool

      Does the pseudocode window contain valid code? We lock windows before modifying them, to avoid recursion due to the events generated by the IDA kernel. 
              
      :returns: true: The window is locked and may have stale info



   .. py:method:: set_visible(v: bool) -> None


   .. py:method:: set_valid(v: bool) -> None


   .. py:method:: set_locked(v: bool) -> bool


   .. py:attribute:: view_idx
      :type:  int

      pseudocode window index (0..)



   .. py:attribute:: ct
      :type:  TWidget *

      pseudocode view



   .. py:attribute:: toplevel
      :type:  TWidget *


   .. py:attribute:: mba
      :type:  mba_t *

      pointer to underlying microcode



   .. py:attribute:: cfunc
      :type:  cfuncptr_t

      pointer to function object



   .. py:attribute:: last_code
      :type:  merror_t

      result of the last user action. See Microcode error code



   .. py:attribute:: cpos
      :type:  ctext_position_t

      Current ctext position.



   .. py:attribute:: head
      :type:  ctree_item_t

      First ctree item on the current line (for block comments)



   .. py:attribute:: item
      :type:  ctree_item_t

      Current ctree item.



   .. py:attribute:: tail
      :type:  ctree_item_t

      Tail ctree item on the current line (for indented comments)



   .. py:method:: refresh_view(redo_mba: bool) -> None

      Refresh pseudocode window. This is the highest level refresh function. It causes the most profound refresh possible and can lead to redecompilation of the current function. Please consider using refresh_ctext() if you need a more superficial refresh. 
              
      :param redo_mba: true means to redecompile the current function
       false means to rebuild ctree without regenerating microcode



   .. py:method:: refresh_ctext(activate: bool = True) -> None

      Refresh pseudocode window. This function refreshes the pseudocode window by regenerating its text from cfunc_t. Instead of this function use refresh_func_ctext(), which refreshes all pseudocode windows for the function. 
              



   .. py:method:: switch_to(f: cfuncptr_t, activate: bool) -> None

      Display the specified pseudocode. This function replaces the pseudocode window contents with the specified cfunc_t. 
              
      :param f: pointer to the function to display.
      :param activate: should the pseudocode window get focus?



   .. py:method:: in_ctree() -> bool

      Is the current item a statement?

      :returns: false if the cursor is in the local variable/type declaration area
       true if the cursor is in the statement area



   .. py:method:: get_number() -> cnumber_t *

      Get current number. If the current item is a number, return pointer to it. 
              
      :returns: nullptr if the current item is not a number This function returns non-null for the cases of a 'switch' statement Also, if the current item is a casted number, then this function will succeed.



   .. py:method:: get_current_label() -> int

      Get current label. If there is a label under the cursor, return its number. 
              
      :returns: -1 if there is no label under the cursor. prereq: get_current_item() has been called



   .. py:method:: clear() -> None

      Clear the pseudocode window. It deletes the current function and microcode. 
              



   .. py:method:: refresh_cpos(idv: input_device_t) -> bool

      Refresh the current position. This function refreshes the cpos field. 
              
      :param idv: keyboard or mouse
      :returns: false if failed



   .. py:method:: get_current_item(idv: input_device_t) -> bool

      Get current item. This function refreshes the cpos, item, tail fields. 
              
      :param idv: keyboard or mouse
      :returns: false if failed



   .. py:method:: ui_rename_lvar(v: lvar_t) -> bool

      Rename local variable. This function displays a dialog box and allows the user to rename a local variable. 
              
      :param v: pointer to local variable
      :returns: false if failed or cancelled



   .. py:method:: rename_lvar(v: lvar_t, name: str, is_user_name: bool) -> bool

      Rename local variable. This function permanently renames a local variable. 
              
      :param v: pointer to local variable
      :param name: new variable name
      :param is_user_name: use true to save the new name into the database. use false to delete the saved name.
      :returns: false if failed



   .. py:method:: ui_set_call_type(e: cexpr_t) -> bool

      Set type of a function call This function displays a dialog box and allows the user to change the type of a function call 
              
      :param e: pointer to call expression
      :returns: false if failed or cancelled



   .. py:method:: ui_set_lvar_type(v: lvar_t) -> bool

      Set local variable type. This function displays a dialog box and allows the user to change the type of a local variable. 
              
      :param v: pointer to local variable
      :returns: false if failed or cancelled



   .. py:method:: set_lvar_type(v: lvar_t, type: tinfo_t) -> bool

      Set local variable type. This function permanently sets a local variable type and clears NOPTR flag if it was set before by function 'set_noptr_lvar' 
              
      :param v: pointer to local variable
      :param type: new variable type
      :returns: false if failed



   .. py:method:: set_noptr_lvar(v: lvar_t) -> bool

      Inform that local variable should have a non-pointer type This function permanently sets a corresponding variable flag (NOPTR) and removes type if it was set before by function 'set_lvar_type' 
              
      :param v: pointer to local variable
      :returns: false if failed



   .. py:method:: ui_edit_lvar_cmt(v: lvar_t) -> bool

      Set local variable comment. This function displays a dialog box and allows the user to edit the comment of a local variable. 
              
      :param v: pointer to local variable
      :returns: false if failed or cancelled



   .. py:method:: set_lvar_cmt(v: lvar_t, cmt: str) -> bool

      Set local variable comment. This function permanently sets a variable comment. 
              
      :param v: pointer to local variable
      :param cmt: new comment
      :returns: false if failed



   .. py:method:: ui_map_lvar(v: lvar_t) -> bool

      Map a local variable to another. This function displays a variable list and allows the user to select mapping. 
              
      :param v: pointer to local variable
      :returns: false if failed or cancelled



   .. py:method:: ui_unmap_lvar(v: lvar_t) -> bool

      Unmap a local variable. This function displays list of variables mapped to the specified variable and allows the user to select a variable to unmap. 
              
      :param v: pointer to local variable
      :returns: false if failed or cancelled



   .. py:method:: map_lvar(frm: lvar_t, to: lvar_t) -> bool

      Map a local variable to another. This function permanently maps one lvar to another. All occurrences of the mapped variable are replaced by the new variable 
              
      :param to: the variable to map to. if nullptr, unmaps the variable
      :returns: false if failed



   .. py:method:: set_udm_type(udt_type: tinfo_t, udm_idx: int) -> bool

      Set structure field type. This function displays a dialog box and allows the user to change the type of a structure field. 
              
      :param udt_type: structure/union type
      :param udm_idx: index of the structure/union member
      :returns: false if failed or cancelled



   .. py:method:: rename_udm(udt_type: tinfo_t, udm_idx: int) -> bool

      Rename structure field. This function displays a dialog box and allows the user to rename a structure field. 
              
      :param udt_type: structure/union type
      :param udm_idx: index of the structure/union member
      :returns: false if failed or cancelled



   .. py:method:: set_global_type(ea: ida_idaapi.ea_t) -> bool

      Set global item type. This function displays a dialog box and allows the user to change the type of a global item (data or function). 
              
      :param ea: address of the global item
      :returns: false if failed or cancelled



   .. py:method:: rename_global(ea: ida_idaapi.ea_t) -> bool

      Rename global item. This function displays a dialog box and allows the user to rename a global item (data or function). 
              
      :param ea: address of the global item
      :returns: false if failed or cancelled



   .. py:method:: rename_label(label: int) -> bool

      Rename a label. This function displays a dialog box and allows the user to rename a statement label. 
              
      :param label: label number
      :returns: false if failed or cancelled



   .. py:method:: jump_enter(idv: input_device_t, omflags: int) -> bool

      Process the Enter key. This function jumps to the definition of the item under the cursor. If the current item is a function, it will be decompiled. If the current item is a global data, its disassemly text will be displayed. 
              
      :param idv: what cursor must be used, the keyboard or the mouse
      :param omflags: OM_NEWWIN: new pseudocode window will open, 0: reuse the existing window
      :returns: false if failed



   .. py:method:: ctree_to_disasm() -> bool

      Jump to disassembly. This function jumps to the address in the disassembly window which corresponds to the current item. The current item is determined based on the current keyboard cursor position. 
              
      :returns: false if failed



   .. py:method:: calc_cmt_type(lnnum: size_t, cmttype: cmt_type_t) -> cmt_type_t

      Check if the specified line can have a comment. Due to the coordinate system for comments: ([https://hex-rays.com/blog/coordinate-system-for-hex-rays](https://hex-rays.com/blog/coordinate-system-for-hex-rays)) some function lines cannot have comments. This function checks if a comment can be attached to the specified line. 
              
      :param lnnum: line number (0 based)
      :param cmttype: comment types to check
      :returns: possible comment types



   .. py:method:: edit_cmt(loc: treeloc_t) -> bool

      Edit an indented comment. This function displays a dialog box and allows the user to edit the comment for the specified ctree location. 
              
      :param loc: comment location
      :returns: false if failed or cancelled



   .. py:method:: edit_func_cmt() -> bool

      Edit a function comment. This function displays a dialog box and allows the user to edit the function comment. 
              
      :returns: false if failed or cancelled



   .. py:method:: del_orphan_cmts() -> bool

      Delete all orphan comments. Delete all orphan comments and refresh the screen. 
              
      :returns: true



   .. py:method:: set_num_radix(base: int) -> bool

      Change number base. This function changes the current number representation. 
              
      :param base: number radix (10 or 16)
       0 means a character constant
      :returns: false if failed



   .. py:method:: set_num_enum() -> bool

      Convert number to symbolic constant. This function displays a dialog box and allows the user to select a symbolic constant to represent the number. 
              
      :returns: false if failed or cancelled



   .. py:method:: set_num_stroff() -> bool

      Convert number to structure field offset. Currently not implemented. 
              
      :returns: false if failed or cancelled



   .. py:method:: invert_sign() -> bool

      Negate a number. This function negates the current number. 
              
      :returns: false if failed.



   .. py:method:: invert_bits() -> bool

      Bitwise negate a number. This function inverts all bits of the current number. 
              
      :returns: false if failed.



   .. py:method:: collapse_item(hide: bool) -> bool

      Collapse/uncollapse item. This function collapses the current item. 
              
      :returns: false if failed.



   .. py:method:: collapse_lvars(hide: bool) -> bool

      Collapse/uncollapse local variable declarations. 
              
      :returns: false if failed.



   .. py:method:: split_item(split: bool) -> bool

      Split/unsplit item. This function splits the current assignment expression. 
              
      :returns: false if failed.



.. py:data:: CMT_NONE

   No comment is possible.


.. py:data:: CMT_TAIL

   Indented comment.


.. py:data:: CMT_BLOCK1

   Anterioir block comment.


.. py:data:: CMT_BLOCK2

   Posterior block comment.


.. py:data:: CMT_LVAR

   Local variable comment.


.. py:data:: CMT_FUNC

   Function comment.


.. py:data:: CMT_ALL

   All comments.


.. py:data:: VDUI_VISIBLE

   is visible?


.. py:data:: VDUI_VALID

   is valid?


.. py:class:: ui_stroff_op_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: text
      :type:  str

      any text for the column "Operand" of widget



   .. py:attribute:: offset
      :type:  int

      operand offset, will be used when calculating the UDT path



.. py:class:: ui_stroff_applicator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: apply(opnum: size_t, path: intvec_t, top_tif: tinfo_t, spath: str) -> bool

      :param opnum: operand ordinal number, see below
      :param path: path describing the union selection, maybe empty
      :param top_tif: tinfo_t of the selected toplevel UDT
      :param spath: selected path



.. py:function:: select_udt_by_offset(udts: qvector< tinfo_t > const *, ops: ui_stroff_ops_t, applicator: ui_stroff_applicator_t) -> int

   Select UDT 
           
   :param udts: list of UDT tinfo_t for the selection, if nullptr or empty then UDTs from the "Local types" will be used
   :param ops: operands
   :param applicator: callback will be called to apply the selection for every operand


.. py:data:: hx_user_numforms_begin

.. py:data:: hx_user_numforms_end

.. py:data:: hx_user_numforms_next

.. py:data:: hx_user_numforms_prev

.. py:data:: hx_user_numforms_first

.. py:data:: hx_user_numforms_second

.. py:data:: hx_user_numforms_find

.. py:data:: hx_user_numforms_insert

.. py:data:: hx_user_numforms_erase

.. py:data:: hx_user_numforms_clear

.. py:data:: hx_user_numforms_size

.. py:data:: hx_user_numforms_free

.. py:data:: hx_user_numforms_new

.. py:data:: hx_lvar_mapping_begin

.. py:data:: hx_lvar_mapping_end

.. py:data:: hx_lvar_mapping_next

.. py:data:: hx_lvar_mapping_prev

.. py:data:: hx_lvar_mapping_first

.. py:data:: hx_lvar_mapping_second

.. py:data:: hx_lvar_mapping_find

.. py:data:: hx_lvar_mapping_insert

.. py:data:: hx_lvar_mapping_erase

.. py:data:: hx_lvar_mapping_clear

.. py:data:: hx_lvar_mapping_size

.. py:data:: hx_lvar_mapping_free

.. py:data:: hx_lvar_mapping_new

.. py:data:: hx_udcall_map_begin

.. py:data:: hx_udcall_map_end

.. py:data:: hx_udcall_map_next

.. py:data:: hx_udcall_map_prev

.. py:data:: hx_udcall_map_first

.. py:data:: hx_udcall_map_second

.. py:data:: hx_udcall_map_find

.. py:data:: hx_udcall_map_insert

.. py:data:: hx_udcall_map_erase

.. py:data:: hx_udcall_map_clear

.. py:data:: hx_udcall_map_size

.. py:data:: hx_udcall_map_free

.. py:data:: hx_udcall_map_new

.. py:data:: hx_user_cmts_begin

.. py:data:: hx_user_cmts_end

.. py:data:: hx_user_cmts_next

.. py:data:: hx_user_cmts_prev

.. py:data:: hx_user_cmts_first

.. py:data:: hx_user_cmts_second

.. py:data:: hx_user_cmts_find

.. py:data:: hx_user_cmts_insert

.. py:data:: hx_user_cmts_erase

.. py:data:: hx_user_cmts_clear

.. py:data:: hx_user_cmts_size

.. py:data:: hx_user_cmts_free

.. py:data:: hx_user_cmts_new

.. py:data:: hx_user_iflags_begin

.. py:data:: hx_user_iflags_end

.. py:data:: hx_user_iflags_next

.. py:data:: hx_user_iflags_prev

.. py:data:: hx_user_iflags_first

.. py:data:: hx_user_iflags_second

.. py:data:: hx_user_iflags_find

.. py:data:: hx_user_iflags_insert

.. py:data:: hx_user_iflags_erase

.. py:data:: hx_user_iflags_clear

.. py:data:: hx_user_iflags_size

.. py:data:: hx_user_iflags_free

.. py:data:: hx_user_iflags_new

.. py:data:: hx_user_unions_begin

.. py:data:: hx_user_unions_end

.. py:data:: hx_user_unions_next

.. py:data:: hx_user_unions_prev

.. py:data:: hx_user_unions_first

.. py:data:: hx_user_unions_second

.. py:data:: hx_user_unions_find

.. py:data:: hx_user_unions_insert

.. py:data:: hx_user_unions_erase

.. py:data:: hx_user_unions_clear

.. py:data:: hx_user_unions_size

.. py:data:: hx_user_unions_free

.. py:data:: hx_user_unions_new

.. py:data:: hx_user_labels_begin

.. py:data:: hx_user_labels_end

.. py:data:: hx_user_labels_next

.. py:data:: hx_user_labels_prev

.. py:data:: hx_user_labels_first

.. py:data:: hx_user_labels_second

.. py:data:: hx_user_labels_find

.. py:data:: hx_user_labels_insert

.. py:data:: hx_user_labels_erase

.. py:data:: hx_user_labels_clear

.. py:data:: hx_user_labels_size

.. py:data:: hx_user_labels_free

.. py:data:: hx_user_labels_new

.. py:data:: hx_eamap_begin

.. py:data:: hx_eamap_end

.. py:data:: hx_eamap_next

.. py:data:: hx_eamap_prev

.. py:data:: hx_eamap_first

.. py:data:: hx_eamap_second

.. py:data:: hx_eamap_find

.. py:data:: hx_eamap_insert

.. py:data:: hx_eamap_erase

.. py:data:: hx_eamap_clear

.. py:data:: hx_eamap_size

.. py:data:: hx_eamap_free

.. py:data:: hx_eamap_new

.. py:data:: hx_boundaries_begin

.. py:data:: hx_boundaries_end

.. py:data:: hx_boundaries_next

.. py:data:: hx_boundaries_prev

.. py:data:: hx_boundaries_first

.. py:data:: hx_boundaries_second

.. py:data:: hx_boundaries_find

.. py:data:: hx_boundaries_insert

.. py:data:: hx_boundaries_erase

.. py:data:: hx_boundaries_clear

.. py:data:: hx_boundaries_size

.. py:data:: hx_boundaries_free

.. py:data:: hx_boundaries_new

.. py:data:: hx_block_chains_begin

.. py:data:: hx_block_chains_end

.. py:data:: hx_block_chains_next

.. py:data:: hx_block_chains_prev

.. py:data:: hx_block_chains_get

.. py:data:: hx_block_chains_find

.. py:data:: hx_block_chains_insert

.. py:data:: hx_block_chains_erase

.. py:data:: hx_block_chains_clear

.. py:data:: hx_block_chains_size

.. py:data:: hx_block_chains_free

.. py:data:: hx_block_chains_new

.. py:data:: hx_hexrays_alloc

.. py:data:: hx_hexrays_free

.. py:data:: hx_valrng_t_clear

.. py:data:: hx_valrng_t_copy

.. py:data:: hx_valrng_t_assign

.. py:data:: hx_valrng_t_compare

.. py:data:: hx_valrng_t_set_eq

.. py:data:: hx_valrng_t_set_cmp

.. py:data:: hx_valrng_t_reduce_size

.. py:data:: hx_valrng_t_intersect_with

.. py:data:: hx_valrng_t_unite_with

.. py:data:: hx_valrng_t_inverse

.. py:data:: hx_valrng_t_has

.. py:data:: hx_valrng_t_print

.. py:data:: hx_valrng_t_dstr

.. py:data:: hx_valrng_t_cvt_to_single_value

.. py:data:: hx_valrng_t_cvt_to_cmp

.. py:data:: hx_get_merror_desc

.. py:data:: hx_must_mcode_close_block

.. py:data:: hx_is_mcode_propagatable

.. py:data:: hx_negate_mcode_relation

.. py:data:: hx_swap_mcode_relation

.. py:data:: hx_get_signed_mcode

.. py:data:: hx_get_unsigned_mcode

.. py:data:: hx_mcode_modifies_d

.. py:data:: hx_operand_locator_t_compare

.. py:data:: hx_vd_printer_t_print

.. py:data:: hx_file_printer_t_print

.. py:data:: hx_qstring_printer_t_print

.. py:data:: hx_dstr

.. py:data:: hx_is_type_correct

.. py:data:: hx_is_small_udt

.. py:data:: hx_is_nonbool_type

.. py:data:: hx_is_bool_type

.. py:data:: hx_partial_type_num

.. py:data:: hx_get_float_type

.. py:data:: hx_get_int_type_by_width_and_sign

.. py:data:: hx_get_unk_type

.. py:data:: hx_dummy_ptrtype

.. py:data:: hx_get_member_type

.. py:data:: hx_make_pointer

.. py:data:: hx_create_typedef

.. py:data:: hx_get_type

.. py:data:: hx_set_type

.. py:data:: hx_vdloc_t_dstr

.. py:data:: hx_vdloc_t_compare

.. py:data:: hx_vdloc_t_is_aliasable

.. py:data:: hx_print_vdloc

.. py:data:: hx_arglocs_overlap

.. py:data:: hx_lvar_locator_t_compare

.. py:data:: hx_lvar_locator_t_dstr

.. py:data:: hx_lvar_t_dstr

.. py:data:: hx_lvar_t_is_promoted_arg

.. py:data:: hx_lvar_t_accepts_type

.. py:data:: hx_lvar_t_set_lvar_type

.. py:data:: hx_lvar_t_set_width

.. py:data:: hx_lvar_t_append_list

.. py:data:: hx_lvar_t_append_list_

.. py:data:: hx_lvars_t_find_stkvar

.. py:data:: hx_lvars_t_find

.. py:data:: hx_lvars_t_find_lvar

.. py:data:: hx_restore_user_lvar_settings

.. py:data:: hx_save_user_lvar_settings

.. py:data:: hx_modify_user_lvars

.. py:data:: hx_modify_user_lvar_info

.. py:data:: hx_locate_lvar

.. py:data:: hx_restore_user_defined_calls

.. py:data:: hx_save_user_defined_calls

.. py:data:: hx_parse_user_call

.. py:data:: hx_convert_to_user_call

.. py:data:: hx_install_microcode_filter

.. py:data:: hx_udc_filter_t_cleanup

.. py:data:: hx_udc_filter_t_init

.. py:data:: hx_udc_filter_t_apply

.. py:data:: hx_bitset_t_bitset_t

.. py:data:: hx_bitset_t_copy

.. py:data:: hx_bitset_t_add

.. py:data:: hx_bitset_t_add_

.. py:data:: hx_bitset_t_add__

.. py:data:: hx_bitset_t_sub

.. py:data:: hx_bitset_t_sub_

.. py:data:: hx_bitset_t_sub__

.. py:data:: hx_bitset_t_cut_at

.. py:data:: hx_bitset_t_shift_down

.. py:data:: hx_bitset_t_has

.. py:data:: hx_bitset_t_has_all

.. py:data:: hx_bitset_t_has_any

.. py:data:: hx_bitset_t_dstr

.. py:data:: hx_bitset_t_empty

.. py:data:: hx_bitset_t_count

.. py:data:: hx_bitset_t_count_

.. py:data:: hx_bitset_t_last

.. py:data:: hx_bitset_t_fill_with_ones

.. py:data:: hx_bitset_t_fill_gaps

.. py:data:: hx_bitset_t_has_common

.. py:data:: hx_bitset_t_intersect

.. py:data:: hx_bitset_t_is_subset_of

.. py:data:: hx_bitset_t_compare

.. py:data:: hx_bitset_t_goup

.. py:data:: hx_ivl_t_dstr

.. py:data:: hx_ivl_t_compare

.. py:data:: hx_ivlset_t_add

.. py:data:: hx_ivlset_t_add_

.. py:data:: hx_ivlset_t_addmasked

.. py:data:: hx_ivlset_t_sub

.. py:data:: hx_ivlset_t_sub_

.. py:data:: hx_ivlset_t_has_common

.. py:data:: hx_ivlset_t_print

.. py:data:: hx_ivlset_t_dstr

.. py:data:: hx_ivlset_t_count

.. py:data:: hx_ivlset_t_has_common_

.. py:data:: hx_ivlset_t_contains

.. py:data:: hx_ivlset_t_includes

.. py:data:: hx_ivlset_t_intersect

.. py:data:: hx_ivlset_t_compare

.. py:data:: hx_rlist_t_print

.. py:data:: hx_rlist_t_dstr

.. py:data:: hx_mlist_t_addmem

.. py:data:: hx_mlist_t_print

.. py:data:: hx_mlist_t_dstr

.. py:data:: hx_mlist_t_compare

.. py:data:: hx_get_temp_regs

.. py:data:: hx_is_kreg

.. py:data:: hx_reg2mreg

.. py:data:: hx_mreg2reg

.. py:data:: hx_get_mreg_name

.. py:data:: hx_install_optinsn_handler

.. py:data:: hx_remove_optinsn_handler

.. py:data:: hx_install_optblock_handler

.. py:data:: hx_remove_optblock_handler

.. py:data:: hx_simple_graph_t_compute_dominators

.. py:data:: hx_simple_graph_t_compute_immediate_dominators

.. py:data:: hx_simple_graph_t_depth_first_preorder

.. py:data:: hx_simple_graph_t_depth_first_postorder

.. py:data:: hx_simple_graph_t_goup

.. py:data:: hx_mutable_graph_t_resize

.. py:data:: hx_mutable_graph_t_goup

.. py:data:: hx_mutable_graph_t_del_edge

.. py:data:: hx_lvar_ref_t_compare

.. py:data:: hx_lvar_ref_t_var

.. py:data:: hx_stkvar_ref_t_compare

.. py:data:: hx_stkvar_ref_t_get_stkvar

.. py:data:: hx_fnumber_t_print

.. py:data:: hx_fnumber_t_dstr

.. py:data:: hx_mop_t_copy

.. py:data:: hx_mop_t_assign

.. py:data:: hx_mop_t_swap

.. py:data:: hx_mop_t_erase

.. py:data:: hx_mop_t_print

.. py:data:: hx_mop_t_dstr

.. py:data:: hx_mop_t_create_from_mlist

.. py:data:: hx_mop_t_create_from_ivlset

.. py:data:: hx_mop_t_create_from_vdloc

.. py:data:: hx_mop_t_create_from_scattered_vdloc

.. py:data:: hx_mop_t_create_from_insn

.. py:data:: hx_mop_t_make_number

.. py:data:: hx_mop_t_make_fpnum

.. py:data:: hx_mop_t__make_gvar

.. py:data:: hx_mop_t_make_gvar

.. py:data:: hx_mop_t_make_reg_pair

.. py:data:: hx_mop_t_make_helper

.. py:data:: hx_mop_t_is_bit_reg

.. py:data:: hx_mop_t_may_use_aliased_memory

.. py:data:: hx_mop_t_is01

.. py:data:: hx_mop_t_is_sign_extended_from

.. py:data:: hx_mop_t_is_zero_extended_from

.. py:data:: hx_mop_t_equal_mops

.. py:data:: hx_mop_t_lexcompare

.. py:data:: hx_mop_t_for_all_ops

.. py:data:: hx_mop_t_for_all_scattered_submops

.. py:data:: hx_mop_t_is_constant

.. py:data:: hx_mop_t_get_stkoff

.. py:data:: hx_mop_t_make_low_half

.. py:data:: hx_mop_t_make_high_half

.. py:data:: hx_mop_t_make_first_half

.. py:data:: hx_mop_t_make_second_half

.. py:data:: hx_mop_t_shift_mop

.. py:data:: hx_mop_t_change_size

.. py:data:: hx_mop_t_preserve_side_effects

.. py:data:: hx_mop_t_apply_ld_mcode

.. py:data:: hx_mcallarg_t_print

.. py:data:: hx_mcallarg_t_dstr

.. py:data:: hx_mcallarg_t_set_regarg

.. py:data:: hx_mcallinfo_t_lexcompare

.. py:data:: hx_mcallinfo_t_set_type

.. py:data:: hx_mcallinfo_t_get_type

.. py:data:: hx_mcallinfo_t_print

.. py:data:: hx_mcallinfo_t_dstr

.. py:data:: hx_mcases_t_compare

.. py:data:: hx_mcases_t_print

.. py:data:: hx_mcases_t_dstr

.. py:data:: hx_vivl_t_extend_to_cover

.. py:data:: hx_vivl_t_intersect

.. py:data:: hx_vivl_t_print

.. py:data:: hx_vivl_t_dstr

.. py:data:: hx_chain_t_print

.. py:data:: hx_chain_t_dstr

.. py:data:: hx_chain_t_append_list

.. py:data:: hx_chain_t_append_list_

.. py:data:: hx_block_chains_t_get_chain

.. py:data:: hx_block_chains_t_print

.. py:data:: hx_block_chains_t_dstr

.. py:data:: hx_graph_chains_t_for_all_chains

.. py:data:: hx_graph_chains_t_release

.. py:data:: hx_minsn_t_init

.. py:data:: hx_minsn_t_copy

.. py:data:: hx_minsn_t_set_combined

.. py:data:: hx_minsn_t_swap

.. py:data:: hx_minsn_t_print

.. py:data:: hx_minsn_t_dstr

.. py:data:: hx_minsn_t_setaddr

.. py:data:: hx_minsn_t_optimize_subtree

.. py:data:: hx_minsn_t_for_all_ops

.. py:data:: hx_minsn_t_for_all_insns

.. py:data:: hx_minsn_t__make_nop

.. py:data:: hx_minsn_t_equal_insns

.. py:data:: hx_minsn_t_lexcompare

.. py:data:: hx_minsn_t_is_noret_call

.. py:data:: hx_minsn_t_is_helper

.. py:data:: hx_minsn_t_find_call

.. py:data:: hx_minsn_t_has_side_effects

.. py:data:: hx_minsn_t_find_opcode

.. py:data:: hx_minsn_t_find_ins_op

.. py:data:: hx_minsn_t_find_num_op

.. py:data:: hx_minsn_t_modifies_d

.. py:data:: hx_minsn_t_is_between

.. py:data:: hx_minsn_t_may_use_aliased_memory

.. py:data:: hx_minsn_t_serialize

.. py:data:: hx_minsn_t_deserialize

.. py:data:: hx_getf_reginsn

.. py:data:: hx_getb_reginsn

.. py:data:: hx_mblock_t_init

.. py:data:: hx_mblock_t_print

.. py:data:: hx_mblock_t_dump

.. py:data:: hx_mblock_t_vdump_block

.. py:data:: hx_mblock_t_insert_into_block

.. py:data:: hx_mblock_t_remove_from_block

.. py:data:: hx_mblock_t_for_all_insns

.. py:data:: hx_mblock_t_for_all_ops

.. py:data:: hx_mblock_t_for_all_uses

.. py:data:: hx_mblock_t_optimize_insn

.. py:data:: hx_mblock_t_optimize_block

.. py:data:: hx_mblock_t_build_lists

.. py:data:: hx_mblock_t_optimize_useless_jump

.. py:data:: hx_mblock_t_append_use_list

.. py:data:: hx_mblock_t_append_def_list

.. py:data:: hx_mblock_t_build_use_list

.. py:data:: hx_mblock_t_build_def_list

.. py:data:: hx_mblock_t_find_first_use

.. py:data:: hx_mblock_t_find_redefinition

.. py:data:: hx_mblock_t_is_rhs_redefined

.. py:data:: hx_mblock_t_find_access

.. py:data:: hx_mblock_t_get_valranges

.. py:data:: hx_mblock_t_get_valranges_

.. py:data:: hx_mblock_t_get_reginsn_qty

.. py:data:: hx_mba_ranges_t_range_contains

.. py:data:: hx_mba_t_stkoff_vd2ida

.. py:data:: hx_mba_t_stkoff_ida2vd

.. py:data:: hx_mba_t_idaloc2vd

.. py:data:: hx_mba_t_idaloc2vd_

.. py:data:: hx_mba_t_vd2idaloc

.. py:data:: hx_mba_t_vd2idaloc_

.. py:data:: hx_mba_t_term

.. py:data:: hx_mba_t_get_curfunc

.. py:data:: hx_mba_t_set_maturity

.. py:data:: hx_mba_t_optimize_local

.. py:data:: hx_mba_t_build_graph

.. py:data:: hx_mba_t_get_graph

.. py:data:: hx_mba_t_analyze_calls

.. py:data:: hx_mba_t_optimize_global

.. py:data:: hx_mba_t_alloc_lvars

.. py:data:: hx_mba_t_dump

.. py:data:: hx_mba_t_vdump_mba

.. py:data:: hx_mba_t_print

.. py:data:: hx_mba_t_verify

.. py:data:: hx_mba_t_mark_chains_dirty

.. py:data:: hx_mba_t_insert_block

.. py:data:: hx_mba_t_remove_block

.. py:data:: hx_mba_t_copy_block

.. py:data:: hx_mba_t_remove_empty_and_unreachable_blocks

.. py:data:: hx_mba_t_merge_blocks

.. py:data:: hx_mba_t_for_all_ops

.. py:data:: hx_mba_t_for_all_insns

.. py:data:: hx_mba_t_for_all_topinsns

.. py:data:: hx_mba_t_find_mop

.. py:data:: hx_mba_t_create_helper_call

.. py:data:: hx_mba_t_get_func_output_lists

.. py:data:: hx_mba_t_arg

.. py:data:: hx_mba_t_alloc_fict_ea

.. py:data:: hx_mba_t_map_fict_ea

.. py:data:: hx_mba_t_serialize

.. py:data:: hx_mba_t_deserialize

.. py:data:: hx_mba_t_save_snapshot

.. py:data:: hx_mba_t_alloc_kreg

.. py:data:: hx_mba_t_free_kreg

.. py:data:: hx_mba_t_inline_func

.. py:data:: hx_mba_t_locate_stkpnt

.. py:data:: hx_mba_t_set_lvar_name

.. py:data:: hx_mbl_graph_t_is_accessed_globally

.. py:data:: hx_mbl_graph_t_get_ud

.. py:data:: hx_mbl_graph_t_get_du

.. py:data:: hx_cdg_insn_iterator_t_next

.. py:data:: hx_codegen_t_clear

.. py:data:: hx_codegen_t_emit

.. py:data:: hx_codegen_t_emit_

.. py:data:: hx_change_hexrays_config

.. py:data:: hx_get_hexrays_version

.. py:data:: hx_open_pseudocode

.. py:data:: hx_close_pseudocode

.. py:data:: hx_get_widget_vdui

.. py:data:: hx_decompile_many

.. py:data:: hx_hexrays_failure_t_desc

.. py:data:: hx_send_database

.. py:data:: hx_gco_info_t_append_to_list

.. py:data:: hx_get_current_operand

.. py:data:: hx_remitem

.. py:data:: hx_negated_relation

.. py:data:: hx_swapped_relation

.. py:data:: hx_get_op_signness

.. py:data:: hx_asgop

.. py:data:: hx_asgop_revert

.. py:data:: hx_cnumber_t_print

.. py:data:: hx_cnumber_t_value

.. py:data:: hx_cnumber_t_assign

.. py:data:: hx_cnumber_t_compare

.. py:data:: hx_var_ref_t_compare

.. py:data:: hx_ctree_visitor_t_apply_to

.. py:data:: hx_ctree_visitor_t_apply_to_exprs

.. py:data:: hx_ctree_parentee_t_recalc_parent_types

.. py:data:: hx_cfunc_parentee_t_calc_rvalue_type

.. py:data:: hx_citem_locator_t_compare

.. py:data:: hx_citem_t_contains_expr

.. py:data:: hx_citem_t_contains_label

.. py:data:: hx_citem_t_find_parent_of

.. py:data:: hx_citem_t_find_closest_addr

.. py:data:: hx_cexpr_t_assign

.. py:data:: hx_cexpr_t_compare

.. py:data:: hx_cexpr_t_replace_by

.. py:data:: hx_cexpr_t_cleanup

.. py:data:: hx_cexpr_t_put_number

.. py:data:: hx_cexpr_t_print1

.. py:data:: hx_cexpr_t_calc_type

.. py:data:: hx_cexpr_t_equal_effect

.. py:data:: hx_cexpr_t_is_child_of

.. py:data:: hx_cexpr_t_contains_operator

.. py:data:: hx_cexpr_t_get_high_nbit_bound

.. py:data:: hx_cexpr_t_get_low_nbit_bound

.. py:data:: hx_cexpr_t_requires_lvalue

.. py:data:: hx_cexpr_t_has_side_effects

.. py:data:: hx_cexpr_t_maybe_ptr

.. py:data:: hx_cexpr_t_dstr

.. py:data:: hx_cif_t_assign

.. py:data:: hx_cif_t_compare

.. py:data:: hx_cloop_t_assign

.. py:data:: hx_cfor_t_compare

.. py:data:: hx_cwhile_t_compare

.. py:data:: hx_cdo_t_compare

.. py:data:: hx_creturn_t_compare

.. py:data:: hx_cthrow_t_compare

.. py:data:: hx_cgoto_t_compare

.. py:data:: hx_casm_t_compare

.. py:data:: hx_cinsn_t_assign

.. py:data:: hx_cinsn_t_compare

.. py:data:: hx_cinsn_t_replace_by

.. py:data:: hx_cinsn_t_cleanup

.. py:data:: hx_cinsn_t_new_insn

.. py:data:: hx_cinsn_t_create_if

.. py:data:: hx_cinsn_t_print

.. py:data:: hx_cinsn_t_print1

.. py:data:: hx_cinsn_t_is_ordinary_flow

.. py:data:: hx_cinsn_t_contains_insn

.. py:data:: hx_cinsn_t_collect_free_breaks

.. py:data:: hx_cinsn_t_collect_free_continues

.. py:data:: hx_cinsn_t_dstr

.. py:data:: hx_cblock_t_compare

.. py:data:: hx_carglist_t_compare

.. py:data:: hx_ccase_t_compare

.. py:data:: hx_ccases_t_compare

.. py:data:: hx_cswitch_t_compare

.. py:data:: hx_ccatch_t_compare

.. py:data:: hx_ctry_t_compare

.. py:data:: hx_ctree_item_t_get_udm

.. py:data:: hx_ctree_item_t_get_edm

.. py:data:: hx_ctree_item_t_get_lvar

.. py:data:: hx_ctree_item_t_get_ea

.. py:data:: hx_ctree_item_t_get_label_num

.. py:data:: hx_ctree_item_t_print

.. py:data:: hx_ctree_item_t_dstr

.. py:data:: hx_lnot

.. py:data:: hx_new_block

.. py:data:: hx_vcreate_helper

.. py:data:: hx_vcall_helper

.. py:data:: hx_make_num

.. py:data:: hx_make_ref

.. py:data:: hx_dereference

.. py:data:: hx_save_user_labels

.. py:data:: hx_save_user_cmts

.. py:data:: hx_save_user_numforms

.. py:data:: hx_save_user_iflags

.. py:data:: hx_save_user_unions

.. py:data:: hx_restore_user_labels

.. py:data:: hx_restore_user_cmts

.. py:data:: hx_restore_user_numforms

.. py:data:: hx_restore_user_iflags

.. py:data:: hx_restore_user_unions

.. py:data:: hx_cfunc_t_build_c_tree

.. py:data:: hx_cfunc_t_verify

.. py:data:: hx_cfunc_t_print_dcl

.. py:data:: hx_cfunc_t_print_func

.. py:data:: hx_cfunc_t_get_func_type

.. py:data:: hx_cfunc_t_get_lvars

.. py:data:: hx_cfunc_t_get_stkoff_delta

.. py:data:: hx_cfunc_t_find_label

.. py:data:: hx_cfunc_t_remove_unused_labels

.. py:data:: hx_cfunc_t_get_user_cmt

.. py:data:: hx_cfunc_t_set_user_cmt

.. py:data:: hx_cfunc_t_get_user_iflags

.. py:data:: hx_cfunc_t_set_user_iflags

.. py:data:: hx_cfunc_t_has_orphan_cmts

.. py:data:: hx_cfunc_t_del_orphan_cmts

.. py:data:: hx_cfunc_t_get_user_union_selection

.. py:data:: hx_cfunc_t_set_user_union_selection

.. py:data:: hx_cfunc_t_save_user_labels

.. py:data:: hx_cfunc_t_save_user_cmts

.. py:data:: hx_cfunc_t_save_user_numforms

.. py:data:: hx_cfunc_t_save_user_iflags

.. py:data:: hx_cfunc_t_save_user_unions

.. py:data:: hx_cfunc_t_get_line_item

.. py:data:: hx_cfunc_t_get_warnings

.. py:data:: hx_cfunc_t_get_eamap

.. py:data:: hx_cfunc_t_get_boundaries

.. py:data:: hx_cfunc_t_get_pseudocode

.. py:data:: hx_cfunc_t_refresh_func_ctext

.. py:data:: hx_cfunc_t_gather_derefs

.. py:data:: hx_cfunc_t_find_item_coords

.. py:data:: hx_cfunc_t_cleanup

.. py:data:: hx_close_hexrays_waitbox

.. py:data:: hx_decompile

.. py:data:: hx_gen_microcode

.. py:data:: hx_create_cfunc

.. py:data:: hx_mark_cfunc_dirty

.. py:data:: hx_clear_cached_cfuncs

.. py:data:: hx_has_cached_cfunc

.. py:data:: hx_get_ctype_name

.. py:data:: hx_create_field_name

.. py:data:: hx_install_hexrays_callback

.. py:data:: hx_remove_hexrays_callback

.. py:data:: hx_vdui_t_set_locked

.. py:data:: hx_vdui_t_refresh_view

.. py:data:: hx_vdui_t_refresh_ctext

.. py:data:: hx_vdui_t_switch_to

.. py:data:: hx_vdui_t_get_number

.. py:data:: hx_vdui_t_get_current_label

.. py:data:: hx_vdui_t_clear

.. py:data:: hx_vdui_t_refresh_cpos

.. py:data:: hx_vdui_t_get_current_item

.. py:data:: hx_vdui_t_ui_rename_lvar

.. py:data:: hx_vdui_t_rename_lvar

.. py:data:: hx_vdui_t_ui_set_call_type

.. py:data:: hx_vdui_t_ui_set_lvar_type

.. py:data:: hx_vdui_t_set_lvar_type

.. py:data:: hx_vdui_t_set_noptr_lvar

.. py:data:: hx_vdui_t_ui_edit_lvar_cmt

.. py:data:: hx_vdui_t_set_lvar_cmt

.. py:data:: hx_vdui_t_ui_map_lvar

.. py:data:: hx_vdui_t_ui_unmap_lvar

.. py:data:: hx_vdui_t_map_lvar

.. py:data:: hx_vdui_t_set_udm_type

.. py:data:: hx_vdui_t_rename_udm

.. py:data:: hx_vdui_t_set_global_type

.. py:data:: hx_vdui_t_rename_global

.. py:data:: hx_vdui_t_rename_label

.. py:data:: hx_vdui_t_jump_enter

.. py:data:: hx_vdui_t_ctree_to_disasm

.. py:data:: hx_vdui_t_calc_cmt_type

.. py:data:: hx_vdui_t_edit_cmt

.. py:data:: hx_vdui_t_edit_func_cmt

.. py:data:: hx_vdui_t_del_orphan_cmts

.. py:data:: hx_vdui_t_set_num_radix

.. py:data:: hx_vdui_t_set_num_enum

.. py:data:: hx_vdui_t_set_num_stroff

.. py:data:: hx_vdui_t_invert_sign

.. py:data:: hx_vdui_t_invert_bits

.. py:data:: hx_vdui_t_collapse_item

.. py:data:: hx_vdui_t_collapse_lvars

.. py:data:: hx_vdui_t_split_item

.. py:data:: hx_select_udt_by_offset

.. py:data:: hx_catchexpr_t_compare

.. py:data:: hx_mba_t_split_block

.. py:data:: hx_mba_t_remove_blocks

.. py:data:: hx_cfunc_t_recalc_item_addresses

.. py:data:: hx_int64_emulator_t_mop_value

.. py:data:: hx_int64_emulator_t_minsn_value

.. py:class:: user_numforms_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  iterator_word


.. py:function:: user_numforms_first(p: user_numforms_iterator_t) -> operand_locator_t const &

   Get reference to the current map key.


.. py:function:: user_numforms_second(p: user_numforms_iterator_t) -> number_format_t &

   Get reference to the current map value.


.. py:function:: user_numforms_find(map: user_numforms_t, key: operand_locator_t) -> user_numforms_iterator_t

   Find the specified key in user_numforms_t.


.. py:function:: user_numforms_insert(map: user_numforms_t, key: operand_locator_t, val: number_format_t) -> user_numforms_iterator_t

   Insert new (operand_locator_t, number_format_t) pair into user_numforms_t.


.. py:function:: user_numforms_begin(map: user_numforms_t) -> user_numforms_iterator_t

   Get iterator pointing to the beginning of user_numforms_t.


.. py:function:: user_numforms_end(map: user_numforms_t) -> user_numforms_iterator_t

   Get iterator pointing to the end of user_numforms_t.


.. py:function:: user_numforms_next(p: user_numforms_iterator_t) -> user_numforms_iterator_t

   Move to the next element.


.. py:function:: user_numforms_prev(p: user_numforms_iterator_t) -> user_numforms_iterator_t

   Move to the previous element.


.. py:function:: user_numforms_erase(map: user_numforms_t, p: user_numforms_iterator_t) -> None

   Erase current element from user_numforms_t.


.. py:function:: user_numforms_clear(map: user_numforms_t) -> None

   Clear user_numforms_t.


.. py:function:: user_numforms_size(map: user_numforms_t) -> size_t

   Get size of user_numforms_t.


.. py:function:: user_numforms_free(map: user_numforms_t) -> None

   Delete user_numforms_t instance.


.. py:function:: user_numforms_new() -> user_numforms_t *

   Create a new user_numforms_t instance.


.. py:class:: lvar_mapping_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  iterator_word


.. py:function:: lvar_mapping_first(p: lvar_mapping_iterator_t) -> lvar_locator_t const &

   Get reference to the current map key.


.. py:function:: lvar_mapping_second(p: lvar_mapping_iterator_t) -> lvar_locator_t &

   Get reference to the current map value.


.. py:function:: lvar_mapping_find(map: lvar_mapping_t, key: lvar_locator_t) -> lvar_mapping_iterator_t

   Find the specified key in lvar_mapping_t.


.. py:function:: lvar_mapping_insert(map: lvar_mapping_t, key: lvar_locator_t, val: lvar_locator_t) -> lvar_mapping_iterator_t

   Insert new (lvar_locator_t, lvar_locator_t) pair into lvar_mapping_t.


.. py:function:: lvar_mapping_begin(map: lvar_mapping_t) -> lvar_mapping_iterator_t

   Get iterator pointing to the beginning of lvar_mapping_t.


.. py:function:: lvar_mapping_end(map: lvar_mapping_t) -> lvar_mapping_iterator_t

   Get iterator pointing to the end of lvar_mapping_t.


.. py:function:: lvar_mapping_next(p: lvar_mapping_iterator_t) -> lvar_mapping_iterator_t

   Move to the next element.


.. py:function:: lvar_mapping_prev(p: lvar_mapping_iterator_t) -> lvar_mapping_iterator_t

   Move to the previous element.


.. py:function:: lvar_mapping_erase(map: lvar_mapping_t, p: lvar_mapping_iterator_t) -> None

   Erase current element from lvar_mapping_t.


.. py:function:: lvar_mapping_clear(map: lvar_mapping_t) -> None

   Clear lvar_mapping_t.


.. py:function:: lvar_mapping_size(map: lvar_mapping_t) -> size_t

   Get size of lvar_mapping_t.


.. py:function:: lvar_mapping_free(map: lvar_mapping_t) -> None

   Delete lvar_mapping_t instance.


.. py:function:: lvar_mapping_new() -> lvar_mapping_t *

   Create a new lvar_mapping_t instance.


.. py:class:: udcall_map_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  iterator_word


.. py:function:: udcall_map_first(p: udcall_map_iterator_t) -> ea_t const &

   Get reference to the current map key.


.. py:function:: udcall_map_second(p: udcall_map_iterator_t) -> udcall_t &

   Get reference to the current map value.


.. py:function:: udcall_map_find(map: udcall_map_t const *, key: ea_t const &) -> udcall_map_iterator_t

   Find the specified key in udcall_map_t.


.. py:function:: udcall_map_insert(map: udcall_map_t *, key: ea_t const &, val: udcall_t) -> udcall_map_iterator_t

   Insert new (ea_t, udcall_t) pair into udcall_map_t.


.. py:function:: udcall_map_begin(map: udcall_map_t const *) -> udcall_map_iterator_t

   Get iterator pointing to the beginning of udcall_map_t.


.. py:function:: udcall_map_end(map: udcall_map_t const *) -> udcall_map_iterator_t

   Get iterator pointing to the end of udcall_map_t.


.. py:function:: udcall_map_next(p: udcall_map_iterator_t) -> udcall_map_iterator_t

   Move to the next element.


.. py:function:: udcall_map_prev(p: udcall_map_iterator_t) -> udcall_map_iterator_t

   Move to the previous element.


.. py:function:: udcall_map_erase(map: udcall_map_t *, p: udcall_map_iterator_t) -> None

   Erase current element from udcall_map_t.


.. py:function:: udcall_map_clear(map: udcall_map_t *) -> None

   Clear udcall_map_t.


.. py:function:: udcall_map_size(map: udcall_map_t *) -> size_t

   Get size of udcall_map_t.


.. py:function:: udcall_map_free(map: udcall_map_t *) -> None

   Delete udcall_map_t instance.


.. py:function:: udcall_map_new() -> udcall_map_t *

   Create a new udcall_map_t instance.


.. py:class:: user_cmts_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  iterator_word


.. py:function:: user_cmts_first(p: user_cmts_iterator_t) -> treeloc_t const &

   Get reference to the current map key.


.. py:function:: user_cmts_second(p: user_cmts_iterator_t) -> citem_cmt_t &

   Get reference to the current map value.


.. py:function:: user_cmts_find(map: user_cmts_t, key: treeloc_t) -> user_cmts_iterator_t

   Find the specified key in user_cmts_t.


.. py:function:: user_cmts_insert(map: user_cmts_t, key: treeloc_t, val: citem_cmt_t) -> user_cmts_iterator_t

   Insert new (treeloc_t, citem_cmt_t) pair into user_cmts_t.


.. py:function:: user_cmts_begin(map: user_cmts_t) -> user_cmts_iterator_t

   Get iterator pointing to the beginning of user_cmts_t.


.. py:function:: user_cmts_end(map: user_cmts_t) -> user_cmts_iterator_t

   Get iterator pointing to the end of user_cmts_t.


.. py:function:: user_cmts_next(p: user_cmts_iterator_t) -> user_cmts_iterator_t

   Move to the next element.


.. py:function:: user_cmts_prev(p: user_cmts_iterator_t) -> user_cmts_iterator_t

   Move to the previous element.


.. py:function:: user_cmts_erase(map: user_cmts_t, p: user_cmts_iterator_t) -> None

   Erase current element from user_cmts_t.


.. py:function:: user_cmts_clear(map: user_cmts_t) -> None

   Clear user_cmts_t.


.. py:function:: user_cmts_size(map: user_cmts_t) -> size_t

   Get size of user_cmts_t.


.. py:function:: user_cmts_free(map: user_cmts_t) -> None

   Delete user_cmts_t instance.


.. py:function:: user_cmts_new() -> user_cmts_t *

   Create a new user_cmts_t instance.


.. py:class:: user_iflags_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  iterator_word


.. py:function:: user_iflags_first(p: user_iflags_iterator_t) -> citem_locator_t const &

   Get reference to the current map key.


.. py:function:: user_iflags_find(map: user_iflags_t, key: citem_locator_t) -> user_iflags_iterator_t

   Find the specified key in user_iflags_t.


.. py:function:: user_iflags_insert(map: user_iflags_t, key: citem_locator_t, val: int32 const &) -> user_iflags_iterator_t

   Insert new (citem_locator_t, int32) pair into user_iflags_t.


.. py:function:: user_iflags_begin(map: user_iflags_t) -> user_iflags_iterator_t

   Get iterator pointing to the beginning of user_iflags_t.


.. py:function:: user_iflags_end(map: user_iflags_t) -> user_iflags_iterator_t

   Get iterator pointing to the end of user_iflags_t.


.. py:function:: user_iflags_next(p: user_iflags_iterator_t) -> user_iflags_iterator_t

   Move to the next element.


.. py:function:: user_iflags_prev(p: user_iflags_iterator_t) -> user_iflags_iterator_t

   Move to the previous element.


.. py:function:: user_iflags_erase(map: user_iflags_t, p: user_iflags_iterator_t) -> None

   Erase current element from user_iflags_t.


.. py:function:: user_iflags_clear(map: user_iflags_t) -> None

   Clear user_iflags_t.


.. py:function:: user_iflags_size(map: user_iflags_t) -> size_t

   Get size of user_iflags_t.


.. py:function:: user_iflags_free(map: user_iflags_t) -> None

   Delete user_iflags_t instance.


.. py:function:: user_iflags_new() -> user_iflags_t *

   Create a new user_iflags_t instance.


.. py:class:: user_unions_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  iterator_word


.. py:function:: user_unions_first(p: user_unions_iterator_t) -> ea_t const &

   Get reference to the current map key.


.. py:function:: user_unions_second(p: user_unions_iterator_t) -> intvec_t &

   Get reference to the current map value.


.. py:function:: user_unions_find(map: user_unions_t, key: ea_t const &) -> user_unions_iterator_t

   Find the specified key in user_unions_t.


.. py:function:: user_unions_insert(map: user_unions_t, key: ea_t const &, val: intvec_t) -> user_unions_iterator_t

   Insert new (ea_t, intvec_t) pair into user_unions_t.


.. py:function:: user_unions_begin(map: user_unions_t) -> user_unions_iterator_t

   Get iterator pointing to the beginning of user_unions_t.


.. py:function:: user_unions_end(map: user_unions_t) -> user_unions_iterator_t

   Get iterator pointing to the end of user_unions_t.


.. py:function:: user_unions_next(p: user_unions_iterator_t) -> user_unions_iterator_t

   Move to the next element.


.. py:function:: user_unions_prev(p: user_unions_iterator_t) -> user_unions_iterator_t

   Move to the previous element.


.. py:function:: user_unions_erase(map: user_unions_t, p: user_unions_iterator_t) -> None

   Erase current element from user_unions_t.


.. py:function:: user_unions_clear(map: user_unions_t) -> None

   Clear user_unions_t.


.. py:function:: user_unions_size(map: user_unions_t) -> size_t

   Get size of user_unions_t.


.. py:function:: user_unions_free(map: user_unions_t) -> None

   Delete user_unions_t instance.


.. py:function:: user_unions_new() -> user_unions_t *

   Create a new user_unions_t instance.


.. py:class:: user_labels_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  iterator_word


.. py:function:: user_labels_first(p: user_labels_iterator_t) -> int const &

   Get reference to the current map key.


.. py:function:: user_labels_second(p: user_labels_iterator_t) -> str

   Get reference to the current map value.


.. py:function:: user_labels_find(map: user_labels_t, key: int const &) -> user_labels_iterator_t

   Find the specified key in user_labels_t.


.. py:function:: user_labels_insert(map: user_labels_t, key: int const &, val: str) -> user_labels_iterator_t

   Insert new (int, qstring) pair into user_labels_t.


.. py:function:: user_labels_begin(map: user_labels_t) -> user_labels_iterator_t

   Get iterator pointing to the beginning of user_labels_t.


.. py:function:: user_labels_end(map: user_labels_t) -> user_labels_iterator_t

   Get iterator pointing to the end of user_labels_t.


.. py:function:: user_labels_next(p: user_labels_iterator_t) -> user_labels_iterator_t

   Move to the next element.


.. py:function:: user_labels_prev(p: user_labels_iterator_t) -> user_labels_iterator_t

   Move to the previous element.


.. py:function:: user_labels_erase(map: user_labels_t, p: user_labels_iterator_t) -> None

   Erase current element from user_labels_t.


.. py:function:: user_labels_clear(map: user_labels_t) -> None

   Clear user_labels_t.


.. py:function:: user_labels_size(map: user_labels_t) -> size_t

   Get size of user_labels_t.


.. py:function:: user_labels_free(map: user_labels_t) -> None

   Delete user_labels_t instance.


.. py:function:: user_labels_new() -> user_labels_t *

   Create a new user_labels_t instance.


.. py:class:: eamap_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  iterator_word


.. py:function:: eamap_first(p: eamap_iterator_t) -> ea_t const &

   Get reference to the current map key.


.. py:function:: eamap_second(p: eamap_iterator_t) -> cinsnptrvec_t &

   Get reference to the current map value.


.. py:function:: eamap_find(map: eamap_t, key: ea_t const &) -> eamap_iterator_t

   Find the specified key in eamap_t.


.. py:function:: eamap_insert(map: eamap_t, key: ea_t const &, val: cinsnptrvec_t) -> eamap_iterator_t

   Insert new (ea_t, cinsnptrvec_t) pair into eamap_t.


.. py:function:: eamap_begin(map: eamap_t) -> eamap_iterator_t

   Get iterator pointing to the beginning of eamap_t.


.. py:function:: eamap_end(map: eamap_t) -> eamap_iterator_t

   Get iterator pointing to the end of eamap_t.


.. py:function:: eamap_next(p: eamap_iterator_t) -> eamap_iterator_t

   Move to the next element.


.. py:function:: eamap_prev(p: eamap_iterator_t) -> eamap_iterator_t

   Move to the previous element.


.. py:function:: eamap_erase(map: eamap_t, p: eamap_iterator_t) -> None

   Erase current element from eamap_t.


.. py:function:: eamap_clear(map: eamap_t) -> None

   Clear eamap_t.


.. py:function:: eamap_size(map: eamap_t) -> size_t

   Get size of eamap_t.


.. py:function:: eamap_free(map: eamap_t) -> None

   Delete eamap_t instance.


.. py:function:: eamap_new() -> eamap_t *

   Create a new eamap_t instance.


.. py:class:: boundaries_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  iterator_word


.. py:function:: boundaries_first(p: boundaries_iterator_t) -> cinsn_t *const &

   Get reference to the current map key.


.. py:function:: boundaries_second(p: boundaries_iterator_t) -> rangeset_t &

   Get reference to the current map value.


.. py:function:: boundaries_begin(map: boundaries_t) -> boundaries_iterator_t

   Get iterator pointing to the beginning of boundaries_t.


.. py:function:: boundaries_end(map: boundaries_t) -> boundaries_iterator_t

   Get iterator pointing to the end of boundaries_t.


.. py:function:: boundaries_next(p: boundaries_iterator_t) -> boundaries_iterator_t

   Move to the next element.


.. py:function:: boundaries_prev(p: boundaries_iterator_t) -> boundaries_iterator_t

   Move to the previous element.


.. py:function:: boundaries_erase(map: boundaries_t, p: boundaries_iterator_t) -> None

   Erase current element from boundaries_t.


.. py:function:: boundaries_clear(map: boundaries_t) -> None

   Clear boundaries_t.


.. py:function:: boundaries_size(map: boundaries_t) -> size_t

   Get size of boundaries_t.


.. py:function:: boundaries_free(map: boundaries_t) -> None

   Delete boundaries_t instance.


.. py:function:: boundaries_new() -> boundaries_t *

   Create a new boundaries_t instance.


.. py:class:: block_chains_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  iterator_word


.. py:function:: block_chains_get(p: block_chains_iterator_t) -> chain_t &

   Get reference to the current set value.


.. py:function:: block_chains_find(set: block_chains_t, val: chain_t) -> block_chains_iterator_t

   Find the specified key in set block_chains_t.


.. py:function:: block_chains_insert(set: block_chains_t, val: chain_t) -> block_chains_iterator_t

   Insert new (chain_t) into set block_chains_t.


.. py:function:: block_chains_begin(set: block_chains_t) -> block_chains_iterator_t

   Get iterator pointing to the beginning of block_chains_t.


.. py:function:: block_chains_end(set: block_chains_t) -> block_chains_iterator_t

   Get iterator pointing to the end of block_chains_t.


.. py:function:: block_chains_next(p: block_chains_iterator_t) -> block_chains_iterator_t

   Move to the next element.


.. py:function:: block_chains_prev(p: block_chains_iterator_t) -> block_chains_iterator_t

   Move to the previous element.


.. py:function:: block_chains_erase(set: block_chains_t, p: block_chains_iterator_t) -> None

   Erase current element from block_chains_t.


.. py:function:: block_chains_clear(set: block_chains_t) -> None

   Clear block_chains_t.


.. py:function:: block_chains_size(set: block_chains_t) -> size_t

   Get size of block_chains_t.


.. py:function:: block_chains_free(set: block_chains_t) -> None

   Delete block_chains_t instance.


.. py:function:: block_chains_new() -> block_chains_t *

   Create a new block_chains_t instance.


.. py:data:: is_allowed_on_small_struni

.. py:data:: is_small_struni

.. py:data:: mbl_array_t

.. py:exception:: DecompilationFailure

   Bases: :py:obj:`Exception`


   Common base class for all non-exit exceptions.


.. py:function:: decompile(ea, hf=None, flags=0)

   Decompile a snippet or a function. 
           
   :param hf: extended error information (if failed)
   :returns: pointer to the decompilation result (a reference counted pointer). nullptr if failed.


.. py:function:: citem_to_specific_type(self)

   cast the citem_t object to its more specific type, either cexpr_t or cinsn_t. 


.. py:function:: property_op_to_typename(self)

.. py:function:: cexpr_operands(self)

   return a dictionary with the operands of a cexpr_t. 


.. py:function:: cinsn_details(self)

   return the details pointer for the cinsn_t object depending on the value of its op member.     this is one of the cblock_t, cif_t, etc. objects.


.. py:function:: cfunc_type(self)

   Get the function's return type tinfo_t object. 


.. py:function:: lnot(e)

   Logically negate the specified expression. The specified expression will be logically negated. For example, "x == y" is converted into "x != y" by this function. 
           
   :param e: expression to negate. After the call, e must not be used anymore because it can be changed by the function. The function return value must be used to refer to the expression.
   :returns: logically negated expression.


.. py:function:: make_ref(e)

   Create a reference. This function performs the following conversion: "obj" => "&obj". It can handle casts, annihilate "&*", and process other special cases. 
           


.. py:function:: dereference(e, ptrsize, is_float=False)

   Dereference a pointer. This function dereferences a pointer expression. It performs the following conversion: "ptr" => "*ptr" It can handle discrepancies in the pointer type and the access size. 
           
   :param e: expression to deference
   :param ptrsize: access size
   :returns: dereferenced expression


.. py:function:: call_helper(rettype, args, *rest)

   Create a helper call.


.. py:function:: new_block()

   Create a new block-statement.


.. py:function:: make_num(*args)

   Create a number expression 
           
   :param n: value
   :param func: current function
   :param ea: definition address of the number
   :param opnum: operand number of the number (in the disassembly listing)
   :param sign: number sign
   :param size: size of number in bytes Please note that the type of the resulting expression can be anything because it can be inherited from the disassembly listing or taken from the user specified number representation in the pseudocode view.


.. py:function:: create_helper(*args)

   Create a helper object..


.. py:function:: install_hexrays_callback(callback)

   Install handler for decompiler events. 
           
   :param callback: handler to install
   :returns: false if failed


.. py:function:: remove_hexrays_callback(callback)

   Uninstall handler for decompiler events. 
           
   :param callback: handler to uninstall
   :returns: number of uninstalled handlers.



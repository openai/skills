ida_typeinf
===========

.. py:module:: ida_typeinf

.. autoapi-nested-parse::

   Type information in IDA.

   In IDA, types are represented by and manipulated through tinfo_t objects.

   A tinfo_t can represent a simple type (e.g., `int`, `float`), a complex type 
   (a structure, enum, union, typedef), or even an array, or a function prototype.

   The key types in this file are:

   * til_t - a type info library. Holds type information in serialized form.
   * tinfo_t - information about a type (simple, complex, ...)


   Glossary
   --------

   All throughout this file, there are certain terms that will keep appearing:

   * udt: "user-defined type": a structure or union - but not enums. See udt_type_data_t
   * udm: "udt member": i.e., a structure or union member. See udm_t
   * edm: "enum member": i.e., an enumeration member - i.e., an enumerator. See edm_t


   Under the hood
   --------------

   The tinfo_t type provides a lot of useful methods already, but it's possible to 
   achieve even more by retrieving its contents into the container classes:

   * udt_type_data_t - for structures & unions. See tinfo_t::get_udt_details. 
     Essentially, a vector of udm_t
   * enum_type_data_t - for enumerations. See tinfo_t::get_enum_details. 
     Essentially, a vector of edm_t
   * ptr_type_data_t - for pointers. See tinfo_t::get_ptr_details
   * array_type_data_t - for arrays. See tinfo_t::get_array_details
   * func_type_data_t - for function prototypes. See tinfo_t::get_func_details
   * bitfield_type_data_t - for bitfields. See tinfo_t::get_bitfield_details


   Attached & detached tinfo_t objects
   ------------------------------------

   tinfo_t objects can be attached to a til_t library, or can be created without 
   using any til_t.

   Here is an example, assigning a function prototype::

       func_type_data_t func_info;
       funcarg_t argc; 
       argc.name = "argc"; 
       argc.type = tinfo_t(BT_INT); 
       func_info.push_back(argc);
       funcarg_t argv; 
       argc.name = "argv"; 
       argc.type = tinfo_t("const char **"); 
       func_info.push_back(argv)
       tinfo_t tif; 
       if ( tif.create_func(func_info) ) { 
           ea_t ea = // get address of "main" 
           apply_tinfo(ea, tif, TINFO_DEFINITE); 
       }

   This code manipulates a "detached" tinfo_t object, which does not depend on any 
   til_t file. However, any complex type will require a til_t file. In IDA, there 
   is always a default til_t file for each idb file. This til_t file can be 
   specified by nullptr.

   On the other hand, the following code manipulates an "attached" tinfo_t object, 
   and any operation that modifies it, will also modify it in the hosting til_t::

       tinfo_t tif; 
       # Load type from the "Local Types" til_t. 
       # Note: we could have used `get_idati()` instead of nullptr 
       if ( tif.get_named_type(nullptr, "my_struct_t") ) 
           tif.add_udm("extra_field", "unsigned long long");

   You can check if a tinfo_t instance is attached to a type in a til_t file by 
   calling tinfo_t::is_typeref.

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For type operations, see :mod:`ida_domain.types`.



Attributes
----------

.. autoapisummary::

   ida_typeinf.DEFMASK64
   ida_typeinf.RESERVED_BYTE
   ida_typeinf.TAH_BYTE
   ida_typeinf.FAH_BYTE
   ida_typeinf.MAX_DECL_ALIGN
   ida_typeinf.TAH_HASATTRS
   ida_typeinf.TAUDT_UNALIGNED
   ida_typeinf.TAUDT_MSSTRUCT
   ida_typeinf.TAUDT_CPPOBJ
   ida_typeinf.TAUDT_VFTABLE
   ida_typeinf.TAUDT_FIXED
   ida_typeinf.TAUDT_TUPLE
   ida_typeinf.TAFLD_BASECLASS
   ida_typeinf.TAFLD_UNALIGNED
   ida_typeinf.TAFLD_VIRTBASE
   ida_typeinf.TAFLD_VFTABLE
   ida_typeinf.TAFLD_METHOD
   ida_typeinf.TAFLD_GAP
   ida_typeinf.TAFLD_REGCMT
   ida_typeinf.TAFLD_FRAME_R
   ida_typeinf.TAFLD_FRAME_S
   ida_typeinf.TAFLD_BYTIL
   ida_typeinf.TAPTR_PTR32
   ida_typeinf.TAPTR_PTR64
   ida_typeinf.TAPTR_RESTRICT
   ida_typeinf.TAPTR_SHIFTED
   ida_typeinf.TAENUM_64BIT
   ida_typeinf.TAENUM_UNSIGNED
   ida_typeinf.TAENUM_SIGNED
   ida_typeinf.TAENUM_OCT
   ida_typeinf.TAENUM_BIN
   ida_typeinf.TAENUM_NUMSIGN
   ida_typeinf.TAENUM_LZERO
   ida_typeinf.TAH_ALL
   ida_typeinf.cvar
   ida_typeinf.TYPE_BASE_MASK
   ida_typeinf.TYPE_FLAGS_MASK
   ida_typeinf.TYPE_MODIF_MASK
   ida_typeinf.TYPE_FULL_MASK
   ida_typeinf.BT_UNK
   ida_typeinf.BT_VOID
   ida_typeinf.BTMT_SIZE0
   ida_typeinf.BTMT_SIZE12
   ida_typeinf.BTMT_SIZE48
   ida_typeinf.BTMT_SIZE128
   ida_typeinf.BT_INT8
   ida_typeinf.BT_INT16
   ida_typeinf.BT_INT32
   ida_typeinf.BT_INT64
   ida_typeinf.BT_INT128
   ida_typeinf.BT_INT
   ida_typeinf.BTMT_UNKSIGN
   ida_typeinf.BTMT_SIGNED
   ida_typeinf.BTMT_USIGNED
   ida_typeinf.BTMT_UNSIGNED
   ida_typeinf.BTMT_CHAR
   ida_typeinf.BT_BOOL
   ida_typeinf.BTMT_DEFBOOL
   ida_typeinf.BTMT_BOOL1
   ida_typeinf.BTMT_BOOL2
   ida_typeinf.BTMT_BOOL8
   ida_typeinf.BTMT_BOOL4
   ida_typeinf.BT_FLOAT
   ida_typeinf.BTMT_FLOAT
   ida_typeinf.BTMT_DOUBLE
   ida_typeinf.BTMT_LNGDBL
   ida_typeinf.BTMT_SPECFLT
   ida_typeinf.BT_PTR
   ida_typeinf.BTMT_DEFPTR
   ida_typeinf.BTMT_NEAR
   ida_typeinf.BTMT_FAR
   ida_typeinf.BTMT_CLOSURE
   ida_typeinf.BT_ARRAY
   ida_typeinf.BTMT_NONBASED
   ida_typeinf.BTMT_ARRESERV
   ida_typeinf.BT_FUNC
   ida_typeinf.BTMT_DEFCALL
   ida_typeinf.BTMT_NEARCALL
   ida_typeinf.BTMT_FARCALL
   ida_typeinf.BTMT_INTCALL
   ida_typeinf.BT_COMPLEX
   ida_typeinf.BTMT_STRUCT
   ida_typeinf.BTMT_UNION
   ida_typeinf.BTMT_ENUM
   ida_typeinf.BTMT_TYPEDEF
   ida_typeinf.BT_BITFIELD
   ida_typeinf.BTMT_BFLDI8
   ida_typeinf.BTMT_BFLDI16
   ida_typeinf.BTMT_BFLDI32
   ida_typeinf.BTMT_BFLDI64
   ida_typeinf.BT_RESERVED
   ida_typeinf.BTM_CONST
   ida_typeinf.BTM_VOLATILE
   ida_typeinf.BTE_SIZE_MASK
   ida_typeinf.BTE_RESERVED
   ida_typeinf.BTE_BITMASK
   ida_typeinf.BTE_OUT_MASK
   ida_typeinf.BTE_HEX
   ida_typeinf.BTE_CHAR
   ida_typeinf.BTE_SDEC
   ida_typeinf.BTE_UDEC
   ida_typeinf.BTE_ALWAYS
   ida_typeinf.BT_SEGREG
   ida_typeinf.BT_UNK_BYTE
   ida_typeinf.BT_UNK_WORD
   ida_typeinf.BT_UNK_DWORD
   ida_typeinf.BT_UNK_QWORD
   ida_typeinf.BT_UNK_OWORD
   ida_typeinf.BT_UNKNOWN
   ida_typeinf.BTF_BYTE
   ida_typeinf.BTF_UNK
   ida_typeinf.BTF_VOID
   ida_typeinf.BTF_INT8
   ida_typeinf.BTF_CHAR
   ida_typeinf.BTF_UCHAR
   ida_typeinf.BTF_UINT8
   ida_typeinf.BTF_INT16
   ida_typeinf.BTF_UINT16
   ida_typeinf.BTF_INT32
   ida_typeinf.BTF_UINT32
   ida_typeinf.BTF_INT64
   ida_typeinf.BTF_UINT64
   ida_typeinf.BTF_INT128
   ida_typeinf.BTF_UINT128
   ida_typeinf.BTF_INT
   ida_typeinf.BTF_UINT
   ida_typeinf.BTF_SINT
   ida_typeinf.BTF_BOOL
   ida_typeinf.BTF_FLOAT
   ida_typeinf.BTF_DOUBLE
   ida_typeinf.BTF_LDOUBLE
   ida_typeinf.BTF_TBYTE
   ida_typeinf.BTF_STRUCT
   ida_typeinf.BTF_UNION
   ida_typeinf.BTF_ENUM
   ida_typeinf.BTF_TYPEDEF
   ida_typeinf.TA_ORG_TYPEDEF
   ida_typeinf.TA_ORG_ARRDIM
   ida_typeinf.TA_FORMAT
   ida_typeinf.TA_VALUE_REPR
   ida_typeinf.no_sign
   ida_typeinf.type_signed
   ida_typeinf.type_unsigned
   ida_typeinf.TIL_ZIP
   ida_typeinf.TIL_MAC
   ida_typeinf.TIL_ESI
   ida_typeinf.TIL_UNI
   ida_typeinf.TIL_ORD
   ida_typeinf.TIL_ALI
   ida_typeinf.TIL_MOD
   ida_typeinf.TIL_STM
   ida_typeinf.TIL_SLD
   ida_typeinf.TIL_ECC
   ida_typeinf.TIL_ADD_FAILED
   ida_typeinf.TIL_ADD_OK
   ida_typeinf.TIL_ADD_ALREADY
   ida_typeinf.CM_MASK
   ida_typeinf.CM_UNKNOWN
   ida_typeinf.CM_N8_F16
   ida_typeinf.CM_N64
   ida_typeinf.CM_N16_F32
   ida_typeinf.CM_N32_F48
   ida_typeinf.CM_M_MASK
   ida_typeinf.CM_M_NN
   ida_typeinf.CM_M_FF
   ida_typeinf.CM_M_NF
   ida_typeinf.CM_M_FN
   ida_typeinf.CM_CC_MASK
   ida_typeinf.CM_CC_INVALID
   ida_typeinf.CM_CC_UNKNOWN
   ida_typeinf.CM_CC_VOIDARG
   ida_typeinf.CM_CC_CDECL
   ida_typeinf.CM_CC_ELLIPSIS
   ida_typeinf.CM_CC_STDCALL
   ida_typeinf.CM_CC_PASCAL
   ida_typeinf.CM_CC_FASTCALL
   ida_typeinf.CM_CC_THISCALL
   ida_typeinf.CM_CC_SWIFT
   ida_typeinf.CM_CC_SPOILED
   ida_typeinf.CM_CC_GOLANG
   ida_typeinf.CM_CC_RESERVE3
   ida_typeinf.CM_CC_SPECIALE
   ida_typeinf.CM_CC_SPECIALP
   ida_typeinf.CM_CC_SPECIAL
   ida_typeinf.CM_CC_LAST_USERCALL
   ida_typeinf.CM_CC_GOSTK
   ida_typeinf.CM_CC_FIRST_PLAIN_CUSTOM
   ida_typeinf.BFA_NORET
   ida_typeinf.BFA_PURE
   ida_typeinf.BFA_HIGH
   ida_typeinf.BFA_STATIC
   ida_typeinf.BFA_VIRTUAL
   ida_typeinf.BFA_FUNC_MARKER
   ida_typeinf.BFA_FUNC_EXT_FORMAT
   ida_typeinf.ALOC_NONE
   ida_typeinf.ALOC_STACK
   ida_typeinf.ALOC_DIST
   ida_typeinf.ALOC_REG1
   ida_typeinf.ALOC_REG2
   ida_typeinf.ALOC_RREL
   ida_typeinf.ALOC_STATIC
   ida_typeinf.ALOC_CUSTOM
   ida_typeinf.PRALOC_VERIFY
   ida_typeinf.PRALOC_STKOFF
   ida_typeinf.C_PC_TINY
   ida_typeinf.C_PC_SMALL
   ida_typeinf.C_PC_COMPACT
   ida_typeinf.C_PC_MEDIUM
   ida_typeinf.C_PC_LARGE
   ida_typeinf.C_PC_HUGE
   ida_typeinf.C_PC_FLAT
   ida_typeinf.CCI_VARARG
   ida_typeinf.CCI_PURGE
   ida_typeinf.CCI_USER
   ida_typeinf.ARGREGS_POLICY_UNDEFINED
   ida_typeinf.ARGREGS_GP_ONLY
   ida_typeinf.ARGREGS_INDEPENDENT
   ida_typeinf.ARGREGS_BY_SLOTS
   ida_typeinf.ARGREGS_FP_MASKS_GP
   ida_typeinf.ARGREGS_MIPS_O32
   ida_typeinf.ARGREGS_RISCV
   ida_typeinf.SETCOMP_OVERRIDE
   ida_typeinf.SETCOMP_ONLY_ID
   ida_typeinf.SETCOMP_ONLY_ABI
   ida_typeinf.SETCOMP_BY_USER
   ida_typeinf.MAX_FUNC_ARGS
   ida_typeinf.ABS_UNK
   ida_typeinf.ABS_NO
   ida_typeinf.ABS_YES
   ida_typeinf.SC_UNK
   ida_typeinf.SC_TYPE
   ida_typeinf.SC_EXT
   ida_typeinf.SC_STAT
   ida_typeinf.SC_REG
   ida_typeinf.SC_AUTO
   ida_typeinf.SC_FRIEND
   ida_typeinf.SC_VIRT
   ida_typeinf.HTI_CPP
   ida_typeinf.HTI_INT
   ida_typeinf.HTI_EXT
   ida_typeinf.HTI_LEX
   ida_typeinf.HTI_UNP
   ida_typeinf.HTI_TST
   ida_typeinf.HTI_FIL
   ida_typeinf.HTI_MAC
   ida_typeinf.HTI_NWR
   ida_typeinf.HTI_NER
   ida_typeinf.HTI_DCL
   ida_typeinf.HTI_NDC
   ida_typeinf.HTI_PAK
   ida_typeinf.HTI_PAK_SHIFT
   ida_typeinf.HTI_PAKDEF
   ida_typeinf.HTI_PAK1
   ida_typeinf.HTI_PAK2
   ida_typeinf.HTI_PAK4
   ida_typeinf.HTI_PAK8
   ida_typeinf.HTI_PAK16
   ida_typeinf.HTI_HIGH
   ida_typeinf.HTI_LOWER
   ida_typeinf.HTI_RAWARGS
   ida_typeinf.HTI_RELAXED
   ida_typeinf.HTI_NOBASE
   ida_typeinf.HTI_SEMICOLON
   ida_typeinf.HTI_STANDALONE
   ida_typeinf.PT_SIL
   ida_typeinf.PT_NDC
   ida_typeinf.PT_TYP
   ida_typeinf.PT_VAR
   ida_typeinf.PT_PACKMASK
   ida_typeinf.PT_HIGH
   ida_typeinf.PT_LOWER
   ida_typeinf.PT_REPLACE
   ida_typeinf.PT_RAWARGS
   ida_typeinf.PT_RELAXED
   ida_typeinf.PT_EMPTY
   ida_typeinf.PT_SEMICOLON
   ida_typeinf.PT_SYMBOL
   ida_typeinf.PRTYPE_1LINE
   ida_typeinf.PRTYPE_MULTI
   ida_typeinf.PRTYPE_TYPE
   ida_typeinf.PRTYPE_PRAGMA
   ida_typeinf.PRTYPE_SEMI
   ida_typeinf.PRTYPE_CPP
   ida_typeinf.PRTYPE_DEF
   ida_typeinf.PRTYPE_NOARGS
   ida_typeinf.PRTYPE_NOARRS
   ida_typeinf.PRTYPE_NORES
   ida_typeinf.PRTYPE_RESTORE
   ida_typeinf.PRTYPE_NOREGEX
   ida_typeinf.PRTYPE_COLORED
   ida_typeinf.PRTYPE_METHODS
   ida_typeinf.PRTYPE_1LINCMT
   ida_typeinf.PRTYPE_HEADER
   ida_typeinf.PRTYPE_OFFSETS
   ida_typeinf.PRTYPE_MAXSTR
   ida_typeinf.PRTYPE_TAIL
   ida_typeinf.PRTYPE_ARGLOCS
   ida_typeinf.NTF_TYPE
   ida_typeinf.NTF_SYMU
   ida_typeinf.NTF_SYMM
   ida_typeinf.NTF_NOBASE
   ida_typeinf.NTF_REPLACE
   ida_typeinf.NTF_UMANGLED
   ida_typeinf.NTF_NOCUR
   ida_typeinf.NTF_64BIT
   ida_typeinf.NTF_FIXNAME
   ida_typeinf.NTF_IDBENC
   ida_typeinf.NTF_CHKSYNC
   ida_typeinf.NTF_NO_NAMECHK
   ida_typeinf.NTF_COPY
   ida_typeinf.TERR_OK
   ida_typeinf.TERR_SAVE_ERROR
   ida_typeinf.TERR_SERIALIZE
   ida_typeinf.TERR_BAD_NAME
   ida_typeinf.TERR_BAD_ARG
   ida_typeinf.TERR_BAD_TYPE
   ida_typeinf.TERR_BAD_SIZE
   ida_typeinf.TERR_BAD_INDEX
   ida_typeinf.TERR_BAD_ARRAY
   ida_typeinf.TERR_BAD_BF
   ida_typeinf.TERR_BAD_OFFSET
   ida_typeinf.TERR_BAD_UNIVAR
   ida_typeinf.TERR_BAD_VARLAST
   ida_typeinf.TERR_OVERLAP
   ida_typeinf.TERR_BAD_SUBTYPE
   ida_typeinf.TERR_BAD_VALUE
   ida_typeinf.TERR_NO_BMASK
   ida_typeinf.TERR_BAD_BMASK
   ida_typeinf.TERR_BAD_MSKVAL
   ida_typeinf.TERR_BAD_REPR
   ida_typeinf.TERR_GRP_NOEMPTY
   ida_typeinf.TERR_DUPNAME
   ida_typeinf.TERR_UNION_BF
   ida_typeinf.TERR_BAD_TAH
   ida_typeinf.TERR_BAD_BASE
   ida_typeinf.TERR_BAD_GAP
   ida_typeinf.TERR_NESTED
   ida_typeinf.TERR_NOT_COMPAT
   ida_typeinf.TERR_BAD_LAYOUT
   ida_typeinf.TERR_BAD_GROUPS
   ida_typeinf.TERR_BAD_SERIAL
   ida_typeinf.TERR_ALIEN_NAME
   ida_typeinf.TERR_STOCK
   ida_typeinf.TERR_ENUM_SIZE
   ida_typeinf.TERR_NOT_IMPL
   ida_typeinf.TERR_TYPE_WORSE
   ida_typeinf.TERR_BAD_FX_SIZE
   ida_typeinf.TERR_STRUCT_SIZE
   ida_typeinf.TERR_NOT_FOUND
   ida_typeinf.TERR_COUNT
   ida_typeinf.CCN_C
   ida_typeinf.CCN_CPP
   ida_typeinf.ADDTIL_DEFAULT
   ida_typeinf.ADDTIL_INCOMP
   ida_typeinf.ADDTIL_SILENT
   ida_typeinf.ADDTIL_FAILED
   ida_typeinf.ADDTIL_OK
   ida_typeinf.ADDTIL_COMP
   ida_typeinf.ADDTIL_ABORTED
   ida_typeinf.TINFO_GUESSED
   ida_typeinf.TINFO_DEFINITE
   ida_typeinf.TINFO_DELAYFUNC
   ida_typeinf.TINFO_STRICT
   ida_typeinf.GUESS_FUNC_FAILED
   ida_typeinf.GUESS_FUNC_TRIVIAL
   ida_typeinf.GUESS_FUNC_OK
   ida_typeinf.STI_PCHAR
   ida_typeinf.STI_PUCHAR
   ida_typeinf.STI_PCCHAR
   ida_typeinf.STI_PCUCHAR
   ida_typeinf.STI_PBYTE
   ida_typeinf.STI_PINT
   ida_typeinf.STI_PUINT
   ida_typeinf.STI_PVOID
   ida_typeinf.STI_PPVOID
   ida_typeinf.STI_PCVOID
   ida_typeinf.STI_ACHAR
   ida_typeinf.STI_AUCHAR
   ida_typeinf.STI_ACCHAR
   ida_typeinf.STI_ACUCHAR
   ida_typeinf.STI_FPURGING
   ida_typeinf.STI_FDELOP
   ida_typeinf.STI_MSGSEND
   ida_typeinf.STI_AEABI_LCMP
   ida_typeinf.STI_AEABI_ULCMP
   ida_typeinf.STI_DONT_USE
   ida_typeinf.STI_SIZE_T
   ida_typeinf.STI_SSIZE_T
   ida_typeinf.STI_AEABI_MEMCPY
   ida_typeinf.STI_AEABI_MEMSET
   ida_typeinf.STI_AEABI_MEMCLR
   ida_typeinf.STI_RTC_CHECK_2
   ida_typeinf.STI_RTC_CHECK_4
   ida_typeinf.STI_RTC_CHECK_8
   ida_typeinf.STI_COMPLEX64
   ida_typeinf.STI_COMPLEX128
   ida_typeinf.STI_PUNKNOWN
   ida_typeinf.STI_LAST
   ida_typeinf.ETF_NO_SAVE
   ida_typeinf.ETF_NO_LAYOUT
   ida_typeinf.ETF_MAY_DESTROY
   ida_typeinf.ETF_COMPATIBLE
   ida_typeinf.ETF_FUNCARG
   ida_typeinf.ETF_FORCENAME
   ida_typeinf.ETF_AUTONAME
   ida_typeinf.ETF_BYTIL
   ida_typeinf.ETF_NO_ARRAY
   ida_typeinf.GTD_CALC_LAYOUT
   ida_typeinf.GTD_NO_LAYOUT
   ida_typeinf.GTD_DEL_BITFLDS
   ida_typeinf.GTD_CALC_ARGLOCS
   ida_typeinf.GTD_NO_ARGLOCS
   ida_typeinf.GTS_NESTED
   ida_typeinf.GTS_BASECLASS
   ida_typeinf.SUDT_SORT
   ida_typeinf.SUDT_ALIGN
   ida_typeinf.SUDT_GAPS
   ida_typeinf.SUDT_UNEX
   ida_typeinf.SUDT_FAST
   ida_typeinf.SUDT_CONST
   ida_typeinf.SUDT_VOLATILE
   ida_typeinf.SUDT_TRUNC
   ida_typeinf.SUDT_SERDEF
   ida_typeinf.COMP_MASK
   ida_typeinf.COMP_UNK
   ida_typeinf.COMP_MS
   ida_typeinf.COMP_BC
   ida_typeinf.COMP_WATCOM
   ida_typeinf.COMP_GNU
   ida_typeinf.COMP_VISAGE
   ida_typeinf.COMP_BP
   ida_typeinf.COMP_UNSURE
   ida_typeinf.BADSIZE
   ida_typeinf.FIRST_NONTRIVIAL_TYPID
   ida_typeinf.TYPID_ISREF
   ida_typeinf.TYPID_SHIFT
   ida_typeinf.STRMEM_MASK
   ida_typeinf.STRMEM_OFFSET
   ida_typeinf.STRMEM_INDEX
   ida_typeinf.STRMEM_AUTO
   ida_typeinf.STRMEM_NAME
   ida_typeinf.STRMEM_TYPE
   ida_typeinf.STRMEM_SIZE
   ida_typeinf.STRMEM_MINS
   ida_typeinf.STRMEM_MAXS
   ida_typeinf.STRMEM_LOWBND
   ida_typeinf.STRMEM_NEXT
   ida_typeinf.STRMEM_VFTABLE
   ida_typeinf.STRMEM_SKIP_EMPTY
   ida_typeinf.STRMEM_CASTABLE_TO
   ida_typeinf.STRMEM_ANON
   ida_typeinf.STRMEM_SKIP_GAPS
   ida_typeinf.TCMP_EQUAL
   ida_typeinf.TCMP_IGNMODS
   ida_typeinf.TCMP_AUTOCAST
   ida_typeinf.TCMP_MANCAST
   ida_typeinf.TCMP_CALL
   ida_typeinf.TCMP_DELPTR
   ida_typeinf.TCMP_DECL
   ida_typeinf.TCMP_ANYBASE
   ida_typeinf.TCMP_SKIPTHIS
   ida_typeinf.TCMP_DEEP_UDT
   ida_typeinf.FAI_HIDDEN
   ida_typeinf.FAI_RETPTR
   ida_typeinf.FAI_STRUCT
   ida_typeinf.FAI_ARRAY
   ida_typeinf.FAI_UNUSED
   ida_typeinf.FTI_SPOILED
   ida_typeinf.FTI_NORET
   ida_typeinf.FTI_PURE
   ida_typeinf.FTI_HIGH
   ida_typeinf.FTI_STATIC
   ida_typeinf.FTI_VIRTUAL
   ida_typeinf.FTI_CALLTYPE
   ida_typeinf.FTI_DEFCALL
   ida_typeinf.FTI_NEARCALL
   ida_typeinf.FTI_FARCALL
   ida_typeinf.FTI_INTCALL
   ida_typeinf.FTI_ARGLOCS
   ida_typeinf.FTI_EXPLOCS
   ida_typeinf.FTI_CONST
   ida_typeinf.FTI_CTOR
   ida_typeinf.FTI_DTOR
   ida_typeinf.FTI_ALL
   ida_typeinf.CC_CDECL_OK
   ida_typeinf.CC_ALLOW_ARGPERM
   ida_typeinf.CC_ALLOW_REGHOLES
   ida_typeinf.CC_HAS_ELLIPSIS
   ida_typeinf.CC_GOLANG_OK
   ida_typeinf.FMTFUNC_PRINTF
   ida_typeinf.FMTFUNC_SCANF
   ida_typeinf.FMTFUNC_STRFTIME
   ida_typeinf.FMTFUNC_STRFMON
   ida_typeinf.MAX_ENUM_SERIAL
   ida_typeinf.FRB_MASK
   ida_typeinf.FRB_UNK
   ida_typeinf.FRB_NUMB
   ida_typeinf.FRB_NUMO
   ida_typeinf.FRB_NUMH
   ida_typeinf.FRB_NUMD
   ida_typeinf.FRB_FLOAT
   ida_typeinf.FRB_CHAR
   ida_typeinf.FRB_SEG
   ida_typeinf.FRB_ENUM
   ida_typeinf.FRB_OFFSET
   ida_typeinf.FRB_STRLIT
   ida_typeinf.FRB_STROFF
   ida_typeinf.FRB_CUSTOM
   ida_typeinf.FRB_INVSIGN
   ida_typeinf.FRB_INVBITS
   ida_typeinf.FRB_SIGNED
   ida_typeinf.FRB_LZERO
   ida_typeinf.FRB_TABFORM
   ida_typeinf.STRUC_SEPARATOR
   ida_typeinf.VTBL_SUFFIX
   ida_typeinf.VTBL_MEMNAME
   ida_typeinf.TPOS_LNNUM
   ida_typeinf.TPOS_REGCMT
   ida_typeinf.TVIS_TYPE
   ida_typeinf.TVIS_NAME
   ida_typeinf.TVIS_CMT
   ida_typeinf.TVIS_RPTCMT
   ida_typeinf.TVST_PRUNE
   ida_typeinf.TVST_DEF
   ida_typeinf.TVST_LEVEL
   ida_typeinf.PIO_NOATTR_FAIL
   ida_typeinf.PIO_IGNORE_PTRS
   ida_typeinf.UTP_ENUM
   ida_typeinf.UTP_STRUCT
   ida_typeinf.VALSTR_OPEN
   ida_typeinf.PDF_INCL_DEPS
   ida_typeinf.PDF_DEF_FWD
   ida_typeinf.PDF_DEF_BASE
   ida_typeinf.PDF_HEADER_CMT
   ida_typeinf.PT_FILE
   ida_typeinf.PT_STANDALONE
   ida_typeinf.cvar
   ida_typeinf.sc_auto
   ida_typeinf.sc_ext
   ida_typeinf.sc_friend
   ida_typeinf.sc_reg
   ida_typeinf.sc_stat
   ida_typeinf.sc_type
   ida_typeinf.sc_unk
   ida_typeinf.sc_virt
   ida_typeinf.TERR_SAVE
   ida_typeinf.TERR_WRONGNAME
   ida_typeinf.BADORD
   ida_typeinf.enum_member_vec_t
   ida_typeinf.enum_member_t
   ida_typeinf.udt_member_t


Classes
-------

.. autoapisummary::

   ida_typeinf.funcargvec_t
   ida_typeinf.reginfovec_t
   ida_typeinf.edmvec_t
   ida_typeinf.argpartvec_t
   ida_typeinf.valstrvec_t
   ida_typeinf.regobjvec_t
   ida_typeinf.type_attrs_t
   ida_typeinf.udtmembervec_template_t
   ida_typeinf.type_attr_t
   ida_typeinf.til_t
   ida_typeinf.rrel_t
   ida_typeinf.argloc_t
   ida_typeinf.argpart_t
   ida_typeinf.scattered_aloc_t
   ida_typeinf.aloc_visitor_t
   ida_typeinf.const_aloc_visitor_t
   ida_typeinf.stkarg_area_info_t
   ida_typeinf.custom_callcnv_t
   ida_typeinf.callregs_t
   ida_typeinf.tinfo_t
   ida_typeinf.simd_info_t
   ida_typeinf.ptr_type_data_t
   ida_typeinf.array_type_data_t
   ida_typeinf.funcarg_t
   ida_typeinf.func_type_data_t
   ida_typeinf.edm_t
   ida_typeinf.enum_type_data_t
   ida_typeinf.typedef_type_data_t
   ida_typeinf.custom_data_type_info_t
   ida_typeinf.value_repr_t
   ida_typeinf.udm_t
   ida_typeinf.udtmembervec_t
   ida_typeinf.udt_type_data_t
   ida_typeinf.udm_visitor_t
   ida_typeinf.bitfield_type_data_t
   ida_typeinf.type_mods_t
   ida_typeinf.tinfo_visitor_t
   ida_typeinf.regobj_t
   ida_typeinf.regobjs_t
   ida_typeinf.argtinfo_helper_t
   ida_typeinf.lowertype_helper_t
   ida_typeinf.ida_lowertype_helper_t
   ida_typeinf.valstr_t
   ida_typeinf.valstrs_t
   ida_typeinf.text_sink_t
   ida_typeinf.til_symbol_t
   ida_typeinf.predicate_t
   ida_typeinf.til_type_ref_t


Functions
---------

.. autoapisummary::

   ida_typeinf.deserialize_tinfo
   ida_typeinf.is_type_const
   ida_typeinf.is_type_volatile
   ida_typeinf.get_base_type
   ida_typeinf.get_type_flags
   ida_typeinf.get_full_type
   ida_typeinf.is_typeid_last
   ida_typeinf.is_type_partial
   ida_typeinf.is_type_void
   ida_typeinf.is_type_unknown
   ida_typeinf.is_type_ptr
   ida_typeinf.is_type_complex
   ida_typeinf.is_type_func
   ida_typeinf.is_type_array
   ida_typeinf.is_type_typedef
   ida_typeinf.is_type_sue
   ida_typeinf.is_type_struct
   ida_typeinf.is_type_union
   ida_typeinf.is_type_struni
   ida_typeinf.is_type_enum
   ida_typeinf.is_type_bitfld
   ida_typeinf.is_type_int
   ida_typeinf.is_type_int128
   ida_typeinf.is_type_int64
   ida_typeinf.is_type_int32
   ida_typeinf.is_type_int16
   ida_typeinf.is_type_char
   ida_typeinf.is_type_paf
   ida_typeinf.is_type_ptr_or_array
   ida_typeinf.is_type_floating
   ida_typeinf.is_type_integral
   ida_typeinf.is_type_ext_integral
   ida_typeinf.is_type_arithmetic
   ida_typeinf.is_type_ext_arithmetic
   ida_typeinf.is_type_uint
   ida_typeinf.is_type_uchar
   ida_typeinf.is_type_uint16
   ida_typeinf.is_type_uint32
   ida_typeinf.is_type_uint64
   ida_typeinf.is_type_uint128
   ida_typeinf.is_type_ldouble
   ida_typeinf.is_type_double
   ida_typeinf.is_type_float
   ida_typeinf.is_type_tbyte
   ida_typeinf.is_type_bool
   ida_typeinf.is_tah_byte
   ida_typeinf.is_sdacl_byte
   ida_typeinf.append_argloc
   ida_typeinf.extract_argloc
   ida_typeinf.resolve_typedef
   ida_typeinf.is_restype_void
   ida_typeinf.is_restype_enum
   ida_typeinf.is_restype_struni
   ida_typeinf.is_restype_struct
   ida_typeinf.get_scalar_bt
   ida_typeinf.new_til
   ida_typeinf.load_til
   ida_typeinf.compact_til
   ida_typeinf.store_til
   ida_typeinf.free_til
   ida_typeinf.load_til_header
   ida_typeinf.is_code_far
   ida_typeinf.is_data_far
   ida_typeinf.verify_argloc
   ida_typeinf.optimize_argloc
   ida_typeinf.print_argloc
   ida_typeinf.for_all_arglocs
   ida_typeinf.for_all_const_arglocs
   ida_typeinf.is_user_cc
   ida_typeinf.is_vararg_cc
   ida_typeinf.is_purging_cc
   ida_typeinf.is_golang_cc
   ida_typeinf.is_custom_callcnv
   ida_typeinf.is_swift_cc
   ida_typeinf.get_stkarg_area_info
   ida_typeinf.get_custom_callcnv
   ida_typeinf.find_custom_callcnv
   ida_typeinf.get_custom_callcnvs
   ida_typeinf.get_comp
   ida_typeinf.get_compiler_name
   ida_typeinf.get_compiler_abbr
   ida_typeinf.get_compilers
   ida_typeinf.is_comp_unsure
   ida_typeinf.default_compiler
   ida_typeinf.is_gcc
   ida_typeinf.is_gcc32
   ida_typeinf.is_gcc64
   ida_typeinf.gcc_layout
   ida_typeinf.set_compiler
   ida_typeinf.set_compiler_id
   ida_typeinf.set_abi_name
   ida_typeinf.get_abi_name
   ida_typeinf.append_abi_opts
   ida_typeinf.remove_abi_opts
   ida_typeinf.set_compiler_string
   ida_typeinf.use_golang_cc
   ida_typeinf.switch_to_golang
   ida_typeinf.convert_pt_flags_to_hti
   ida_typeinf.parse_decl
   ida_typeinf.parse_decls
   ida_typeinf.print_type
   ida_typeinf.tinfo_errstr
   ida_typeinf.del_named_type
   ida_typeinf.first_named_type
   ida_typeinf.next_named_type
   ida_typeinf.copy_named_type
   ida_typeinf.decorate_name
   ida_typeinf.gen_decorate_name
   ida_typeinf.calc_c_cpp_name
   ida_typeinf.enable_numbered_types
   ida_typeinf.alloc_type_ordinals
   ida_typeinf.alloc_type_ordinal
   ida_typeinf.get_ordinal_limit
   ida_typeinf.get_ordinal_count
   ida_typeinf.del_numbered_type
   ida_typeinf.set_type_alias
   ida_typeinf.get_alias_target
   ida_typeinf.get_type_ordinal
   ida_typeinf.get_numbered_type_name
   ida_typeinf.create_numbered_type_name
   ida_typeinf.is_ordinal_name
   ida_typeinf.is_type_choosable
   ida_typeinf.set_type_choosable
   ida_typeinf.get_vftable_ea
   ida_typeinf.get_vftable_ordinal
   ida_typeinf.set_vftable_ea
   ida_typeinf.del_vftable_ea
   ida_typeinf.deref_ptr
   ida_typeinf.add_til
   ida_typeinf.del_til
   ida_typeinf.apply_named_type
   ida_typeinf.apply_tinfo
   ida_typeinf.apply_cdecl
   ida_typeinf.apply_callee_tinfo
   ida_typeinf.apply_once_tinfo_and_name
   ida_typeinf.guess_tinfo
   ida_typeinf.set_c_header_path
   ida_typeinf.get_c_header_path
   ida_typeinf.set_c_macros
   ida_typeinf.get_c_macros
   ida_typeinf.get_idati
   ida_typeinf.get_idainfo_by_type
   ida_typeinf.get_tinfo_by_flags
   ida_typeinf.copy_tinfo_t
   ida_typeinf.detach_tinfo_t
   ida_typeinf.clear_tinfo_t
   ida_typeinf.create_tinfo
   ida_typeinf.verify_tinfo
   ida_typeinf.get_tinfo_details
   ida_typeinf.get_tinfo_size
   ida_typeinf.get_tinfo_pdata
   ida_typeinf.get_tinfo_property
   ida_typeinf.get_tinfo_property4
   ida_typeinf.set_tinfo_property
   ida_typeinf.set_tinfo_property4
   ida_typeinf.serialize_tinfo
   ida_typeinf.find_tinfo_udt_member
   ida_typeinf.print_tinfo
   ida_typeinf.dstr_tinfo
   ida_typeinf.visit_subtypes
   ida_typeinf.compare_tinfo
   ida_typeinf.lexcompare_tinfo
   ida_typeinf.get_stock_tinfo
   ida_typeinf.read_tinfo_bitfield_value
   ida_typeinf.write_tinfo_bitfield_value
   ida_typeinf.get_tinfo_attr
   ida_typeinf.set_tinfo_attr
   ida_typeinf.del_tinfo_attr
   ida_typeinf.get_tinfo_attrs
   ida_typeinf.set_tinfo_attrs
   ida_typeinf.score_tinfo
   ida_typeinf.save_tinfo
   ida_typeinf.append_tinfo_covered
   ida_typeinf.calc_tinfo_gaps
   ida_typeinf.value_repr_t__from_opinfo
   ida_typeinf.value_repr_t__print_
   ida_typeinf.udt_type_data_t__find_member
   ida_typeinf.udt_type_data_t__get_best_fit_member
   ida_typeinf.get_tinfo_by_edm_name
   ida_typeinf.remove_pointer
   ida_typeinf.guess_func_cc
   ida_typeinf.dump_func_type_data
   ida_typeinf.calc_arglocs
   ida_typeinf.calc_varglocs
   ida_typeinf.stroff_as_size
   ida_typeinf.visit_stroff_udms
   ida_typeinf.is_one_bit_mask
   ida_typeinf.inf_pack_stkargs
   ida_typeinf.inf_big_arg_align
   ida_typeinf.inf_huge_arg_align
   ida_typeinf.unpack_idcobj_from_idb
   ida_typeinf.unpack_idcobj_from_bv
   ida_typeinf.pack_idcobj_to_idb
   ida_typeinf.pack_idcobj_to_bv
   ida_typeinf.apply_tinfo_to_stkarg
   ida_typeinf.gen_use_arg_tinfos
   ida_typeinf.func_has_stkframe_hole
   ida_typeinf.lower_type
   ida_typeinf.replace_ordinal_typerefs
   ida_typeinf.begin_type_updating
   ida_typeinf.end_type_updating
   ida_typeinf.get_named_type_tid
   ida_typeinf.get_tid_name
   ida_typeinf.get_tid_ordinal
   ida_typeinf.get_udm_by_fullname
   ida_typeinf.get_idainfo_by_udm
   ida_typeinf.create_enum_type
   ida_typeinf.calc_number_of_children
   ida_typeinf.get_enum_member_expr
   ida_typeinf.choose_named_type
   ida_typeinf.choose_local_tinfo
   ida_typeinf.choose_local_tinfo_and_delta
   ida_typeinf.calc_retloc
   ida_typeinf.register_custom_callcnv
   ida_typeinf.unregister_custom_callcnv
   ida_typeinf.idc_parse_decl
   ida_typeinf.calc_type_size
   ida_typeinf.apply_type
   ida_typeinf.get_arg_addrs
   ida_typeinf.unpack_object_from_idb
   ida_typeinf.unpack_object_from_bv
   ida_typeinf.pack_object_to_idb
   ida_typeinf.pack_object_to_bv
   ida_typeinf.idc_parse_types
   ida_typeinf.idc_get_type_raw
   ida_typeinf.idc_get_local_type_raw
   ida_typeinf.idc_guess_type
   ida_typeinf.idc_get_type
   ida_typeinf.idc_set_local_type
   ida_typeinf.idc_get_local_type
   ida_typeinf.idc_print_type
   ida_typeinf.idc_get_local_type_name
   ida_typeinf.get_named_type
   ida_typeinf.get_named_type64
   ida_typeinf.print_decls
   ida_typeinf.remove_tinfo_pointer
   ida_typeinf.get_numbered_type
   ida_typeinf.set_numbered_type


Module Contents
---------------

.. py:data:: DEFMASK64

   default bitmask 64bits


.. py:function:: deserialize_tinfo(tif: tinfo_t, til: til_t, ptype: type_t const **, pfields: p_list const **, pfldcmts: p_list const **, cmt: str = None) -> bool

.. py:class:: funcargvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> funcarg_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> funcarg_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: funcargvec_t) -> None


   .. py:method:: extract() -> funcarg_t *


   .. py:method:: inject(s: funcarg_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< funcarg_t >::const_iterator


   .. py:method:: end(*args) -> qvector< funcarg_t >::const_iterator


   .. py:method:: insert(it: funcarg_t, x: funcarg_t) -> qvector< funcarg_t >::iterator


   .. py:method:: erase(*args) -> qvector< funcarg_t >::iterator


   .. py:method:: find(*args) -> qvector< funcarg_t >::const_iterator


   .. py:method:: has(x: funcarg_t) -> bool


   .. py:method:: add_unique(x: funcarg_t) -> bool


   .. py:method:: append(x: funcarg_t) -> None


   .. py:method:: extend(x: funcargvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: reginfovec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> reg_info_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> reg_info_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: reginfovec_t) -> None


   .. py:method:: extract() -> reg_info_t *


   .. py:method:: inject(s: reg_info_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< reg_info_t >::const_iterator


   .. py:method:: end(*args) -> qvector< reg_info_t >::const_iterator


   .. py:method:: insert(it: reg_info_t, x: reg_info_t) -> qvector< reg_info_t >::iterator


   .. py:method:: erase(*args) -> qvector< reg_info_t >::iterator


   .. py:method:: find(*args) -> qvector< reg_info_t >::const_iterator


   .. py:method:: has(x: reg_info_t) -> bool


   .. py:method:: add_unique(x: reg_info_t) -> bool


   .. py:method:: append(x: reg_info_t) -> None


   .. py:method:: extend(x: reginfovec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: edmvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> edm_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> edm_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: edmvec_t) -> None


   .. py:method:: extract() -> edm_t *


   .. py:method:: inject(s: edm_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< edm_t >::const_iterator


   .. py:method:: end(*args) -> qvector< edm_t >::const_iterator


   .. py:method:: insert(it: edm_t, x: edm_t) -> qvector< edm_t >::iterator


   .. py:method:: erase(*args) -> qvector< edm_t >::iterator


   .. py:method:: find(*args) -> qvector< edm_t >::const_iterator


   .. py:method:: has(x: edm_t) -> bool


   .. py:method:: add_unique(x: edm_t) -> bool


   .. py:method:: append(x: edm_t) -> None


   .. py:method:: extend(x: edmvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: argpartvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> argpart_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> argpart_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: argpartvec_t) -> None


   .. py:method:: extract() -> argpart_t *


   .. py:method:: inject(s: argpart_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< argpart_t >::const_iterator


   .. py:method:: end(*args) -> qvector< argpart_t >::const_iterator


   .. py:method:: insert(it: argpart_t, x: argpart_t) -> qvector< argpart_t >::iterator


   .. py:method:: erase(*args) -> qvector< argpart_t >::iterator


   .. py:method:: find(*args) -> qvector< argpart_t >::const_iterator


   .. py:method:: has(x: argpart_t) -> bool


   .. py:method:: add_unique(x: argpart_t) -> bool


   .. py:method:: append(x: argpart_t) -> None


   .. py:method:: extend(x: argpartvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: valstrvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> valstr_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> valstr_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: valstrvec_t) -> None


   .. py:method:: extract() -> valstr_t *


   .. py:method:: inject(s: valstr_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< valstr_t >::const_iterator


   .. py:method:: end(*args) -> qvector< valstr_t >::const_iterator


   .. py:method:: insert(it: valstr_t, x: valstr_t) -> qvector< valstr_t >::iterator


   .. py:method:: erase(*args) -> qvector< valstr_t >::iterator


   .. py:method:: append(x: valstr_t) -> None


   .. py:method:: extend(x: valstrvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: regobjvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> regobj_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> regobj_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: regobjvec_t) -> None


   .. py:method:: extract() -> regobj_t *


   .. py:method:: inject(s: regobj_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< regobj_t >::const_iterator


   .. py:method:: end(*args) -> qvector< regobj_t >::const_iterator


   .. py:method:: insert(it: regobj_t, x: regobj_t) -> qvector< regobj_t >::iterator


   .. py:method:: erase(*args) -> qvector< regobj_t >::iterator


   .. py:method:: append(x: regobj_t) -> None


   .. py:method:: extend(x: regobjvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: type_attrs_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> type_attr_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> type_attr_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: type_attrs_t) -> None


   .. py:method:: extract() -> type_attr_t *


   .. py:method:: inject(s: type_attr_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< type_attr_t >::const_iterator


   .. py:method:: end(*args) -> qvector< type_attr_t >::const_iterator


   .. py:method:: insert(it: type_attr_t, x: type_attr_t) -> qvector< type_attr_t >::iterator


   .. py:method:: erase(*args) -> qvector< type_attr_t >::iterator


   .. py:method:: append(x: type_attr_t) -> None


   .. py:method:: extend(x: type_attrs_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: udtmembervec_template_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> udm_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> udm_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: udtmembervec_template_t) -> None


   .. py:method:: extract() -> udm_t *


   .. py:method:: inject(s: udm_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< udm_t >::const_iterator


   .. py:method:: end(*args) -> qvector< udm_t >::const_iterator


   .. py:method:: insert(it: udm_t, x: udm_t) -> qvector< udm_t >::iterator


   .. py:method:: erase(*args) -> qvector< udm_t >::iterator


   .. py:method:: find(*args) -> qvector< udm_t >::const_iterator


   .. py:method:: has(x: udm_t) -> bool


   .. py:method:: add_unique(x: udm_t) -> bool


   .. py:method:: append(x: udm_t) -> None


   .. py:method:: extend(x: udtmembervec_template_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:data:: RESERVED_BYTE

   multifunctional purpose


.. py:function:: is_type_const(t: type_t) -> bool

   See BTM_CONST.


.. py:function:: is_type_volatile(t: type_t) -> bool

   See BTM_VOLATILE.


.. py:function:: get_base_type(t: type_t) -> type_t

   Get get basic type bits (TYPE_BASE_MASK)


.. py:function:: get_type_flags(t: type_t) -> type_t

   Get type flags (TYPE_FLAGS_MASK)


.. py:function:: get_full_type(t: type_t) -> type_t

   Get basic type bits + type flags (TYPE_FULL_MASK)


.. py:function:: is_typeid_last(t: type_t) -> bool

   Is the type_t the last byte of type declaration? (there are no additional bytes after a basic type, see _BT_LAST_BASIC) 
           


.. py:function:: is_type_partial(t: type_t) -> bool

   Identifies an unknown or void type with a known size (see Basic type: unknown & void)


.. py:function:: is_type_void(t: type_t) -> bool

   See BTF_VOID.


.. py:function:: is_type_unknown(t: type_t) -> bool

   See BT_UNKNOWN.


.. py:function:: is_type_ptr(t: type_t) -> bool

   See BT_PTR.


.. py:function:: is_type_complex(t: type_t) -> bool

   See BT_COMPLEX.


.. py:function:: is_type_func(t: type_t) -> bool

   See BT_FUNC.


.. py:function:: is_type_array(t: type_t) -> bool

   See BT_ARRAY.


.. py:function:: is_type_typedef(t: type_t) -> bool

   See BTF_TYPEDEF.


.. py:function:: is_type_sue(t: type_t) -> bool

   Is the type a struct/union/enum?


.. py:function:: is_type_struct(t: type_t) -> bool

   See BTF_STRUCT.


.. py:function:: is_type_union(t: type_t) -> bool

   See BTF_UNION.


.. py:function:: is_type_struni(t: type_t) -> bool

   Is the type a struct or union?


.. py:function:: is_type_enum(t: type_t) -> bool

   See BTF_ENUM.


.. py:function:: is_type_bitfld(t: type_t) -> bool

   See BT_BITFIELD.


.. py:function:: is_type_int(bt: type_t) -> bool

   Does the type_t specify one of the basic types in Basic type: integer?


.. py:function:: is_type_int128(t: type_t) -> bool

   Does the type specify a 128-bit value? (signed or unsigned, see Basic type: integer)


.. py:function:: is_type_int64(t: type_t) -> bool

   Does the type specify a 64-bit value? (signed or unsigned, see Basic type: integer)


.. py:function:: is_type_int32(t: type_t) -> bool

   Does the type specify a 32-bit value? (signed or unsigned, see Basic type: integer)


.. py:function:: is_type_int16(t: type_t) -> bool

   Does the type specify a 16-bit value? (signed or unsigned, see Basic type: integer)


.. py:function:: is_type_char(t: type_t) -> bool

   Does the type specify a char value? (signed or unsigned, see Basic type: integer)


.. py:function:: is_type_paf(t: type_t) -> bool

   Is the type a pointer, array, or function type?


.. py:function:: is_type_ptr_or_array(t: type_t) -> bool

   Is the type a pointer or array type?


.. py:function:: is_type_floating(t: type_t) -> bool

   Is the type a floating point type?


.. py:function:: is_type_integral(t: type_t) -> bool

   Is the type an integral type (char/short/int/long/bool)?


.. py:function:: is_type_ext_integral(t: type_t) -> bool

   Is the type an extended integral type? (integral or enum)


.. py:function:: is_type_arithmetic(t: type_t) -> bool

   Is the type an arithmetic type? (floating or integral)


.. py:function:: is_type_ext_arithmetic(t: type_t) -> bool

   Is the type an extended arithmetic type? (arithmetic or enum)


.. py:function:: is_type_uint(t: type_t) -> bool

   See BTF_UINT.


.. py:function:: is_type_uchar(t: type_t) -> bool

   See BTF_UCHAR.


.. py:function:: is_type_uint16(t: type_t) -> bool

   See BTF_UINT16.


.. py:function:: is_type_uint32(t: type_t) -> bool

   See BTF_UINT32.


.. py:function:: is_type_uint64(t: type_t) -> bool

   See BTF_UINT64.


.. py:function:: is_type_uint128(t: type_t) -> bool

   See BTF_UINT128.


.. py:function:: is_type_ldouble(t: type_t) -> bool

   See BTF_LDOUBLE.


.. py:function:: is_type_double(t: type_t) -> bool

   See BTF_DOUBLE.


.. py:function:: is_type_float(t: type_t) -> bool

   See BTF_FLOAT.


.. py:function:: is_type_tbyte(t: type_t) -> bool

   See BTF_FLOAT.


.. py:function:: is_type_bool(t: type_t) -> bool

   See BTF_BOOL.


.. py:data:: TAH_BYTE

   type attribute header byte


.. py:data:: FAH_BYTE

   function argument attribute header byte


.. py:data:: MAX_DECL_ALIGN

.. py:data:: TAH_HASATTRS

   has extended attributes


.. py:data:: TAUDT_UNALIGNED

   struct: unaligned struct


.. py:data:: TAUDT_MSSTRUCT

   struct: gcc msstruct attribute


.. py:data:: TAUDT_CPPOBJ

   struct: a c++ object, not simple pod type


.. py:data:: TAUDT_VFTABLE

   struct: is virtual function table


.. py:data:: TAUDT_FIXED

   struct: fixed field offsets, stored in serialized form; cannot be set for unions 
           


.. py:data:: TAUDT_TUPLE

   tuple: tuples are like structs but are returned differently from functions 
           


.. py:data:: TAFLD_BASECLASS

   field: do not include but inherit from the current field


.. py:data:: TAFLD_UNALIGNED

   field: unaligned field


.. py:data:: TAFLD_VIRTBASE

   field: virtual base (not supported yet)


.. py:data:: TAFLD_VFTABLE

   field: ptr to virtual function table


.. py:data:: TAFLD_METHOD

   denotes a udt member function


.. py:data:: TAFLD_GAP

   field: gap member (displayed as padding in type details)


.. py:data:: TAFLD_REGCMT

   field: the comment is regular (if not set, it is repeatable)


.. py:data:: TAFLD_FRAME_R

   frame: function return address frame slot


.. py:data:: TAFLD_FRAME_S

   frame: function saved registers frame slot


.. py:data:: TAFLD_BYTIL

   field: was the member created due to the type system


.. py:data:: TAPTR_PTR32

   ptr: __ptr32


.. py:data:: TAPTR_PTR64

   ptr: __ptr64


.. py:data:: TAPTR_RESTRICT

   ptr: __restrict


.. py:data:: TAPTR_SHIFTED

   ptr: __shifted(parent_struct, delta)


.. py:data:: TAENUM_64BIT

   enum: store 64-bit values


.. py:data:: TAENUM_UNSIGNED

   enum: unsigned


.. py:data:: TAENUM_SIGNED

   enum: signed


.. py:data:: TAENUM_OCT

   enum: octal representation, if BTE_HEX


.. py:data:: TAENUM_BIN

   enum: binary representation, if BTE_HEX only one of OCT/BIN bits can be set. they are meaningful only if BTE_HEX is used. 
           


.. py:data:: TAENUM_NUMSIGN

   enum: signed representation, if BTE_HEX


.. py:data:: TAENUM_LZERO

   enum: print numbers with leading zeroes (only for HEX/OCT/BIN)


.. py:data:: TAH_ALL

   all defined bits


.. py:function:: is_tah_byte(t: type_t) -> bool

   The TAH byte (type attribute header byte) denotes the start of type attributes. (see "tah-typeattrs" in the type bit definitions) 
           


.. py:function:: is_sdacl_byte(t: type_t) -> bool

   Identify an sdacl byte. The first sdacl byte has the following format: 11xx000x. The sdacl bytes are appended to udt fields. They indicate the start of type attributes (as the tah-bytes do). The sdacl bytes are used in the udt headers instead of the tah-byte. This is done for compatibility with old databases, they were already using sdacl bytes in udt headers and as udt field postfixes. (see "sdacl-typeattrs" in the type bit definitions) 
           


.. py:class:: type_attr_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: key
      :type:  str

      one symbol keys are reserved to be used by the kernel the ones starting with an underscore are reserved too 
              



   .. py:attribute:: value
      :type:  bytevec_t

      attribute bytes



.. py:data:: cvar

.. py:data:: TYPE_BASE_MASK

   the low 4 bits define the basic type


.. py:data:: TYPE_FLAGS_MASK

   type flags - they have different meaning depending on the basic type 
           


.. py:data:: TYPE_MODIF_MASK

   modifiers.
   * for BT_ARRAY see Derived type: array
   * BT_VOID can have them ONLY in 'void *' 


           


.. py:data:: TYPE_FULL_MASK

   basic type with type flags


.. py:data:: BT_UNK

   unknown


.. py:data:: BT_VOID

   void


.. py:data:: BTMT_SIZE0

   BT_VOID - normal void; BT_UNK - don't use


.. py:data:: BTMT_SIZE12

   size = 1 byte if BT_VOID; 2 if BT_UNK


.. py:data:: BTMT_SIZE48

   size = 4 bytes if BT_VOID; 8 if BT_UNK


.. py:data:: BTMT_SIZE128

   size = 16 bytes if BT_VOID; unknown if BT_UNK (IN struct alignment - see below) 
           


.. py:data:: BT_INT8

   __int8


.. py:data:: BT_INT16

   __int16


.. py:data:: BT_INT32

   __int32


.. py:data:: BT_INT64

   __int64


.. py:data:: BT_INT128

   __int128 (for alpha & future use)


.. py:data:: BT_INT

   natural int. (size provided by idp module)


.. py:data:: BTMT_UNKSIGN

   unknown signedness


.. py:data:: BTMT_SIGNED

   signed


.. py:data:: BTMT_USIGNED

   unsigned


.. py:data:: BTMT_UNSIGNED

.. py:data:: BTMT_CHAR

   specify char or segment register
   * BT_INT8 - char
   * BT_INT - segment register
   * other BT_INT... - don't use 


           


.. py:data:: BT_BOOL

   bool


.. py:data:: BTMT_DEFBOOL

   size is model specific or unknown(?)


.. py:data:: BTMT_BOOL1

   size 1byte


.. py:data:: BTMT_BOOL2

   size 2bytes - !inf_is_64bit()


.. py:data:: BTMT_BOOL8

   size 8bytes - inf_is_64bit()


.. py:data:: BTMT_BOOL4

   size 4bytes


.. py:data:: BT_FLOAT

   float


.. py:data:: BTMT_FLOAT

   float (4 bytes)


.. py:data:: BTMT_DOUBLE

   double (8 bytes)


.. py:data:: BTMT_LNGDBL

   long double (compiler specific)


.. py:data:: BTMT_SPECFLT

   float (variable size). if processor_t::use_tbyte() then use processor_t::tbyte_size, otherwise 2 bytes 
           


.. py:data:: BT_PTR

   pointer. has the following format: [db sizeof(ptr)]; [tah-typeattrs]; type_t... 
           


.. py:data:: BTMT_DEFPTR

   default for model


.. py:data:: BTMT_NEAR

   near


.. py:data:: BTMT_FAR

   far


.. py:data:: BTMT_CLOSURE

   closure.
   * if ptr to BT_FUNC - __closure. in this case next byte MUST be RESERVED_BYTE, and after it BT_FUNC
   * else the next byte contains sizeof(ptr) allowed values are 1 - ph.max_ptr_size
   * if value is bigger than ph.max_ptr_size, based_ptr_name_and_size() is called to find out the typeinfo 


           


.. py:data:: BT_ARRAY

   array


.. py:data:: BTMT_NONBASED

   set
     array base==0
     format: dt num_elem; [tah-typeattrs]; type_t...
     if num_elem==0 then the array size is unknown

     format: da num_elem, base; [tah-typeattrs]; type_t... 


      


.. py:data:: BTMT_ARRESERV

   reserved bit


.. py:data:: BT_FUNC

   function. format: 
   optional: CM_CC_SPOILED | num_of_spoiled_regs
             if num_of_spoiled_reg == BFA_FUNC_MARKER:
               ::bfa_byte
               if (bfa_byte & BFA_FUNC_EXT_FORMAT) != 0
                ::fti_bits (only low bits: FTI_SPOILED,...,FTI_VIRTUAL)
                num_of_spoiled_reg times: spoiled reg info (see extract_spoiledreg)
               else
                 bfa_byte is function attribute byte (see Function attribute byte...)
             else:
               num_of_spoiled_reg times: spoiled reg info (see extract_spoiledreg)
   cm_t ... calling convention and memory model
   [tah-typeattrs];
   type_t ... return type;
   [serialized argloc_t of returned value (if CM_CC_SPECIAL{PE} && !return void);
   if !CM_CC_VOIDARG:
     dt N (N=number of parameters)
     if ( N == 0 )
     if CM_CC_ELLIPSIS or CM_CC_SPECIALE
         func(...)
       else
         parameters are unknown
     else
       N records:
         type_t ... (i.e. type of each parameter)
         [serialized argloc_t (if CM_CC_SPECIAL{PE})] (i.e. place of each parameter)
         [FAH_BYTE + de( funcarg_t::flags )]  
     


.. py:data:: BTMT_DEFCALL

   call method - default for model or unknown


.. py:data:: BTMT_NEARCALL

   function returns by retn


.. py:data:: BTMT_FARCALL

   function returns by retf


.. py:data:: BTMT_INTCALL

   function returns by iret in this case cc MUST be 'unknown' 
           


.. py:data:: BT_COMPLEX

   struct/union/enum/typedef. format: 
   [dt N (N=field count) if !BTMT_TYPEDEF]
   if N == 0:
     p_string name (unnamed types have names "anon_...")
     [sdacl-typeattrs];
   else, for struct & union:
     if N == 0x7FFE   // Support for high (i.e., > 4095) members count
       N = deserialize_de()
     ALPOW = N & 0x7
     MCNT = N >> 3
     if MCNT == 0
       empty struct
     if ALPOW == 0
       ALIGN = get_default_align()
     else
       ALIGN = (1 << (ALPOW - 1))
     [sdacl-typeattrs];
   else, for enums:
     if N == 0x7FFE   // Support for high enum entries count.
       N = deserialize_de()
     [tah-typeattrs];  
    


.. py:data:: BTMT_STRUCT

   struct: MCNT records: type_t; [sdacl-typeattrs]; 
           


.. py:data:: BTMT_UNION

   union: MCNT records: type_t... 
           


.. py:data:: BTMT_ENUM

   enum: next byte bte_t (see below) N records: de delta(s) OR blocks (see below) 
           


.. py:data:: BTMT_TYPEDEF

   named reference always p_string name 
           


.. py:data:: BT_BITFIELD

   bitfield (only in struct) ['bitmasked' enum see below] next byte is dt ((size in bits << 1) | (unsigned ? 1 : 0)) 
           


.. py:data:: BTMT_BFLDI8

   __int8


.. py:data:: BTMT_BFLDI16

   __int16


.. py:data:: BTMT_BFLDI32

   __int32


.. py:data:: BTMT_BFLDI64

   __int64


.. py:data:: BT_RESERVED

   RESERVED.


.. py:data:: BTM_CONST

   const


.. py:data:: BTM_VOLATILE

   volatile


.. py:data:: BTE_SIZE_MASK

   storage size.
   * if == 0 then inf_get_cc_size_e()
   * else 1 << (n -1) = 1,2,4,8
   * n == 5,6,7 are reserved 


           


.. py:data:: BTE_RESERVED

   must be 0, in order to distinguish from a tah-byte 
           


.. py:data:: BTE_BITMASK

   'subarrays'. In this case ANY record has the following format:
   * 'de' mask (has name)
   * 'dt' cnt
   * cnt records of 'de' values (cnt CAN be 0)



.. py:data:: BTE_OUT_MASK

   output style mask


.. py:data:: BTE_HEX

   hex


.. py:data:: BTE_CHAR

   char or hex


.. py:data:: BTE_SDEC

   signed decimal


.. py:data:: BTE_UDEC

   unsigned decimal


.. py:data:: BTE_ALWAYS

   this bit MUST be present


.. py:data:: BT_SEGREG

   segment register


.. py:data:: BT_UNK_BYTE

   1 byte


.. py:data:: BT_UNK_WORD

   2 bytes


.. py:data:: BT_UNK_DWORD

   4 bytes


.. py:data:: BT_UNK_QWORD

   8 bytes


.. py:data:: BT_UNK_OWORD

   16 bytes


.. py:data:: BT_UNKNOWN

   unknown size - for parameters


.. py:data:: BTF_BYTE

   byte


.. py:data:: BTF_UNK

   unknown


.. py:data:: BTF_VOID

   void


.. py:data:: BTF_INT8

   signed byte


.. py:data:: BTF_CHAR

   signed char


.. py:data:: BTF_UCHAR

   unsigned char


.. py:data:: BTF_UINT8

   unsigned byte


.. py:data:: BTF_INT16

   signed short


.. py:data:: BTF_UINT16

   unsigned short


.. py:data:: BTF_INT32

   signed int


.. py:data:: BTF_UINT32

   unsigned int


.. py:data:: BTF_INT64

   signed long


.. py:data:: BTF_UINT64

   unsigned long


.. py:data:: BTF_INT128

   signed 128-bit value


.. py:data:: BTF_UINT128

   unsigned 128-bit value


.. py:data:: BTF_INT

   int, unknown signedness


.. py:data:: BTF_UINT

   unsigned int


.. py:data:: BTF_SINT

   singed int


.. py:data:: BTF_BOOL

   boolean


.. py:data:: BTF_FLOAT

   float


.. py:data:: BTF_DOUBLE

   double


.. py:data:: BTF_LDOUBLE

   long double


.. py:data:: BTF_TBYTE

   see BTMT_SPECFLT


.. py:data:: BTF_STRUCT

   struct


.. py:data:: BTF_UNION

   union


.. py:data:: BTF_ENUM

   enum


.. py:data:: BTF_TYPEDEF

   typedef


.. py:data:: TA_ORG_TYPEDEF

   the original typedef name (simple string)


.. py:data:: TA_ORG_ARRDIM

   the original array dimension (pack_dd)


.. py:data:: TA_FORMAT

   info about the 'format' argument. 3 times pack_dd: format_functype_t, argument number of 'format', argument number of '...' 
           


.. py:data:: TA_VALUE_REPR

   serialized value_repr_t (used for scalars and arrays)


.. py:function:: append_argloc(out: qtype *, vloc: argloc_t) -> bool

   Serialize argument location 
           


.. py:function:: extract_argloc(vloc: argloc_t, ptype: type_t const **, forbid_stkoff: bool) -> bool

   Deserialize an argument location. Argument FORBID_STKOFF checks location type. It can be used, for example, to check the return location of a function that cannot return a value in the stack 
           


.. py:function:: resolve_typedef(til: til_t, type: type_t const *) -> type_t const *

.. py:function:: is_restype_void(til: til_t, type: type_t const *) -> bool

.. py:function:: is_restype_enum(til: til_t, type: type_t const *) -> bool

.. py:function:: is_restype_struni(til: til_t, type: type_t const *) -> bool

.. py:function:: is_restype_struct(til: til_t, type: type_t const *) -> bool

.. py:function:: get_scalar_bt(size: int) -> type_t

.. py:class:: til_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  char *

      short file name (without path and extension)



   .. py:attribute:: desc
      :type:  char *

      human readable til description



   .. py:attribute:: nbases
      :type:  int

      number of base tils



   .. py:attribute:: flags
      :type:  int

      Type info library property bits 
              



   .. py:method:: is_dirty() -> bool

      Has the til been modified? (TIL_MOD)



   .. py:method:: set_dirty() -> None

      Mark the til as modified (TIL_MOD)



   .. py:method:: find_base(n: str) -> til_t *

      Find the base til with the provided name 
              
      :param n: the base til name
      :returns: the found til_t, or nullptr



   .. py:attribute:: cc
      :type:  compiler_info_t

      information about the target compiler



   .. py:attribute:: nrefs
      :type:  int

      number of references to the til



   .. py:attribute:: nstreams
      :type:  int

      number of extra streams



   .. py:attribute:: streams
      :type:  til_stream_t **

      symbol stream storage



   .. py:method:: base(n: int) -> til_t *


   .. py:method:: import_type(src)

      Import a type (and all its dependencies) into this type info library.

      :param src: The type to import
      :returns: the imported copy, or None



   .. py:method:: named_types()

      Returns a generator over the named types contained in this
      type library.

      Every iteration returns a fresh new tinfo_t object

      :returns: a tinfo_t-producing generator



   .. py:method:: numbered_types()

      Returns a generator over the numbered types contained in this
      type library.

      Every iteration returns a fresh new tinfo_t object

      :returns: a tinfo_t-producing generator



   .. py:method:: get_named_type(name)

      Retrieves a tinfo_t representing the named type in this type library.

      :param name: a type name
      :returns: a new tinfo_t object, or None if not found



   .. py:method:: get_numbered_type(ordinal)

      Retrieves a tinfo_t representing the numbered type in this type library.

      :param ordinal: a type ordinal
      :returns: a new tinfo_t object, or None if not found



   .. py:method:: get_type_names()


   .. py:attribute:: type_names


.. py:data:: no_sign

   no sign, or unknown


.. py:data:: type_signed

   signed type


.. py:data:: type_unsigned

   unsigned type


.. py:data:: TIL_ZIP

   pack buckets using zip


.. py:data:: TIL_MAC

   til has macro table


.. py:data:: TIL_ESI

   extended sizeof info (short, long, longlong)


.. py:data:: TIL_UNI

   universal til for any compiler


.. py:data:: TIL_ORD

   type ordinal numbers are present


.. py:data:: TIL_ALI

   type aliases are present (this bit is used only on the disk)


.. py:data:: TIL_MOD

   til has been modified, should be saved


.. py:data:: TIL_STM

   til has extra streams


.. py:data:: TIL_SLD

   sizeof(long double)


.. py:data:: TIL_ECC

   extended callcnv_t


.. py:function:: new_til(name: str, desc: str) -> til_t *

   Initialize a til.


.. py:data:: TIL_ADD_FAILED

   see errbuf


.. py:data:: TIL_ADD_OK

   some tils were added


.. py:data:: TIL_ADD_ALREADY

   the base til was already added


.. py:function:: load_til(name: str, tildir: str = None) -> str

   Load til from a file without adding it to the database list (see also add_til). Failure to load base tils are reported into 'errbuf'. They do not prevent loading of the main til. 
           
   :param name: filename of the til. If it's an absolute path, tildir is ignored.
   * NB: the file extension is forced to .til
   :param tildir: directory where to load the til from. nullptr means default til subdirectories.
   :returns: pointer to resulting til, nullptr if failed and error message is in errbuf


.. py:function:: compact_til(ti: til_t) -> bool

   Collect garbage in til. Must be called before storing the til. 
           
   :returns: true if any memory was freed


.. py:function:: store_til(ti: til_t, tildir: str, name: str) -> bool

   Store til to a file. If the til contains garbage, it will be collected before storing the til. Your plugin should call compact_til() before calling store_til(). 
           
   :param ti: type library to store
   :param tildir: directory where to store the til. nullptr means current directory.
   :param name: filename of the til. If it's an absolute path, tildir is ignored.
   * NB: the file extension is forced to .til
   :returns: success


.. py:function:: free_til(ti: til_t) -> None

   Free memory allocated by til.


.. py:function:: load_til_header(tildir: str, name: str) -> str

   Get human-readable til description.


.. py:function:: is_code_far(cm: cm_t) -> bool

   Does the given model specify far code?.


.. py:function:: is_data_far(cm: cm_t) -> bool

   Does the given model specify far data?.


.. py:class:: rrel_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: off
      :type:  int

      displacement from the address pointed by the register



   .. py:attribute:: reg
      :type:  int

      register index (into ph.reg_names)



.. py:data:: CM_MASK

.. py:data:: CM_UNKNOWN

   unknown


.. py:data:: CM_N8_F16

   if sizeof(int)<=2: near 1 byte, far 2 bytes


.. py:data:: CM_N64

   if sizeof(int)>2: near 8 bytes, far 8 bytes


.. py:data:: CM_N16_F32

   near 2 bytes, far 4 bytes


.. py:data:: CM_N32_F48

   near 4 bytes, far 6 bytes


.. py:data:: CM_M_MASK

.. py:data:: CM_M_NN

   small: code=near, data=near (or unknown if CM_UNKNOWN)


.. py:data:: CM_M_FF

   large: code=far, data=far


.. py:data:: CM_M_NF

   compact: code=near, data=far


.. py:data:: CM_M_FN

   medium: code=far, data=near


.. py:data:: CM_CC_MASK

.. py:data:: CM_CC_INVALID

   this value is invalid


.. py:data:: CM_CC_UNKNOWN

   unknown calling convention


.. py:data:: CM_CC_VOIDARG

   function without arguments if has other cc and argnum == 0, represent as f() - unknown list 
           


.. py:data:: CM_CC_CDECL

   stack


.. py:data:: CM_CC_ELLIPSIS

   cdecl + ellipsis


.. py:data:: CM_CC_STDCALL

   stack, purged


.. py:data:: CM_CC_PASCAL

   stack, purged, reverse order of args


.. py:data:: CM_CC_FASTCALL

   stack, purged (x86), first args are in regs (compiler-dependent)


.. py:data:: CM_CC_THISCALL

   stack, purged (x86), first arg is in reg (compiler-dependent)


.. py:data:: CM_CC_SWIFT

   (Swift) arguments and return values in registers (compiler-dependent)


.. py:data:: CM_CC_SPOILED

   This is NOT a cc! Mark of __spoil record the low nibble is count and after n {spoilreg_t} present real cm_t byte. if n == BFA_FUNC_MARKER, the next byte is the function attribute byte. 
           


.. py:data:: CM_CC_GOLANG

   (Go) arguments and return value reg/stack depending on version


.. py:data:: CM_CC_RESERVE3

   reserved; used for internal needs


.. py:data:: CM_CC_SPECIALE

   CM_CC_SPECIAL with ellipsis


.. py:data:: CM_CC_SPECIALP

   Equal to CM_CC_SPECIAL, but with purged stack.


.. py:data:: CM_CC_SPECIAL

   usercall: locations of all arguments and the return value are explicitly specified 
           


.. py:data:: CM_CC_LAST_USERCALL

.. py:data:: CM_CC_GOSTK

   (Go) arguments and return value in stack


.. py:data:: CM_CC_FIRST_PLAIN_CUSTOM

.. py:data:: BFA_NORET

   __noreturn


.. py:data:: BFA_PURE

   __pure


.. py:data:: BFA_HIGH

   high level prototype (with possibly hidden args)


.. py:data:: BFA_STATIC

   static


.. py:data:: BFA_VIRTUAL

   virtual


.. py:data:: BFA_FUNC_MARKER

   This is NOT a cc! (used internally as a marker)


.. py:data:: BFA_FUNC_EXT_FORMAT

   This is NOT a real attribute (used internally as marker for extended format)


.. py:data:: ALOC_NONE

   none


.. py:data:: ALOC_STACK

   stack offset


.. py:data:: ALOC_DIST

   distributed (scattered)


.. py:data:: ALOC_REG1

   one register (and offset within it)


.. py:data:: ALOC_REG2

   register pair


.. py:data:: ALOC_RREL

   register relative


.. py:data:: ALOC_STATIC

   global address


.. py:data:: ALOC_CUSTOM

   custom argloc (7 or higher)


.. py:class:: argloc_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: swap(r: argloc_t) -> None

      Assign this == r and r == this.



   .. py:method:: atype() -> argloc_type_t

      Get type (Argument location types)



   .. py:method:: is_reg1() -> bool

      See ALOC_REG1.



   .. py:method:: is_reg2() -> bool

      See ALOC_REG2.



   .. py:method:: is_reg() -> bool

      is_reg1() || is_reg2()



   .. py:method:: is_rrel() -> bool

      See ALOC_RREL.



   .. py:method:: is_ea() -> bool

      See ALOC_STATIC.



   .. py:method:: is_stkoff() -> bool

      See ALOC_STACK.



   .. py:method:: is_scattered() -> bool

      See ALOC_DIST.



   .. py:method:: has_reg() -> bool

      TRUE if argloc has a register part.



   .. py:method:: has_stkoff() -> bool

      TRUE if argloc has a stack part.



   .. py:method:: is_mixed_scattered() -> bool

      mixed scattered: consists of register and stack parts



   .. py:method:: in_stack() -> bool

      TRUE if argloc is in stack entirely.



   .. py:method:: is_fragmented() -> bool

      is_scattered() || is_reg2()



   .. py:method:: is_custom() -> bool

      See ALOC_CUSTOM.



   .. py:method:: is_badloc() -> bool

      See ALOC_NONE.



   .. py:method:: reg1() -> int

      Get the register info. Use when atype() == ALOC_REG1 or ALOC_REG2 
              



   .. py:method:: regoff() -> int

      Get offset from the beginning of the register in bytes. Use when atype() == ALOC_REG1 
              



   .. py:method:: reg2() -> int

      Get info for the second register. Use when atype() == ALOC_REG2 
              



   .. py:method:: get_reginfo() -> int

      Get all register info. Use when atype() == ALOC_REG1 or ALOC_REG2 
              



   .. py:method:: stkoff() -> int

      Get the stack offset. Use if atype() == ALOC_STACK 
              



   .. py:method:: get_ea() -> ida_idaapi.ea_t

      Get the global address. Use when atype() == ALOC_STATIC 
              



   .. py:method:: scattered() -> scattered_aloc_t &

      Get scattered argument info. Use when atype() == ALOC_DIST 
              



   .. py:method:: get_rrel() -> rrel_t &

      Get register-relative info. Use when atype() == ALOC_RREL 
              



   .. py:method:: get_custom() -> void *

      Get custom argloc info. Use if atype() == ALOC_CUSTOM 
              



   .. py:method:: get_biggest() -> argloc_t::biggest_t

      Get largest element in internal union.



   .. py:method:: set_reg1(reg: int, off: int = 0) -> None

      Set register location.



   .. py:method:: set_reg2(_reg1: int, _reg2: int) -> None

      Set secondary register location.



   .. py:method:: set_stkoff(off: int) -> None

      Set stack offset location.



   .. py:method:: set_ea(_ea: ida_idaapi.ea_t) -> None

      Set static ea location.



   .. py:method:: consume_rrel(p: rrel_t) -> None

      Set register-relative location - can't be nullptr.



   .. py:method:: set_badloc() -> None

      Set to invalid location.



   .. py:method:: calc_offset() -> int

      Calculate offset that can be used to compare 2 similar arglocs.



   .. py:method:: advance(delta: int) -> bool

      Move the location to point 'delta' bytes further.



   .. py:method:: align_reg_high(size: size_t, _slotsize: size_t) -> None

      Set register offset to align it to the upper part of _SLOTSIZE.



   .. py:method:: align_stkoff_high(size: size_t, _slotsize: size_t) -> None

      Set stack offset to align to the upper part of _SLOTSIZE.



   .. py:method:: compare(r: argloc_t) -> int


   .. py:method:: consume_scattered(p: scattered_aloc_t) -> None

      Set distributed argument location.



.. py:class:: argpart_t(*args)

   Bases: :py:obj:`argloc_t`


   .. py:attribute:: thisown


   .. py:attribute:: off
      :type:  ushort

      offset from the beginning of the argument



   .. py:attribute:: size
      :type:  ushort

      the number of bytes



   .. py:method:: bad_offset() -> bool

      Does this argpart have a valid offset?



   .. py:method:: bad_size() -> bool

      Does this argpart have a valid size?



   .. py:method:: swap(r: argpart_t) -> None

      Assign this = r and r = this.



.. py:class:: scattered_aloc_t

   Bases: :py:obj:`argpartvec_t`


   .. py:attribute:: thisown


.. py:function:: verify_argloc(vloc: argloc_t, size: int, gaps: rangeset_t) -> int

   Verify argloc_t. 
           
   :param vloc: argloc to verify
   :param size: total size of the variable
   :param gaps: if not nullptr, specifies gaps in structure definition. these gaps should not map to any argloc, but everything else must be covered
   :returns: 0 if ok, otherwise an interr code.


.. py:function:: optimize_argloc(vloc: argloc_t, size: int, gaps: rangeset_t) -> bool

   Verify and optimize scattered argloc into simple form. All new arglocs must be processed by this function. 
           
   :returns: true: success
   :returns: false: the input argloc was illegal


.. py:function:: print_argloc(vloc: argloc_t, size: int = 0, vflags: int = 0) -> size_t

   Convert an argloc to human readable form.


.. py:data:: PRALOC_VERIFY

   interr if illegal argloc


.. py:data:: PRALOC_STKOFF

   print stack offsets


.. py:class:: aloc_visitor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: visit_location(v: argloc_t, off: int, size: int) -> int


.. py:function:: for_all_arglocs(vv: aloc_visitor_t, vloc: argloc_t, size: int, off: int = 0) -> int

   Compress larger argloc types and initiate the aloc visitor.


.. py:class:: const_aloc_visitor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: visit_location(v: argloc_t, off: int, size: int) -> int


.. py:function:: for_all_const_arglocs(vv: const_aloc_visitor_t, vloc: argloc_t, size: int, off: int = 0) -> int

   See for_all_arglocs()


.. py:function:: is_user_cc(cc: callcnv_t) -> bool

   Does the calling convention specify argument locations explicitly?


.. py:function:: is_vararg_cc(cc: callcnv_t) -> bool

   Does the calling convention use ellipsis?


.. py:function:: is_purging_cc(cc: callcnv_t) -> bool

   Does the calling convention clean the stack arguments upon return?. 
           


.. py:function:: is_golang_cc(cc: callcnv_t) -> bool

   GO language calling convention (return value in stack)?


.. py:function:: is_custom_callcnv(cc: callcnv_t) -> bool

   Is custom calling convention?


.. py:function:: is_swift_cc(cc: callcnv_t) -> bool

   Swift calling convention (arguments and return values in registers)?


.. py:function:: get_stkarg_area_info(out: stkarg_area_info_t, cc: callcnv_t) -> bool

   Some calling conventions foresee special areas on the stack for call arguments. This structure lists their sizes. 
           


.. py:class:: stkarg_area_info_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: cb
      :type:  size_t


   .. py:attribute:: stkarg_offset
      :type:  int

      Offset from the SP to the first stack argument (can include linkage area) examples: pc: 0, hppa: -0x34, ppc aix: 0x18 
              



   .. py:attribute:: shadow_size
      :type:  int

      Size of the shadow area. explanations at: [https://stackoverflow.com/questions/30190132/what-is-the-shadow-space-in-x64-assembly](https://stackoverflow.com/questions/30190132/what-is-the-shadow-space-in-x64-assembly) examples: x64 Visual Studio C++: 0x20, x64 gcc: 0, ppc aix: 0x20 
              



   .. py:attribute:: linkage_area
      :type:  int

      Size of the linkage area. explanations at: [https://www.ibm.com/docs/en/xl-fortran-aix/16.1.0?topic=conventions-linkage-area](https://www.ibm.com/docs/en/xl-fortran-aix/16.1.0?topic=conventions-linkage-area) examples: pc: 0, hppa: 0, ppc aix: 0x18 (equal to stkarg_offset) 
              



.. py:data:: C_PC_TINY

.. py:data:: C_PC_SMALL

.. py:data:: C_PC_COMPACT

.. py:data:: C_PC_MEDIUM

.. py:data:: C_PC_LARGE

.. py:data:: C_PC_HUGE

.. py:data:: C_PC_FLAT

.. py:class:: custom_callcnv_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: flags
      :type:  uint64


   .. py:attribute:: name
      :type:  str

      the name is used as a keyword in the function prototype



   .. py:attribute:: abibits
      :type:  int

      abibits to be used for the calling convention



   .. py:method:: is_vararg() -> bool


   .. py:method:: is_purging() -> bool


   .. py:method:: is_usercall() -> bool


   .. py:method:: validate_func(fti: func_type_data_t, reterr: str) -> bool

      Validate a function prototype. This function is used during parsing or deserializing a function prototype to verify semantic limitations of the prototype (for example, returning arrays is forbidden in C) 
              
      :param fti: function prototype
      :param reterr: buffer for error message



   .. py:method:: calc_retloc(fti: func_type_data_t) -> bool

      Calculate the location of the return value. This function must fill fti->retloc. 
              
      :param fti: function prototype
      :returns: success



   .. py:method:: calc_arglocs(fti: func_type_data_t) -> bool

      Calculate the argument locations. This function must fill all fti->at(i).argloc instances. It may be called for variadic functions too, in calc_varglocs fails. 
              
      :param fti: function prototype
      :returns: success



   .. py:method:: find_varargs(fti: func_type_data_t, call_ea: ida_idaapi.ea_t, blk: mblock_t *) -> ssize_t

      Discover variadic arguments. This function is called only for variadic functions. It is currently used by the decompiler. 
              
      :param fti: function prototype. find_varargs() should append the discovered variadic arguments to it.
      :param call_ea: address of the call instruction
      :param blk: microcode block with the call instruction
      :returns: >0 - total number of arguments after the call <0 - failure ==0 - means to use the standard algorithm to discover variadic args



   .. py:method:: calc_varglocs(fti: func_type_data_t, regs: regobjs_t, stkargs: relobj_t, nfixed: int) -> bool

      Calculate the argument locations for a variadic function. This function must fill all fti->at(i).argloc instances and provide more detailed info about registers and stkargs. 
              
      :param fti: function prototype
      :param regs: buffer for hidden register arguments, may be nullptr
      :param stkargs: buffer for hidden stack arguments, may be nullptr
      :param nfixed: number of fixed arguments
      :returns: success



   .. py:method:: get_cc_regs(out: callregs_t) -> bool

      Retrieve generic information about call registers.



   .. py:method:: get_stkarg_area_info(out: stkarg_area_info_t) -> bool

      Retrieve generic information about stack arguments.



   .. py:method:: calc_purged_bytes(*args) -> int

      Calculate the number of purged bytes 
              
      :param fti: function prototype
      :param call_ea: address of the call instruction (not used yet)



   .. py:method:: decorate_name(name: str, should_decorate: bool, cc: callcnv_t, type: tinfo_t) -> bool

      Function to be overloaded for custom calling conventions.

      Decorate a function name. Some compilers decorate names depending on the calling convention. This function provides the means to handle it for custom callcnvs. Please note that this is about name decoration (C), not name mangling (C++). 
              



   .. py:method:: lower_func_type(fti: func_type_data_t) -> int

      Lower a function type. See lower_type() for more explanations. 
              
      :param fti: function prototype
      :returns: <0-failure, >=0-ok, 2-made substantial changes



.. py:data:: CCI_VARARG

   is variadic?


.. py:data:: CCI_PURGE

   purges arguments?


.. py:data:: CCI_USER

   is usercall? not tested


.. py:function:: get_custom_callcnv(callcnv: callcnv_t) -> custom_callcnv_t const *

   Retrieve custom calling convention details.


.. py:function:: find_custom_callcnv(name: str) -> callcnv_t

   Find a calling convention by its name 
           
   :returns: CM_CC_INVALID is not found


.. py:function:: get_custom_callcnvs(names: qstrvec_t *, codes: callcnvs_t *) -> size_t

   Get all custom calling conventions 
           
   :param names: output buffer for the convention names
   :param codes: output buffer for the convention codes The two output buffers correspond to each other.
   :returns: number of the calling conventions added to the output buffers


.. py:data:: ARGREGS_POLICY_UNDEFINED

.. py:data:: ARGREGS_GP_ONLY

   GP registers used for all arguments.


.. py:data:: ARGREGS_INDEPENDENT

   FP/GP registers used separately (like gcc64)


.. py:data:: ARGREGS_BY_SLOTS

   fixed FP/GP register per each slot (like vc64)


.. py:data:: ARGREGS_FP_MASKS_GP

   FP register also consumes one or more GP regs but not vice versa (aix ppc ABI)


.. py:data:: ARGREGS_MIPS_O32

   MIPS ABI o32.


.. py:data:: ARGREGS_RISCV

   Risc-V API FP arguments are passed in GP registers if FP registers are exhausted and GP ones are not. Wide FP arguments are passed in GP registers. Variadic FP arguments are passed in GP registers. 
             


.. py:class:: callregs_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: policy
      :type:  argreg_policy_t

      argument policy



   .. py:attribute:: nregs
      :type:  int

      max number of registers that can be used in a call



   .. py:attribute:: gpregs
      :type:  intvec_t

      array of gp registers (general purpose)



   .. py:attribute:: fpregs
      :type:  intvec_t

      array of fp registers (floating point)



   .. py:method:: swap(r: callregs_t) -> None

      swap two instances



   .. py:method:: init_regs(cc: callcnv_t) -> bool

      Init policy & registers for given CC.



   .. py:method:: by_slots() -> bool


   .. py:method:: set(_policy: argreg_policy_t, gprs: int const *, fprs: int const *) -> None

      Init policy & registers (arrays are -1-terminated)



   .. py:attribute:: GPREGS


   .. py:attribute:: FPREGS


   .. py:method:: append_registers(kind: callregs_t::reg_kind_t, first_reg: int, last_reg: int) -> None


   .. py:method:: set_registers(kind: callregs_t::reg_kind_t, first_reg: int, last_reg: int) -> None


   .. py:method:: reset() -> None

      Set policy and registers to invalid values.



   .. py:method:: regcount(cc: callcnv_t) -> int
      :staticmethod:


      Get max number of registers may be used in a function call.



   .. py:method:: reginds(gp_ind: int *, fp_ind: int *, r: int) -> bool

      Get register indexes within GP/FP arrays. (-1 -> is not present in the corresponding array) 
              



.. py:function:: get_comp(comp: comp_t) -> comp_t

   Get compiler bits.


.. py:function:: get_compiler_name(id: comp_t) -> str

   Get full compiler name.


.. py:function:: get_compiler_abbr(id: comp_t) -> str

   Get abbreviated compiler name.


.. py:function:: get_compilers(ids: compvec_t *, names: qstrvec_t *, abbrs: qstrvec_t *) -> None

   Get names of all built-in compilers.


.. py:function:: is_comp_unsure(comp: comp_t) -> comp_t

   See COMP_UNSURE.


.. py:function:: default_compiler() -> comp_t

   Get compiler specified by inf.cc.


.. py:function:: is_gcc() -> bool

   Is the target compiler COMP_GNU?


.. py:function:: is_gcc32() -> bool

   Is the target compiler 32 bit gcc?


.. py:function:: is_gcc64() -> bool

   Is the target compiler 64 bit gcc?


.. py:function:: gcc_layout() -> bool

   Should use the struct/union layout as done by gcc?


.. py:function:: set_compiler(cc: compiler_info_t, flags: int, abiname: str = None) -> bool

   Change current compiler. 
           
   :param cc: compiler to switch to
   :param flags: Set compiler flags
   :param abiname: ABI name
   :returns: success


.. py:data:: SETCOMP_OVERRIDE

   may override old compiler info


.. py:data:: SETCOMP_ONLY_ID

   cc has only 'id' field; the rest will be set to defaults corresponding to the program bitness 
           


.. py:data:: SETCOMP_ONLY_ABI

   ignore cc field complete, use only abiname


.. py:data:: SETCOMP_BY_USER

   invoked by user, cannot be replaced by module/loader


.. py:function:: set_compiler_id(id: comp_t, abiname: str = None) -> bool

   Set the compiler id (see Compiler IDs)


.. py:function:: set_abi_name(abiname: str, user_level: bool = False) -> bool

   Set abi name (see Compiler IDs)


.. py:function:: get_abi_name() -> str

   Get ABI name. 
           
   :returns: length of the name (>=0)


.. py:function:: append_abi_opts(abi_opts: str, user_level: bool = False) -> bool

   Add/remove/check ABI option General form of full abi name: abiname-opt1-opt2-... or -opt1-opt2-... 
           
   :param abi_opts: - ABI options to add/remove in form opt1-opt2-...
   :param user_level: - initiated by user if TRUE (==SETCOMP_BY_USER)
   :returns: success


.. py:function:: remove_abi_opts(abi_opts: str, user_level: bool = False) -> bool

.. py:function:: set_compiler_string(compstr: str, user_level: bool) -> bool

   :param compstr: - compiler description in form <abbr>:<abiname>
   :param user_level: - initiated by user if TRUE
   :returns: success


.. py:function:: use_golang_cc() -> bool

   is GOLANG calling convention used by default?


.. py:function:: switch_to_golang() -> None

   switch to GOLANG calling convention (to be used as default CC)


.. py:data:: MAX_FUNC_ARGS

   max number of function arguments


.. py:data:: ABS_UNK

.. py:data:: ABS_NO

.. py:data:: ABS_YES

.. py:data:: SC_UNK

   unknown


.. py:data:: SC_TYPE

   typedef


.. py:data:: SC_EXT

   extern


.. py:data:: SC_STAT

   static


.. py:data:: SC_REG

   register


.. py:data:: SC_AUTO

   auto


.. py:data:: SC_FRIEND

   friend


.. py:data:: SC_VIRT

   virtual


.. py:data:: HTI_CPP

   C++ mode (not implemented)


.. py:data:: HTI_INT

   debug: print internal representation of types


.. py:data:: HTI_EXT

   debug: print external representation of types


.. py:data:: HTI_LEX

   debug: print tokens


.. py:data:: HTI_UNP

   debug: check the result by unpacking it


.. py:data:: HTI_TST

   test mode: discard the result


.. py:data:: HTI_FIL

   "input" is file name, otherwise "input" contains a C declaration 
           


.. py:data:: HTI_MAC

   define macros from the base tils


.. py:data:: HTI_NWR

   no warning messages


.. py:data:: HTI_NER

   ignore all errors but display them


.. py:data:: HTI_DCL

   don't complain about redeclarations


.. py:data:: HTI_NDC

   don't decorate names


.. py:data:: HTI_PAK

   explicit structure pack value (#pragma pack)


.. py:data:: HTI_PAK_SHIFT

   shift for HTI_PAK. This field should be used if you want to remember an explicit pack value for each structure/union type. See HTI_PAK... definitions 
           


.. py:data:: HTI_PAKDEF

   default pack value


.. py:data:: HTI_PAK1

   #pragma pack(1)


.. py:data:: HTI_PAK2

   #pragma pack(2)


.. py:data:: HTI_PAK4

   #pragma pack(4)


.. py:data:: HTI_PAK8

   #pragma pack(8)


.. py:data:: HTI_PAK16

   #pragma pack(16)


.. py:data:: HTI_HIGH

   assume high level prototypes (with hidden args, etc) 
           


.. py:data:: HTI_LOWER

   lower the function prototypes


.. py:data:: HTI_RAWARGS

   leave argument names unchanged (do not remove underscores)


.. py:data:: HTI_RELAXED

   accept references to unknown namespaces


.. py:data:: HTI_NOBASE

   do not inspect base tils


.. py:data:: HTI_SEMICOLON

   do not complain if the terminating semicolon is absent


.. py:data:: HTI_STANDALONE

   should parse standalone declaration, it may contain qualified name and type names, strictly speaking it is not a valid C++ code, IDA Pro specific 
           


.. py:function:: convert_pt_flags_to_hti(pt_flags: int) -> int

   Convert Type parsing flags to Type formatting flags. Type parsing flags lesser than 0x10 don't have stable meaning and will be ignored (more on these flags can be seen in idc.idc) 
           


.. py:function:: parse_decl(out_tif: tinfo_t, til: til_t, decl: str, pt_flags: int) -> str

   Parse ONE declaration. If the input string contains more than one declaration, the first complete type declaration (PT_TYP) or the last variable declaration (PT_VAR) will be used. 
           
   :param out_tif: type info
   :param til: type library to use. may be nullptr
   :param decl: C declaration to parse
   :param pt_flags: combination of Type parsing flags bits
   :returns: true: ok
   :returns: false: declaration is bad, the error message is displayed if !PT_SIL


.. py:data:: PT_SIL

   silent, no messages


.. py:data:: PT_NDC

   don't decorate names


.. py:data:: PT_TYP

   return declared type information


.. py:data:: PT_VAR

   return declared object information


.. py:data:: PT_PACKMASK

   mask for pack alignment values


.. py:data:: PT_HIGH

   assume high level prototypes (with hidden args, etc) 
           


.. py:data:: PT_LOWER

   lower the function prototypes


.. py:data:: PT_REPLACE

   replace the old type (used in idc)


.. py:data:: PT_RAWARGS

   leave argument names unchanged (do not remove underscores)


.. py:data:: PT_RELAXED

   accept references to unknown namespaces


.. py:data:: PT_EMPTY

   accept empty decl


.. py:data:: PT_SEMICOLON

   append the terminating semicolon


.. py:data:: PT_SYMBOL

   accept a symbol name and return its type. e.g. "LoadLibrary" will return its prototype 
           


.. py:function:: parse_decls(til: til_t, input: str, printer: printer_t *, hti_flags: int) -> int

   Parse many declarations and store them in a til. If there are any errors, they will be printed using 'printer'. This function uses default include path and predefined macros from the database settings. It always uses the HTI_DCL bit. 
           
   :param til: type library to store the result
   :param input: input string or file name (see hti_flags)
   :param printer: function to output error messages (use msg or nullptr or your own callback)
   :param hti_flags: combination of Type formatting flags
   :returns: number of errors, 0 means ok.


.. py:function:: print_type(ea: ida_idaapi.ea_t, prtype_flags: int) -> str

   Get type declaration for the specified address. 
           
   :param ea: address
   :param prtype_flags: combination of Type printing flags
   :returns: success


.. py:data:: PRTYPE_1LINE

   print to one line


.. py:data:: PRTYPE_MULTI

   print to many lines


.. py:data:: PRTYPE_TYPE

   print type declaration (not variable declaration)


.. py:data:: PRTYPE_PRAGMA

   print pragmas for alignment


.. py:data:: PRTYPE_SEMI

   append ; to the end


.. py:data:: PRTYPE_CPP

   use c++ name (only for print_type())


.. py:data:: PRTYPE_DEF

   tinfo_t: print definition, if available


.. py:data:: PRTYPE_NOARGS

   tinfo_t: do not print function argument names


.. py:data:: PRTYPE_NOARRS

   tinfo_t: print arguments with FAI_ARRAY as pointers


.. py:data:: PRTYPE_NORES

   tinfo_t: never resolve types (meaningful with PRTYPE_DEF)


.. py:data:: PRTYPE_RESTORE

   tinfo_t: print restored types for FAI_ARRAY and FAI_STRUCT


.. py:data:: PRTYPE_NOREGEX

   do not apply regular expressions to beautify name


.. py:data:: PRTYPE_COLORED

   add color tag COLOR_SYMBOL for any parentheses, commas and colons


.. py:data:: PRTYPE_METHODS

   tinfo_t: print udt methods


.. py:data:: PRTYPE_1LINCMT

   print comments even in the one line mode


.. py:data:: PRTYPE_HEADER

   print only type header (only for definitions)


.. py:data:: PRTYPE_OFFSETS

   print udt member offsets


.. py:data:: PRTYPE_MAXSTR

   limit the output length to 1024 bytes (the output may be slightly longer)


.. py:data:: PRTYPE_TAIL

   print only the definition tail (only for definitions, exclusive with PRTYPE_HEADER)


.. py:data:: PRTYPE_ARGLOCS

   print function arglocs (not only for usercall)


.. py:data:: NTF_TYPE

   type name


.. py:data:: NTF_SYMU

   symbol, name is unmangled ('func')


.. py:data:: NTF_SYMM

   symbol, name is mangled ('_func'); only one of NTF_TYPE and NTF_SYMU, NTF_SYMM can be used 
           


.. py:data:: NTF_NOBASE

   don't inspect base tils (for get_named_type)


.. py:data:: NTF_REPLACE

   replace original type (for set_named_type)


.. py:data:: NTF_UMANGLED

   name is unmangled (don't use this flag)


.. py:data:: NTF_NOCUR

   don't inspect current til file (for get_named_type)


.. py:data:: NTF_64BIT

   value is 64bit


.. py:data:: NTF_FIXNAME

   force-validate the name of the type when setting (set_named_type, set_numbered_type only) 
           


.. py:data:: NTF_IDBENC

   the name is given in the IDB encoding; non-ASCII bytes will be decoded accordingly (set_named_type, set_numbered_type only) 
           


.. py:data:: NTF_CHKSYNC

   check that synchronization to IDB passed OK (set_numbered_type, set_named_type) 
           


.. py:data:: NTF_NO_NAMECHK

   do not validate type name (set_numbered_type, set_named_type) 
           


.. py:data:: NTF_COPY

   save a new type definition, not a typeref (tinfo_t::set_numbered_type, tinfo_t::set_named_type)


.. py:data:: TERR_OK

   ok


.. py:data:: TERR_SAVE_ERROR

   failed to save


.. py:data:: TERR_SERIALIZE

   failed to serialize


.. py:data:: TERR_BAD_NAME

   name s is not acceptable


.. py:data:: TERR_BAD_ARG

   bad argument


.. py:data:: TERR_BAD_TYPE

   bad type


.. py:data:: TERR_BAD_SIZE

   bad size d


.. py:data:: TERR_BAD_INDEX

   bad index d


.. py:data:: TERR_BAD_ARRAY

   arrays are forbidden as function arguments


.. py:data:: TERR_BAD_BF

   bitfields are forbidden as function arguments


.. py:data:: TERR_BAD_OFFSET

   bad member offset s


.. py:data:: TERR_BAD_UNIVAR

   unions cannot have variable sized members


.. py:data:: TERR_BAD_VARLAST

   variable sized member must be the last member in the structure


.. py:data:: TERR_OVERLAP

   the member overlaps with other members that cannot be deleted


.. py:data:: TERR_BAD_SUBTYPE

   recursive structure nesting is forbidden


.. py:data:: TERR_BAD_VALUE

   value 0xI64X is not acceptable


.. py:data:: TERR_NO_BMASK

   bitmask 0xI64X is not found


.. py:data:: TERR_BAD_BMASK

   Bad enum member mask 0xI64X. The specified mask should not intersect with any existing mask in the enum. Zero masks are prohibited too.


.. py:data:: TERR_BAD_MSKVAL

   bad bmask and value combination (value=0xI64X; bitmask 0xI64X)


.. py:data:: TERR_BAD_REPR

   bad or incompatible field representation


.. py:data:: TERR_GRP_NOEMPTY

   could not delete group mask for not empty group 0xI64X


.. py:data:: TERR_DUPNAME

   duplicate name s


.. py:data:: TERR_UNION_BF

   unions cannot have bitfields


.. py:data:: TERR_BAD_TAH

   bad bits in the type attributes (TAH bits)


.. py:data:: TERR_BAD_BASE

   bad base class


.. py:data:: TERR_BAD_GAP

   bad gap


.. py:data:: TERR_NESTED

   recursive structure nesting is forbidden


.. py:data:: TERR_NOT_COMPAT

   the new type is not compatible with the old type


.. py:data:: TERR_BAD_LAYOUT

   failed to calculate the structure/union layout


.. py:data:: TERR_BAD_GROUPS

   bad group sizes for bitmask enum


.. py:data:: TERR_BAD_SERIAL

   enum value has too many serials


.. py:data:: TERR_ALIEN_NAME

   enum member name is used in another enum


.. py:data:: TERR_STOCK

   stock type info cannot be modified


.. py:data:: TERR_ENUM_SIZE

   bad enum size


.. py:data:: TERR_NOT_IMPL

   not implemented


.. py:data:: TERR_TYPE_WORSE

   the new type is worse than the old type


.. py:data:: TERR_BAD_FX_SIZE

   cannot extend struct beyond fixed size


.. py:data:: TERR_STRUCT_SIZE

   bad fixed structure size


.. py:data:: TERR_NOT_FOUND

   member not found


.. py:data:: TERR_COUNT

.. py:function:: tinfo_errstr(code: tinfo_code_t) -> str

   Helper function to convert an error code into a printable string. Additional arguments are handled using the functions from err.h 
           


.. py:function:: del_named_type(ti: til_t, name: str, ntf_flags: int) -> bool

   Delete information about a symbol. 
           
   :param ti: type library
   :param name: name of symbol
   :param ntf_flags: combination of Flags for named types
   :returns: success


.. py:function:: first_named_type(ti: til_t, ntf_flags: int) -> str

   Enumerate types. 
           
   :param ti: type library. nullptr means the local type library for the current database.
   :param ntf_flags: combination of Flags for named types
   :returns: Type or symbol names, depending of ntf_flags. Returns mangled names. Never returns anonymous types. To include them, enumerate types by ordinals.


.. py:function:: next_named_type(ti: til_t, name: str, ntf_flags: int) -> str

   Enumerate types. 
           
   :param ti: type library. nullptr means the local type library for the current database.
   :param name: the current name. the name that follows this one will be returned.
   :param ntf_flags: combination of Flags for named types
   :returns: Type or symbol names, depending of ntf_flags. Returns mangled names. Never returns anonymous types. To include them, enumerate types by ordinals.


.. py:function:: copy_named_type(dsttil: til_t, srctil: til_t, name: str) -> int

   Copy a named type from one til to another. This function will copy the specified type and all dependent types from the source type library to the destination library. 
           
   :param dsttil: Destination til. It must have original types enabled
   :param srctil: Source til.
   :param name: name of the type to copy
   :returns: ordinal number of the copied type. 0 means error


.. py:function:: decorate_name(*args) -> str

   Decorate/undecorate a C symbol name. 
           
   :param out: output buffer
   :param name: name of symbol
   :param should_decorate: true-decorate name, false-undecorate
   :param cc: calling convention
   :param type: name type (nullptr-unknown)
   :returns: success


.. py:function:: gen_decorate_name(name: str, should_decorate: bool, cc: callcnv_t, type: tinfo_t) -> str

   Generic function for decorate_name() (may be used in IDP modules)


.. py:function:: calc_c_cpp_name(name: str, type: tinfo_t, ccn_flags: int) -> str

   Get C or C++ form of the name. 
           
   :param name: original (mangled or decorated) name
   :param type: name type if known, otherwise nullptr
   :param ccn_flags: one of C/C++ naming flags


.. py:data:: CCN_C

.. py:data:: CCN_CPP

.. py:function:: enable_numbered_types(ti: til_t, enable: bool) -> bool

   Enable the use of numbered types in til. Currently it is impossible to disable numbered types once they are enabled 
           


.. py:function:: alloc_type_ordinals(ti: til_t, qty: int) -> int

   Allocate a range of ordinal numbers for new types. 
           
   :param ti: type library
   :param qty: number of ordinals to allocate
   :returns: the first ordinal. 0 means failure.


.. py:function:: alloc_type_ordinal(ti: til_t) -> int

   alloc_type_ordinals(ti, 1)


.. py:function:: get_ordinal_limit(ti: til_t = None) -> int

   Get number of allocated ordinals + 1. If there are no allocated ordinals, return 0. To enumerate all ordinals, use: for ( uint32 i = 1; i < limit; ++i ) 
           
   :param ti: type library; nullptr means the local types for the current database.
   :returns: uint32(-1) if ordinals have not been enabled for the til. For local types (idati), ordinals are always enabled.


.. py:function:: get_ordinal_count(ti: til_t = None) -> int

   Get number of allocated ordinals. 
           
   :param ti: type library; nullptr means the local types for the current database.
   :returns: 0 if ordinals have not been enabled for the til.


.. py:function:: del_numbered_type(ti: til_t, ordinal: int) -> bool

   Delete a numbered type.


.. py:function:: set_type_alias(ti: til_t, src_ordinal: int, dst_ordinal: int) -> bool

   Create a type alias. Redirects all references to source type to the destination type. This is equivalent to instantaneous replacement all references to srctype by dsttype. 
           


.. py:function:: get_alias_target(ti: til_t, ordinal: int) -> int

   Find the final alias destination. If the ordinal has not been aliased, return the specified ordinal itself If failed, returns 0. 
           


.. py:function:: get_type_ordinal(ti: til_t, name: str) -> int

   Get type ordinal by its name.


.. py:function:: get_numbered_type_name(ti: til_t, ordinal: int) -> str

   Get type name (if exists) by its ordinal. If the type is anonymous, returns "". If failed, returns nullptr 
           


.. py:function:: create_numbered_type_name(ord: int) -> str

   Create anonymous name for numbered type. This name can be used to reference a numbered type by its ordinal Ordinal names have the following format: '#' + set_de(ord) Returns: -1 if error, otherwise the name length 
           


.. py:function:: is_ordinal_name(name: str, ord: uint32 * = None) -> bool

   Check if the name is an ordinal name. Ordinal names have the following format: '#' + set_de(ord) 
           


.. py:function:: is_type_choosable(ti: til_t, ordinal: int) -> bool

   Check if a struct/union type is choosable 
           
   :param ti: type library
   :param ordinal: ordinal number of a UDT type


.. py:function:: set_type_choosable(ti: til_t, ordinal: int, value: bool) -> None

   Enable/disable 'choosability' flag for a struct/union type 
           
   :param ti: type library
   :param ordinal: ordinal number of a UDT type
   :param value: flag value


.. py:function:: get_vftable_ea(ordinal: int) -> ida_idaapi.ea_t

   Get address of a virtual function table. 
           
   :param ordinal: ordinal number of a vftable type.
   :returns: address of the corresponding virtual function table in the current database.


.. py:function:: get_vftable_ordinal(vftable_ea: ida_idaapi.ea_t) -> int

   Get ordinal number of the virtual function table. 
           
   :param vftable_ea: address of a virtual function table.
   :returns: ordinal number of the corresponding vftable type. 0 - failure.


.. py:function:: set_vftable_ea(ordinal: int, vftable_ea: ida_idaapi.ea_t) -> bool

   Set the address of a vftable instance for a vftable type. 
           
   :param ordinal: ordinal number of the corresponding vftable type.
   :param vftable_ea: address of a virtual function table.
   :returns: success


.. py:function:: del_vftable_ea(ordinal: int) -> bool

   Delete the address of a vftable instance for a vftable type. 
           
   :param ordinal: ordinal number of a vftable type.
   :returns: success


.. py:function:: deref_ptr(ptr_ea: ea_t *, tif: tinfo_t, closure_obj: ea_t * = None) -> bool

   Dereference a pointer. 
           
   :param ptr_ea: in/out parameter
   * in: address of the pointer
   * out: the pointed address
   :param tif: type of the pointer
   :param closure_obj: closure object (not used yet)
   :returns: success


.. py:function:: add_til(name: str, flags: int) -> int

   Load a til file and add it the database type libraries list. IDA will also apply function prototypes for matching function names. 
           
   :param name: til name
   :param flags: combination of Load TIL flags
   :returns: one of Load TIL result codes


.. py:data:: ADDTIL_DEFAULT

   default behavior


.. py:data:: ADDTIL_INCOMP

   load incompatible tils


.. py:data:: ADDTIL_SILENT

   do not ask any questions


.. py:data:: ADDTIL_FAILED

   something bad, the warning is displayed


.. py:data:: ADDTIL_OK

   ok, til is loaded


.. py:data:: ADDTIL_COMP

   ok, but til is not compatible with the current compiler


.. py:data:: ADDTIL_ABORTED

   til was not loaded (incompatible til rejected by user)


.. py:function:: del_til(name: str) -> bool

   Unload a til file.


.. py:function:: apply_named_type(ea: ida_idaapi.ea_t, name: str) -> bool

   Apply the specified named type to the address. 
           
   :param ea: linear address
   :param name: the type name, e.g. "FILE"
   :returns: success


.. py:function:: apply_tinfo(ea: ida_idaapi.ea_t, tif: tinfo_t, flags: int) -> bool

   Apply the specified type to the specified address. This function sets the type and tries to convert the item at the specified address to conform the type. 
           
   :param ea: linear address
   :param tif: new type
   :param flags: combination of Apply tinfo flags
   :returns: success


.. py:data:: TINFO_GUESSED

   this is a guessed type


.. py:data:: TINFO_DEFINITE

   this is a definite type


.. py:data:: TINFO_DELAYFUNC

   if type is a function and no function exists at ea, schedule its creation and argument renaming to auto-analysis, otherwise try to create it immediately 
           


.. py:data:: TINFO_STRICT

   never convert given type to another one before applying


.. py:function:: apply_cdecl(til: til_t, ea: ida_idaapi.ea_t, decl: str, flags: int = 0) -> bool

   Apply the specified type to the address. This function parses the declaration and calls apply_tinfo() 
           
   :param til: type library
   :param ea: linear address
   :param decl: type declaration in C form
   :param flags: flags to pass to apply_tinfo (TINFO_DEFINITE is always passed)
   :returns: success


.. py:function:: apply_callee_tinfo(caller: ida_idaapi.ea_t, tif: tinfo_t) -> bool

   Apply the type of the called function to the calling instruction. This function will append parameter comments and rename the local variables of the calling function. It also stores information about the instructions that initialize call arguments in the database. Use get_arg_addrs() to retrieve it if necessary. Alternatively it is possible to hook to processor_t::arg_addrs_ready event. 
           
   :param caller: linear address of the calling instruction. must belong to a function.
   :param tif: type info
   :returns: success


.. py:function:: apply_once_tinfo_and_name(dea: ida_idaapi.ea_t, tif: tinfo_t, name: str) -> bool

   Apply the specified type and name to the address. This function checks if the address already has a type. If the old type 
   does not exist or the new type is 'better' than the old type, then the 
   new type will be applied. A type is considered better if it has more 
   information (e.g. BTMT_STRUCT is better than BT_INT). 
   The same logic is with the name: if the address already have a meaningful 
   name, it will be preserved. Only if the old name does not exist or it 
   is a dummy name like byte_123, it will be replaced by the new name. 
           
   :param dea: linear address
   :param tif: new type
   :param name: new name for the address
   :returns: success


.. py:function:: guess_tinfo(out: tinfo_t, id: tid_t) -> int

   Generate a type information about the id from the disassembly. id can be a structure/union/enum id or an address. 
           
   :returns: one of Guess tinfo codes


.. py:data:: GUESS_FUNC_FAILED

   couldn't guess the function type


.. py:data:: GUESS_FUNC_TRIVIAL

   the function type doesn't have interesting info


.. py:data:: GUESS_FUNC_OK

   ok, some non-trivial information is gathered


.. py:function:: set_c_header_path(incdir: str) -> None

   Set include directory path the target compiler.


.. py:function:: get_c_header_path() -> str

   Get the include directory path of the target compiler.


.. py:function:: set_c_macros(macros: str) -> None

   Set predefined macros for the target compiler.


.. py:function:: get_c_macros() -> str

   Get predefined macros for the target compiler.


.. py:function:: get_idati() -> til_t *

   Pointer to the local type library - this til is private for each IDB file Functions that accept til_t* default to `idati` when is nullptr provided. 
           


.. py:function:: get_idainfo_by_type(tif: tinfo_t) -> size_t *, flags64_t *, opinfo_t *, size_t *

   Extract information from a tinfo_t. 
           
   :param tif: the type to inspect


.. py:function:: get_tinfo_by_flags(out: tinfo_t, flags: flags64_t) -> bool

   Get tinfo object that corresponds to data flags 
           
   :param out: type info
   :param flags: simple flags (byte, word, ..., zword)


.. py:data:: STI_PCHAR

   char *


.. py:data:: STI_PUCHAR

   uint8 *


.. py:data:: STI_PCCHAR

   const char *


.. py:data:: STI_PCUCHAR

   const uint8 *


.. py:data:: STI_PBYTE

   _BYTE *


.. py:data:: STI_PINT

   int *


.. py:data:: STI_PUINT

   unsigned int *


.. py:data:: STI_PVOID

   void *


.. py:data:: STI_PPVOID

   void **


.. py:data:: STI_PCVOID

   const void *


.. py:data:: STI_ACHAR

   char[]


.. py:data:: STI_AUCHAR

   uint8[]


.. py:data:: STI_ACCHAR

   const char[]


.. py:data:: STI_ACUCHAR

   const uint8[]


.. py:data:: STI_FPURGING

   void __userpurge(int)


.. py:data:: STI_FDELOP

   void __cdecl(void *)


.. py:data:: STI_MSGSEND

   void *(void *, const char *, ...)


.. py:data:: STI_AEABI_LCMP

   int __fastcall __pure(int64 x, int64 y)


.. py:data:: STI_AEABI_ULCMP

   int __fastcall __pure(uint64 x, uint64 y)


.. py:data:: STI_DONT_USE

   unused stock type id; should not be used


.. py:data:: STI_SIZE_T

   size_t


.. py:data:: STI_SSIZE_T

   ssize_t


.. py:data:: STI_AEABI_MEMCPY

   void __fastcall(void *, const void *, size_t)


.. py:data:: STI_AEABI_MEMSET

   void __fastcall(void *, size_t, int)


.. py:data:: STI_AEABI_MEMCLR

   void __fastcall(void *, size_t)


.. py:data:: STI_RTC_CHECK_2

   int16 __fastcall(int16 x)


.. py:data:: STI_RTC_CHECK_4

   int32 __fastcall(int32 x)


.. py:data:: STI_RTC_CHECK_8

   int64 __fastcall(int64 x)


.. py:data:: STI_COMPLEX64

   struct complex64_t { float real, imag; }


.. py:data:: STI_COMPLEX128

   struct complex128_t { double real, imag; }


.. py:data:: STI_PUNKNOWN

   _UNKNOWN *


.. py:data:: STI_LAST

.. py:data:: ETF_NO_SAVE

   don't save to til (normally typerefs are saved to til) A call with ETF_NO_SAVE must be followed by a call without it. Otherwise there may be inconsistencies between the memory and the type library. 
             


.. py:data:: ETF_NO_LAYOUT

   don't calc type layout before editing


.. py:data:: ETF_MAY_DESTROY

   may destroy other members


.. py:data:: ETF_COMPATIBLE

   new type must be compatible with the old


.. py:data:: ETF_FUNCARG

   udm - member is a function argument (cannot create arrays)


.. py:data:: ETF_FORCENAME

   anyway use name, see below for more usage description


.. py:data:: ETF_AUTONAME

   udm - generate a member name if was not specified (add_udm, set_udm_type)


.. py:data:: ETF_BYTIL

   udm - new type was created by the type subsystem


.. py:data:: ETF_NO_ARRAY

   add_udm, set_udm_type - do not convert type to an array on the size mismatch


.. py:data:: GTD_CALC_LAYOUT

   calculate udt layout


.. py:data:: GTD_NO_LAYOUT

   don't calculate udt layout please note that udt layout may have been calculated earlier 
             


.. py:data:: GTD_DEL_BITFLDS

   delete udt bitfields


.. py:data:: GTD_CALC_ARGLOCS

   calculate func arg locations


.. py:data:: GTD_NO_ARGLOCS

   don't calculate func arg locations please note that the locations may have been calculated earlier 
             


.. py:data:: GTS_NESTED

   nested type (embedded into a udt)


.. py:data:: GTS_BASECLASS

   is baseclass of a udt


.. py:data:: SUDT_SORT

   fields are not sorted by offset, sort them first


.. py:data:: SUDT_ALIGN

   recalculate field alignments, struct packing, etc to match the offsets and size info 
           


.. py:data:: SUDT_GAPS

   allow to fill gaps with additional members (_BYTE[])


.. py:data:: SUDT_UNEX

   references to nonexistent member types are acceptable; in this case it is better to set the corresponding udm_t::fda field to the type alignment. If this field is not set, ida will try to guess the alignment. 
           


.. py:data:: SUDT_FAST

   serialize without verifying offsets and alignments


.. py:data:: SUDT_CONST

   only for serialize_udt: make type const


.. py:data:: SUDT_VOLATILE

   only for serialize_udt: make type volatile


.. py:data:: SUDT_TRUNC

   serialize: truncate useless strings from fields, fldcmts


.. py:data:: SUDT_SERDEF

   serialize: if a typeref, serialize its definition


.. py:function:: copy_tinfo_t(_this: tinfo_t, r: tinfo_t) -> None

.. py:function:: detach_tinfo_t(_this: tinfo_t) -> bool

.. py:function:: clear_tinfo_t(_this: tinfo_t) -> None

.. py:function:: create_tinfo(_this: tinfo_t, bt: type_t, bt2: type_t, ptr: void *) -> bool

.. py:function:: verify_tinfo(typid: typid_t) -> int

.. py:function:: get_tinfo_details(typid: typid_t, bt2: type_t, buf: void *) -> bool

.. py:function:: get_tinfo_size(p_effalign: uint32 *, typid: typid_t, gts_code: int) -> size_t

.. py:function:: get_tinfo_pdata(outptr: void *, typid: typid_t, what: int) -> size_t

.. py:function:: get_tinfo_property(typid: typid_t, gta_prop: int) -> size_t

.. py:function:: get_tinfo_property4(typid: typid_t, gta_prop: int, p1: size_t, p2: size_t, p3: size_t, p4: size_t) -> size_t

.. py:function:: set_tinfo_property(tif: tinfo_t, sta_prop: int, x: size_t) -> size_t

.. py:function:: set_tinfo_property4(tif: tinfo_t, sta_prop: int, p1: size_t, p2: size_t, p3: size_t, p4: size_t) -> size_t

.. py:function:: serialize_tinfo(type: qtype *, fields: qtype *, fldcmts: qtype *, tif: tinfo_t, sudt_flags: int) -> bool

.. py:function:: find_tinfo_udt_member(udm: udm_t, typid: typid_t, strmem_flags: int) -> int

.. py:function:: print_tinfo(prefix: str, indent: int, cmtindent: int, flags: int, tif: tinfo_t, name: str, cmt: str) -> str

.. py:function:: dstr_tinfo(tif: tinfo_t) -> str

.. py:function:: visit_subtypes(visitor: tinfo_visitor_t, out: type_mods_t, tif: tinfo_t, name: str, cmt: str) -> int

.. py:function:: compare_tinfo(t1: typid_t, t2: typid_t, tcflags: int) -> bool

.. py:function:: lexcompare_tinfo(t1: typid_t, t2: typid_t, arg3: int) -> int

.. py:function:: get_stock_tinfo(tif: tinfo_t, id: stock_type_id_t) -> bool

.. py:function:: read_tinfo_bitfield_value(typid: typid_t, v: uint64, bitoff: int) -> uint64

.. py:function:: write_tinfo_bitfield_value(typid: typid_t, dst: uint64, v: uint64, bitoff: int) -> uint64

.. py:function:: get_tinfo_attr(typid: typid_t, key: str, bv: bytevec_t *, all_attrs: bool) -> bool

.. py:function:: set_tinfo_attr(tif: tinfo_t, ta: type_attr_t, may_overwrite: bool) -> bool

.. py:function:: del_tinfo_attr(tif: tinfo_t, key: str, make_copy: bool) -> bool

.. py:function:: get_tinfo_attrs(typid: typid_t, tav: type_attrs_t, include_ref_attrs: bool) -> bool

.. py:function:: set_tinfo_attrs(tif: tinfo_t, ta: type_attrs_t) -> bool

.. py:function:: score_tinfo(tif: tinfo_t) -> int

.. py:function:: save_tinfo(tif: tinfo_t, til: til_t, ord: size_t, name: str, ntf_flags: int) -> tinfo_code_t

.. py:function:: append_tinfo_covered(out: rangeset_t, typid: typid_t, offset: uint64) -> bool

.. py:function:: calc_tinfo_gaps(out: rangeset_t, typid: typid_t) -> bool

.. py:function:: value_repr_t__from_opinfo(_this: value_repr_t, flags: flags64_t, afl: aflags_t, opinfo: opinfo_t, ap: array_parameters_t) -> bool

.. py:function:: value_repr_t__print_(_this: value_repr_t, colored: bool) -> str

.. py:function:: udt_type_data_t__find_member(_this: udt_type_data_t, udm: udm_t, strmem_flags: int) -> ssize_t

.. py:function:: udt_type_data_t__get_best_fit_member(_this: udt_type_data_t, disp: asize_t) -> ssize_t

.. py:function:: get_tinfo_by_edm_name(tif: tinfo_t, til: til_t, mname: str) -> ssize_t

.. py:class:: tinfo_t(*args, ordinal=None, name=None, tid=None, til=None)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: clear() -> None

      Clear contents of this tinfo, and remove from the type system.



   .. py:method:: swap(r: tinfo_t) -> None

      Assign this = r and r = this.



   .. py:method:: get_named_type(*args) -> bool

      This function has the following signatures:

          0. get_named_type(til: const til_t *, name: str, decl_type: type_t=BTF_TYPEDEF, resolve: bool=true, try_ordinal: bool=true) -> bool
          1. get_named_type(name: str, decl_type: type_t=BTF_TYPEDEF, resolve: bool=true, try_ordinal: bool=true) -> bool

      # 0: get_named_type(til: const til_t *, name: str, decl_type: type_t=BTF_TYPEDEF, resolve: bool=true, try_ordinal: bool=true) -> bool

      Create a tinfo_t object for an existing named type. 
              

      # 1: get_named_type(name: str, decl_type: type_t=BTF_TYPEDEF, resolve: bool=true, try_ordinal: bool=true) -> bool



   .. py:method:: get_numbered_type(*args) -> bool

      This function has the following signatures:

          0. get_numbered_type(til: const til_t *, ordinal: int, decl_type: type_t=BTF_TYPEDEF, resolve: bool=true) -> bool
          1. get_numbered_type(ordinal: int, decl_type: type_t=BTF_TYPEDEF, resolve: bool=true) -> bool

      # 0: get_numbered_type(til: const til_t *, ordinal: int, decl_type: type_t=BTF_TYPEDEF, resolve: bool=true) -> bool

      Create a tinfo_t object for an existing ordinal type. 
              

      # 1: get_numbered_type(ordinal: int, decl_type: type_t=BTF_TYPEDEF, resolve: bool=true) -> bool



   .. py:method:: detach() -> bool

      Detach tinfo_t from the underlying type. After calling this finction, tinfo_t will lose its link to the underlying named or numbered type (if any) and will become a reference to a unique type. After that, any modifications to tinfo_t will affect only its type. 
              



   .. py:method:: is_correct() -> bool

      Is the type object correct?. It is possible to create incorrect types. For example, we can define a function that returns an enum and then delete the enum type. If this function returns false, the type should not be used in disassembly. Please note that this function does not verify all involved types: for example, pointers to undefined types are permitted. 
              



   .. py:method:: get_realtype(full: bool = False) -> type_t

      Get the resolved base type. Deserialization options:
      * if full=true, the referenced type will be deserialized fully, this may not always be desirable (slows down things)
      * if full=false, we just return the base type, the referenced type will be resolved again later if necessary (this may lead to multiple resolvings of the same type) imho full=false is a better approach because it does not perform unnecessary actions just in case. however, in some cases the caller knows that it is very likely that full type info will be required. in those cases full=true makes sense 


              



   .. py:method:: get_decltype() -> type_t

      Get declared type (without resolving type references; they are returned as is). Obviously this is a very fast function and should be used instead of get_realtype() if possible. Please note that for typerefs this function will return BTF_TYPEDEF. To determine if a typeref is a typedef, use is_typedef() 
              



   .. py:method:: empty() -> bool

      Was tinfo_t initialized with some type info or not?



   .. py:method:: present() -> bool

      Is the type really present? (not a reference to a missing type, for example)



   .. py:method:: get_size(p_effalign: uint32 * = None, gts_code: int = 0) -> size_t

      Get the type size in bytes. 
              
      :param p_effalign: buffer for the alignment value
      :param gts_code: combination of GTS_... constants
      :returns: BADSIZE in case of problems



   .. py:method:: get_unpadded_size() -> size_t

      Get the type size in bytes without the final padding, in bytes. For some UDTs get_unpadded_size() != get_size() 
              



   .. py:method:: get_alignment() -> int

      Get type alignment This function returns the effective type alignment. Zero means error. 
              



   .. py:method:: get_sign() -> type_sign_t

      Get type sign.



   .. py:method:: is_signed() -> bool

      Is this a signed type?



   .. py:method:: is_unsigned() -> bool

      Is this an unsigned type?



   .. py:method:: get_declalign() -> uchar

      Get declared alignment of the type.



   .. py:method:: is_typeref() -> bool

      Is this type a type reference?.



   .. py:method:: has_details() -> bool

      Does this type refer to a nontrivial type?



   .. py:method:: get_type_name() -> bool

      Does a type refer to a name?. If yes, fill the provided buffer with the type name and return true. Names are returned for numbered types too: either a user-defined nice name or, if a user-provided name does not exist, an ordinal name (like #xx, see create_numbered_type_name()). 
              



   .. py:method:: get_nice_type_name() -> bool

      Get the beautified type name. Get the referenced name and apply regular expressions from goodname.cfg to beautify the name 
              



   .. py:method:: rename_type(name: str, ntf_flags: int = 0) -> tinfo_code_t

      Rename a type 
              
      :param name: new type name
      :param ntf_flags: Flags for named types



   .. py:method:: get_final_type_name() -> bool

      Use in the case of typedef chain (TYPE1 -> TYPE2 -> TYPE3...TYPEn). 
              
      :returns: the name of the last type in the chain (TYPEn). if there is no chain, returns TYPE1



   .. py:method:: get_next_type_name() -> bool

      Use In the case of typedef chain (TYPE1 -> TYPE2 -> TYPE3...TYPEn). 
              
      :returns: the name of the next type in the chain (TYPE2). if there is no chain, returns failure



   .. py:method:: get_tid() -> tid_t

      Get the type tid Each type in the local type library has a so-called `tid` associated with it. The tid is used to collect xrefs to the type. The tid is created when the type is created in the local type library and does not change afterwards. It can be passed to xref-related functions instead of the address. 
              
      :returns: tid or BADADDR



   .. py:method:: force_tid() -> tid_t

      Get the type tid. Create if it does not exist yet. If the type comes from a base til, the type will be copied to the local til and a new tid will be created for it. (if the type comes from a base til, it does not have a tid yet). If the type comes from the local til, this function is equivalent to get_tid() 
              
      :returns: tid or BADADDR



   .. py:method:: get_ordinal() -> int

      Get type ordinal (only if the type was created as a numbered type, 0 if none)



   .. py:method:: get_final_ordinal() -> int

      Get final type ordinal (0 if none)



   .. py:method:: get_til() -> til_t *

      Get the type library for tinfo_t.



   .. py:method:: is_from_subtil() -> bool

      Was the named type found in some base type library (not the top level type library)?. If yes, it usually means that the type comes from some loaded type library, not the local type library for the database 
              



   .. py:method:: is_forward_decl() -> bool

      Is this a forward declaration?. Forward declarations are placeholders: the type definition does not exist 
              



   .. py:method:: get_forward_type() -> type_t

      Get type of a forward declaration. For a forward declaration this function returns its base type. In other cases it returns BT_UNK 
              



   .. py:method:: is_forward_struct() -> bool


   .. py:method:: is_forward_union() -> bool


   .. py:method:: is_forward_enum() -> bool


   .. py:method:: is_typedef() -> bool

      Is this a typedef?. This function will return true for a reference to a local type that is declared as a typedef. 
              



   .. py:method:: get_type_cmt() -> int

      Get type comment 
              
      :returns: 0-failed, 1-returned regular comment, 2-returned repeatable comment



   .. py:method:: get_type_rptcmt() -> bool

      Get type comment only if it is repeatable.



   .. py:method:: is_decl_const() -> bool

      is_type_const(get_decltype())



   .. py:method:: is_decl_volatile() -> bool

      is_type_volatile(get_decltype())



   .. py:method:: is_decl_void() -> bool

      is_type_void(get_decltype())



   .. py:method:: is_decl_partial() -> bool

      is_type_partial(get_decltype())



   .. py:method:: is_decl_unknown() -> bool

      is_type_unknown(get_decltype())



   .. py:method:: is_decl_last() -> bool

      is_typeid_last(get_decltype())



   .. py:method:: is_decl_ptr() -> bool

      is_type_ptr(get_decltype())



   .. py:method:: is_decl_array() -> bool

      is_type_array(get_decltype())



   .. py:method:: is_decl_func() -> bool

      is_type_func(get_decltype())



   .. py:method:: is_decl_complex() -> bool

      is_type_complex(get_decltype())



   .. py:method:: is_decl_typedef() -> bool

      is_type_typedef(get_decltype())



   .. py:method:: is_decl_sue() -> bool

      is_type_sue(get_decltype())



   .. py:method:: is_decl_struct() -> bool

      is_type_struct(get_decltype())



   .. py:method:: is_decl_union() -> bool

      is_type_union(get_decltype())



   .. py:method:: is_decl_udt() -> bool

      is_type_struni(get_decltype())



   .. py:method:: is_decl_enum() -> bool

      is_type_enum(get_decltype())



   .. py:method:: is_decl_bitfield() -> bool

      is_type_bitfld(get_decltype())



   .. py:method:: is_decl_int128() -> bool

      is_type_int128(get_decltype())



   .. py:method:: is_decl_int64() -> bool

      is_type_int64(get_decltype())



   .. py:method:: is_decl_int32() -> bool

      is_type_int32(get_decltype())



   .. py:method:: is_decl_int16() -> bool

      is_type_int16(get_decltype())



   .. py:method:: is_decl_int() -> bool

      is_type_int(get_decltype())



   .. py:method:: is_decl_char() -> bool

      is_type_char(get_decltype())



   .. py:method:: is_decl_uint() -> bool

      is_type_uint(get_decltype())



   .. py:method:: is_decl_uchar() -> bool

      is_type_uchar(get_decltype())



   .. py:method:: is_decl_uint16() -> bool

      is_type_uint16(get_decltype())



   .. py:method:: is_decl_uint32() -> bool

      is_type_uint32(get_decltype())



   .. py:method:: is_decl_uint64() -> bool

      is_type_uint64(get_decltype())



   .. py:method:: is_decl_uint128() -> bool

      is_type_uint128(get_decltype())



   .. py:method:: is_decl_ldouble() -> bool

      is_type_ldouble(get_decltype())



   .. py:method:: is_decl_double() -> bool

      is_type_double(get_decltype())



   .. py:method:: is_decl_float() -> bool

      is_type_float(get_decltype())



   .. py:method:: is_decl_tbyte() -> bool

      is_type_tbyte(get_decltype())



   .. py:method:: is_decl_floating() -> bool

      is_type_floating(get_decltype())



   .. py:method:: is_decl_bool() -> bool

      is_type_bool(get_decltype())



   .. py:method:: is_decl_paf() -> bool

      is_type_paf(get_decltype())



   .. py:method:: is_well_defined() -> bool

      !(empty()) && !(is_decl_partial()) && !(is_punknown())



   .. py:method:: is_const() -> bool

      is_type_const(get_realtype())



   .. py:method:: is_volatile() -> bool

      is_type_volatile(get_realtype())



   .. py:method:: is_void() -> bool

      is_type_void(get_realtype())



   .. py:method:: is_partial() -> bool

      is_type_partial(get_realtype())



   .. py:method:: is_unknown() -> bool

      is_type_unknown(get_realtype())



   .. py:method:: is_ptr() -> bool

      is_type_ptr(get_realtype())



   .. py:method:: is_array() -> bool

      is_type_array(get_realtype())



   .. py:method:: is_func() -> bool

      is_type_func(get_realtype())



   .. py:method:: is_complex() -> bool

      is_type_complex(get_realtype())



   .. py:method:: is_struct() -> bool

      is_type_struct(get_realtype())



   .. py:method:: is_union() -> bool

      is_type_union(get_realtype())



   .. py:method:: is_udt() -> bool

      is_type_struni(get_realtype())



   .. py:method:: is_enum() -> bool

      is_type_enum(get_realtype())



   .. py:method:: is_sue() -> bool

      is_type_sue(get_realtype())



   .. py:method:: is_bitfield() -> bool

      is_type_bitfld(get_realtype())



   .. py:method:: is_int128() -> bool

      is_type_int128(get_realtype())



   .. py:method:: is_int64() -> bool

      is_type_int64(get_realtype())



   .. py:method:: is_int32() -> bool

      is_type_int32(get_realtype())



   .. py:method:: is_int16() -> bool

      is_type_int16(get_realtype())



   .. py:method:: is_int() -> bool

      is_type_int(get_realtype())



   .. py:method:: is_char() -> bool

      is_type_char(get_realtype())



   .. py:method:: is_uint() -> bool

      is_type_uint(get_realtype())



   .. py:method:: is_uchar() -> bool

      is_type_uchar(get_realtype())



   .. py:method:: is_uint16() -> bool

      is_type_uint16(get_realtype())



   .. py:method:: is_uint32() -> bool

      is_type_uint32(get_realtype())



   .. py:method:: is_uint64() -> bool

      is_type_uint64(get_realtype())



   .. py:method:: is_uint128() -> bool

      is_type_uint128(get_realtype())



   .. py:method:: is_ldouble() -> bool

      is_type_ldouble(get_realtype())



   .. py:method:: is_double() -> bool

      is_type_double(get_realtype())



   .. py:method:: is_float() -> bool

      is_type_float(get_realtype())



   .. py:method:: is_tbyte() -> bool

      is_type_tbyte(get_realtype())



   .. py:method:: is_bool() -> bool

      is_type_bool(get_realtype())



   .. py:method:: is_paf() -> bool

      is_type_paf(get_realtype())



   .. py:method:: is_ptr_or_array() -> bool

      is_type_ptr_or_array(get_realtype())



   .. py:method:: is_integral() -> bool

      is_type_integral(get_realtype())



   .. py:method:: is_ext_integral() -> bool

      is_type_ext_integral(get_realtype())



   .. py:method:: is_floating() -> bool

      is_type_floating(get_realtype())



   .. py:method:: is_arithmetic() -> bool

      is_type_arithmetic(get_realtype())



   .. py:method:: is_ext_arithmetic() -> bool

      is_type_ext_arithmetic(get_realtype()) 
              



   .. py:method:: is_scalar() -> bool

      Does the type represent a single number?



   .. py:method:: get_ptr_details(pi: ptr_type_data_t) -> bool

      Get the pointer info.



   .. py:method:: get_array_details(ai: array_type_data_t) -> bool

      Get the array specific info.



   .. py:method:: get_enum_details(ei: enum_type_data_t) -> bool

      Get the enum specific info.



   .. py:method:: get_bitfield_details(bi: bitfield_type_data_t) -> bool

      Get the bitfield specific info.



   .. py:method:: get_udt_details(udt: udt_type_data_t, gtd: gtd_udt_t = GTD_CALC_LAYOUT) -> bool

      Get the udt specific info.



   .. py:method:: get_func_details(fi: func_type_data_t, gtd: gtd_func_t = GTD_CALC_ARGLOCS) -> bool

      Get only the function specific info for this tinfo_t.



   .. py:method:: is_funcptr() -> bool

      Is this pointer to a function?



   .. py:method:: is_shifted_ptr() -> bool

      Is a shifted pointer?



   .. py:method:: is_varstruct() -> bool

      Is a variable-size structure?



   .. py:method:: is_varmember() -> bool

      Can the type be of a variable struct member? This function checks for: is_array() && array.nelems==0 Such a member can be only the very last member of a structure 
              



   .. py:method:: get_ptrarr_objsize() -> int

      BT_PTR & BT_ARRAY: get size of pointed object or array element. On error returns -1



   .. py:method:: get_ptrarr_object() -> tinfo_t

      BT_PTR & BT_ARRAY: get the pointed object or array element. If the current type is not a pointer or array, return empty type info. 
              



   .. py:method:: get_pointed_object() -> tinfo_t

      BT_PTR: get type of pointed object. If the current type is not a pointer, return empty type info. See also get_ptrarr_object() and remove_pointer() 
              



   .. py:method:: is_pvoid() -> bool

      Is "void *"?. This function does not check the pointer attributes and type modifiers.



   .. py:method:: is_punknown() -> bool

      Is "_UNKNOWN *"?. This function does not check the pointer attributes and type modifiers.



   .. py:method:: get_array_element() -> tinfo_t

      BT_ARRAY: get type of array element. See also get_ptrarr_object()



   .. py:method:: get_final_element() -> tinfo_t

      repeat recursively: if an array, return the type of its element; else return the type itself.



   .. py:method:: get_array_nelems() -> int

      BT_ARRAY: get number of elements (-1 means error)



   .. py:method:: get_nth_arg(n: int) -> tinfo_t

      BT_FUNC or BT_PTR BT_FUNC: Get type of n-th arg (-1 means return type, see get_rettype())



   .. py:method:: get_rettype() -> tinfo_t

      BT_FUNC or BT_PTR BT_FUNC: Get the function's return type



   .. py:method:: get_nargs() -> int

      BT_FUNC or BT_PTR BT_FUNC: Calculate number of arguments (-1 - error)



   .. py:method:: is_user_cc() -> bool

      is_user_cc(get_cc())



   .. py:method:: is_vararg_cc() -> bool

      is_vararg_cc(get_cc())



   .. py:method:: is_purging_cc() -> bool

      is_purging_cc(get_cc())



   .. py:method:: calc_purged_bytes() -> int

      BT_FUNC: Calculate number of purged bytes



   .. py:method:: is_high_func() -> bool

      BT_FUNC: Is high level type?



   .. py:method:: get_methods(methods: udtmembervec_t) -> bool

      BT_COMPLEX: get a list of member functions declared in this udt. 
              
      :returns: false if no member functions exist



   .. py:method:: get_bit_buckets(buckets: range64vec_t) -> bool

      ::BT_STRUCT: get bit buckets Bit buckets are used to layout bitfields 
              
      :returns: false if wrong type was passed



   .. py:method:: find_udm(*args) -> int

      This function has the following signatures:

          0. find_udm(udm: udm_t *, strmem_flags: int) -> int
          1. find_udm(offset: uint64, strmem_flags: int=0) -> int
          2. find_udm(name: str, strmem_flags: int=0) -> int

      # 0: find_udm(udm: udm_t *, strmem_flags: int) -> int

      BTF_STRUCT,BTF_UNION: Find a udt member.
      * at the specified offset (STRMEM_OFFSET)
      * with the specified index (STRMEM_INDEX)
      * with the specified type (STRMEM_TYPE)
      * with the specified name (STRMEM_NAME)



      :returns: the index of the found member or -1

      # 1: find_udm(offset: uint64, strmem_flags: int=0) -> int

      BTF_STRUCT,BTF_UNION: Find an udt member at the specified offset 
              
      :returns: the index of the found member or -1

      # 2: find_udm(name: str, strmem_flags: int=0) -> int

      BTF_STRUCT,BTF_UNION: Find an udt member by name 
              
      :returns: the index of the found member or -1



   .. py:method:: get_udm(*args) -> Union[Tuple[int, udm_t], Tuple[None, None]]

      Retrieve a structure/union member with either the specified name
      or the specified index, in the specified tinfo_t object.

      This function has the following signatures:

          1. get_udm(index: int)
          2. get_udm(name: str)

      :param index: a member index (1st form)
      :param name: a member name (2nd form)
      :returns: a tuple (int, udm_t), or (-1, None) if member not found



   .. py:method:: get_udm_by_offset(offset: int)

      Retrieve a structure/union member with the specified offset,
      in the specified tinfo_t object.

      :param offset: the member offset
      :returns: a tuple (int, udm_t), or (-1, None) if member not found



   .. py:method:: get_udt_nmembers() -> int

      Get number of udt members. -1-error.



   .. py:method:: is_empty_udt() -> bool

      Is an empty struct/union? (has no fields)



   .. py:method:: is_small_udt() -> bool

      Is a small udt? (can fit a register or a pair of registers)



   .. py:method:: get_udt_taudt_bits() -> int

      Get udt_type_data_t::taudt_bits.



   .. py:method:: is_unaligned_struct() -> bool

      Is an unaligned struct.



   .. py:method:: is_msstruct() -> bool

      Is gcc msstruct attribute applied.



   .. py:method:: is_cpp_struct() -> bool

      Is a c++ object, not simple pod type.



   .. py:method:: is_vftable() -> bool

      Is a vftable type?



   .. py:method:: is_fixed_struct() -> bool

      Is a structure with fixed offsets?



   .. py:method:: is_tuple() -> bool

      Is a tuple?



   .. py:method:: requires_qualifier(name: str, offset: uint64) -> bool

      Requires full qualifier? (name is not unique) 
              
      :param name: field name
      :param offset: field offset in bits
      :returns: if the name is not unique, returns true



   .. py:method:: append_covered(out: rangeset_t, offset: uint64 = 0) -> bool

      Calculate set of covered bytes for the type 
              
      :param out: pointer to the output buffer. covered bytes will be appended to it.
      :param offset: delta in bytes to add to all calculations. used internally during recurion.



   .. py:method:: calc_gaps(out: rangeset_t) -> bool

      Calculate set of padding bytes for the type 
              
      :param out: pointer to the output buffer; old buffer contents will be lost.



   .. py:method:: is_one_fpval() -> bool

      Floating value or an object consisting of one floating member entirely.



   .. py:method:: is_sse_type() -> bool

      Is a SSE vector type?



   .. py:method:: is_anonymous_udt() -> bool

      Is an anonymous struct/union? We assume that types with names are anonymous if the name starts with $ 
              



   .. py:method:: has_vftable() -> bool

      Has a vftable?



   .. py:method:: has_union() -> bool

      Has a member of type "union"?



   .. py:method:: get_enum_nmembers() -> size_t

      Get number of enum members. 
              
      :returns: BADSIZE if error



   .. py:method:: is_empty_enum() -> bool

      Is an empty enum? (has no constants)



   .. py:method:: get_enum_base_type() -> type_t

      Get enum base type (convert enum to integer type) Returns BT_UNK if failed to convert 
              



   .. py:method:: is_bitmask_enum() -> bool

      Is bitmask enum? 
              
      :returns: true for bitmask enum and false in other cases enum_type_data_t::is_bf()



   .. py:method:: get_enum_radix() -> int

      Get enum constant radix 
              
      :returns: radix or 1 for BTE_CHAR enum_type_data_t::get_enum_radix()



   .. py:method:: get_enum_repr(repr: value_repr_t) -> tinfo_code_t

      Set the representation of enum members. 
              
      :param repr: value_repr_t



   .. py:method:: get_enum_width() -> int

      Get enum width 
              
      :returns: width of enum base type in bytes, 0 - unspecified, or -1 enum_type_data_t::calc_nbytes()



   .. py:method:: calc_enum_mask() -> uint64


   .. py:method:: get_edm_by_value(value: int, bmask: int = DEFMASK64, serial: int = 0) -> Tuple[int, edm_t]

      Retrieve an enumerator with the specified value,
      in the specified tinfo_t object.

      :param value: the enumerator value
      :returns: a tuple (int, edm_t), or (-1, None) if member not found



   .. py:method:: get_edm_tid(idx: size_t) -> tid_t

      Get enum member TID 
              
      :param idx: enum member index
      :returns: tid or BADADDR The tid is used to collect xrefs to the member, it can be passed to xref-related functions instead of the address.



   .. py:method:: get_onemember_type() -> tinfo_t

      For objects consisting of one member entirely: return type of the member.



   .. py:method:: get_innermost_udm(bitoffset: uint64) -> tinfo_t

      Get the innermost member at the given offset 
              
      :param bitoffset: bit offset into the structure
      :returns: udt: with the innermost member
      :returns: empty: type if it is not a struct type or OFFSET could not be found



   .. py:method:: get_innermost_member_type(bitoffset: uint64) -> tinfo_t

      Get the innermost member type at the given offset 
              
      :param bitoffset: bit offset into the structure
      :returns: the: innermost member type



   .. py:method:: calc_score() -> int

      Calculate the type score (the higher - the nicer is the type)



   .. py:method:: dstr() -> str

      Function to facilitate debugging.



   .. py:method:: get_attrs(tav: type_attrs_t, all_attrs: bool = False) -> bool

      Get type attributes (all_attrs: include attributes of referenced types, if any)



   .. py:method:: set_attrs(tav: type_attrs_t) -> bool

      Set type attributes. If necessary, a new typid will be created. this function modifies tav! (returns old attributes, if any) 
              
      :returns: false: bad attributes



   .. py:method:: set_attr(ta: type_attr_t, may_overwrite: bool = True) -> bool

      Set a type attribute. If necessary, a new typid will be created.



   .. py:method:: del_attrs() -> None

      Del all type attributes. typerefs cannot be modified by this function.



   .. py:method:: del_attr(key: str, make_copy: bool = True) -> bool

      Del a type attribute. typerefs cannot be modified by this function.



   .. py:method:: create_simple_type(decl_type: type_t) -> bool


   .. py:method:: create_ptr(*args) -> bool


   .. py:method:: create_array(*args) -> bool


   .. py:method:: create_typedef(*args) -> None


   .. py:method:: create_bitfield(*args) -> bool


   .. py:method:: parse(decl: str, til: til_t = None, pt_flags: int = 0) -> bool

      Convenience function to parse a string with a type declaration 
              
      :param decl: a type declaration
      :param til: type library to use
      :param pt_flags: combination of Type parsing flags bits



   .. py:method:: create_udt(*args) -> bool

      Create an empty structure/union.



   .. py:method:: create_enum(*args) -> bool

      Create an empty enum.



   .. py:method:: create_func(*args) -> bool


   .. py:method:: get_udm_by_tid(udm: udm_t, tid: tid_t) -> ssize_t


   .. py:method:: get_edm_by_tid(edm: edm_t, tid: tid_t) -> ssize_t


   .. py:method:: get_type_by_tid(tid: tid_t) -> bool


   .. py:method:: get_by_edm_name(mname: str, til: til_t = None) -> ssize_t

      Retrieve enum tinfo using enum member name 
              
      :param mname: enum type member name
      :param til: type library
      :returns: member index, otherwise returns -1. If the function fails, THIS object becomes empty.



   .. py:method:: set_named_type(til: til_t, name: str, ntf_flags: int = 0) -> tinfo_code_t


   .. py:method:: set_symbol_type(til: til_t, name: str, ntf_flags: int = 0) -> tinfo_code_t


   .. py:method:: set_numbered_type(til: til_t, ord: int, ntf_flags: int = 0, name: str = None) -> tinfo_code_t


   .. py:method:: save_type(*args) -> tinfo_code_t


   .. py:method:: copy_type(*args) -> tinfo_code_t


   .. py:method:: create_forward_decl(til: til_t, decl_type: type_t, name: str, ntf_flags: int = 0) -> tinfo_code_t

      Create a forward declaration. decl_type: BTF_STRUCT, BTF_UNION, or BTF_ENUM 
              



   .. py:method:: get_stock(id: stock_type_id_t) -> tinfo_t
      :staticmethod:


      Get stock type information. This function can be used to get tinfo_t for some common types. The same tinfo_t will be returned for the same id, thus saving memory and increasing the speed Please note that retrieving the STI_SIZE_T or STI_SSIZE_T stock type, will also have the side-effect of adding that type to the 'idati' TIL, under the well-known name 'size_t' or 'ssize_t' (respectively). The same is valid for STI_COMPLEX64 and STI_COMPLEX64 stock types with names 'complex64_t' and 'complex128_t' (respectively). 
              



   .. py:method:: convert_array_to_ptr() -> bool

      Convert an array into a pointer. type[] => type * 
              



   .. py:method:: remove_ptr_or_array() -> bool

      Replace the current type with the ptr obj or array element. This function performs one of the following conversions:
      * type[] => type
      * type* => type If the conversion is performed successfully, return true 


              



   .. py:method:: read_bitfield_value(v: uint64, bitoff: int) -> uint64


   .. py:method:: write_bitfield_value(dst: uint64, v: uint64, bitoff: int) -> uint64


   .. py:method:: get_modifiers() -> type_t


   .. py:method:: set_modifiers(mod: type_t) -> None


   .. py:method:: set_const() -> None


   .. py:method:: set_volatile() -> None


   .. py:method:: clr_decl_const_volatile() -> None


   .. py:method:: clr_const() -> bool


   .. py:method:: clr_volatile() -> bool


   .. py:method:: clr_const_volatile() -> bool


   .. py:method:: set_type_alignment(declalign: uchar, etf_flags: uint = 0) -> tinfo_code_t

      Set type alignment.



   .. py:method:: set_declalign(declalign: uchar) -> bool


   .. py:method:: change_sign(sign: type_sign_t) -> bool

      Change the type sign. Works only for the types that may have sign.



   .. py:method:: calc_udt_aligns(sudt_flags: int = 4) -> bool

      Calculate the udt alignments using the field offsets/sizes and the total udt size This function does not work on typerefs 
              



   .. py:method:: set_methods(methods: udtmembervec_t) -> bool

      BT_COMPLEX: set the list of member functions. This function consumes 'methods' (makes it empty). 
              
      :returns: false if this type is not a udt, or if the given list is empty



   .. py:method:: set_type_cmt(cmt: str, is_regcmt: bool = False, etf_flags: uint = 0) -> tinfo_code_t

      Set type comment This function works only for non-trivial types 
              



   .. py:method:: get_alias_target() -> int

      Get type alias If the type has no alias, return 0. 
              



   .. py:method:: is_aliased() -> bool


   .. py:method:: set_type_alias(dest_ord: int) -> bool

      Set type alias Redirects all references to source type to the destination type. This is equivalent to instantaneous replacement all references to srctype by dsttype. 
              



   .. py:method:: set_udt_alignment(sda: int, etf_flags: uint = 0) -> tinfo_code_t

      Set declared structure alignment (sda) This alignment supersedes the alignment returned by get_declalign() and is really used when calculating the struct layout. However, the effective structure alignment may differ from `sda` because of packing. The type editing functions (they accept etf_flags) may overwrite this attribute. 
              



   .. py:method:: set_udt_pack(pack: int, etf_flags: uint = 0) -> tinfo_code_t

      Set structure packing. The value controls how little a structure member alignment can be. Example: if pack=1, then it is possible to align a double to a byte. __attribute__((aligned(1))) double x; However, if pack=3, a double will be aligned to 8 (2**3) even if requested to be aligned to a byte. pack==0 will have the same effect. The type editing functions (they accept etf_flags) may overwrite this attribute. 
              



   .. py:method:: get_udm_tid(idx: size_t) -> tid_t

      Get udt member TID 
              
      :param idx: the index of udt the member
      :returns: tid or BADADDR The tid is used to collect xrefs to the member, it can be passed to xref-related functions instead of the address.



   .. py:method:: add_udm(*args)

      Add a member to the current structure/union.

      When creating a new structure/union from scratch, you might
      want to first call `create_udt()`

      This method has the following signatures:

          1. add_udm(udm: udm_t, etf_flags: int = 0, times: int = 1, idx: int = -1)
          2. add_udm(name: str, type: type_t | tinfo_t | str, offset: int = 0, etf_flags: int = 0, times: int = 1, idx: int = -1)

      In the 2nd form, the 'type' descriptor, can be one of:

      * type_t: if the type is simple (integral/floating/bool). E.g., `BTF_INT`
      * tinfo_t: can handle more complex types (structures, pointers, arrays, ...)
      * str: a C type declaration

      If an input argument is incorrect, the constructor may raise an exception

      :param udm:       The member, fully initialized (1st form)
      :param name:      Member name - must not be empty
      :param type:      Member type
      :param offset:    the member offset in bits. It is the caller's responsibility
                        to specify correct offsets.
      :param etf_flags: an OR'ed combination of ETF_ flags
      :param times:     how many times to add the new member
      :param idx:       the index in the udm array where the new udm should be placed.
                        If the specified index cannot be honored because it would spoil
                        the udm sorting order, it is silently ignored.



   .. py:method:: del_udm(index: size_t, etf_flags: uint = 0) -> tinfo_code_t

      Delete a structure/union member.



   .. py:method:: del_udms(idx1: size_t, idx2: size_t, etf_flags: uint = 0) -> tinfo_code_t

      Delete structure/union members in the range [idx1, idx2)



   .. py:method:: rename_udm(index: size_t, name: str, etf_flags: uint = 0) -> tinfo_code_t

      Rename a structure/union member. The new name must be unique. 
              



   .. py:method:: set_udm_type(index: size_t, tif: tinfo_t, etf_flags: uint = 0, repr: value_repr_t = None) -> tinfo_code_t

      Set type of a structure/union member. 
              
      :param index: member index in the udm array
      :param tif: new type for the member
      :param etf_flags: etf_flag_t
      :param repr: new representation for the member (optional)
      :returns: tinfo_code_t



   .. py:method:: set_udm_cmt(index: size_t, cmt: str, is_regcmt: bool = False, etf_flags: uint = 0) -> tinfo_code_t

      Set a comment for a structure/union member. A member may have just one comment, and it is either repeatable or regular. 
              



   .. py:method:: set_udm_repr(index: size_t, repr: value_repr_t, etf_flags: uint = 0) -> tinfo_code_t

      Set the representation of a structure/union member.



   .. py:method:: is_udm_by_til(idx: size_t) -> bool

      Was the member created due to the type system 
              
      :param idx: index of the member



   .. py:method:: set_udm_by_til(idx: size_t, on: bool = True, etf_flags: uint = 0) -> tinfo_code_t

      The member is created due to the type system 
              
      :param idx: index of the member
      :param etf_flags: etf_flag_t



   .. py:method:: set_fixed_struct(on: bool = True) -> tinfo_code_t

      Declare struct member offsets as fixed. For such structures, IDA will not recalculate the member offsets. If a member does not fit into its place anymore, it will be deleted. This function works only with structures (not unions). 
              



   .. py:method:: set_struct_size(new_size: size_t) -> tinfo_code_t

      Explicitly specify the struct size. This function works only with fixed structures. The new struct size can be equal or higher the unpadded struct size (IOW, all existing members should fit into the specified size). 
              
      :param new_size: new structure size in bytes



   .. py:method:: expand_udt(idx: size_t, delta: adiff_t, etf_flags: uint = 0) -> tinfo_code_t

      Expand/shrink a structure by adding/removing a gap before the specified member.
      For regular structures, either the gap can be accommodated by aligning the next member with an alignment directive, or an explicit "gap" member will be inserted. Also note that it is impossible to add a gap at the end of a regular structure.
      When it comes to fixed-layout structures, there is no need to either add new "gap" members or align existing members, since all members have a fixed offset. It is possible to add a gap at the end of a fixed-layout structure, by passing `-1` as index.

      :param idx: index of the member
      :param delta: number of bytes to add or remove
      :param etf_flags: etf_flag_t



   .. py:method:: set_tuple(on: bool = True) -> tinfo_code_t

      Declare struct as a tuple. Currently, tuples in IDA behave the same way as structures but they are returned in a different manner from functions. Also, 2 different tuples having the same members are considered to be equal. This function works only with structures (not unions). 
              



   .. py:method:: get_func_frame(pfn: func_t const *) -> bool

      Create a tinfo_t object for the function frame 
              
      :param pfn: function



   .. py:method:: is_frame() -> bool

      Is a function frame?



   .. py:method:: get_frame_func() -> ida_idaapi.ea_t

      Get function address for the frame.



   .. py:method:: set_enum_width(nbytes: int, etf_flags: uint = 0) -> tinfo_code_t

      Set the width of enum base type 
              
      :param nbytes: width of enum base type, allowed values: 0 (unspecified),1,2,4,8,16,32,64
      :param etf_flags: etf_flag_t



   .. py:method:: set_enum_sign(sign: type_sign_t, etf_flags: uint = 0) -> tinfo_code_t

      Set enum sign 
              
      :param sign: type_sign_t
      :param etf_flags: etf_flag_t



   .. py:attribute:: ENUMBM_OFF

      convert to ordinal enum



   .. py:attribute:: ENUMBM_ON

      convert to bitmask enum



   .. py:attribute:: ENUMBM_AUTO

      convert to bitmask if the outcome is nice and useful



   .. py:method:: set_enum_is_bitmask(*args) -> tinfo_code_t


   .. py:method:: set_enum_repr(repr: value_repr_t, etf_flags: uint = 0) -> tinfo_code_t

      Set the representation of enum members. 
              
      :param repr: value_repr_t
      :param etf_flags: etf_flag_t



   .. py:method:: set_enum_radix(radix: int, sign: bool, etf_flags: uint = 0) -> tinfo_code_t

      Set enum radix to display constants 
              
      :param radix: radix 2, 4, 8, 16, with the special case 1 to display as character
      :param sign: display as signed or unsigned
      :param etf_flags: etf_flag_t



   .. py:method:: add_edm(*args)

      Add an enumerator to the current enumeration.

      When creating a new enumeration from scratch, you might
      want to first call `create_enum()`

      This method has the following signatures:

          1. add_edm(edm: edm_t, bmask: int = -1, etf_flags: int = 0, idx: int = -1)
          2. add_edm(name: str, value: int, bmask: int = -1, etf_flags: int = 0, idx: int = -1)

      If an input argument is incorrect, the constructor may raise an exception

      :param edm:       The member, fully initialized (1st form)
      :param name:      Enumerator name - must not be empty
      :param value:     Enumerator value
      :param bmask:     A bitmask to which the enumerator belongs
      :param etf_flags: an OR'ed combination of ETF_ flags
      :param idx:       the index in the edm array where the new udm should be placed.
                        If the specified index cannot be honored because it would spoil
                        the edm sorting order, it is silently ignored.



   .. py:method:: del_edms(idx1: size_t, idx2: size_t, etf_flags: uint = 0) -> tinfo_code_t

      Delete enum members 
              
      :param idx1: index in edmvec_t
      :param idx2: index in edmvec_t or size_t(-1)
      :param etf_flags: etf_flag_t Delete enum members in [idx1, idx2)



   .. py:method:: del_edm(*args)

      Delete an enumerator with the specified name
      or the specified index, in the specified tinfo_t object.

      This method has the following signatures:

          1. del_edm(name: str) -> int
          2. del_edm(index: int) -> int

      :param name: an enumerator name (1st form)
      :param index: an enumerator index (2nd form)
      :returns: TERR_OK in case of success, or another TERR_* value in case of error



   .. py:method:: del_edm_by_value(value: int, etf_flags: int = 0, bmask: int = DEFMASK64, serial: int = 0)

      Delete an enumerator with the specified value,
      in the specified tinfo_t object.

      :param value: the enumerator value
      :returns: TERR_OK in case of success, or another TERR_* value in case of error



   .. py:method:: rename_edm(idx: size_t, name: str, etf_flags: uint = 0) -> tinfo_code_t

      Rename a enum member 
              
      :param idx: index in edmvec_t
      :param name: new name
      :param etf_flags: etf_flag_t ETF_FORCENAME may be used in case of TERR_ALIEN_NAME



   .. py:method:: set_edm_cmt(idx: size_t, cmt: str, etf_flags: uint = 0) -> tinfo_code_t

      Set a comment for an enum member. Such comments are always considered as repeatable. 
              
      :param idx: index in edmvec_t
      :param cmt: comment
      :param etf_flags: etf_flag_t



   .. py:method:: edit_edm(*args) -> tinfo_code_t

      Change constant value and/or bitmask 
              
      :param idx: index in edmvec_t
      :param value: old or new value
      :param bmask: old or new bitmask
      :param etf_flags: etf_flag_t



   .. py:method:: rename_funcarg(index: size_t, name: str, etf_flags: uint = 0) -> tinfo_code_t

      Rename a function argument. The new name must be unique. 
              
      :param index: argument index in the function array
      :param name: new name
      :param etf_flags: etf_flag_t



   .. py:method:: set_funcarg_type(index: size_t, tif: tinfo_t, etf_flags: uint = 0) -> tinfo_code_t

      Set type of a function argument. 
              
      :param index: argument index in the function array
      :param tif: new type for the argument
      :param etf_flags: etf_flag_t
      :returns: tinfo_code_t



   .. py:method:: set_func_rettype(tif: tinfo_t, etf_flags: uint = 0) -> tinfo_code_t

      Set function return type . 
              
      :param tif: new type for the return type
      :param etf_flags: etf_flag_t
      :returns: tinfo_code_t



   .. py:method:: del_funcargs(idx1: size_t, idx2: size_t, etf_flags: uint = 0) -> tinfo_code_t

      Delete function arguments 
              
      :param idx1: index in funcargvec_t
      :param idx2: index in funcargvec_t or size_t(-1)
      :param etf_flags: etf_flag_t Delete function arguments in [idx1, idx2)



   .. py:method:: del_funcarg(idx: size_t, etf_flags: uint = 0) -> tinfo_code_t


   .. py:method:: add_funcarg(farg: funcarg_t, etf_flags: uint = 0, idx: ssize_t = -1) -> tinfo_code_t

      Add a function argument. 
              
      :param farg: argument to add
      :param etf_flags: type changing flags flags
      :param idx: the index in the funcarg array where the new funcarg should be placed. if the specified index cannot be honored because it would spoil the funcarg sorting order, it is silently ignored.



   .. py:method:: set_func_cc(cc: callcnv_t, etf_flags: uint = 0) -> tinfo_code_t

      Set function calling convention.



   .. py:method:: set_funcarg_loc(index: size_t, argloc: argloc_t, etf_flags: uint = 0) -> tinfo_code_t

      Set location of a function argument. 
              
      :param index: argument index in the function array
      :param argloc: new location for the argument
      :param etf_flags: etf_flag_t
      :returns: tinfo_code_t



   .. py:method:: set_func_retloc(argloc: argloc_t, etf_flags: uint = 0) -> tinfo_code_t

      Set location of function return value. 
              
      :param argloc: new location for the return value
      :param etf_flags: etf_flag_t
      :returns: tinfo_code_t



   .. py:method:: compare(r: tinfo_t) -> int


   .. py:method:: compare_with(r: tinfo_t, tcflags: int = 0) -> bool

      Compare two types, based on given flags (see tinfo_t comparison flags)



   .. py:method:: equals_to(r: tinfo_t) -> bool


   .. py:method:: is_castable_to(target: tinfo_t) -> bool


   .. py:method:: is_manually_castable_to(target: tinfo_t) -> bool


   .. py:method:: serialize(*args) -> PyObject *

      Serialize tinfo_t object into a type string.



   .. py:method:: deserialize(*args) -> bool

      This function has the following signatures:

          0. deserialize(til: const til_t *, ptype: const type_t **, pfields: const p_list **=nullptr, pfldcmts: const p_list **=nullptr, cmt: str=nullptr) -> bool
          1. deserialize(til: const til_t *, ptype: const qtype *, pfields: const qtype *=nullptr, pfldcmts: const qtype *=nullptr, cmt: str=nullptr) -> bool

      # 0: deserialize(til: const til_t *, ptype: const type_t **, pfields: const p_list **=nullptr, pfldcmts: const p_list **=nullptr, cmt: str=nullptr) -> bool

      Deserialize a type string into a tinfo_t object.


      # 1: deserialize(til: const til_t *, ptype: const qtype *, pfields: const qtype *=nullptr, pfldcmts: const qtype *=nullptr, cmt: str=nullptr) -> bool

      Deserialize a type string into a tinfo_t object.



   .. py:method:: get_stkvar(insn: insn_t const &, x: op_t const, v: int) -> ssize_t

      Retrieve frame tinfo for a stack variable 
              
      :param insn: the instruction
      :param x: reference to instruction operand, may be nullptr
      :param v: immediate value in the operand (usually x.addr)
      :returns: returns the member index, otherwise returns -1. if the function fails, THIS object becomes empty.



   .. py:method:: copy() -> tinfo_t


   .. py:method:: get_attr(key: str, all_attrs: bool = True) -> PyObject *

      Get a type attribute.



   .. py:method:: get_edm(*args) -> Tuple[int, edm_t]

      Retrieve an enumerator with either the specified name
      or the specified index, in the specified tinfo_t object.

      This function has the following signatures:

          1. get_edm(index: int)
          2. get_edm(name: str)

      :param index: an enumerator index (1st form).
      :param name: an enumerator name (2nd form).
      :returns: a tuple (int, edm_t), or (-1, None) if member not found



   .. py:method:: find_edm(*args) -> ssize_t


   .. py:method:: iter_struct()

      Iterate on the members composing this structure.

      Example:

          til = ida_typeinf.get_idati()
          tif = til.get_named_type("my_struc")
          for udm in tif.iter_struct():
              print(f"{udm.name} at bit offset {udm.offset}")

      Will raise an exception if this type is not a structure.

      :returns: a udm_t-producing generator



   .. py:method:: iter_union()

      Iterate on the members composing this union.

      Example:

          til = ida_typeinf.get_idati()
          tif = til.get_named_type("my_union")
          for udm in tif.iter_union():
              print(f"{udm.name}, with type {udm.type}")

      Will raise an exception if this type is not a union.

      :returns: a udm_t-producing generator



   .. py:method:: iter_udt()

      Iterate on the members composing this structure, or union.

      Example:

          til = ida_typeinf.get_idati()
          tif = til.get_named_type("my_type")
          for udm in tif.iter_udt():
              print(f"{udm.name} at bit offset {udm.offset} with type {udm.type}")

      Will raise an exception if this type is not a structure, or union

      :returns: a udm_t-producing generator



   .. py:method:: iter_enum()

      Iterate on the members composing this enumeration.

      Example:

          til = ida_typeinf.get_idati()
          tif = til.get_named_type("my_enum")
          for edm in tif.iter_enum():
              print(f"{edm.name} = {edm.value}")

      Will raise an exception if this type is not an enumeration

      :returns: a edm_t-producing generator



   .. py:method:: iter_func()

      Iterate on the arguments contained in this function prototype

      Example:

          address = ...
          func = ida_funcs.get_func(address)
          func_type = func.prototype
          for arg in func_type.iter_func():
              print(f"{arg.name}, of type {arg.type}")

      Will raise an exception if this type is not a function

      :returns: a funcarg_t-producing generator



   .. py:attribute:: get_edm_by_name


.. py:data:: COMP_MASK

.. py:data:: COMP_UNK

   Unknown.


.. py:data:: COMP_MS

   Visual C++.


.. py:data:: COMP_BC

   Borland C++.


.. py:data:: COMP_WATCOM

   Watcom C++.


.. py:data:: COMP_GNU

   GNU C++.


.. py:data:: COMP_VISAGE

   Visual Age C++.


.. py:data:: COMP_BP

   Delphi.


.. py:data:: COMP_UNSURE

   uncertain compiler id


.. py:data:: BADSIZE

   bad type size


.. py:data:: FIRST_NONTRIVIAL_TYPID

   Denotes the first bit describing a nontrivial type.


.. py:data:: TYPID_ISREF

   Identifies that a type that is a typeref.


.. py:data:: TYPID_SHIFT

   First type detail bit.


.. py:function:: remove_pointer(tif: tinfo_t) -> tinfo_t

   BT_PTR: If the current type is a pointer, return the pointed object. If the current type is not a pointer, return the current type. See also get_ptrarr_object() and get_pointed_object() 
           


.. py:data:: STRMEM_MASK

.. py:data:: STRMEM_OFFSET

   get member by offset
   * in: udm->offset - is a member offset in bits 


           


.. py:data:: STRMEM_INDEX

   get member by number
   * in: udm->offset - is a member number 


           


.. py:data:: STRMEM_AUTO

   get member by offset if struct, or get member by index if union
   * nb: union: index is stored in the udm->offset field!
   * nb: struct: offset is in bytes (not in bits)! 


           


.. py:data:: STRMEM_NAME

   get member by name
   * in: udm->name - the desired member name. 


           


.. py:data:: STRMEM_TYPE

   get member by type.
   * in: udm->type - the desired member type. member types are compared with tinfo_t::equals_to() 


           


.. py:data:: STRMEM_SIZE

   get member by size.
   * in: udm->size - the desired member size. 


           


.. py:data:: STRMEM_MINS

   get smallest member by size.


.. py:data:: STRMEM_MAXS

   get biggest member by size.


.. py:data:: STRMEM_LOWBND

   get member by offset or the next member (lower bound)
   * in: udm->offset - is a member offset in bits 


           


.. py:data:: STRMEM_NEXT

   get next member after the offset
   * in: udm->offset - is a member offset in bits 


           


.. py:data:: STRMEM_VFTABLE

   can be combined with STRMEM_OFFSET, STRMEM_AUTO get vftable instead of the base class 
           


.. py:data:: STRMEM_SKIP_EMPTY

   can be combined with STRMEM_OFFSET, STRMEM_AUTO skip empty members (i.e. having zero size) only last empty member can be returned 
           


.. py:data:: STRMEM_CASTABLE_TO

   can be combined with STRMEM_TYPE: member type must be castable to the specified type 
           


.. py:data:: STRMEM_ANON

   can be combined with STRMEM_NAME: look inside anonymous members too. 
           


.. py:data:: STRMEM_SKIP_GAPS

   can be combined with STRMEM_OFFSET, STRMEM_LOWBND skip gap members 
           


.. py:data:: TCMP_EQUAL

   are types equal?


.. py:data:: TCMP_IGNMODS

   ignore const/volatile modifiers


.. py:data:: TCMP_AUTOCAST

   can t1 be cast into t2 automatically?


.. py:data:: TCMP_MANCAST

   can t1 be cast into t2 manually?


.. py:data:: TCMP_CALL

   can t1 be called with t2 type?


.. py:data:: TCMP_DELPTR

   remove pointer from types before comparing


.. py:data:: TCMP_DECL

   compare declarations without resolving them


.. py:data:: TCMP_ANYBASE

   accept any base class when casting


.. py:data:: TCMP_SKIPTHIS

   skip the first function argument in comparison


.. py:data:: TCMP_DEEP_UDT

   compare udt by member/attributes


.. py:class:: simd_info_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str

      name of SIMD type (nullptr-undefined)



   .. py:attribute:: tif
      :type:  tinfo_t

      SIMD type (empty-undefined)



   .. py:attribute:: size
      :type:  uint16

      SIMD type size in bytes (0-undefined)



   .. py:attribute:: memtype
      :type:  type_t

      member type BTF_INT8/16/32/64/128, BTF_UINT8/16/32/64/128 BTF_INT - integrals of any size/sign BTF_FLOAT, BTF_DOUBLE BTF_TBYTE - floatings of any size BTF_UNION - union of integral and floating types BTF_UNK - undefined 
              



   .. py:method:: match_pattern(pattern: simd_info_t) -> bool


.. py:function:: guess_func_cc(fti: func_type_data_t, npurged: int, cc_flags: int) -> callcnv_t

   Use func_type_data_t::guess_cc()


.. py:function:: dump_func_type_data(fti: func_type_data_t, praloc_bits: int) -> str

   Use func_type_data_t::dump()


.. py:function:: calc_arglocs(fti: func_type_data_t) -> bool

.. py:function:: calc_varglocs(fti: func_type_data_t, regs: regobjs_t, stkargs: relobj_t, nfixed: int) -> bool

.. py:class:: ptr_type_data_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: obj_type
      :type:  tinfo_t

      pointed object type



   .. py:attribute:: closure
      :type:  tinfo_t

      cannot have both closure and based_ptr_size



   .. py:attribute:: parent
      :type:  tinfo_t

      Parent struct.



   .. py:attribute:: delta
      :type:  int

      Offset from the beginning of the parent struct.



   .. py:attribute:: based_ptr_size
      :type:  uchar


   .. py:attribute:: taptr_bits
      :type:  uchar

      TAH bits.



   .. py:method:: swap(r: ptr_type_data_t) -> None

      Set this = r and r = this.



   .. py:method:: is_code_ptr() -> bool

      Are we pointing to code?



   .. py:method:: is_shifted() -> bool


.. py:class:: array_type_data_t(b: size_t = 0, n: size_t = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: elem_type
      :type:  tinfo_t

      element type



   .. py:attribute:: base
      :type:  int

      array base



   .. py:attribute:: nelems
      :type:  int

      number of elements



   .. py:method:: swap(r: array_type_data_t) -> None

      set this = r and r = this



.. py:class:: funcarg_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: argloc
      :type:  argloc_t

      argument location



   .. py:attribute:: name
      :type:  str

      argument name (may be empty)



   .. py:attribute:: cmt
      :type:  str

      argument comment (may be empty)



   .. py:attribute:: type
      :type:  tinfo_t

      argument type



   .. py:attribute:: flags
      :type:  int

      Function argument property bits 
              



.. py:data:: FAI_HIDDEN

   hidden argument


.. py:data:: FAI_RETPTR

   pointer to return value. implies hidden


.. py:data:: FAI_STRUCT

   was initially a structure


.. py:data:: FAI_ARRAY

   was initially an array; see "__org_typedef" or "__org_arrdim" type attributes to determine the original type 
           


.. py:data:: FAI_UNUSED

   argument is not used by the function


.. py:class:: func_type_data_t

   Bases: :py:obj:`funcargvec_t`


   .. py:attribute:: thisown


   .. py:attribute:: flags
      :type:  int

      Function type data property bits 
              



   .. py:attribute:: rettype
      :type:  tinfo_t

      return type



   .. py:attribute:: retloc
      :type:  argloc_t

      return location



   .. py:attribute:: stkargs
      :type:  int

      size of stack arguments (not used in build_func_type)



   .. py:attribute:: spoiled
      :type:  reginfovec_t

      spoiled register information. if spoiled register info is present, it overrides the standard spoil info (eax, edx, ecx for x86) 
              



   .. py:method:: get_explicit_cc() -> callcnv_t


   .. py:method:: set_cc(cc: callcnv_t) -> None


   .. py:method:: swap(r: func_type_data_t) -> None


   .. py:method:: is_high() -> bool


   .. py:method:: is_noret() -> bool


   .. py:method:: is_pure() -> bool


   .. py:method:: is_static() -> bool


   .. py:method:: is_virtual() -> bool


   .. py:method:: is_const() -> bool


   .. py:method:: is_ctor() -> bool


   .. py:method:: is_dtor() -> bool


   .. py:method:: get_call_method() -> int


   .. py:method:: is_vararg_cc() -> bool


   .. py:method:: is_golang_cc() -> bool


   .. py:method:: is_swift_cc() -> bool


   .. py:method:: is_user_cc() -> bool


   .. py:method:: guess_cc(purged: int, cc_flags: int) -> callcnv_t

      Guess function calling convention use the following info: argument locations and 'stkargs' 
              



   .. py:method:: dump(praloc_bits: int = 2) -> bool

      Dump information that is not always visible in the function prototype. (argument locations, return location, total stkarg size) 
              



   .. py:method:: find_argument(*args) -> ssize_t

      find argument by name



.. py:data:: FTI_SPOILED

   information about spoiled registers is present


.. py:data:: FTI_NORET

   noreturn


.. py:data:: FTI_PURE

   __pure


.. py:data:: FTI_HIGH

   high level prototype (with possibly hidden args)


.. py:data:: FTI_STATIC

   static


.. py:data:: FTI_VIRTUAL

   virtual


.. py:data:: FTI_CALLTYPE

   mask for FTI_*CALL


.. py:data:: FTI_DEFCALL

   default call


.. py:data:: FTI_NEARCALL

   near call


.. py:data:: FTI_FARCALL

   far call


.. py:data:: FTI_INTCALL

   interrupt call


.. py:data:: FTI_ARGLOCS

   info about argument locations has been calculated (stkargs and retloc too) 
           


.. py:data:: FTI_EXPLOCS

   all arglocs are specified explicitly


.. py:data:: FTI_CONST

   const member function


.. py:data:: FTI_CTOR

   constructor


.. py:data:: FTI_DTOR

   destructor


.. py:data:: FTI_ALL

   all defined bits


.. py:data:: CC_CDECL_OK

   can use __cdecl calling convention?


.. py:data:: CC_ALLOW_ARGPERM

   disregard argument order?


.. py:data:: CC_ALLOW_REGHOLES

   allow holes in register argument list?


.. py:data:: CC_HAS_ELLIPSIS

   function has a variable list of arguments?


.. py:data:: CC_GOLANG_OK

   can use __golang calling convention 
           


.. py:data:: FMTFUNC_PRINTF

.. py:data:: FMTFUNC_SCANF

.. py:data:: FMTFUNC_STRFTIME

.. py:data:: FMTFUNC_STRFMON

.. py:class:: edm_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str


   .. py:attribute:: cmt
      :type:  str


   .. py:attribute:: value
      :type:  uint64


   .. py:method:: empty() -> bool


   .. py:method:: swap(r: edm_t) -> None


   .. py:method:: get_tid() -> tid_t


.. py:class:: enum_type_data_t(*args)

   Bases: :py:obj:`edmvec_t`


   .. py:attribute:: thisown


   .. py:attribute:: group_sizes
      :type:  intvec_t

      if present, specifies bitmask group sizes each non-trivial group starts with a mask member 
              



   .. py:attribute:: taenum_bits
      :type:  int

      Type attributes for enums



   .. py:attribute:: bte
      :type:  bte_t

      enum member sizes (shift amount) and style. do not manually set BTE_BITMASK, use set_enum_is_bitmask() 
              



   .. py:method:: get_enum_radix() -> int

      Get enum constant radix 
              
      :returns: radix or 1 for BTE_CHAR



   .. py:method:: is_number_signed() -> bool


   .. py:method:: set_enum_radix(radix: int, sign: bool) -> None

      Set radix to display constants 
              
      :param radix: radix with the special case 1 to display as character



   .. py:method:: is_char() -> bool


   .. py:method:: is_dec() -> bool


   .. py:method:: is_hex() -> bool


   .. py:method:: is_oct() -> bool


   .. py:method:: is_bin() -> bool


   .. py:method:: is_udec() -> bool


   .. py:method:: is_shex() -> bool


   .. py:method:: is_soct() -> bool


   .. py:method:: is_sbin() -> bool


   .. py:method:: has_lzero() -> bool


   .. py:method:: set_lzero(on: bool) -> None


   .. py:method:: calc_mask() -> uint64


   .. py:method:: store_64bit_values() -> bool


   .. py:method:: is_bf() -> bool

      is bitmask or ordinary enum?



   .. py:method:: calc_nbytes() -> int

      get the width of enum in bytes



   .. py:method:: set_nbytes(nbytes: int) -> bool

      set enum width (nbytes)



   .. py:method:: is_group_mask_at(idx: size_t) -> bool

      is the enum member at IDX a non-trivial group mask? a trivial group consist of one bit and has just one member, which can be considered as a mask or a bitfield constant 
              
      :param idx: index
      :returns: success



   .. py:method:: is_valid_group_sizes() -> bool

      is valid group sizes



   .. py:method:: find_member(*args) -> ssize_t

      This function has the following signatures:

          0. find_member(name: str, from: size_t=0, to: size_t=size_t(-1)) -> ssize_t
          1. find_member(value: uint64, serial: uchar, from: size_t=0, to: size_t=size_t(-1), vmask: uint64=uint64(-1)) -> ssize_t

      # 0: find_member(name: str, from: size_t=0, to: size_t=size_t(-1)) -> ssize_t

      find member (constant or bmask) by name


      # 1: find_member(value: uint64, serial: uchar, from: size_t=0, to: size_t=size_t(-1), vmask: uint64=uint64(-1)) -> ssize_t

      find member (constant or bmask) by value



   .. py:method:: swap(r: enum_type_data_t) -> None

      swap two instances



   .. py:method:: add_constant(name: str, value: uint64, cmt: str = None) -> None

      add constant for regular enum



   .. py:method:: get_value_repr(repr: value_repr_t) -> tinfo_code_t

      get enum radix and other representation info 
              
      :param repr: value display info



   .. py:method:: set_value_repr(repr: value_repr_t) -> tinfo_code_t

      set enum radix and other representation info 
              
      :param repr: value display info



   .. py:method:: get_serial(index: size_t) -> uchar

      returns serial for the constant



   .. py:method:: get_max_serial(value: uint64) -> uchar

      return the maximum serial for the value



   .. py:method:: get_constant_group(*args) -> PyObject *

      get group parameters for the constant, valid for bitmask enum 
              
      :param group_start_index: index of the group mask
      :param group_size: group size (>=1)
      :param idx: constant index
      :returns: success



   .. py:method:: all_groups(skip_trivial=False)

      Generate tuples for bitmask enum groups.
      Each tupple is:
      [0] enum member index of group start
      [1] group size
      Tupples may include or not the group with 1 element.



   .. py:method:: all_constants()

      Generate tupples of all constants except of bitmasks.
      Each tupple is:
      [0] constant index
      [1] enum member index of group start
      [2] group size
      In case of regular enum the second element of tupple is 0 and the third element of tupple is the number of enum members.



.. py:class:: typedef_type_data_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: til
      :type:  til_t const *

      type library to use when resolving



   .. py:attribute:: name
      :type:  str

      is_ordref=false: target type name. we do not own this pointer!



   .. py:attribute:: ordinal
      :type:  int

      is_ordref=true: type ordinal number



   .. py:attribute:: is_ordref
      :type:  bool

      is reference by ordinal?



   .. py:attribute:: resolve
      :type:  bool

      should resolve immediately?



   .. py:method:: swap(r: typedef_type_data_t) -> None


.. py:data:: MAX_ENUM_SERIAL

   Max number of identical constants allowed for one enum type.


.. py:class:: custom_data_type_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: dtid
      :type:  int16

      data type id



   .. py:attribute:: fid
      :type:  int16

      data format ids



.. py:class:: value_repr_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: bits
      :type:  uint64


   .. py:attribute:: ri
      :type:  refinfo_t

      FRB_OFFSET.



   .. py:attribute:: strtype
      :type:  int

      FRB_STRLIT.



   .. py:attribute:: delta
      :type:  adiff_t

      FRB_STROFF.



   .. py:attribute:: type_ordinal
      :type:  int

      FRB_STROFF, FRB_ENUM.



   .. py:attribute:: cd
      :type:  custom_data_type_info_t

      FRB_CUSTOM.



   .. py:attribute:: ap
      :type:  array_parameters_t

      FRB_TABFORM, AP_SIGNED is ignored, use FRB_SIGNED instead 
              



   .. py:method:: swap(r: value_repr_t) -> None


   .. py:method:: clear() -> None


   .. py:method:: empty() -> bool


   .. py:method:: is_enum() -> bool


   .. py:method:: is_offset() -> bool


   .. py:method:: is_strlit() -> bool


   .. py:method:: is_custom() -> bool


   .. py:method:: is_stroff() -> bool


   .. py:method:: is_typref() -> bool


   .. py:method:: is_signed() -> bool


   .. py:method:: has_tabform() -> bool


   .. py:method:: has_lzeroes() -> bool


   .. py:method:: get_vtype() -> uint64


   .. py:method:: set_vtype(vt: uint64) -> None


   .. py:method:: set_signed(on: bool) -> None


   .. py:method:: set_tabform(on: bool) -> None


   .. py:method:: set_lzeroes(on: bool) -> None


   .. py:method:: set_ap(_ap: array_parameters_t) -> None


   .. py:method:: init_ap(_ap: array_parameters_t) -> None


   .. py:method:: from_opinfo(flags: flags64_t, afl: aflags_t, opinfo: opinfo_t, _ap: array_parameters_t) -> bool


   .. py:method:: parse_value_repr(*args) -> bool


.. py:data:: FRB_MASK

   Mask for the value type (* means requires additional info):


.. py:data:: FRB_UNK

   Unknown.


.. py:data:: FRB_NUMB

   Binary number.


.. py:data:: FRB_NUMO

   Octal number.


.. py:data:: FRB_NUMH

   Hexadecimal number.


.. py:data:: FRB_NUMD

   Decimal number.


.. py:data:: FRB_FLOAT

   Floating point number (for interpreting an integer type as a floating value) 
           


.. py:data:: FRB_CHAR

   Char.


.. py:data:: FRB_SEG

   Segment.


.. py:data:: FRB_ENUM

   *Enumeration


.. py:data:: FRB_OFFSET

   *Offset


.. py:data:: FRB_STRLIT

   *String literal (used for arrays)


.. py:data:: FRB_STROFF

   *Struct offset


.. py:data:: FRB_CUSTOM

   *Custom data type


.. py:data:: FRB_INVSIGN

   Invert sign (0x01 is represented as -0xFF)


.. py:data:: FRB_INVBITS

   Invert bits (0x01 is represented as ~0xFE)


.. py:data:: FRB_SIGNED

   Force signed representation.


.. py:data:: FRB_LZERO

   Toggle leading zeroes (used for integers)


.. py:data:: FRB_TABFORM

   has additional tabular parameters 
           


.. py:class:: udm_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: offset
      :type:  uint64

      member offset in bits



   .. py:attribute:: size
      :type:  uint64

      size in bits



   .. py:attribute:: name
      :type:  str

      member name



   .. py:attribute:: cmt
      :type:  str

      member comment



   .. py:attribute:: type
      :type:  tinfo_t

      member type



   .. py:attribute:: repr
      :type:  value_repr_t

      radix, refinfo, strpath, custom_id, strtype



   .. py:attribute:: effalign
      :type:  int

      effective field alignment (in bytes)



   .. py:attribute:: tafld_bits
      :type:  int

      TAH bits.



   .. py:attribute:: fda
      :type:  uchar

      field alignment (shift amount)



   .. py:method:: empty() -> bool


   .. py:method:: is_bitfield() -> bool


   .. py:method:: is_zero_bitfield() -> bool


   .. py:method:: is_unaligned() -> bool


   .. py:method:: is_baseclass() -> bool


   .. py:method:: is_virtbase() -> bool


   .. py:method:: is_vftable() -> bool


   .. py:method:: is_method() -> bool


   .. py:method:: is_gap() -> bool


   .. py:method:: is_regcmt() -> bool


   .. py:method:: is_retaddr() -> bool


   .. py:method:: is_savregs() -> bool


   .. py:method:: is_special_member() -> bool


   .. py:method:: is_by_til() -> bool


   .. py:method:: set_unaligned(on: bool = True) -> None


   .. py:method:: set_baseclass(on: bool = True) -> None


   .. py:method:: set_virtbase(on: bool = True) -> None


   .. py:method:: set_vftable(on: bool = True) -> None


   .. py:method:: set_method(on: bool = True) -> None


   .. py:method:: set_regcmt(on: bool = True) -> None


   .. py:method:: set_retaddr(on: bool = True) -> None


   .. py:method:: set_savregs(on: bool = True) -> None


   .. py:method:: set_by_til(on: bool = True) -> None


   .. py:method:: clr_unaligned() -> None


   .. py:method:: clr_baseclass() -> None


   .. py:method:: clr_virtbase() -> None


   .. py:method:: clr_vftable() -> None


   .. py:method:: clr_method() -> None


   .. py:method:: begin() -> uint64


   .. py:method:: end() -> uint64


   .. py:method:: compare_with(r: udm_t, tcflags: int) -> bool


   .. py:method:: swap(r: udm_t) -> None


   .. py:method:: is_anonymous_udm() -> bool


   .. py:method:: set_value_repr(r: value_repr_t) -> None


   .. py:method:: can_be_dtor() -> bool


   .. py:method:: can_rename() -> bool


.. py:class:: udtmembervec_t

   Bases: :py:obj:`udtmembervec_template_t`


   .. py:attribute:: thisown


.. py:class:: udt_type_data_t

   Bases: :py:obj:`udtmembervec_t`


   .. py:attribute:: thisown


   .. py:attribute:: total_size
      :type:  size_t

      total structure size in bytes



   .. py:attribute:: unpadded_size
      :type:  size_t

      unpadded structure size in bytes



   .. py:attribute:: effalign
      :type:  int

      effective structure alignment (in bytes)



   .. py:attribute:: taudt_bits
      :type:  int

      TA... and TAUDT... bits.



   .. py:attribute:: version
      :type:  uchar

      version of udt_type_data_t



   .. py:attribute:: sda
      :type:  uchar

      declared structure alignment (shift amount+1). 0 - unspecified



   .. py:attribute:: pack
      :type:  uchar

      #pragma pack() alignment (shift amount)



   .. py:attribute:: is_union
      :type:  bool

      is union or struct?



   .. py:method:: swap(r: udt_type_data_t) -> None


   .. py:method:: is_unaligned() -> bool


   .. py:method:: is_msstruct() -> bool


   .. py:method:: is_cppobj() -> bool


   .. py:method:: is_vftable() -> bool


   .. py:method:: is_fixed() -> bool


   .. py:method:: is_tuple() -> bool


   .. py:method:: set_vftable(on: bool = True) -> None


   .. py:method:: set_fixed(on: bool = True) -> None


   .. py:method:: set_tuple(on: bool = True) -> None


   .. py:method:: is_last_baseclass(idx: size_t) -> bool


   .. py:method:: add_member(_name: str, _type: tinfo_t, _offset: uint64 = 0) -> udm_t &

      Add a new member to a structure or union. This function just pushes a new member to the back of the structure/union member vector.

      :param _name: Member name. Must not be nullptr.
      :param _type: Member type. Must not be empty.
      :param _offset: Member offset in bits. It is the caller's responsibility to specify correct offsets.
      :returns: { Reference to the newly added member }



   .. py:method:: find_member(*args) -> ssize_t

      This function has the following signatures:

          0. find_member(pattern_udm: udm_t *, strmem_flags: int) -> ssize_t
          1. find_member(name: str) -> ssize_t
          2. find_member(bit_offset: uint64) -> ssize_t

      # 0: find_member(pattern_udm: udm_t *, strmem_flags: int) -> ssize_t

      tinfo_t::find_udm 
              
      :returns: the index of the found member or -1

      # 1: find_member(name: str) -> ssize_t


      # 2: find_member(bit_offset: uint64) -> ssize_t



   .. py:method:: get_best_fit_member(disp)

      Get the member that is most likely referenced by the specified offset.

      :param disp: the byte offset
      :returns: a tuple (int, udm_t), or (-1, None) if member not found



.. py:data:: STRUC_SEPARATOR

   structname.fieldname


.. py:data:: VTBL_SUFFIX

.. py:data:: VTBL_MEMNAME

.. py:function:: stroff_as_size(plen: int, tif: tinfo_t, value: asize_t) -> bool

   Should display a structure offset expression as the structure size?


.. py:class:: udm_visitor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: visit_udm(tid: tid_t, tif: tinfo_t, udt: udt_type_data_t, idx: ssize_t) -> int

      :param tid: udt tid
      :param tif: udt type info (may be nullptr for corrupted idbs)
      :param udt: udt type data (may be nullptr for corrupted idbs)
      :param idx: the index of udt the member (may be -1 if udm was not found)



.. py:function:: visit_stroff_udms(sfv: udm_visitor_t, path: tid_t const *, disp: adiff_t *, appzero: bool) -> adiff_t *

   Visit structure fields in a stroff expression or in a reference to a struct data variable. This function can be used to enumerate all components of an expression like 'a.b.c'. 
           
   :param sfv: visitor object
   :param path: struct path (path[0] contains the initial struct id)
   :param disp: offset into structure
   :param appzero: should visit field at offset zero?
   :returns: visitor result


.. py:class:: bitfield_type_data_t(_nbytes: uchar = 0, _width: uchar = 0, _is_unsigned: bool = False)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: nbytes
      :type:  uchar

      enclosing type size (1,2,4,8 bytes)



   .. py:attribute:: width
      :type:  uchar

      number of bits



   .. py:attribute:: is_unsigned
      :type:  bool

      is bitfield unsigned?



   .. py:method:: compare(r: bitfield_type_data_t) -> int


   .. py:method:: swap(r: bitfield_type_data_t) -> None


   .. py:method:: is_valid_bitfield() -> bool


.. py:data:: TPOS_LNNUM

.. py:data:: TPOS_REGCMT

.. py:function:: is_one_bit_mask(mask: int) -> bool

   Is bitmask one bit?


.. py:function:: inf_pack_stkargs(*args) -> bool

.. py:function:: inf_big_arg_align(*args) -> bool

.. py:function:: inf_huge_arg_align(*args) -> bool

.. py:class:: type_mods_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: type
      :type:  tinfo_t

      current type



   .. py:attribute:: name
      :type:  str

      current type name



   .. py:attribute:: cmt
      :type:  str

      comment for current type



   .. py:attribute:: flags
      :type:  int

      Type modification bits 
              



   .. py:method:: clear() -> None


   .. py:method:: set_new_type(t: tinfo_t) -> None

      The visit_type() function may optionally save the modified type info. Use the following functions for that. The new name and comment will be applied only if the current tinfo element has storage for them. 
              



   .. py:method:: set_new_name(n: str) -> None


   .. py:method:: set_new_cmt(c: str, rptcmt: bool) -> None


   .. py:method:: has_type() -> bool


   .. py:method:: has_name() -> bool


   .. py:method:: has_cmt() -> bool


   .. py:method:: is_rptcmt() -> bool


   .. py:method:: has_info() -> bool


.. py:data:: TVIS_TYPE

   new type info is present


.. py:data:: TVIS_NAME

   new name is present (only for funcargs and udt members)


.. py:data:: TVIS_CMT

   new comment is present (only for udt members)


.. py:data:: TVIS_RPTCMT

   the new comment is repeatable


.. py:class:: tinfo_visitor_t(s: int = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: state
      :type:  int

      tinfo visitor states 
              



   .. py:method:: visit_type(out: type_mods_t, tif: tinfo_t, name: str, cmt: str) -> int

      Visit a subtype. this function must be implemented in the derived class. it may optionally fill out with the new type info. this can be used to modify types (in this case the 'out' argument of apply_to() may not be nullptr) return 0 to continue the traversal. return !=0 to stop the traversal. 
              



   .. py:method:: prune_now() -> None

      To refuse to visit children of the current type, use this:



   .. py:method:: apply_to(tif: tinfo_t, out: type_mods_t = None, name: str = None, cmt: str = None) -> int

      Call this function to initiate the traversal.



.. py:data:: TVST_PRUNE

   don't visit children of current type


.. py:data:: TVST_DEF

   visit type definition (meaningful for typerefs)


.. py:data:: TVST_LEVEL

.. py:class:: regobj_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: regidx
      :type:  int

      index into dbg->registers



   .. py:attribute:: relocate
      :type:  int

      0-plain num, 1-must relocate



   .. py:attribute:: value
      :type:  bytevec_t


   .. py:method:: size() -> size_t


.. py:class:: regobjs_t

   Bases: :py:obj:`regobjvec_t`


   .. py:attribute:: thisown


.. py:function:: unpack_idcobj_from_idb(obj: idc_value_t *, tif: tinfo_t, ea: ida_idaapi.ea_t, off0: bytevec_t const *, pio_flags: int = 0) -> error_t

   Collection of register objects.

   Read a typed idc object from the database 
           


.. py:data:: PIO_NOATTR_FAIL

   missing attributes are not ok


.. py:data:: PIO_IGNORE_PTRS

   do not follow pointers


.. py:function:: unpack_idcobj_from_bv(obj: idc_value_t *, tif: tinfo_t, bytes: bytevec_t const &, pio_flags: int = 0) -> error_t

   Read a typed idc object from the byte vector.


.. py:function:: pack_idcobj_to_idb(obj: idc_value_t const *, tif: tinfo_t, ea: ida_idaapi.ea_t, pio_flags: int = 0) -> error_t

   Write a typed idc object to the database.


.. py:function:: pack_idcobj_to_bv(obj: idc_value_t const *, tif: tinfo_t, bytes: relobj_t, objoff: void *, pio_flags: int = 0) -> error_t

   Write a typed idc object to the byte vector. Byte vector may be non-empty, this function will append data to it 
           


.. py:function:: apply_tinfo_to_stkarg(insn: insn_t const &, x: op_t const &, v: int, tif: tinfo_t, name: str) -> bool

   Helper function for the processor modules. to be called from processor_t::use_stkarg_type 
           


.. py:class:: argtinfo_helper_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: reserved
      :type:  size_t


   .. py:method:: set_op_tinfo(insn: insn_t const &, x: op_t const &, tif: tinfo_t, name: str) -> bool

      Set the operand type as specified.



   .. py:method:: is_stkarg_load(insn: insn_t const &, src: int *, dst: int *) -> bool

      Is the current insn a stkarg load?. if yes:
      * src: index of the source operand in insn_t::ops
      * dst: index of the destination operand in insn_t::ops insn_t::ops[dst].addr is expected to have the stack offset 


              



   .. py:method:: has_delay_slot(arg0: ida_idaapi.ea_t) -> bool

      The call instruction with a delay slot?.



   .. py:method:: use_arg_tinfos(caller: ida_idaapi.ea_t, fti: func_type_data_t, rargs: funcargvec_t) -> None

      This function is to be called by the processor module in response to ev_use_arg_types. 
              



.. py:function:: gen_use_arg_tinfos(_this: argtinfo_helper_t, caller: ida_idaapi.ea_t, fti: func_type_data_t, rargs: funcargvec_t) -> None

   Do not call this function directly, use argtinfo_helper_t.


.. py:function:: func_has_stkframe_hole(ea: ida_idaapi.ea_t, fti: func_type_data_t) -> bool

   Looks for a hole at the beginning of the stack arguments. Will make use of the IDB's func_t function at that place (if present) to help determine the presence of such a hole. 
           


.. py:class:: lowertype_helper_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: func_has_stkframe_hole(candidate: tinfo_t, candidate_data: func_type_data_t) -> bool


   .. py:method:: get_func_purged_bytes(candidate: tinfo_t, candidate_data: func_type_data_t) -> int


.. py:class:: ida_lowertype_helper_t(_tif: tinfo_t, _ea: ida_idaapi.ea_t, _pb: int)

   Bases: :py:obj:`lowertype_helper_t`


   .. py:attribute:: thisown


   .. py:method:: func_has_stkframe_hole(candidate: tinfo_t, candidate_data: func_type_data_t) -> bool


   .. py:method:: get_func_purged_bytes(candidate: tinfo_t, arg3: func_type_data_t) -> int


.. py:function:: lower_type(til: til_t, tif: tinfo_t, name: str = None, _helper: lowertype_helper_t = None) -> int

   Lower type. Inspect the type and lower all function subtypes using lower_func_type(). 
   We call the prototypes usually encountered in source files "high level" 
   They may have implicit arguments, array arguments, big structure retvals, etc 
   We introduce explicit arguments (i.e. 'this' pointer) and call the result 
   "low level prototype". See FTI_HIGH.
   In order to improve heuristics for recognition of big structure retvals, 
   it is recommended to pass a helper that will be used to make decisions. 
   That helper will be used only for lowering 'tif', and not for the children 
   types walked through by recursion. 
           
   :returns: 1: removed FTI_HIGH,
   :returns: 2: made substantial changes
   :returns: -1: failure


.. py:function:: replace_ordinal_typerefs(til: til_t, tif: tinfo_t) -> int

   Replace references to ordinal types by name references. This function 'unties' the type from the current local type library and makes it easier to export it. 
           
   :param til: type library to use. may be nullptr.
   :param tif: type to modify (in/out)
   :returns: number: of replaced subtypes, -1 on failure


.. py:data:: UTP_ENUM

.. py:data:: UTP_STRUCT

.. py:function:: begin_type_updating(utp: update_type_t) -> None

   Mark the beginning of a large update operation on the types. Can be used with add_enum_member(), add_struc_member, etc... Also see end_type_updating() 
           


.. py:function:: end_type_updating(utp: update_type_t) -> None

   Mark the end of a large update operation on the types (see begin_type_updating())


.. py:function:: get_named_type_tid(name: str) -> tid_t

   Get named local type TID 
           
   :param name: type name
   :returns: TID or BADADDR


.. py:function:: get_tid_name(tid: tid_t) -> str

   Get a type name for the specified TID 
           
   :param tid: type TID
   :returns: true if there is type with TID


.. py:function:: get_tid_ordinal(tid: tid_t) -> int

   Get type ordinal number for TID 
           
   :param tid: type/enum constant/udt member TID
   :returns: type ordinal number or 0


.. py:function:: get_udm_by_fullname(udm: udm_t, fullname: str) -> ssize_t

   Get udt member by full name 
           
   :param udm: member, can be NULL
   :param fullname: udt member name in format <udt name>.<member name>
   :returns: member index into udt_type_data_t or -1


.. py:function:: get_idainfo_by_udm(*args) -> bool

   Calculate IDA info from udt member 
           
   :param udm: udt member
   :param refinfo_ea: if specified will be used to adjust the refinfo_t data


.. py:function:: create_enum_type(enum_name: str, ei: enum_type_data_t, enum_width: int, sign: type_sign_t, convert_to_bitmask: bool, enum_cmt: str = None) -> tid_t

   Create type enum 
           
   :param enum_name: type name
   :param ei: enum type data
   :param enum_width: the width of an enum element allowed values: 0 (unspecified),1,2,4,8,16,32,64
   :param sign: enum sign
   :param convert_to_bitmask: try convert enum to bitmask enum
   :param enum_cmt: enum type comment
   :returns: enum TID


.. py:class:: valstr_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: oneline
      :type:  str

      result if printed on one line in UTF-8 encoding



   .. py:attribute:: length
      :type:  size_t

      length if printed on one line



   .. py:attribute:: members
      :type:  valstrs_t *

      strings for members, each member separately



   .. py:attribute:: info
      :type:  valinfo_t *

      additional info



   .. py:attribute:: props
      :type:  int

      temporary properties, used internally



.. py:data:: VALSTR_OPEN

   printed opening curly brace '{'


.. py:class:: valstrs_t

   Bases: :py:obj:`valstrvec_t`


   .. py:attribute:: thisown


.. py:class:: text_sink_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


.. py:data:: PDF_INCL_DEPS

   Include all type dependencies.


.. py:data:: PDF_DEF_FWD

   Allow forward declarations.


.. py:data:: PDF_DEF_BASE

   Include base types: __int8, __int16, etc..


.. py:data:: PDF_HEADER_CMT

   Prepend output with a descriptive comment.


.. py:function:: calc_number_of_children(loc: argloc_t, tif: tinfo_t, dont_deref_ptr: bool = False) -> int

   Calculate max number of lines of a formatted c data, when expanded (PTV_EXPAND). 
           
   :param loc: location of the data (ALOC_STATIC or ALOC_CUSTOM)
   :param tif: type info
   :param dont_deref_ptr: consider 'ea' as the ptr value
   :returns: 0: data is not expandable
   :returns: -1: error, see qerrno
   :returns: else: the max number of lines


.. py:function:: get_enum_member_expr(tif: tinfo_t, serial: int, value: uint64) -> str

   Return a C expression that can be used to represent an enum member. If the value does not correspond to any single enum member, this function tries to find a bitwise combination of enum members that correspond to it. If more than half of value bits do not match any enum members, it fails. 
           
   :param tif: enumeration type
   :param serial: which enumeration member to use (0 means the first with the given value)
   :param value: value to search in the enumeration type
   :returns: success


.. py:class:: til_symbol_t(n: str = None, t: til_t = None)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str

      symbol name



   .. py:attribute:: til
      :type:  til_t const *

      pointer to til



.. py:class:: predicate_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: should_display(til: til_t, name: str, type: type_t const *, fields: p_list const *) -> bool


.. py:function:: choose_named_type(out_sym: til_symbol_t, root_til: til_t, title: str, ntf_flags: int, predicate: predicate_t = None) -> bool

   Choose a type from a type library. 
           
   :param out_sym: pointer to be filled with the chosen type
   :param root_til: pointer to starting til (the function will inspect the base tils if allowed by flags)
   :param title: title of listbox to display
   :param ntf_flags: combination of Flags for named types
   :param predicate: predicate to select types to display (maybe nullptr)
   :returns: false if nothing is chosen, otherwise true


.. py:function:: choose_local_tinfo(ti: til_t, title: str, func: local_tinfo_predicate_t * = None, def_ord: int = 0, ud: void * = None) -> int

   Choose a type from the local type library. 
           
   :param ti: pointer to til
   :param title: title of listbox to display
   :param func: predicate to select types to display (maybe nullptr)
   :param def_ord: ordinal to position cursor before choose
   :param ud: user data
   :returns: == 0 means nothing is chosen, otherwise an ordinal number


.. py:function:: choose_local_tinfo_and_delta(delta: int32 *, ti: til_t, title: str, func: local_tinfo_predicate_t * = None, def_ord: int = 0, ud: void * = None) -> int

   Choose a type from the local type library and specify the pointer shift value. 
           
   :param delta: pointer shift value
   :param ti: pointer to til
   :param title: title of listbox to display
   :param func: predicate to select types to display (maybe nullptr)
   :param def_ord: ordinal to position cursor before choose
   :param ud: user data
   :returns: == 0 means nothing is chosen, otherwise an ordinal number


.. py:function:: calc_retloc(*args) -> bool

   This function has the following signatures:

       0. calc_retloc(fti: func_type_data_t *) -> bool
       1. calc_retloc(retloc: argloc_t *, rettype: const tinfo_t &, cc: callcnv_t) -> bool

   # 0: calc_retloc(fti: func_type_data_t *) -> bool


   # 1: calc_retloc(retloc: argloc_t *, rettype: const tinfo_t &, cc: callcnv_t) -> bool


.. py:class:: til_type_ref_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: cb
      :type:  size_t


   .. py:attribute:: tif
      :type:  tinfo_t


   .. py:attribute:: cursor
      :type:  tif_cursor_t


   .. py:attribute:: ordinal
      :type:  int


   .. py:attribute:: is_writable
      :type:  bool


   .. py:attribute:: is_detached
      :type:  bool


   .. py:attribute:: is_forward
      :type:  bool


   .. py:attribute:: kind
      :type:  type_t


   .. py:attribute:: memidx
      :type:  ssize_t


   .. py:attribute:: nmembers
      :type:  size_t


   .. py:attribute:: udm
      :type:  udm_t

      BTF_STRUCT or BTF_UNION: the current member.



   .. py:attribute:: total_size
      :type:  size_t


   .. py:attribute:: unpadded_size
      :type:  size_t


   .. py:attribute:: last_udm_offset
      :type:  uint64


   .. py:attribute:: bucket_start
      :type:  uint64


   .. py:attribute:: bf_bitoff
      :type:  int


   .. py:attribute:: offset
      :type:  uint64


   .. py:attribute:: edm
      :type:  edm_t

      BTF_ENUM: the current enum member.



   .. py:attribute:: fa
      :type:  funcarg_t const *

      BT_FUNC: the current argument, nullptr - ellipsis.



   .. py:method:: clear() -> None


   .. py:method:: on_member() -> bool


   .. py:method:: is_typedef() -> bool


   .. py:method:: is_struct() -> bool


   .. py:method:: is_union() -> bool


   .. py:method:: is_enum() -> bool


   .. py:method:: is_func() -> bool


   .. py:method:: is_udt() -> bool


.. py:function:: register_custom_callcnv(cnv_incref: custom_callcnv_t) -> custom_callcnv_t *

   Register a calling convention 
           
   :returns: CM_CC_INVALID means failure:
   * bad ccinf.name
   * ccinf.name already exists
   * the calling convention is special (usercall, purging, vararg) and there are too many of them already


.. py:function:: unregister_custom_callcnv(cnv_decref: custom_callcnv_t) -> custom_callcnv_t *

   Unregister a calling convention 
           
   :returns: true if successfully unregistered the custom calling convention


.. py:function:: idc_parse_decl(til: til_t, decl: str, flags: int) -> Tuple[str, bytes, bytes]

.. py:function:: calc_type_size(til: til_t, type: bytes)

   Returns the size of a type
   :param til: Type info library. 'None' can be passed.
   :param type: serialized type byte string
   :returns: The size of the type (None on failure)


.. py:function:: apply_type(til: til_t, type: bytes, fields: bytes, ea: ida_idaapi.ea_t, flags: int) -> bool

   Apply the specified type to the address

   :param til: Type info library. 'None' can be used.
   :param type: type string
   :param fields: fields string (may be empty or None)
   :param ea: the address of the object
   :param flags: combination of TINFO_... constants or 0
   :returns: Boolean


.. py:function:: get_arg_addrs(caller: ida_idaapi.ea_t)

   Retrieve addresses of argument initialization instructions

   :param caller: the address of the call instruction
   :returns: list of instruction addresses


.. py:function:: unpack_object_from_idb(til: til_t, type: bytes, fields: bytes, ea: ida_idaapi.ea_t, pio_flags: int = 0)

   Unpacks from the database at 'ea' to an object.
   Please refer to unpack_object_from_bv()


.. py:function:: unpack_object_from_bv(til: til_t, type: unpack_object_from_bv.bytes, fields: unpack_object_from_bv.bytes, bytes, pio_flags: int = 0)

   Unpacks a buffer into an object.
   Returns the error_t returned by idaapi.pack_object_to_idb

   :param til: Type library. 'None' can be passed.
   :param type: type string
   :param fields: fields string (may be empty or None)
   :param bytes: the bytes to unpack
   :param pio_flags: flags used while unpacking
   :returns: tuple(1, obj) on success, or tuple(0, err) on failure


.. py:function:: pack_object_to_idb(obj, til: til_t, type: bytes, fields: bytes, ea: ida_idaapi.ea_t, pio_flags: int = 0)

   Write a typed object to the database.
   Raises an exception if wrong parameters were passed or conversion fails
   Returns the error_t returned by idaapi.pack_object_to_idb

   :param til: Type library. 'None' can be passed.
   :param type: type string
   :param fields: fields string (may be empty or None)
   :param ea: ea to be used while packing
   :param pio_flags: flags used while unpacking


.. py:function:: pack_object_to_bv(obj, til: til_t, type: bytes, fields: bytes, base_ea: ida_idaapi.ea_t, pio_flags: int = 0)

   Packs a typed object to a string

   :param til: Type library. 'None' can be passed.
   :param type: type string
   :param fields: fields string (may be empty or None)
   :param base_ea: base ea used to relocate the pointers in the packed object
   :param pio_flags: flags used while unpacking
   :returns: tuple(1, packed_buf) on success, or tuple(0, err_code) on failure


.. py:data:: PT_FILE

.. py:data:: PT_STANDALONE

.. py:function:: idc_parse_types(input: str, flags: int) -> int

.. py:function:: idc_get_type_raw(ea: ida_idaapi.ea_t) -> PyObject *

.. py:function:: idc_get_local_type_raw(ordinal) -> Tuple[bytes, bytes]

.. py:function:: idc_guess_type(ea: ida_idaapi.ea_t) -> str

.. py:function:: idc_get_type(ea: ida_idaapi.ea_t) -> str

.. py:function:: idc_set_local_type(ordinal: int, dcl: str, flags: int) -> int

.. py:function:: idc_get_local_type(ordinal: int, flags: int) -> str

.. py:function:: idc_print_type(type: bytes, fields: bytes, name: str, flags: int) -> str

.. py:function:: idc_get_local_type_name(ordinal: int) -> str

.. py:function:: get_named_type(til: til_t, name: str, ntf_flags: int)

   Get a type data by its name.

   :param til: Type library
   :param name: the type name
   :param ntf_flags: a combination of NTF_* constants
   :returns: tuple(code, type_str, fields_str, cmt, field_cmts, sclass, value) on success, or None on failure


.. py:function:: get_named_type64(til: til_t, name: str, ntf_flags: int = 0) -> Union[Tuple[int, bytes, bytes, str, str, int, int], None]

   Get a named type from a type library.

   Please use til_t.get_named_type instead.


.. py:function:: print_decls(printer: text_sink_t, til: til_t, ordinals: List[int], flags: int) -> int

   Print types (and possibly their dependencies) in a format suitable for using in
   a header file. This is the reverse parse_decls().

   :param printer: a handler for printing text
   :param til: the type library holding the ordinals
   :param ordinals: a list of ordinals corresponding to the types to print
   :param flags: a combination of PDF_ constants
   :returns:  >0: the number of types exported
   :returns:   0: an error occurred
   :returns:  <0: the negated number of types exported. There were minor errors and
                  the resulting output might not be compilable.


.. py:function:: remove_tinfo_pointer(tif: tinfo_t, name: str, til: til_t) -> Tuple[bool, str]

   Remove pointer of a type. (i.e. convert "char *" into "char"). Optionally remove
   the "lp" (or similar) prefix of the input name. If the input type is not a
   pointer, then fail.

   :param tif: the type info
   :param name: the name of the type to "unpointerify"
   :param til: the type library
   :returns: a tuple (success, new-name)


.. py:function:: get_numbered_type(til: til_t, ordinal: int) -> Union[Tuple[bytes, bytes, str, str, int], None]

   Get a type from a type library, by its ordinal

   Please use til_t.get_numbered_type instead.


.. py:function:: set_numbered_type(ti: til_t, ordinal: int, ntf_flags: int, name: str, type: type_t const *, fields: p_list const * = None, cmt: str = None, fldcmts: p_list const * = None, sclass: sclass_t const * = None) -> tinfo_code_t

.. py:data:: cvar

.. py:data:: sc_auto

.. py:data:: sc_ext

.. py:data:: sc_friend

.. py:data:: sc_reg

.. py:data:: sc_stat

.. py:data:: sc_type

.. py:data:: sc_unk

.. py:data:: sc_virt

.. py:data:: TERR_SAVE

.. py:data:: TERR_WRONGNAME

.. py:data:: BADORD
   :value: 4294967295


.. py:data:: enum_member_vec_t

.. py:data:: enum_member_t

.. py:data:: udt_member_t


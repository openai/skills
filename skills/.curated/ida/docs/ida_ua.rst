ida_ua
======

.. py:module:: ida_ua

.. autoapi-nested-parse::

   Functions that deal with the disassembling of program instructions.

   There are 2 kinds of functions:

   * functions that are called from the kernel to disassemble an instruction. 
     These functions call IDP module for it.
   * functions that are called from IDP module to disassemble an instruction. 
     We will call them 'helper functions'.


   Disassembly of an instruction is made in three steps:

   0. analysis: ana.cpp
   1. emulation: emu.cpp
   2. conversion to text: out.cpp


   The kernel calls the IDP module to perform these steps. At first, the kernel 
   always calls the analysis. The analyzer must decode the instruction and fill 
   the insn_t instance that it receives through its callback. It must not change 
   anything in the database.

   The second step, the emulation, is called for each instruction. This step must 
   make necessary changes to the database, plan analysis of subsequent instructions, 
   track register values, memory contents, etc. Please keep in mind that the kernel 
   may call the emulation step for any address in the program - there is no ordering 
   of addresses. Usually, the emulation is called for consecutive addresses but 
   this is not guaranteed.

   The last step, conversion to text, is called each time an instruction is 
   displayed on the screen. The kernel will always call the analysis step before 
   calling the text conversion step. The emulation and the text conversion steps 
   should use the information stored in the insn_t instance they receive. They 
   should not access the bytes of the instruction and decode it again - this 
   should only be done in the analysis step.

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For instruction operations, see :mod:`ida_domain.instructions`.



Attributes
----------

.. autoapisummary::

   ida_ua.cvar
   ida_ua.o_void
   ida_ua.o_reg
   ida_ua.o_mem
   ida_ua.o_phrase
   ida_ua.o_displ
   ida_ua.o_imm
   ida_ua.o_far
   ida_ua.o_near
   ida_ua.o_idpspec0
   ida_ua.o_idpspec1
   ida_ua.o_idpspec2
   ida_ua.o_idpspec3
   ida_ua.o_idpspec4
   ida_ua.o_idpspec5
   ida_ua.OF_NO_BASE_DISP
   ida_ua.OF_OUTER_DISP
   ida_ua.PACK_FORM_DEF
   ida_ua.OF_NUMBER
   ida_ua.OF_SHOW
   ida_ua.dt_byte
   ida_ua.dt_word
   ida_ua.dt_dword
   ida_ua.dt_float
   ida_ua.dt_double
   ida_ua.dt_tbyte
   ida_ua.dt_packreal
   ida_ua.dt_qword
   ida_ua.dt_byte16
   ida_ua.dt_code
   ida_ua.dt_void
   ida_ua.dt_fword
   ida_ua.dt_bitfild
   ida_ua.dt_string
   ida_ua.dt_unicode
   ida_ua.dt_ldbl
   ida_ua.dt_byte32
   ida_ua.dt_byte64
   ida_ua.dt_half
   ida_ua.INSN_MACRO
   ida_ua.INSN_MODMAC
   ida_ua.INSN_64BIT
   ida_ua.STKVAR_VALID_SIZE
   ida_ua.STKVAR_KEEP_EXISTING
   ida_ua.CTXF_MAIN
   ida_ua.CTXF_MULTI
   ida_ua.CTXF_CODE
   ida_ua.CTXF_STACK
   ida_ua.CTXF_GEN_XREFS
   ida_ua.CTXF_XREF_STATE
   ida_ua.XREFSTATE_NONE
   ida_ua.XREFSTATE_GO
   ida_ua.XREFSTATE_DONE
   ida_ua.CTXF_GEN_CMT
   ida_ua.CTXF_CMT_STATE
   ida_ua.COMMSTATE_NONE
   ida_ua.COMMSTATE_GO
   ida_ua.COMMSTATE_DONE
   ida_ua.CTXF_VOIDS
   ida_ua.CTXF_NORMAL_LABEL
   ida_ua.CTXF_DEMANGLED_LABEL
   ida_ua.CTXF_LABEL_OK
   ida_ua.CTXF_DEMANGLED_OK
   ida_ua.CTXF_OVSTORE_PRNT
   ida_ua.CTXF_OUTCTX_T
   ida_ua.CTXF_DBLIND_OPND
   ida_ua.CTXF_BINOP_STATE
   ida_ua.BINOPSTATE_NONE
   ida_ua.BINOPSTATE_GO
   ida_ua.BINOPSTATE_DONE
   ida_ua.CTXF_HIDDEN_ADDR
   ida_ua.CTXF_BIT_PREFIX
   ida_ua.CTXF_UNHIDE
   ida_ua.OOF_SIGNMASK
   ida_ua.OOFS_IFSIGN
   ida_ua.OOFS_NOSIGN
   ida_ua.OOFS_NEEDSIGN
   ida_ua.OOF_SIGNED
   ida_ua.OOF_NUMBER
   ida_ua.OOF_WIDTHMASK
   ida_ua.OOFW_IMM
   ida_ua.OOFW_8
   ida_ua.OOFW_16
   ida_ua.OOFW_24
   ida_ua.OOFW_32
   ida_ua.OOFW_64
   ida_ua.OOF_ADDR
   ida_ua.OOF_OUTER
   ida_ua.OOF_ZSTROFF
   ida_ua.OOF_NOBNOT
   ida_ua.OOF_SPACES
   ida_ua.OOF_ANYSERIAL
   ida_ua.OOF_LZEROES
   ida_ua.OOF_NO_LZEROES
   ida_ua.DEFAULT_INDENT
   ida_ua.MAKELINE_NONE
   ida_ua.MAKELINE_BINPREF
   ida_ua.MAKELINE_VOID
   ida_ua.MAKELINE_STACK
   ida_ua.GH_PRINT_PROC
   ida_ua.GH_PRINT_ASM
   ida_ua.GH_PRINT_BYTESEX
   ida_ua.GH_PRINT_HEADER
   ida_ua.GH_BYTESEX_HAS_HIGHBYTE
   ida_ua.GH_PRINT_PROC_AND_ASM
   ida_ua.GH_PRINT_PROC_ASM_AND_BYTESEX
   ida_ua.GH_PRINT_ALL
   ida_ua.GH_PRINT_ALL_BUT_BYTESEX
   ida_ua.FCBF_CONT
   ida_ua.FCBF_ERR_REPL
   ida_ua.FCBF_FF_LIT
   ida_ua.FCBF_DELIM
   ida_ua.ua_mnem


Classes
-------

.. autoapisummary::

   ida_ua.operands_array
   ida_ua.op_t
   ida_ua.insn_t
   ida_ua.outctx_base_t
   ida_ua.outctx_t
   ida_ua.macro_constructor_t


Functions
---------

.. autoapisummary::

   ida_ua.insn_add_cref
   ida_ua.insn_add_dref
   ida_ua.insn_add_off_drefs
   ida_ua.insn_create_stkvar
   ida_ua.get_lookback
   ida_ua.calc_dataseg
   ida_ua.map_data_ea
   ida_ua.map_code_ea
   ida_ua.map_ea
   ida_ua.create_outctx
   ida_ua.print_insn_mnem
   ida_ua.get_dtype_flag
   ida_ua.get_dtype_size
   ida_ua.is_floating_dtype
   ida_ua.create_insn
   ida_ua.decode_insn
   ida_ua.can_decode
   ida_ua.print_operand
   ida_ua.decode_prev_insn
   ida_ua.decode_preceding_insn
   ida_ua.construct_macro
   ida_ua.get_dtype_by_size
   ida_ua.get_immvals
   ida_ua.get_printable_immvals
   ida_ua.insn_t__from_ptrval__
   ida_ua.op_t__from_ptrval__
   ida_ua.outctx_base_t__from_ptrval__
   ida_ua.outctx_t__from_ptrval__


Module Contents
---------------

.. py:class:: operands_array(data: op_t (&)[8])

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  op_t (&)[8]


   .. py:attribute:: bytes


.. py:class:: op_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: n
      :type:  uchar

      Number of operand (0,1,2). Initialized once at the start of work. You have no right to change its value. 
              



   .. py:attribute:: type
      :type:  optype_t

      Type of operand (see Operand types)



   .. py:attribute:: offb
      :type:  char

      Offset of operand value from the instruction start (0 means unknown). Of course this field is meaningful only for certain types of operands. Leave it equal to zero if the operand has no offset. This offset should point to the 'interesting' part of operand. For example, it may point to the address of a function in `call func ` or it may point to bytes holding '5' in `mov  ax, [bx+5] ` Usually bytes pointed to this offset are relocated (have fixup information). 
              



   .. py:attribute:: offo
      :type:  char

      Same as offb (some operands have 2 numeric values used to form an operand). This field is used for the second part of operand if it exists. Currently this field is used only for outer offsets of Motorola processors. Leave it equal to zero if the operand has no offset. 
              



   .. py:attribute:: flags
      :type:  uchar

      Operand flags 
              



   .. py:method:: set_shown() -> None

      Set operand to be shown.



   .. py:method:: clr_shown() -> None

      Set operand to hidden.



   .. py:method:: shown() -> bool

      Is operand set to be shown?



   .. py:attribute:: dtype
      :type:  op_dtype_t

      Type of operand value (see Operand value types). This is the type of the operand itself, not the size of the addressing mode. for example, byte ptr [epb+32_bit_offset] will have the dt_byte type. 
              



   .. py:attribute:: reg
      :type:  uint16

      number of register (o_reg)



   .. py:attribute:: phrase
      :type:  uint16

      number of register phrase (o_phrase,o_displ). you yourself define numbers of phrases as you like 
              



   .. py:method:: is_reg(r: int) -> bool

      Is register operand?



   .. py:attribute:: value
      :type:  int

      operand value (o_imm) or outer displacement (o_displ+OF_OUTER_DISP). integer values should be in IDA's (little-endian) order. when using ieee_realcvt(), floating point values should be in the processor's native byte order. dt_double and dt_qword values take up 8 bytes (value and addr fields for 32-bit modules). NB: in case a dt_dword/dt_qword immediate is forced to float by user, the kernel converts it to processor's native order before calling FP conversion routines. 
              



   .. py:method:: is_imm(v: int) -> bool

      Is immediate operand?



   .. py:attribute:: addr
      :type:  ida_idaapi.ea_t

      virtual address pointed or used by the operand. (o_mem,o_displ,o_far,o_near) 
              



   .. py:attribute:: specval
      :type:  ida_idaapi.ea_t

      This field may be used as you want. 
              



   .. py:attribute:: specflag1
      :type:  char


   .. py:attribute:: specflag2
      :type:  char


   .. py:attribute:: specflag3
      :type:  char


   .. py:attribute:: specflag4
      :type:  char


   .. py:method:: assign(other: op_t) -> None


   .. py:method:: has_reg(r)

      Checks if the operand accesses the given processor register



   .. py:attribute:: value64


.. py:data:: cvar

.. py:data:: o_void

   No Operand.


.. py:data:: o_reg

   General Register (al,ax,es,ds...).

   The register number should be stored in op_t::reg. All processor registers, including special registers, can be represented by this operand type. 
           


.. py:data:: o_mem

   A direct memory reference to a data item. Use this operand type when the address can be calculated statically.
   A direct memory data reference whose target address is known at compilation time. The target virtual address is stored in op_t::addr and the full address is calculated as to_ea(  insn_t::cs, op_t::addr ). For the processors with complex memory organization the final address can be calculated using other segment registers. For flat memories, op_t::addr is the final address and insn_t::cs is usually equal to zero. In any case, the address within the segment should be stored in op_t::addr. 
           


.. py:data:: o_phrase

   An indirect memory reference that uses a register: [reg] There can be several registers but no displacement.
   A memory reference using register contents. Indexed, register based, and other addressing modes can be represented with the operand type. This addressing mode cannot contain immediate values (use o_displ instead). The phrase number should be stored in op_t::phrase. To denote the pre-increment and similar features please use additional operand fields like op_t::specflag... Usually op_t::phrase contains the register number and additional information is stored in op_t::specflags... Please note that this operand type cannot contain immediate values (except the scaling coefficients). 
           


.. py:data:: o_displ

   An indirect memory reference that uses a register and has an immediate constant added to it: [reg+N] There can be several registers.
   A memory reference using register contents with displacement. The displacement should be stored in the op_t::addr field. The rest of information is stored the same way as in o_phrase. 
           


.. py:data:: o_imm

   An immediate Value (constant).

   Any operand consisting of only a number is represented by this operand type. The value should be stored in op_t::value. You may sign extend short (1-2 byte) values. In any case don't forget to specify op_t::dtype (should be set for all operand types). 
           


.. py:data:: o_far

   An immediate far code reference (inter-segment)

   If the current processor has a special addressing mode for inter-segment references, then this operand type should be used instead of o_near. If you want, you may use PR_CHK_XREF in processor_t::flag to disable inter-segment calls if o_near operand type is used. Currently only IBM PC uses this flag. 
           


.. py:data:: o_near

   An immediate near code reference (intra-segment)

   A direct memory code reference whose target address is known at the compilation time. The target virtual address is stored in op_t::addr and the final address is always to_ea( insn_t::cs, op_t::addr). Usually this operand type is used for the branches and calls whose target address is known. If the current processor has 2 different types of references for inter-segment and intra-segment references, then this should be used only for intra-segment references.
   If the above operand types do not cover all possible addressing modes, then use o_idpspec... operand types. 
           


.. py:data:: o_idpspec0

   processor specific type.


.. py:data:: o_idpspec1

   processor specific type.


.. py:data:: o_idpspec2

   processor specific type.


.. py:data:: o_idpspec3

   processor specific type.


.. py:data:: o_idpspec4

   processor specific type.


.. py:data:: o_idpspec5

   processor specific type. (there can be more processor specific types) 
           


.. py:data:: OF_NO_BASE_DISP

   base displacement doesn't exist. meaningful only for o_displ type. if set, base displacement (op_t::addr) doesn't exist. 
           


.. py:data:: OF_OUTER_DISP

   outer displacement exists. meaningful only for o_displ type. if set, outer displacement (op_t::value) exists. 
           


.. py:data:: PACK_FORM_DEF

   packed factor defined. (!o_reg + dt_packreal) 
           


.. py:data:: OF_NUMBER

   the operand can be converted to a number only


.. py:data:: OF_SHOW

   should the operand be displayed?


.. py:data:: dt_byte

   8 bit integer


.. py:data:: dt_word

   16 bit integer


.. py:data:: dt_dword

   32 bit integer


.. py:data:: dt_float

   4 byte floating point


.. py:data:: dt_double

   8 byte floating point


.. py:data:: dt_tbyte

   variable size ( processor_t::tbyte_size) floating point


.. py:data:: dt_packreal

   packed real format for mc68040


.. py:data:: dt_qword

   64 bit integer


.. py:data:: dt_byte16

   128 bit integer


.. py:data:: dt_code

   ptr to code


.. py:data:: dt_void

   none


.. py:data:: dt_fword

   48 bit


.. py:data:: dt_bitfild

   bit field (mc680x0)


.. py:data:: dt_string

   pointer to asciiz string


.. py:data:: dt_unicode

   pointer to unicode string


.. py:data:: dt_ldbl

   long double (which may be different from tbyte)


.. py:data:: dt_byte32

   256 bit integer


.. py:data:: dt_byte64

   512 bit integer


.. py:data:: dt_half

   2-byte floating point


.. py:function:: insn_add_cref(insn: insn_t, to: ida_idaapi.ea_t, opoff: int, type: cref_t) -> None

.. py:function:: insn_add_dref(insn: insn_t, to: ida_idaapi.ea_t, opoff: int, type: dref_t) -> None

.. py:function:: insn_add_off_drefs(insn: insn_t, x: op_t, type: dref_t, outf: int) -> ida_idaapi.ea_t

.. py:function:: insn_create_stkvar(insn: insn_t, x: op_t, v: adiff_t, flags: int) -> bool

.. py:class:: insn_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: cs
      :type:  ida_idaapi.ea_t

      Current segment base paragraph. Initialized by the kernel.



   .. py:attribute:: ip
      :type:  ida_idaapi.ea_t

      Virtual address of the instruction (address within the segment). Initialized by the kernel. 
              



   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      Linear address of the instruction. Initialized by the kernel. 
              



   .. py:attribute:: itype
      :type:  uint16

      Internal code of instruction (only for canonical insns - not user defined!). IDP should define its own instruction codes. These codes are usually defined in ins.hpp. The array of instruction names and features (ins.cpp) is accessed using this code. 
              



   .. py:attribute:: size
      :type:  uint16

      Size of instruction in bytes. The analyzer should put here the actual size of the instruction. 
              



   .. py:attribute:: auxpref
      :type:  int

      processor dependent field



   .. py:attribute:: auxpref_u16
      :type:  uint16 [2]


   .. py:attribute:: auxpref_u8
      :type:  uint8 [4]


   .. py:attribute:: segpref
      :type:  char

      processor dependent field



   .. py:attribute:: insnpref
      :type:  char

      processor dependent field



   .. py:attribute:: flags
      :type:  int16

      Instruction flags



   .. py:attribute:: ops
      :type:  op_t [8]

      array of operands



   .. py:method:: is_macro() -> bool

      Is a macro instruction?



   .. py:method:: is_64bit() -> bool

      Belongs to a 64bit segment?



   .. py:method:: get_next_byte() -> uint8


   .. py:method:: get_next_word() -> uint16


   .. py:method:: get_next_dword() -> int


   .. py:method:: get_next_qword() -> uint64


   .. py:method:: create_op_data(*args) -> bool


   .. py:method:: create_stkvar(x: op_t, v: adiff_t, flags_: int) -> bool


   .. py:method:: add_cref(to: ida_idaapi.ea_t, opoff: int, type: cref_t) -> None

      Add a code cross-reference from the instruction. 
              
      :param to: target linear address
      :param opoff: offset of the operand from the start of instruction. if the offset is unknown, then 0.
      :param type: type of xref



   .. py:method:: add_dref(to: ida_idaapi.ea_t, opoff: int, type: dref_t) -> None

      Add a data cross-reference from the instruction. See add_off_drefs() - usually it can be used in most cases. 
              
      :param to: target linear address
      :param opoff: offset of the operand from the start of instruction if the offset is unknown, then 0
      :param type: type of xref



   .. py:method:: add_off_drefs(x: op_t, type: dref_t, outf: int) -> ida_idaapi.ea_t

      Add xrefs for an operand of the instruction. This function creates all cross references for 'enum', 'offset' and 'structure offset' operands. Use add_off_drefs() in the presence of negative offsets. 
              
      :param x: reference to operand
      :param type: type of xref
      :param outf: out_value() flags. These flags should match the flags used to output the operand
      :returns: if: is_off(): the reference target address (the same as calc_reference_data).
      :returns: if: is_stroff(): BADADDR because for stroffs the target address is unknown
      :returns: otherwise: BADADDR because enums do not represent addresses



   .. py:method:: assign(other: insn_t) -> None


   .. py:method:: is_canon_insn(*args) -> bool

      see processor_t::is_canon_insn()



   .. py:method:: get_canon_feature(*args) -> int

      see instruc_t::feature



   .. py:method:: get_canon_mnem(*args) -> str

      see instruc_t::name



   .. py:attribute:: Op1


   .. py:attribute:: Op2


   .. py:attribute:: Op3


   .. py:attribute:: Op4


   .. py:attribute:: Op5


   .. py:attribute:: Op6


   .. py:attribute:: Op7


   .. py:attribute:: Op8


.. py:data:: INSN_MACRO

   macro instruction


.. py:data:: INSN_MODMAC

   may modify the database to make room for the macro insn


.. py:data:: INSN_64BIT

   belongs to 64bit segment?


.. py:data:: STKVAR_VALID_SIZE

   x.dtype contains correct variable type (for insns like 'lea' this bit must be off). in general, dr_O references do not allow to determine the variable size 
           


.. py:data:: STKVAR_KEEP_EXISTING

   if a stack variable for this operand already exists then we do not create a new variable 
           


.. py:function:: get_lookback() -> int

   Number of instructions to look back. This variable is not used by the kernel. Its value may be specified in ida.cfg: LOOKBACK = <number>. IDP may use it as you like it. (TMS module uses it) 
           


.. py:function:: calc_dataseg(insn: insn_t, n: int = -1, rgnum: int = -1) -> ida_idaapi.ea_t

.. py:function:: map_data_ea(*args) -> ida_idaapi.ea_t

.. py:function:: map_code_ea(*args) -> ida_idaapi.ea_t

.. py:function:: map_ea(*args) -> ida_idaapi.ea_t

.. py:class:: outctx_base_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: insn_ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: outbuf
      :type:  str

      buffer for the current output line once ready, it is moved to lnar 
              



   .. py:attribute:: F32
      :type:  flags_t

      please use outctx_t::F instead



   .. py:attribute:: default_lnnum
      :type:  int

      index of the most important line in lnar



   .. py:method:: only_main_line() -> bool


   .. py:method:: multiline() -> bool


   .. py:method:: force_code() -> bool


   .. py:method:: stack_view() -> bool


   .. py:method:: display_voids() -> bool


   .. py:method:: display_hidden() -> bool


   .. py:method:: set_gen_xrefs(on: bool = True) -> None


   .. py:method:: set_gen_cmt(on: bool = True) -> None


   .. py:method:: clr_gen_label() -> None


   .. py:method:: set_gen_label() -> None


   .. py:method:: set_gen_demangled_label() -> None


   .. py:method:: set_comment_addr(ea: ida_idaapi.ea_t) -> None


   .. py:method:: set_dlbind_opnd() -> None


   .. py:method:: print_label_now() -> bool


   .. py:method:: forbid_annotations() -> int


   .. py:method:: restore_ctxflags(saved_flags: int) -> None


   .. py:method:: out_printf(format: str) -> size_t

      ------------------------------------------------------------------------- Functions to append text to the current output buffer (outbuf) Append a formatted string to the output string. 
              
      :returns: the number of characters appended



   .. py:method:: out_value(x: op_t, outf: int = 0) -> flags64_t

      Output immediate value. Try to use this function to output all constants of instruction operands. This function outputs a number from x.addr or x.value in the form determined by F. It outputs colored text. 
              
      :param x: value to output
      :param outf: Output value flags
      :returns: flags of the output value, otherwise:
      :returns: -1: if printed a number with COLOR_ERROR
      :returns: 0: if printed a nice number or character or segment or enum



   .. py:method:: out_symbol(c: char) -> None

      Output a character with COLOR_SYMBOL color.



   .. py:method:: out_chars(c: char, n: int) -> None

      Append a character multiple times.



   .. py:method:: out_spaces(len: ssize_t) -> None

      Appends spaces to outbuf until its tag_strlen becomes 'len'.



   .. py:method:: out_line(str: outctx_base_t.out_line.str, color: color_t = 0) -> None

      Output a string with the specified color.



   .. py:method:: out_keyword(str: outctx_base_t.out_keyword.str) -> None

      Output a string with COLOR_KEYWORD color.



   .. py:method:: out_register(str: outctx_base_t.out_register.str) -> None

      Output a character with COLOR_REG color.



   .. py:method:: out_lvar(name: str, width: int = -1) -> None

      Output local variable name with COLOR_LOCNAME color.



   .. py:method:: out_tagon(tag: color_t) -> None

      Output "turn color on" escape sequence.



   .. py:method:: out_tagoff(tag: color_t) -> None

      Output "turn color off" escape sequence.



   .. py:method:: out_addr_tag(ea: ida_idaapi.ea_t) -> None

      Output "address" escape sequence.



   .. py:method:: out_colored_register_line(str: outctx_base_t.out_colored_register_line.str) -> None

      Output a colored line with register names in it. The register names will be substituted by user-defined names (regvar_t) Please note that out_tagoff tries to make substitutions too (when called with COLOR_REG) 
              



   .. py:method:: out_char(c: char) -> None

      Output one character. The character is output without color codes. see also out_symbol() 
              



   .. py:method:: out_btoa(Word: int, radix: char = 0) -> None

      Output a number with the specified base (binary, octal, decimal, hex) The number is output without color codes. see also out_long() 
              



   .. py:method:: out_long(v: int, radix: char) -> None

      Output a number with appropriate color. Low level function. Use out_value() if you can. if 'suspop' is set then this function uses COLOR_VOIDOP instead of COLOR_NUMBER. 'suspop' is initialized:
      * in out_one_operand()
      * in ..\ida\gl.cpp (before calling processor_t::d_out())



      :param v: value to output
      :param radix: base (2,8,10,16)



   .. py:method:: out_name_expr(*args) -> bool

      Output a name expression. 
              
      :param x: instruction operand referencing the name expression
      :param ea: address to convert to name expression
      :param off: the value of name expression. this parameter is used only to check that the name expression will have the wanted value. You may pass BADADDR for this parameter but I discourage it because it prohibits checks.
      :returns: true if the name expression has been produced



   .. py:method:: close_comment() -> None


   .. py:method:: flush_outbuf(indent: int = -1) -> bool

      ------------------------------------------------------------------------- Functions to populate the output line array (lnar) Move the contents of the output buffer to the line array (outbuf->lnar) The kernel augments the outbuf contents with additional text like the line prefix, user-defined comments, xrefs, etc at this call. 
              



   .. py:method:: flush_buf(buf: str, indent: int = -1) -> bool

      Append contents of 'buf' to the line array. Behaves like flush_outbuf but accepts an arbitrary buffer 
              



   .. py:method:: term_outctx(prefix: str = None) -> int

      Finalize the output context. 
              
      :returns: the number of generated lines.



   .. py:method:: gen_printf(indent: int, format: str) -> bool

      printf-like function to add lines to the line array. 
              
      :param indent: indention of the line. if indent == -1, the kernel will indent the line at idainfo::indent. if indent < 0, -indent will be used for indention. The first line printed with indent < 0 is considered as the most important line at the current address. Usually it is the line with the instruction itself. This line will be displayed in the cross-reference lists and other places. If you need to output an additional line before the main line then pass DEFAULT_INDENT instead of -1. The kernel will know that your line is not the most important one.
      :param format: printf style colored line to generate
      :returns: overflow, lnar_maxsize has been reached



   .. py:method:: gen_empty_line() -> bool

      Generate empty line. This function does nothing if generation of empty lines is disabled. 
              
      :returns: overflow, lnar_maxsize has been reached



   .. py:method:: gen_border_line(solid: bool = False) -> bool

      Generate thin border line. This function does nothing if generation of border lines is disabled. 
              
      :param solid: generate solid border line (with =), otherwise with -
      :returns: overflow, lnar_maxsize has been reached



   .. py:method:: gen_cmt_line(format: str) -> bool

      Generate one non-indented comment line, colored with COLOR_AUTOCMT. 
              
      :param format: printf() style format line. The resulting comment line should not include comment character (;)
      :returns: overflow, lnar_maxsize has been reached



   .. py:method:: gen_collapsed_line(format: str) -> bool

      Generate one non-indented comment line, colored with COLOR_COLLAPSED. 
              
      :param format: printf() style format line. The resulting comment line should not include comment character (;)
      :returns: overflow, lnar_maxsize has been reached



   .. py:method:: gen_block_cmt(cmt: str, color: color_t) -> bool

      Generate big non-indented comment lines. 
              
      :param cmt: comment text. may contain \n characters to denote new lines. should not contain comment character (;)
      :param color: color of comment text (one of Color tags)
      :returns: overflow, lnar_maxsize has been reached



   .. py:method:: setup_outctx(prefix: str, makeline_flags: int) -> None

      Initialization; normally used only by the kernel.



   .. py:method:: retrieve_cmt() -> ssize_t


   .. py:method:: retrieve_name(arg2: str, arg3: color_t *) -> ssize_t


   .. py:method:: gen_xref_lines() -> bool


   .. py:method:: init_lines_array(answers: qstrvec_t *, maxsize: int) -> None


   .. py:method:: get_stkvar(x: op_t, v: int, vv: sval_t *, is_sp_based: int *, _frame: tinfo_t) -> ssize_t


   .. py:method:: gen_empty_line_without_annotations() -> None


   .. py:method:: getF() -> flags64_t


.. py:data:: CTXF_MAIN

   produce only the essential line(s)


.. py:data:: CTXF_MULTI

   enable multi-line essential lines


.. py:data:: CTXF_CODE

   display as code regardless of the database flags


.. py:data:: CTXF_STACK

   stack view (display undefined items as 2/4/8 bytes)


.. py:data:: CTXF_GEN_XREFS

   generate the xrefs along with the next line


.. py:data:: CTXF_XREF_STATE

   xref state:


.. py:data:: XREFSTATE_NONE

   not generated yet


.. py:data:: XREFSTATE_GO

   being generated


.. py:data:: XREFSTATE_DONE

   have been generated


.. py:data:: CTXF_GEN_CMT

   generate the comment along with the next line


.. py:data:: CTXF_CMT_STATE

   comment state:


.. py:data:: COMMSTATE_NONE

   not generated yet


.. py:data:: COMMSTATE_GO

   being generated


.. py:data:: COMMSTATE_DONE

   have been generated


.. py:data:: CTXF_VOIDS

   display void marks


.. py:data:: CTXF_NORMAL_LABEL

   generate plain label (+demangled label as cmt)


.. py:data:: CTXF_DEMANGLED_LABEL

   generate only demangled label as comment


.. py:data:: CTXF_LABEL_OK

   the label have been generated


.. py:data:: CTXF_DEMANGLED_OK

   the label has been demangled successfully


.. py:data:: CTXF_OVSTORE_PRNT

   out_value should store modified values


.. py:data:: CTXF_OUTCTX_T

   instance is, in fact, a outctx_t


.. py:data:: CTXF_DBLIND_OPND

   an operand was printed with double indirection (e.g. =var in arm)


.. py:data:: CTXF_BINOP_STATE

   opcode bytes state:


.. py:data:: BINOPSTATE_NONE

   not generated yet


.. py:data:: BINOPSTATE_GO

   being generated


.. py:data:: BINOPSTATE_DONE

   have been generated


.. py:data:: CTXF_HIDDEN_ADDR

   generate an hidden addr tag at the beginning of the line


.. py:data:: CTXF_BIT_PREFIX

   generate a line prefix with a bit offset, e.g.: 12345678.3


.. py:data:: CTXF_UNHIDE

   display hidden objects (segment, function, range)


.. py:data:: OOF_SIGNMASK

   sign symbol (+/-) output


.. py:data:: OOFS_IFSIGN

   output sign if needed


.. py:data:: OOFS_NOSIGN

   don't output sign, forbid the user to change the sign


.. py:data:: OOFS_NEEDSIGN

   always out sign (+-)


.. py:data:: OOF_SIGNED

   output as signed if < 0


.. py:data:: OOF_NUMBER

   always as a number


.. py:data:: OOF_WIDTHMASK

   width of value in bits


.. py:data:: OOFW_IMM

   take from x.dtype


.. py:data:: OOFW_8

   8 bit width


.. py:data:: OOFW_16

   16 bit width


.. py:data:: OOFW_24

   24 bit width


.. py:data:: OOFW_32

   32 bit width


.. py:data:: OOFW_64

   64 bit width


.. py:data:: OOF_ADDR

   output x.addr, otherwise x.value OOF_WIDTHMASK must be explicitly specified with it 
           


.. py:data:: OOF_OUTER

   output outer operand


.. py:data:: OOF_ZSTROFF

   meaningful only if is_stroff(F); append a struct field name if the field offset is zero? if AFL_ZSTROFF is set, then this flag is ignored. 
           


.. py:data:: OOF_NOBNOT

   prohibit use of binary not


.. py:data:: OOF_SPACES

   do not suppress leading spaces; currently works only for floating point numbers 
           


.. py:data:: OOF_ANYSERIAL

   if enum: select first available serial


.. py:data:: OOF_LZEROES

   print leading zeroes


.. py:data:: OOF_NO_LZEROES

   do not print leading zeroes; if none of OOF_LZEROES and OOF_NO_LZEROES was specified, is_lzero() is used 
           


.. py:data:: DEFAULT_INDENT

.. py:data:: MAKELINE_NONE

.. py:data:: MAKELINE_BINPREF

   allow display of binary prefix


.. py:data:: MAKELINE_VOID

   allow display of '<suspicious>' marks


.. py:data:: MAKELINE_STACK

   allow display of sp trace prefix


.. py:class:: outctx_t(*args, **kwargs)

   Bases: :py:obj:`outctx_base_t`


   .. py:attribute:: thisown


   .. py:attribute:: bin_ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: bin_state
      :type:  char


   .. py:attribute:: gl_bpsize
      :type:  int


   .. py:attribute:: bin_width
      :type:  int


   .. py:attribute:: insn
      :type:  insn_t


   .. py:attribute:: curlabel
      :type:  str


   .. py:attribute:: wif
      :type:  printop_t const *


   .. py:attribute:: procmod
      :type:  procmod_t *


   .. py:attribute:: ph
      :type:  processor_t &


   .. py:attribute:: ash
      :type:  asm_t &


   .. py:attribute:: saved_immvals
      :type:  uval_t [8]


   .. py:attribute:: prefix_ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: next_line_ea
      :type:  ida_idaapi.ea_t


   .. py:method:: setup_outctx(prefix: str, flags: int) -> None

      Initialization; normally used only by the kernel.



   .. py:method:: term_outctx(prefix: str = None) -> int

      Finalize the output context. 
              
      :returns: the number of generated lines.



   .. py:method:: retrieve_cmt() -> ssize_t


   .. py:method:: retrieve_name(arg2: str, arg3: color_t *) -> ssize_t


   .. py:method:: gen_xref_lines() -> bool


   .. py:method:: out_btoa(Word: int, radix: char = 0) -> None

      Output a number with the specified base (binary, octal, decimal, hex) The number is output without color codes. see also out_long() 
              



   .. py:method:: set_bin_state(value: int) -> None


   .. py:method:: out_mnem(width: int = 8, postfix: str = None) -> None

      Output instruction mnemonic for 'insn' using information in 'ph.instruc' array. This function outputs colored text. It should be called from processor_t::ev_out_insn() or processor_t::ev_out_mnem() handler. It will output at least one space after the instruction. mnemonic even if the specified 'width' is not enough. 
              
      :param width: width of field with mnemonic. if < 0, then 'postfix' will be output before the mnemonic, i.e. as a prefix
      :param postfix: optional postfix added to the instruction mnemonic



   .. py:method:: out_custom_mnem(mnem: str, width: int = 8, postfix: str = None) -> None

      Output custom mnemonic for 'insn'. E.g. if it should differ from the one in 'ph.instruc'. This function outputs colored text. See out_mnem 
              
      :param mnem: custom mnemonic
      :param width: width of field with mnemonic. if < 0, then 'postfix' will be output before the mnemonic, i.e. as a prefix
      :param postfix: optional postfix added to 'mnem'



   .. py:method:: out_mnemonic() -> None

      Output instruction mnemonic using information in 'insn'. It should be called from processor_t::ev_out_insn() and it will call processor_t::ev_out_mnem() or out_mnem. This function outputs colored text. 
              



   .. py:method:: out_one_operand(n: int) -> bool

      Use this function to output an operand of an instruction. This function checks for the existence of a manually defined operand and will output it if it exists. It should be called from processor_t::ev_out_insn() and it will call processor_t::ev_out_operand(). This function outputs colored text. 
              
      :param n: 0..UA_MAXOP-1 operand number
      :returns: 1: operand is displayed
      :returns: 0: operand is hidden



   .. py:method:: out_immchar_cmts() -> None

      Print all operand values as commented character constants. This function is used to comment void operands with their representation in the form of character constants. This function outputs colored text. 
              



   .. py:method:: gen_func_header(pfn: func_t *) -> None


   .. py:method:: gen_func_footer(pfn: func_t const *) -> None


   .. py:method:: out_data(analyze_only: bool) -> None


   .. py:method:: out_specea(segtype: uchar) -> bool


   .. py:method:: gen_header_extra() -> None


   .. py:method:: gen_header(*args) -> None


   .. py:method:: out_fcref_names() -> None

      Print addresses referenced *from* the specified address as commented symbolic names. This function is used to show, for example, multiple callees of an indirect call. This function outputs colored text. 
              



.. py:data:: GH_PRINT_PROC

   processor name


.. py:data:: GH_PRINT_ASM

   selected assembler


.. py:data:: GH_PRINT_BYTESEX

   byte sex


.. py:data:: GH_PRINT_HEADER

   lines from ash.header


.. py:data:: GH_BYTESEX_HAS_HIGHBYTE

   describe inf.is_wide_high_byte_first()


.. py:data:: GH_PRINT_PROC_AND_ASM

.. py:data:: GH_PRINT_PROC_ASM_AND_BYTESEX

.. py:data:: GH_PRINT_ALL

.. py:data:: GH_PRINT_ALL_BUT_BYTESEX

.. py:function:: create_outctx(ea: ida_idaapi.ea_t, F: flags64_t = 0, suspop: int = 0) -> outctx_base_t *

   Create a new output context. To delete it, just use "delete pctx" 
           


.. py:function:: print_insn_mnem(ea: ida_idaapi.ea_t) -> str

   Print instruction mnemonics. 
           
   :param ea: linear address of the instruction
   :returns: success


.. py:data:: FCBF_CONT

   don't stop on decoding, or any other kind of error


.. py:data:: FCBF_ERR_REPL

   in case of an error, use a CP_REPLCHAR instead of a hex representation of the problematic byte 
           


.. py:data:: FCBF_FF_LIT

   in case of codepoints == 0xFF, use it as-is (i.e., LATIN SMALL LETTER Y WITH DIAERESIS). If both this, and FCBF_REPL are specified, this will take precedence 
           


.. py:data:: FCBF_DELIM

   add the 'ash'-specified delimiters around the generated data. Note: if those are not defined and the INFFL_ALLASM is not set, format_charlit() will return an error 
           


.. py:function:: get_dtype_flag(dtype: op_dtype_t) -> flags64_t

   Get flags for op_t::dtype field.


.. py:function:: get_dtype_size(dtype: op_dtype_t) -> size_t

   Get size of opt_::dtype field.


.. py:function:: is_floating_dtype(dtype: op_dtype_t) -> bool

   Is a floating type operand?


.. py:function:: create_insn(ea: ida_idaapi.ea_t, out: insn_t = None) -> int

   Create an instruction at the specified address. This function checks if an instruction is present at the specified address and will try to create one if there is none. It will fail if there is a data item or other items hindering the creation of the new instruction. This function will also fill the 'out' structure. 
           
   :param ea: linear address
   :param out: the resulting instruction
   :returns: the length of the instruction or 0


.. py:function:: decode_insn(out: insn_t, ea: ida_idaapi.ea_t) -> int

   Analyze the specified address and fill 'out'. This function does not modify the database. It just tries to interpret the specified address as an instruction and fills the 'out' structure. 
           
   :param out: the resulting instruction
   :param ea: linear address
   :returns: the length of the (possible) instruction or 0


.. py:function:: can_decode(ea: ida_idaapi.ea_t) -> bool

   Can the bytes at address 'ea' be decoded as instruction? 
           
   :param ea: linear address
   :returns: whether or not the contents at that address could be a valid instruction


.. py:function:: print_operand(ea: ida_idaapi.ea_t, n: int, getn_flags: int = 0, newtype: printop_t = None) -> str

   Generate text representation for operand #n. This function will generate the text representation of the specified operand (includes color codes.) 
           
   :param ea: the item address (instruction or data)
   :param n: 0..UA_MAXOP-1 operand number, meaningful only for instructions
   :param getn_flags: Name expression flags Currently only GETN_NODUMMY is accepted.
   :param newtype: if specified, print the operand using the specified type
   :returns: success


.. py:function:: decode_prev_insn(out: insn_t, ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Decode previous instruction if it exists, fill 'out'. 
           
   :param out: the resulting instruction
   :param ea: the address to decode the previous instruction from
   :returns: the previous instruction address (BADADDR-no such insn)


.. py:class:: macro_constructor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: reserved
      :type:  size_t


   .. py:method:: construct_macro(insn: insn_t, enable: bool) -> bool

      Construct a macro instruction. This function may be called from ana() to generate a macro instruction.
      The real work is done by the 'build_macro()' virtual function. It must be defined by the processor module.
      construct_macro() modifies the database using the info provided by build_macro(). It verifies if the instruction can really be created (for example, that other items do not hinder), may plan to reanalyze the macro, etc. If the macro instructions are disabled by the user, construct_macro() will destroy the macro instruction. Note: if INSN_MODMAC is not set in insn.flags, the database will not be modified.

      :param insn: the instruction to modify into a macro
      :param enable: enable macro generation
      :returns: true: the macro instruction is generated in 'insn'
      :returns: false: did not create a macro



   .. py:method:: build_macro(insn: insn_t, may_go_forward: bool) -> bool

      Try to extend the instruction.
      This function may modify 'insn' and return false; these changes will be accepted by the kernel but the instruction will not be considered as a macro.

      :param insn: Instruction to modify, usually the first instruction of the macro
      :param may_go_forward: Is it ok to consider the next instruction for the macro? This argument may be false, for example, if there is a cross reference to the end of INSN. In this case creating a macro is not desired. However, it may still be useful to perform minor tweaks to the instruction using the information about the surrounding instructions.
      :returns: true if created an macro instruction.



.. py:function:: decode_preceding_insn(out: insn_t, ea: ida_idaapi.ea_t) -> Tuple[ida_idaapi.ea_t, bool]

   Decodes the preceding instruction.

   :param out: instruction storage
   :param ea: current ea
   :returns: tuple(preceeding_ea or BADADDR, farref = Boolean)


.. py:function:: construct_macro(*args)

   See ua.hpp's construct_macro().

   This function has the following signatures

       1. construct_macro(insn: insn_t, enable: bool, build_macro: callable) -> bool
       2. construct_macro(constuctor: macro_constructor_t, insn: insn_t, enable: bool) -> bool

   :param insn: the instruction to build the macro for
   :param enable: enable macro generation
   :param build_macro: a callable with 2 arguments: an insn_t, and
                       whether it is ok to consider the next instruction
                       for the macro
   :param constructor: a macro_constructor_t implementation
   :returns: success


.. py:function:: get_dtype_by_size(size: asize_t) -> int

   Get op_t::dtype from size.


.. py:function:: get_immvals(ea: ida_idaapi.ea_t, n: int, F: flags64_t = 0) -> PyObject *

   Get immediate values at the specified address. This function decodes instruction at the specified address or inspects the data item. It finds immediate values and copies them to 'out'. This function will store the original value of the operands in 'out', unless the last bits of 'F' are "...0 11111111", in which case the transformed values (as needed for printing) will be stored instead. 
           
   :param ea: address to analyze
   :param n: 0..UA_MAXOP-1 operand number, OPND_ALL all the operands
   :param F: flags for the specified address
   :returns: number of immediate values (0..2*UA_MAXOP)


.. py:function:: get_printable_immvals(ea: ida_idaapi.ea_t, n: int, F: flags64_t = 0) -> PyObject *

   Get immediate ready-to-print values at the specified address 
           
   :param ea: address to analyze
   :param n: 0..UA_MAXOP-1 operand number, OPND_ALL all the operands
   :param F: flags for the specified address
   :returns: number of immediate values (0..2*UA_MAXOP)


.. py:function:: insn_t__from_ptrval__(ptrval: size_t) -> insn_t *

.. py:function:: op_t__from_ptrval__(ptrval: size_t) -> op_t *

.. py:function:: outctx_base_t__from_ptrval__(ptrval: size_t) -> outctx_base_t *

.. py:function:: outctx_t__from_ptrval__(ptrval: size_t) -> outctx_t *

.. py:data:: ua_mnem


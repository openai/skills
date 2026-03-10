ida_lines
=========

.. py:module:: ida_lines

.. autoapi-nested-parse::

   High level functions that deal with the generation of the disassembled text lines.

   This file also contains definitions for the syntax highlighting.
   Finally there are functions that deal with anterior/posterior user-defined lines. 
       



Attributes
----------

.. autoapisummary::

   ida_lines.COLOR_ON
   ida_lines.COLOR_OFF
   ida_lines.COLOR_ESC
   ida_lines.COLOR_INV
   ida_lines.SCOLOR_ON
   ida_lines.SCOLOR_OFF
   ida_lines.SCOLOR_ESC
   ida_lines.SCOLOR_INV
   ida_lines.SCOLOR_DEFAULT
   ida_lines.SCOLOR_REGCMT
   ida_lines.SCOLOR_RPTCMT
   ida_lines.SCOLOR_AUTOCMT
   ida_lines.SCOLOR_INSN
   ida_lines.SCOLOR_DATNAME
   ida_lines.SCOLOR_DNAME
   ida_lines.SCOLOR_DEMNAME
   ida_lines.SCOLOR_SYMBOL
   ida_lines.SCOLOR_CHAR
   ida_lines.SCOLOR_STRING
   ida_lines.SCOLOR_NUMBER
   ida_lines.SCOLOR_VOIDOP
   ida_lines.SCOLOR_CREF
   ida_lines.SCOLOR_DREF
   ida_lines.SCOLOR_CREFTAIL
   ida_lines.SCOLOR_DREFTAIL
   ida_lines.SCOLOR_ERROR
   ida_lines.SCOLOR_PREFIX
   ida_lines.SCOLOR_BINPREF
   ida_lines.SCOLOR_EXTRA
   ida_lines.SCOLOR_ALTOP
   ida_lines.SCOLOR_HIDNAME
   ida_lines.SCOLOR_LIBNAME
   ida_lines.SCOLOR_LOCNAME
   ida_lines.SCOLOR_CODNAME
   ida_lines.SCOLOR_ASMDIR
   ida_lines.SCOLOR_MACRO
   ida_lines.SCOLOR_DSTR
   ida_lines.SCOLOR_DCHAR
   ida_lines.SCOLOR_DNUM
   ida_lines.SCOLOR_KEYWORD
   ida_lines.SCOLOR_REG
   ida_lines.SCOLOR_IMPNAME
   ida_lines.SCOLOR_SEGNAME
   ida_lines.SCOLOR_UNKNAME
   ida_lines.SCOLOR_CNAME
   ida_lines.SCOLOR_UNAME
   ida_lines.SCOLOR_COLLAPSED
   ida_lines.SCOLOR_ADDR
   ida_lines.COLOR_SELECTED
   ida_lines.COLOR_LIBFUNC
   ida_lines.COLOR_REGFUNC
   ida_lines.COLOR_CODE
   ida_lines.COLOR_DATA
   ida_lines.COLOR_UNKNOWN
   ida_lines.COLOR_EXTERN
   ida_lines.COLOR_CURITEM
   ida_lines.COLOR_CURLINE
   ida_lines.COLOR_HIDLINE
   ida_lines.COLOR_LUMFUNC
   ida_lines.COLOR_BG_MAX
   ida_lines.cvar
   ida_lines.COLOR_DEFAULT
   ida_lines.COLOR_REGCMT
   ida_lines.COLOR_RPTCMT
   ida_lines.COLOR_AUTOCMT
   ida_lines.COLOR_INSN
   ida_lines.COLOR_DATNAME
   ida_lines.COLOR_DNAME
   ida_lines.COLOR_DEMNAME
   ida_lines.COLOR_SYMBOL
   ida_lines.COLOR_CHAR
   ida_lines.COLOR_STRING
   ida_lines.COLOR_NUMBER
   ida_lines.COLOR_VOIDOP
   ida_lines.COLOR_CREF
   ida_lines.COLOR_DREF
   ida_lines.COLOR_CREFTAIL
   ida_lines.COLOR_DREFTAIL
   ida_lines.COLOR_ERROR
   ida_lines.COLOR_PREFIX
   ida_lines.COLOR_BINPREF
   ida_lines.COLOR_EXTRA
   ida_lines.COLOR_ALTOP
   ida_lines.COLOR_HIDNAME
   ida_lines.COLOR_LIBNAME
   ida_lines.COLOR_LOCNAME
   ida_lines.COLOR_CODNAME
   ida_lines.COLOR_ASMDIR
   ida_lines.COLOR_MACRO
   ida_lines.COLOR_DSTR
   ida_lines.COLOR_DCHAR
   ida_lines.COLOR_DNUM
   ida_lines.COLOR_KEYWORD
   ida_lines.COLOR_REG
   ida_lines.COLOR_IMPNAME
   ida_lines.COLOR_SEGNAME
   ida_lines.COLOR_UNKNAME
   ida_lines.COLOR_CNAME
   ida_lines.COLOR_UNAME
   ida_lines.COLOR_COLLAPSED
   ida_lines.COLOR_FG_MAX
   ida_lines.COLOR_ADDR
   ida_lines.COLOR_OPND1
   ida_lines.COLOR_OPND2
   ida_lines.COLOR_OPND3
   ida_lines.COLOR_OPND4
   ida_lines.COLOR_OPND5
   ida_lines.COLOR_OPND6
   ida_lines.COLOR_OPND7
   ida_lines.COLOR_OPND8
   ida_lines.COLOR_RESERVED1
   ida_lines.COLOR_LUMINA
   ida_lines.VEL_POST
   ida_lines.VEL_CMT
   ida_lines.GDISMF_AS_STACK
   ida_lines.GDISMF_ADDR_TAG
   ida_lines.GDISMF_REMOVE_TAGS
   ida_lines.GDISMF_UNHIDE
   ida_lines.GENDSM_FORCE_CODE
   ida_lines.GENDSM_MULTI_LINE
   ida_lines.GENDSM_REMOVE_TAGS
   ida_lines.GENDSM_UNHIDE
   ida_lines.COLOR_ADDR_SIZE
   ida_lines.SCOLOR_FG_MAX
   ida_lines.cvar
   ida_lines.SCOLOR_OPND1
   ida_lines.SCOLOR_OPND2
   ida_lines.SCOLOR_OPND3
   ida_lines.SCOLOR_OPND4
   ida_lines.SCOLOR_OPND5
   ida_lines.SCOLOR_OPND6
   ida_lines.SCOLOR_UTF8
   ida_lines.PALETTE_SIZE
   ida_lines.E_PREV
   ida_lines.E_NEXT


Classes
-------

.. autoapisummary::

   ida_lines.user_defined_prefix_t


Functions
---------

.. autoapisummary::

   ida_lines.tag_strlen
   ida_lines.calc_prefix_color
   ida_lines.calc_bg_color
   ida_lines.add_sourcefile
   ida_lines.get_sourcefile
   ida_lines.del_sourcefile
   ida_lines.install_user_defined_prefix
   ida_lines.add_extra_line
   ida_lines.add_extra_cmt
   ida_lines.add_pgm_cmt
   ida_lines.generate_disasm_line
   ida_lines.get_first_free_extra_cmtidx
   ida_lines.update_extra_cmt
   ida_lines.del_extra_cmt
   ida_lines.get_extra_cmt
   ida_lines.delete_extra_cmts
   ida_lines.create_encoding_helper
   ida_lines.tag_remove
   ida_lines.tag_addr
   ida_lines.tag_skipcode
   ida_lines.tag_skipcodes
   ida_lines.tag_advance
   ida_lines.generate_disassembly
   ida_lines.requires_color_esc
   ida_lines.COLSTR


Module Contents
---------------

.. py:data:: COLOR_ON

   Escape character (ON). Followed by a color code (color_t). 
           


.. py:data:: COLOR_OFF

   Escape character (OFF). Followed by a color code (color_t). 
           


.. py:data:: COLOR_ESC

   Escape character (Quote next character). This is needed to output '\1' and '\2' characters. 
           


.. py:data:: COLOR_INV

   Escape character (Inverse foreground and background colors). This escape character has no corresponding COLOR_OFF. Its action continues until the next COLOR_INV or end of line. 
           


.. py:data:: SCOLOR_ON

   Escape character (ON)


.. py:data:: SCOLOR_OFF

   Escape character (OFF)


.. py:data:: SCOLOR_ESC

   Escape character (Quote next character)


.. py:data:: SCOLOR_INV

   Escape character (Inverse colors)


.. py:data:: SCOLOR_DEFAULT

   Default.


.. py:data:: SCOLOR_REGCMT

   Regular comment.


.. py:data:: SCOLOR_RPTCMT

   Repeatable comment (defined not here)


.. py:data:: SCOLOR_AUTOCMT

   Automatic comment.


.. py:data:: SCOLOR_INSN

   Instruction.


.. py:data:: SCOLOR_DATNAME

   Dummy Data Name.


.. py:data:: SCOLOR_DNAME

   Regular Data Name.


.. py:data:: SCOLOR_DEMNAME

   Demangled Name.


.. py:data:: SCOLOR_SYMBOL

   Punctuation.


.. py:data:: SCOLOR_CHAR

   Char constant in instruction.


.. py:data:: SCOLOR_STRING

   String constant in instruction.


.. py:data:: SCOLOR_NUMBER

   Numeric constant in instruction.


.. py:data:: SCOLOR_VOIDOP

   Void operand.


.. py:data:: SCOLOR_CREF

   Code reference.


.. py:data:: SCOLOR_DREF

   Data reference.


.. py:data:: SCOLOR_CREFTAIL

   Code reference to tail byte.


.. py:data:: SCOLOR_DREFTAIL

   Data reference to tail byte.


.. py:data:: SCOLOR_ERROR

   Error or problem.


.. py:data:: SCOLOR_PREFIX

   Line prefix.


.. py:data:: SCOLOR_BINPREF

   Binary line prefix bytes.


.. py:data:: SCOLOR_EXTRA

   Extra line.


.. py:data:: SCOLOR_ALTOP

   Alternative operand.


.. py:data:: SCOLOR_HIDNAME

   Hidden name.


.. py:data:: SCOLOR_LIBNAME

   Library function name.


.. py:data:: SCOLOR_LOCNAME

   Local variable name.


.. py:data:: SCOLOR_CODNAME

   Dummy code name.


.. py:data:: SCOLOR_ASMDIR

   Assembler directive.


.. py:data:: SCOLOR_MACRO

   Macro.


.. py:data:: SCOLOR_DSTR

   String constant in data directive.


.. py:data:: SCOLOR_DCHAR

   Char constant in data directive.


.. py:data:: SCOLOR_DNUM

   Numeric constant in data directive.


.. py:data:: SCOLOR_KEYWORD

   Keywords.


.. py:data:: SCOLOR_REG

   Register name.


.. py:data:: SCOLOR_IMPNAME

   Imported name.


.. py:data:: SCOLOR_SEGNAME

   Segment name.


.. py:data:: SCOLOR_UNKNAME

   Dummy unknown name.


.. py:data:: SCOLOR_CNAME

   Regular code name.


.. py:data:: SCOLOR_UNAME

   Regular unknown name.


.. py:data:: SCOLOR_COLLAPSED

   Collapsed line.


.. py:data:: SCOLOR_ADDR

   Hidden address mark.


.. py:data:: COLOR_SELECTED

   Selected.


.. py:data:: COLOR_LIBFUNC

   Library function.


.. py:data:: COLOR_REGFUNC

   Regular function.


.. py:data:: COLOR_CODE

   Single instruction.


.. py:data:: COLOR_DATA

   Data bytes.


.. py:data:: COLOR_UNKNOWN

   Unexplored byte.


.. py:data:: COLOR_EXTERN

   External name definition segment.


.. py:data:: COLOR_CURITEM

   Current item.


.. py:data:: COLOR_CURLINE

   Current line.


.. py:data:: COLOR_HIDLINE

   Hidden line.


.. py:data:: COLOR_LUMFUNC

   Lumina function.


.. py:data:: COLOR_BG_MAX

   Max color number.


.. py:function:: tag_strlen(line: str) -> ssize_t

   Calculate length of a colored string This function computes the length in unicode codepoints of a line 
           
   :returns: the number of codepoints in the line, or -1 on error


.. py:function:: calc_prefix_color(ea: ida_idaapi.ea_t) -> color_t

   Get prefix color for line at 'ea' 
           
   :returns: Line prefix colors


.. py:function:: calc_bg_color(ea: ida_idaapi.ea_t) -> bgcolor_t

   Get background color for line at 'ea' 
           
   :returns: RGB color


.. py:function:: add_sourcefile(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, filename: str) -> bool

.. py:function:: get_sourcefile(ea: ida_idaapi.ea_t, bounds: range_t = None) -> str

.. py:function:: del_sourcefile(ea: ida_idaapi.ea_t) -> bool

.. py:function:: install_user_defined_prefix(*args) -> bool

.. py:class:: user_defined_prefix_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: get_user_defined_prefix(ea: ida_idaapi.ea_t, insn: insn_t const &, lnnum: int, indent: int, line: str) -> None

      This callback must be overridden by the derived class. 
              
      :param ea: the current address
      :param insn: the current instruction. if the current item is not an instruction, then insn.itype is zero.
      :param lnnum: number of the current line (each address may have several listing lines for it). 0 means the very first line for the current address.
      :param indent: see explanations for gen_printf()
      :param line: the line to be generated. the line usually contains color tags. this argument can be examined to decide whether to generate the prefix.



.. py:data:: cvar

.. py:data:: COLOR_DEFAULT

   Default.


.. py:data:: COLOR_REGCMT

   Regular comment.


.. py:data:: COLOR_RPTCMT

   Repeatable comment (comment defined somewhere else)


.. py:data:: COLOR_AUTOCMT

   Automatic comment.


.. py:data:: COLOR_INSN

   Instruction.


.. py:data:: COLOR_DATNAME

   Dummy Data Name.


.. py:data:: COLOR_DNAME

   Regular Data Name.


.. py:data:: COLOR_DEMNAME

   Demangled Name.


.. py:data:: COLOR_SYMBOL

   Punctuation.


.. py:data:: COLOR_CHAR

   Char constant in instruction.


.. py:data:: COLOR_STRING

   String constant in instruction.


.. py:data:: COLOR_NUMBER

   Numeric constant in instruction.


.. py:data:: COLOR_VOIDOP

   Void operand.


.. py:data:: COLOR_CREF

   Code reference.


.. py:data:: COLOR_DREF

   Data reference.


.. py:data:: COLOR_CREFTAIL

   Code reference to tail byte.


.. py:data:: COLOR_DREFTAIL

   Data reference to tail byte.


.. py:data:: COLOR_ERROR

   Error or problem.


.. py:data:: COLOR_PREFIX

   Line prefix.


.. py:data:: COLOR_BINPREF

   Binary line prefix bytes.


.. py:data:: COLOR_EXTRA

   Extra line.


.. py:data:: COLOR_ALTOP

   Alternative operand.


.. py:data:: COLOR_HIDNAME

   Hidden name.


.. py:data:: COLOR_LIBNAME

   Library function name.


.. py:data:: COLOR_LOCNAME

   Local variable name.


.. py:data:: COLOR_CODNAME

   Dummy code name.


.. py:data:: COLOR_ASMDIR

   Assembler directive.


.. py:data:: COLOR_MACRO

   Macro.


.. py:data:: COLOR_DSTR

   String constant in data directive.


.. py:data:: COLOR_DCHAR

   Char constant in data directive.


.. py:data:: COLOR_DNUM

   Numeric constant in data directive.


.. py:data:: COLOR_KEYWORD

   Keywords.


.. py:data:: COLOR_REG

   Register name.


.. py:data:: COLOR_IMPNAME

   Imported name.


.. py:data:: COLOR_SEGNAME

   Segment name.


.. py:data:: COLOR_UNKNAME

   Dummy unknown name.


.. py:data:: COLOR_CNAME

   Regular code name.


.. py:data:: COLOR_UNAME

   Regular unknown name.


.. py:data:: COLOR_COLLAPSED

   Collapsed line.


.. py:data:: COLOR_FG_MAX

   Max color number.


.. py:data:: COLOR_ADDR

   Hidden address marks. the address is represented as 16-digit hex number: 01234567ABCDEF00. it doesn't have the COLOR_OFF pair. 
           


.. py:data:: COLOR_OPND1

   Instruction operand 1.


.. py:data:: COLOR_OPND2

   Instruction operand 2.


.. py:data:: COLOR_OPND3

   Instruction operand 3.


.. py:data:: COLOR_OPND4

   Instruction operand 4.


.. py:data:: COLOR_OPND5

   Instruction operand 5.


.. py:data:: COLOR_OPND6

   Instruction operand 6.


.. py:data:: COLOR_OPND7

   Instruction operand 7.


.. py:data:: COLOR_OPND8

   Instruction operand 8.


.. py:data:: COLOR_RESERVED1

   This tag is reserved for internal IDA use.


.. py:data:: COLOR_LUMINA

   Lumina-related, only for the navigation band.


.. py:data:: VEL_POST

   append posterior line


.. py:data:: VEL_CMT

   append comment line


.. py:function:: add_extra_line(*args) -> bool

.. py:function:: add_extra_cmt(*args) -> bool

.. py:function:: add_pgm_cmt(*args) -> bool

.. py:data:: GDISMF_AS_STACK

.. py:data:: GDISMF_ADDR_TAG

.. py:data:: GDISMF_REMOVE_TAGS

.. py:data:: GDISMF_UNHIDE

.. py:function:: generate_disasm_line(ea: ida_idaapi.ea_t, flags: int = 0) -> str

.. py:data:: GENDSM_FORCE_CODE

.. py:data:: GENDSM_MULTI_LINE

.. py:data:: GENDSM_REMOVE_TAGS

.. py:data:: GENDSM_UNHIDE

.. py:function:: get_first_free_extra_cmtidx(ea: ida_idaapi.ea_t, start: int) -> int

.. py:function:: update_extra_cmt(ea: ida_idaapi.ea_t, what: int, str: update_extra_cmt.str) -> bool

.. py:function:: del_extra_cmt(ea: ida_idaapi.ea_t, what: int) -> bool

.. py:function:: get_extra_cmt(ea: ida_idaapi.ea_t, what: int) -> int

.. py:function:: delete_extra_cmts(ea: ida_idaapi.ea_t, what: int) -> None

.. py:function:: create_encoding_helper(*args) -> encoder_t *

.. py:function:: tag_remove(nonnul_instr: str) -> str

   Remove color escape sequences from a string. 
           
   :returns: length of resulting string, -1 if error


.. py:function:: tag_addr(ea: ida_idaapi.ea_t) -> str

   Insert an address mark into a string. 
           
   :param ea: address to include


.. py:function:: tag_skipcode(line: str) -> int

   Skip one color code. This function should be used if you are interested in color codes and want to analyze all of them. Otherwise tag_skipcodes() function is better since it will skip all colors at once. This function will skip the current color code if there is one. If the current symbol is not a color code, it will return the input. 
           
   :returns: moved pointer


.. py:function:: tag_skipcodes(line: str) -> int

   Move the pointer past all color codes. 
           
   :param line: can't be nullptr
   :returns: moved pointer, can't be nullptr


.. py:function:: tag_advance(line: str, cnt: int) -> int

   Move pointer to a 'line' to 'cnt' positions right. Take into account escape sequences. 
           
   :param line: pointer to string
   :param cnt: number of positions to move right
   :returns: moved pointer


.. py:function:: generate_disassembly(ea, max_lines, as_stack, notag, include_hidden: Boolean = False)

   Generate disassembly lines (many lines) and put them into a buffer

   :param ea: address to generate disassembly for
   :param max_lines: how many lines max to generate
   :param as_stack: Display undefined items as 2/4/8 bytes
   :param notag: remove color tags
   :param include_hidden: automatically unhide hidden objects
   :returns: tuple(most_important_line_number, list(lines)) : Returns a tuple containing
             the most important line number and a list of generated lines
   :returns: None on failure


.. py:data:: COLOR_ADDR_SIZE
   :value: 16


   Size of a tagged address (see COLOR_ADDR)


.. py:data:: SCOLOR_FG_MAX
   :value: '('


.. py:data:: cvar

.. py:data:: SCOLOR_OPND1

.. py:data:: SCOLOR_OPND2

.. py:data:: SCOLOR_OPND3

.. py:data:: SCOLOR_OPND4

.. py:data:: SCOLOR_OPND5

.. py:data:: SCOLOR_OPND6

.. py:data:: SCOLOR_UTF8

.. py:data:: PALETTE_SIZE

.. py:function:: requires_color_esc(c)

   Is the given char a color escape character?


.. py:function:: COLSTR(str, tag)

   Utility function to create a colored line
   :param str: The string
   :param tag: Color tag constant. One of SCOLOR_XXXX


.. py:data:: E_PREV

.. py:data:: E_NEXT


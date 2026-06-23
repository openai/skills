ida_name
========

.. py:module:: ida_name

.. autoapi-nested-parse::

   Functions that deal with names.

   A non-tail address of the program may have a name. Tail addresses (i.e. the addresses in the middle of an instruction or data item) cannot have names. 

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For name and symbol operations, see :mod:`ida_domain.names`.



Attributes
----------

.. autoapisummary::

   ida_name.MAXNAMELEN
   ida_name.FUNC_IMPORT_PREFIX
   ida_name.SN_CHECK
   ida_name.SN_NOCHECK
   ida_name.SN_PUBLIC
   ida_name.SN_NON_PUBLIC
   ida_name.SN_WEAK
   ida_name.SN_NON_WEAK
   ida_name.SN_AUTO
   ida_name.SN_NON_AUTO
   ida_name.SN_NOLIST
   ida_name.SN_NOWARN
   ida_name.SN_LOCAL
   ida_name.SN_IDBENC
   ida_name.SN_FORCE
   ida_name.SN_NODUMMY
   ida_name.SN_DELTAIL
   ida_name.SN_MULTI
   ida_name.SN_MULTI_FORCE
   ida_name.UCDR_STRLIT
   ida_name.UCDR_NAME
   ida_name.UCDR_MANGLED
   ida_name.UCDR_TYPE
   ida_name.VNT_IDENT
   ida_name.VNT_TYPE
   ida_name.VNT_UDTMEM
   ida_name.VNT_STRLIT
   ida_name.VNT_VISIBLE
   ida_name.NT_NONE
   ida_name.NT_BYTE
   ida_name.NT_LOCAL
   ida_name.NT_STKVAR
   ida_name.NT_ENUM
   ida_name.NT_ABS
   ida_name.NT_SEG
   ida_name.NT_STROFF
   ida_name.NT_BMASK
   ida_name.NT_REGVAR
   ida_name.GN_VISIBLE
   ida_name.GN_COLORED
   ida_name.GN_DEMANGLED
   ida_name.GN_STRICT
   ida_name.GN_SHORT
   ida_name.GN_LONG
   ida_name.GN_LOCAL
   ida_name.GN_ISRET
   ida_name.GN_NOT_ISRET
   ida_name.GN_NOT_DUMMY
   ida_name.GETN_APPZERO
   ida_name.GETN_NOFIXUP
   ida_name.GETN_NODUMMY
   ida_name.GNCN_NOSEG
   ida_name.GNCN_NOCOLOR
   ida_name.GNCN_NOLABEL
   ida_name.GNCN_NOFUNC
   ida_name.GNCN_SEG_FUNC
   ida_name.GNCN_SEGNUM
   ida_name.GNCN_REQFUNC
   ida_name.GNCN_REQNAME
   ida_name.GNCN_NODBGNM
   ida_name.GNCN_PREFDBG
   ida_name.DEBNAME_EXACT
   ida_name.DEBNAME_LOWER
   ida_name.DEBNAME_UPPER
   ida_name.DEBNAME_NICE
   ida_name.DQT_NPURGED_8
   ida_name.DQT_NPURGED_4
   ida_name.DQT_NPURGED_2
   ida_name.DQT_COMPILER
   ida_name.DQT_NAME_TYPE
   ida_name.DQT_FULL
   ida_name.CN_KEEP_TRAILING_DIGITS
   ida_name.CN_KEEP_UNDERSCORES
   ida_name.ME_INTERR
   ida_name.ME_PARAMERR
   ida_name.ME_ILLSTR
   ida_name.ME_SMALLANS
   ida_name.ME_FRAME
   ida_name.ME_NOCOMP
   ida_name.ME_ERRAUTO
   ida_name.ME_NOHASHMEM
   ida_name.ME_NOSTRMEM
   ida_name.ME_NOERROR_LIMIT
   ida_name.M_PRCMSK
   ida_name.MT_DEFAULT
   ida_name.MT_CDECL
   ida_name.MT_PASCAL
   ida_name.MT_STDCALL
   ida_name.MT_FASTCALL
   ida_name.MT_THISCALL
   ida_name.MT_FORTRAN
   ida_name.MT_SYSCALL
   ida_name.MT_INTERRUPT
   ida_name.MT_MSFASTCALL
   ida_name.MT_CLRCALL
   ida_name.MT_DMDCALL
   ida_name.MT_VECTORCALL
   ida_name.MT_REGCALL
   ida_name.MT_LOCALNAME
   ida_name.M_SAVEREGS
   ida_name.M_CLASS
   ida_name.MT_PUBLIC
   ida_name.MT_PRIVATE
   ida_name.MT_PROTECT
   ida_name.MT_MEMBER
   ida_name.MT_VTABLE
   ida_name.MT_RTTI
   ida_name.M_PARMSK
   ida_name.MT_PARSHF
   ida_name.MT_PARMAX
   ida_name.M_ELLIPSIS
   ida_name.MT_VOIDARG
   ida_name.M_STATIC
   ida_name.M_VIRTUAL
   ida_name.M_AUTOCRT
   ida_name.M_TYPMASK
   ida_name.MT_OPERAT
   ida_name.MT_CONSTR
   ida_name.MT_DESTR
   ida_name.MT_CASTING
   ida_name.MT_CLRCDTOR
   ida_name.M_TRUNCATE
   ida_name.M_THUNK
   ida_name.M_ANONNSP
   ida_name.M_TMPLNAM
   ida_name.M_DBGNAME
   ida_name.M_COMPILER
   ida_name.MT_MSCOMP
   ida_name.MT_BORLAN
   ida_name.MT_WATCOM
   ida_name.MT_OTHER
   ida_name.MT_GNU
   ida_name.MT_GCC3
   ida_name.MT_VISAGE
   ida_name.MNG_PTRMSK
   ida_name.MNG_DEFNEAR
   ida_name.MNG_DEFNEARANY
   ida_name.MNG_DEFFAR
   ida_name.MNG_NOPTRTYP16
   ida_name.MNG_DEFHUGE
   ida_name.MNG_DEFPTR64
   ida_name.MNG_DEFNONE
   ida_name.MNG_NOPTRTYP
   ida_name.MNG_NODEFINIT
   ida_name.MNG_NOUNDERSCORE
   ida_name.MNG_NOTYPE
   ida_name.MNG_NORETTYPE
   ida_name.MNG_NOBASEDT
   ida_name.MNG_NOCALLC
   ida_name.MNG_NOPOSTFC
   ida_name.MNG_NOSCTYP
   ida_name.MNG_NOTHROW
   ida_name.MNG_NOSTVIR
   ida_name.MNG_NOECSU
   ida_name.MNG_NOCSVOL
   ida_name.MNG_NOCLOSUR
   ida_name.MNG_NOUNALG
   ida_name.MNG_NOMANAGE
   ida_name.MNG_NOMODULE
   ida_name.MNG_SHORT_S
   ida_name.MNG_SHORT_U
   ida_name.MNG_ZPT_SPACE
   ida_name.MNG_DROP_IMP
   ida_name.MNG_IGN_ANYWAY
   ida_name.MNG_IGN_JMP
   ida_name.MNG_MOVE_JMP
   ida_name.MNG_COMPILER_MSK
   ida_name.MNG_SHORT_FORM
   ida_name.MNG_LONG_FORM
   ida_name.MNG_CALC_VALID
   ida_name.cvar
   ida_name.ignore_none
   ida_name.ignore_regvar
   ida_name.ignore_llabel
   ida_name.ignore_stkvar
   ida_name.ignore_glabel
   ida_name.MANGLED_CODE
   ida_name.MANGLED_DATA
   ida_name.MANGLED_UNKNOWN


Classes
-------

.. autoapisummary::

   ida_name.ea_name_vec_t
   ida_name.ea_name_t
   ida_name.NearestName


Functions
---------

.. autoapisummary::

   ida_name.get_name
   ida_name.get_colored_name
   ida_name.set_name
   ida_name.force_name
   ida_name.del_global_name
   ida_name.del_local_name
   ida_name.set_dummy_name
   ida_name.make_name_auto
   ida_name.make_name_user
   ida_name.is_valid_cp
   ida_name.set_cp_validity
   ida_name.get_cp_validity
   ida_name.is_ident_cp
   ida_name.is_strlit_cp
   ida_name.is_visible_cp
   ida_name.is_ident
   ida_name.is_uname
   ida_name.is_valid_typename
   ida_name.extract_name
   ida_name.hide_name
   ida_name.show_name
   ida_name.get_name_ea
   ida_name.get_name_base_ea
   ida_name.get_name_value
   ida_name.get_visible_name
   ida_name.get_short_name
   ida_name.get_long_name
   ida_name.get_colored_short_name
   ida_name.get_colored_long_name
   ida_name.get_demangled_name
   ida_name.get_colored_demangled_name
   ida_name.get_name_color
   ida_name.get_name_expr
   ida_name.get_nice_colored_name
   ida_name.append_struct_fields
   ida_name.is_public_name
   ida_name.make_name_public
   ida_name.make_name_non_public
   ida_name.is_weak_name
   ida_name.make_name_weak
   ida_name.make_name_non_weak
   ida_name.get_nlist_size
   ida_name.get_nlist_idx
   ida_name.is_in_nlist
   ida_name.get_nlist_ea
   ida_name.get_nlist_name
   ida_name.rebuild_nlist
   ida_name.reorder_dummy_names
   ida_name.set_debug_name
   ida_name.get_debug_name
   ida_name.del_debug_names
   ida_name.get_debug_name_ea
   ida_name.demangle_name
   ida_name.is_name_defined_locally
   ida_name.cleanup_name
   ida_name.get_mangled_name_type
   ida_name.get_debug_names
   ida_name.get_ea_name
   ida_name.validate_name
   ida_name.calc_gtn_flags


Module Contents
---------------

.. py:class:: ea_name_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> ea_name_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> ea_name_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: ea_name_vec_t) -> None


   .. py:method:: extract() -> ea_name_t *


   .. py:method:: inject(s: ea_name_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< ea_name_t >::const_iterator


   .. py:method:: end(*args) -> qvector< ea_name_t >::const_iterator


   .. py:method:: insert(it: ea_name_t, x: ea_name_t) -> qvector< ea_name_t >::iterator


   .. py:method:: erase(*args) -> qvector< ea_name_t >::iterator


   .. py:method:: append(x: ea_name_t) -> None


   .. py:method:: extend(x: ea_name_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:function:: get_name(ea: ida_idaapi.ea_t) -> str

.. py:function:: get_colored_name(ea: ida_idaapi.ea_t) -> str

.. py:data:: MAXNAMELEN

   Maximum length of a name in IDA (with the trailing zero)


.. py:data:: FUNC_IMPORT_PREFIX

   Name prefix used by IDA for the imported functions.


.. py:function:: set_name(ea: ida_idaapi.ea_t, name: str, flags: int = 0) -> bool

   Set or delete name of an item at the specified address. An item can be anything: instruction, function, data byte, word, string, structure, etc... Include name into the list of names. 
           
   :param ea: linear address. do nothing if ea is not valid (return 0). tail bytes can't have names.
   :param name: new name.
   * nullptr: do nothing (return 0).
   * "" : delete name.
   * otherwise this is a new name.
   :param flags: Set name flags. If a bit is not specified, then the corresponding action is not performed and the name will retain the same bits as before calling this function. For new names, default is: non-public, non-weak, non-auto.
   :returns: 1: ok, name is changed
   :returns: 0: failure, a warning is displayed


.. py:data:: SN_CHECK

   Fail if the name contains invalid characters.


.. py:data:: SN_NOCHECK

   Replace invalid characters silently. If this bit is set, all invalid chars (not in NameChars or MangleChars) will be replaced by '_' List of valid characters is defined in ida.cfg 
           


.. py:data:: SN_PUBLIC

   if set, make name public


.. py:data:: SN_NON_PUBLIC

   if set, make name non-public


.. py:data:: SN_WEAK

   if set, make name weak


.. py:data:: SN_NON_WEAK

   if set, make name non-weak


.. py:data:: SN_AUTO

   if set, make name autogenerated


.. py:data:: SN_NON_AUTO

   if set, make name non-autogenerated


.. py:data:: SN_NOLIST

   if set, exclude name from the list. if not set, then include the name into the list (however, if other bits are set, the name might be immediately excluded from the list). 
           


.. py:data:: SN_NOWARN

   don't display a warning if failed


.. py:data:: SN_LOCAL

   create local name. a function should exist. local names can't be public or weak. also they are not included into the list of names they can't have dummy prefixes. 
           


.. py:data:: SN_IDBENC

   the name is given in the IDB encoding; non-ASCII bytes will be decoded accordingly. Specifying SN_IDBENC also implies SN_NODUMMY 
           


.. py:data:: SN_FORCE

   if the specified name is already present in the database, try variations with a numerical suffix like "_123" 
           


.. py:data:: SN_NODUMMY

   automatically prepend the name with '_' if it begins with a dummy suffix such as 'sub_'. See also SN_IDBENC 
           


.. py:data:: SN_DELTAIL

   if name cannot be set because of a tail byte, delete the hindering item 
           


.. py:data:: SN_MULTI

   if the specified address already has a name, then add the new name as a regular comment "Alternative name is ...". Except when the new name is public and the old one is not or when the old name is weak and the new one is not. In these cases we act as if bit SN_MULTI_FORCE is specified. If the new name only slightly differs from the old one, for example, only by the initial underscore or the artificial suffix '_##', then we ignore it. 
           


.. py:data:: SN_MULTI_FORCE

   if the specified address already has a name, put this old name into a regular comment and set the specified name. This bit may be used only with SN_MULTI. 
           


.. py:function:: force_name(ea: ida_idaapi.ea_t, name: str, flags: int = 0) -> bool

.. py:function:: del_global_name(ea: ida_idaapi.ea_t) -> bool

.. py:function:: del_local_name(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_dummy_name(_from: ida_idaapi.ea_t, ea: ida_idaapi.ea_t) -> bool

   Give an autogenerated (dummy) name. Autogenerated names have special prefixes (loc_...). 
           
   :param ea: linear address
   :returns: 1: ok, dummy name is generated or the byte already had a name
   :returns: 0: failure, invalid address or tail byte


.. py:function:: make_name_auto(ea: ida_idaapi.ea_t) -> bool

.. py:function:: make_name_user(ea: ida_idaapi.ea_t) -> bool

.. py:data:: UCDR_STRLIT

   string literals


.. py:data:: UCDR_NAME

   regular (unmangled) names


.. py:data:: UCDR_MANGLED

   mangled names


.. py:data:: UCDR_TYPE

   type names


.. py:data:: VNT_IDENT

   identifier (e.g., function name)


.. py:data:: VNT_TYPE

   type name (can contain '<', '>', ...)


.. py:data:: VNT_UDTMEM

   UDT (structure, union, enum) member.


.. py:data:: VNT_STRLIT

   string literal


.. py:data:: VNT_VISIBLE

   visible cp (obsolete; will be deleted)


.. py:function:: is_valid_cp(cp: wchar32_t, kind: nametype_t, data: void * = None) -> bool

   Is the given codepoint acceptable in the given context?


.. py:function:: set_cp_validity(*args) -> None

   Mark the given codepoint (or range) as acceptable or unacceptable in the given context If 'endcp' is not BADCP, it is considered to be the end of the range: [cp, endcp), and is not included in the range 
           


.. py:function:: get_cp_validity(*args) -> bool

   Is the given codepoint (or range) acceptable in the given context? If 'endcp' is not BADCP, it is considered to be the end of the range: [cp, endcp), and is not included in the range 
           


.. py:function:: is_ident_cp(cp: wchar32_t) -> bool

   Can a character appear in a name? (present in ::NameChars or ::MangleChars)


.. py:function:: is_strlit_cp(cp: wchar32_t, specific_ranges: rangeset_crefvec_t const * = None) -> bool

   Can a character appear in a string literal (present in ::StrlitChars) If 'specific_ranges' are specified, those will be used instead of the ones corresponding to the current culture (only if ::StrlitChars is configured to use the current culture) 
           


.. py:function:: is_visible_cp(cp: wchar32_t) -> bool

   Can a character be displayed in a name? (present in ::NameChars)


.. py:function:: is_ident(name: str) -> bool

   Is a valid name? (including ::MangleChars)


.. py:function:: is_uname(name: str) -> bool

   Is valid user-specified name? (valid name & !dummy prefix). 
           
   :param name: name to test. may be nullptr.
   :returns: 1: yes
   :returns: 0: no


.. py:function:: is_valid_typename(name: str) -> bool

   Is valid type name? 
           
   :param name: name to test. may be nullptr.
   :returns: 1: yes
   :returns: 0: no


.. py:function:: extract_name(line: str, x: int) -> str

   Extract a name or address from the specified string. 
           
   :param line: input string
   :param x: x coordinate of cursor
   :returns: -1 if cannot extract. otherwise length of the name


.. py:function:: hide_name(ea: ida_idaapi.ea_t) -> None

   Remove name from the list of names 
           
   :param ea: address of the name


.. py:function:: show_name(ea: ida_idaapi.ea_t) -> None

   Insert name to the list of names.


.. py:function:: get_name_ea(_from: ida_idaapi.ea_t, name: str) -> ida_idaapi.ea_t

   Get the address of a name. This function resolves a name into an address. It can handle regular global and local names, as well as debugger names. 
           
   :param name: any name in the program or nullptr
   :returns: address of the name or BADADDR


.. py:function:: get_name_base_ea(_from: ida_idaapi.ea_t, to: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get address of the name used in the expression for the address 
           
   :param to: the referenced address
   :returns: address of the name used to represent the operand


.. py:function:: get_name_value(_from: ida_idaapi.ea_t, name: str) -> uval_t *

   Get value of the name. This function knows about: regular names, enums, special segments, etc. 
           
   :param name: any name in the program or nullptr
   :returns: Name value result codes


.. py:data:: NT_NONE

   name doesn't exist or has no value


.. py:data:: NT_BYTE

   name is byte name (regular name)


.. py:data:: NT_LOCAL

   name is local label


.. py:data:: NT_STKVAR

   name is stack variable name


.. py:data:: NT_ENUM

   name is symbolic constant


.. py:data:: NT_ABS

   name is absolute symbol (SEG_ABSSYM)


.. py:data:: NT_SEG

   name is segment or segment register name


.. py:data:: NT_STROFF

   name is structure member


.. py:data:: NT_BMASK

   name is a bit group mask name


.. py:data:: NT_REGVAR

   name is a renamed register (*value is idx into pfn->regvars)


.. py:data:: GN_VISIBLE

   replace forbidden characters by SUBSTCHAR


.. py:data:: GN_COLORED

   return colored name


.. py:data:: GN_DEMANGLED

   return demangled name


.. py:data:: GN_STRICT

   fail if cannot demangle


.. py:data:: GN_SHORT

   use short form of demangled name


.. py:data:: GN_LONG

   use long form of demangled name


.. py:data:: GN_LOCAL

   try to get local name first; if failed, get global


.. py:data:: GN_ISRET

   for dummy names: use retloc


.. py:data:: GN_NOT_ISRET

   for dummy names: do not use retloc


.. py:data:: GN_NOT_DUMMY

   do not return a dummy name


.. py:function:: get_visible_name(ea: ida_idaapi.ea_t, gtn_flags: int = 0) -> str

.. py:function:: get_short_name(ea: ida_idaapi.ea_t, gtn_flags: int = 0) -> str

.. py:function:: get_long_name(ea: ida_idaapi.ea_t, gtn_flags: int = 0) -> str

.. py:function:: get_colored_short_name(ea: ida_idaapi.ea_t, gtn_flags: int = 0) -> str

.. py:function:: get_colored_long_name(ea: ida_idaapi.ea_t, gtn_flags: int = 0) -> str

.. py:function:: get_demangled_name(ea: ida_idaapi.ea_t, inhibitor: int, demform: int, gtn_flags: int = 0) -> str

.. py:function:: get_colored_demangled_name(ea: ida_idaapi.ea_t, inhibitor: int, demform: int, gtn_flags: int = 0) -> str

.. py:function:: get_name_color(_from: ida_idaapi.ea_t, ea: ida_idaapi.ea_t) -> color_t

   Calculate flags for get_ea_name() function.

   Get name color. 
           
   :param ea: linear address


.. py:data:: GETN_APPZERO

   meaningful only if the name refers to a structure. append a struct field name if the field offset is zero? 
           


.. py:data:: GETN_NOFIXUP

   ignore the fixup information when producing the name


.. py:data:: GETN_NODUMMY

   do not create a new dummy name but pretend it exists


.. py:function:: get_name_expr(_from: ida_idaapi.ea_t, n: int, ea: ida_idaapi.ea_t, off: int, flags: int = 1) -> str

   Convert address to name expression (name with a displacement). This function takes into account fixup information and returns a colored name expression (in the form <name> +/- <offset>). It also knows about structure members and arrays. If the specified address doesn't have a name, a dummy name is generated. 
           
   :param n: number of referencing operand. for data items specify 0
   :param ea: address to convert to name expression
   :param off: the value of name expression. this parameter is used only to check that the name expression will have the wanted value. 'off' may be equal to BADADDR but this is discouraged because it prohibits checks.
   :param flags: Name expression flags
   :returns: < 0 if address is not valid, no segment or other failure. otherwise the length of the name expression in characters.


.. py:function:: get_nice_colored_name(ea: ida_idaapi.ea_t, flags: int = 0) -> str

   Get a nice colored name at the specified address. Ex:
   * segment:sub+offset
   * segment:sub:local_label
   * segment:label
   * segment:address
   * segment:address+offset



   :param ea: linear address
   :param flags: Nice colored name flags
   :returns: the length of the generated name in bytes.


.. py:data:: GNCN_NOSEG

   ignore the segment prefix when producing the name


.. py:data:: GNCN_NOCOLOR

   generate an uncolored name


.. py:data:: GNCN_NOLABEL

   don't generate labels


.. py:data:: GNCN_NOFUNC

   don't generate funcname+... expressions


.. py:data:: GNCN_SEG_FUNC

   generate both segment and function names (default is to omit segment name if a function name is present)


.. py:data:: GNCN_SEGNUM

   segment part is displayed as a hex number


.. py:data:: GNCN_REQFUNC

   return 0 if the address does not belong to a function


.. py:data:: GNCN_REQNAME

   return 0 if the address can only be represented as a hex number


.. py:data:: GNCN_NODBGNM

   don't use debug names


.. py:data:: GNCN_PREFDBG

   if using debug names, prefer debug names over function names


.. py:function:: append_struct_fields(disp: adiff_t *, n: int, path: tid_t const *, flags: flags64_t, delta: adiff_t, appzero: bool) -> str

   Append names of struct fields to a name if the name is a struct name. 
           
   :param disp: displacement from the name
   :param n: operand number in which the name appears
   :param path: path in the struct. path is an array of id's. maximal length of array is MAXSTRUCPATH. the first element of the array is the structure id. consecutive elements are id's of used union members (if any).
   :param flags: the input flags. they will be returned if the struct cannot be found.
   :param delta: delta to add to displacement
   :param appzero: should append a struct field name if the displacement is zero?
   :returns: flags of the innermost struct member or the input flags


.. py:function:: is_public_name(ea: ida_idaapi.ea_t) -> bool

.. py:function:: make_name_public(ea: ida_idaapi.ea_t) -> None

.. py:function:: make_name_non_public(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_weak_name(ea: ida_idaapi.ea_t) -> bool

.. py:function:: make_name_weak(ea: ida_idaapi.ea_t) -> None

.. py:function:: make_name_non_weak(ea: ida_idaapi.ea_t) -> None

.. py:function:: get_nlist_size() -> size_t

.. py:function:: get_nlist_idx(ea: ida_idaapi.ea_t) -> size_t

.. py:function:: is_in_nlist(ea: ida_idaapi.ea_t) -> bool

.. py:function:: get_nlist_ea(idx: size_t) -> ida_idaapi.ea_t

.. py:function:: get_nlist_name(idx: size_t) -> str

.. py:function:: rebuild_nlist() -> None

.. py:function:: reorder_dummy_names() -> None

   Renumber dummy names.


.. py:data:: DEBNAME_EXACT

   find a name at exactly the specified address


.. py:data:: DEBNAME_LOWER

   find a name with the address >= the specified address


.. py:data:: DEBNAME_UPPER

   find a name with the address > the specified address


.. py:data:: DEBNAME_NICE

   find a name with the address <= the specified address


.. py:class:: ea_name_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: name
      :type:  str


.. py:function:: set_debug_name(ea: ida_idaapi.ea_t, name: str) -> bool

.. py:function:: get_debug_name(ea_ptr: ea_t *, how: debug_name_how_t) -> str

.. py:function:: del_debug_names(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> None

.. py:function:: get_debug_name_ea(name: str) -> ida_idaapi.ea_t

.. py:data:: DQT_NPURGED_8

   only calculate number of purged bytes (sizeof(arg)==8)


.. py:data:: DQT_NPURGED_4

   only calculate number of purged bytes (sizeof(arg)==4)


.. py:data:: DQT_NPURGED_2

   only calculate number of purged bytes (sizeof(arg)==2)


.. py:data:: DQT_COMPILER

   only detect compiler that generated the name


.. py:data:: DQT_NAME_TYPE

   only detect the name type (data/code)


.. py:data:: DQT_FULL

   really demangle


.. py:function:: demangle_name(name: str, disable_mask: int, demreq: demreq_type_t = DQT_FULL) -> str

   Demangle a name. 
           
   :param name: name to demangle
   :param disable_mask: bits to inhibit parts of demangled name (see MNG_). by the M_COMPILER bits a specific compiler can be selected (see MT_).
   :param demreq: the request type demreq_type_t
   :returns: ME_... or MT__ bitmasks from demangle.hpp


.. py:function:: is_name_defined_locally(*args) -> bool

   Is the name defined locally in the specified function? 
           
   :param pfn: pointer to function
   :param name: name to check
   :param ignore_name_def: which names to ignore when checking
   :param ea1: the starting address of the range inside the function (optional)
   :param ea2: the ending address of the range inside the function (optional)
   :returns: true if the name has been defined


.. py:function:: cleanup_name(ea: ida_idaapi.ea_t, name: str, flags: int = 0) -> str

.. py:data:: CN_KEEP_TRAILING_DIGITS

   do not remove "_\d+" at the end of name


.. py:data:: CN_KEEP_UNDERSCORES

   do not remove leading underscores. but it is ok to remove __imp_. 
           


.. py:data:: ME_INTERR

.. py:data:: ME_PARAMERR

.. py:data:: ME_ILLSTR

.. py:data:: ME_SMALLANS

.. py:data:: ME_FRAME

.. py:data:: ME_NOCOMP

.. py:data:: ME_ERRAUTO

.. py:data:: ME_NOHASHMEM

.. py:data:: ME_NOSTRMEM

.. py:data:: ME_NOERROR_LIMIT

.. py:data:: M_PRCMSK

.. py:data:: MT_DEFAULT

.. py:data:: MT_CDECL

.. py:data:: MT_PASCAL

.. py:data:: MT_STDCALL

.. py:data:: MT_FASTCALL

.. py:data:: MT_THISCALL

.. py:data:: MT_FORTRAN

.. py:data:: MT_SYSCALL

.. py:data:: MT_INTERRUPT

.. py:data:: MT_MSFASTCALL

.. py:data:: MT_CLRCALL

.. py:data:: MT_DMDCALL

.. py:data:: MT_VECTORCALL

.. py:data:: MT_REGCALL

.. py:data:: MT_LOCALNAME

.. py:data:: M_SAVEREGS

.. py:data:: M_CLASS

.. py:data:: MT_PUBLIC

.. py:data:: MT_PRIVATE

.. py:data:: MT_PROTECT

.. py:data:: MT_MEMBER

.. py:data:: MT_VTABLE

.. py:data:: MT_RTTI

.. py:data:: M_PARMSK

.. py:data:: MT_PARSHF

.. py:data:: MT_PARMAX

.. py:data:: M_ELLIPSIS

.. py:data:: MT_VOIDARG

.. py:data:: M_STATIC

.. py:data:: M_VIRTUAL

.. py:data:: M_AUTOCRT

.. py:data:: M_TYPMASK

.. py:data:: MT_OPERAT

.. py:data:: MT_CONSTR

.. py:data:: MT_DESTR

.. py:data:: MT_CASTING

.. py:data:: MT_CLRCDTOR

.. py:data:: M_TRUNCATE

.. py:data:: M_THUNK

.. py:data:: M_ANONNSP

.. py:data:: M_TMPLNAM

.. py:data:: M_DBGNAME

.. py:data:: M_COMPILER

.. py:data:: MT_MSCOMP

.. py:data:: MT_BORLAN

.. py:data:: MT_WATCOM

.. py:data:: MT_OTHER

.. py:data:: MT_GNU

.. py:data:: MT_GCC3

.. py:data:: MT_VISAGE

.. py:data:: MNG_PTRMSK

.. py:data:: MNG_DEFNEAR

.. py:data:: MNG_DEFNEARANY

.. py:data:: MNG_DEFFAR

.. py:data:: MNG_NOPTRTYP16

.. py:data:: MNG_DEFHUGE

.. py:data:: MNG_DEFPTR64

.. py:data:: MNG_DEFNONE

.. py:data:: MNG_NOPTRTYP

.. py:data:: MNG_NODEFINIT

.. py:data:: MNG_NOUNDERSCORE

.. py:data:: MNG_NOTYPE

.. py:data:: MNG_NORETTYPE

.. py:data:: MNG_NOBASEDT

.. py:data:: MNG_NOCALLC

.. py:data:: MNG_NOPOSTFC

.. py:data:: MNG_NOSCTYP

.. py:data:: MNG_NOTHROW

.. py:data:: MNG_NOSTVIR

.. py:data:: MNG_NOECSU

.. py:data:: MNG_NOCSVOL

.. py:data:: MNG_NOCLOSUR

.. py:data:: MNG_NOUNALG

.. py:data:: MNG_NOMANAGE

.. py:data:: MNG_NOMODULE

.. py:data:: MNG_SHORT_S

.. py:data:: MNG_SHORT_U

.. py:data:: MNG_ZPT_SPACE

.. py:data:: MNG_DROP_IMP

.. py:data:: MNG_IGN_ANYWAY

.. py:data:: MNG_IGN_JMP

.. py:data:: MNG_MOVE_JMP

.. py:data:: MNG_COMPILER_MSK

.. py:data:: MNG_SHORT_FORM

.. py:data:: MNG_LONG_FORM

.. py:data:: MNG_CALC_VALID

.. py:function:: get_mangled_name_type(name: str) -> mangled_name_type_t

.. py:function:: get_debug_names(*args) -> PyObject *

.. py:function:: get_ea_name(ea: ida_idaapi.ea_t, gtn_flags: int = 0) -> str

   Get name at the specified address. 
           
   :param ea: linear address
   :param gtn_flags: how exactly the name should be retrieved. combination of bits for get_ea_name() function. There is a convenience bits
   :returns: success


.. py:function:: validate_name(name: str, type: nametype_t, flags: int = 1) -> PyObject *

   Validate a name. If SN_NOCHECK is specified, this function replaces all invalid characters in the name with SUBSTCHAR. However, it will return false if name is valid but not allowed to be an identifier (is a register name).

   :param name: ptr to name. the name will be modified
   :param type: the type of name we want to validate
   :param flags: see SN_*
   :returns: success


.. py:class:: NearestName(ea_names)

   Bases: :py:obj:`object`


   Utility class to help find the nearest name in a given ea/name dictionary


   .. py:method:: update(ea_names)

      Updates the ea/names map



   .. py:method:: find(ea)

      Returns a tupple (ea, name, pos) that is the nearest to the passed ea
      If no name is matched then None is returned



.. py:function:: calc_gtn_flags(fromaddr, ea)

   Calculate flags for get_ea_name() function

   :param fromaddr: the referring address. May be BADADDR.
   :param ea: linear address

   :returns: flags


.. py:data:: cvar

.. py:data:: ignore_none

.. py:data:: ignore_regvar

.. py:data:: ignore_llabel

.. py:data:: ignore_stkvar

.. py:data:: ignore_glabel

.. py:data:: MANGLED_CODE

.. py:data:: MANGLED_DATA

.. py:data:: MANGLED_UNKNOWN


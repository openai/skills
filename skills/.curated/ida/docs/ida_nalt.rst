ida_nalt
========

.. py:module:: ida_nalt

.. autoapi-nested-parse::

   Definitions of various information kept in netnodes.

   Each address in the program has a corresponding netnode: netnode(ea).
   If we have no information about an address, the corresponding netnode is not created. Otherwise we will create a netnode and save information in it. All variable length information (names, comments, offset information, etc) is stored in the netnode.
   Don't forget that some information is already stored in the flags (bytes.hpp)
   netnode. 
       



Attributes
----------

.. autoapisummary::

   ida_nalt.NALT_SWITCH
   ida_nalt.NALT_STRUCT
   ida_nalt.NALT_AFLAGS
   ida_nalt.NALT_LINNUM
   ida_nalt.NALT_ABSBASE
   ida_nalt.NALT_ENUM0
   ida_nalt.NALT_ENUM1
   ida_nalt.NALT_PURGE
   ida_nalt.NALT_STRTYPE
   ida_nalt.NALT_ALIGN
   ida_nalt.NALT_COLOR
   ida_nalt.NSUP_CMT
   ida_nalt.NSUP_REPCMT
   ida_nalt.NSUP_FOP1
   ida_nalt.NSUP_FOP2
   ida_nalt.NSUP_JINFO
   ida_nalt.NSUP_ARRAY
   ida_nalt.NSUP_OMFGRP
   ida_nalt.NSUP_FOP3
   ida_nalt.NSUP_SWITCH
   ida_nalt.NSUP_REF0
   ida_nalt.NSUP_REF1
   ida_nalt.NSUP_REF2
   ida_nalt.NSUP_OREF0
   ida_nalt.NSUP_OREF1
   ida_nalt.NSUP_OREF2
   ida_nalt.NSUP_STROFF0
   ida_nalt.NSUP_STROFF1
   ida_nalt.NSUP_SEGTRANS
   ida_nalt.NSUP_FOP4
   ida_nalt.NSUP_FOP5
   ida_nalt.NSUP_FOP6
   ida_nalt.NSUP_REF3
   ida_nalt.NSUP_REF4
   ida_nalt.NSUP_REF5
   ida_nalt.NSUP_OREF3
   ida_nalt.NSUP_OREF4
   ida_nalt.NSUP_OREF5
   ida_nalt.NSUP_XREFPOS
   ida_nalt.NSUP_CUSTDT
   ida_nalt.NSUP_GROUPS
   ida_nalt.NSUP_ARGEAS
   ida_nalt.NSUP_FOP7
   ida_nalt.NSUP_FOP8
   ida_nalt.NSUP_REF6
   ida_nalt.NSUP_REF7
   ida_nalt.NSUP_OREF6
   ida_nalt.NSUP_OREF7
   ida_nalt.NSUP_EX_FLAGS
   ida_nalt.NSUP_POINTS
   ida_nalt.NSUP_MANUAL
   ida_nalt.NSUP_TYPEINFO
   ida_nalt.NSUP_REGVAR
   ida_nalt.NSUP_LLABEL
   ida_nalt.NSUP_REGARG
   ida_nalt.NSUP_FTAILS
   ida_nalt.NSUP_GROUP
   ida_nalt.NSUP_OPTYPES
   ida_nalt.NSUP_ORIGFMD
   ida_nalt.NSUP_FRAME
   ida_nalt.NALT_CREF_TO
   ida_nalt.NALT_CREF_FROM
   ida_nalt.NALT_DREF_TO
   ida_nalt.NALT_DREF_FROM
   ida_nalt.NSUP_GR_INFO
   ida_nalt.NALT_GR_LAYX
   ida_nalt.NSUP_GR_LAYT
   ida_nalt.PATCH_TAG
   ida_nalt.IDB_DESKTOPS_NODE_NAME
   ida_nalt.IDB_DESKTOPS_TAG
   ida_nalt.AFL_LINNUM
   ida_nalt.AFL_USERSP
   ida_nalt.AFL_PUBNAM
   ida_nalt.AFL_WEAKNAM
   ida_nalt.AFL_HIDDEN
   ida_nalt.AFL_MANUAL
   ida_nalt.AFL_NOBRD
   ida_nalt.AFL_ZSTROFF
   ida_nalt.AFL_BNOT0
   ida_nalt.AFL_BNOT1
   ida_nalt.AFL_LIB
   ida_nalt.AFL_TI
   ida_nalt.AFL_TI0
   ida_nalt.AFL_TI1
   ida_nalt.AFL_LNAME
   ida_nalt.AFL_TILCMT
   ida_nalt.AFL_LZERO0
   ida_nalt.AFL_LZERO1
   ida_nalt.AFL_COLORED
   ida_nalt.AFL_TERSESTR
   ida_nalt.AFL_SIGN0
   ida_nalt.AFL_SIGN1
   ida_nalt.AFL_NORET
   ida_nalt.AFL_FIXEDSPD
   ida_nalt.AFL_ALIGNFLOW
   ida_nalt.AFL_USERTI
   ida_nalt.AFL_RETFP
   ida_nalt.AFL_USEMODSP
   ida_nalt.AFL_NOTCODE
   ida_nalt.AFL_NOTPROC
   ida_nalt.AFL_TYPE_GUESSED
   ida_nalt.AFL_IDA_GUESSED
   ida_nalt.AFL_HR_GUESSED_FUNC
   ida_nalt.AFL_HR_GUESSED_DATA
   ida_nalt.AFL_HR_DETERMINED
   ida_nalt.STRWIDTH_1B
   ida_nalt.STRWIDTH_2B
   ida_nalt.STRWIDTH_4B
   ida_nalt.STRWIDTH_MASK
   ida_nalt.STRLYT_TERMCHR
   ida_nalt.STRLYT_PASCAL1
   ida_nalt.STRLYT_PASCAL2
   ida_nalt.STRLYT_PASCAL4
   ida_nalt.STRLYT_MASK
   ida_nalt.STRLYT_SHIFT
   ida_nalt.STRTYPE_TERMCHR
   ida_nalt.STRTYPE_C
   ida_nalt.STRTYPE_C_16
   ida_nalt.STRTYPE_C_32
   ida_nalt.STRTYPE_PASCAL
   ida_nalt.STRTYPE_PASCAL_16
   ida_nalt.STRTYPE_PASCAL_32
   ida_nalt.STRTYPE_LEN2
   ida_nalt.STRTYPE_LEN2_16
   ida_nalt.STRTYPE_LEN2_32
   ida_nalt.STRTYPE_LEN4
   ida_nalt.STRTYPE_LEN4_16
   ida_nalt.STRTYPE_LEN4_32
   ida_nalt.STRENC_DEFAULT
   ida_nalt.STRENC_NONE
   ida_nalt.AP_ALLOWDUPS
   ida_nalt.AP_SIGNED
   ida_nalt.AP_INDEX
   ida_nalt.AP_ARRAY
   ida_nalt.AP_IDXBASEMASK
   ida_nalt.AP_IDXDEC
   ida_nalt.AP_IDXHEX
   ida_nalt.AP_IDXOCT
   ida_nalt.AP_IDXBIN
   ida_nalt.SWI_SPARSE
   ida_nalt.SWI_V32
   ida_nalt.SWI_J32
   ida_nalt.SWI_VSPLIT
   ida_nalt.SWI_USER
   ida_nalt.SWI_DEF_IN_TBL
   ida_nalt.SWI_JMP_INV
   ida_nalt.SWI_SHIFT_MASK
   ida_nalt.SWI_ELBASE
   ida_nalt.SWI_JSIZE
   ida_nalt.SWI_VSIZE
   ida_nalt.SWI_SEPARATE
   ida_nalt.SWI_SIGNED
   ida_nalt.SWI_CUSTOM
   ida_nalt.SWI_INDIRECT
   ida_nalt.SWI_SUBTRACT
   ida_nalt.SWI_HXNOLOWCASE
   ida_nalt.SWI_STDTBL
   ida_nalt.SWI_DEFRET
   ida_nalt.SWI_SELFREL
   ida_nalt.SWI_JMPINSN
   ida_nalt.SWI_VERSION
   ida_nalt.cvar
   ida_nalt.V695_REF_OFF8
   ida_nalt.REF_OFF16
   ida_nalt.REF_OFF32
   ida_nalt.REF_LOW8
   ida_nalt.REF_LOW16
   ida_nalt.REF_HIGH8
   ida_nalt.REF_HIGH16
   ida_nalt.V695_REF_VHIGH
   ida_nalt.V695_REF_VLOW
   ida_nalt.REF_OFF64
   ida_nalt.REF_OFF8
   ida_nalt.REF_LAST
   ida_nalt.REFINFO_TYPE
   ida_nalt.REFINFO_RVAOFF
   ida_nalt.REFINFO_PASTEND
   ida_nalt.REFINFO_CUSTOM
   ida_nalt.REFINFO_NOBASE
   ida_nalt.REFINFO_SUBTRACT
   ida_nalt.REFINFO_SIGNEDOP
   ida_nalt.REFINFO_NO_ZEROS
   ida_nalt.REFINFO_NO_ONES
   ida_nalt.REFINFO_SELFREF
   ida_nalt.MAXSTRUCPATH
   ida_nalt.POF_VALID_TI
   ida_nalt.POF_VALID_AFLAGS
   ida_nalt.POF_IS_F64
   ida_nalt.RIDX_FILE_FORMAT_NAME
   ida_nalt.RIDX_SELECTORS
   ida_nalt.RIDX_GROUPS
   ida_nalt.RIDX_H_PATH
   ida_nalt.RIDX_C_MACROS
   ida_nalt.RIDX_SMALL_IDC_OLD
   ida_nalt.RIDX_NOTEPAD
   ida_nalt.RIDX_INCLUDE
   ida_nalt.RIDX_SMALL_IDC
   ida_nalt.RIDX_DUALOP_GRAPH
   ida_nalt.RIDX_DUALOP_TEXT
   ida_nalt.RIDX_MD5
   ida_nalt.RIDX_IDA_VERSION
   ida_nalt.RIDX_STR_ENCODINGS
   ida_nalt.RIDX_SRCDBG_PATHS
   ida_nalt.RIDX_DBG_BINPATHS
   ida_nalt.RIDX_SHA256
   ida_nalt.RIDX_ABINAME
   ida_nalt.RIDX_ARCHIVE_PATH
   ida_nalt.RIDX_PROBLEMS
   ida_nalt.RIDX_SRCDBG_UNDESIRED
   ida_nalt.BPU_1B
   ida_nalt.BPU_2B
   ida_nalt.BPU_4B
   ida_nalt.GOTEA_NODE_NAME
   ida_nalt.GOTEA_NODE_IDX
   ida_nalt.get_initial_version


Classes
-------

.. autoapisummary::

   ida_nalt.custom_data_type_ids_fids_array
   ida_nalt.strpath_ids_array
   ida_nalt.array_parameters_t
   ida_nalt.switch_info_t
   ida_nalt.custom_data_type_ids_t
   ida_nalt.refinfo_t
   ida_nalt.strpath_t
   ida_nalt.enum_const_t
   ida_nalt.opinfo_t
   ida_nalt.printop_t


Functions
---------

.. autoapisummary::

   ida_nalt.ea2node
   ida_nalt.node2ea
   ida_nalt.end_ea2node
   ida_nalt.getnode
   ida_nalt.get_strid
   ida_nalt.set_aflags
   ida_nalt.upd_abits
   ida_nalt.set_abits
   ida_nalt.clr_abits
   ida_nalt.get_aflags
   ida_nalt.del_aflags
   ida_nalt.has_aflag_linnum
   ida_nalt.is_aflag_usersp
   ida_nalt.is_aflag_public_name
   ida_nalt.is_aflag_weak_name
   ida_nalt.is_aflag_hidden_item
   ida_nalt.is_aflag_manual_insn
   ida_nalt.is_aflag_hidden_border
   ida_nalt.is_aflag_zstroff
   ida_nalt.is_aflag__bnot0
   ida_nalt.is_aflag__bnot1
   ida_nalt.is_aflag_libitem
   ida_nalt.has_aflag_ti
   ida_nalt.has_aflag_ti0
   ida_nalt.has_aflag_ti1
   ida_nalt.has_aflag_lname
   ida_nalt.is_aflag_tilcmt
   ida_nalt.is_aflag_lzero0
   ida_nalt.is_aflag_lzero1
   ida_nalt.is_aflag_colored_item
   ida_nalt.is_aflag_terse_struc
   ida_nalt.is_aflag__invsign0
   ida_nalt.is_aflag__invsign1
   ida_nalt.is_aflag_noret
   ida_nalt.is_aflag_fixed_spd
   ida_nalt.is_aflag_align_flow
   ida_nalt.is_aflag_userti
   ida_nalt.is_aflag_retfp
   ida_nalt.uses_aflag_modsp
   ida_nalt.is_aflag_notcode
   ida_nalt.is_aflag_notproc
   ida_nalt.is_aflag_type_guessed_by_ida
   ida_nalt.is_aflag_func_guessed_by_hexrays
   ida_nalt.is_aflag_data_guessed_by_hexrays
   ida_nalt.is_aflag_type_determined_by_hexrays
   ida_nalt.is_aflag_type_guessed_by_hexrays
   ida_nalt.is_hidden_item
   ida_nalt.hide_item
   ida_nalt.unhide_item
   ida_nalt.is_hidden_border
   ida_nalt.hide_border
   ida_nalt.unhide_border
   ida_nalt.uses_modsp
   ida_nalt.set_usemodsp
   ida_nalt.clr_usemodsp
   ida_nalt.is_zstroff
   ida_nalt.set_zstroff
   ida_nalt.clr_zstroff
   ida_nalt.is__bnot0
   ida_nalt.set__bnot0
   ida_nalt.clr__bnot0
   ida_nalt.is__bnot1
   ida_nalt.set__bnot1
   ida_nalt.clr__bnot1
   ida_nalt.is_libitem
   ida_nalt.set_libitem
   ida_nalt.clr_libitem
   ida_nalt.has_ti
   ida_nalt.set_has_ti
   ida_nalt.clr_has_ti
   ida_nalt.has_ti0
   ida_nalt.set_has_ti0
   ida_nalt.clr_has_ti0
   ida_nalt.has_ti1
   ida_nalt.set_has_ti1
   ida_nalt.clr_has_ti1
   ida_nalt.has_lname
   ida_nalt.set_has_lname
   ida_nalt.clr_has_lname
   ida_nalt.is_tilcmt
   ida_nalt.set_tilcmt
   ida_nalt.clr_tilcmt
   ida_nalt.is_usersp
   ida_nalt.set_usersp
   ida_nalt.clr_usersp
   ida_nalt.is_lzero0
   ida_nalt.set_lzero0
   ida_nalt.clr_lzero0
   ida_nalt.is_lzero1
   ida_nalt.set_lzero1
   ida_nalt.clr_lzero1
   ida_nalt.is_colored_item
   ida_nalt.set_colored_item
   ida_nalt.clr_colored_item
   ida_nalt.is_terse_struc
   ida_nalt.set_terse_struc
   ida_nalt.clr_terse_struc
   ida_nalt.is__invsign0
   ida_nalt.set__invsign0
   ida_nalt.clr__invsign0
   ida_nalt.is__invsign1
   ida_nalt.set__invsign1
   ida_nalt.clr__invsign1
   ida_nalt.is_noret
   ida_nalt.set_noret
   ida_nalt.clr_noret
   ida_nalt.is_fixed_spd
   ida_nalt.set_fixed_spd
   ida_nalt.clr_fixed_spd
   ida_nalt.is_align_flow
   ida_nalt.set_align_flow
   ida_nalt.clr_align_flow
   ida_nalt.is_userti
   ida_nalt.set_userti
   ida_nalt.clr_userti
   ida_nalt.is_retfp
   ida_nalt.set_retfp
   ida_nalt.clr_retfp
   ida_nalt.is_notproc
   ida_nalt.set_notproc
   ida_nalt.clr_notproc
   ida_nalt.is_type_guessed_by_ida
   ida_nalt.is_func_guessed_by_hexrays
   ida_nalt.is_data_guessed_by_hexrays
   ida_nalt.is_type_determined_by_hexrays
   ida_nalt.is_type_guessed_by_hexrays
   ida_nalt.set_type_guessed_by_ida
   ida_nalt.set_func_guessed_by_hexrays
   ida_nalt.set_data_guessed_by_hexrays
   ida_nalt.set_type_determined_by_hexrays
   ida_nalt.set_notcode
   ida_nalt.clr_notcode
   ida_nalt.is_notcode
   ida_nalt.set_visible_item
   ida_nalt.is_visible_item
   ida_nalt.is_finally_visible_item
   ida_nalt.set_source_linnum
   ida_nalt.get_source_linnum
   ida_nalt.del_source_linnum
   ida_nalt.get_absbase
   ida_nalt.set_absbase
   ida_nalt.del_absbase
   ida_nalt.get_ind_purged
   ida_nalt.del_ind_purged
   ida_nalt.get_str_type
   ida_nalt.set_str_type
   ida_nalt.del_str_type
   ida_nalt.get_str_type_code
   ida_nalt.get_str_term1
   ida_nalt.get_str_term2
   ida_nalt.get_str_encoding_idx
   ida_nalt.set_str_encoding_idx
   ida_nalt.make_str_type
   ida_nalt.is_pascal
   ida_nalt.get_str_type_prefix_length
   ida_nalt.get_alignment
   ida_nalt.set_alignment
   ida_nalt.del_alignment
   ida_nalt.set_item_color
   ida_nalt.get_item_color
   ida_nalt.del_item_color
   ida_nalt.get_array_parameters
   ida_nalt.set_array_parameters
   ida_nalt.del_array_parameters
   ida_nalt.get_switch_info
   ida_nalt.set_switch_info
   ida_nalt.del_switch_info
   ida_nalt.get_switch_parent
   ida_nalt.set_switch_parent
   ida_nalt.del_switch_parent
   ida_nalt.get_custom_data_type_ids
   ida_nalt.set_custom_data_type_ids
   ida_nalt.del_custom_data_type_ids
   ida_nalt.is_reftype_target_optional
   ida_nalt.get_reftype_by_size
   ida_nalt.find_custom_refinfo
   ida_nalt.get_custom_refinfo
   ida_nalt.set_refinfo_ex
   ida_nalt.set_refinfo
   ida_nalt.get_refinfo
   ida_nalt.del_refinfo
   ida_nalt.get_tinfo
   ida_nalt.set_tinfo
   ida_nalt.del_tinfo
   ida_nalt.get_op_tinfo
   ida_nalt.set_op_tinfo
   ida_nalt.del_op_tinfo
   ida_nalt.get_root_filename
   ida_nalt.dbg_get_input_path
   ida_nalt.get_input_file_path
   ida_nalt.set_root_filename
   ida_nalt.retrieve_input_file_size
   ida_nalt.retrieve_input_file_crc32
   ida_nalt.retrieve_input_file_md5
   ida_nalt.retrieve_input_file_sha256
   ida_nalt.get_asm_inc_file
   ida_nalt.set_asm_inc_file
   ida_nalt.get_imagebase
   ida_nalt.set_imagebase
   ida_nalt.get_ids_modnode
   ida_nalt.set_ids_modnode
   ida_nalt.get_archive_path
   ida_nalt.set_archive_path
   ida_nalt.get_loader_format_name
   ida_nalt.set_loader_format_name
   ida_nalt.get_initial_ida_version
   ida_nalt.get_ida_notepad_text
   ida_nalt.set_ida_notepad_text
   ida_nalt.get_srcdbg_paths
   ida_nalt.set_srcdbg_paths
   ida_nalt.get_srcdbg_undesired_paths
   ida_nalt.set_srcdbg_undesired_paths
   ida_nalt.get_initial_idb_version
   ida_nalt.get_idb_ctime
   ida_nalt.get_elapsed_secs
   ida_nalt.get_idb_nopens
   ida_nalt.get_encoding_qty
   ida_nalt.get_encoding_name
   ida_nalt.add_encoding
   ida_nalt.del_encoding
   ida_nalt.rename_encoding
   ida_nalt.get_encoding_bpu
   ida_nalt.get_encoding_bpu_by_name
   ida_nalt.get_strtype_bpu
   ida_nalt.get_default_encoding_idx
   ida_nalt.set_default_encoding_idx
   ida_nalt.encoding_from_strtype
   ida_nalt.get_outfile_encoding_idx
   ida_nalt.set_outfile_encoding_idx
   ida_nalt.get_import_module_qty
   ida_nalt.delete_imports
   ida_nalt.set_gotea
   ida_nalt.get_gotea
   ida_nalt.get_import_module_name
   ida_nalt.enum_import_names
   ida_nalt.switch_info_t__from_ptrval__
   ida_nalt.get_switch_info
   ida_nalt.get_abi_name


Module Contents
---------------

.. py:class:: custom_data_type_ids_fids_array(data: short (&)[8])

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  short (&)[8]


   .. py:attribute:: bytes


.. py:class:: strpath_ids_array(data: unsigned long long (&)[32])

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  unsigned long long (&)[32]


   .. py:attribute:: bytes


.. py:data:: NALT_SWITCH

   switch idiom address (used at jump targets)


.. py:data:: NALT_STRUCT

   struct id


.. py:data:: NALT_AFLAGS

   additional flags for an item


.. py:data:: NALT_LINNUM

   source line number


.. py:data:: NALT_ABSBASE

   absolute segment location


.. py:data:: NALT_ENUM0

   enum id for the first operand


.. py:data:: NALT_ENUM1

   enum id for the second operand


.. py:data:: NALT_PURGE

   number of bytes purged from the stack when a function is called indirectly


.. py:data:: NALT_STRTYPE

   type of string item


.. py:data:: NALT_ALIGN

   alignment value if the item is FF_ALIGN (should by equal to power of 2) 
           


.. py:data:: NALT_COLOR

   instruction/data background color


.. py:data:: NSUP_CMT

   regular comment


.. py:data:: NSUP_REPCMT

   repeatable comment


.. py:data:: NSUP_FOP1

   forced operand 1


.. py:data:: NSUP_FOP2

   forced operand 2


.. py:data:: NSUP_JINFO

   jump table info


.. py:data:: NSUP_ARRAY

   array parameters


.. py:data:: NSUP_OMFGRP

   OMF: group of segments (not used anymore)


.. py:data:: NSUP_FOP3

   forced operand 3


.. py:data:: NSUP_SWITCH

   switch information


.. py:data:: NSUP_REF0

   complex reference information for operand 1


.. py:data:: NSUP_REF1

   complex reference information for operand 2


.. py:data:: NSUP_REF2

   complex reference information for operand 3


.. py:data:: NSUP_OREF0

   outer complex reference information for operand 1


.. py:data:: NSUP_OREF1

   outer complex reference information for operand 2


.. py:data:: NSUP_OREF2

   outer complex reference information for operand 3


.. py:data:: NSUP_STROFF0

   stroff: struct path for the first operand


.. py:data:: NSUP_STROFF1

   stroff: struct path for the second operand


.. py:data:: NSUP_SEGTRANS

   segment translations


.. py:data:: NSUP_FOP4

   forced operand 4


.. py:data:: NSUP_FOP5

   forced operand 5


.. py:data:: NSUP_FOP6

   forced operand 6


.. py:data:: NSUP_REF3

   complex reference information for operand 4


.. py:data:: NSUP_REF4

   complex reference information for operand 5


.. py:data:: NSUP_REF5

   complex reference information for operand 6


.. py:data:: NSUP_OREF3

   outer complex reference information for operand 4


.. py:data:: NSUP_OREF4

   outer complex reference information for operand 5


.. py:data:: NSUP_OREF5

   outer complex reference information for operand 6


.. py:data:: NSUP_XREFPOS

   saved xref address and type in the xrefs window


.. py:data:: NSUP_CUSTDT

   custom data type id


.. py:data:: NSUP_GROUPS

   SEG_GRP: pack_dd encoded list of selectors.


.. py:data:: NSUP_ARGEAS

   instructions that initialize call arguments


.. py:data:: NSUP_FOP7

   forced operand 7


.. py:data:: NSUP_FOP8

   forced operand 8


.. py:data:: NSUP_REF6

   complex reference information for operand 7


.. py:data:: NSUP_REF7

   complex reference information for operand 8


.. py:data:: NSUP_OREF6

   outer complex reference information for operand 7


.. py:data:: NSUP_OREF7

   outer complex reference information for operand 8


.. py:data:: NSUP_EX_FLAGS

   Extended flags.


.. py:data:: NSUP_POINTS

   SP change points blob (see funcs.cpp). values NSUP_POINTS..NSUP_POINTS+0x1000 are reserved 
           


.. py:data:: NSUP_MANUAL

   manual instruction. values NSUP_MANUAL..NSUP_MANUAL+0x1000 are reserved 
           


.. py:data:: NSUP_TYPEINFO

   type information. values NSUP_TYPEINFO..NSUP_TYPEINFO+0x1000 are reserved 
           


.. py:data:: NSUP_REGVAR

   register variables. values NSUP_REGVAR..NSUP_REGVAR+0x1000 are reserved 
           


.. py:data:: NSUP_LLABEL

   local labels. values NSUP_LLABEL..NSUP_LLABEL+0x1000 are reserved 
           


.. py:data:: NSUP_REGARG

   register argument type/name descriptions values NSUP_REGARG..NSUP_REGARG+0x1000 are reserved 
           


.. py:data:: NSUP_FTAILS

   function tails or tail referers values NSUP_FTAILS..NSUP_FTAILS+0x1000 are reserved 
           


.. py:data:: NSUP_GROUP

   graph group information values NSUP_GROUP..NSUP_GROUP+0x1000 are reserved 
           


.. py:data:: NSUP_OPTYPES

   operand type information. values NSUP_OPTYPES..NSUP_OPTYPES+0x100000 are reserved 
           


.. py:data:: NSUP_ORIGFMD

   function metadata before lumina information was applied values NSUP_ORIGFMD..NSUP_ORIGFMD+0x1000 are reserved 
           


.. py:data:: NSUP_FRAME

   function frame type values NSUP_FRAME..NSUP_FRAME+0x10000 are reserved 
           


.. py:data:: NALT_CREF_TO

   code xref to, idx: target address


.. py:data:: NALT_CREF_FROM

   code xref from, idx: source address


.. py:data:: NALT_DREF_TO

   data xref to, idx: target address


.. py:data:: NALT_DREF_FROM

   data xref from, idx: source address


.. py:data:: NSUP_GR_INFO

   group node info: color, ea, text


.. py:data:: NALT_GR_LAYX

   group layout ptrs, hash: md5 of 'belongs'


.. py:data:: NSUP_GR_LAYT

   group layouts, idx: layout pointer


.. py:data:: PATCH_TAG

   Patch netnode tag.


.. py:data:: IDB_DESKTOPS_NODE_NAME

   hash indexed by desktop name with dekstop netnode


.. py:data:: IDB_DESKTOPS_TAG

   tag to store desktop blob & timestamp


.. py:function:: ea2node(ea: ida_idaapi.ea_t) -> nodeidx_t

   Get netnode for the specified address.


.. py:function:: node2ea(ndx: nodeidx_t) -> ida_idaapi.ea_t

.. py:function:: end_ea2node(ea: ida_idaapi.ea_t) -> nodeidx_t

.. py:function:: getnode(ea: ida_idaapi.ea_t) -> netnode

.. py:function:: get_strid(ea: ida_idaapi.ea_t) -> tid_t

.. py:data:: AFL_LINNUM

   has line number info


.. py:data:: AFL_USERSP

   user-defined SP value


.. py:data:: AFL_PUBNAM

   name is public (inter-file linkage)


.. py:data:: AFL_WEAKNAM

   name is weak


.. py:data:: AFL_HIDDEN

   the item is hidden completely


.. py:data:: AFL_MANUAL

   the instruction/data is specified by the user


.. py:data:: AFL_NOBRD

   the code/data border is hidden


.. py:data:: AFL_ZSTROFF

   display struct field name at 0 offset when displaying an offset. example: `offset somestruct.field_0 ` if this flag is clear, then `offset somestruct ` 
           


.. py:data:: AFL_BNOT0

   the 1st operand is bitwise negated


.. py:data:: AFL_BNOT1

   the 2nd operand is bitwise negated


.. py:data:: AFL_LIB

   item from the standard library. low level flag, is used to set FUNC_LIB of func_t 
           


.. py:data:: AFL_TI

   has typeinfo? (NSUP_TYPEINFO); used only for addresses, not for member_t


.. py:data:: AFL_TI0

   has typeinfo for operand 0? (NSUP_OPTYPES)


.. py:data:: AFL_TI1

   has typeinfo for operand 1? (NSUP_OPTYPES+1)


.. py:data:: AFL_LNAME

   has local name too (FF_NAME should be set)


.. py:data:: AFL_TILCMT

   has type comment? (such a comment may be changed by IDA)


.. py:data:: AFL_LZERO0

   toggle leading zeroes for the 1st operand


.. py:data:: AFL_LZERO1

   toggle leading zeroes for the 2nd operand


.. py:data:: AFL_COLORED

   has user defined instruction color?


.. py:data:: AFL_TERSESTR

   terse structure variable display?


.. py:data:: AFL_SIGN0

   code: toggle sign of the 1st operand


.. py:data:: AFL_SIGN1

   code: toggle sign of the 2nd operand


.. py:data:: AFL_NORET

   for imported function pointers: doesn't return. this flag can also be used for any instruction which halts or finishes the program execution 
           


.. py:data:: AFL_FIXEDSPD

   sp delta value is fixed by analysis. should not be modified by modules 
           


.. py:data:: AFL_ALIGNFLOW

   the previous insn was created for alignment purposes only


.. py:data:: AFL_USERTI

   the type information is definitive. (comes from the user or type library) if not set see AFL_TYPE_GUESSED 
           


.. py:data:: AFL_RETFP

   function returns a floating point value


.. py:data:: AFL_USEMODSP

   insn modifes SP and uses the modified value; example: pop [rsp+N] 
           


.. py:data:: AFL_NOTCODE

   autoanalysis should not create code here


.. py:data:: AFL_NOTPROC

   autoanalysis should not create proc here


.. py:data:: AFL_TYPE_GUESSED

   who guessed the type information?


.. py:data:: AFL_IDA_GUESSED

   the type is guessed by IDA


.. py:data:: AFL_HR_GUESSED_FUNC

   the function type is guessed by the decompiler


.. py:data:: AFL_HR_GUESSED_DATA

   the data type is guessed by the decompiler


.. py:data:: AFL_HR_DETERMINED

   the type is definitely guessed by the decompiler


.. py:function:: set_aflags(ea: ida_idaapi.ea_t, flags: aflags_t) -> None

.. py:function:: upd_abits(ea: ida_idaapi.ea_t, clr_bits: aflags_t, set_bits: aflags_t) -> None

.. py:function:: set_abits(ea: ida_idaapi.ea_t, bits: aflags_t) -> None

.. py:function:: clr_abits(ea: ida_idaapi.ea_t, bits: aflags_t) -> None

.. py:function:: get_aflags(ea: ida_idaapi.ea_t) -> aflags_t

.. py:function:: del_aflags(ea: ida_idaapi.ea_t) -> None

.. py:function:: has_aflag_linnum(flags: aflags_t) -> bool

.. py:function:: is_aflag_usersp(flags: aflags_t) -> bool

.. py:function:: is_aflag_public_name(flags: aflags_t) -> bool

.. py:function:: is_aflag_weak_name(flags: aflags_t) -> bool

.. py:function:: is_aflag_hidden_item(flags: aflags_t) -> bool

.. py:function:: is_aflag_manual_insn(flags: aflags_t) -> bool

.. py:function:: is_aflag_hidden_border(flags: aflags_t) -> bool

.. py:function:: is_aflag_zstroff(flags: aflags_t) -> bool

.. py:function:: is_aflag__bnot0(flags: aflags_t) -> bool

.. py:function:: is_aflag__bnot1(flags: aflags_t) -> bool

.. py:function:: is_aflag_libitem(flags: aflags_t) -> bool

.. py:function:: has_aflag_ti(flags: aflags_t) -> bool

.. py:function:: has_aflag_ti0(flags: aflags_t) -> bool

.. py:function:: has_aflag_ti1(flags: aflags_t) -> bool

.. py:function:: has_aflag_lname(flags: aflags_t) -> bool

.. py:function:: is_aflag_tilcmt(flags: aflags_t) -> bool

.. py:function:: is_aflag_lzero0(flags: aflags_t) -> bool

.. py:function:: is_aflag_lzero1(flags: aflags_t) -> bool

.. py:function:: is_aflag_colored_item(flags: aflags_t) -> bool

.. py:function:: is_aflag_terse_struc(flags: aflags_t) -> bool

.. py:function:: is_aflag__invsign0(flags: aflags_t) -> bool

.. py:function:: is_aflag__invsign1(flags: aflags_t) -> bool

.. py:function:: is_aflag_noret(flags: aflags_t) -> bool

.. py:function:: is_aflag_fixed_spd(flags: aflags_t) -> bool

.. py:function:: is_aflag_align_flow(flags: aflags_t) -> bool

.. py:function:: is_aflag_userti(flags: aflags_t) -> bool

.. py:function:: is_aflag_retfp(flags: aflags_t) -> bool

.. py:function:: uses_aflag_modsp(flags: aflags_t) -> bool

.. py:function:: is_aflag_notcode(flags: aflags_t) -> bool

.. py:function:: is_aflag_notproc(flags: aflags_t) -> bool

.. py:function:: is_aflag_type_guessed_by_ida(flags: aflags_t) -> bool

.. py:function:: is_aflag_func_guessed_by_hexrays(flags: aflags_t) -> bool

.. py:function:: is_aflag_data_guessed_by_hexrays(flags: aflags_t) -> bool

.. py:function:: is_aflag_type_determined_by_hexrays(flags: aflags_t) -> bool

.. py:function:: is_aflag_type_guessed_by_hexrays(flags: aflags_t) -> bool

.. py:function:: is_hidden_item(ea: ida_idaapi.ea_t) -> bool

.. py:function:: hide_item(ea: ida_idaapi.ea_t) -> None

.. py:function:: unhide_item(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_hidden_border(ea: ida_idaapi.ea_t) -> bool

.. py:function:: hide_border(ea: ida_idaapi.ea_t) -> None

.. py:function:: unhide_border(ea: ida_idaapi.ea_t) -> None

.. py:function:: uses_modsp(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_usemodsp(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_usemodsp(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_zstroff(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_zstroff(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_zstroff(ea: ida_idaapi.ea_t) -> None

.. py:function:: is__bnot0(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set__bnot0(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr__bnot0(ea: ida_idaapi.ea_t) -> None

.. py:function:: is__bnot1(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set__bnot1(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr__bnot1(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_libitem(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_libitem(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_libitem(ea: ida_idaapi.ea_t) -> None

.. py:function:: has_ti(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_has_ti(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_has_ti(ea: ida_idaapi.ea_t) -> None

.. py:function:: has_ti0(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_has_ti0(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_has_ti0(ea: ida_idaapi.ea_t) -> None

.. py:function:: has_ti1(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_has_ti1(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_has_ti1(ea: ida_idaapi.ea_t) -> None

.. py:function:: has_lname(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_has_lname(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_has_lname(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_tilcmt(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_tilcmt(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_tilcmt(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_usersp(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_usersp(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_usersp(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_lzero0(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_lzero0(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_lzero0(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_lzero1(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_lzero1(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_lzero1(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_colored_item(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_colored_item(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_colored_item(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_terse_struc(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_terse_struc(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_terse_struc(ea: ida_idaapi.ea_t) -> None

.. py:function:: is__invsign0(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set__invsign0(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr__invsign0(ea: ida_idaapi.ea_t) -> None

.. py:function:: is__invsign1(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set__invsign1(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr__invsign1(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_noret(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_noret(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_noret(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_fixed_spd(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_fixed_spd(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_fixed_spd(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_align_flow(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_align_flow(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_align_flow(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_userti(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_userti(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_userti(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_retfp(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_retfp(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_retfp(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_notproc(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_notproc(ea: ida_idaapi.ea_t) -> None

.. py:function:: clr_notproc(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_type_guessed_by_ida(ea: ida_idaapi.ea_t) -> bool

.. py:function:: is_func_guessed_by_hexrays(ea: ida_idaapi.ea_t) -> bool

.. py:function:: is_data_guessed_by_hexrays(ea: ida_idaapi.ea_t) -> bool

.. py:function:: is_type_determined_by_hexrays(ea: ida_idaapi.ea_t) -> bool

.. py:function:: is_type_guessed_by_hexrays(ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_type_guessed_by_ida(ea: ida_idaapi.ea_t) -> None

.. py:function:: set_func_guessed_by_hexrays(ea: ida_idaapi.ea_t) -> None

.. py:function:: set_data_guessed_by_hexrays(ea: ida_idaapi.ea_t) -> None

.. py:function:: set_type_determined_by_hexrays(ea: ida_idaapi.ea_t) -> None

.. py:function:: set_notcode(ea: ida_idaapi.ea_t) -> None

   Mark address so that it cannot be converted to instruction.


.. py:function:: clr_notcode(ea: ida_idaapi.ea_t) -> None

   Clear not-code mark.


.. py:function:: is_notcode(ea: ida_idaapi.ea_t) -> bool

   Is the address marked as not-code?


.. py:function:: set_visible_item(ea: ida_idaapi.ea_t, visible: bool) -> None

   Change visibility of item at given ea.


.. py:function:: is_visible_item(ea: ida_idaapi.ea_t) -> bool

   Test visibility of item at given ea.


.. py:function:: is_finally_visible_item(ea: ida_idaapi.ea_t) -> bool

   Is instruction visible?


.. py:function:: set_source_linnum(ea: ida_idaapi.ea_t, lnnum: int) -> None

.. py:function:: get_source_linnum(ea: ida_idaapi.ea_t) -> int

.. py:function:: del_source_linnum(ea: ida_idaapi.ea_t) -> None

.. py:function:: get_absbase(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

.. py:function:: set_absbase(ea: ida_idaapi.ea_t, x: ida_idaapi.ea_t) -> None

.. py:function:: del_absbase(ea: ida_idaapi.ea_t) -> None

.. py:function:: get_ind_purged(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

.. py:function:: del_ind_purged(ea: ida_idaapi.ea_t) -> None

.. py:function:: get_str_type(ea: ida_idaapi.ea_t) -> int

.. py:function:: set_str_type(ea: ida_idaapi.ea_t, x: int) -> None

.. py:function:: del_str_type(ea: ida_idaapi.ea_t) -> None

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

   C-style string.


.. py:data:: STRTYPE_C

   Zero-terminated 16bit chars.


.. py:data:: STRTYPE_C_16

   Zero-terminated 32bit chars.


.. py:data:: STRTYPE_C_32

   Pascal-style, one-byte length prefix.


.. py:data:: STRTYPE_PASCAL

   Pascal-style, 16bit chars, one-byte length prefix.


.. py:data:: STRTYPE_PASCAL_16

   Pascal-style, 32bit chars, one-byte length prefix.


.. py:data:: STRTYPE_PASCAL_32

   Pascal-style, two-byte length prefix.


.. py:data:: STRTYPE_LEN2

   Pascal-style, 16bit chars, two-byte length prefix.


.. py:data:: STRTYPE_LEN2_16

   Pascal-style, 32bit chars, two-byte length prefix.


.. py:data:: STRTYPE_LEN2_32

   Pascal-style, four-byte length prefix.


.. py:data:: STRTYPE_LEN4

   Pascal-style, 16bit chars, four-byte length prefix.


.. py:data:: STRTYPE_LEN4_16

   Pascal-style, 32bit chars, four-byte length prefix.


.. py:data:: STRTYPE_LEN4_32

.. py:function:: get_str_type_code(strtype: int) -> uchar

.. py:function:: get_str_term1(strtype: int) -> char

.. py:function:: get_str_term2(strtype: int) -> char

.. py:function:: get_str_encoding_idx(strtype: int) -> uchar

.. py:function:: set_str_encoding_idx(strtype: int, encoding_idx: int) -> int

.. py:function:: make_str_type(type_code: uchar, encoding_idx: int, term1: uchar = 0, term2: uchar = 0) -> int

.. py:function:: is_pascal(strtype: int) -> bool

.. py:function:: get_str_type_prefix_length(strtype: int) -> size_t

.. py:data:: STRENC_DEFAULT

   use default encoding for this type (see get_default_encoding_idx())


.. py:data:: STRENC_NONE

   force no-conversion encoding


.. py:function:: get_alignment(ea: ida_idaapi.ea_t) -> int

.. py:function:: set_alignment(ea: ida_idaapi.ea_t, x: int) -> None

.. py:function:: del_alignment(ea: ida_idaapi.ea_t) -> None

.. py:function:: set_item_color(ea: ida_idaapi.ea_t, color: bgcolor_t) -> None

.. py:function:: get_item_color(ea: ida_idaapi.ea_t) -> bgcolor_t

.. py:function:: del_item_color(ea: ida_idaapi.ea_t) -> bool

.. py:class:: array_parameters_t(_f: int = 1, _l: int = 0, _a: int = -1)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: flags
      :type:  int


   .. py:attribute:: lineitems
      :type:  int

      number of items on a line



   .. py:attribute:: alignment
      :type:  int

      -1 - don't align. 0 - align automatically. else item width 
              



   .. py:method:: is_default() -> bool


.. py:data:: AP_ALLOWDUPS

   use 'dup' construct


.. py:data:: AP_SIGNED

   treats numbers as signed


.. py:data:: AP_INDEX

   display array element indexes as comments


.. py:data:: AP_ARRAY

   create as array (this flag is not stored in database)


.. py:data:: AP_IDXBASEMASK

   mask for number base of the indexes


.. py:data:: AP_IDXDEC

   display indexes in decimal


.. py:data:: AP_IDXHEX

   display indexes in hex


.. py:data:: AP_IDXOCT

   display indexes in octal


.. py:data:: AP_IDXBIN

   display indexes in binary


.. py:function:: get_array_parameters(out: array_parameters_t, ea: ida_idaapi.ea_t) -> ssize_t

.. py:function:: set_array_parameters(ea: ida_idaapi.ea_t, _in: array_parameters_t) -> None

.. py:function:: del_array_parameters(ea: ida_idaapi.ea_t) -> None

.. py:class:: switch_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: flags
      :type:  int

      Switch info flags 
              



   .. py:method:: get_shift() -> int

      See SWI_SHIFT_MASK. possible answers: 0..3. 
              



   .. py:method:: set_shift(shift: int) -> None

      See SWI_SHIFT_MASK.



   .. py:method:: get_jtable_element_size() -> int


   .. py:method:: set_jtable_element_size(size: int) -> None


   .. py:method:: get_vtable_element_size() -> int


   .. py:method:: set_vtable_element_size(size: int) -> None


   .. py:method:: has_default() -> bool


   .. py:method:: has_elbase() -> bool


   .. py:method:: is_sparse() -> bool


   .. py:method:: is_custom() -> bool


   .. py:method:: is_indirect() -> bool


   .. py:method:: is_subtract() -> bool


   .. py:method:: is_nolowcase() -> bool


   .. py:method:: use_std_table() -> bool


   .. py:method:: is_user_defined() -> bool


   .. py:attribute:: ncases
      :type:  ushort

      number of cases (excluding default)



   .. py:attribute:: jumps
      :type:  ida_idaapi.ea_t

      jump table start address



   .. py:attribute:: values
      :type:  ida_idaapi.ea_t

      values table address (if SWI_SPARSE is set)



   .. py:attribute:: lowcase
      :type:  int

      the lowest value in cases



   .. py:attribute:: defjump
      :type:  ida_idaapi.ea_t

      default jump address (BADADDR if no default case)



   .. py:attribute:: startea
      :type:  ida_idaapi.ea_t

      start of the switch idiom



   .. py:attribute:: jcases
      :type:  int

      number of entries in the jump table (SWI_INDIRECT)



   .. py:attribute:: ind_lowcase
      :type:  int


   .. py:method:: get_lowcase() -> int


   .. py:attribute:: elbase
      :type:  ida_idaapi.ea_t

      element base



   .. py:attribute:: regnum
      :type:  int

      the switch expression as a value of the REGNUM register before the instruction at EXPR_EA. -1 means 'unknown' 
              



   .. py:attribute:: regdtype
      :type:  op_dtype_t

      size of the switch expression register as dtype



   .. py:method:: get_jtable_size() -> int


   .. py:method:: set_jtable_size(size: int) -> None


   .. py:method:: set_elbase(base: ida_idaapi.ea_t) -> None


   .. py:method:: set_expr(r: int, dt: op_dtype_t) -> None


   .. py:method:: get_jrange_vrange(jrange: range_t = None, vrange: range_t = None) -> bool

      get separate parts of the switch



   .. py:attribute:: custom
      :type:  int

      information for custom tables (filled and used by modules)



   .. py:attribute:: SWITCH_INFO_VERSION


   .. py:method:: get_version() -> int


   .. py:attribute:: expr_ea
      :type:  ida_idaapi.ea_t

      the address before that the switch expression is in REGNUM. If BADADDR, then the first insn marked as IM_SWITCH after STARTEA is used. 
              



   .. py:attribute:: marks
      :type:  eavec_t

      the insns marked as IM_SWITCH. They are used to delete the switch.



   .. py:method:: clear() -> None


   .. py:method:: assign(other: switch_info_t) -> None


.. py:data:: SWI_SPARSE

   sparse switch (value table present), otherwise lowcase present 
           


.. py:data:: SWI_V32

   32-bit values in table


.. py:data:: SWI_J32

   32-bit jump offsets


.. py:data:: SWI_VSPLIT

   value table is split (only for 32-bit values)


.. py:data:: SWI_USER

   user specified switch (starting from version 2)


.. py:data:: SWI_DEF_IN_TBL

   default case is an entry in the jump table. This flag is applicable in 2 cases:
   * The sparse indirect switch (i.e. a switch with a values table) {jump table size} == {value table size} + 1. The default case entry is the last one in the table (or the first one in the case of an inversed jump table).
   * The switch with insns in the jump table. The default case entry is before the first entry of the table. 
    See also the find_defjump_from_table() helper function. 


           


.. py:data:: SWI_JMP_INV

   jumptable is inversed. (last entry is for first entry in values table) 
           


.. py:data:: SWI_SHIFT_MASK

   use formula (element<<shift) + elbase to find jump targets


.. py:data:: SWI_ELBASE

   elbase is present (otherwise the base of the switch segment will be used) 
           


.. py:data:: SWI_JSIZE

   jump offset expansion bit


.. py:data:: SWI_VSIZE

   value table element size expansion bit


.. py:data:: SWI_SEPARATE

   create an array of individual elements (otherwise separate items)


.. py:data:: SWI_SIGNED

   jump table entries are signed


.. py:data:: SWI_CUSTOM

   custom jump table. processor_t::create_switch_xrefs will be called to create code xrefs for the table. Custom jump table must be created by the module (see also SWI_STDTBL) 
           


.. py:data:: SWI_INDIRECT

   value table elements are used as indexes into the jump table (for sparse switches) 
           


.. py:data:: SWI_SUBTRACT

   table values are subtracted from the elbase instead of being added


.. py:data:: SWI_HXNOLOWCASE

   lowcase value should not be used by the decompiler (internal flag)


.. py:data:: SWI_STDTBL

   custom jump table with standard table formatting. ATM IDA doesn't use SWI_CUSTOM for switches with standard table formatting. So this flag can be considered as obsolete. 
           


.. py:data:: SWI_DEFRET

   return in the default case (defjump==BADADDR)


.. py:data:: SWI_SELFREL

   jump address is relative to the element not to ELBASE


.. py:data:: SWI_JMPINSN

   jump table entries are insns. For such entries SHIFT has a different meaning. It denotes the number of insns in the entry. For example, 0 - the entry contains the jump to the case, 1 - the entry contains one insn like a 'mov' and jump to the end of case, and so on. 
           


.. py:data:: SWI_VERSION

   the structure contains the VERSION member


.. py:function:: get_switch_info(out: switch_info_t, ea: ida_idaapi.ea_t) -> ssize_t

.. py:function:: set_switch_info(ea: ida_idaapi.ea_t, _in: switch_info_t) -> None

.. py:function:: del_switch_info(ea: ida_idaapi.ea_t) -> None

.. py:function:: get_switch_parent(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

.. py:function:: set_switch_parent(ea: ida_idaapi.ea_t, x: ida_idaapi.ea_t) -> None

.. py:function:: del_switch_parent(ea: ida_idaapi.ea_t) -> None

.. py:class:: custom_data_type_ids_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: dtid
      :type:  int16

      data type id



   .. py:attribute:: fids
      :type:  int16 [8]

      data format ids



   .. py:method:: set(tid: tid_t) -> None


   .. py:method:: get_dtid() -> tid_t


.. py:function:: get_custom_data_type_ids(cdis: custom_data_type_ids_t, ea: ida_idaapi.ea_t) -> int

.. py:function:: set_custom_data_type_ids(ea: ida_idaapi.ea_t, cdis: custom_data_type_ids_t) -> None

.. py:function:: del_custom_data_type_ids(ea: ida_idaapi.ea_t) -> None

.. py:function:: is_reftype_target_optional(type: reftype_t) -> bool

   Can the target be calculated using operand value?


.. py:function:: get_reftype_by_size(size: size_t) -> reftype_t

   Get REF_... constant from size Supported sizes: 1,2,4,8,16 For other sizes returns reftype_t(-1) 
           


.. py:class:: refinfo_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: target
      :type:  ida_idaapi.ea_t

      reference target (BADADDR-none)



   .. py:attribute:: base
      :type:  ida_idaapi.ea_t

      base of reference (may be BADADDR)



   .. py:attribute:: tdelta
      :type:  adiff_t

      offset from the target



   .. py:attribute:: flags
      :type:  int

      Reference info flags 
              



   .. py:method:: type() -> reftype_t


   .. py:method:: is_target_optional() -> bool

      < is_reftype_target_optional()



   .. py:method:: no_base_xref() -> bool


   .. py:method:: is_pastend() -> bool


   .. py:method:: is_rvaoff() -> bool


   .. py:method:: is_custom() -> bool


   .. py:method:: is_subtract() -> bool


   .. py:method:: is_signed() -> bool


   .. py:method:: is_no_zeros() -> bool


   .. py:method:: is_no_ones() -> bool


   .. py:method:: is_selfref() -> bool


   .. py:method:: set_type(rt: reftype_t) -> None


   .. py:method:: init(*args) -> None


.. py:data:: cvar

.. py:data:: V695_REF_OFF8

   reserved


.. py:data:: REF_OFF16

   16bit full offset


.. py:data:: REF_OFF32

   32bit full offset


.. py:data:: REF_LOW8

   low 8bits of 16bit offset


.. py:data:: REF_LOW16

   low 16bits of 32bit offset


.. py:data:: REF_HIGH8

   high 8bits of 16bit offset


.. py:data:: REF_HIGH16

   high 16bits of 32bit offset


.. py:data:: V695_REF_VHIGH

   obsolete


.. py:data:: V695_REF_VLOW

   obsolete


.. py:data:: REF_OFF64

   64bit full offset


.. py:data:: REF_OFF8

   8bit full offset


.. py:data:: REF_LAST

.. py:data:: REFINFO_TYPE

   reference type (reftype_t), or custom reference ID if REFINFO_CUSTOM set 
           


.. py:data:: REFINFO_RVAOFF

   based reference (rva); refinfo_t::base will be forced to get_imagebase(); such a reference is displayed with the asm_t::a_rva keyword 
           


.. py:data:: REFINFO_PASTEND

   reference past an item; it may point to an nonexistent address; do not destroy alignment dirs 
           


.. py:data:: REFINFO_CUSTOM

   a custom reference. see custom_refinfo_handler_t. the id of the custom refinfo is stored under the REFINFO_TYPE mask. 
           


.. py:data:: REFINFO_NOBASE

   don't create the base xref; implies that the base can be any value. nb: base xrefs are created only if the offset base points to the middle of a segment 
           


.. py:data:: REFINFO_SUBTRACT

   the reference value is subtracted from the base value instead of (as usual) being added to it


.. py:data:: REFINFO_SIGNEDOP

   the operand value is sign-extended (only supported for REF_OFF8/16/32/64)


.. py:data:: REFINFO_NO_ZEROS

   an opval of 0 will be considered invalid


.. py:data:: REFINFO_NO_ONES

   an opval of ~0 will be considered invalid


.. py:data:: REFINFO_SELFREF

   the self-based reference; refinfo_t::base will be forced to the reference address 
           


.. py:function:: find_custom_refinfo(name: str) -> int

   Get id of a custom refinfo type.


.. py:function:: get_custom_refinfo(crid: int) -> custom_refinfo_handler_t const *

   Get definition of a registered custom refinfo type.


.. py:data:: MAXSTRUCPATH

   maximal inclusion depth of unions


.. py:class:: strpath_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: len
      :type:  int


   .. py:attribute:: ids
      :type:  tid_t [32]


   .. py:attribute:: delta
      :type:  adiff_t


.. py:class:: enum_const_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: tid
      :type:  tid_t


   .. py:attribute:: serial
      :type:  uchar


.. py:class:: opinfo_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ri
      :type:  refinfo_t

      for offset members



   .. py:attribute:: tid
      :type:  tid_t

      for struct, etc. members



   .. py:attribute:: path
      :type:  strpath_t

      for stroff



   .. py:attribute:: strtype
      :type:  int

      for strings (String type codes)



   .. py:attribute:: ec
      :type:  enum_const_t

      for enums



   .. py:attribute:: cd
      :type:  custom_data_type_ids_t

      for custom data



.. py:class:: printop_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: ti
      :type:  opinfo_t


   .. py:attribute:: features
      :type:  uchar


   .. py:attribute:: suspop
      :type:  int


   .. py:attribute:: aflags
      :type:  aflags_t


   .. py:attribute:: flags
      :type:  flags64_t


   .. py:method:: is_ti_initialized() -> bool


   .. py:method:: set_ti_initialized(v: bool = True) -> None


   .. py:method:: is_aflags_initialized() -> bool


   .. py:method:: set_aflags_initialized(v: bool = True) -> None


   .. py:method:: is_f64() -> bool


   .. py:method:: get_ti() -> opinfo_t const *


   .. py:attribute:: is_ti_valid


.. py:data:: POF_VALID_TI

.. py:data:: POF_VALID_AFLAGS

.. py:data:: POF_IS_F64

.. py:function:: set_refinfo_ex(ea: ida_idaapi.ea_t, n: int, ri: refinfo_t) -> bool

.. py:function:: set_refinfo(*args) -> bool

.. py:function:: get_refinfo(ri: refinfo_t, ea: ida_idaapi.ea_t, n: int) -> bool

.. py:function:: del_refinfo(ea: ida_idaapi.ea_t, n: int) -> bool

.. py:function:: get_tinfo(tif: tinfo_t, ea: ida_idaapi.ea_t) -> bool

.. py:function:: set_tinfo(ea: ida_idaapi.ea_t, tif: tinfo_t) -> bool

.. py:function:: del_tinfo(ea: ida_idaapi.ea_t) -> None

.. py:function:: get_op_tinfo(tif: tinfo_t, ea: ida_idaapi.ea_t, n: int) -> bool

.. py:function:: set_op_tinfo(ea: ida_idaapi.ea_t, n: int, tif: tinfo_t) -> bool

.. py:function:: del_op_tinfo(ea: ida_idaapi.ea_t, n: int) -> None

.. py:data:: RIDX_FILE_FORMAT_NAME

   file format name for loader modules


.. py:data:: RIDX_SELECTORS

   2..63 are for selector_t blob (see init_selectors())


.. py:data:: RIDX_GROUPS

   segment group information (see init_groups())


.. py:data:: RIDX_H_PATH

   C header path.


.. py:data:: RIDX_C_MACROS

   C predefined macros.


.. py:data:: RIDX_SMALL_IDC_OLD

   Instant IDC statements (obsolete)


.. py:data:: RIDX_NOTEPAD

   notepad blob, occupies 1000 indexes (1MB of text)


.. py:data:: RIDX_INCLUDE

   assembler include file name


.. py:data:: RIDX_SMALL_IDC

   Instant IDC statements, blob.


.. py:data:: RIDX_DUALOP_GRAPH

   Graph text representation options.


.. py:data:: RIDX_DUALOP_TEXT

   Text text representation options.


.. py:data:: RIDX_MD5

   MD5 of the input file.


.. py:data:: RIDX_IDA_VERSION

   version of ida which created the database


.. py:data:: RIDX_STR_ENCODINGS

   a list of encodings for the program strings


.. py:data:: RIDX_SRCDBG_PATHS

   source debug paths, occupies 20 indexes


.. py:data:: RIDX_DBG_BINPATHS

   unused (20 indexes)


.. py:data:: RIDX_SHA256

   SHA256 of the input file.


.. py:data:: RIDX_ABINAME

   ABI name (processor specific)


.. py:data:: RIDX_ARCHIVE_PATH

   archive file path


.. py:data:: RIDX_PROBLEMS

   problem lists


.. py:data:: RIDX_SRCDBG_UNDESIRED

   user-closed source files, occupies 20 indexes


.. py:function:: get_root_filename() -> str

   Get file name only of the input file.


.. py:function:: dbg_get_input_path() -> str

   Get debugger input file name/path (see LFLG_DBG_NOPATH)


.. py:function:: get_input_file_path() -> str

   Get full path of the input file.


.. py:function:: set_root_filename(file: str) -> None

   Set full path of the input file.


.. py:function:: retrieve_input_file_size() -> size_t

   Get size of input file in bytes.


.. py:function:: retrieve_input_file_crc32() -> int

   Get input file crc32 stored in the database. it can be used to check that the input file has not been changed. 
           


.. py:function:: retrieve_input_file_md5() -> bytes

   Get input file md5.


.. py:function:: retrieve_input_file_sha256() -> bytes

   Get input file sha256.


.. py:function:: get_asm_inc_file() -> str

   Get name of the include file.


.. py:function:: set_asm_inc_file(file: str) -> bool

   Set name of the include file.


.. py:function:: get_imagebase() -> ida_idaapi.ea_t

   Get image base address.


.. py:function:: set_imagebase(base: ida_idaapi.ea_t) -> None

   Set image base address.


.. py:function:: get_ids_modnode() -> netnode

   Get ids modnode.


.. py:function:: set_ids_modnode(id: netnode) -> None

   Set ids modnode.


.. py:function:: get_archive_path() -> str

   Get archive file path from which input file was extracted.


.. py:function:: set_archive_path(file: str) -> bool

   Set archive file path from which input file was extracted.


.. py:function:: get_loader_format_name() -> str

   Get file format name for loader modules.


.. py:function:: set_loader_format_name(name: str) -> None

   Set file format name for loader modules.


.. py:function:: get_initial_ida_version() -> str

   Get version of ida which created the database (string format like "7.5")


.. py:function:: get_ida_notepad_text() -> str

   Get notepad text.


.. py:function:: set_ida_notepad_text(text: str, size: size_t = 0) -> None

   Set notepad text.


.. py:function:: get_srcdbg_paths() -> str

   Get source debug paths.


.. py:function:: set_srcdbg_paths(paths: str) -> None

   Set source debug paths.


.. py:function:: get_srcdbg_undesired_paths() -> str

   Get user-closed source files.


.. py:function:: set_srcdbg_undesired_paths(paths: str) -> None

   Set user-closed source files.


.. py:function:: get_initial_idb_version() -> ushort

   Get initial version of the database (numeric format like 700)


.. py:function:: get_idb_ctime() -> time_t

   Get database creation timestamp.


.. py:function:: get_elapsed_secs() -> size_t

   Get seconds database stayed open.


.. py:function:: get_idb_nopens() -> size_t

   Get number of times the database is opened.


.. py:function:: get_encoding_qty() -> int

.. py:function:: get_encoding_name(idx: int) -> str

.. py:function:: add_encoding(encname: str) -> int

.. py:function:: del_encoding(idx: int) -> bool

.. py:function:: rename_encoding(idx: int, encname: str) -> bool

.. py:data:: BPU_1B

.. py:data:: BPU_2B

.. py:data:: BPU_4B

.. py:function:: get_encoding_bpu(idx: int) -> int

.. py:function:: get_encoding_bpu_by_name(encname: str) -> int

.. py:function:: get_strtype_bpu(strtype: int) -> int

.. py:function:: get_default_encoding_idx(bpu: int) -> int

.. py:function:: set_default_encoding_idx(bpu: int, idx: int) -> bool

.. py:function:: encoding_from_strtype(strtype: int) -> str

.. py:function:: get_outfile_encoding_idx() -> int

.. py:function:: set_outfile_encoding_idx(idx: int) -> bool

.. py:function:: get_import_module_qty() -> uint

.. py:function:: delete_imports() -> None

.. py:data:: GOTEA_NODE_NAME

   node containing address of .got section


.. py:data:: GOTEA_NODE_IDX

.. py:function:: set_gotea(gotea: ida_idaapi.ea_t) -> None

.. py:function:: get_gotea() -> ida_idaapi.ea_t

.. py:function:: get_import_module_name(mod_index)

   Returns the name of an imported module given its index

   :param mod_index: the module index
   :returns: None or the module name


.. py:function:: enum_import_names(mod_index, callback)

   Enumerate imports from a specific module.
   Please refer to list_imports.py example.

   :param mod_index: The module index
   :param callback: A callable object that will be invoked with an ea, name (could be None) and ordinal.
   :returns: 1-finished ok, -1 on error, otherwise callback return value (<=0)


.. py:function:: switch_info_t__from_ptrval__(ptrval: size_t) -> switch_info_t *

.. py:function:: get_switch_info(*args)

.. py:function:: get_abi_name()

.. py:data:: get_initial_version


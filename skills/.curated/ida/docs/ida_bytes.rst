ida_bytes
=========

.. py:module:: ida_bytes

.. autoapi-nested-parse::

   Contains functions that deal with individual byte characteristics.

   Each byte of the disassembled program is represented by a 32-bit value. We will 
   call this value 'flags'. The structure of the flags is here.

   You are not allowed to inspect individual bits of flags and modify them directly. 
   Use special functions to inspect and/or modify flags.

   Flags are kept in a virtual array file (*.id1). Addresses (ea) are all 32-bit 
   (or 64-bit) quantities.

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For byte-level operations, see :mod:`ida_domain.bytes`.



Attributes
----------

.. autoapisummary::

   ida_bytes.ITEM_END_FIXUP
   ida_bytes.ITEM_END_INITED
   ida_bytes.ITEM_END_NAME
   ida_bytes.ITEM_END_XREF
   ida_bytes.ITEM_END_CANCEL
   ida_bytes.GFE_VALUE
   ida_bytes.GFE_IDB_VALUE
   ida_bytes.GFE_32BIT
   ida_bytes.MS_VAL
   ida_bytes.FF_IVL
   ida_bytes.GMB_READALL
   ida_bytes.GMB_WAITBOX
   ida_bytes.MS_CLS
   ida_bytes.FF_CODE
   ida_bytes.FF_DATA
   ida_bytes.FF_TAIL
   ida_bytes.FF_UNK
   ida_bytes.DELIT_SIMPLE
   ida_bytes.DELIT_EXPAND
   ida_bytes.DELIT_DELNAMES
   ida_bytes.DELIT_NOTRUNC
   ida_bytes.DELIT_NOUNAME
   ida_bytes.DELIT_NOCMT
   ida_bytes.DELIT_KEEPFUNC
   ida_bytes.MS_COMM
   ida_bytes.FF_COMM
   ida_bytes.FF_REF
   ida_bytes.FF_LINE
   ida_bytes.FF_NAME
   ida_bytes.FF_LABL
   ida_bytes.FF_FLOW
   ida_bytes.FF_SIGN
   ida_bytes.FF_BNOT
   ida_bytes.FF_UNUSED
   ida_bytes.FF_ANYNAME
   ida_bytes.MS_N_TYPE
   ida_bytes.FF_N_VOID
   ida_bytes.FF_N_NUMH
   ida_bytes.FF_N_NUMD
   ida_bytes.FF_N_CHAR
   ida_bytes.FF_N_SEG
   ida_bytes.FF_N_OFF
   ida_bytes.FF_N_NUMB
   ida_bytes.FF_N_NUMO
   ida_bytes.FF_N_ENUM
   ida_bytes.FF_N_FOP
   ida_bytes.FF_N_STRO
   ida_bytes.FF_N_STK
   ida_bytes.FF_N_FLT
   ida_bytes.FF_N_CUST
   ida_bytes.OPND_OUTER
   ida_bytes.OPND_MASK
   ida_bytes.OPND_ALL
   ida_bytes.DT_TYPE
   ida_bytes.FF_BYTE
   ida_bytes.FF_WORD
   ida_bytes.FF_DWORD
   ida_bytes.FF_QWORD
   ida_bytes.FF_TBYTE
   ida_bytes.FF_STRLIT
   ida_bytes.FF_STRUCT
   ida_bytes.FF_OWORD
   ida_bytes.FF_FLOAT
   ida_bytes.FF_DOUBLE
   ida_bytes.FF_PACKREAL
   ida_bytes.FF_ALIGN
   ida_bytes.FF_CUSTOM
   ida_bytes.FF_YWORD
   ida_bytes.FF_ZWORD
   ida_bytes.ALOPT_IGNHEADS
   ida_bytes.ALOPT_IGNPRINT
   ida_bytes.ALOPT_IGNCLT
   ida_bytes.ALOPT_MAX4K
   ida_bytes.ALOPT_ONLYTERM
   ida_bytes.ALOPT_APPEND
   ida_bytes.STRCONV_ESCAPE
   ida_bytes.STRCONV_REPLCHAR
   ida_bytes.STRCONV_INCLLEN
   ida_bytes.PSTF_TNORM
   ida_bytes.PSTF_TBRIEF
   ida_bytes.PSTF_TINLIN
   ida_bytes.PSTF_TMASK
   ida_bytes.PSTF_HOTKEY
   ida_bytes.PSTF_ENC
   ida_bytes.PSTF_ONLY_ENC
   ida_bytes.PSTF_ATTRIB
   ida_bytes.MS_CODE
   ida_bytes.FF_FUNC
   ida_bytes.FF_IMMD
   ida_bytes.FF_JUMP
   ida_bytes.DTP_NODUP
   ida_bytes.PBSENC_DEF1BPU
   ida_bytes.PBSENC_ALL
   ida_bytes.BIN_SEARCH_CASE
   ida_bytes.BIN_SEARCH_NOCASE
   ida_bytes.BIN_SEARCH_NOBREAK
   ida_bytes.BIN_SEARCH_INITED
   ida_bytes.BIN_SEARCH_NOSHOW
   ida_bytes.BIN_SEARCH_FORWARD
   ida_bytes.BIN_SEARCH_BACKWARD
   ida_bytes.BIN_SEARCH_BITMASK
   ida_bytes.MS_0TYPE
   ida_bytes.FF_0VOID
   ida_bytes.FF_0NUMH
   ida_bytes.FF_0NUMD
   ida_bytes.FF_0CHAR
   ida_bytes.FF_0SEG
   ida_bytes.FF_0OFF
   ida_bytes.FF_0NUMB
   ida_bytes.FF_0NUMO
   ida_bytes.FF_0ENUM
   ida_bytes.FF_0FOP
   ida_bytes.FF_0STRO
   ida_bytes.FF_0STK
   ida_bytes.FF_0FLT
   ida_bytes.FF_0CUST
   ida_bytes.MS_1TYPE
   ida_bytes.FF_1VOID
   ida_bytes.FF_1NUMH
   ida_bytes.FF_1NUMD
   ida_bytes.FF_1CHAR
   ida_bytes.FF_1SEG
   ida_bytes.FF_1OFF
   ida_bytes.FF_1NUMB
   ida_bytes.FF_1NUMO
   ida_bytes.FF_1ENUM
   ida_bytes.FF_1FOP
   ida_bytes.FF_1STRO
   ida_bytes.FF_1STK
   ida_bytes.FF_1FLT
   ida_bytes.FF_1CUST
   ida_bytes.DTP_NODUP


Classes
-------

.. autoapisummary::

   ida_bytes.compiled_binpat_vec_t
   ida_bytes.octet_generator_t
   ida_bytes.data_type_t
   ida_bytes.data_format_t
   ida_bytes.compiled_binpat_t
   ida_bytes.hidden_range_t


Functions
---------

.. autoapisummary::

   ida_bytes.enable_flags
   ida_bytes.disable_flags
   ida_bytes.change_storage_type
   ida_bytes.next_addr
   ida_bytes.prev_addr
   ida_bytes.next_chunk
   ida_bytes.prev_chunk
   ida_bytes.chunk_start
   ida_bytes.chunk_size
   ida_bytes.find_free_chunk
   ida_bytes.next_that
   ida_bytes.next_unknown
   ida_bytes.prev_that
   ida_bytes.prev_unknown
   ida_bytes.prev_head
   ida_bytes.next_head
   ida_bytes.prev_not_tail
   ida_bytes.next_not_tail
   ida_bytes.prev_visea
   ida_bytes.next_visea
   ida_bytes.get_item_head
   ida_bytes.get_item_end
   ida_bytes.calc_max_item_end
   ida_bytes.get_item_size
   ida_bytes.is_mapped
   ida_bytes.get_flags_ex
   ida_bytes.get_flags32
   ida_bytes.get_flags
   ida_bytes.get_full_flags
   ida_bytes.get_item_flag
   ida_bytes.get_item_refinfo
   ida_bytes.has_value
   ida_bytes.del_value
   ida_bytes.is_loaded
   ida_bytes.nbits
   ida_bytes.bytesize
   ida_bytes.get_byte
   ida_bytes.get_db_byte
   ida_bytes.get_word
   ida_bytes.get_dword
   ida_bytes.get_qword
   ida_bytes.get_wide_byte
   ida_bytes.get_wide_word
   ida_bytes.get_wide_dword
   ida_bytes.get_octet
   ida_bytes.get_16bit
   ida_bytes.get_32bit
   ida_bytes.get_64bit
   ida_bytes.get_data_value
   ida_bytes.get_original_byte
   ida_bytes.get_original_word
   ida_bytes.get_original_dword
   ida_bytes.get_original_qword
   ida_bytes.put_byte
   ida_bytes.put_word
   ida_bytes.put_dword
   ida_bytes.put_qword
   ida_bytes.patch_byte
   ida_bytes.patch_word
   ida_bytes.patch_dword
   ida_bytes.patch_qword
   ida_bytes.revert_byte
   ida_bytes.add_byte
   ida_bytes.add_word
   ida_bytes.add_dword
   ida_bytes.add_qword
   ida_bytes.get_zero_ranges
   ida_bytes.put_bytes
   ida_bytes.patch_bytes
   ida_bytes.is_code
   ida_bytes.f_is_code
   ida_bytes.is_data
   ida_bytes.f_is_data
   ida_bytes.is_tail
   ida_bytes.f_is_tail
   ida_bytes.is_not_tail
   ida_bytes.f_is_not_tail
   ida_bytes.is_unknown
   ida_bytes.is_head
   ida_bytes.f_is_head
   ida_bytes.del_items
   ida_bytes.is_manual_insn
   ida_bytes.get_manual_insn
   ida_bytes.set_manual_insn
   ida_bytes.is_flow
   ida_bytes.has_extra_cmts
   ida_bytes.f_has_extra_cmts
   ida_bytes.has_cmt
   ida_bytes.f_has_cmt
   ida_bytes.has_xref
   ida_bytes.f_has_xref
   ida_bytes.has_name
   ida_bytes.f_has_name
   ida_bytes.has_dummy_name
   ida_bytes.f_has_dummy_name
   ida_bytes.has_auto_name
   ida_bytes.has_any_name
   ida_bytes.has_user_name
   ida_bytes.f_has_user_name
   ida_bytes.is_invsign
   ida_bytes.toggle_sign
   ida_bytes.is_bnot
   ida_bytes.toggle_bnot
   ida_bytes.is_lzero
   ida_bytes.set_lzero
   ida_bytes.clr_lzero
   ida_bytes.toggle_lzero
   ida_bytes.leading_zero_important
   ida_bytes.get_operand_type_shift
   ida_bytes.get_operand_flag
   ida_bytes.is_flag_for_operand
   ida_bytes.is_defarg0
   ida_bytes.is_defarg1
   ida_bytes.is_off0
   ida_bytes.is_off1
   ida_bytes.is_char0
   ida_bytes.is_char1
   ida_bytes.is_seg0
   ida_bytes.is_seg1
   ida_bytes.is_enum0
   ida_bytes.is_enum1
   ida_bytes.is_stroff0
   ida_bytes.is_stroff1
   ida_bytes.is_stkvar0
   ida_bytes.is_stkvar1
   ida_bytes.is_float0
   ida_bytes.is_float1
   ida_bytes.is_custfmt0
   ida_bytes.is_custfmt1
   ida_bytes.is_numop0
   ida_bytes.is_numop1
   ida_bytes.get_optype_flags0
   ida_bytes.get_optype_flags1
   ida_bytes.is_defarg
   ida_bytes.is_off
   ida_bytes.is_char
   ida_bytes.is_seg
   ida_bytes.is_enum
   ida_bytes.is_manual
   ida_bytes.is_stroff
   ida_bytes.is_stkvar
   ida_bytes.is_fltnum
   ida_bytes.is_custfmt
   ida_bytes.is_numop
   ida_bytes.is_suspop
   ida_bytes.op_adds_xrefs
   ida_bytes.set_op_type
   ida_bytes.op_seg
   ida_bytes.op_enum
   ida_bytes.get_enum_id
   ida_bytes.op_based_stroff
   ida_bytes.op_stkvar
   ida_bytes.set_forced_operand
   ida_bytes.get_forced_operand
   ida_bytes.is_forced_operand
   ida_bytes.combine_flags
   ida_bytes.char_flag
   ida_bytes.off_flag
   ida_bytes.enum_flag
   ida_bytes.stroff_flag
   ida_bytes.stkvar_flag
   ida_bytes.flt_flag
   ida_bytes.custfmt_flag
   ida_bytes.seg_flag
   ida_bytes.num_flag
   ida_bytes.hex_flag
   ida_bytes.dec_flag
   ida_bytes.oct_flag
   ida_bytes.bin_flag
   ida_bytes.op_chr
   ida_bytes.op_num
   ida_bytes.op_hex
   ida_bytes.op_dec
   ida_bytes.op_oct
   ida_bytes.op_bin
   ida_bytes.op_flt
   ida_bytes.op_custfmt
   ida_bytes.clr_op_type
   ida_bytes.get_default_radix
   ida_bytes.get_radix
   ida_bytes.code_flag
   ida_bytes.byte_flag
   ida_bytes.word_flag
   ida_bytes.dword_flag
   ida_bytes.qword_flag
   ida_bytes.oword_flag
   ida_bytes.yword_flag
   ida_bytes.zword_flag
   ida_bytes.tbyte_flag
   ida_bytes.strlit_flag
   ida_bytes.stru_flag
   ida_bytes.cust_flag
   ida_bytes.align_flag
   ida_bytes.float_flag
   ida_bytes.double_flag
   ida_bytes.packreal_flag
   ida_bytes.is_byte
   ida_bytes.is_word
   ida_bytes.is_dword
   ida_bytes.is_qword
   ida_bytes.is_oword
   ida_bytes.is_yword
   ida_bytes.is_zword
   ida_bytes.is_tbyte
   ida_bytes.is_float
   ida_bytes.is_double
   ida_bytes.is_pack_real
   ida_bytes.is_strlit
   ida_bytes.is_struct
   ida_bytes.is_align
   ida_bytes.is_custom
   ida_bytes.f_is_byte
   ida_bytes.f_is_word
   ida_bytes.f_is_dword
   ida_bytes.f_is_qword
   ida_bytes.f_is_oword
   ida_bytes.f_is_yword
   ida_bytes.f_is_tbyte
   ida_bytes.f_is_float
   ida_bytes.f_is_double
   ida_bytes.f_is_pack_real
   ida_bytes.f_is_strlit
   ida_bytes.f_is_struct
   ida_bytes.f_is_align
   ida_bytes.f_is_custom
   ida_bytes.is_same_data_type
   ida_bytes.get_flags_by_size
   ida_bytes.create_data
   ida_bytes.calc_dflags
   ida_bytes.create_byte
   ida_bytes.create_word
   ida_bytes.create_dword
   ida_bytes.create_qword
   ida_bytes.create_oword
   ida_bytes.create_yword
   ida_bytes.create_zword
   ida_bytes.create_tbyte
   ida_bytes.create_float
   ida_bytes.create_double
   ida_bytes.create_packed_real
   ida_bytes.create_struct
   ida_bytes.create_custdata
   ida_bytes.create_align
   ida_bytes.calc_min_align
   ida_bytes.calc_max_align
   ida_bytes.calc_def_align
   ida_bytes.create_16bit_data
   ida_bytes.create_32bit_data
   ida_bytes.get_max_strlit_length
   ida_bytes.create_strlit
   ida_bytes.get_opinfo
   ida_bytes.set_opinfo
   ida_bytes.get_data_elsize
   ida_bytes.get_full_data_elsize
   ida_bytes.is_varsize_item
   ida_bytes.get_possible_item_varsize
   ida_bytes.can_define_item
   ida_bytes.has_immd
   ida_bytes.is_func
   ida_bytes.set_immd
   ida_bytes.get_custom_data_type
   ida_bytes.get_custom_data_format
   ida_bytes.attach_custom_data_format
   ida_bytes.detach_custom_data_format
   ida_bytes.is_attached_custom_data_format
   ida_bytes.get_custom_data_types
   ida_bytes.get_custom_data_formats
   ida_bytes.find_custom_data_type
   ida_bytes.find_custom_data_format
   ida_bytes.set_cmt
   ida_bytes.get_cmt
   ida_bytes.append_cmt
   ida_bytes.get_predef_insn_cmt
   ida_bytes.find_byte
   ida_bytes.find_byter
   ida_bytes.parse_binpat_str
   ida_bytes.bin_search
   ida_bytes.next_inited
   ida_bytes.prev_inited
   ida_bytes.equal_bytes
   ida_bytes.update_hidden_range
   ida_bytes.add_hidden_range
   ida_bytes.get_hidden_range
   ida_bytes.getn_hidden_range
   ida_bytes.get_hidden_range_qty
   ida_bytes.get_hidden_range_num
   ida_bytes.get_prev_hidden_range
   ida_bytes.get_next_hidden_range
   ida_bytes.get_first_hidden_range
   ida_bytes.get_last_hidden_range
   ida_bytes.del_hidden_range
   ida_bytes.add_mapping
   ida_bytes.del_mapping
   ida_bytes.use_mapping
   ida_bytes.get_mappings_qty
   ida_bytes.get_mapping
   ida_bytes.visit_patched_bytes
   ida_bytes.get_bytes
   ida_bytes.get_bytes_and_mask
   ida_bytes.get_strlit_contents
   ida_bytes.print_strlit_type
   ida_bytes.op_stroff
   ida_bytes.get_stroff_path
   ida_bytes.register_custom_data_type
   ida_bytes.unregister_custom_data_type
   ida_bytes.register_custom_data_format
   ida_bytes.unregister_custom_data_format
   ida_bytes.register_data_types_and_formats
   ida_bytes.unregister_data_types_and_formats
   ida_bytes.find_bytes
   ida_bytes.find_string


Module Contents
---------------

.. py:class:: compiled_binpat_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> compiled_binpat_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> compiled_binpat_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: compiled_binpat_vec_t) -> None


   .. py:method:: extract() -> compiled_binpat_t *


   .. py:method:: inject(s: compiled_binpat_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< compiled_binpat_t >::const_iterator


   .. py:method:: end(*args) -> qvector< compiled_binpat_t >::const_iterator


   .. py:method:: insert(it: compiled_binpat_t, x: compiled_binpat_t) -> qvector< compiled_binpat_t >::iterator


   .. py:method:: erase(*args) -> qvector< compiled_binpat_t >::iterator


   .. py:method:: find(*args) -> qvector< compiled_binpat_t >::const_iterator


   .. py:method:: has(x: compiled_binpat_t) -> bool


   .. py:method:: add_unique(x: compiled_binpat_t) -> bool


   .. py:method:: append(x: compiled_binpat_t) -> None


   .. py:method:: extend(x: compiled_binpat_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


   .. py:method:: parse(ea: ida_idaapi.ea_t, text: str, radix: int = -1, strlits_encoding: int = -1) -> compiled_binpat_vec_t
      :staticmethod:


      Convert user-specified binary string to internal representation.

      The 'in' parameter contains space-separated tokens:

          *numbers (numeric base is determined by 'radix')
              - if value of number fits a byte, it is considered as a byte
              - if value of number fits a word, it is considered as 2 bytes
              - if value of number fits a dword,it is considered as 4 bytes
          * "..." string constants
          * 'x'  single-character constants
          * ?    variable bytes

      Note that string constants are surrounded with double quotes.

      Here are a few examples (assuming base 16):

          * CD 21          - bytes 0xCD, 0x21
          * 21CD           - bytes 0xCD, 0x21 (little endian ) or 0x21, 0xCD (big-endian)
          * "Hello", 0     - the null terminated string "Hello"
          * L"Hello"       - 'H', 0, 'e', 0, 'l', 0, 'l', 0, 'o', 0
          * B8 ? ? ? ? 90  - byte 0xB8, 4 bytes with any value, byte 0x90

      This method will throw an exception if the pattern could not be parsed

      :param ea: linear address to convert for (the conversion depends on the
                 address, because the number of bits in a byte depend on the
                 segment type)
      :param text: input text string
      :param radix: numeric base of numbers (8,10,16). If `-1` (the default), then the default radix will be used (see get_default_radix)
      :param strlits_encoding: the target encoding into which the string
                           literals present in 'in', should be encoded.
                           Can be any from [1, get_encoding_qty()), or
                           the special values PBSENC_*
      :returns: a set of patterns



.. py:function:: enable_flags(start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t, stt: storage_type_t) -> error_t

   Allocate flags for address range. This function does not change the storage type of existing ranges. Exit with an error message if not enough disk space. 
           
   :param start_ea: should be lower than end_ea.
   :param end_ea: does not belong to the range.
   :param stt: storage_type_t
   :returns: 0 if ok, otherwise an error code


.. py:function:: disable_flags(start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t) -> error_t

   Deallocate flags for address range. Exit with an error message if not enough disk space (this may occur too). 
           
   :param start_ea: should be lower than end_ea.
   :param end_ea: does not belong to the range.
   :returns: 0 if ok, otherwise return error code


.. py:function:: change_storage_type(start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t, stt: storage_type_t) -> error_t

   Change flag storage type for address range. 
           
   :param start_ea: should be lower than end_ea.
   :param end_ea: does not belong to the range.
   :param stt: storage_type_t
   :returns: error code


.. py:function:: next_addr(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get next address in the program (i.e. next address which has flags). 
           
   :returns: BADADDR if no such address exist.


.. py:function:: prev_addr(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get previous address in the program. 
           
   :returns: BADADDR if no such address exist.


.. py:function:: next_chunk(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get the first address of next contiguous chunk in the program. 
           
   :returns: BADADDR if next chunk doesn't exist.


.. py:function:: prev_chunk(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get the last address of previous contiguous chunk in the program. 
           
   :returns: BADADDR if previous chunk doesn't exist.


.. py:function:: chunk_start(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get start of the contiguous address block containing 'ea'. 
           
   :returns: BADADDR if 'ea' doesn't belong to the program.


.. py:function:: chunk_size(ea: ida_idaapi.ea_t) -> asize_t

   Get size of the contiguous address block containing 'ea'. 
           
   :returns: 0 if 'ea' doesn't belong to the program.


.. py:function:: find_free_chunk(start: ida_idaapi.ea_t, size: asize_t, alignment: asize_t) -> ida_idaapi.ea_t

   Search for a hole in the addressing space of the program. 
           
   :param start: Address to start searching from
   :param size: Size of the desired empty range
   :param alignment: Alignment bitmask, must be a pow2-1. (for example, 0xF would align the returned range to 16 bytes).
   :returns: Start of the found empty range or BADADDR


.. py:function:: next_that(ea: ida_idaapi.ea_t, maxea: ida_idaapi.ea_t, testf: testf_t *) -> ida_idaapi.ea_t

   Find next address with a flag satisfying the function 'testf'. 
           
   :param ea: start searching at this address + 1
   :param maxea: not included in the search range.
   :param testf: test function to find next address
   :returns: the found address or BADADDR.


.. py:function:: next_unknown(ea: ida_idaapi.ea_t, maxea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Similar to next_that(), but will find the next address that is unexplored.


.. py:function:: prev_that(ea: ida_idaapi.ea_t, minea: ida_idaapi.ea_t, testf: testf_t *) -> ida_idaapi.ea_t

   Find previous address with a flag satisfying the function 'testf'. 
           
   :param ea: start searching from this address - 1.
   :param minea: included in the search range.
   :param testf: test function to find previous address
   :returns: the found address or BADADDR.


.. py:function:: prev_unknown(ea: ida_idaapi.ea_t, minea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Similar to prev_that(), but will find the previous address that is unexplored.


.. py:function:: prev_head(ea: ida_idaapi.ea_t, minea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get start of previous defined item. 
           
   :param ea: begin search at this address
   :param minea: included in the search range
   :returns: BADADDR if none exists.


.. py:function:: next_head(ea: ida_idaapi.ea_t, maxea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get start of next defined item. 
           
   :param ea: begin search at this address
   :param maxea: not included in the search range
   :returns: BADADDR if none exists.


.. py:function:: prev_not_tail(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get address of previous non-tail byte. 
           
   :returns: BADADDR if none exists.


.. py:function:: next_not_tail(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get address of next non-tail byte. 
           
   :returns: BADADDR if none exists.


.. py:function:: prev_visea(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get previous visible address. 
           
   :returns: BADADDR if none exists.


.. py:function:: next_visea(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get next visible address. 
           
   :returns: BADADDR if none exists.


.. py:function:: get_item_head(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get the start address of the item at 'ea'. If there is no current item, then 'ea' will be returned (see definition at the end of bytes.hpp source) 
           


.. py:function:: get_item_end(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Get the end address of the item at 'ea'. The returned address doesn't belong to the current item. Unexplored bytes are counted as 1 byte entities. 
           


.. py:function:: calc_max_item_end(ea: ida_idaapi.ea_t, how: int = 15) -> ida_idaapi.ea_t

   Calculate maximal reasonable end address of a new item. This function will limit the item with the current segment bounds. 
           
   :param ea: linear address
   :param how: when to stop the search. A combination of Item end search flags
   :returns: end of new item. If it is not possible to create an item, it will return 'ea'. If operation was cancelled by user, it will return 'ea'


.. py:data:: ITEM_END_FIXUP

   stop at the first fixup


.. py:data:: ITEM_END_INITED

   stop when initialization changes i.e.
   * if is_loaded(ea): stop if uninitialized byte is encountered
   * if !is_loaded(ea): stop if initialized byte is encountered 


           


.. py:data:: ITEM_END_NAME

   stop at the first named location


.. py:data:: ITEM_END_XREF

   stop at the first referenced location


.. py:data:: ITEM_END_CANCEL

   stop when operation cancelled, it is the responsibility of the caller to show the wait dialog 
           


.. py:function:: get_item_size(ea: ida_idaapi.ea_t) -> asize_t

   Get size of item (instruction/data) in bytes. Unexplored bytes have length of 1 byte. This function returns 0 only for BADADDR. 
           


.. py:function:: is_mapped(ea: ida_idaapi.ea_t) -> bool

   Is the specified address 'ea' present in the program?


.. py:function:: get_flags_ex(ea: ida_idaapi.ea_t, how: int) -> flags64_t

   Get flags for the specified address, extended form.


.. py:data:: GFE_VALUE

   get flags with FF_IVL & MS_VAL. It is much slower under remote debugging because the kernel needs to read the process memory. 
           


.. py:data:: GFE_IDB_VALUE

   get flags with FF_IVL & MS_VAL. but never use the debugger memory. 
           


.. py:data:: GFE_32BIT

   get only low 32 bits of flags


.. py:function:: get_flags32(ea: ida_idaapi.ea_t) -> flags64_t

   Get only 32 low bits of flags. This function returns the most commonly used bits of the flags. However, it does not return the operand info for the operands beyond the first two operands (0,1). If you need to deal with the operands (2..n), then use get_flags(). It is customary to assign the return value to the variable named "F32", to distinguish is from 64-bit flags. 
           
   :returns: 0 if address is not present in the program


.. py:function:: get_flags(ea: ida_idaapi.ea_t) -> flags64_t

   Get flags value for address 'ea'. The byte value is not included in the flags. This function should be used if the operand types of any operand beyond the first two operands is required. This function is more expensive to use than get_flags32() 
           
   :returns: 0 if address is not present in the program


.. py:function:: get_full_flags(ea: ida_idaapi.ea_t) -> flags64_t

   Get full flags value for address 'ea'. This function returns the byte value in the flags as well. See FF_IVL and MS_VAL. This function is more expensive to use than get_flags() 
           
   :returns: 0 if address is not present in the program


.. py:function:: get_item_flag(_from: ida_idaapi.ea_t, n: int, ea: ida_idaapi.ea_t, appzero: bool) -> flags64_t

   Get flag of the item at 'ea' even if it is a tail byte of some array or structure. This function is used to get flags of structure members or array elements. 
           
   :param n: operand number which refers to 'ea' or OPND_ALL for one of the operands
   :param ea: the referenced address
   :param appzero: append a struct field name if the field offset is zero? meaningful only if the name refers to a structure.
   :returns: flags or 0 (if failed)


.. py:function:: get_item_refinfo(ri: refinfo_t, ea: ida_idaapi.ea_t, n: int) -> bool

   Get refinfo of the item at 'ea'. This function works for a regular offset operand as well as for a tail byte of a structure variable (in this case refinfo to corresponding structure member will be returned) 
           
   :param ri: refinfo holder
   :param ea: the item address
   :param n: operand number which refers to 'ea' or OPND_ALL for one of the operands
   :returns: success


.. py:data:: MS_VAL

   Mask for byte value.


.. py:data:: FF_IVL

   Byte has value ?


.. py:function:: has_value(F: flags64_t) -> bool

   Do flags contain byte value?


.. py:function:: del_value(ea: ida_idaapi.ea_t) -> None

   Delete byte value from flags. The corresponding byte becomes uninitialized. 
           


.. py:function:: is_loaded(ea: ida_idaapi.ea_t) -> bool

   Does the specified address have a byte value (is initialized?)


.. py:function:: nbits(ea: ida_idaapi.ea_t) -> int

   Get number of bits in a byte at the given address. 
           
   :returns: processor_t::dnbits() if the address doesn't belong to a segment, otherwise the result depends on the segment type


.. py:function:: bytesize(ea: ida_idaapi.ea_t) -> int

   Get number of bytes required to store a byte at the given address.


.. py:function:: get_byte(ea: ida_idaapi.ea_t) -> uchar

   Get one byte (8-bit) of the program at 'ea'. This function works only for 8bit byte processors. 
           


.. py:function:: get_db_byte(ea: ida_idaapi.ea_t) -> uchar

   Get one byte (8-bit) of the program at 'ea' from the database. Works even if the debugger is active. See also get_dbg_byte() to read the process memory directly. This function works only for 8bit byte processors. 
           


.. py:function:: get_word(ea: ida_idaapi.ea_t) -> ushort

   Get one word (16-bit) of the program at 'ea'. This function takes into account order of bytes specified in idainfo::is_be() This function works only for 8bit byte processors. 
           


.. py:function:: get_dword(ea: ida_idaapi.ea_t) -> int

   Get one dword (32-bit) of the program at 'ea'. This function takes into account order of bytes specified in idainfo::is_be() This function works only for 8bit byte processors. 
           


.. py:function:: get_qword(ea: ida_idaapi.ea_t) -> uint64

   Get one qword (64-bit) of the program at 'ea'. This function takes into account order of bytes specified in idainfo::is_be() This function works only for 8bit byte processors. 
           


.. py:function:: get_wide_byte(ea: ida_idaapi.ea_t) -> uint64

   Get one wide byte of the program at 'ea'. Some processors may access more than 8bit quantity at an address. These processors have 32-bit byte organization from the IDA's point of view. 
           


.. py:function:: get_wide_word(ea: ida_idaapi.ea_t) -> uint64

   Get one wide word (2 'byte') of the program at 'ea'. Some processors may access more than 8bit quantity at an address. These processors have 32-bit byte organization from the IDA's point of view. This function takes into account order of bytes specified in idainfo::is_be() 
           


.. py:function:: get_wide_dword(ea: ida_idaapi.ea_t) -> uint64

   Get two wide words (4 'bytes') of the program at 'ea'. Some processors may access more than 8bit quantity at an address. These processors have 32-bit byte organization from the IDA's point of view. This function takes into account order of bytes specified in idainfo::is_be() 
           


.. py:class:: octet_generator_t(_ea: ida_idaapi.ea_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: value
      :type:  uint64


   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t


   .. py:attribute:: avail_bits
      :type:  int


   .. py:attribute:: high_byte_first
      :type:  bool


   .. py:method:: invert_byte_order() -> None


.. py:function:: get_octet(ogen: octet_generator_t) -> uchar *

.. py:function:: get_16bit(ea: ida_idaapi.ea_t) -> int

   Get 16bits of the program at 'ea'. 
           
   :returns: 1 byte (getFullByte()) if the current processor has 16-bit byte, otherwise return get_word()


.. py:function:: get_32bit(ea: ida_idaapi.ea_t) -> int

   Get not more than 32bits of the program at 'ea'. 
           
   :returns: 32 bit value, depending on processor_t::nbits:
   * if ( nbits <= 8 ) return get_dword(ea);
   * if ( nbits <= 16) return get_wide_word(ea);
   * return get_wide_byte(ea);


.. py:function:: get_64bit(ea: ida_idaapi.ea_t) -> uint64

   Get not more than 64bits of the program at 'ea'. 
           
   :returns: 64 bit value, depending on processor_t::nbits:
   * if ( nbits <= 8 ) return get_qword(ea);
   * if ( nbits <= 16) return get_wide_dword(ea);
   * return get_wide_byte(ea);


.. py:function:: get_data_value(v: uval_t *, ea: ida_idaapi.ea_t, size: asize_t) -> bool

   Get the value at of the item at 'ea'. This function works with entities up to sizeof(ea_t) (bytes, word, etc) 
           
   :param v: pointer to the result. may be nullptr
   :param ea: linear address
   :param size: size of data to read. If 0, then the item type at 'ea' will be used
   :returns: success


.. py:function:: get_original_byte(ea: ida_idaapi.ea_t) -> uint64

   Get original byte value (that was before patching). This function works for wide byte processors too. 
           


.. py:function:: get_original_word(ea: ida_idaapi.ea_t) -> uint64

   Get original word value (that was before patching). This function works for wide byte processors too. This function takes into account order of bytes specified in idainfo::is_be() 
           


.. py:function:: get_original_dword(ea: ida_idaapi.ea_t) -> uint64

   Get original dword (that was before patching) This function works for wide byte processors too. This function takes into account order of bytes specified in idainfo::is_be() 
           


.. py:function:: get_original_qword(ea: ida_idaapi.ea_t) -> uint64

   Get original qword value (that was before patching) This function DOESN'T work for wide byte processors too. This function takes into account order of bytes specified in idainfo::is_be() 
           


.. py:function:: put_byte(ea: ida_idaapi.ea_t, x: uint64) -> bool

   Set value of one byte of the program. This function modifies the database. If the debugger is active then the debugged process memory is patched too. 
           
   :param ea: linear address
   :param x: byte value
   :returns: true if the database has been modified


.. py:function:: put_word(ea: ida_idaapi.ea_t, x: uint64) -> None

   Set value of one word of the program. This function takes into account order of bytes specified in idainfo::is_be() This function works for wide byte processors too. 
           


.. py:function:: put_dword(ea: ida_idaapi.ea_t, x: uint64) -> None

   Set value of one dword of the program. This function takes into account order of bytes specified in idainfo::is_be() This function works for wide byte processors too. 
           
   :param ea: linear address
   :param x: dword value


.. py:function:: put_qword(ea: ida_idaapi.ea_t, x: uint64) -> None

   Set value of one qword (8 bytes) of the program. This function takes into account order of bytes specified in idainfo::is_be() This function DOESN'T works for wide byte processors. 
           
   :param ea: linear address
   :param x: qword value


.. py:function:: patch_byte(ea: ida_idaapi.ea_t, x: uint64) -> bool

   Patch a byte of the program. The original value of the byte is saved and can be obtained by get_original_byte(). This function works for wide byte processors too. 
           
   :returns: true: the database has been modified,
   :returns: false: the debugger is running and the process' memory has value 'x' at address 'ea', or the debugger is not running, and the IDB has value 'x' at address 'ea already.


.. py:function:: patch_word(ea: ida_idaapi.ea_t, x: uint64) -> bool

   Patch a word of the program. The original value of the word is saved and can be obtained by get_original_word(). This function works for wide byte processors too. This function takes into account order of bytes specified in idainfo::is_be() 
           
   :returns: true: the database has been modified,
   :returns: false: the debugger is running and the process' memory has value 'x' at address 'ea', or the debugger is not running, and the IDB has value 'x' at address 'ea already.


.. py:function:: patch_dword(ea: ida_idaapi.ea_t, x: uint64) -> bool

   Patch a dword of the program. The original value of the dword is saved and can be obtained by get_original_dword(). This function DOESN'T work for wide byte processors. This function takes into account order of bytes specified in idainfo::is_be() 
           
   :returns: true: the database has been modified,
   :returns: false: the debugger is running and the process' memory has value 'x' at address 'ea', or the debugger is not running, and the IDB has value 'x' at address 'ea already.


.. py:function:: patch_qword(ea: ida_idaapi.ea_t, x: uint64) -> bool

   Patch a qword of the program. The original value of the qword is saved and can be obtained by get_original_qword(). This function DOESN'T work for wide byte processors. This function takes into account order of bytes specified in idainfo::is_be() 
           
   :returns: true: the database has been modified,
   :returns: false: the debugger is running and the process' memory has value 'x' at address 'ea', or the debugger is not running, and the IDB has value 'x' at address 'ea already.


.. py:function:: revert_byte(ea: ida_idaapi.ea_t) -> bool

   Revert patched byte 
           
   :returns: true: byte was patched before and reverted now


.. py:function:: add_byte(ea: ida_idaapi.ea_t, value: int) -> None

   Add a value to one byte of the program. This function works for wide byte processors too. 
           
   :param ea: linear address
   :param value: byte value


.. py:function:: add_word(ea: ida_idaapi.ea_t, value: uint64) -> None

   Add a value to one word of the program. This function works for wide byte processors too. This function takes into account order of bytes specified in idainfo::is_be() 
           
   :param ea: linear address
   :param value: byte value


.. py:function:: add_dword(ea: ida_idaapi.ea_t, value: uint64) -> None

   Add a value to one dword of the program. This function works for wide byte processors too. This function takes into account order of bytes specified in idainfo::is_be() 
           
   :param ea: linear address
   :param value: byte value


.. py:function:: add_qword(ea: ida_idaapi.ea_t, value: uint64) -> None

   Add a value to one qword of the program. This function does not work for wide byte processors. This function takes into account order of bytes specified in idainfo::is_be() 
           
   :param ea: linear address
   :param value: byte value


.. py:function:: get_zero_ranges(zranges: rangeset_t, range: range_t) -> bool

   Return set of ranges with zero initialized bytes. The returned set includes only big zero initialized ranges (at least >1KB). Some zero initialized byte ranges may be not included. Only zero bytes that use the sparse storage method (STT_MM) are reported. 
           
   :param zranges: pointer to the return value. cannot be nullptr
   :param range: the range of addresses to verify. can be nullptr - means all ranges
   :returns: true if the result is a non-empty set


.. py:data:: GMB_READALL

   try to read all bytes; if this bit is not set, fail at first uninited byte 
           


.. py:data:: GMB_WAITBOX

   show wait box (may return -1 in this case)


.. py:function:: put_bytes(ea: ida_idaapi.ea_t, buf: void const *) -> None

   Modify the specified number of bytes of the program. This function does not save the original values of bytes. See also patch_bytes(). 
           
   :param ea: linear address
   :param buf: buffer with new values of bytes


.. py:function:: patch_bytes(ea: ida_idaapi.ea_t, buf: void const *) -> None

   Patch the specified number of bytes of the program. Original values of bytes are saved and are available with get_original...() functions. See also put_bytes(). 
           
   :param ea: linear address
   :param buf: buffer with new values of bytes


.. py:data:: MS_CLS

   Mask for typing.


.. py:data:: FF_CODE

   Code ?


.. py:data:: FF_DATA

   Data ?


.. py:data:: FF_TAIL

   Tail ?


.. py:data:: FF_UNK

   Unknown ?


.. py:function:: is_code(F: flags64_t) -> bool

   Does flag denote start of an instruction?


.. py:function:: f_is_code(F: flags64_t, arg2: void *) -> bool

   Does flag denote start of an instruction?


.. py:function:: is_data(F: flags64_t) -> bool

   Does flag denote start of data?


.. py:function:: f_is_data(F: flags64_t, arg2: void *) -> bool

   Does flag denote start of data?


.. py:function:: is_tail(F: flags64_t) -> bool

   Does flag denote tail byte?


.. py:function:: f_is_tail(F: flags64_t, arg2: void *) -> bool

   Does flag denote tail byte?


.. py:function:: is_not_tail(F: flags64_t) -> bool

   Does flag denote tail byte?


.. py:function:: f_is_not_tail(F: flags64_t, arg2: void *) -> bool

   Does flag denote tail byte?


.. py:function:: is_unknown(F: flags64_t) -> bool

   Does flag denote unexplored byte?


.. py:function:: is_head(F: flags64_t) -> bool

   Does flag denote start of instruction OR data?


.. py:function:: f_is_head(F: flags64_t, arg2: void *) -> bool

   Does flag denote start of instruction OR data?


.. py:function:: del_items(ea: ida_idaapi.ea_t, flags: int = 0, nbytes: asize_t = 1, may_destroy: may_destroy_cb_t * = None) -> bool

   Convert item (instruction/data) to unexplored bytes. The whole item (including the head and tail bytes) will be destroyed. It is allowed to pass any address in the item to this function 
           
   :param ea: any address within the first item to delete
   :param flags: combination of Unexplored byte conversion flags
   :param nbytes: number of bytes in the range to be undefined
   :param may_destroy: optional routine invoked before deleting a head item. If callback returns false then item is not to be deleted and operation fails
   :returns: true on sucessful operation, otherwise false


.. py:data:: DELIT_SIMPLE

   simply undefine the specified item(s)


.. py:data:: DELIT_EXPAND

   propagate undefined items; for example if removing an instruction removes all references to the next instruction, then plan to convert to unexplored the next instruction too. 
           


.. py:data:: DELIT_DELNAMES

   delete any names at the specified address range (except for the starting address). this bit is valid if nbytes > 1 
           


.. py:data:: DELIT_NOTRUNC

   don't truncate the current function even if AF_TRFUNC is set 
           


.. py:data:: DELIT_NOUNAME

   reject to delete if a user name is in address range (except for the starting address). this bit is valid if nbytes > 1 
           


.. py:data:: DELIT_NOCMT

   reject to delete if a comment is in address range (except for the starting address). this bit is valid if nbytes > 1 
           


.. py:data:: DELIT_KEEPFUNC

   do not undefine the function start. Just delete xrefs, ops e.t.c. 
           


.. py:function:: is_manual_insn(ea: ida_idaapi.ea_t) -> bool

   Is the instruction overridden? 
           
   :param ea: linear address of the instruction or data item


.. py:function:: get_manual_insn(ea: ida_idaapi.ea_t) -> str

   Retrieve the user-specified string for the manual instruction. 
           
   :param ea: linear address of the instruction or data item
   :returns: size of manual instruction or -1


.. py:function:: set_manual_insn(ea: ida_idaapi.ea_t, manual_insn: str) -> None

   Set manual instruction string. 
           
   :param ea: linear address of the instruction or data item
   :param manual_insn: "" - delete manual string. nullptr - do nothing


.. py:data:: MS_COMM

   Mask of common bits.


.. py:data:: FF_COMM

   Has comment?


.. py:data:: FF_REF

   has references


.. py:data:: FF_LINE

   Has next or prev lines?


.. py:data:: FF_NAME

   Has name?


.. py:data:: FF_LABL

   Has dummy name?


.. py:data:: FF_FLOW

   Exec flow from prev instruction.


.. py:data:: FF_SIGN

   Inverted sign of operands.


.. py:data:: FF_BNOT

   Bitwise negation of operands.


.. py:data:: FF_UNUSED

   unused bit (was used for variable bytes)


.. py:function:: is_flow(F: flags64_t) -> bool

   Does the previous instruction exist and pass execution flow to the current byte?


.. py:function:: has_extra_cmts(F: flags64_t) -> bool

   Does the current byte have additional anterior or posterior lines?


.. py:function:: f_has_extra_cmts(f: flags64_t, arg2: void *) -> bool

.. py:function:: has_cmt(F: flags64_t) -> bool

   Does the current byte have an indented comment?


.. py:function:: f_has_cmt(f: flags64_t, arg2: void *) -> bool

.. py:function:: has_xref(F: flags64_t) -> bool

   Does the current byte have cross-references to it?


.. py:function:: f_has_xref(f: flags64_t, arg2: void *) -> bool

   Does the current byte have cross-references to it?


.. py:function:: has_name(F: flags64_t) -> bool

   Does the current byte have non-trivial (non-dummy) name?


.. py:function:: f_has_name(f: flags64_t, arg2: void *) -> bool

   Does the current byte have non-trivial (non-dummy) name?


.. py:data:: FF_ANYNAME

   Has name or dummy name?


.. py:function:: has_dummy_name(F: flags64_t) -> bool

   Does the current byte have dummy (auto-generated, with special prefix) name?


.. py:function:: f_has_dummy_name(f: flags64_t, arg2: void *) -> bool

   Does the current byte have dummy (auto-generated, with special prefix) name?


.. py:function:: has_auto_name(F: flags64_t) -> bool

   Does the current byte have auto-generated (no special prefix) name?


.. py:function:: has_any_name(F: flags64_t) -> bool

   Does the current byte have any name?


.. py:function:: has_user_name(F: flags64_t) -> bool

   Does the current byte have user-specified name?


.. py:function:: f_has_user_name(F: flags64_t, arg2: void *) -> bool

   Does the current byte have user-specified name?


.. py:function:: is_invsign(ea: ida_idaapi.ea_t, F: flags64_t, n: int) -> bool

   Should sign of n-th operand inverted during output?. allowed values of n: 0-first operand, 1-other operands 
           


.. py:function:: toggle_sign(ea: ida_idaapi.ea_t, n: int) -> bool

   Toggle sign of n-th operand. allowed values of n: 0-first operand, 1-other operands 
           


.. py:function:: is_bnot(ea: ida_idaapi.ea_t, F: flags64_t, n: int) -> bool

   Should we negate the operand?. asm_t::a_bnot should be defined in the idp module in order to work with this function 
           


.. py:function:: toggle_bnot(ea: ida_idaapi.ea_t, n: int) -> bool

   Toggle binary negation of operand. also see is_bnot()


.. py:function:: is_lzero(ea: ida_idaapi.ea_t, n: int) -> bool

   Display leading zeroes? Display leading zeroes in operands. The global switch for the leading zeroes is in idainfo::s_genflags Note: the leading zeroes doesn't work if for the target assembler octal numbers start with 0. 
           
   :param ea: the item (insn/data) address
   :param n: the operand number (0-first operand, 1-other operands)
   :returns: success


.. py:function:: set_lzero(ea: ida_idaapi.ea_t, n: int) -> bool

   Set toggle lzero bit. This function changes the display of leading zeroes for the specified operand. If the default is not to display leading zeroes, this function will display them and vice versa. 
           
   :param ea: the item (insn/data) address
   :param n: the operand number (0-first operand, 1-other operands)
   :returns: success


.. py:function:: clr_lzero(ea: ida_idaapi.ea_t, n: int) -> bool

   Clear toggle lzero bit. This function reset the display of leading zeroes for the specified operand to the default. If the default is not to display leading zeroes, leading zeroes will not be displayed, as vice versa. 
           
   :param ea: the item (insn/data) address
   :param n: the operand number (0-first operand, 1-other operands)
   :returns: success


.. py:function:: toggle_lzero(ea: ida_idaapi.ea_t, n: int) -> bool

   Toggle lzero bit. 
           
   :param ea: the item (insn/data) address
   :param n: the operand number (0-first operand, 1-other operands)
   :returns: success


.. py:function:: leading_zero_important(ea: ida_idaapi.ea_t, n: int) -> bool

   Check if leading zeroes are important.


.. py:data:: MS_N_TYPE

   Mask for nth arg (a 64-bit constant)


.. py:data:: FF_N_VOID

   Void (unknown)?


.. py:data:: FF_N_NUMH

   Hexadecimal number?


.. py:data:: FF_N_NUMD

   Decimal number?


.. py:data:: FF_N_CHAR

   Char ('x')?


.. py:data:: FF_N_SEG

   Segment?


.. py:data:: FF_N_OFF

   Offset?


.. py:data:: FF_N_NUMB

   Binary number?


.. py:data:: FF_N_NUMO

   Octal number?


.. py:data:: FF_N_ENUM

   Enumeration?


.. py:data:: FF_N_FOP

   Forced operand?


.. py:data:: FF_N_STRO

   Struct offset?


.. py:data:: FF_N_STK

   Stack variable?


.. py:data:: FF_N_FLT

   Floating point number?


.. py:data:: FF_N_CUST

   Custom representation?


.. py:function:: get_operand_type_shift(n: int) -> int

   Get the shift in `flags64_t` for the nibble representing operand `n`'s type
   Note: n must be < UA_MAXOP, and is not checked

   :param n: the operand number
   :returns: the shift to the nibble


.. py:function:: get_operand_flag(typebits: uint8, n: int) -> flags64_t

   Place operand `n`'s type flag in the right nibble of a 64-bit flags set.

   :param typebits: the type bits (one of `FF_N_`)
   :param n: the operand number
   :returns: the shift to the nibble


.. py:function:: is_flag_for_operand(F: flags64_t, typebits: uint8, n: int) -> bool

   Check that the 64-bit flags set has the expected type for operand `n`.

   :param F: the flags
   :param typebits: the type bits (one of `FF_N_`)
   :param n: the operand number
   :returns: success


.. py:function:: is_defarg0(F: flags64_t) -> bool

   Is the first operand defined? Initially operand has no defined representation.


.. py:function:: is_defarg1(F: flags64_t) -> bool

   Is the second operand defined? Initially operand has no defined representation.


.. py:function:: is_off0(F: flags64_t) -> bool

   Is the first operand offset? (example: push offset xxx)


.. py:function:: is_off1(F: flags64_t) -> bool

   Is the second operand offset? (example: mov ax, offset xxx)


.. py:function:: is_char0(F: flags64_t) -> bool

   Is the first operand character constant? (example: push 'a')


.. py:function:: is_char1(F: flags64_t) -> bool

   Is the second operand character constant? (example: mov al, 'a')


.. py:function:: is_seg0(F: flags64_t) -> bool

   Is the first operand segment selector? (example: push seg seg001)


.. py:function:: is_seg1(F: flags64_t) -> bool

   Is the second operand segment selector? (example: mov dx, seg dseg)


.. py:function:: is_enum0(F: flags64_t) -> bool

   Is the first operand a symbolic constant (enum member)?


.. py:function:: is_enum1(F: flags64_t) -> bool

   Is the second operand a symbolic constant (enum member)?


.. py:function:: is_stroff0(F: flags64_t) -> bool

   Is the first operand an offset within a struct?


.. py:function:: is_stroff1(F: flags64_t) -> bool

   Is the second operand an offset within a struct?


.. py:function:: is_stkvar0(F: flags64_t) -> bool

   Is the first operand a stack variable?


.. py:function:: is_stkvar1(F: flags64_t) -> bool

   Is the second operand a stack variable?


.. py:function:: is_float0(F: flags64_t) -> bool

   Is the first operand a floating point number?


.. py:function:: is_float1(F: flags64_t) -> bool

   Is the second operand a floating point number?


.. py:function:: is_custfmt0(F: flags64_t) -> bool

   Does the first operand use a custom data representation?


.. py:function:: is_custfmt1(F: flags64_t) -> bool

   Does the second operand use a custom data representation?


.. py:function:: is_numop0(F: flags64_t) -> bool

   Is the first operand a number (i.e. binary, octal, decimal or hex?)


.. py:function:: is_numop1(F: flags64_t) -> bool

   Is the second operand a number (i.e. binary, octal, decimal or hex?)


.. py:function:: get_optype_flags0(F: flags64_t) -> flags64_t

   Get flags for first operand.


.. py:function:: get_optype_flags1(F: flags64_t) -> flags64_t

   Get flags for second operand.


.. py:data:: OPND_OUTER

   outer offset base (combined with operand number). used only in set, get, del_offset() functions 
           


.. py:data:: OPND_MASK

   mask for operand number


.. py:data:: OPND_ALL

   all operands


.. py:function:: is_defarg(F: flags64_t, n: int) -> bool

   is defined?


.. py:function:: is_off(F: flags64_t, n: int) -> bool

   is offset?


.. py:function:: is_char(F: flags64_t, n: int) -> bool

   is character constant?


.. py:function:: is_seg(F: flags64_t, n: int) -> bool

   is segment?


.. py:function:: is_enum(F: flags64_t, n: int) -> bool

   is enum?


.. py:function:: is_manual(F: flags64_t, n: int) -> bool

   is forced operand? (use is_forced_operand())


.. py:function:: is_stroff(F: flags64_t, n: int) -> bool

   is struct offset?


.. py:function:: is_stkvar(F: flags64_t, n: int) -> bool

   is stack variable?


.. py:function:: is_fltnum(F: flags64_t, n: int) -> bool

   is floating point number?


.. py:function:: is_custfmt(F: flags64_t, n: int) -> bool

   is custom data format?


.. py:function:: is_numop(F: flags64_t, n: int) -> bool

   is number (bin, oct, dec, hex)?


.. py:function:: is_suspop(ea: ida_idaapi.ea_t, F: flags64_t, n: int) -> bool

   is suspicious operand?


.. py:function:: op_adds_xrefs(F: flags64_t, n: int) -> bool

   Should processor module create xrefs from the operand?. Currently 'offset', 'structure offset', 'stack' and 'enum' operands create xrefs 
           


.. py:function:: set_op_type(ea: ida_idaapi.ea_t, type: flags64_t, n: int) -> bool

   (internal function) change representation of operand(s). 
           
   :param ea: linear address
   :param type: new flag value (should be obtained from char_flag(), num_flag() and similar functions)
   :param n: 0..UA_MAXOP-1 operand number, OPND_ALL all operands
   :returns: 1: ok
   :returns: 0: failed (applied to a tail byte)


.. py:function:: op_seg(ea: ida_idaapi.ea_t, n: int) -> bool

   Set operand representation to be 'segment'. If applied to unexplored bytes, converts them to 16/32bit word data 
           
   :param ea: linear address
   :param n: 0..UA_MAXOP-1 operand number, OPND_ALL all operands
   :returns: success


.. py:function:: op_enum(ea: ida_idaapi.ea_t, n: int, id: tid_t, serial: uchar = 0) -> bool

   Set operand representation to be enum type If applied to unexplored bytes, converts them to 16/32bit word data 
           
   :param ea: linear address
   :param n: 0..UA_MAXOP-1 operand number, OPND_ALL all operands
   :param id: id of enum
   :param serial: the serial number of the constant in the enumeration, usually 0. the serial numbers are used if the enumeration contains several constants with the same value
   :returns: success


.. py:function:: get_enum_id(ea: ida_idaapi.ea_t, n: int) -> uchar *

   Get enum id of 'enum' operand. 
           
   :param ea: linear address
   :param n: 0..UA_MAXOP-1 operand number, OPND_ALL one of the operands
   :returns: id of enum or BADNODE


.. py:function:: op_based_stroff(insn: insn_t const &, n: int, opval: adiff_t, base: ida_idaapi.ea_t) -> bool

   Set operand representation to be 'struct offset' if the operand likely points to a structure member. For example, let's there is a structure at 1000 1000 stru_1000 Elf32_Sym <...> the operand #8 will be represented as '#Elf32_Sym.st_size' after the call of 'op_based_stroff(..., 8, 0x1000)' By the way, after the call of 'op_plain_offset(..., 0x1000)' it will be represented as '#(stru_1000.st_size - 0x1000)' 
           
   :param insn: the instruction
   :param n: 0..UA_MAXOP-1 operand number, OPND_ALL all operands
   :param opval: operand value (usually op_t::value or op_t::addr)
   :param base: base reference
   :returns: success


.. py:function:: op_stkvar(ea: ida_idaapi.ea_t, n: int) -> bool

   Set operand representation to be 'stack variable'. Should be applied to an instruction within a function. Should be applied after creating a stack var using insn_t::create_stkvar(). 
           
   :param ea: linear address
   :param n: 0..UA_MAXOP-1 operand number, OPND_ALL all operands
   :returns: success


.. py:function:: set_forced_operand(ea: ida_idaapi.ea_t, n: int, op: str) -> bool

   Set forced operand. 
           
   :param ea: linear address
   :param n: 0..UA_MAXOP-1 operand number
   :param op: text of operand
   * nullptr: do nothing (return 0)
   * "" : delete forced operand
   :returns: success


.. py:function:: get_forced_operand(ea: ida_idaapi.ea_t, n: int) -> str

   Get forced operand. 
           
   :param ea: linear address
   :param n: 0..UA_MAXOP-1 operand number
   :returns: size of forced operand or -1


.. py:function:: is_forced_operand(ea: ida_idaapi.ea_t, n: int) -> bool

   Is operand manually defined?. 
           
   :param ea: linear address
   :param n: 0..UA_MAXOP-1 operand number


.. py:function:: combine_flags(F: flags64_t) -> flags64_t

.. py:function:: char_flag() -> flags64_t

   see FF_opbits


.. py:function:: off_flag() -> flags64_t

   see FF_opbits


.. py:function:: enum_flag() -> flags64_t

   see FF_opbits


.. py:function:: stroff_flag() -> flags64_t

   see FF_opbits


.. py:function:: stkvar_flag() -> flags64_t

   see FF_opbits


.. py:function:: flt_flag() -> flags64_t

   see FF_opbits


.. py:function:: custfmt_flag() -> flags64_t

   see FF_opbits


.. py:function:: seg_flag() -> flags64_t

   see FF_opbits


.. py:function:: num_flag() -> flags64_t

   Get number of default base (bin, oct, dec, hex) 
           


.. py:function:: hex_flag() -> flags64_t

   Get number flag of the base, regardless of current processor - better to use num_flag()


.. py:function:: dec_flag() -> flags64_t

   Get number flag of the base, regardless of current processor - better to use num_flag()


.. py:function:: oct_flag() -> flags64_t

   Get number flag of the base, regardless of current processor - better to use num_flag()


.. py:function:: bin_flag() -> flags64_t

   Get number flag of the base, regardless of current processor - better to use num_flag()


.. py:function:: op_chr(ea: ida_idaapi.ea_t, n: int) -> bool

   set op type to char_flag()


.. py:function:: op_num(ea: ida_idaapi.ea_t, n: int) -> bool

   set op type to num_flag()


.. py:function:: op_hex(ea: ida_idaapi.ea_t, n: int) -> bool

   set op type to hex_flag()


.. py:function:: op_dec(ea: ida_idaapi.ea_t, n: int) -> bool

   set op type to dec_flag()


.. py:function:: op_oct(ea: ida_idaapi.ea_t, n: int) -> bool

   set op type to oct_flag()


.. py:function:: op_bin(ea: ida_idaapi.ea_t, n: int) -> bool

   set op type to bin_flag()


.. py:function:: op_flt(ea: ida_idaapi.ea_t, n: int) -> bool

   set op type to flt_flag()


.. py:function:: op_custfmt(ea: ida_idaapi.ea_t, n: int, fid: int) -> bool

   Set custom data format for operand (fid-custom data format id)


.. py:function:: clr_op_type(ea: ida_idaapi.ea_t, n: int) -> bool

   Remove operand representation information. (set operand representation to be 'undefined') 
           
   :param ea: linear address
   :param n: 0..UA_MAXOP-1 operand number, OPND_ALL all operands
   :returns: success


.. py:function:: get_default_radix() -> int

   Get default base of number for the current processor. 
           
   :returns: 2, 8, 10, 16


.. py:function:: get_radix(F: flags64_t, n: int) -> int

   Get radix of the operand, in: flags. If the operand is not a number, returns get_default_radix() 
           
   :param F: flags
   :param n: number of operand (0, 1, -1)
   :returns: 2, 8, 10, 16


.. py:data:: DT_TYPE

   Mask for DATA typing.


.. py:data:: FF_BYTE

   byte


.. py:data:: FF_WORD

   word


.. py:data:: FF_DWORD

   double word


.. py:data:: FF_QWORD

   quadro word


.. py:data:: FF_TBYTE

   tbyte


.. py:data:: FF_STRLIT

   string literal


.. py:data:: FF_STRUCT

   struct variable


.. py:data:: FF_OWORD

   octaword/xmm word (16 bytes/128 bits)


.. py:data:: FF_FLOAT

   float


.. py:data:: FF_DOUBLE

   double


.. py:data:: FF_PACKREAL

   packed decimal real


.. py:data:: FF_ALIGN

   alignment directive


.. py:data:: FF_CUSTOM

   custom data type


.. py:data:: FF_YWORD

   ymm word (32 bytes/256 bits)


.. py:data:: FF_ZWORD

   zmm word (64 bytes/512 bits)


.. py:function:: code_flag() -> flags64_t

   FF_CODE


.. py:function:: byte_flag() -> flags64_t

   Get a flags64_t representing a byte.


.. py:function:: word_flag() -> flags64_t

   Get a flags64_t representing a word.


.. py:function:: dword_flag() -> flags64_t

   Get a flags64_t representing a double word.


.. py:function:: qword_flag() -> flags64_t

   Get a flags64_t representing a quad word.


.. py:function:: oword_flag() -> flags64_t

   Get a flags64_t representing a octaword.


.. py:function:: yword_flag() -> flags64_t

   Get a flags64_t representing a ymm word.


.. py:function:: zword_flag() -> flags64_t

   Get a flags64_t representing a zmm word.


.. py:function:: tbyte_flag() -> flags64_t

   Get a flags64_t representing a tbyte.


.. py:function:: strlit_flag() -> flags64_t

   Get a flags64_t representing a string literal.


.. py:function:: stru_flag() -> flags64_t

   Get a flags64_t representing a struct.


.. py:function:: cust_flag() -> flags64_t

   Get a flags64_t representing custom type data.


.. py:function:: align_flag() -> flags64_t

   Get a flags64_t representing an alignment directive.


.. py:function:: float_flag() -> flags64_t

   Get a flags64_t representing a float.


.. py:function:: double_flag() -> flags64_t

   Get a flags64_t representing a double.


.. py:function:: packreal_flag() -> flags64_t

   Get a flags64_t representing a packed decimal real.


.. py:function:: is_byte(F: flags64_t) -> bool

   FF_BYTE


.. py:function:: is_word(F: flags64_t) -> bool

   FF_WORD


.. py:function:: is_dword(F: flags64_t) -> bool

   FF_DWORD


.. py:function:: is_qword(F: flags64_t) -> bool

   FF_QWORD


.. py:function:: is_oword(F: flags64_t) -> bool

   FF_OWORD


.. py:function:: is_yword(F: flags64_t) -> bool

   FF_YWORD


.. py:function:: is_zword(F: flags64_t) -> bool

   FF_ZWORD


.. py:function:: is_tbyte(F: flags64_t) -> bool

   FF_TBYTE


.. py:function:: is_float(F: flags64_t) -> bool

   FF_FLOAT


.. py:function:: is_double(F: flags64_t) -> bool

   FF_DOUBLE


.. py:function:: is_pack_real(F: flags64_t) -> bool

   FF_PACKREAL


.. py:function:: is_strlit(F: flags64_t) -> bool

   FF_STRLIT


.. py:function:: is_struct(F: flags64_t) -> bool

   FF_STRUCT


.. py:function:: is_align(F: flags64_t) -> bool

   FF_ALIGN


.. py:function:: is_custom(F: flags64_t) -> bool

   FF_CUSTOM


.. py:function:: f_is_byte(F: flags64_t, arg2: void *) -> bool

   See is_byte()


.. py:function:: f_is_word(F: flags64_t, arg2: void *) -> bool

   See is_word()


.. py:function:: f_is_dword(F: flags64_t, arg2: void *) -> bool

   See is_dword()


.. py:function:: f_is_qword(F: flags64_t, arg2: void *) -> bool

   See is_qword()


.. py:function:: f_is_oword(F: flags64_t, arg2: void *) -> bool

   See is_oword()


.. py:function:: f_is_yword(F: flags64_t, arg2: void *) -> bool

   See is_yword()


.. py:function:: f_is_tbyte(F: flags64_t, arg2: void *) -> bool

   See is_tbyte()


.. py:function:: f_is_float(F: flags64_t, arg2: void *) -> bool

   See is_float()


.. py:function:: f_is_double(F: flags64_t, arg2: void *) -> bool

   See is_double()


.. py:function:: f_is_pack_real(F: flags64_t, arg2: void *) -> bool

   See is_pack_real()


.. py:function:: f_is_strlit(F: flags64_t, arg2: void *) -> bool

   See is_strlit()


.. py:function:: f_is_struct(F: flags64_t, arg2: void *) -> bool

   See is_struct()


.. py:function:: f_is_align(F: flags64_t, arg2: void *) -> bool

   See is_align()


.. py:function:: f_is_custom(F: flags64_t, arg2: void *) -> bool

   See is_custom()


.. py:function:: is_same_data_type(F1: flags64_t, F2: flags64_t) -> bool

   Do the given flags specify the same data type?


.. py:function:: get_flags_by_size(size: size_t) -> flags64_t

   Get flags from size (in bytes). Supported sizes: 1, 2, 4, 8, 16, 32. For other sizes returns 0 
           


.. py:function:: create_data(ea: ida_idaapi.ea_t, dataflag: flags64_t, size: asize_t, tid: tid_t) -> bool

   Convert to data (byte, word, dword, etc). This function may be used to create arrays. 
           
   :param ea: linear address
   :param dataflag: type of data. Value of function byte_flag(), word_flag(), etc.
   :param size: size of array in bytes. should be divisible by the size of one item of the specified type. for variable sized items it can be specified as 0, and the kernel will try to calculate the size.
   :param tid: type id. If the specified type is a structure, then tid is structure id. Otherwise should be BADNODE.
   :returns: success


.. py:function:: calc_dflags(f: flags64_t, force: bool) -> flags64_t

.. py:function:: create_byte(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to byte.


.. py:function:: create_word(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to word.


.. py:function:: create_dword(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to dword.


.. py:function:: create_qword(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to quadword.


.. py:function:: create_oword(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to octaword/xmm word.


.. py:function:: create_yword(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to ymm word.


.. py:function:: create_zword(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to zmm word.


.. py:function:: create_tbyte(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to tbyte.


.. py:function:: create_float(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to float.


.. py:function:: create_double(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to double.


.. py:function:: create_packed_real(ea: ida_idaapi.ea_t, length: asize_t, force: bool = False) -> bool

   Convert to packed decimal real.


.. py:function:: create_struct(ea: ida_idaapi.ea_t, length: asize_t, tid: tid_t, force: bool = False) -> bool

   Convert to struct.


.. py:function:: create_custdata(ea: ida_idaapi.ea_t, length: asize_t, dtid: int, fid: int, force: bool = False) -> bool

   Convert to custom data type.


.. py:function:: create_align(ea: ida_idaapi.ea_t, length: asize_t, alignment: int) -> bool

   Create an alignment item. 
           
   :param ea: linear address
   :param length: size of the item in bytes. 0 means to infer from ALIGNMENT
   :param alignment: alignment exponent. Example: 3 means align to 8 bytes. 0 means to infer from LENGTH It is forbidden to specify both LENGTH and ALIGNMENT as 0.
   :returns: success


.. py:function:: calc_min_align(length: asize_t) -> int

   Calculate the minimal possible alignment exponent. 
           
   :param length: size of the item in bytes.
   :returns: a value in the 1..32 range


.. py:function:: calc_max_align(endea: ida_idaapi.ea_t) -> int

   Calculate the maximal possible alignment exponent. 
           
   :param endea: end address of the alignment item.
   :returns: a value in the 0..32 range


.. py:function:: calc_def_align(ea: ida_idaapi.ea_t, mina: int, maxa: int) -> int

   Calculate the default alignment exponent. 
           
   :param ea: linear address
   :param mina: minimal possible alignment exponent.
   :param maxa: minimal possible alignment exponent.


.. py:function:: create_16bit_data(ea: ida_idaapi.ea_t, length: asize_t) -> bool

   Convert to 16-bit quantity (take the byte size into account)


.. py:function:: create_32bit_data(ea: ida_idaapi.ea_t, length: asize_t) -> bool

   Convert to 32-bit quantity (take the byte size into account)


.. py:data:: ALOPT_IGNHEADS

   don't stop if another data item is encountered. only the byte values will be used to determine the string length. if not set, a defined data item or instruction will truncate the string 
           


.. py:data:: ALOPT_IGNPRINT

   if set, don't stop at non-printable codepoints, but only at the terminating character (or not unicode-mapped character (e.g., 0x8f in CP1252)) 
           


.. py:data:: ALOPT_IGNCLT

   if set, don't stop at codepoints that are not part of the current 'culture'; accept all those that are graphical (this is typically used used by user-initiated actions creating string literals.) 
           


.. py:data:: ALOPT_MAX4K

   if string length is more than 4K, return the accumulated length 
           


.. py:data:: ALOPT_ONLYTERM

   only the termination characters can be at the string end. Without this option illegal characters also terminate the string. 
           


.. py:data:: ALOPT_APPEND

   if an existing strlit is encountered, then append it to the string. 
           


.. py:function:: get_max_strlit_length(ea: ida_idaapi.ea_t, strtype: int, options: int = 0) -> size_t

   Determine maximum length of string literal.
   If the string literal has a length prefix (e.g., STRTYPE_LEN2 has a two-byte length prefix), the length of that prefix (i.e., 2) will be part of the returned value.

   :param ea: starting address
   :param strtype: string type. one of String type codes
   :param options: combination of string literal length options
   :returns: length of the string in octets (octet==8bit)


.. py:data:: STRCONV_ESCAPE

   convert non-printable characters to C escapes (
   , \xNN, \uNNNN)


.. py:data:: STRCONV_REPLCHAR

   convert non-printable characters to the Unicode replacement character (U+FFFD)


.. py:data:: STRCONV_INCLLEN

   for Pascal-style strings, include the prefixing length byte(s) as C-escaped sequence


.. py:function:: create_strlit(start: ida_idaapi.ea_t, len: size_t, strtype: int) -> bool

   Convert to string literal and give a meaningful name. 'start' may be higher than 'end', the kernel will swap them in this case 
           
   :param start: starting address
   :param len: length of the string in bytes. if 0, then get_max_strlit_length() will be used to determine the length
   :param strtype: string type. one of String type codes
   :returns: success


.. py:data:: PSTF_TNORM

   use normal name


.. py:data:: PSTF_TBRIEF

   use brief name (e.g., in the 'Strings' window)


.. py:data:: PSTF_TINLIN

   use 'inline' name (e.g., in the structures comments)


.. py:data:: PSTF_TMASK

   type mask


.. py:data:: PSTF_HOTKEY

   have hotkey markers part of the name


.. py:data:: PSTF_ENC

   if encoding is specified, append it


.. py:data:: PSTF_ONLY_ENC

   generate only the encoding name


.. py:data:: PSTF_ATTRIB

   generate for type attribute usage


.. py:function:: get_opinfo(buf: opinfo_t, ea: ida_idaapi.ea_t, n: int, flags: flags64_t) -> opinfo_t *

   Get additional information about an operand representation. 
           
   :param buf: buffer to receive the result. may not be nullptr
   :param ea: linear address of item
   :param n: number of operand, 0 or 1
   :param flags: flags of the item
   :returns: nullptr if no additional representation information


.. py:function:: set_opinfo(ea: ida_idaapi.ea_t, n: int, flag: flags64_t, ti: opinfo_t, suppress_events: bool = False) -> bool

   Set additional information about an operand representation. This function is a low level one. Only the kernel should use it. 
           
   :param ea: linear address of the item
   :param n: number of operand, 0 or 1 (see the note below)
   :param flag: flags of the item
   :param ti: additional representation information
   :param suppress_events: do not generate changing_op_type and op_type_changed events
   :returns: success


.. py:function:: get_data_elsize(ea: ida_idaapi.ea_t, F: flags64_t, ti: opinfo_t = None) -> asize_t

   Get size of data type specified in flags 'F'. 
           
   :param ea: linear address of the item
   :param F: flags
   :param ti: additional information about the data type. For example, if the current item is a structure instance, then ti->tid is structure id. Otherwise is ignored (may be nullptr). If specified as nullptr, will be automatically retrieved from the database
   :returns: * byte : 1
   * word : 2
   * etc...


.. py:function:: get_full_data_elsize(ea: ida_idaapi.ea_t, F: flags64_t, ti: opinfo_t = None) -> asize_t

   Get full size of data type specified in flags 'F'. takes into account processors with wide bytes e.g. returns 2 for a byte element with 16-bit bytes 
           


.. py:function:: is_varsize_item(ea: ida_idaapi.ea_t, F: flags64_t, ti: opinfo_t = None, itemsize: asize_t * = None) -> int

   Is the item at 'ea' variable size?. 
           
   :param ea: linear address of the item
   :param F: flags
   :param ti: additional information about the data type. For example, if the current item is a structure instance, then ti->tid is structure id. Otherwise is ignored (may be nullptr). If specified as nullptr, will be automatically retrieved from the database
   :param itemsize: if not nullptr and the item is varsize, itemsize will contain the calculated item size (for struct types, the minimal size is returned)
   :returns: 1: varsize item
   :returns: 0: fixed item
   :returns: -1: error (bad data definition)


.. py:function:: get_possible_item_varsize(ea: ida_idaapi.ea_t, tif: tinfo_t) -> asize_t

   Return the possible size of the item at EA of type TIF if TIF is the variable structure. 
           
   :param ea: the linear address of the item
   :param tif: the item type
   :returns: the possible size
   :returns: asize_t(-1): TIF is not a variable structure


.. py:function:: can_define_item(ea: ida_idaapi.ea_t, length: asize_t, flags: flags64_t) -> bool

   Can define item (instruction/data) of the specified 'length', starting at 'ea'? 
   * a new item would cross segment boundaries
   * a new item would overlap with existing items (except items specified by 'flags') 


           
   :param ea: start of the range for the new item
   :param length: length of the new item in bytes
   :param flags: if not 0, then the kernel will ignore the data types specified by the flags and destroy them. For example: 
                    1000 dw 5
                    1002 db 5 ; undef
                    1003 db 5 ; undef
                    1004 dw 5
                    1006 dd 5
                     can_define_item(1000, 6, 0) - false because of dw at 1004 
    can_define_item(1000, 6, word_flag()) - true, word at 1004 is destroyed
   :returns: 1-yes, 0-no


.. py:data:: MS_CODE

   Mask for code bits.


.. py:data:: FF_FUNC

   function start?


.. py:data:: FF_IMMD

   Has Immediate value ?


.. py:data:: FF_JUMP

   Has jump table or switch_info?


.. py:function:: has_immd(F: flags64_t) -> bool

   Has immediate value?


.. py:function:: is_func(F: flags64_t) -> bool

   Is function start?


.. py:function:: set_immd(ea: ida_idaapi.ea_t) -> bool

   Set 'has immediate operand' flag. Returns true if the FF_IMMD bit was not set and now is set 
           


.. py:class:: data_type_t(_self: PyObject *, name: str, value_size: asize_t = 0, menu_name: str = None, hotkey: str = None, asm_keyword: str = None, props: int = 0)

   Bases: :py:obj:`object`


   Information about a data type


   .. py:attribute:: thisown


   .. py:attribute:: props
      :type:  int

      properties



   .. py:attribute:: name
      :type:  str

      name of the data type. must be unique



   .. py:attribute:: menu_name
      :type:  str

      Visible data type name to use in menus if nullptr, no menu item will be created 
              



   .. py:attribute:: hotkey
      :type:  str

      Hotkey for the corresponding menu item if nullptr, no hotkey will be associated with the menu item 
              



   .. py:attribute:: asm_keyword
      :type:  str

      keyword to use for this type in the assembly if nullptr, the data type cannot be used in the listing it can still be used in cpuregs window 
              



   .. py:attribute:: value_size
      :type:  asize_t

      size of the value in bytes



   .. py:method:: is_present_in_menus() -> bool

      Should this type be shown in UI menus 
              
      :returns: success



   .. py:attribute:: id


.. py:data:: DTP_NODUP

   do not use dup construct


.. py:class:: data_format_t(_self: PyObject *, name: str, value_size: asize_t = 0, menu_name: str = None, props: int = 0, hotkey: str = None, text_width: int = 0)

   Bases: :py:obj:`object`


   Information about a data format


   .. py:attribute:: thisown


   .. py:attribute:: props
      :type:  int

      properties (currently 0)



   .. py:attribute:: name
      :type:  str

      Format name, must be unique.



   .. py:attribute:: menu_name
      :type:  str

      Visible format name to use in menus if nullptr, no menu item will be created 
              



   .. py:attribute:: hotkey
      :type:  str

      Hotkey for the corresponding menu item if nullptr, no hotkey will be associated with the menu item 
              



   .. py:attribute:: value_size
      :type:  asize_t

      size of the value in bytes 0 means any size is ok data formats that are registered for standard types (dtid 0) may be called with any value_size (instruction operands only) 
              



   .. py:attribute:: text_width
      :type:  int

      Usual width of the text representation This value is used to calculate the width of the control to display values of this type 
              



   .. py:method:: is_present_in_menus() -> bool

      Should this format be shown in UI menus 
              
      :returns: success



   .. py:attribute:: id


.. py:function:: get_custom_data_type(dtid: int) -> data_type_t const *

   Get definition of a registered custom data type. 
           
   :param dtid: data type id
   :returns: data type definition or nullptr


.. py:function:: get_custom_data_format(dfid: int) -> data_format_t const *

   Get definition of a registered custom data format. 
           
   :param dfid: data format id
   :returns: data format definition or nullptr


.. py:function:: attach_custom_data_format(dtid: int, dfid: int) -> bool

   Attach the data format to the data type. 
           
   :param dtid: data type id that can use the data format. 0 means all standard data types. Such data formats can be applied to any data item or instruction operands. For instruction operands, the data_format_t::value_size check is not performed by the kernel.
   :param dfid: data format id
   :returns: true: ok
   :returns: false: no such `dtid`, or no such `dfid', or the data format has already been attached to the data type


.. py:function:: detach_custom_data_format(dtid: int, dfid: int) -> bool

   Detach the data format from the data type. Unregistering a custom data type detaches all attached data formats, no need to detach them explicitly. You still need unregister them. Unregistering a custom data format detaches it from all attached data types. 
           
   :param dtid: data type id to detach data format from
   :param dfid: data format id to detach
   :returns: true: ok
   :returns: false: no such `dtid`, or no such `dfid', or the data format was not attached to the data type


.. py:function:: is_attached_custom_data_format(dtid: int, dfid: int) -> bool

   Is the custom data format attached to the custom data type? 
           
   :param dtid: data type id
   :param dfid: data format id
   :returns: true or false


.. py:function:: get_custom_data_types(*args) -> int

   Get list of registered custom data type ids. 
           
   :param out: buffer for the output. may be nullptr
   :param min_size: minimum value size
   :param max_size: maximum value size
   :returns: number of custom data types with the specified size limits


.. py:function:: get_custom_data_formats(out: intvec_t *, dtid: int) -> int

   Get list of attached custom data formats for the specified data type. 
           
   :param out: buffer for the output. may be nullptr
   :param dtid: data type id
   :returns: number of returned custom data formats. if error, returns -1


.. py:function:: find_custom_data_type(name: str) -> int

   Get id of a custom data type. 
           
   :param name: name of the custom data type
   :returns: id or -1


.. py:function:: find_custom_data_format(name: str) -> int

   Get id of a custom data format. 
           
   :param name: name of the custom data format
   :returns: id or -1


.. py:function:: set_cmt(ea: ida_idaapi.ea_t, comm: str, rptble: bool) -> bool

   Set an indented comment. 
           
   :param ea: linear address
   :param comm: comment string
   * nullptr: do nothing (return 0)
   * "" : delete comment
   :param rptble: is repeatable?
   :returns: success


.. py:function:: get_cmt(ea: ida_idaapi.ea_t, rptble: bool) -> str

   Get an indented comment. 
           
   :param ea: linear address. may point to tail byte, the function will find start of the item
   :param rptble: get repeatable comment?
   :returns: size of comment or -1


.. py:function:: append_cmt(ea: ida_idaapi.ea_t, str: append_cmt.str, rptble: bool) -> bool

   Append to an indented comment. Creates a new comment if none exists. Appends a newline character and the specified string otherwise. 
           
   :param ea: linear address
   :param str: comment string to append
   :param rptble: append to repeatable comment?
   :returns: success


.. py:function:: get_predef_insn_cmt(ins: insn_t const &) -> str

   Get predefined comment. 
           
   :param ins: current instruction information
   :returns: size of comment or -1


.. py:function:: find_byte(sEA: ida_idaapi.ea_t, size: asize_t, value: uchar, bin_search_flags: int) -> ida_idaapi.ea_t

   Find forward a byte with the specified value (only 8-bit value from the database). example: ea=4 size=3 will inspect addresses 4, 5, and 6 
           
   :param sEA: linear address
   :param size: number of bytes to inspect
   :param value: value to find
   :param bin_search_flags: combination of Search flags
   :returns: address of byte or BADADDR


.. py:function:: find_byter(sEA: ida_idaapi.ea_t, size: asize_t, value: uchar, bin_search_flags: int) -> ida_idaapi.ea_t

   Find reverse a byte with the specified value (only 8-bit value from the database). example: ea=4 size=3 will inspect addresses 6, 5, and 4 
           
   :param sEA: the lower address of the search range
   :param size: number of bytes to inspect
   :param value: value to find
   :param bin_search_flags: combination of Search flags
   :returns: address of byte or BADADDR


.. py:class:: compiled_binpat_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: bytes
      :type:  bytevec_t


   .. py:attribute:: mask
      :type:  bytevec_t


   .. py:attribute:: strlits
      :type:  rangevec_t


   .. py:attribute:: encidx
      :type:  int


   .. py:method:: all_bytes_defined() -> bool


   .. py:method:: qclear() -> None


.. py:data:: PBSENC_DEF1BPU

   Use the default 1 byte-per-unit IDB encoding.


.. py:data:: PBSENC_ALL

   Use all IDB encodings.


.. py:function:: parse_binpat_str(out: compiled_binpat_vec_t, ea: ida_idaapi.ea_t, _in: str, radix: int, strlits_encoding: int = 0) -> bool

   Deprecated.

   Please use compiled_binpat_vec_t.from_pattern() instead.


.. py:function:: bin_search(*args)

   Search for a set of bytes in the program

   This function has the following signatures:

       1. bin_search(start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t, data: compiled_binpat_vec_t, flags: int) -> Tuple[ida_idaapi.ea_t, int]
       2. bin_search(start_ea: ida_idaapi.ea_t, end_ea: ida_idaapi.ea_t, image: bytes, mask: bytes, len: int, flags: int) -> ida_idaapi.ea_t

   The return value type will differ depending on the form:

       1. a tuple `(matched-address, index-in-compiled_binpat_vec_t)` (1st form)
       2. the address of a match, or ida_idaapi.BADADDR if not found (2nd form)

   This is a low-level function; more user-friendly alternatives
   are available. Please see 'find_bytes' and 'find_string'.

   :param start_ea: linear address, start of range to search
   :param end_ea: linear address, end of range to search (exclusive)
   :param data: (1st form) the prepared data to search for (see parse_binpat_str())
   :param bytes: (2nd form) a set of bytes to match
   :param mask: (2nd form) a mask to apply to the set of bytes
   :param flags: combination of BIN_SEARCH_* flags
   :returns: either a tuple holding both the address of the match and the index of the compiled pattern that matched, or the address of a match (ida_idaapi.BADADDR if not found)


.. py:data:: BIN_SEARCH_CASE

   case sensitive


.. py:data:: BIN_SEARCH_NOCASE

   case insensitive


.. py:data:: BIN_SEARCH_NOBREAK

   don't check for Ctrl-Break


.. py:data:: BIN_SEARCH_INITED

   find_byte, find_byter: any initilized value


.. py:data:: BIN_SEARCH_NOSHOW

   don't show search progress or update screen


.. py:data:: BIN_SEARCH_FORWARD

   search forward for bytes


.. py:data:: BIN_SEARCH_BACKWARD

   search backward for bytes


.. py:data:: BIN_SEARCH_BITMASK

   searching using strict bit mask


.. py:function:: next_inited(ea: ida_idaapi.ea_t, maxea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Find the next initialized address.


.. py:function:: prev_inited(ea: ida_idaapi.ea_t, minea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Find the previous initialized address.


.. py:function:: equal_bytes(ea: ida_idaapi.ea_t, image: uchar const *, mask: uchar const *, len: size_t, bin_search_flags: int) -> bool

   Compare 'len' bytes of the program starting from 'ea' with 'image'. 
           
   :param ea: linear address
   :param image: bytes to compare with
   :param mask: array of mask bytes, it's length is 'len'. if the flag BIN_SEARCH_BITMASK is passsed, 'bitwise AND' is used to compare. if not; 1 means to perform the comparison of the corresponding byte. 0 means not to perform. if mask == nullptr, then all bytes of 'image' will be compared. if mask == SKIP_FF_MASK then 0xFF bytes will be skipped
   :param len: length of block to compare in bytes.
   :param bin_search_flags: combination of Search flags
   :returns: 1: equal
   :returns: 0: not equal


.. py:class:: hidden_range_t

   Bases: :py:obj:`ida_range.range_t`


   .. py:attribute:: thisown


   .. py:attribute:: description
      :type:  char *

      description to display if the range is collapsed



   .. py:attribute:: header
      :type:  char *

      header lines to display if the range is expanded



   .. py:attribute:: footer
      :type:  char *

      footer lines to display if the range is expanded



   .. py:attribute:: visible
      :type:  bool

      the range state



   .. py:attribute:: color
      :type:  bgcolor_t

      range color



.. py:function:: update_hidden_range(ha: hidden_range_t) -> bool

   Update hidden range information in the database. You cannot use this function to change the range boundaries 
           
   :param ha: range to update
   :returns: success


.. py:function:: add_hidden_range(*args) -> bool

   Mark a range of addresses as hidden. The range will be created in the invisible state with the default color 
           
   :param ea1: linear address of start of the address range
   :param ea2: linear address of end of the address range
   :param description: range parameters
   :param header: range parameters
   :param footer: range parameters
   :param color: the range color
   :returns: success


.. py:function:: get_hidden_range(ea: ida_idaapi.ea_t) -> hidden_range_t *

   Get pointer to hidden range structure, in: linear address. 
           
   :param ea: any address in the hidden range


.. py:function:: getn_hidden_range(n: int) -> hidden_range_t *

   Get pointer to hidden range structure, in: number of hidden range. 
           
   :param n: number of hidden range, is in range 0..get_hidden_range_qty()-1


.. py:function:: get_hidden_range_qty() -> int

   Get number of hidden ranges.


.. py:function:: get_hidden_range_num(ea: ida_idaapi.ea_t) -> int

   Get number of a hidden range. 
           
   :param ea: any address in the hidden range
   :returns: number of hidden range (0..get_hidden_range_qty()-1)


.. py:function:: get_prev_hidden_range(ea: ida_idaapi.ea_t) -> hidden_range_t *

   Get pointer to previous hidden range. 
           
   :param ea: any address in the program
   :returns: ptr to hidden range or nullptr if previous hidden range doesn't exist


.. py:function:: get_next_hidden_range(ea: ida_idaapi.ea_t) -> hidden_range_t *

   Get pointer to next hidden range. 
           
   :param ea: any address in the program
   :returns: ptr to hidden range or nullptr if next hidden range doesn't exist


.. py:function:: get_first_hidden_range() -> hidden_range_t *

   Get pointer to the first hidden range. 
           
   :returns: ptr to hidden range or nullptr


.. py:function:: get_last_hidden_range() -> hidden_range_t *

   Get pointer to the last hidden range. 
           
   :returns: ptr to hidden range or nullptr


.. py:function:: del_hidden_range(ea: ida_idaapi.ea_t) -> bool

   Delete hidden range. 
           
   :param ea: any address in the hidden range
   :returns: success


.. py:function:: add_mapping(_from: ida_idaapi.ea_t, to: ida_idaapi.ea_t, size: asize_t) -> bool

   IDA supports memory mapping. References to the addresses from the mapped range use data and meta-data from the mapping range. 
           
   :param to: start of the mapping range (existent address)
   :param size: size of the range
   :returns: success


.. py:function:: del_mapping(ea: ida_idaapi.ea_t) -> None

   Delete memory mapping range. 
           
   :param ea: any address in the mapped range


.. py:function:: use_mapping(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Translate address according to current mappings. 
           
   :param ea: address to translate
   :returns: translated address


.. py:function:: get_mappings_qty() -> size_t

   Get number of mappings.


.. py:function:: get_mapping(n: size_t) -> ea_t *, ea_t *, asize_t *

   Get memory mapping range by its number. 
           
   :param n: number of mapping range (0..get_mappings_qty()-1)
   :returns: false if the specified range doesn't exist, otherwise returns `from`, `to`, `size`


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

.. py:data:: FF_0FLT

.. py:data:: FF_0CUST

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

.. py:data:: FF_1FLT

.. py:data:: FF_1CUST

.. py:function:: visit_patched_bytes(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, callable)

   Enumerates patched bytes in the given range and invokes a callable

   :param ea1: start address
   :param ea2: end address
   :param callable: a Python callable with the following prototype:
                    callable(ea, fpos, org_val, patch_val).
                    If the callable returns non-zero then that value will be
                    returned to the caller and the enumeration will be
                    interrupted.
   :returns: Zero if the enumeration was successful or the return
            value of the callback if enumeration was interrupted.


.. py:function:: get_bytes(ea: ida_idaapi.ea_t, size: int, gmb_flags: int = GMB_READALL)

   Get the specified number of bytes of the program.

   :param ea: program address
   :param size: number of bytes to return
   :param gmb_flags: OR'ed combination of GMB_* values (defaults to GMB_READALL)
   :returns: the bytes (as bytes object), or None in case of failure


.. py:function:: get_bytes_and_mask(ea: ida_idaapi.ea_t, size: int, gmb_flags: int = GMB_READALL)

   Get the specified number of bytes of the program, and a bitmask
   specifying what bytes are defined and what bytes are not.

   :param ea: program address
   :param size: number of bytes to return
   :param gmb_flags: OR'ed combination of GMB_* values (defaults to GMB_READALL)
   :returns: a tuple (bytes, mask), or None in case of failure.
            Both 'bytes' and 'mask' are 'str' instances.


.. py:function:: get_strlit_contents(ea: ida_idaapi.ea_t, len: int, type: int, flags: int = 0)

   Get contents of string literal, as UTF-8-encoded codepoints.
   It works even if the string has not been created in the database yet.

   Note that the returned value will be of type 'bytes'; if
   you want auto-conversion to unicode strings (that is: real Python
   strings), you should probably be using the idautils.Strings class.

   :param ea: linear address of the string
   :param len: length of the string in bytes (including terminating 0)
   :param type: type of the string. Represents both the character encoding,
                <u>and</u> the 'type' of string at the given location.
   :param flags: combination of STRCONV_..., to perform output conversion.
   :returns: a bytes-filled str object.


.. py:function:: print_strlit_type(strtype: int, flags: int = 0) -> PyObject *

   Get string type information: the string type name (possibly decorated with hotkey markers), and the tooltip.

   :param strtype: the string type
   :param flags: or'ed PSTF_* constants
   :returns: length of generated text


.. py:function:: op_stroff(*args) -> bool

   Set operand representation to be 'struct offset'.

   This function has the following signatures:

       1. op_stroff(ins: ida_ua.insn_t, n: int, path: List[int], delta: int)
       2. op_stroff(ins: ida_ua.insn_t, n: int, path: ida_pro.tid_array, path_len: int, delta: int) (backward-compatibility only)

   Here is an example using this function:

       ins = ida_ua.insn_t()
       if ida_ua.decode_insn(ins, some_address):
           operand = 0
           path = [ida_typeinf.get_named_type_tid("my_stucture_t")] # a one-element path
           ida_bytes.op_stroff(ins, operand, path, 0)


.. py:function:: get_stroff_path(*args)

   Get the structure offset path for operand `n`, at the
   specified address.

   This function has the following signatures:

       1. get_stroff_path(ea: ida_idaapi.ea_t, n : int) -> Tuple[List[int], int]
       2. get_stroff_path(path: tid_array, delta: sval_pointer, ea: ida_idaapi.ea_t, n : int) (backward-compatibility only)

   :param ea: address where the operand holds a path to a structure offset (1st form)
   :param n: operand number (1st form)
   :returns: a tuple holding a (list_of_tid_t's, delta_within_the_last_type), or (None, None)


.. py:function:: register_custom_data_type(dt)

   Registers a custom data type.

   :param dt: an instance of the data_type_t class
   :returns: < 0 if failed to register
   :returns: > 0 data type id


.. py:function:: unregister_custom_data_type(dtid)

   Unregisters a custom data type.

   :param dtid: the data type id
   :returns: Boolean


.. py:function:: register_custom_data_format(df)

   Registers a custom data format with a given data type.

   :param df: an instance of data_format_t
   :returns: < 0 if failed to register
   :returns: > 0 data format id


.. py:function:: unregister_custom_data_format(dfid)

   Unregisters a custom data format

   :param dfid: data format id
   :returns: Boolean


.. py:data:: DTP_NODUP
   :value: 1


   do not use dup construct


.. py:function:: register_data_types_and_formats(formats)

   Registers multiple data types and formats at once.
   To register one type/format at a time use register_custom_data_type/register_custom_data_format

   It employs a special table of types and formats described below:

   The 'formats' is a list of tuples. If a tuple has one element then it is the format to be registered with dtid=0
   If the tuple has more than one element, then tuple[0] is the data type and tuple[1:] are the data formats. For example:
   many_formats = [
     (pascal_data_type(), pascal_data_format()),
     (simplevm_data_type(), simplevm_data_format()),
     (makedword_data_format(),),
     (simplevm_data_format(),)
   ]
   The first two tuples describe data types and their associated formats.
   The last two tuples describe two data formats to be used with built-in data types.
   The data format may be attached to several data types. The id of the
   data format is stored in the first data_format_t object. For example:
   assert many_formats[1][1] != -1
   assert many_formats[2][0] != -1
   assert many_formats[3][0] == -1


.. py:function:: unregister_data_types_and_formats(formats)

   As opposed to register_data_types_and_formats(), this function
   unregisters multiple data types and formats at once.


.. py:function:: find_bytes(bs: Union[bytes, bytearray, str], range_start: int, range_size: Optional[int] = None, range_end: Optional[int] = ida_idaapi.BADADDR, mask: Optional[Union[bytes, bytearray]] = None, flags: Optional[int] = BIN_SEARCH_FORWARD | BIN_SEARCH_NOSHOW, radix: Optional[int] = 16, strlit_encoding: Optional[Union[int, str]] = PBSENC_DEF1BPU) -> int

.. py:function:: find_string(_str: str, range_start: int, range_end: Optional[int] = ida_idaapi.BADADDR, range_size: Optional[int] = None, strlit_encoding: Optional[Union[int, str]] = PBSENC_DEF1BPU, flags: Optional[int] = BIN_SEARCH_FORWARD | BIN_SEARCH_NOSHOW) -> int


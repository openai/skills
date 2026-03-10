ida_segment
===========

.. py:module:: ida_segment

.. autoapi-nested-parse::

   Functions that deal with segments.

   IDA requires that all program addresses belong to segments (each address must 
   belong to exactly one segment). The situation when an address doesn't belong to 
   any segment is allowed as a temporary situation only when the user changes 
   program segmentation. Bytes outside a segment can't be converted to instructions, 
   have names, comments, etc. Each segment has its start address, ending address 
   and represents a contiguous range of addresses. There might be unused holes 
   between segments.

   Each segment has its unique segment selector. This selector is used to 
   distinguish the segment from other segments. For 16-bit programs the selector 
   is equal to the segment base paragraph. For 32-bit programs there is special 
   array to translate the selectors to the segment base paragraphs. A selector is 
   a 32/64 bit value.

   The segment base paragraph determines the offsets in the segment. If the start 
   address of the segment == (base << 4) then the first offset in the segment will 
   be 0. The start address should be higher or equal to (base << 4). We will call 
   the offsets in the segment 'virtual addresses'. So, the virtual address of the 
   first byte of the segment is (start address of segment - segment base linear 
   address).

   For IBM PC, the virtual address corresponds to the offset part of the address. 
   For other processors (Z80, for example), virtual addresses correspond to Z80 
   addresses and linear addresses are used only internally. For MS Windows programs 
   the segment base paragraph is 0 and therefore the segment virtual addresses are 
   equal to linear addresses.

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For segment operations, see :mod:`ida_domain.segments`.



Attributes
----------

.. autoapisummary::

   ida_segment.SREG_NUM
   ida_segment.saAbs
   ida_segment.saRelByte
   ida_segment.saRelWord
   ida_segment.saRelPara
   ida_segment.saRelPage
   ida_segment.saRelDble
   ida_segment.saRel4K
   ida_segment.saGroup
   ida_segment.saRel32Bytes
   ida_segment.saRel64Bytes
   ida_segment.saRelQword
   ida_segment.saRel128Bytes
   ida_segment.saRel512Bytes
   ida_segment.saRel1024Bytes
   ida_segment.saRel2048Bytes
   ida_segment.saRel_MAX_ALIGN_CODE
   ida_segment.scPriv
   ida_segment.scGroup
   ida_segment.scPub
   ida_segment.scPub2
   ida_segment.scStack
   ida_segment.scCommon
   ida_segment.scPub3
   ida_segment.sc_MAX_COMB_CODE
   ida_segment.SEGPERM_EXEC
   ida_segment.SEGPERM_WRITE
   ida_segment.SEGPERM_READ
   ida_segment.SEGPERM_MAXVAL
   ida_segment.SEG_MAX_BITNESS_CODE
   ida_segment.SFL_COMORG
   ida_segment.SFL_OBOK
   ida_segment.SFL_HIDDEN
   ida_segment.SFL_DEBUG
   ida_segment.SFL_LOADER
   ida_segment.SFL_HIDETYPE
   ida_segment.SFL_HEADER
   ida_segment.SEG_NORM
   ida_segment.SEG_XTRN
   ida_segment.SEG_CODE
   ida_segment.SEG_DATA
   ida_segment.SEG_IMP
   ida_segment.SEG_GRP
   ida_segment.SEG_NULL
   ida_segment.SEG_UNDF
   ida_segment.SEG_BSS
   ida_segment.SEG_ABSSYM
   ida_segment.SEG_COMM
   ida_segment.SEG_IMEM
   ida_segment.SEG_MAX_SEGTYPE_CODE
   ida_segment.ADDSEG_NOSREG
   ida_segment.ADDSEG_OR_DIE
   ida_segment.ADDSEG_NOTRUNC
   ida_segment.ADDSEG_QUIET
   ida_segment.ADDSEG_FILLGAP
   ida_segment.ADDSEG_SPARSE
   ida_segment.ADDSEG_NOAA
   ida_segment.ADDSEG_IDBENC
   ida_segment.SEGMOD_KILL
   ida_segment.SEGMOD_KEEP
   ida_segment.SEGMOD_SILENT
   ida_segment.SEGMOD_KEEP0
   ida_segment.SEGMOD_KEEPSEL
   ida_segment.SEGMOD_NOMOVE
   ida_segment.SEGMOD_SPARSE
   ida_segment.MOVE_SEGM_OK
   ida_segment.MOVE_SEGM_PARAM
   ida_segment.MOVE_SEGM_ROOM
   ida_segment.MOVE_SEGM_IDP
   ida_segment.MOVE_SEGM_CHUNK
   ida_segment.MOVE_SEGM_LOADER
   ida_segment.MOVE_SEGM_ODD
   ida_segment.MOVE_SEGM_ORPHAN
   ida_segment.MOVE_SEGM_DEBUG
   ida_segment.MOVE_SEGM_SOURCEFILES
   ida_segment.MOVE_SEGM_MAPPING
   ida_segment.MOVE_SEGM_INVAL
   ida_segment.MSF_SILENT
   ida_segment.MSF_NOFIX
   ida_segment.MSF_LDKEEP
   ida_segment.MSF_FIXONCE
   ida_segment.MSF_PRIORITY
   ida_segment.MSF_NETNODES
   ida_segment.CSS_OK
   ida_segment.CSS_NODBG
   ida_segment.CSS_NORANGE
   ida_segment.CSS_NOMEM
   ida_segment.CSS_BREAK
   ida_segment.SNAP_ALL_SEG
   ida_segment.SNAP_LOAD_SEG
   ida_segment.SNAP_CUR_SEG
   ida_segment.MAX_GROUPS
   ida_segment.MAX_SEGM_TRANSLATIONS


Classes
-------

.. autoapisummary::

   ida_segment.segment_defsr_array
   ida_segment.segment_t
   ida_segment.lock_segment


Functions
---------

.. autoapisummary::

   ida_segment.set_segment_translations
   ida_segment.is_visible_segm
   ida_segment.is_finally_visible_segm
   ida_segment.set_visible_segm
   ida_segment.is_spec_segm
   ida_segment.is_spec_ea
   ida_segment.lock_segm
   ida_segment.is_segm_locked
   ida_segment.getn_selector
   ida_segment.get_selector_qty
   ida_segment.setup_selector
   ida_segment.allocate_selector
   ida_segment.find_free_selector
   ida_segment.set_selector
   ida_segment.del_selector
   ida_segment.sel2para
   ida_segment.sel2ea
   ida_segment.find_selector
   ida_segment.get_segm_by_sel
   ida_segment.add_segm_ex
   ida_segment.add_segm
   ida_segment.del_segm
   ida_segment.get_segm_qty
   ida_segment.getseg
   ida_segment.getnseg
   ida_segment.get_segm_num
   ida_segment.get_next_seg
   ida_segment.get_prev_seg
   ida_segment.get_first_seg
   ida_segment.get_last_seg
   ida_segment.get_segm_by_name
   ida_segment.set_segm_end
   ida_segment.set_segm_start
   ida_segment.move_segm_start
   ida_segment.move_segm_strerror
   ida_segment.move_segm
   ida_segment.change_segment_status
   ida_segment.take_memory_snapshot
   ida_segment.is_miniidb
   ida_segment.set_segm_base
   ida_segment.set_group_selector
   ida_segment.get_group_selector
   ida_segment.add_segment_translation
   ida_segment.del_segment_translations
   ida_segment.get_segment_translations
   ida_segment.get_segment_cmt
   ida_segment.set_segment_cmt
   ida_segment.std_out_segm_footer
   ida_segment.set_segm_name
   ida_segment.get_segm_name
   ida_segment.get_visible_segm_name
   ida_segment.get_segm_class
   ida_segment.set_segm_class
   ida_segment.segtype
   ida_segment.get_segment_alignment
   ida_segment.get_segment_combination
   ida_segment.get_segm_para
   ida_segment.get_segm_base
   ida_segment.set_segm_addressing
   ida_segment.update_segm
   ida_segment.segm_adjust_diff
   ida_segment.segm_adjust_ea
   ida_segment.get_defsr
   ida_segment.set_defsr
   ida_segment.rebase_program


Module Contents
---------------

.. py:class:: segment_defsr_array(data: unsigned long long (&)[SREG_NUM])

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  unsigned long long (&)[SREG_NUM]


   .. py:attribute:: bytes


.. py:function:: set_segment_translations(segstart: ida_idaapi.ea_t, transmap: eavec_t const &) -> bool

   Set new translation list. 
           
   :param segstart: start address of the segment to add translation to
   :param transmap: vector of segment start addresses for the translation list. If transmap is empty, the translation list is deleted.
   :returns: 1: ok
   :returns: 0: too many translations or bad segstart


.. py:data:: SREG_NUM

   Maximum number of segment registers is 16 (see segregs.hpp)


.. py:class:: segment_t

   Bases: :py:obj:`ida_range.range_t`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  int

      use get/set_segm_name() functions



   .. py:attribute:: sclass
      :type:  int

      use get/set_segm_class() functions



   .. py:attribute:: orgbase
      :type:  int

      this field is IDP dependent. you may keep your information about the segment here 
              



   .. py:attribute:: align
      :type:  uchar

      Segment alignment codes 
              



   .. py:attribute:: comb
      :type:  uchar

      Segment combination codes 
              



   .. py:attribute:: perm
      :type:  uchar

      Segment permissions (0 means no information) 
              



   .. py:attribute:: bitness
      :type:  uchar

      Number of bits in the segment addressing
      * 0: 16 bits
      * 1: 32 bits
      * 2: 64 bits 


              



   .. py:method:: is_16bit() -> bool

      Is a 16-bit segment?



   .. py:method:: is_32bit() -> bool

      Is a 32-bit segment?



   .. py:method:: is_64bit() -> bool

      Is a 64-bit segment?



   .. py:method:: abits() -> int

      Get number of address bits.



   .. py:method:: abytes() -> int

      Get number of address bytes.



   .. py:attribute:: flags
      :type:  ushort

      Segment flags



   .. py:method:: comorg() -> bool


   .. py:method:: set_comorg() -> None


   .. py:method:: clr_comorg() -> None


   .. py:method:: ob_ok() -> bool


   .. py:method:: set_ob_ok() -> None


   .. py:method:: clr_ob_ok() -> None


   .. py:method:: is_visible_segm() -> bool


   .. py:method:: set_visible_segm(visible: bool) -> None


   .. py:method:: set_debugger_segm(debseg: bool) -> None


   .. py:method:: is_loader_segm() -> bool


   .. py:method:: set_loader_segm(ldrseg: bool) -> None


   .. py:method:: is_hidden_segtype() -> bool


   .. py:method:: set_hidden_segtype(hide: bool) -> None


   .. py:method:: is_header_segm() -> bool


   .. py:method:: set_header_segm(on: bool) -> None


   .. py:attribute:: sel
      :type:  sel_t

      segment selector - should be unique. You can't change this field after creating the segment. Exception: 16bit OMF files may have several segments with the same selector, but this is not good (no way to denote a segment exactly) so it should be fixed in the future. 
              



   .. py:attribute:: defsr
      :type:  sel_t [16]

      default segment register values. first element of this array keeps information about value of processor_t::reg_first_sreg 
              



   .. py:attribute:: type
      :type:  uchar

      segment type (see Segment types). The kernel treats different segment types differently. Segments marked with '*' contain no instructions or data and are not declared as 'segments' in the disassembly. 
              



   .. py:attribute:: color
      :type:  bgcolor_t

      the segment color



   .. py:method:: update() -> bool

      Update segment information. You must call this function after modification of segment characteristics. Note that not all fields of segment structure may be modified directly, there are special functions to modify some fields. 
              
      :returns: success



   .. py:attribute:: start_ea
      :type:  ida_idaapi.ea_t

      start_ea included



   .. py:attribute:: end_ea
      :type:  ida_idaapi.ea_t

      end_ea excluded



   .. py:attribute:: use64


.. py:data:: saAbs

   Absolute segment.


.. py:data:: saRelByte

   Relocatable, byte aligned.


.. py:data:: saRelWord

   Relocatable, word (2-byte) aligned.


.. py:data:: saRelPara

   Relocatable, paragraph (16-byte) aligned.


.. py:data:: saRelPage

   Relocatable, aligned on 256-byte boundary.


.. py:data:: saRelDble

   Relocatable, aligned on a double word (4-byte) boundary. 
           


.. py:data:: saRel4K

   This value is used by the PharLap OMF for page (4K) alignment. It is not supported by LINK. 
           


.. py:data:: saGroup

   Segment group.


.. py:data:: saRel32Bytes

   32 bytes


.. py:data:: saRel64Bytes

   64 bytes


.. py:data:: saRelQword

   8 bytes


.. py:data:: saRel128Bytes

   128 bytes


.. py:data:: saRel512Bytes

   512 bytes


.. py:data:: saRel1024Bytes

   1024 bytes


.. py:data:: saRel2048Bytes

   2048 bytes


.. py:data:: saRel_MAX_ALIGN_CODE

.. py:data:: scPriv

   Private. Do not combine with any other program segment. 
           


.. py:data:: scGroup

   Segment group.


.. py:data:: scPub

   Public. Combine by appending at an offset that meets the alignment requirement. 
           


.. py:data:: scPub2

   As defined by Microsoft, same as C=2 (public).


.. py:data:: scStack

   Stack. Combine as for C=2. This combine type forces byte alignment. 
           


.. py:data:: scCommon

   Common. Combine by overlay using maximum size.


.. py:data:: scPub3

   As defined by Microsoft, same as C=2 (public).


.. py:data:: sc_MAX_COMB_CODE

.. py:data:: SEGPERM_EXEC

   Execute.


.. py:data:: SEGPERM_WRITE

   Write.


.. py:data:: SEGPERM_READ

   Read.


.. py:data:: SEGPERM_MAXVAL

   Execute + Write + Read.


.. py:data:: SEG_MAX_BITNESS_CODE

   Maximum segment bitness value.


.. py:data:: SFL_COMORG

   IDP dependent field (IBM PC: if set, ORG directive is not commented out) 
           


.. py:data:: SFL_OBOK

   Orgbase is present? (IDP dependent field) 
           


.. py:data:: SFL_HIDDEN

   Is the segment hidden? 
           


.. py:data:: SFL_DEBUG

   Is the segment created for the debugger?. Such segments are temporary and do not have permanent flags. 
           


.. py:data:: SFL_LOADER

   Is the segment created by the loader? 
           


.. py:data:: SFL_HIDETYPE

   Hide segment type (do not print it in the listing) 
           


.. py:data:: SFL_HEADER

   Header segment (do not create offsets to it in the disassembly) 
           


.. py:data:: SEG_NORM

   unknown type, no assumptions


.. py:data:: SEG_XTRN

   * segment with 'extern' definitions. no instructions are allowed 
           


.. py:data:: SEG_CODE

   code segment


.. py:data:: SEG_DATA

   data segment


.. py:data:: SEG_IMP

   java: implementation segment


.. py:data:: SEG_GRP

   * group of segments


.. py:data:: SEG_NULL

   zero-length segment


.. py:data:: SEG_UNDF

   undefined segment type (not used)


.. py:data:: SEG_BSS

   uninitialized segment


.. py:data:: SEG_ABSSYM

   * segment with definitions of absolute symbols


.. py:data:: SEG_COMM

   * segment with communal definitions


.. py:data:: SEG_IMEM

   internal processor memory & sfr (8051)


.. py:data:: SEG_MAX_SEGTYPE_CODE

   maximum value segment type can take


.. py:function:: is_visible_segm(s: segment_t) -> bool

   See SFL_HIDDEN.


.. py:function:: is_finally_visible_segm(s: segment_t) -> bool

   See SFL_HIDDEN, SCF_SHHID_SEGM.


.. py:function:: set_visible_segm(s: segment_t, visible: bool) -> None

   See SFL_HIDDEN.


.. py:function:: is_spec_segm(seg_type: uchar) -> bool

   Has segment a special type?. (SEG_XTRN, SEG_GRP, SEG_ABSSYM, SEG_COMM) 
           


.. py:function:: is_spec_ea(ea: ida_idaapi.ea_t) -> bool

   Does the address belong to a segment with a special type?. (SEG_XTRN, SEG_GRP, SEG_ABSSYM, SEG_COMM) 
           
   :param ea: linear address


.. py:function:: lock_segm(segm: segment_t, lock: bool) -> None

   Lock segment pointer Locked pointers are guaranteed to remain valid until they are unlocked. Ranges with locked pointers cannot be deleted or moved. 
           


.. py:class:: lock_segment(_segm: segment_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


.. py:function:: is_segm_locked(segm: segment_t) -> bool

   Is a segment pointer locked?


.. py:function:: getn_selector(n: int) -> sel_t *, ea_t *

   Get description of selector (0..get_selector_qty()-1)


.. py:function:: get_selector_qty() -> size_t

   Get number of defined selectors.


.. py:function:: setup_selector(segbase: ida_idaapi.ea_t) -> sel_t

   Allocate a selector for a segment if necessary. You must call this function before calling add_segm_ex(). add_segm() calls this function itself, so you don't need to allocate a selector. This function will allocate a selector if 'segbase' requires more than 16 bits and the current processor is IBM PC. Otherwise it will return the segbase value. 
           
   :param segbase: a new segment base paragraph
   :returns: the allocated selector number


.. py:function:: allocate_selector(segbase: ida_idaapi.ea_t) -> sel_t

   Allocate a selector for a segment unconditionally. You must call this function before calling add_segm_ex(). add_segm() calls this function itself, so you don't need to allocate a selector. This function will allocate a new free selector and setup its mapping using find_free_selector() and set_selector() functions. 
           
   :param segbase: a new segment base paragraph
   :returns: the allocated selector number


.. py:function:: find_free_selector() -> sel_t

   Find first unused selector. 
           
   :returns: a number >= 1


.. py:function:: set_selector(selector: sel_t, paragraph: ida_idaapi.ea_t) -> int

   Set mapping of selector to a paragraph. You should call this function _before_ creating a segment which uses the selector, otherwise the creation of the segment will fail. 
           
   :param selector: number of selector to map
   * if selector == BADSEL, then return 0 (fail)
   * if the selector has had a mapping, old mapping is destroyed
   * if the selector number is equal to paragraph value, then the mapping is destroyed because we don't need to keep trivial mappings.
   :param paragraph: paragraph to map selector
   :returns: 1: ok
   :returns: 0: failure (bad selector or too many mappings)


.. py:function:: del_selector(selector: sel_t) -> None

   Delete mapping of a selector. Be wary of deleting selectors that are being used in the program, this can make a mess in the segments. 
           
   :param selector: number of selector to remove from the translation table


.. py:function:: sel2para(selector: sel_t) -> ida_idaapi.ea_t

   Get mapping of a selector. 
           
   :param selector: number of selector to translate
   :returns: paragraph the specified selector is mapped to. if there is no mapping, returns 'selector'.


.. py:function:: sel2ea(selector: sel_t) -> ida_idaapi.ea_t

   Get mapping of a selector as a linear address. 
           
   :param selector: number of selector to translate to linear address
   :returns: linear address the specified selector is mapped to. if there is no mapping, returns to_ea(selector,0);


.. py:function:: find_selector(base: ida_idaapi.ea_t) -> sel_t

   Find a selector that has mapping to the specified paragraph. 
           
   :param base: paragraph to search in the translation table
   :returns: selector value or base


.. py:function:: get_segm_by_sel(selector: sel_t) -> segment_t *

   Get pointer to segment structure. This function finds a segment by its selector. If there are several segments with the same selectors, the last one will be returned. 
           
   :param selector: a segment with the specified selector will be returned
   :returns: pointer to segment or nullptr


.. py:function:: add_segm_ex(NONNULL_s: segment_t, name: str, sclass: str, flags: int) -> bool

   Add a new segment. If a segment already exists at the specified range of addresses, this segment will be truncated. Instructions and data in the old segment will be deleted if the new segment has another addressing mode or another segment base address. 
           
   :param name: name of new segment. may be nullptr. if specified, the segment is immediately renamed
   :param sclass: class of the segment. may be nullptr. if specified, the segment class is immediately changed
   :param flags: Add segment flags
   :returns: 1: ok
   :returns: 0: failed, a warning message is displayed


.. py:data:: ADDSEG_NOSREG

   set all default segment register values to BADSEL (undefine all default segment registers) 
           


.. py:data:: ADDSEG_OR_DIE

   qexit() if can't add a segment


.. py:data:: ADDSEG_NOTRUNC

   don't truncate the new segment at the beginning of the next segment if they overlap. destroy/truncate old segments instead. 
           


.. py:data:: ADDSEG_QUIET

   silent mode, no "Adding segment..." in the messages window


.. py:data:: ADDSEG_FILLGAP

   fill gap between new segment and previous one. i.e. if such a gap exists, and this gap is less than 64K, then fill the gap by extending the previous segment and adding .align directive to it. This way we avoid gaps between segments. too many gaps lead to a virtual array failure. it cannot hold more than ~1000 gaps. 
           


.. py:data:: ADDSEG_SPARSE

   use sparse storage method for the new ranges of the created segment. please note that the ranges that were already enabled before creating the segment will not change their storage type. 
           


.. py:data:: ADDSEG_NOAA

   do not mark new segment for auto-analysis


.. py:data:: ADDSEG_IDBENC

   'name' and 'sclass' are given in the IDB encoding; non-ASCII bytes will be decoded accordingly 
           


.. py:function:: add_segm(para: ida_idaapi.ea_t, start: ida_idaapi.ea_t, end: ida_idaapi.ea_t, name: str, sclass: str, flags: int = 0) -> bool

   Add a new segment, second form. Segment alignment is set to saRelByte. Segment combination is "public" or "stack" (if segment class is "STACK"). Addressing mode of segment is taken as default (16bit or 32bit). Default segment registers are set to BADSEL. If a segment already exists at the specified range of addresses, this segment will be truncated. Instructions and data in the old segment will be deleted if the new segment has another addressing mode or another segment base address. 
           
   :param para: segment base paragraph. if paragraph can't fit in 16bit, then a new selector is allocated and mapped to the paragraph.
   :param start: start address of the segment. if start==BADADDR then start <- to_ea(para,0).
   :param end: end address of the segment. end address should be higher than start address. For emulate empty segments, use SEG_NULL segment type. If the end address is lower than start address, then fail. If end==BADADDR, then a segment up to the next segment will be created (if the next segment doesn't exist, then 1 byte segment will be created). If 'end' is too high and the new segment would overlap the next segment, 'end' is adjusted properly.
   :param name: name of new segment. may be nullptr
   :param sclass: class of the segment. may be nullptr. type of the new segment is modified if class is one of predefined names:
   * "CODE" -> SEG_CODE
   * "DATA" -> SEG_DATA
   * "CONST" -> SEG_DATA
   * "STACK" -> SEG_BSS
   * "BSS" -> SEG_BSS
   * "XTRN" -> SEG_XTRN
   * "COMM" -> SEG_COMM
   * "ABS" -> SEG_ABSSYM
   :param flags: Add segment flags
   :returns: 1: ok
   :returns: 0: failed, a warning message is displayed


.. py:function:: del_segm(ea: ida_idaapi.ea_t, flags: int) -> bool

   Delete a segment. 
           
   :param ea: any address belonging to the segment
   :param flags: Segment modification flags
   :returns: 1: ok
   :returns: 0: failed, no segment at 'ea'.


.. py:data:: SEGMOD_KILL

   disable addresses if segment gets shrinked or deleted


.. py:data:: SEGMOD_KEEP

   keep information (code & data, etc)


.. py:data:: SEGMOD_SILENT

   be silent


.. py:data:: SEGMOD_KEEP0

   flag for internal use, don't set


.. py:data:: SEGMOD_KEEPSEL

   do not try to delete unused selector


.. py:data:: SEGMOD_NOMOVE

   don't move info from the start of segment to the new start address (for set_segm_start()) 
           


.. py:data:: SEGMOD_SPARSE

   use sparse storage if extending the segment (for set_segm_start(), set_segm_end()) 
           


.. py:function:: get_segm_qty() -> int

   Get number of segments.


.. py:function:: getseg(ea: ida_idaapi.ea_t) -> segment_t *

   Get pointer to segment by linear address. 
           
   :param ea: linear address belonging to the segment
   :returns: nullptr or pointer to segment structure


.. py:function:: getnseg(n: int) -> segment_t *

   Get pointer to segment by its number. 
           
   :param n: segment number in the range (0..get_segm_qty()-1)
   :returns: nullptr or pointer to segment structure


.. py:function:: get_segm_num(ea: ida_idaapi.ea_t) -> int

   Get number of segment by address. 
           
   :param ea: linear address belonging to the segment
   :returns: -1 if no segment occupies the specified address. otherwise returns number of the specified segment (0..get_segm_qty()-1)


.. py:function:: get_next_seg(ea: ida_idaapi.ea_t) -> segment_t *

   Get pointer to the next segment.


.. py:function:: get_prev_seg(ea: ida_idaapi.ea_t) -> segment_t *

   Get pointer to the previous segment.


.. py:function:: get_first_seg() -> segment_t *

   Get pointer to the first segment.


.. py:function:: get_last_seg() -> segment_t *

   Get pointer to the last segment.


.. py:function:: get_segm_by_name(name: str) -> segment_t *

   Get pointer to segment by its name. If there are several segments with the same name, returns the first of them. 
           
   :param name: segment name. may be nullptr.
   :returns: nullptr or pointer to segment structure


.. py:function:: set_segm_end(ea: ida_idaapi.ea_t, newend: ida_idaapi.ea_t, flags: int) -> bool

   Set segment end address. The next segment is shrinked to allow expansion of the specified segment. The kernel might even delete the next segment if necessary. The kernel will ask the user for a permission to destroy instructions or data going out of segment scope if such instructions exist. 
           
   :param ea: any address belonging to the segment
   :param newend: new end address of the segment
   :param flags: Segment modification flags
   :returns: 1: ok
   :returns: 0: failed, a warning message is displayed


.. py:function:: set_segm_start(ea: ida_idaapi.ea_t, newstart: ida_idaapi.ea_t, flags: int) -> bool

   Set segment start address. The previous segment is trimmed to allow expansion of the specified segment. The kernel might even delete the previous segment if necessary. The kernel will ask the user for a permission to destroy instructions or data going out of segment scope if such instructions exist. 
           
   :param ea: any address belonging to the segment
   :param newstart: new start address of the segment note that segment start address should be higher than segment base linear address.
   :param flags: Segment modification flags
   :returns: 1: ok
   :returns: 0: failed, a warning message is displayed


.. py:function:: move_segm_start(ea: ida_idaapi.ea_t, newstart: ida_idaapi.ea_t, mode: int) -> bool

   Move segment start. The main difference between this function and set_segm_start() is that this function may expand the previous segment while set_segm_start() never does it. So, this function allows to change bounds of two segments simultaneously. If the previous segment and the specified segment have the same addressing mode and segment base, then instructions and data are not destroyed - they simply move from one segment to another. Otherwise all instructions/data which migrate from one segment to another are destroyed. 
           
   :param ea: any address belonging to the segment
   :param newstart: new start address of the segment note that segment start address should be higher than segment base linear address.
   :param mode: policy for destroying defined items
   * 0: if it is necessary to destroy defined items, display a dialog box and ask confirmation
   * 1: if it is necessary to destroy defined items, just destroy them without asking the user
   * -1: if it is necessary to destroy defined items, don't destroy them (i.e. function will fail)
   * -2: don't destroy defined items (function will succeed)
   :returns: 1: ok
   :returns: 0: failed, a warning message is displayed


.. py:data:: MOVE_SEGM_OK

   all ok


.. py:data:: MOVE_SEGM_PARAM

   The specified segment does not exist.


.. py:data:: MOVE_SEGM_ROOM

   Not enough free room at the target address.


.. py:data:: MOVE_SEGM_IDP

   IDP module forbids moving the segment.


.. py:data:: MOVE_SEGM_CHUNK

   Too many chunks are defined, can't move.


.. py:data:: MOVE_SEGM_LOADER

   The segment has been moved but the loader complained.


.. py:data:: MOVE_SEGM_ODD

   Cannot move segments by an odd number of bytes.


.. py:data:: MOVE_SEGM_ORPHAN

   Orphan bytes hinder segment movement.


.. py:data:: MOVE_SEGM_DEBUG

   Debugger segments cannot be moved.


.. py:data:: MOVE_SEGM_SOURCEFILES

   Source files ranges of addresses hinder segment movement.


.. py:data:: MOVE_SEGM_MAPPING

   Memory mapping ranges of addresses hinder segment movement.


.. py:data:: MOVE_SEGM_INVAL

   Invalid argument (delta/target does not fit the address space)


.. py:function:: move_segm_strerror(code: move_segm_code_t) -> str

   Return string describing error MOVE_SEGM_... code.


.. py:function:: move_segm(s: segment_t, to: ida_idaapi.ea_t, flags: int = 0) -> move_segm_code_t

   This function moves all information to the new address. It fixes up address sensitive information in the kernel. The total effect is equal to reloading the segment to the target address. For the file format dependent address sensitive information, loader_t::move_segm is called. Also IDB notification event idb_event::segm_moved is called. 
           
   :param s: segment to move
   :param to: new segment start address
   :param flags: Move segment flags
   :returns: Move segment result codes


.. py:data:: MSF_SILENT

   don't display a "please wait" box on the screen


.. py:data:: MSF_NOFIX

   don't call the loader to fix relocations


.. py:data:: MSF_LDKEEP

   keep the loader in the memory (optimization)


.. py:data:: MSF_FIXONCE

   call loader only once with the special calling method. valid for rebase_program(). see loader_t::move_segm. 
           


.. py:data:: MSF_PRIORITY

   loader segments will overwrite any existing debugger segments when moved. valid for move_segm() 
           


.. py:data:: MSF_NETNODES

   move netnodes instead of changing inf.netdelta (this is slower); valid for rebase_program() 
           


.. py:function:: change_segment_status(s: segment_t, is_deb_segm: bool) -> int

   Convert a debugger segment to a regular segment and vice versa. When converting debug->regular, the memory contents will be copied to the database. 
           
   :param s: segment to modify
   :param is_deb_segm: new status of the segment
   :returns: Change segment status result codes


.. py:data:: CSS_OK

   ok


.. py:data:: CSS_NODBG

   debugger is not running


.. py:data:: CSS_NORANGE

   could not find corresponding memory range


.. py:data:: CSS_NOMEM

   not enough memory (might be because the segment is too big) 
           


.. py:data:: CSS_BREAK

   memory reading process stopped by user


.. py:data:: SNAP_ALL_SEG

   Take a snapshot of all segments.


.. py:data:: SNAP_LOAD_SEG

   Take a snapshot of loader segments.


.. py:data:: SNAP_CUR_SEG

   Take a snapshot of current segment.


.. py:function:: take_memory_snapshot(type: int) -> bool

   Take a memory snapshot of the running process. 
           
   :param type: specifies which snapshot we want (see SNAP_ Snapshot types)
   :returns: success


.. py:function:: is_miniidb() -> bool

   Is the database a miniidb created by the debugger?. 
           
   :returns: true if the database contains no segments or only debugger segments


.. py:function:: set_segm_base(s: segment_t, newbase: ida_idaapi.ea_t) -> bool

   Internal function.


.. py:function:: set_group_selector(grp: sel_t, sel: sel_t) -> int

   Create a new group of segments (used OMF files). 
           
   :param grp: selector of group segment (segment type is SEG_GRP) You should create an 'empty' (1 byte) group segment It won't contain anything and will be used to redirect references to the group of segments to the common selector.
   :param sel: common selector of all segments belonging to the segment You should create all segments within the group with the same selector value.
   :returns: 1: ok
   :returns: 0: too many groups (see MAX_GROUPS)


.. py:data:: MAX_GROUPS

   max number of segment groups


.. py:function:: get_group_selector(grpsel: sel_t) -> sel_t

   Get common selector for a group of segments. 
           
   :param grpsel: selector of group segment
   :returns: common selector of the group or 'grpsel' if no such group is found


.. py:function:: add_segment_translation(segstart: ida_idaapi.ea_t, mappedseg: ida_idaapi.ea_t) -> bool

   Add segment translation. 
           
   :param segstart: start address of the segment to add translation to
   :param mappedseg: start address of the overlayed segment
   :returns: 1: ok
   :returns: 0: too many translations or bad segstart


.. py:data:: MAX_SEGM_TRANSLATIONS

   max number of segment translations


.. py:function:: del_segment_translations(segstart: ida_idaapi.ea_t) -> None

   Delete the translation list 
           
   :param segstart: start address of the segment to delete translation list


.. py:function:: get_segment_translations(transmap: eavec_t *, segstart: ida_idaapi.ea_t) -> ssize_t

   Get segment translation list. 
           
   :param transmap: vector of segment start addresses for the translation list
   :param segstart: start address of the segment to get information about
   :returns: -1 if no translation list or bad segstart. otherwise returns size of translation list.


.. py:function:: get_segment_cmt(s: segment_t, repeatable: bool) -> str

   Get segment comment. 
           
   :param s: pointer to segment structure
   :param repeatable: 0: get regular comment. 1: get repeatable comment.
   :returns: size of comment or -1


.. py:function:: set_segment_cmt(s: segment_t, cmt: str, repeatable: bool) -> None

   Set segment comment. 
           
   :param s: pointer to segment structure
   :param cmt: comment string, may be multiline (with '
   '). maximal size is 4096 bytes. Use empty str ("") to delete comment
   :param repeatable: 0: set regular comment. 1: set repeatable comment.


.. py:function:: std_out_segm_footer(ctx: outctx_t &, seg: segment_t) -> None

   Generate segment footer line as a comment line. This function may be used in IDP modules to generate segment footer if the target assembler doesn't have 'ends' directive. 
           


.. py:function:: set_segm_name(s: segment_t, name: str, flags: int = 0) -> int

   Rename segment. The new name is validated (see validate_name). A segment always has a name. If you hadn't specified a name, the kernel will assign it "seg###" name where ### is segment number. 
           
   :param s: pointer to segment (may be nullptr)
   :param name: new segment name
   :param flags: ADDSEG_IDBENC or 0
   :returns: 1: ok, name is good and segment is renamed
   :returns: 0: failure, name is bad or segment is nullptr


.. py:function:: get_segm_name(s: segment_t, flags: int = 0) -> str

   Get true segment name by pointer to segment. 
           
   :param s: pointer to segment
   :param flags: 0-return name as is; 1-substitute bad symbols with _ 1 corresponds to GN_VISIBLE
   :returns: size of segment name (-1 if s==nullptr)


.. py:function:: get_visible_segm_name(s: segment_t) -> str

   Get segment name by pointer to segment. 
           
   :param s: pointer to segment
   :returns: size of segment name (-1 if s==nullptr)


.. py:function:: get_segm_class(s: segment_t) -> str

   Get segment class. Segment class is arbitrary text (max 8 characters). 
           
   :param s: pointer to segment
   :returns: size of segment class (-1 if s==nullptr or bufsize<=0)


.. py:function:: set_segm_class(s: segment_t, sclass: str, flags: int = 0) -> int

   Set segment class. 
           
   :param s: pointer to segment (may be nullptr)
   :param sclass: segment class (may be nullptr). If segment type is SEG_NORM and segment class is one of predefined names, then segment type is changed to:
   * "CODE" -> SEG_CODE
   * "DATA" -> SEG_DATA
   * "STACK" -> SEG_BSS
   * "BSS" -> SEG_BSS
   * if "UNK" then segment type is reset to SEG_NORM.
   :param flags: Add segment flags
   :returns: 1: ok, name is good and segment is renamed
   :returns: 0: failure, name is nullptr or bad or segment is nullptr


.. py:function:: segtype(ea: ida_idaapi.ea_t) -> uchar

   Get segment type. 
           
   :param ea: any linear address within the segment
   :returns: Segment types, SEG_UNDF if no segment found at 'ea'


.. py:function:: get_segment_alignment(align: uchar) -> str

   Get text representation of segment alignment code. 
           
   :returns: text digestable by IBM PC assembler.


.. py:function:: get_segment_combination(comb: uchar) -> str

   Get text representation of segment combination code. 
           
   :returns: text digestable by IBM PC assembler.


.. py:function:: get_segm_para(s: segment_t) -> ida_idaapi.ea_t

   Get segment base paragraph. Segment base paragraph may be converted to segment base linear address using to_ea() function. In fact, to_ea(get_segm_para(s), 0) == get_segm_base(s). 
           
   :param s: pointer to segment
   :returns: 0 if s == nullptr, the segment base paragraph


.. py:function:: get_segm_base(s: segment_t) -> ida_idaapi.ea_t

   Get segment base linear address. Segment base linear address is used to calculate virtual addresses. The virtual address of the first byte of the segment will be (start address of segment - segment base linear address) 
           
   :param s: pointer to segment
   :returns: 0 if s == nullptr, otherwise segment base linear address


.. py:function:: set_segm_addressing(s: segment_t, bitness: size_t) -> bool

   Change segment addressing mode (16, 32, 64 bits). You must use this function to change segment addressing, never change the 'bitness' field directly. This function will delete all instructions, comments and names in the segment 
           
   :param s: pointer to segment
   :param bitness: new addressing mode of segment
   * 2: 64bit segment
   * 1: 32bit segment
   * 0: 16bit segment
   :returns: success


.. py:function:: update_segm(s: segment_t) -> bool

.. py:function:: segm_adjust_diff(s: segment_t, delta: adiff_t) -> adiff_t

   Truncate and sign extend a delta depending on the segment.


.. py:function:: segm_adjust_ea(s: segment_t, ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Truncate an address depending on the segment.


.. py:function:: get_defsr(s, reg)

   Deprecated, use instead:
   value = s.defsr[reg]


.. py:function:: set_defsr(s, reg, value)

   Deprecated, use instead:
   s.defsr[reg] = value


.. py:function:: rebase_program(delta: PyObject *, flags: int) -> int

   Rebase the whole program by 'delta' bytes. 
           
   :param delta: number of bytes to move the program
   :param flags: Move segment flags it is recommended to use MSF_FIXONCE so that the loader takes care of global variables it stored in the database
   :returns: Move segment result codes



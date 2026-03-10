ida_merge
=========

.. py:module:: ida_merge

.. autoapi-nested-parse::

   Merge functionality.

   NOTE: this functionality is available in IDA Teams (not IDA Pro)
   There are 3 databases involved in merging: base_idb, local_db, and remote_idb.
   * base_idb: the common base ancestor of 'local_db' and 'remote_db'. in the UI this database is located in the middle.
   * local_idb: local database that will contain the result of the merging. in the UI this database is located on the left.
   * remote_idb: remote database that will merge into local_idb. It may reside locally on the current computer, despite its name. in the UI this database is located on the right. base_idb and remote_idb are opened for reading only. base_idb may be absent, in this case a 2-way merging is performed.


   Conflicts can be resolved automatically or interactively. The automatic resolving scores the conflicting blocks and takes the better one. The interactive resolving displays the full rendered contents side by side, and expects the user to select the better side for each conflict.
   Since IDB files contain various kinds of information, there are many merging phases. The entire list can be found in merge.cpp. Below are just some selected examples:
   * merge global database settings (inf and other global vars)
   * merge segmentation and changes to the database bytes
   * merge various lists: exports, imports, loaded tils, etc
   * merge names, functions, function frames
   * merge debugger settings, breakpoints
   * merge struct/enum views
   * merge local type libraries
   * merge the disassembly items (i.e. the segment contents) this includes operand types, code/data separation, etc
   * merge plugin specific info like decompiler types, dwarf mappings, etc


   To unify UI elements of each merge phase, we use merger views:
   * A view that consists of 2 or 3 panes: left (local_idb) and right (remote_idb). The common base is in the middle, if present.
   * Rendering of the panes depends on the phase, different phases show different contents.
   * The conflicts are highlighted by a colored background. Also, the detail pane can be consulted for additional info.
   * The user can select a conflict (or a bunch of conflicts) and say "use this block".
   * The user can browse the panes as he wishes. He will not be forced to handle conflicts in any particular order. However, once he finishes working with a merge handler and proceeds to the next one, he cannot go back.
   * Scrolling the left pane will synchronously scroll the right pane and vice versa.
   * There are the navigation commands like "go to the prev/next conflict"
   * The number of remaining conflicts to resolve is printed in the "Progress" chooser.
   * The user may manually modify local database inside the merger view. For that he may use the regular hotkeys. However, editing the database may lead to new conflicts, so we better restrict the available actions to some reasonable minimum. Currently, this is not implemented.


   IDA works in a new "merge" mode during merging. In this mode most events are not generated. We forbid them to reduce the risk that a rogue third-party plugin that is not aware of the "merge" mode would spoil something.
   For example, normally renaming a function causes a cascade of events and may lead to other database modifications. Some of them may be desired, some - not. Since there are some undesired events, it is better to stop generating them. However, some events are required to render the disassembly listing. For example, ev_ana_insn, av_out_insn. This is why some events are still generated in the "merge" mode.
   To let processor modules and plugins merge their data, we introduce a new event: ev_create_merge_handlers. It is generated immediately after opening all three idbs. The interested modules should react to this event by creating new merge handlers, if they need them.
   While the kernel can create arbitrary merge handlers, modules can create only the standard ones returned by:
   create_nodeval_merge_handler() create_nodeval_merge_handlers() create_std_modmerge_handlers()
   We do not document merge_handler_t because once a merge handler is created, it is used exclusively by the kernel.
   See mergemod.hpp for more information about the merge mode for modules. 
       



Attributes
----------

.. autoapisummary::

   ida_merge.MERGE_KIND_NETNODE
   ida_merge.MERGE_KIND_AUTOQ
   ida_merge.MERGE_KIND_INF
   ida_merge.MERGE_KIND_ENCODINGS
   ida_merge.MERGE_KIND_ENCODINGS2
   ida_merge.MERGE_KIND_SCRIPTS2
   ida_merge.MERGE_KIND_SCRIPTS
   ida_merge.MERGE_KIND_CUSTDATA
   ida_merge.MERGE_KIND_CUSTCNV
   ida_merge.MERGE_KIND_ENUMS
   ida_merge.MERGE_KIND_STRUCTS
   ida_merge.MERGE_KIND_TILS
   ida_merge.MERGE_KIND_TINFO
   ida_merge.MERGE_KIND_STRMEM
   ida_merge.MERGE_KIND_UDTMEM
   ida_merge.MERGE_KIND_GHSTRCMT
   ida_merge.MERGE_KIND_STRMEMCMT
   ida_merge.MERGE_KIND_SELECTORS
   ida_merge.MERGE_KIND_STT
   ida_merge.MERGE_KIND_SEGMENTS
   ida_merge.MERGE_KIND_SEGGRPS
   ida_merge.MERGE_KIND_SEGREGS
   ida_merge.MERGE_KIND_ORPHANS
   ida_merge.MERGE_KIND_BYTEVAL
   ida_merge.MERGE_KIND_FIXUPS
   ida_merge.MERGE_KIND_MAPPING
   ida_merge.MERGE_KIND_EXPORTS
   ida_merge.MERGE_KIND_IMPORTS
   ida_merge.MERGE_KIND_PATCHES
   ida_merge.MERGE_KIND_FLAGS
   ida_merge.MERGE_KIND_EXTRACMT
   ida_merge.MERGE_KIND_AFLAGS_EA
   ida_merge.MERGE_KIND_IGNOREMICRO
   ida_merge.MERGE_KIND_FILEREGIONS
   ida_merge.MERGE_KIND_HIDDENRANGES
   ida_merge.MERGE_KIND_SOURCEFILES
   ida_merge.MERGE_KIND_FUNC
   ida_merge.MERGE_KIND_FRAMEMGR
   ida_merge.MERGE_KIND_FRAME
   ida_merge.MERGE_KIND_STKPNTS
   ida_merge.MERGE_KIND_FLOWS
   ida_merge.MERGE_KIND_CREFS
   ida_merge.MERGE_KIND_DREFS
   ida_merge.MERGE_KIND_BPTS
   ida_merge.MERGE_KIND_WATCHPOINTS
   ida_merge.MERGE_KIND_BOOKMARKS
   ida_merge.MERGE_KIND_TRYBLKS
   ida_merge.MERGE_KIND_DIRTREE
   ida_merge.MERGE_KIND_VFTABLES
   ida_merge.MERGE_KIND_SIGNATURES
   ida_merge.MERGE_KIND_PROBLEMS
   ida_merge.MERGE_KIND_UI
   ida_merge.MERGE_KIND_DEKSTOPS
   ida_merge.MERGE_KIND_NOTEPAD
   ida_merge.MERGE_KIND_LOADER
   ida_merge.MERGE_KIND_DEBUGGER
   ida_merge.MERGE_KIND_DBG_MEMREGS
   ida_merge.MERGE_KIND_LUMINA
   ida_merge.MERGE_KIND_LAST
   ida_merge.MERGE_KIND_END
   ida_merge.MERGE_KIND_NONE
   ida_merge.MH_LISTEN
   ida_merge.MH_TERSE
   ida_merge.MH_UI_NODETAILS
   ida_merge.MH_UI_COMPLEX
   ida_merge.MH_UI_DP_NOLINEDIFF
   ida_merge.MH_UI_DP_SHORTNAME
   ida_merge.MH_UI_INDENT
   ida_merge.MH_UI_SPLITNAME
   ida_merge.MH_UI_CHAR_MASK
   ida_merge.MH_UI_COMMANAME
   ida_merge.MH_UI_COLONNAME
   ida_merge.NDS_IS_BOOL
   ida_merge.NDS_IS_EA
   ida_merge.NDS_IS_RELATIVE
   ida_merge.NDS_IS_STR
   ida_merge.NDS_SUPVAL
   ida_merge.NDS_BLOB
   ida_merge.NDS_EV_RANGE
   ida_merge.NDS_EV_FUNC
   ida_merge.NDS_MAP_IDX
   ida_merge.NDS_MAP_VAL
   ida_merge.NDS_VAL8
   ida_merge.NDS_INC
   ida_merge.NDS_UI_ND


Classes
-------

.. autoapisummary::

   ida_merge.merge_data_t
   ida_merge.item_block_locator_t
   ida_merge.merge_handler_params_t
   ida_merge.moddata_diff_helper_t
   ida_merge.merge_node_helper_t
   ida_merge.merge_node_info_t


Functions
---------

.. autoapisummary::

   ida_merge.is_diff_merge_mode
   ida_merge.create_nodeval_merge_handler
   ida_merge.create_nodeval_merge_handlers
   ida_merge.destroy_moddata_merge_handlers
   ida_merge.get_ea_diffpos_name


Module Contents
---------------

.. py:data:: MERGE_KIND_NETNODE

   netnode (no merging, to be used in idbunits)


.. py:data:: MERGE_KIND_AUTOQ

   auto queues


.. py:data:: MERGE_KIND_INF

   merge the inf variable (global settings)


.. py:data:: MERGE_KIND_ENCODINGS

   merge encodings


.. py:data:: MERGE_KIND_ENCODINGS2

   merge default encodings


.. py:data:: MERGE_KIND_SCRIPTS2

   merge scripts common info


.. py:data:: MERGE_KIND_SCRIPTS

   merge scripts


.. py:data:: MERGE_KIND_CUSTDATA

   merge custom data type and formats


.. py:data:: MERGE_KIND_CUSTCNV

   merge custom calling conventions


.. py:data:: MERGE_KIND_ENUMS

   merge enums


.. py:data:: MERGE_KIND_STRUCTS

   merge structs (globally: add/delete structs entirely)


.. py:data:: MERGE_KIND_TILS

   merge type libraries


.. py:data:: MERGE_KIND_TINFO

   merge tinfo


.. py:data:: MERGE_KIND_STRMEM

   merge struct members


.. py:data:: MERGE_KIND_UDTMEM

   merge UDT members (local types)


.. py:data:: MERGE_KIND_GHSTRCMT

   merge ghost structure comment


.. py:data:: MERGE_KIND_STRMEMCMT

   merge member comments for ghost struc


.. py:data:: MERGE_KIND_SELECTORS

   merge selectors


.. py:data:: MERGE_KIND_STT

   merge flag storage types


.. py:data:: MERGE_KIND_SEGMENTS

   merge segments


.. py:data:: MERGE_KIND_SEGGRPS

   merge segment groups


.. py:data:: MERGE_KIND_SEGREGS

   merge segment registers


.. py:data:: MERGE_KIND_ORPHANS

   merge orphan bytes


.. py:data:: MERGE_KIND_BYTEVAL

   merge byte values


.. py:data:: MERGE_KIND_FIXUPS

   merge fixups


.. py:data:: MERGE_KIND_MAPPING

   merge manual memory mapping


.. py:data:: MERGE_KIND_EXPORTS

   merge exports


.. py:data:: MERGE_KIND_IMPORTS

   merge imports


.. py:data:: MERGE_KIND_PATCHES

   merge patched bytes


.. py:data:: MERGE_KIND_FLAGS

   merge flags64_t


.. py:data:: MERGE_KIND_EXTRACMT

   merge extra next or prev lines


.. py:data:: MERGE_KIND_AFLAGS_EA

   merge aflags for mapped EA


.. py:data:: MERGE_KIND_IGNOREMICRO

   IM ("$ ignore micro") flags.


.. py:data:: MERGE_KIND_FILEREGIONS

   merge fileregions


.. py:data:: MERGE_KIND_HIDDENRANGES

   merge hidden ranges


.. py:data:: MERGE_KIND_SOURCEFILES

   merge source files ranges


.. py:data:: MERGE_KIND_FUNC

   merge func info


.. py:data:: MERGE_KIND_FRAMEMGR

   merge frames (globally: add/delete frames entirely)


.. py:data:: MERGE_KIND_FRAME

   merge function frame info (frame members)


.. py:data:: MERGE_KIND_STKPNTS

   merge SP change points


.. py:data:: MERGE_KIND_FLOWS

   merge flows


.. py:data:: MERGE_KIND_CREFS

   merge crefs


.. py:data:: MERGE_KIND_DREFS

   merge drefs


.. py:data:: MERGE_KIND_BPTS

   merge breakpoints


.. py:data:: MERGE_KIND_WATCHPOINTS

   merge watchpoints


.. py:data:: MERGE_KIND_BOOKMARKS

   merge bookmarks


.. py:data:: MERGE_KIND_TRYBLKS

   merge try blocks


.. py:data:: MERGE_KIND_DIRTREE

   merge std dirtrees


.. py:data:: MERGE_KIND_VFTABLES

   merge vftables


.. py:data:: MERGE_KIND_SIGNATURES

   signatures


.. py:data:: MERGE_KIND_PROBLEMS

   problems


.. py:data:: MERGE_KIND_UI

   UI.


.. py:data:: MERGE_KIND_DEKSTOPS

   dekstops


.. py:data:: MERGE_KIND_NOTEPAD

   notepad


.. py:data:: MERGE_KIND_LOADER

   loader data


.. py:data:: MERGE_KIND_DEBUGGER

   debugger data


.. py:data:: MERGE_KIND_DBG_MEMREGS

   manual memory regions (debugger)


.. py:data:: MERGE_KIND_LUMINA

   lumina function metadata


.. py:data:: MERGE_KIND_LAST

   last predefined merge handler type. please note that there can be more merge handler types, registered by plugins and processor modules. 
             


.. py:data:: MERGE_KIND_END

   insert to the end of handler list, valid for merge_handler_params_t::insert_after 
             


.. py:data:: MERGE_KIND_NONE

.. py:function:: is_diff_merge_mode() -> bool

   Return TRUE if IDA is running in diff mode (MERGE_POLICY_MDIFF/MERGE_POLICY_VDIFF)


.. py:class:: merge_data_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: dbctx_ids
      :type:  int [3]

      local, remote, base ids



   .. py:attribute:: nbases
      :type:  int

      number of database participating in merge process, maybe 2 or 3 
              



   .. py:attribute:: ev_handlers
      :type:  merge_handlers_t

      event handlers



   .. py:attribute:: item_block_locator
      :type:  merge_data_t::item_block_locator_t *


   .. py:attribute:: last_udt_related_merger
      :type:  merge_handler_t *


   .. py:method:: set_dbctx_ids(local: int, remote: int, base: int) -> None


   .. py:method:: local_id() -> int


   .. py:method:: remote_id() -> int


   .. py:method:: base_id() -> int


   .. py:method:: add_event_handler(handler: merge_handler_t *) -> None


   .. py:method:: remove_event_handler(handler: merge_handler_t *) -> None


   .. py:method:: get_block_head(idx: diff_source_idx_t, item_head: ida_idaapi.ea_t) -> ida_idaapi.ea_t


   .. py:method:: setup_blocks(dst_idx: diff_source_idx_t, src_idx: diff_source_idx_t, region: diff_range_t const &) -> bool


   .. py:method:: has_existing_node(nodename: str) -> bool

      check that node exists in any of databases



   .. py:method:: map_privrange_id(tid: tid_t *, ea: ida_idaapi.ea_t, _from: diff_source_idx_t, to: diff_source_idx_t, strict: bool = True) -> bool

      map IDs of structures, enumerations and their members 
              
      :param tid: item ID in TO database
      :param ea: item ID to find counterpart
      :param to: destination database index, diff_source_idx_t
      :param strict: raise interr if could not map
      :returns: success



   .. py:method:: map_tinfo(tif: tinfo_t, _from: diff_source_idx_t, to: diff_source_idx_t, strict: bool = True) -> bool

      migrate type, replaces type references into FROM database to references into TO database 
              
      :param tif: type to migrate, will be cleared in case of fail
      :param to: destination database index, diff_source_idx_t
      :param strict: raise interr if could not map
      :returns: success



   .. py:method:: compare_merging_tifs(tif1: tinfo_t, diffidx1: diff_source_idx_t, tif2: tinfo_t, diffidx2: diff_source_idx_t) -> int

      compare types from two databases 
              
      :param tif1: type
      :param diffidx1: database index, diff_source_idx_t
      :param tif2: type
      :param diffidx2: database index, diff_source_idx_t
      :returns: -1, 0, 1



.. py:class:: item_block_locator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: get_block_head(md: merge_data_t, idx: diff_source_idx_t, item_head: ida_idaapi.ea_t) -> ida_idaapi.ea_t


   .. py:method:: setup_blocks(md: merge_data_t, _from: diff_source_idx_t, to: diff_source_idx_t, region: diff_range_t const &) -> bool


.. py:class:: merge_handler_params_t(_md: merge_data_t, _label: str, _kind: merge_kind_t, _insert_after: merge_kind_t, _mh_flags: int)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: md
      :type:  merge_data_t &


   .. py:attribute:: label
      :type:  str


   .. py:attribute:: kind
      :type:  merge_kind_t

      merge handler kind merge_kind_t



   .. py:attribute:: insert_after
      :type:  merge_kind_t

      desired position inside 'handlers' merge_kind_t



   .. py:attribute:: mh_flags
      :type:  int


   .. py:method:: ui_has_details(*args) -> bool

      This function has the following signatures:

          0. ui_has_details() -> bool
          1. ui_has_details(_mh_flags: int) -> bool

      # 0: ui_has_details() -> bool


      # 1: ui_has_details(_mh_flags: int) -> bool

      Should IDA display the diffpos detail pane?



   .. py:method:: ui_complex_details(*args) -> bool

      This function has the following signatures:

          0. ui_complex_details() -> bool
          1. ui_complex_details(_mh_flags: int) -> bool

      # 0: ui_complex_details() -> bool


      # 1: ui_complex_details(_mh_flags: int) -> bool

      Do not display the diffpos details in the chooser. For example, the MERGE_KIND_SCRIPTS handler puts the script body as the diffpos detail. It would not be great to show them as part of the chooser. 
              



   .. py:method:: ui_complex_name(*args) -> bool

      This function has the following signatures:

          0. ui_complex_name() -> bool
          1. ui_complex_name(_mh_flags: int) -> bool

      # 0: ui_complex_name() -> bool


      # 1: ui_complex_name(_mh_flags: int) -> bool

      It customary to create long diffpos names having many components that are separated by any 7-bit ASCII character (besides of '\0'). In this case it is possible to instruct IDA to use this separator to create a multi-column chooser. For example the MERGE_KIND_ENUMS handler has the following diffpos name: enum_1,enum_2 If MH_UI_COMMANAME is specified, IDA will create 2 columns for these names. 
              



   .. py:method:: ui_split_char(*args) -> char

      This function has the following signatures:

          0. ui_split_char() -> char
          1. ui_split_char(_mh_flags: int) -> char

      # 0: ui_split_char() -> char


      # 1: ui_split_char(_mh_flags: int) -> char



   .. py:method:: ui_split_str(*args) -> str

      This function has the following signatures:

          0. ui_split_str() -> str
          1. ui_split_str(_mh_flags: int) -> str

      # 0: ui_split_str() -> str


      # 1: ui_split_str(_mh_flags: int) -> str



   .. py:method:: ui_dp_shortname(*args) -> bool

      This function has the following signatures:

          0. ui_dp_shortname() -> bool
          1. ui_dp_shortname(_mh_flags: int) -> bool

      # 0: ui_dp_shortname() -> bool


      # 1: ui_dp_shortname(_mh_flags: int) -> bool

      The detail pane shows the diffpos details for the current diffpos range as a tree-like view. In this pane the diffpos names are used as tree node names and the diffpos details as their children. Sometimes, for complex diffpos names, the first part of the name looks better than the entire name. For example, the MERGE_KIND_SEGMENTS handler has the following diffpos name: <range>,<segm1>,<segm2>,<segm3> if MH_UI_DP_SHORTNAME is specified, IDA will use <range> as a tree node name 
              



   .. py:method:: ui_linediff(*args) -> bool

      This function has the following signatures:

          0. ui_linediff() -> bool
          1. ui_linediff(_mh_flags: int) -> bool

      # 0: ui_linediff() -> bool


      # 1: ui_linediff(_mh_flags: int) -> bool

      In detail pane IDA shows difference between diffpos details. IDA marks added or deleted detail by color. In the modified detail the changes are marked. Use this UI hint if you do not want to show the differences inside detail. 
              



   .. py:method:: ui_indent(*args) -> bool

      This function has the following signatures:

          0. ui_indent() -> bool
          1. ui_indent(_mh_flags: int) -> bool

      # 0: ui_indent() -> bool


      # 1: ui_indent(_mh_flags: int) -> bool

      In the ordinary situation the spaces from the both sides of diffpos name are trimmed. Use this UI hint to preserve the leading spaces. 
              



.. py:data:: MH_LISTEN

   merge handler will receive merge events


.. py:data:: MH_TERSE

   do not display equal lines in the merge results table


.. py:data:: MH_UI_NODETAILS

   ida will not show the diffpos details


.. py:data:: MH_UI_COMPLEX

   diffpos details won't be displayed in the diffpos chooser


.. py:data:: MH_UI_DP_NOLINEDIFF

   Detail pane: do not show differences inside the line.


.. py:data:: MH_UI_DP_SHORTNAME

   Detail pane: use the first part of a complex diffpos name as the tree node name.


.. py:data:: MH_UI_INDENT

   preserve indent for diffpos name in diffpos chooser


.. py:data:: MH_UI_SPLITNAME

   ida will split the diffpos name by 7-bit ASCII char to create chooser columns 
           


.. py:data:: MH_UI_CHAR_MASK

   7-bit ASCII split character


.. py:data:: MH_UI_COMMANAME

   ida will split the diffpos name by ',' to create chooser columns


.. py:data:: MH_UI_COLONNAME

   ida will split the diffpos name by ':' to create chooser columns


.. py:class:: moddata_diff_helper_t(_module_name: str, _netnode_name: str, _fields: idbattr_info_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: module_name
      :type:  str

      will be used as a prefix for field desc



   .. py:attribute:: netnode_name
      :type:  str

      name of netnode with module data attributes



   .. py:attribute:: fields
      :type:  idbattr_info_t const *

      module data attribute descriptions



   .. py:attribute:: nfields
      :type:  size_t

      number of descriptions



   .. py:attribute:: additional_mh_flags
      :type:  int

      additional merge handler flags



   .. py:method:: merge_starting(arg0: diff_source_idx_t, arg1: void *) -> None


   .. py:method:: merge_ending(arg0: diff_source_idx_t, arg1: void *) -> None


   .. py:method:: get_struc_ptr(arg0: merge_data_t, arg1: diff_source_idx_t, arg2: idbattr_info_t) -> void *


   .. py:method:: print_diffpos_details(arg0: qstrvec_t *, arg1: idbattr_info_t) -> None


   .. py:method:: val2str(arg0: str, arg1: idbattr_info_t, arg2: uint64) -> bool


   .. py:method:: str2val(arg0: uint64 *, arg1: idbattr_info_t, arg2: str) -> bool


.. py:data:: NDS_IS_BOOL

   boolean value


.. py:data:: NDS_IS_EA

   EA value.


.. py:data:: NDS_IS_RELATIVE

   value is relative to index (stored as delta)


.. py:data:: NDS_IS_STR

   string value


.. py:data:: NDS_SUPVAL

   stored as netnode supvals (not scalar)


.. py:data:: NDS_BLOB

   stored as netnode blobs


.. py:data:: NDS_EV_RANGE

   enable default handling of mev_modified_ranges, mev_deleting_segm


.. py:data:: NDS_EV_FUNC

   enable default handling of mev_added_func/mev_deleting_func


.. py:data:: NDS_MAP_IDX

   apply ea2node() to index (==NETMAP_IDX)


.. py:data:: NDS_MAP_VAL

   apply ea2node() to value. Along with NDS_INC it gives effect of NETMAP_VAL, examples: altval_ea : NDS_MAP_IDX charval : NDS_VAL8 charval_ea: NDS_MAP_IDX|NDS_VAL8 eaget : NDS_MAP_IDX|NDS_MAP_VAL|NDS_INC 
             


.. py:data:: NDS_VAL8

   use 8-bit values (==NETMAP_V8)


.. py:data:: NDS_INC

   stored value is incremented (scalars only)


.. py:data:: NDS_UI_ND

   UI: no need to show diffpos detail pane, MH_UI_NODETAILS, make sense if merge_node_helper_t is used 
             


.. py:class:: merge_node_helper_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: print_entry_name(arg0: uchar, arg1: nodeidx_t, arg2: void *) -> str

      print the name of the specified entry (to be used in print_diffpos_name) 
              



   .. py:method:: print_entry_details(arg0: qstrvec_t *, arg1: uchar, arg2: nodeidx_t, arg3: void *) -> None

      print the details of the specified entry usually contains multiple lines, one for each attribute or detail. (to be used in print_diffpos_details) 
              



   .. py:method:: get_column_headers(arg0: qstrvec_t *, arg1: uchar, arg2: void *) -> None

      get column headers for chooser (to be used in linear_diff_source_t::get_column_headers) 
              



   .. py:method:: is_mergeable(arg0: uchar, arg1: nodeidx_t) -> bool

      filter: check if we should perform merging for given record



   .. py:method:: get_netnode() -> netnode

      return netnode to be used as source. If this function returns BADNODE netnode will be created using netnode name passed to create_nodeval_diff_source 
              



   .. py:method:: map_scalar(arg0: nodeidx_t *, arg1: void *, arg2: diff_source_idx_t, arg3: diff_source_idx_t) -> None

      map scalar/string/buffered value



   .. py:method:: map_string(arg0: str, arg1: void *, arg2: diff_source_idx_t, arg3: diff_source_idx_t) -> None


   .. py:method:: refresh(arg0: uchar, arg1: void *) -> None

      notify helper that some data was changed in the database and internal structures (e.g. caches) should be refreshed 
              



   .. py:method:: append_eavec(s: str, prefix: str, eas: eavec_t const &) -> None
      :staticmethod:


      can be used by derived classes



.. py:class:: merge_node_info_t(name: str, tag: uchar, nds_flags: int, node_helper: merge_node_helper_t = None)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str

      name of the array (label)



   .. py:attribute:: tag
      :type:  uchar

      a tag used to access values in the netnode



   .. py:attribute:: nds_flags
      :type:  int

      node value attributes (a combination of nds_flags_t)



   .. py:attribute:: node_helper
      :type:  merge_node_helper_t *


.. py:function:: create_nodeval_merge_handler(mhp: merge_handler_params_t, label: str, nodename: str, tag: uchar, nds_flags: int, node_helper: merge_node_helper_t = None, skip_empty_nodes: bool = True) -> merge_handler_t *

   Create a merge handler for netnode scalar/string values 
           
   :param mhp: merging parameters
   :param label: handler short name (to be be appended to mhp.label)
   :param nodename: netnode name
   :param tag: a tag used to access values in the netnode
   :param nds_flags: netnode value attributes (a combination of nds_flags_t)
   :param skip_empty_nodes: do not create handler in case of empty netnode
   :returns: diff source object (normally should be attahced to a merge handler)


.. py:function:: create_nodeval_merge_handlers(out: merge_handlers_t *, mhp: merge_handler_params_t, nodename: str, valdesc: merge_node_info_t, skip_empty_nodes: bool = True) -> None

   Create a serie of merge handlers for netnode scalar/string values (call create_nodeval_merge_handler() for each member of VALDESC) 
           
   :param out: [out] created handlers will be placed here
   :param mhp: merging parameters
   :param nodename: netnode name
   :param valdesc: array of handler descriptions
   :param skip_empty_nodes: do not create handlers for empty netnodes
   :returns: diff source object (normally should be attahced to a merge handler)


.. py:function:: destroy_moddata_merge_handlers(data_id: int) -> None

.. py:function:: get_ea_diffpos_name(ea: ida_idaapi.ea_t) -> str

   Get nice name for EA diffpos 
           
   :param ea: diffpos



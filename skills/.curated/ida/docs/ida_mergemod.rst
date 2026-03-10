ida_mergemod
============

.. py:module:: ida_mergemod

.. autoapi-nested-parse::

   Merge functionality for modules.

   NOTE: this functionality is available in IDA Teams (not IDA Pro)
   This file contains helper classes and convenience functions for module (plugin or processor module) merging.
   Each module is responsible for merging the data it owns (the module data). At the very beginning, the merging engine generates the ev_create_merge_handlers event. Modules should hook to this event to create merge handlers (mergers) that are responsible for the module data.
   We assume that each module may have:

   * its data structure, derived from plugmod_t or procmod_t. we call this structure moddata.
   * a dedicated netnode (module node), modnode for short.


   Moddata is registered with the IDA kernel using the set_module_data() function, which returns an integer, moddata_id. moddata_id is used to access the module data structure during merging, so it is mandatory for all modules that support merging.
   The following sources of mergeable data are supported:
   1. Data fields inside moddata 2. Values (scalar or binary, including blobs) stored in the module node 3. Values (scalar or binary, including blobs) stored in arbitrary netnodes 4. Data fields inside an auxiliary structure (provided by a special helper) 5. Indexed arrays of data stored in netnodes
   Usually the sources #1-4 are handled by a single merger, which can be parameterized using the folowing information:

   * moddata_id
   * module name
   * module node name
   * array of field descriptors (idbattr_info_t idpopts_info[], see ida.hpp)


   See plugins/mex1 for an example of such a merger.
   These parameters are stored in a helper class (moddata_diff_helper_t or derived). The helper class can override the following virtual methods:
   merge_starting - prepare module data for merging (e.g. load data from idb) merge_ending - opposite to merge_starting (e.g. save merged data to idb) get_struc_ptr - get pointer to the auxiliary structure (to handle source #4); this method will be called only if the fields with the IDI_HLPSTRUC bit are present in the idpopts_info[] array
   For most plugins, the default implementation of moddata_diff_helper_t or the std_moddata_diff_helper_t helper (presented below) is sufficient. You can find examples of non-standard helpers in plugins/mex2.
   The source #5 is handled by a different set of mergers described by an array of merge_node_info_t entries: a merger per entry. A non-trivial example can be found in plugins/mex3 and plugins/ex_merge_ldrdata.
   A module can use the create_std_modmerge_handlers() function to create necessary merge handlers. Please pay attention to the following arguments:
   helper - a helper class responsible for access to the internal module data for the sources #1-4. It can be used to prepare a pointer to the internal module structure and load/save data before/after merging (example: plugins/mex2). Im most cases the default helper class moddata_diff_helper_t can be used. merge_node_info - array of descriptions for the source #5. Note that the same module node is used for all array elements. If you need this kind of mergers for other netnodes, you should add them manually using the create_nodeval_merge_handler() function (example: plugins/mex3)
   See also module/mergecmn.cpp for procmod-specific functions and macros.
   Glossary:
   modmerger = module merger moddata = module data moddata_id = module data id 
       



Functions
---------

.. autoapisummary::

   ida_mergemod.create_std_modmerge_handlers


Module Contents
---------------

.. py:function:: create_std_modmerge_handlers(mhp: merge_handler_params_t &, helper: moddata_diff_helper_t &, merge_node_info: merge_node_info2_t const * = None) -> None

   convinience function to create merge handlers for modules/plugins



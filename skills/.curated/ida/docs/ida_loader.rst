ida_loader
==========

.. py:module:: ida_loader

.. autoapi-nested-parse::

   Definitions of IDP, LDR, PLUGIN module interfaces.

   This file also contains:

   * functions to load files into the database
   * functions to generate output files
   * high level functions to work with the database (open, save, close)


   The LDR interface consists of one structure: loader_t

   The IDP interface consists of one structure: processor_t

   The PLUGIN interface consists of one structure: plugin_t

   Modules can't use standard FILE* functions. They must use functions from <fpro.h>

   Modules can't use standard memory allocation functions. They must use functions 
   from <pro.h>

   The exported entry #1 in the module should point to the the appropriate 
   structure. (loader_t for LDR module, for example)

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For database operations, see :mod:`ida_domain.database`.



Attributes
----------

.. autoapisummary::

   ida_loader.LDRF_RELOAD
   ida_loader.LDRF_REQ_PROC
   ida_loader.ACCEPT_ARCHIVE
   ida_loader.ACCEPT_CONTINUE
   ida_loader.ACCEPT_FIRST
   ida_loader.NEF_SEGS
   ida_loader.NEF_RSCS
   ida_loader.NEF_NAME
   ida_loader.NEF_MAN
   ida_loader.NEF_FILL
   ida_loader.NEF_IMPS
   ida_loader.NEF_FIRST
   ida_loader.NEF_CODE
   ida_loader.NEF_RELOAD
   ida_loader.NEF_FLAT
   ida_loader.NEF_MINI
   ida_loader.NEF_LOPT
   ida_loader.NEF_LALL
   ida_loader.DLLEXT
   ida_loader.LOADER_DLL
   ida_loader.OFILE_MAP
   ida_loader.OFILE_EXE
   ida_loader.OFILE_IDC
   ida_loader.OFILE_LST
   ida_loader.OFILE_ASM
   ida_loader.OFILE_DIF
   ida_loader.GENFLG_MAPSEG
   ida_loader.GENFLG_MAPNAME
   ida_loader.GENFLG_MAPDMNG
   ida_loader.GENFLG_MAPLOC
   ida_loader.GENFLG_IDCTYPE
   ida_loader.GENFLG_ASMTYPE
   ida_loader.GENFLG_GENHTML
   ida_loader.GENFLG_ASMINC
   ida_loader.FILEREG_PATCHABLE
   ida_loader.FILEREG_NOTPATCHABLE
   ida_loader.PLUGIN_DLL
   ida_loader.MODULE_ENTRY_LOADER
   ida_loader.MODULE_ENTRY_PLUGIN
   ida_loader.MODULE_ENTRY_IDP
   ida_loader.IDP_DLL
   ida_loader.MAX_DATABASE_DESCRIPTION
   ida_loader.SSF_AUTOMATIC
   ida_loader.SSUF_DESC
   ida_loader.SSUF_PATH
   ida_loader.SSUF_FLAGS
   ida_loader.DBFL_KILL
   ida_loader.DBFL_COMP
   ida_loader.DBFL_BAK
   ida_loader.DBFL_TEMP
   ida_loader.PATH_TYPE_CMD
   ida_loader.PATH_TYPE_IDB
   ida_loader.PATH_TYPE_ID0


Classes
-------

.. autoapisummary::

   ida_loader.qvector_snapshotvec_t
   ida_loader.loader_t
   ida_loader.idp_name_t
   ida_loader.idp_desc_t
   ida_loader.plugin_info_t
   ida_loader.snapshot_t


Functions
---------

.. autoapisummary::

   ida_loader.load_binary_file
   ida_loader.process_archive
   ida_loader.gen_file
   ida_loader.file2base
   ida_loader.base2file
   ida_loader.get_basic_file_type
   ida_loader.get_file_type_name
   ida_loader.set_import_ordinal
   ida_loader.set_import_name
   ida_loader.load_ids_module
   ida_loader.get_plugin_options
   ida_loader.find_plugin
   ida_loader.get_fileregion_offset
   ida_loader.get_fileregion_ea
   ida_loader.gen_exe_file
   ida_loader.reload_file
   ida_loader.build_snapshot_tree
   ida_loader.flush_buffers
   ida_loader.is_trusted_idb
   ida_loader.save_database
   ida_loader.is_database_flag
   ida_loader.set_database_flag
   ida_loader.clr_database_flag
   ida_loader.get_path
   ida_loader.set_path
   ida_loader.get_elf_debug_file_directory
   ida_loader.mem2base
   ida_loader.load_plugin
   ida_loader.run_plugin
   ida_loader.load_and_run_plugin
   ida_loader.extract_module_from_archive


Module Contents
---------------

.. py:class:: qvector_snapshotvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> snapshot_t *&


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> snapshot_t *const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: qvector_snapshotvec_t) -> None


   .. py:method:: extract() -> snapshot_t **


   .. py:method:: inject(s: snapshot_t **, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< snapshot_t * >::const_iterator


   .. py:method:: end(*args) -> qvector< snapshot_t * >::const_iterator


   .. py:method:: insert(it: qvector< snapshot_t * >::iterator, x: snapshot_t) -> qvector< snapshot_t * >::iterator


   .. py:method:: erase(*args) -> qvector< snapshot_t * >::iterator


   .. py:method:: find(*args) -> qvector< snapshot_t * >::const_iterator


   .. py:method:: has(x: snapshot_t) -> bool


   .. py:method:: add_unique(x: snapshot_t) -> bool


   .. py:method:: append(x: snapshot_t) -> None


   .. py:method:: extend(x: qvector_snapshotvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: loader_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: version
      :type:  int

      api version, should be IDP_INTERFACE_VERSION



   .. py:attribute:: flags
      :type:  int

      Loader flags 
              



.. py:data:: LDRF_RELOAD

   loader recognizes NEF_RELOAD flag


.. py:data:: LDRF_REQ_PROC

   Requires a processor to be set. if this bit is not set, load_file() must call set_processor_type(..., SETPROC_LOADER) 
           


.. py:data:: ACCEPT_ARCHIVE

   Specify that a file format is served by archive loader See loader_t::accept_file 
           


.. py:data:: ACCEPT_CONTINUE

   Specify that the function must be called another time See loader_t::accept_file 
           


.. py:data:: ACCEPT_FIRST

   Specify that a file format should be place first in "load file" dialog box. See loader_t::accept_file 
           


.. py:data:: NEF_SEGS

   Create segments.


.. py:data:: NEF_RSCS

   Load resources.


.. py:data:: NEF_NAME

   Rename entries.


.. py:data:: NEF_MAN

   Manual load.


.. py:data:: NEF_FILL

   Fill segment gaps.


.. py:data:: NEF_IMPS

   Create import segment.


.. py:data:: NEF_FIRST

   This is the first file loaded into the database. 
           


.. py:data:: NEF_CODE

   for load_binary_file(): load as a code segment 
           


.. py:data:: NEF_RELOAD

   reload the file at the same place:
   * don't create segments
   * don't create fixup info
   * don't import segments
   * etc.


   Load only the bytes into the base. A loader should have the LDRF_RELOAD bit set. 
           


.. py:data:: NEF_FLAT

   Autocreate FLAT group (PE)


.. py:data:: NEF_MINI

   Create mini database (do not copy segment bytes from the input file; use only the file header metadata) 
           


.. py:data:: NEF_LOPT

   Display additional loader options dialog.


.. py:data:: NEF_LALL

   Load all segments without questions.


.. py:data:: DLLEXT

.. py:data:: LOADER_DLL

.. py:function:: load_binary_file(filename: str, li: linput_t *, _neflags: ushort, fileoff: qoff64_t, basepara: ida_idaapi.ea_t, binoff: ida_idaapi.ea_t, nbytes: uint64) -> bool

   Load a binary file into the database. This function usually is called from ui. 
           
   :param filename: the name of input file as is (if the input file is from library, then this is the name from the library)
   :param li: loader input source
   :param _neflags: Load file flags. For the first file, the flag NEF_FIRST must be set.
   :param fileoff: Offset in the input file
   :param basepara: Load address in paragraphs
   :param binoff: Load offset (load_address=(basepara<<4)+binoff)
   :param nbytes: Number of bytes to load from the file.
   * 0: up to the end of the file
   :returns: true: ok
   :returns: false: failed (couldn't open the file)


.. py:function:: process_archive(temp_file: str, li: linput_t *, module_name: str, neflags: ushort *, defmember: str, loader: load_info_t const *) -> str

   Calls loader_t::process_archive() For parameters and return value description look at loader_t::process_archive(). Additional parameter 'loader' is a pointer to load_info_t structure. 
           


.. py:data:: OFILE_MAP

   MAP file.


.. py:data:: OFILE_EXE

   Executable file.


.. py:data:: OFILE_IDC

   IDC file.


.. py:data:: OFILE_LST

   Disassembly listing.


.. py:data:: OFILE_ASM

   Assembly.


.. py:data:: OFILE_DIF

   Difference.


.. py:function:: gen_file(otype: ofile_type_t, fp: FILE *, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, flags: int) -> int

   Generate an output file. OFILE_EXE: 
           
   :param otype: type of output file.
   :param fp: the output file handle
   :param ea1: start address. For some file types this argument is ignored
   :param ea2: end address. For some file types this argument is ignored as usual in ida, the end address of the range is not included
   :param flags: Generate file flags
   :returns: number of the generated lines. -1 if an error occurred
   :returns: 0: can't generate exe file
   :returns: 1: ok


.. py:data:: GENFLG_MAPSEG

   OFILE_MAP: generate map of segments


.. py:data:: GENFLG_MAPNAME

   OFILE_MAP: include dummy names


.. py:data:: GENFLG_MAPDMNG

   OFILE_MAP: demangle names


.. py:data:: GENFLG_MAPLOC

   OFILE_MAP: include local names


.. py:data:: GENFLG_IDCTYPE

   OFILE_IDC: gen only information about types


.. py:data:: GENFLG_ASMTYPE

   OFILE_ASM,OFILE_LST: gen information about types too


.. py:data:: GENFLG_GENHTML

   OFILE_ASM,OFILE_LST: generate html (ui_genfile_callback will be used)


.. py:data:: GENFLG_ASMINC

   OFILE_ASM,OFILE_LST: gen information only about types


.. py:function:: file2base(li: linput_t *, pos: qoff64_t, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, patchable: int) -> int

   Load portion of file into the database. This function will include (ea1..ea2) into the addressing space of the program (make it enabled). 
           
   :param li: pointer of input source
   :param pos: position in the file
   :param ea1: range of destination linear addresses
   :param ea2: range of destination linear addresses
   :param patchable: should the kernel remember correspondence of file offsets to linear addresses.
   :returns: 1: ok
   :returns: 0: read error, a warning is displayed


.. py:data:: FILEREG_PATCHABLE

   means that the input file may be patched (i.e. no compression, no iterated data, etc) 
           


.. py:data:: FILEREG_NOTPATCHABLE

   the data is kept in some encoded form in the file. 
           


.. py:function:: base2file(fp: FILE *, pos: qoff64_t, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> int

   Unload database to a binary file. This function works for wide byte processors too. 
           
   :param fp: pointer to file
   :param pos: position in the file
   :param ea1: range of source linear addresses
   :param ea2: range of source linear addresses
   :returns: 1-ok(always), write error leads to immediate exit


.. py:function:: get_basic_file_type(li: linput_t *) -> filetype_t

   Get the input file type. This function can recognize libraries and zip files. 
           


.. py:function:: get_file_type_name() -> str

   Get name of the current file type. The current file type is kept in idainfo::filetype. 
           
   :returns: size of answer, this function always succeeds


.. py:function:: set_import_ordinal(modnode: int, ea: ida_idaapi.ea_t, ord: int) -> None

   Set information about the ordinal import entry. This function performs 'modnode.altset(ord, ea2node(ea));' 
           
   :param modnode: node with information about imported entries
   :param ea: linear address of the entry
   :param ord: ordinal number of the entry


.. py:function:: set_import_name(modnode: int, ea: ida_idaapi.ea_t, name: str) -> None

   Set information about the named import entry. This function performs 'modnode.supset_ea(ea, name);' 
           
   :param modnode: node with information about imported entries
   :param ea: linear address of the entry
   :param name: name of the entry


.. py:function:: load_ids_module(fname: char *) -> int

   Load and apply IDS file. This function loads the specified IDS file and applies it to the database. If the program imports functions from a module with the same name as the name of the ids file being loaded, then only functions from this module will be affected. Otherwise (i.e. when the program does not import a module with this name) any function in the program may be affected. 
           
   :param fname: name of file to apply
   :returns: 1: ok
   :returns: 0: some error (a message is displayed). if the ids file does not exist, no message is displayed


.. py:function:: get_plugin_options(plugin: str) -> str

   Get plugin options from the command line. If the user has specified the options in the -Oplugin_name:options format, them this function will return the 'options' part of it The 'plugin' parameter should denote the plugin name Returns nullptr if there we no options specified 
           


.. py:data:: PLUGIN_DLL

   Pattern to find plugin files.


.. py:data:: MODULE_ENTRY_LOADER

.. py:data:: MODULE_ENTRY_PLUGIN

.. py:data:: MODULE_ENTRY_IDP

.. py:class:: idp_name_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: lname
      :type:  str

      long processor name



   .. py:attribute:: sname
      :type:  str

      short processor name



   .. py:attribute:: hidden
      :type:  bool

      is hidden



.. py:class:: idp_desc_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: path
      :type:  str

      module file name



   .. py:attribute:: mtime
      :type:  time_t

      time of last modification



   .. py:attribute:: family
      :type:  str

      processor's family



   .. py:attribute:: names
      :type:  idp_names_t

      processor names



   .. py:attribute:: is_script
      :type:  bool

      the processor module is a script



   .. py:attribute:: checked
      :type:  bool

      internal, for cache management



.. py:data:: IDP_DLL

.. py:class:: plugin_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: next
      :type:  plugin_info_t *

      next plugin information



   .. py:attribute:: path
      :type:  char *

      full path to the plugin



   .. py:attribute:: org_name
      :type:  char *

      original short name of the plugin



   .. py:attribute:: name
      :type:  char *

      short name of the plugin it will appear in the menu 
              



   .. py:attribute:: org_hotkey
      :type:  ushort

      original hotkey to run the plugin



   .. py:attribute:: hotkey
      :type:  ushort

      current hotkey to run the plugin



   .. py:attribute:: arg
      :type:  size_t

      argument used to call the plugin



   .. py:attribute:: entry
      :type:  plugin_t *

      pointer to the plugin if it is already loaded



   .. py:attribute:: dllmem
      :type:  idadll_t


   .. py:attribute:: flags
      :type:  int

      a copy of plugin_t::flags



   .. py:attribute:: comment
      :type:  char *

      a copy of plugin_t::comment



   .. py:attribute:: idaplg_name
      :type:  str

      "name" provided by ida-plugin.json or basename of path (without extension)



.. py:function:: find_plugin(name: str, load_if_needed: bool = False) -> plugin_t *

   Find a user-defined plugin and optionally load it. 
           
   :param name: short plugin name without path and extension, or absolute path to the file name
   :param load_if_needed: if the plugin is not present in the memory, try to load it
   :returns: pointer to plugin description block


.. py:function:: get_fileregion_offset(ea: ida_idaapi.ea_t) -> qoff64_t

   Get offset in the input file which corresponds to the given ea. If the specified ea can't be mapped into the input file offset, return -1. 
           


.. py:function:: get_fileregion_ea(offset: qoff64_t) -> ida_idaapi.ea_t

   Get linear address which corresponds to the specified input file offset. If can't be found, return BADADDR 
           


.. py:function:: gen_exe_file(fp: FILE *) -> int

   Generate an exe file (unload the database in binary form). 
           
   :returns: fp the output file handle. if fp == nullptr then return:
   * 1: can generate an executable file
   * 0: can't generate an executable file
   :returns: 1: ok
   :returns: 0: failed


.. py:function:: reload_file(file: str, is_remote: bool) -> bool

   Reload the input file. This function reloads the byte values from the input file. It doesn't modify the segmentation, names, comments, etc. 
           
   :param file: name of the input file. if file == nullptr then returns:
   * 1: can reload the input file
   * 0: can't reload the input file
   :param is_remote: is the file located on a remote computer with the debugger server?
   :returns: success


.. py:data:: MAX_DATABASE_DESCRIPTION

   Maximum database snapshot description length.


.. py:class:: snapshot_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: id
      :type:  qtime64_t

      snapshot ID. This value is computed using qgettimeofday()



   .. py:attribute:: flags
      :type:  uint16

      Snapshot flags 
              



   .. py:attribute:: desc
      :type:  char [128]

      snapshot description



   .. py:attribute:: filename
      :type:  char [QMAXPATH]

      snapshot file name



   .. py:attribute:: children
      :type:  snapshots_t

      snapshot children



   .. py:method:: clear() -> None


.. py:data:: SSF_AUTOMATIC

   automatic snapshot


.. py:function:: build_snapshot_tree(root: snapshot_t) -> bool

   Build the snapshot tree. 
           
   :param root: snapshot root that will contain the snapshot tree elements.
   :returns: success


.. py:data:: SSUF_DESC

   Update the description.


.. py:data:: SSUF_PATH

   Update the path.


.. py:data:: SSUF_FLAGS

   Update the flags.


.. py:function:: flush_buffers() -> int

   Flush buffers to the disk.


.. py:function:: is_trusted_idb() -> bool

   Is the database considered as trusted?


.. py:function:: save_database(outfile: str = None, flags: int = -1, root: snapshot_t = None, attr: snapshot_t = None) -> bool

   Save current database using a new file name. 
           
   :param outfile: output database file name; nullptr means the current path
   :param flags: Database flags; -1 means the current flags
   :param root: optional: snapshot tree root.
   :param attr: optional: snapshot attributes
   :returns: success


.. py:data:: DBFL_KILL

   delete unpacked database


.. py:data:: DBFL_COMP

   collect garbage


.. py:data:: DBFL_BAK

   create backup file (if !DBFL_KILL)


.. py:data:: DBFL_TEMP

   temporary database


.. py:function:: is_database_flag(dbfl: int) -> bool

   Get the current database flag 
           
   :param dbfl: flag Database flags
   :returns: the state of the flag (set or cleared)


.. py:function:: set_database_flag(dbfl: int, cnd: bool = True) -> None

   Set or clear database flag 
           
   :param dbfl: flag Database flags
   :param cnd: set if true or clear flag otherwise


.. py:function:: clr_database_flag(dbfl: int) -> None

.. py:data:: PATH_TYPE_CMD

   full path to the file specified in the command line


.. py:data:: PATH_TYPE_IDB

   full path of IDB file


.. py:data:: PATH_TYPE_ID0

   full path of ID0 file


.. py:function:: get_path(pt: path_type_t) -> str

   Get the file path 
           
   :param pt: file path type Types of the file pathes
   :returns: file path, never returns nullptr


.. py:function:: set_path(pt: path_type_t, path: str) -> None

   Set the file path 
           
   :param pt: file path type Types of the file pathes
   :param path: new file path, use nullptr or empty string to clear the file path


.. py:function:: get_elf_debug_file_directory() -> str

   Get the value of the ELF_DEBUG_FILE_DIRECTORY configuration directive. 
           


.. py:function:: mem2base(mem, ea, fpos)

   Load database from the memory.

   :param mem: the buffer
   :param ea: start linear addresses
   :param fpos: position in the input file the data is taken from.
                if == -1, then no file position correspond to the data.
   :returns: 1, or 0 in case of failure


.. py:function:: load_plugin(name)

   Loads a plugin

   :param name: short plugin name without path and extension,
                or absolute path to the file name
   :returns: An opaque object representing the loaded plugin, or None if plugin could not be loaded


.. py:function:: run_plugin(plg, arg)

   Runs a plugin

   :param plg: A plugin object (returned by load_plugin())
   :param arg: the code to pass to the plugin's "run()" function
   :returns: Boolean


.. py:function:: load_and_run_plugin(name: str, arg: size_t) -> bool

   Load & run a plugin.


.. py:function:: extract_module_from_archive(fname: str, is_remote: bool = False) -> PyObject *

   Extract a module for an archive file. Parse an archive file, show the list of modules to the user, allow him to select a module, extract the selected module to a file (if the extract module is an archive, repeat the process). This function can handle ZIP, AR, AIXAR, OMFLIB files. The temporary file will be automatically deleted by IDA at the end. 
           
   :param is_remote: is the input file remote?
   :returns: true: ok
   :returns: false: something bad happened (error message has been displayed to the user)



# ida_loader

Loader and file operations - loading binaries, database management, file I/O, and plugin loading.

## Key Functions

### Database Operations
- `save_database(outfile=None, flags=-1, root=None, attr=None)` - Save database with optional new filename
- `flush_buffers()` - Flush buffers to disk
- `is_trusted_idb()` - Check if database is trusted
- `get_path(pt)` / `set_path(pt, path)` - Get/set file paths (PATH_TYPE_CMD, PATH_TYPE_IDB, PATH_TYPE_ID0)

### File Loading
- `load_binary_file(filename, li, neflags, fileoff, basepara, binoff, nbytes)` - Load binary into database
- `file2base(li, pos, ea1, ea2, patchable)` - Load file portion into address range
- `mem2base(mem, ea, fpos)` - Load from memory buffer
- `reload_file(file, is_remote)` - Reload input file bytes without losing analysis
- `base2file(fp, pos, ea1, ea2)` - Unload database to binary file

### File Type Detection
- `get_basic_file_type(li)` - Recognize file type (libraries, zip, etc.)
- `get_file_type_name()` - Get current file type name (from idainfo.filetype)

### Output Generation
- `gen_file(otype, fp, ea1, ea2, flags)` - Generate output files (MAP, EXE, IDC, LST, ASM, DIF)
- `gen_exe_file(fp)` - Generate executable file from database

### File/Memory Mapping
- `get_fileregion_offset(ea)` - Get file offset for linear address (returns -1 if unmapped)
- `get_fileregion_ea(offset)` - Get linear address for file offset (returns BADADDR if not found)

### Plugin Management
- `load_plugin(name)` - Load plugin by name or path
- `run_plugin(plg, arg)` - Run loaded plugin with argument
- `load_and_run_plugin(name, arg)` - Load and run plugin in one call
- `find_plugin(name, load_if_needed=False)` - Find plugin, optionally loading it
- `get_plugin_options(plugin)` - Get -Oplugin:options from command line

### Import/IDS
- `set_import_ordinal(modnode, ea, ord)` - Set ordinal import entry info
- `set_import_name(modnode, ea, name)` - Set named import entry info
- `load_ids_module(fname)` - Load and apply IDS file

### Archives
- `process_archive(temp_file, li, module_name, neflags, defmember, loader)` - Process archive file
- `extract_module_from_archive(fname, is_remote=False)` - Extract module from archive interactively

### Snapshots
- `build_snapshot_tree(root)` - Build snapshot tree structure

## Key Classes

### snapshot_t
Database snapshot representation.
- `id` - Snapshot ID (qtime64_t timestamp)
- `flags` - Snapshot flags (SSF_AUTOMATIC, etc.)
- `desc` - Description string (max 128 chars)
- `filename` - Snapshot filename
- `children` - Child snapshots

### plugin_info_t
Plugin metadata.
- `path` - Full plugin path
- `name` - Short name (appears in menu)
- `hotkey` - Current hotkey
- `flags` - Plugin flags
- `comment` - Plugin comment

### loader_t
Loader module interface (low-priority: advanced loader development only).

### idp_desc_t / idp_name_t
Processor module metadata (low-priority: processor module development).

## Key Flags

### Load Flags (NEF_*)
- `NEF_FIRST` - First file loaded into database
- `NEF_SEGS` - Create segments
- `NEF_CODE` - Load as code segment
- `NEF_RELOAD` - Reload at same place (don't recreate segments/fixups)
- `NEF_FLAT` - Autocreate FLAT group (PE)

### Database Flags (DBFL_*)
- `DBFL_KILL` - Delete unpacked database
- `DBFL_COMP` - Collect garbage
- `DBFL_BAK` - Create backup file
- `DBFL_TEMP` - Temporary database

### Output File Types (OFILE_*)
- `OFILE_MAP` - MAP file
- `OFILE_EXE` - Executable
- `OFILE_IDC` - IDC script
- `OFILE_LST` - Disassembly listing
- `OFILE_ASM` - Assembly
- `OFILE_DIF` - Difference

## See Also
Full docs: skill/docs/ida_loader.rst

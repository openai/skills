# ida_diskio

File I/O and IDA directory/resource management.

## IDA Directories

### Path Queries
- `idadir(subdir)` - Get IDA install directory or subdirectory
- `get_user_idadir()` - Get user data directory ($IDAUSR or default)
- `get_ida_subdirs(subdir, flags)` - List all search paths for resource
- `getsysfile(filename, subdir)` - Search for file in IDA paths

### Subdirectory Constants
- `CFG_SUBDIR` - Configuration files
- `IDC_SUBDIR` - IDC scripts
- `IDS_SUBDIR` - IDS files (function signatures)
- `IDP_SUBDIR` - Processor modules
- `LDR_SUBDIR` - Loader modules
- `SIG_SUBDIR` - FLIRT signatures
- `TIL_SUBDIR` - Type libraries
- `PLG_SUBDIR` - Plugins
- `THM_SUBDIR` - Themes

### Search Flags
- `IDA_SUBDIR_IDP` - Append processor name
- `IDA_SUBDIR_IDADIR_FIRST` - Search $IDADIR before $IDAUSR
- `IDA_SUBDIR_ONLY_EXISTING` - Only return existing directories

## File Operations

### Standard I/O Wrappers (use instead of C stdio)
- `fopenRT(file)` / `fopenWT(file)` - Open text read/write
- `fopenRB(file)` / `fopenWB(file)` - Open binary read/write
- `fopenM(file)` - Open for modification
- `fopenA(file)` - Open for append

## Linput (IDA Binary Input)

### Creation
- `open_linput(file, remote)` - Open file as linput
- `create_memory_linput(start, size)` - Create from IDB memory range
- `create_bytearray_linput(s)` - Create from Python bytes
- `create_generic_linput(gl)` - Create from custom reader

### Operations
- `qlgetz(li, fpos)` - Read null-terminated string at position
- `get_linput_type(li)` - Get linput type (LINPUT_LOCAL/RFILE/PROCMEM/GENERIC)
- `close_linput(li)` - Close linput

### Linput Types
- `LINPUT_LOCAL` - Local file
- `LINPUT_RFILE` - Remote file
- `LINPUT_PROCMEM` - Process memory
- `LINPUT_GENERIC` - Custom reader

### generic_linput_t
Base class for custom binary readers.

- `filesize` - Total size
- `blocksize` - Read block size
- `read(off, buffer, nbytes)` - Read bytes at offset

## File Enumeration
- `enumerate_files(path, fname, callback)` - Enumerate files matching pattern

## Platform Folders
- `get_special_folder(csidl)` - Get OS-specific folders
  - `CSIDL_APPDATA` - Application data
  - `CSIDL_LOCAL_APPDATA` - Local app data
  - `CSIDL_PROGRAM_FILES` - Program files directory

## See Also
Full docs: skill/docs/ida_diskio.rst

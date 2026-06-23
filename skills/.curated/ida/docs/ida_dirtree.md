# ida_dirtree

Directory tree organization for IDA items (types, functions, names, etc).

## Overview
Provides virtual directory structure over collections accessed by inode (ID). Used for organizing local types, structures, enums, functions, names, bookmarks, etc.

## Standard Trees
- `DIRTREE_LOCAL_TYPES` - Local type library
- `DIRTREE_FUNCS` - Function list
- `DIRTREE_NAMES` - Named locations
- `DIRTREE_IMPORTS` - Imported functions
- `DIRTREE_BPTS` - Breakpoints
- `get_std_dirtree(id)` - Access standard tree

## Key Classes

### dirtree_t
Main directory tree interface.

- `chdir(path)` / `getcwd()` - Navigate directories
- `mkdir(path)` / `rmdir(path)` - Create/delete directories
- `link(path/inode)` / `unlink(path/inode)` - Add/remove items
- `rename(from, to)` - Rename entry
- `resolve_path(path)` - Convert path to direntry_t
- `get_abspath(cursor/relpath)` - Get absolute path
- `isdir(path/de)` / `isfile(path/de)` - Check entry type
- `findfirst(ff, pattern)` / `findnext(ff)` - Iterate entries
- `traverse(visitor)` - Depth-first traversal with callback

### direntry_t
Represents a directory entry (inode or directory).

- `idx` - inode_t or diridx_t
- `isdir` - True if directory, false if file
- `valid()` - Check if entry exists

### dirtree_cursor_t
Cursor for navigating tree.

- `parent` - Parent directory index
- `rank` - Index within parent
- `is_root_cursor()` / `set_root_cursor()` - Root operations

### dirspec_t
Specialization interface (defines how inodes map to items).

- `get_name(inode, name_flags)` - Get item name
- `get_inode(dirpath, name)` - Lookup inode by name
- `rename_inode(inode, newname)` - Rename item
- `unlink_inode(inode)` - Notification when unlinked

## Error Codes
- `DTE_OK` - Success
- `DTE_ALREADY_EXISTS` - Item exists
- `DTE_NOT_FOUND` - Item not found
- `DTE_NOT_DIRECTORY` - Not a directory
- `DTE_NOT_EMPTY` - Directory not empty
- `DTE_BAD_PATH` - Invalid path

## See Also
Full docs: skill/docs/ida_dirtree.rst

# ida_libfuncs

FLIRT signature library metadata and access.

## Key Functions

- `get_idasgn_header_by_short_name(out_header, name)` - get signature header by short name
- `get_idasgn_path_by_short_name(name)` - get full path to signature file

## idasgn_header_t

Signature file header structure
- `processor_id` - target processor
- `file_formats` - supported file formats
- `ostype` - OS type (OSTYPE_MSDOS, OSTYPE_WIN, OSTYPE_UNIX, etc.)
- `apptype` - application type (APPT_CONSOLE, APPT_GRAPHIC, APPT_LIBRARY, APPT_DRIVER, etc.)
- `libname_length` - library name length
- `number_of_modules` - module count
- `ctype_name` - compiler type name

## Constants

### OS Types
OSTYPE_MSDOS, OSTYPE_WIN, OSTYPE_OS2, OSTYPE_NETW, OSTYPE_UNIX, OSTYPE_OTHER

### Application Types
- APPT_CONSOLE, APPT_GRAPHIC, APPT_PROGRAM, APPT_LIBRARY, APPT_DRIVER
- APPT_1THREAD, APPT_MTHREAD
- APPT_16BIT, APPT_32BIT, APPT_64BIT

## See Also
Full docs: skill/docs/ida_libfuncs.rst

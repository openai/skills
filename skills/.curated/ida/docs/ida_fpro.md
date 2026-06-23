# ida_fpro

System-independent FILE* operations - cross-module file I/O (use these instead of C stdlib functions).

## qfile_t Class

IDA's FILE* wrapper for cross-module compatibility.

### Constructor Methods
- `open(filename, mode) -> bool` - Open file (fopen-style mode string)
- `from_fp(fp) -> qfile_t*` - Wrap existing FILE*
- `from_capsule(pycapsule) -> qfile_t*` - Wrap Python capsule
- `tmpfile() -> qfile_t*` - Create temporary file

### File Operations
- `close()` - Close file
- `opened() -> bool` - Check if open
- `flush()` - Flush buffers
- `size() -> int64` - Get file size
- `filename() -> str` - Get filename

### Reading
- `read(size) -> str` - Read bytes (None on error)
- `readbytes(size, big_endian) -> str` - Read with endianness conversion
- `gets(len) -> str` - Read line (None on EOF)
- `get_byte() -> int` - Read single byte (None on EOF)

### Writing
- `write(buf) -> int` - Write bytes (0 on error, else bytes written)
- `writebytes(size, big_endian) -> int` - Write with endianness conversion
- `puts(str) -> int` - Write string
- `put_byte(chr)` - Write single byte

### Positioning
- `seek(offset, whence=SEEK_SET) -> int` - Seek (returns new position, not 0 like fseek)
- `tell() -> int` - Get current position

## Functions

- `qfclose(fp)` - Close FILE*

## Move Flags (QMOVE_*)
- `QMOVE_CROSS_FS` - Allow cross-filesystem moves
- `QMOVE_OVERWRITE` - Overwrite existing files
- `QMOVE_OVR_RO` - Overwrite read-only files

## Important

**Never mix C stdlib FILE* functions with IDA kernel functions.** Each module has its own FILE* state when statically linked. Use qfile_t for all file I/O in plugins.

## See Also
Full docs: skill/docs/ida_fpro.rst

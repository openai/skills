# ida_pro

Medium-priority: Core types, constants, and utility functions. Foundation module for platform detection and common operations.

## Key Constants

- `IDA_SDK_VERSION` - SDK version (9.2)
- `MAXSTR` - maximum string size
- `BADDIFF` - invalid diff value
- `FMT_EA` / `FMT_64` / `FMT_Z` - format string macros
- `CP_UTF8` / `CP_UTF16` - codepage constants
- `ENC_UTF8` / `ENC_UTF16LE` / `ENC_WIN1252` - encoding constants

## Key Vector Types

- `intvec_t` / `uintvec_t` - int/uint vectors
- `int64vec_t` / `uint64vec_t` - 64-bit int vectors
- `boolvec_t` - boolean vector
- `strvec_t` - string vector
- `eavec_t` - ea_t vector
- Standard methods: `push_back()`, `pop_back()`, `size()`, `at()`, `clear()`, `reserve()`, `find()`, `has()`, `add_unique()`

## Key Functions

- `qexit(code)` - shutdown IDA and exit
- `extend_sign(v, nbytes, sign_extend)` - sign/zero extend value to 64 bits
- `log2ceil(d64)` / `log2floor(d64)` - log2 calculations
- `bitcountr_zero(x)` - count trailing zero bits
- `is_main_thread()` - check if running on main thread
- `get_physical_core_count()` / `get_logical_core_count()` - CPU core info

## Platform Macros

Preprocessor defines: `__NT__` (Windows), `__LINUX__`, `__MAC__`, `__EA64__` (64-bit addresses), `__X64__` / `__X86__`, `__ARM__`, `__PPC__`

## See Also
Full docs: skill/docs/ida_pro.rst

# ida_tryblks

Exception handling (try/catch/SEH) information for binary code analysis.

## Key Classes

### tryblk_t
Represents an exception try block with associated catch/finally handlers.
- `get_kind()` - Check if SEH or C++ try block
- `is_seh()` / `is_cpp()` - Identify exception handling type
- `seh()` - Get SEH handler info (filter + landing pad)
- `cpp()` - Get C++ catch handlers vector
- `level` - Nesting level (auto-calculated)

### catch_t / seh_t
Handler information for C++ catch blocks and SEH (Structured Exception Handling).
- `obj` - Exception object offset (C++)
- `type_id` - Caught exception type ID
- `filter` - SEH filter function range
- `seh_code` - SEH exception code address

## Key Functions

### get_tryblks(tbv, range)
Retrieve all try blocks in address range, sorted and with nesting calculated.

### add_tryblk(tb)
Add try block information. Returns error code (TBERR_OK = success).

### del_tryblks(range)
Delete all try block information in range.

### find_syseh(ea)
Find start address of system exception handler region containing address.

### is_ea_tryblks(ea, flags)
Check if address is part of try/catch/filter (use TBEA_TRY, TBEA_CATCH, TBEA_SEHTRY, etc flags).

## Error Codes

- `TBERR_OK` - Success
- `TBERR_START/END/ORDER` - Invalid address bounds
- `TBERR_INTERSECT` - Try block would intersect inner block
- `TBERR_NO_CATCHES` - No catch handlers defined

## See Also
Full docs: skill/docs/ida_tryblks.rst

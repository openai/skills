# ida_ieee

IEEE floating point conversion utilities.

## Key Classes/Functions

### fpvalue_t
IEEE floating point value representation (internal format)
- `from_str(p)` - parse from string
- `to_str(buf, bufsize, mode)` - convert to string
- `from_sval(x)` / `to_sval(round)` - convert to/from signed integer
- `from_int64(x)` / `to_int64(round)` - convert to/from 64-bit int
- `from_uint64(x)` / `to_uint64(round)` - convert to/from unsigned 64-bit
- `from_10bytes(fpval)` / `to_10bytes(fpval)` - 10-byte float conversions
- `from_12bytes(fpval)` / `to_12bytes(fpval)` - 12-byte float conversions
- `fadd(y)`, `fsub(y)`, `fmul(y)`, `fdiv(y)` - arithmetic operations
- `eabs()`, `negate()` - absolute value and negation
- `is_negative()` - check sign
- `get_kind()` - get value kind (FPV_NORM, FPV_NAN, FPV_PINF, FPV_NINF)

## Error Codes
- REAL_ERROR_OK, REAL_ERROR_FORMAT, REAL_ERROR_RANGE
- REAL_ERROR_BADDATA, REAL_ERROR_FPOVER, REAL_ERROR_BADSTR
- REAL_ERROR_ZERODIV, REAL_ERROR_INTOVER

## See Also
Full docs: skill/docs/ida_ieee.rst

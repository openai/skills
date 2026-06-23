# ida_expr

IDC language interpreter - compile/execute IDC scripts, evaluate expressions, manipulate IDC values and objects.

## Key Functions

### Expression Evaluation
- `eval_expr(rv, where, line) -> str` - Compile and evaluate expression at address context
- `eval_idc_expr(rv, where, line) -> str` - Same as eval_expr but forces IDC interpreter

### Script Execution
- `compile_idc_file(line) -> str` - Compile IDC file
- `compile_idc_text(line) -> str` - Compile IDC text
- `compile_idc_snippet(func, text, resolver=None, only_safe_funcs=False) -> str` - Compile text into named function
- `exec_idc_script(result, path, func, args, argsnum) -> str` - Compile and execute function from file
- `exec_system_script(file, complain_if_no_file=True) -> bool` - Compile and execute "main" from system file

### IDC Value Manipulation
- `idcv_long(v) -> error_t` - Convert to 32/64-bit number
- `idcv_int64(v) -> error_t` - Convert to 64-bit number
- `idcv_num(v) -> error_t` - Convert to long ("true"→1, "false"→0)
- `idcv_string(v) -> error_t` - Convert to string
- `idcv_float(v) -> error_t` - Convert to float
- `idcv_object(v, icls=None) -> error_t` - Create IDC object
- `move_idcv(dst, src) -> error_t` - Move value (efficient, no copy)
- `copy_idcv(dst, src) -> error_t` - Shallow copy (objects copied by reference)
- `deep_copy_idcv(dst, src) -> error_t` - Deep copy objects
- `free_idcv(v)` - Free VT_STR/VT_OBJ storage
- `swap_idcvs(v1, v2)` - Swap two variables

### Object/Attribute Access
- `get_idcv_attr(res, obj, attr, may_use_getattr=False) -> error_t` - Get object attribute
- `set_idcv_attr(obj, attr, value, may_use_setattr=False) -> error_t` - Set object attribute
- `del_idcv_attr(obj, attr) -> error_t` - Delete attribute
- `first_idcv_attr(obj) -> str`, `last_idcv_attr(obj) -> str` - Iterate attributes
- `get_idcv_slice(res, v, i1, i2, flags=0) -> error_t` - Get slice of string/object
- `set_idcv_slice(v, i1, i2, _in, flags=0) -> error_t` - Set slice

### Class/Variable Management
- `add_idc_class(name, super=None) -> idc_class_t*` - Create IDC class
- `find_idc_class(name) -> idc_class_t*` - Find existing class
- `add_idc_gvar(name) -> idc_value_t*` - Add global variable
- `find_idc_gvar(name) -> idc_value_t*` - Find global variable
- `find_idc_func(prefix, n=0) -> str` - Find IDC function by prefix

## idc_value_t Class

Core IDC value container with variant type support.

### Attributes
- `vtype: char` - Type (VT_LONG, VT_FLOAT, VT_STR, VT_OBJ, VT_FUNC, VT_PVOID, VT_INT64, VT_REF)
- `num: int` - Integer value (VT_LONG)
- `i64: int64` - 64-bit integer (VT_INT64)
- `e: fpvalue_t` - Float value (VT_FLOAT)
- `obj: idc_object_t*` - Object reference (VT_OBJ)

### Methods
- `clear()` - Free storage
- `qstr() -> str`, `c_str() -> str` - Get string value
- `set_string(...)`, `set_long(v)`, `set_int64(v)`, `set_float(f)` - Set typed values
- `is_zero() -> bool`, `is_integral() -> bool`, `is_convertible() -> bool` - Type checks

## Value Types (VT_*)
- `VT_LONG` - Integer
- `VT_INT64` - 64-bit integer
- `VT_FLOAT` - Floating point
- `VT_STR` - String
- `VT_OBJ` - Object
- `VT_FUNC` - Function
- `VT_PVOID` - void pointer
- `VT_REF` - Reference

## Compilation Flags (CPL_*)
- `CPL_DEL_MACROS` - Delete macros after compilation
- `CPL_USE_LABELS` - Allow program labels
- `CPL_ONLY_SAFE` - Only thread-safe functions

## Function Flags (EXTFUN_*)
- `EXTFUN_BASE` - Requires open database
- `EXTFUN_NORET` - Does not return
- `EXTFUN_SAFE` - Thread-safe, callable from any thread

## See Also
Full docs: skill/docs/ida_expr.rst

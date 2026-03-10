# ida_typeinf

Type information manipulation in IDA - the foundation for working with structures, enums, function prototypes, and all type data.

## Core Concepts

**tinfo_t** objects represent types. They can be:
- **Detached**: Created without a type library, temporary
- **Attached**: Stored in a til_t (type info library), persistent

**Key terms**:
- **udt**: User-defined type (struct/union, not enum)
- **udm**: UDT member (struct/union field)
- **edm**: Enum member (enumerator)
- **til_t**: Type info library (serialized type storage)

## Essential Classes

### tinfo_t
The fundamental type representation object.

#### Creation
- `tinfo_t()` - Empty type
- `tinfo_t(BT_INT)` - Simple type from base type
- `tinfo_t("const char **")` - Parse C declaration
- `get_named_type(til, "struct_name")` - Load from library
- `create_func(func_type_data_t)` - Build function prototype
- `create_ptr(target_type)` - Build pointer type

#### Inspection
- `get_size()` - Type size in bytes
- `is_ptr()` / `is_func()` / `is_struct()` / `is_array()` - Type checks
- `is_const()` / `is_volatile()` - Qualifier checks
- `get_pointed_object()` - Dereference pointer
- `get_realtype()` - Resolve typedefs
- `print_tinfo(prefix, indent, flags)` - Format as C code

#### Decomposition
- `get_func_details(ftd)` - Extract function prototype to func_type_data_t
- `get_udt_details(udt)` - Extract struct/union to udt_type_data_t
- `get_enum_details(etd)` - Extract enum to enum_type_data_t
- `get_array_details(arr)` - Extract array to array_type_data_t
- `get_ptr_details(ptr)` - Extract pointer to ptr_type_data_t

#### Modification
- `create_typedef(til, name)` - Create typedef alias
- `add_udm(name, type_str)` - Add field to attached struct
- `set_numbered_type(til, ordinal, flags, name)` - Store in library

### func_type_data_t
Function prototype representation (return type + arguments).
- `rettype` - tinfo_t of return value
- `[i]` / `size()` - Access funcarg_t arguments by index
- `push_back(funcarg)` - Add parameter
- `cc` - Calling convention (CM_CC_CDECL, CM_CC_STDCALL, etc)
- `flags` - Function attributes (FTI_NORET, FTI_PURE, FTI_VIRTUAL, etc)

### funcarg_t
Function parameter representation.
- `name` - Parameter name
- `type` - tinfo_t of parameter type
- `argloc` - Physical location (register/stack)

### udt_type_data_t
Struct/union field collection (vector of udm_t).
- `[i]` / `size()` - Access udm_t members by index
- `push_back(udm)` - Add field
- `find_member(name)` - Locate field by name
- `get_best_fit_member(offset)` - Find field at offset
- `total_size` - Struct size in bytes
- `is_union` - True if union, false if struct
- `taudt_bits` - Alignment flags

### udm_t
Single struct/union field.
- `name` - Field name
- `type` - tinfo_t of field type
- `offset` - Byte offset (0 for unions)
- `size` - Field size in bytes
- `cmt` / `rptcmt` - Comments

### enum_type_data_t
Enumeration representation (vector of edm_t).
- `[i]` / `size()` - Access edm_t members by index
- `push_back(edm)` - Add enumerator
- `bte` - Storage size flags
- `taenum_bits` - Display format (hex/dec/oct/bin)

### edm_t
Single enum member.
- `name` - Enumerator name
- `value` - Numeric value

### til_t
Type info library (persistent storage).
- `get_named_type(name)` - Load type by name
- `get_numbered_type(ordinal)` - Load type by ordinal number
- `import_type(src)` - Import type from another til
- `named_types()` / `numbered_types()` - Iterate all types
- `cc` - Compiler info (calling conventions, sizes)

## Key Functions

### Type Library Management

#### get_idati()
Get the local type library (IDB's "Local Types").

#### add_til(name, flags)
Add base type library (e.g., "mssdk64_win7" for Windows types).

#### load_til(name, tildir)
Load til file without adding to IDB.

### Type Application

#### apply_tinfo(ea, tinfo, flags)
Apply type to address (function/data). Flags: TINFO_DEFINITE (override), TINFO_GUESSED (suggestion).

#### apply_cdecl(til, ea, decl)
Parse C declaration and apply to address.

#### guess_tinfo(ea)
Auto-analyze and infer type at address.

### Type Creation

#### parse_decl(til, decl, flags)
Parse C declaration string into tinfo_t. Returns (tinfo, name) tuple.

#### create_typedef(til, name)
Create typedef for existing type.

### Type Queries

#### get_tinfo(ea)
Retrieve type applied to address.

#### print_type(ea, flags)
Format type as C declaration string.

#### get_named_type(til, name)
Load type from library by name.

### Type Comparison

#### compare_tinfo(t1, t2, flags)
Check type compatibility. Flags: TCMP_EQUAL (exact), TCMP_MANCAST (manual cast allowed), etc.

## Base Type Constants

### Integers
- `BT_INT8` / `BT_INT16` / `BT_INT32` / `BT_INT64` / `BT_INT128`
- Combined with: `BTMT_SIGNED`, `BTMT_UNSIGNED`, `BTMT_CHAR`
- Shortcuts: `BTF_INT8`, `BTF_UINT8`, `BTF_CHAR`, `BTF_UCHAR`, etc.

### Floating Point
- `BT_FLOAT` - 4/8/10 byte float (use with BTMT_FLOAT/DOUBLE/LNGDBL)
- Shortcuts: `BTF_FLOAT`, `BTF_DOUBLE`, `BTF_LDOUBLE`, `BTF_TBYTE`

### Complex Types
- `BT_PTR` - Pointer (use with BTMT_NEAR/FAR/CLOSURE)
- `BT_ARRAY` - Array
- `BT_FUNC` - Function
- `BT_COMPLEX` - Struct/union/enum/typedef (use with BTMT_STRUCT/UNION/ENUM/TYPEDEF)
- `BT_BITFIELD` - Bitfield (struct member only)

### Special
- `BT_VOID` - void type
- `BT_BOOL` - bool type
- `BT_UNK` - Unknown type

## Type Modifiers

- `BTM_CONST` - const qualifier
- `BTM_VOLATILE` - volatile qualifier

## Calling Conventions

- `CM_CC_INVALID` / `CM_CC_UNKNOWN`
- `CM_CC_CDECL` - C declaration (caller cleans stack)
- `CM_CC_STDCALL` - Standard call (callee cleans)
- `CM_CC_FASTCALL` - Fast call (register args)
- `CM_CC_THISCALL` - C++ member (ecx/rcx = this)
- `CM_CC_PASCAL` - Pascal (right-to-left)
- `CM_CC_SWIFT` - Swift ABI
- `CM_CC_GOLANG` - Go ABI

## Flags

### Type Application (apply_tinfo)
- `TINFO_GUESSED` - Suggested type (user can override)
- `TINFO_DEFINITE` - Force type (overwrite existing)
- `TINFO_DELAYFUNC` - Delay function analysis

### Parsing (parse_decl)
- `PT_SIL` - Silent (no error messages)
- `PT_TYP` - Parse type only (no name)
- `PT_VAR` - Parse variable (type + name)
- `PT_REPLACE` - Replace existing type

### Printing (print_tinfo)
- `PRTYPE_1LINE` - Single line output
- `PRTYPE_MULTI` - Multiple lines
- `PRTYPE_TYPE` - Type only (no name)
- `PRTYPE_DEF` - Include typedef keyword

## Common Patterns

### Create Function Prototype
```python
# int func(const char *str, int count)
ftd = ida_typeinf.func_type_data_t()
ftd.rettype = ida_typeinf.tinfo_t(ida_typeinf.BTF_INT32)

arg1 = ida_typeinf.funcarg_t()
arg1.name = "str"
arg1.type = ida_typeinf.tinfo_t("const char *")
ftd.push_back(arg1)

arg2 = ida_typeinf.funcarg_t()
arg2.name = "count"
arg2.type = ida_typeinf.tinfo_t(ida_typeinf.BTF_INT32)
ftd.push_back(arg2)

tif = ida_typeinf.tinfo_t()
tif.create_func(ftd)
ida_typeinf.apply_tinfo(ea, tif, ida_typeinf.TINFO_DEFINITE)
```

### Create Structure
```python
udt = ida_typeinf.udt_type_data_t()
udt.is_union = False

# Add field: int x
m1 = ida_typeinf.udm_t()
m1.name = "x"
m1.type = ida_typeinf.tinfo_t(ida_typeinf.BTF_INT32)
m1.offset = 0
m1.size = 4
udt.push_back(m1)

tif = ida_typeinf.tinfo_t()
tif.create_udt(udt, ida_typeinf.BTF_STRUCT)
tif.set_numbered_type(ida_typeinf.get_idati(), 0,
    ida_typeinf.NTF_REPLACE, "MyStruct")
```

### Inspect Function Type
```python
tif = ida_typeinf.tinfo_t()
if ida_typeinf.get_tinfo(tif, ea):
    if tif.is_func():
        ftd = ida_typeinf.func_type_data_t()
        tif.get_func_details(ftd)
        print(f"Return: {ftd.rettype}")
        for i in range(ftd.size()):
            arg = ftd[i]
            print(f"Arg {i}: {arg.name} : {arg.type}")
```

## See Also
Full docs: skill/docs/ida_typeinf.rst
IDA Domain API: https://ida-domain.docs.hex-rays.com/ (simplified type operations)

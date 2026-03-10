# idautils

High-level utility functions for IDA - iteration, xrefs, decoding, assembly.

## Key Functions

### Cross-References
- `XrefsTo(ea, flags=0)` - iterate all xrefs to address (returns xref objects with `.frm`, `.to`, `.type`)
- `XrefsFrom(ea, flags=0)` - iterate all xrefs from address
- `CodeRefsTo(ea, flow)` - code references to address (list of EAs)
- `CodeRefsFrom(ea, flow)` - code references from address
- `DataRefsTo(ea)` - data references to address
- `DataRefsFrom(ea)` - data references from address
- `XrefTypeName(typecode)` - convert xref type code to readable name

### Iteration
- `Functions(start=None, end=None)` - iterate function entry points
- `FuncItems(start)` - iterate items (instructions/data) within function
- `Chunks(start)` - iterate function chunks (returns `(start_ea, end_ea)` tuples)
- `Heads(start=None, end=None)` - iterate all heads (instructions or data items)
- `Segments()` - iterate segment start addresses
- `Names()` - iterate all names (returns `(ea, name)` tuples)
- `Entries()` - iterate entry points/exports (returns `(index, ordinal, ea, name)` tuples)
- `Structs()` - iterate structures (returns `(ordinal, sid, name)` tuples)
- `StructMembers(sid)` - iterate structure members (returns `(offset, name, size)` tuples)

### Instruction Decoding
- `DecodeInstruction(ea)` - decode instruction at EA (returns `insn_t` instance or None)
- `DecodePreviousInstruction(ea)` - decode previous instruction
- `DecodePrecedingInstruction(ea)` - decode preceding instruction in execution flow (returns `(insn_t, farref)`)

### Assembly
- `Assemble(ea, line)` - assemble instruction(s) at address (returns `(success, result)`)

### Debugging
- `Threads()` - iterate thread IDs for current debuggee
- `Modules()` - iterate loaded modules (returns objects with `name`, `size`, `base`, `rebase_to`)

### Miscellaneous
- `GetIdbDir()` - get IDB directory path
- `GetRegisterList()` - get list of processor registers
- `GetInstructionList()` - get list of processor instructions
- `ProcessUiActions(actions, flags=0)` - execute UI actions programmatically
- `GetInputFileMD5` - MD5 hash of input file

## Key Classes

### Strings
Iterator for string list (also used by IDA's "Strings" window).

**Usage**:
```python
s = Strings()
for i in s:
    print(f"{i.ea:x}: len={i.length} type={i.strtype} -> '{i}'")
```

**Methods**:
- `setup(strtypes=[STRTYPE_C], minlen=5, only_7bit=True, ...)` - configure string search
- `refresh()` - refresh string list
- `clear_cache()` - clear string cache

**StringItem attributes**:
- `ea` - string address
- `strtype` - string type (STRTYPE_xxx)
- `length` - string length
- `is_1_byte_encoding()` - check encoding

### peutils_t
PE (Portable Executable) utility class for Windows binaries.

**Attributes**:
- `imagebase` - loading address (usually pe.imagebase)
- `header_offset` - offset of PE header
- `header` - complete PE header (`peheader_t` instance)

## Global Objects

### cpu
Register accessor - use as `cpu.Eax`, `cpu.Rsp`, etc. to read current register values during debugging.

### procregs
Processor register definitions - use to compare operands (e.g., `if x.Op1.reg == procregs.Esp`).

## See Also
Full docs: skill/docs/idautils.rst

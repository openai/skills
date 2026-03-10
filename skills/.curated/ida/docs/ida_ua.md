# ida_ua

Instruction disassembly, operand decoding, and instruction analysis.

## Key Classes

### insn_t
Decoded instruction with full operand details.
- Access via: `idaapi.insn_t()` or `idautils.DecodeInstruction(ea)`
- Contains array of up to 8 `op_t` operands

### op_t
Single instruction operand representation.
- `type` - Operand type (o_reg, o_mem, o_imm, o_displ, etc)
- `dtype` - Data type (dt_byte, dt_word, dt_dword, dt_qword, etc)
- `reg` - Register number (for o_reg)
- `addr` - Memory address (for o_mem, o_displ, o_near, o_far)
- `value` - Immediate value (for o_imm) or displacement
- `phrase` - Register phrase number (for o_phrase, o_displ)
- `shown()` - Check if operand should be displayed
- `is_reg(r)` / `is_imm(v)` - Type checks

## Operand Types

- `o_void` - No operand
- `o_reg` - Register (al, rax, xmm0, etc)
- `o_mem` - Direct memory `[0x401000]`
- `o_phrase` - Register indirect `[rax]`, `[rsi+rdi*4]`
- `o_displ` - Register + displacement `[rbp+var_10]`
- `o_imm` - Immediate constant `42`, `0x1000`
- `o_near` / `o_far` - Code reference (branch/call target)
- `o_idpspec0-5` - Processor-specific types

## Data Types (dtype)

- `dt_byte` (8), `dt_word` (16), `dt_dword` (32), `dt_qword` (64)
- `dt_byte16` (128), `dt_byte32` (256), `dt_byte64` (512)
- `dt_float`, `dt_double`, `dt_ldbl`, `dt_tbyte`

## Key Functions

### create_insn(ea)
Analyze and create instruction at address (updates IDB).

### decode_insn(insn, ea)
Decode instruction into insn_t object (read-only, no IDB changes).

### decode_prev_insn(insn, ea)
Decode instruction before given address.

### print_insn_mnem(ea)
Get instruction mnemonic string.

### print_operand(ea, n)
Get operand text representation (operand index n).

### get_dtype_size(dtype)
Get size in bytes for data type.

### get_dtype_by_size(size)
Get appropriate dtype for byte size.

## Usage Pattern

```python
insn = idaapi.insn_t()
if idaapi.decode_insn(insn, ea) > 0:
    for op in insn.ops:
        if op.type == idaapi.o_void:
            break  # No more operands
        if op.type == idaapi.o_reg:
            print(f"Register: {op.reg}")
        elif op.type == idaapi.o_imm:
            print(f"Immediate: {op.value:#x}")
```

## See Also
Full docs: skill/docs/ida_ua.rst

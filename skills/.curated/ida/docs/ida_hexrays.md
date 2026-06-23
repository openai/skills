# ida_hexrays

Hex-Rays decompiler - microcode and ctree (AST) representations. **Critical for decompilation work.**

## Core Architecture

**Two representations**:
- **Microcode**: Low-level optimized IR (mba_t, mblock_t, minsn_t, mop_t)
- **Ctree**: High-level AST-like C code (cfunc_t, cinsn_t, cexpr_t)

## Key Functions

### Decompilation
- `decompile(ea, hf=None, flags=0)` - Decompile function at address, returns cfuncptr_t
- `decompile_func(pfn, hf=None, flags=0)` - Decompile func_t object
- `gen_microcode(mbr, hf=None, retlist=None, flags=0, reqmat=MMAT_GLBOPT3)` - Generate microcode only

### Callbacks
- `install_hexrays_callback(callback)` - Register event hook (hxe_maturity, hxe_print_func, etc.)

## Ctree Classes (High-Level)

### cfunc_t
Decompiled function - the main result.
- `body` - Root cinsn_t (function body)
- `lvars` - List of local variables (lvar_t)
- `mba` - Underlying microcode (mba_t)
- `get_pseudocode()` - Get text as list of lines
- `build_c_tree()` - Rebuild ctree from microcode
- `verify(allow_cot_empty)` - Validate ctree integrity

### cinsn_t
C statement (if, for, while, return, expression, block, etc.).
- `op` - Statement type (cit_block, cit_if, cit_for, cit_while, cit_return, etc.)
- `ea` - Associated address
- `cif`, `cfor`, `cwhile`, `creturn`, `cexpr` - Type-specific data unions
- Access via: `insn.cif.expr` (if condition), `insn.cblock` (compound statement)

### cexpr_t
C expression (operators, variables, constants, calls, etc.).
- `op` - Expression type (cot_var, cot_num, cot_call, cot_add, cot_cast, etc.)
- `type` - Expression type info (tinfo_t)
- `x`, `y`, `z` - Operands (for binary/ternary ops)
- `n` - Number value (cnumber_t)
- `v` - Variable reference (var_ref_t)
- `obj_ea` - Global variable/function address
- `print1()` - Format as text

### citem_t
Base class for cinsn_t and cexpr_t.
- `ea` - Address
- `op` - Opcode (ctype_t enum)
- `contains_label()` - Has goto label

## Microcode Classes (Low-Level)

### mba_t
Microcode array - function as basic blocks.
- `qty` - Number of blocks
- `get_mblock(n)` - Get block by index
- `natural` - Natural (entry) block array
- `vars` - Local variables (lvars_t)
- `maturity` - Optimization level (MMAT_ZERO to MMAT_LVARS)
- `build_graph()` - Construct CFG
- `optimize_local(blk)` - Optimize single block
- `optimize_global()` - Global optimization pass

### mblock_t
Basic block in microcode.
- `head`, `tail` - First/last instruction (minsn_t)
- `start`, `end` - Address range
- `type` - Block type (BLT_STOP, BLT_1WAY, BLT_2WAY, BLT_NWAY)
- `nsucc()`, `npred()` - Successor/predecessor counts
- `succ(n)`, `pred(n)` - Get nth successor/predecessor
- `for_all_insns(visitor)` - Iterate instructions
- `insert_into_block(ins, where)` - Add instruction

### minsn_t
Microcode instruction.
- `opcode` - Operation (m_mov, m_add, m_call, m_ldx, m_stx, etc.)
- `l`, `r`, `d` - Left, right, destination operands (mop_t)
- `ea` - Instruction address
- `next`, `prev` - Linked list pointers
- `is_assert()` - Check if assertion
- `equal_mops(other)` - Compare operands
- `for_all_ops(visitor)` - Iterate operands

### mop_t
Microcode operand.
- `t` - Operand type (mop_z=none, mop_r=register, mop_n=immediate, mop_S=stack, mop_v=global, mop_b=block, mop_f=case, mop_l=local var, mop_a=address, mop_h=helper, mop_str=string, mop_c=call, mop_fn=function, mop_p=pair, mop_sc=scattered)
- `r` - Register number (if mop_r)
- `nnn` - Immediate value (mnumber_t, if mop_n)
- `g` - Global address (if mop_v)
- `s` - Stack offset (stkvar_ref_t, if mop_S)
- `l` - Local var reference (lvar_t, if mop_l)
- `size` - Operand size in bytes
- `is_reg(reg, size)` - Check if specific register
- `is_const()` - Check if constant

### lvar_t
Local variable (stack/register).
- `name` - Variable name
- `type` - Variable type (tinfo_t)
- `location` - vdloc_t (register or stack location)
- `defea` - Definition address
- `width` - Size in bytes
- `is_stk_var()`, `is_reg_var()` - Location checks
- `set_lvar_type(tif)` - Change type

## Key Event Types

**Maturity levels** (microcode optimization stages):
- MMAT_ZERO - Unoptimized
- MMAT_GENERATED - After instruction generation
- MMAT_PREOPTIMIZED - After pre-optimization
- MMAT_LOCOPT - After local optimization
- MMAT_CALLS - After call analysis
- MMAT_GLBOPT1/2/3 - Global optimization passes
- MMAT_LVARS - After local variable allocation

**Callback events**:
- hxe_maturity - Microcode maturity changed
- hxe_print_func - About to print function
- hxe_func_printed - Function printed
- hxe_open_pseudocode - Pseudocode window opened
- hxe_create_hint - Create hover hint

## Common Patterns

### Decompile and get text
```python
cfunc = ida_hexrays.decompile(ea)
for line in cfunc.get_pseudocode():
    print(line.line)
```

### Modify variable name/type
```python
cfunc = ida_hexrays.decompile(ea)
lvar = cfunc.lvars[0]
lvar.name = "new_name"
lvar.set_lvar_type(new_tinfo)
cfunc.save_user_labels()
```

### Walk ctree
```python
class visitor(ida_hexrays.ctree_visitor_t):
    def visit_expr(self, e):
        if e.op == ida_hexrays.cot_call:
            print(f"Call at {e.ea:#x}")
        return 0

cfunc = ida_hexrays.decompile(ea)
visitor().apply_to(cfunc.body, None)
```

### Walk microcode
```python
mba = ida_hexrays.gen_microcode(...)
for blk in mba.natural:
    ins = blk.head
    while ins:
        print(f"{ins.ea:#x}: {ins.opcode}")
        ins = ins.next
```

## See Also
Full docs: skill/docs/ida_hexrays.rst

**External resources**:
- https://hex-rays.com/blog/hex-rays-decompiler-primer
- https://hex-rays.com/blog/microcode-in-pictures

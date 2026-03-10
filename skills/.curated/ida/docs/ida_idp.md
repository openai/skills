# ida_idp

Interface to processor modules - defines target assembler and processor features.

## Key Classes/Functions

### Instruction Analysis
- `is_call_insn(insn)` - is instruction a call?
- `is_ret_insn(insn, flags)` - is instruction a return?
- `is_indirect_jump_insn(insn)` - is instruction an indirect jump?
- `is_basic_block_end(insn, call_stops_block)` - does instruction end a basic block?
- `has_cf_chg(feature, opnum)` - does instruction modify operand?
- `has_cf_use(feature, opnum)` - does instruction use operand value?

### Processor Info
- `get_ph()` - get processor_t structure
- `get_ash()` - get assembler asm_t structure
- `set_processor_type(processor_name, level)` - change processor module
- `get_idp_name()` - get current processor name
- `str2reg(regname)` - convert register name to index
- `get_reg_name(regidx, width)` - get register name

### processor_t
Global processor structure (accessed via `ph`)
- `ph.id` - processor ID (PLFM_386, PLFM_ARM, PLFM_MIPS, etc.)
- `ph.flag` - processor flags (PR_SEGS, PR_USE32, PR_USE64, etc.)
- `ph.cnbits` / `ph.dnbits` - code/data address bits
- `ph_get_instruc()` - get instruction names

### Instruction Features (CF_*)
- CF_STOP - doesn't continue execution
- CF_CALL - call instruction
- CF_CHG1..CF_CHG8 - modifies operand 1-8
- CF_USE1..CF_USE8 - uses operand 1-8
- CF_JUMP - indirect jump/call

## See Also
Full docs: skill/docs/ida_idp.rst

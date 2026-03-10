# ida_gdl

Low level graph drawing operations - flow charts and call graphs.

## Key Classes

### FlowChart
Pythonic flowchart class for determining basic blocks.
- `FlowChart(f, bounds, flags)` - Create flow chart for function
- `size` - Number of blocks in flow chart
- `refresh()` - Refresh flow chart
- Iterate blocks directly: `for bb in fc: ...`

### BasicBlock
Basic block within a flowchart.
- `id` - Block number
- `start_ea`, `end_ea` - Address range
- `type` - Block type (fcb_normal, fcb_ret, fcb_noret, etc.)
- `preds()` - Iterator over predecessor blocks
- `succs()` - Iterator over successor blocks

### qflow_chart_t
Low-level flow chart builder (use FlowChart instead for Python).
- `create(title, pfn, ea1, ea2, flags)` - Build flow chart
- `nsucc(node)`, `npred(node)` - Successor/predecessor counts
- `succ(node, i)`, `pred(node, i)` - Get nth successor/predecessor

## Key Functions

- `gen_flow_graph(filename, title, pfn, ea1, ea2, gflags)` - Generate flow graph to .dot/.gdl
- `gen_simple_call_chart(filename, wait, title, gflags)` - Simple call graph
- `is_ret_block(btype)` - Check if block returns
- `is_noret_block(btype)` - Check if block never returns

## Constants

**Block types**: fcb_normal, fcb_indjump, fcb_ret, fcb_cndret, fcb_noret, fcb_enoret, fcb_extern, fcb_error

**Flow chart flags**: FC_NOEXT (no external blocks), FC_CALL_ENDS (calls end blocks), FC_NOPREDS (skip predecessors)

**Chart generation**: CHART_GEN_DOT, CHART_GEN_GDL, CHART_WINGRAPH, CHART_NOLIBFUNCS

## See Also
Full docs: skill/docs/ida_gdl.rst

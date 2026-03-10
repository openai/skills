ida_gdl
=======

.. py:module:: ida_gdl

.. autoapi-nested-parse::

   Low level graph drawing operations.

   .. tip:: 
      The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies 
      common tasks and provides better type hints, while remaining fully compatible 
      with IDAPython for advanced use cases.
      
      For graph operations, see :mod:`ida_domain.functions`.



Attributes
----------

.. autoapisummary::

   ida_gdl.fcb_normal
   ida_gdl.fcb_indjump
   ida_gdl.fcb_ret
   ida_gdl.fcb_cndret
   ida_gdl.fcb_noret
   ida_gdl.fcb_enoret
   ida_gdl.fcb_extern
   ida_gdl.fcb_error
   ida_gdl.EDGE_NONE
   ida_gdl.EDGE_TREE
   ida_gdl.EDGE_FORWARD
   ida_gdl.EDGE_BACK
   ida_gdl.EDGE_CROSS
   ida_gdl.EDGE_SUBGRAPH
   ida_gdl.CHART_PRINT_NAMES
   ida_gdl.CHART_GEN_DOT
   ida_gdl.CHART_GEN_GDL
   ida_gdl.CHART_WINGRAPH
   ida_gdl.CHART_NOLIBFUNCS
   ida_gdl.CHART_REFERENCING
   ida_gdl.CHART_REFERENCED
   ida_gdl.CHART_RECURSIVE
   ida_gdl.CHART_FOLLOW_DIRECTION
   ida_gdl.CHART_IGNORE_XTRN
   ida_gdl.CHART_IGNORE_DATA_BSS
   ida_gdl.CHART_IGNORE_LIB_TO
   ida_gdl.CHART_IGNORE_LIB_FROM
   ida_gdl.CHART_PRINT_COMMENTS
   ida_gdl.CHART_PRINT_DOTS
   ida_gdl.FC_PRINT
   ida_gdl.FC_NOEXT
   ida_gdl.FC_RESERVED
   ida_gdl.FC_APPND
   ida_gdl.FC_CHKBREAK
   ida_gdl.FC_CALL_ENDS
   ida_gdl.FC_NOPREDS
   ida_gdl.FC_OUTLINES
   ida_gdl.FC_PREDS


Classes
-------

.. autoapisummary::

   ida_gdl.edge_t
   ida_gdl.edgevec_t
   ida_gdl.node_ordering_t
   ida_gdl.node_iterator
   ida_gdl.gdl_graph_t
   ida_gdl.cancellable_graph_t
   ida_gdl.qbasic_block_t
   ida_gdl.qflow_chart_t
   ida_gdl.BasicBlock
   ida_gdl.FlowChart


Functions
---------

.. autoapisummary::

   ida_gdl.gen_gdl
   ida_gdl.display_gdl
   ida_gdl.gen_flow_graph
   ida_gdl.gen_simple_call_chart
   ida_gdl.gen_complex_call_chart
   ida_gdl.is_noret_block
   ida_gdl.is_ret_block


Module Contents
---------------

.. py:data:: fcb_normal

   normal block


.. py:data:: fcb_indjump

   block ends with indirect jump


.. py:data:: fcb_ret

   return block


.. py:data:: fcb_cndret

   conditional return block


.. py:data:: fcb_noret

   noreturn block


.. py:data:: fcb_enoret

   external noreturn block (does not belong to the function)


.. py:data:: fcb_extern

   external normal block


.. py:data:: fcb_error

   block passes execution past the function end


.. py:class:: edge_t(x: int = 0, y: int = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: src
      :type:  int

      source node number



   .. py:attribute:: dst
      :type:  int

      destination node number



.. py:class:: edgevec_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


.. py:data:: EDGE_NONE

.. py:data:: EDGE_TREE

.. py:data:: EDGE_FORWARD

.. py:data:: EDGE_BACK

.. py:data:: EDGE_CROSS

.. py:data:: EDGE_SUBGRAPH

.. py:class:: node_ordering_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: clear() -> None


   .. py:method:: resize(n: int) -> None


   .. py:method:: size() -> size_t


   .. py:method:: set(_node: int, num: int) -> None


   .. py:method:: clr(_node: int) -> bool


   .. py:method:: node(_order: size_t) -> int


   .. py:method:: order(_node: int) -> int


.. py:class:: node_iterator(_g: gdl_graph_t, n: int)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


.. py:class:: gdl_graph_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: get_node_label(n: int) -> char *


   .. py:method:: print_graph_attributes(fp: FILE *) -> None


   .. py:method:: print_node(fp: FILE *, n: int) -> bool


   .. py:method:: print_edge(fp: FILE *, i: int, j: int) -> bool


   .. py:method:: print_node_attributes(fp: FILE *, n: int) -> None


   .. py:method:: size() -> int


   .. py:method:: node_qty() -> int


   .. py:method:: exists(node: int) -> bool


   .. py:method:: entry() -> int


   .. py:method:: exit() -> int


   .. py:method:: nsucc(node: int) -> int


   .. py:method:: npred(node: int) -> int


   .. py:method:: succ(node: int, i: int) -> int


   .. py:method:: pred(node: int, i: int) -> int


   .. py:method:: empty() -> bool


   .. py:method:: get_node_color(n: int) -> bgcolor_t


   .. py:method:: get_edge_color(i: int, j: int) -> bgcolor_t


   .. py:method:: nedge(node: int, ispred: bool) -> size_t


   .. py:method:: edge(node: int, i: int, ispred: bool) -> int


   .. py:method:: front() -> int


   .. py:method:: begin() -> node_iterator


   .. py:method:: end() -> node_iterator


.. py:function:: gen_gdl(g: gdl_graph_t, fname: str) -> None

   Create GDL file for graph.


.. py:function:: display_gdl(fname: str) -> int

   Display GDL file by calling wingraph32. The exact name of the grapher is taken from the configuration file and set up by setup_graph_subsystem(). The path should point to a temporary file: when wingraph32 succeeds showing the graph, the input file will be deleted. 
           
   :returns: error code from os, 0 if ok


.. py:function:: gen_flow_graph(filename: str, title: str, pfn: func_t *, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, gflags: int) -> bool

   Build and display a flow graph. 
           
   :param filename: output file name. the file extension is not used. maybe nullptr.
   :param title: graph title
   :param pfn: function to graph
   :param ea1: if pfn == nullptr, then the address range
   :param ea2: if pfn == nullptr, then the address range
   :param gflags: combination of Flow graph building flags. if none of CHART_GEN_DOT, CHART_GEN_GDL, CHART_WINGRAPH is specified, the function will return false
   :returns: success. if fails, a warning message is displayed on the screen


.. py:data:: CHART_PRINT_NAMES

   print labels for each block?


.. py:data:: CHART_GEN_DOT

   generate .dot file (file extension is forced to .dot)


.. py:data:: CHART_GEN_GDL

   generate .gdl file (file extension is forced to .gdl)


.. py:data:: CHART_WINGRAPH

   call grapher to display the graph


.. py:function:: gen_simple_call_chart(filename: str, wait: str, title: str, gflags: int) -> bool

   Build and display a simple function call graph. 
           
   :param filename: output file name. the file extension is not used. maybe nullptr.
   :param wait: message to display during graph building
   :param title: graph title
   :param gflags: combination of CHART_NOLIBFUNCS and Flow graph building flags. if none of CHART_GEN_DOT, CHART_GEN_GDL, CHART_WINGRAPH is specified, the function will return false.
   :returns: success. if fails, a warning message is displayed on the screen


.. py:function:: gen_complex_call_chart(filename: str, wait: str, title: str, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, flags: int, recursion_depth: int = -1) -> bool

   Build and display a complex xref graph. 
           
   :param filename: output file name. the file extension is not used. maybe nullptr.
   :param wait: message to display during graph building
   :param title: graph title
   :param ea1: address range
   :param ea2: address range
   :param flags: combination of Call chart building flags and Flow graph building flags. if none of CHART_GEN_DOT, CHART_GEN_GDL, CHART_WINGRAPH is specified, the function will return false.
   :param recursion_depth: optional limit of recursion
   :returns: success. if fails, a warning message is displayed on the screen


.. py:data:: CHART_NOLIBFUNCS

   don't include library functions in the graph


.. py:data:: CHART_REFERENCING

   references to the addresses in the list


.. py:data:: CHART_REFERENCED

   references from the addresses in the list


.. py:data:: CHART_RECURSIVE

   analyze added blocks


.. py:data:: CHART_FOLLOW_DIRECTION

   analyze references to added blocks only in the direction of the reference who discovered the current block


.. py:data:: CHART_IGNORE_XTRN

.. py:data:: CHART_IGNORE_DATA_BSS

.. py:data:: CHART_IGNORE_LIB_TO

   ignore references to library functions


.. py:data:: CHART_IGNORE_LIB_FROM

   ignore references from library functions


.. py:data:: CHART_PRINT_COMMENTS

.. py:data:: CHART_PRINT_DOTS

   print dots if xrefs exist outside of the range recursion depth


.. py:class:: cancellable_graph_t

   Bases: :py:obj:`gdl_graph_t`


   .. py:attribute:: thisown


   .. py:attribute:: cancelled
      :type:  bool


.. py:class:: qbasic_block_t

   Bases: :py:obj:`ida_range.range_t`


   .. py:attribute:: thisown


.. py:function:: is_noret_block(btype: fc_block_type_t) -> bool

   Does this block never return?


.. py:function:: is_ret_block(btype: fc_block_type_t) -> bool

   Does this block return?


.. py:data:: FC_PRINT

   print names (used only by display_flow_chart())


.. py:data:: FC_NOEXT

   do not compute external blocks. Use this to prevent jumps leaving the function from appearing in the flow chart. Unless specified, the targets of those outgoing jumps will be present in the flow chart under the form of one-instruction blocks 
           


.. py:data:: FC_RESERVED

   former FC_PREDS


.. py:data:: FC_APPND

   multirange flowchart (set by append_to_flowchart)


.. py:data:: FC_CHKBREAK

   build_qflow_chart() may be aborted by user


.. py:data:: FC_CALL_ENDS

   call instructions terminate basic blocks


.. py:data:: FC_NOPREDS

   do not compute predecessor lists


.. py:data:: FC_OUTLINES

   include outlined code (with FUNC_OUTLINE)


.. py:class:: qflow_chart_t(*args)

   Bases: :py:obj:`cancellable_graph_t`


   .. py:attribute:: thisown


   .. py:attribute:: title
      :type:  str


   .. py:attribute:: bounds
      :type:  range_t

      overall bounds of the qflow_chart_t instance



   .. py:attribute:: pfn
      :type:  func_t *

      the function this instance was built upon



   .. py:attribute:: flags
      :type:  int

      flags. See Flow chart flags



   .. py:attribute:: nproper
      :type:  int

      number of basic blocks belonging to the specified range



   .. py:method:: create(*args) -> None

      This function has the following signatures:

          0. create(_title: str, _pfn: func_t *, _ea1: ida_idaapi.ea_t, _ea2: ida_idaapi.ea_t, _flags: int) -> None
          1. create(_title: str, ranges: const rangevec_t &, _flags: int) -> None

      # 0: create(_title: str, _pfn: func_t *, _ea1: ida_idaapi.ea_t, _ea2: ida_idaapi.ea_t, _flags: int) -> None


      # 1: create(_title: str, ranges: const rangevec_t &, _flags: int) -> None



   .. py:method:: append_to_flowchart(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> None


   .. py:method:: refresh() -> None


   .. py:method:: calc_block_type(blknum: size_t) -> fc_block_type_t


   .. py:method:: is_ret_block(blknum: size_t) -> bool


   .. py:method:: is_noret_block(blknum: size_t) -> bool


   .. py:method:: print_node_attributes(fp: FILE *, n: int) -> None


   .. py:method:: nsucc(node: int) -> int


   .. py:method:: npred(node: int) -> int


   .. py:method:: succ(node: int, i: int) -> int


   .. py:method:: pred(node: int, i: int) -> int


   .. py:method:: get_node_label(*args) -> char *


   .. py:method:: size() -> int


   .. py:method:: print_names() -> bool


.. py:class:: BasicBlock(id, bb, fc)

   Bases: :py:obj:`object`


   Basic block class. It is returned by the Flowchart class


   .. py:attribute:: id

      Basic block ID



   .. py:attribute:: start_ea

      start_ea of basic block



   .. py:attribute:: end_ea

      end_ea of basic block



   .. py:attribute:: type

      Block type (check fc_block_type_t enum)



   .. py:method:: preds()

      Iterates the predecessors list



   .. py:method:: succs()

      Iterates the successors list



.. py:class:: FlowChart(f=None, bounds=None, flags=0)

   Bases: :py:obj:`object`


   Flowchart class used to determine basic blocks.
   Check ex_gdl_qflow_chart.py for sample usage.


   .. py:attribute:: size

      Number of blocks in the flow chart



   .. py:method:: refresh()

      Refreshes the flow chart



.. py:data:: FC_PREDS
   :value: 0



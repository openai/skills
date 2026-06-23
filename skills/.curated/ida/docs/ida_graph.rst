ida_graph
=========

.. py:module:: ida_graph

.. autoapi-nested-parse::

   Graph view management.



Attributes
----------

.. autoapisummary::

   ida_graph.NIF_BG_COLOR
   ida_graph.NIF_FRAME_COLOR
   ida_graph.NIF_EA
   ida_graph.NIF_TEXT
   ida_graph.NIF_FLAGS
   ida_graph.NIF_ALL
   ida_graph.GLICTL_CENTER
   ida_graph.NIFF_SHOW_CONTENTS
   ida_graph.cvar
   ida_graph.layout_none
   ida_graph.layout_digraph
   ida_graph.layout_tree
   ida_graph.layout_circle
   ida_graph.layout_polar_tree
   ida_graph.layout_orthogonal
   ida_graph.layout_radial_tree
   ida_graph.git_none
   ida_graph.git_edge
   ida_graph.git_node
   ida_graph.git_tool
   ida_graph.git_text
   ida_graph.git_elp
   ida_graph.ygap
   ida_graph.xgap
   ida_graph.arrow_height
   ida_graph.arrow_width
   ida_graph.MTG_GROUP_NODE
   ida_graph.MTG_DOT_NODE
   ida_graph.MTG_NON_DISPLAYABLE_NODE
   ida_graph.COLLAPSED_NODE
   ida_graph.grcode_calculating_layout
   ida_graph.grcode_layout_calculated
   ida_graph.grcode_changed_graph
   ida_graph.grcode_reserved
   ida_graph.grcode_clicked
   ida_graph.grcode_dblclicked
   ida_graph.grcode_creating_group
   ida_graph.grcode_deleting_group
   ida_graph.grcode_group_visibility
   ida_graph.grcode_gotfocus
   ida_graph.grcode_lostfocus
   ida_graph.grcode_user_refresh
   ida_graph.grcode_reserved2
   ida_graph.grcode_user_text
   ida_graph.grcode_user_size
   ida_graph.grcode_user_title
   ida_graph.grcode_user_draw
   ida_graph.grcode_user_hint
   ida_graph.grcode_destroyed
   ida_graph.grcode_create_graph_viewer
   ida_graph.grcode_get_graph_viewer
   ida_graph.grcode_get_viewer_graph
   ida_graph.grcode_create_interactive_graph
   ida_graph.grcode_set_viewer_graph
   ida_graph.grcode_refresh_viewer
   ida_graph.grcode_fit_window
   ida_graph.grcode_get_curnode
   ida_graph.grcode_center_on
   ida_graph.grcode_get_selection
   ida_graph.grcode_del_custom_layout
   ida_graph.grcode_set_custom_layout
   ida_graph.grcode_set_graph_groups
   ida_graph.grcode_clear
   ida_graph.grcode_create_digraph_layout
   ida_graph.grcode_create_tree_layout
   ida_graph.grcode_create_circle_layout
   ida_graph.grcode_get_node_representative
   ida_graph.grcode_find_subgraph_node
   ida_graph.grcode_create_group
   ida_graph.grcode_get_custom_layout
   ida_graph.grcode_get_graph_groups
   ida_graph.grcode_empty
   ida_graph.grcode_is_visible_node
   ida_graph.grcode_delete_group
   ida_graph.grcode_change_group_visibility
   ida_graph.grcode_set_edge
   ida_graph.grcode_node_qty
   ida_graph.grcode_nrect
   ida_graph.grcode_set_titlebar_height
   ida_graph.grcode_create_user_graph_place
   ida_graph.grcode_create_disasm_graph1
   ida_graph.grcode_create_disasm_graph2
   ida_graph.grcode_set_node_info
   ida_graph.grcode_get_node_info
   ida_graph.grcode_del_node_info
   ida_graph.grcode_viewer_create_groups
   ida_graph.grcode_viewer_delete_groups
   ida_graph.grcode_viewer_groups_visibility
   ida_graph.grcode_viewer_create_groups_vec
   ida_graph.grcode_viewer_delete_groups_vec
   ida_graph.grcode_viewer_groups_visibility_vec
   ida_graph.grcode_delete_interactive_graph
   ida_graph.grcode_edge_infos_wrapper_copy
   ida_graph.grcode_edge_infos_wrapper_clear
   ida_graph.grcode_attach_menu_item
   ida_graph.grcode_set_gli
   ida_graph.grcode_get_gli
   ida_graph.edge_t
   ida_graph.node_ordering_t
   ida_graph.abstract_graph_t
   ida_graph.mutable_graph_t
   ida_graph.create_mutable_graph
   ida_graph.delete_mutable_graph
   ida_graph.grcode_create_mutable_graph
   ida_graph.grcode_create_mutable_graph


Classes
-------

.. autoapisummary::

   ida_graph.screen_graph_selection_base_t
   ida_graph.node_layout_t
   ida_graph.pointvec_t
   ida_graph.node_info_t
   ida_graph.graph_node_visitor_t
   ida_graph.graph_path_visitor_t
   ida_graph.point_t
   ida_graph.pointseq_t
   ida_graph.rect_t
   ida_graph.TPointDouble
   ida_graph.edge_info_t
   ida_graph.edge_layout_point_t
   ida_graph.selection_item_t
   ida_graph.screen_graph_selection_t
   ida_graph.edge_segment_t
   ida_graph.graph_item_t
   ida_graph.interval_t
   ida_graph.row_info_t
   ida_graph.drawable_graph_t
   ida_graph.edge_infos_wrapper_t
   ida_graph.interactive_graph_t
   ida_graph.graph_visitor_t
   ida_graph.group_crinfo_t
   ida_graph.user_graph_place_t
   ida_graph.GraphViewer


Functions
---------

.. autoapisummary::

   ida_graph.get_node_info
   ida_graph.set_node_info
   ida_graph.del_node_info
   ida_graph.clr_node_info
   ida_graph.calc_dist
   ida_graph.create_graph_viewer
   ida_graph.get_graph_viewer
   ida_graph.create_interactive_graph
   ida_graph.create_disasm_graph
   ida_graph.get_viewer_graph
   ida_graph.set_viewer_graph
   ida_graph.refresh_viewer
   ida_graph.viewer_fit_window
   ida_graph.viewer_get_curnode
   ida_graph.viewer_center_on
   ida_graph.viewer_set_gli
   ida_graph.viewer_get_gli
   ida_graph.viewer_set_node_info
   ida_graph.viewer_get_node_info
   ida_graph.viewer_del_node_info
   ida_graph.viewer_create_groups
   ida_graph.viewer_delete_groups
   ida_graph.viewer_set_groups_visibility
   ida_graph.viewer_attach_menu_item
   ida_graph.viewer_get_selection
   ida_graph.viewer_set_titlebar_height
   ida_graph.delete_interactive_graph
   ida_graph.create_user_graph_place
   ida_graph.pyg_close
   ida_graph.pyg_select_node
   ida_graph.pyg_show


Module Contents
---------------

.. py:class:: screen_graph_selection_base_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> selection_item_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> selection_item_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: screen_graph_selection_base_t) -> None


   .. py:method:: extract() -> selection_item_t *


   .. py:method:: inject(s: selection_item_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< selection_item_t >::const_iterator


   .. py:method:: end(*args) -> qvector< selection_item_t >::const_iterator


   .. py:method:: insert(it: selection_item_t, x: selection_item_t) -> qvector< selection_item_t >::iterator


   .. py:method:: erase(*args) -> qvector< selection_item_t >::iterator


   .. py:method:: find(*args) -> qvector< selection_item_t >::const_iterator


   .. py:method:: has(x: selection_item_t) -> bool


   .. py:method:: add_unique(x: selection_item_t) -> bool


   .. py:method:: append(x: selection_item_t) -> None


   .. py:method:: extend(x: screen_graph_selection_base_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: node_layout_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> rect_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> rect_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: node_layout_t) -> None


   .. py:method:: extract() -> rect_t *


   .. py:method:: inject(s: rect_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< rect_t >::const_iterator


   .. py:method:: end(*args) -> qvector< rect_t >::const_iterator


   .. py:method:: insert(it: rect_t, x: rect_t) -> qvector< rect_t >::iterator


   .. py:method:: erase(*args) -> qvector< rect_t >::iterator


   .. py:method:: find(*args) -> qvector< rect_t >::const_iterator


   .. py:method:: has(x: rect_t) -> bool


   .. py:method:: add_unique(x: rect_t) -> bool


   .. py:method:: append(x: rect_t) -> None


   .. py:method:: extend(x: node_layout_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: pointvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> point_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> point_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: pointvec_t) -> None


   .. py:method:: extract() -> point_t *


   .. py:method:: inject(s: point_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< point_t >::const_iterator


   .. py:method:: end(*args) -> qvector< point_t >::const_iterator


   .. py:method:: insert(it: point_t, x: point_t) -> qvector< point_t >::iterator


   .. py:method:: erase(*args) -> qvector< point_t >::iterator


   .. py:method:: find(*args) -> qvector< point_t >::const_iterator


   .. py:method:: has(x: point_t) -> bool


   .. py:method:: add_unique(x: point_t) -> bool


   .. py:method:: append(x: point_t) -> None


   .. py:method:: extend(x: pointvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:data:: NIF_BG_COLOR

   node_info_t::bg_color


.. py:data:: NIF_FRAME_COLOR

   node_info_t::frame_color


.. py:data:: NIF_EA

   node_info_t::ea


.. py:data:: NIF_TEXT

   node_info_t::text


.. py:data:: NIF_FLAGS

   node_info_t::flags


.. py:data:: NIF_ALL

.. py:data:: GLICTL_CENTER

   the gli should be set/get as center


.. py:class:: node_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: bg_color
      :type:  bgcolor_t

      background color



   .. py:attribute:: frame_color
      :type:  bgcolor_t

      color of enclosing frame



   .. py:attribute:: flags
      :type:  int

      flags



   .. py:attribute:: ea
      :type:  ida_idaapi.ea_t

      address



   .. py:attribute:: text
      :type:  str

      node contents



   .. py:method:: valid_bg_color() -> bool

      Has valid bg_color?



   .. py:method:: valid_frame_color() -> bool

      Has valid frame_color?



   .. py:method:: valid_ea() -> bool

      Has valid ea?



   .. py:method:: valid_text() -> bool

      Has non-empty text?



   .. py:method:: valid_flags() -> bool

      Has valid flags?



   .. py:method:: get_flags_for_valid() -> int

      Get combination of Node info flags describing which attributes are valid.



.. py:data:: NIFF_SHOW_CONTENTS

.. py:function:: get_node_info(out: node_info_t, gid: graph_id_t, node: int) -> bool

   Get node info. 
           
   :param out: result
   :param gid: id of desired graph
   :param node: node number
   :returns: success


.. py:function:: set_node_info(gid: graph_id_t, node: int, ni: node_info_t, flags: int) -> None

   Set node info. 
           
   :param gid: id of desired graph
   :param node: node number
   :param ni: node info to use
   :param flags: combination of Node info flags, identifying which fields of 'ni' will be used


.. py:function:: del_node_info(gid: graph_id_t, node: int) -> None

   Delete the node_info_t for the given node.


.. py:function:: clr_node_info(gid: graph_id_t, node: int, flags: int) -> None

   Clear node info for the given node. 
           
   :param gid: id of desired graph
   :param node: node number
   :param flags: combination of Node info flags, identifying which fields of node_info_t will be cleared


.. py:class:: graph_node_visitor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: reinit() -> None

      Reset visited nodes.



   .. py:method:: set_visited(n: int) -> None

      Mark node as visited.



   .. py:method:: is_visited(n: int) -> bool

      Have we already visited the given node?



   .. py:method:: visit_node(arg0: int) -> int

      Implements action to take when a node is visited.



   .. py:method:: is_forbidden_edge(arg0: int, arg1: int) -> bool

      Should the edge between 'n' and 'm' be ignored?



.. py:class:: graph_path_visitor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: path
      :type:  intvec_t

      current path



   .. py:attribute:: prune
      :type:  bool

      walk_forward(): prune := true means to stop the current path 
              



   .. py:method:: walk_forward(arg0: int) -> int


   .. py:method:: walk_backward(arg0: int) -> int


.. py:class:: point_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  int


   .. py:attribute:: y
      :type:  int


   .. py:method:: add(r: point_t) -> point_t &


   .. py:method:: sub(r: point_t) -> point_t &


   .. py:method:: negate() -> None


.. py:function:: calc_dist(p: point_t, q: point_t) -> double

   Calculate distance between p and q.


.. py:class:: pointseq_t

   Bases: :py:obj:`pointvec_t`


   .. py:attribute:: thisown


.. py:class:: rect_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: left
      :type:  int


   .. py:attribute:: top
      :type:  int


   .. py:attribute:: right
      :type:  int


   .. py:attribute:: bottom
      :type:  int


   .. py:method:: verify() -> None


   .. py:method:: width() -> int


   .. py:method:: height() -> int


   .. py:method:: move_to(p: point_t) -> None


   .. py:method:: move_by(p: point_t) -> None


   .. py:method:: center() -> point_t


   .. py:method:: topleft() -> point_t


   .. py:method:: bottomright() -> point_t


   .. py:method:: grow(delta: int) -> None


   .. py:method:: intersect(r: rect_t) -> None


   .. py:method:: make_union(r: rect_t) -> None


   .. py:method:: empty() -> bool


   .. py:method:: is_intersection_empty(r: rect_t) -> bool


   .. py:method:: contains(p: point_t) -> bool


   .. py:method:: area() -> int


.. py:class:: TPointDouble(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x
      :type:  double


   .. py:attribute:: y
      :type:  double


   .. py:method:: add(r: TPointDouble) -> None


   .. py:method:: sub(r: TPointDouble) -> None


   .. py:method:: negate() -> None


.. py:class:: edge_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: color
      :type:  bgcolor_t

      edge color



   .. py:attribute:: width
      :type:  int

      edge width



   .. py:attribute:: srcoff
      :type:  int

      source: edge port offset from the left



   .. py:attribute:: dstoff
      :type:  int

      destination: edge port offset from the left



   .. py:attribute:: layout
      :type:  pointseq_t

      describes geometry of edge



   .. py:method:: reverse_layout() -> None


.. py:data:: cvar

.. py:data:: layout_none

.. py:data:: layout_digraph

.. py:data:: layout_tree

.. py:data:: layout_circle

.. py:data:: layout_polar_tree

.. py:data:: layout_orthogonal

.. py:data:: layout_radial_tree

.. py:class:: edge_layout_point_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: pidx
      :type:  int

      index into edge_info_t::layout



   .. py:attribute:: e
      :type:  edge_t

      parent edge



   .. py:method:: compare(r: edge_layout_point_t) -> int


.. py:class:: selection_item_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: is_node
      :type:  bool

      represents a selected node?



   .. py:attribute:: node
      :type:  int

      node number (is_node = true)



   .. py:attribute:: elp
      :type:  edge_layout_point_t

      edge layout point (is_node = false)



   .. py:method:: compare(r: selection_item_t) -> int


.. py:class:: screen_graph_selection_t

   Bases: :py:obj:`screen_graph_selection_base_t`


   .. py:attribute:: thisown


   .. py:method:: has(item: selection_item_t) -> bool


   .. py:method:: add(s: screen_graph_selection_t) -> None


   .. py:method:: sub(s: screen_graph_selection_t) -> None


   .. py:method:: add_node(node: int) -> None


   .. py:method:: del_node(node: int) -> None


   .. py:method:: add_point(e: edge_t, idx: int) -> None


   .. py:method:: del_point(e: edge_t, idx: int) -> None


   .. py:method:: nodes_count() -> size_t


   .. py:method:: points_count() -> size_t


   .. py:method:: items_count(look_for_nodes: bool) -> size_t


.. py:class:: edge_segment_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: e
      :type:  edge_t


   .. py:attribute:: nseg
      :type:  int


   .. py:attribute:: x0
      :type:  int


   .. py:attribute:: x1
      :type:  int


   .. py:method:: length() -> size_t


   .. py:method:: toright() -> bool


.. py:data:: git_none

   nothing


.. py:data:: git_edge

   edge (graph_item_t::e, graph_item_t::n. n is farthest edge endpoint)


.. py:data:: git_node

   node title (graph_item_t::n)


.. py:data:: git_tool

   node title button (graph_item_t::n, graph_item_t::b)


.. py:data:: git_text

   node text (graph_item_t::n, graph_item_t::p)


.. py:data:: git_elp

   edge layout point (graph_item_t::elp)


.. py:class:: graph_item_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: type
      :type:  graph_item_type_t

      type



   .. py:attribute:: e
      :type:  edge_t

      edge source and destination



   .. py:attribute:: n
      :type:  int

      node number



   .. py:attribute:: b
      :type:  int

      button number



   .. py:attribute:: p
      :type:  point_t

      text coordinates in the node



   .. py:attribute:: elp
      :type:  edge_layout_point_t

      edge layout point



   .. py:method:: is_node() -> bool


   .. py:method:: is_edge() -> bool


.. py:class:: interval_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: x0
      :type:  int


   .. py:attribute:: x1
      :type:  int


   .. py:method:: empty() -> bool


   .. py:method:: intersect(r: interval_t) -> None


   .. py:method:: make_union(r: interval_t) -> None


   .. py:method:: move_by(shift: int) -> None


   .. py:method:: length() -> int


   .. py:method:: contains(x: int) -> bool


.. py:class:: row_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: nodes
      :type:  intvec_t

      list of nodes at the row



   .. py:attribute:: top
      :type:  int

      top y coord of the row



   .. py:attribute:: bottom
      :type:  int

      bottom y coord of the row



   .. py:method:: height() -> int


.. py:class:: drawable_graph_t

   Bases: :py:obj:`ida_gdl.gdl_graph_t`


   .. py:attribute:: thisown


   .. py:attribute:: title
      :type:  str

      graph title



   .. py:attribute:: rect_edges_made
      :type:  bool

      have create rectangular edges?



   .. py:attribute:: current_layout
      :type:  layout_type_t

      see Proximity view layouts



   .. py:attribute:: circle_center
      :type:  point_t

      for layout_circle



   .. py:attribute:: circle_radius
      :type:  int

      for layout_circle



   .. py:attribute:: callback_ud
      :type:  void *

      user data for callback



   .. py:method:: create_tree_layout() -> bool


   .. py:method:: create_circle_layout(p: point_t, radius: int) -> bool


   .. py:method:: set_callback(_callback: hook_cb_t *, _ud: void *) -> None


   .. py:method:: grcall(code: int) -> ssize_t


   .. py:method:: get_edge(e: edge_t) -> edge_info_t *


   .. py:method:: nrect(n: int) -> rect_t


.. py:data:: ygap

.. py:data:: xgap

.. py:data:: arrow_height

.. py:data:: arrow_width

.. py:class:: edge_infos_wrapper_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: clear() -> None


   .. py:attribute:: ptr
      :type:  edge_infos_t *


.. py:class:: interactive_graph_t(*args, **kwargs)

   Bases: :py:obj:`drawable_graph_t`


   .. py:attribute:: thisown


   .. py:attribute:: gid
      :type:  int

      graph id - unique for the database for flowcharts it is equal to the function start_ea 
              



   .. py:attribute:: belongs
      :type:  intvec_t

      the subgraph the node belongs to INT_MAX means that the node doesn't exist sign bit means collapsed node 
              



   .. py:attribute:: node_flags
      :type:  bytevec_t

      node flags



   .. py:attribute:: org_succs
      :type:  array_of_intvec_t


   .. py:attribute:: org_preds
      :type:  array_of_intvec_t


   .. py:attribute:: succs
      :type:  array_of_intvec_t


   .. py:attribute:: preds
      :type:  array_of_intvec_t


   .. py:attribute:: nodes
      :type:  interactive_graph_t::node_layout_t


   .. py:attribute:: edges
      :type:  edge_infos_wrapper_t


   .. py:method:: size() -> int

      Get the total number of nodes (including group nodes, and including hidden nodes.)
      See also node_qty()

      :returns: the total number of nodes in the graph



   .. py:method:: node_qty() -> int

      Get the number of visible nodes (the list can be retrieved using gdl.hpp's node_iterator)
      See also size()

      :returns: the number of visible nodes



   .. py:method:: empty() -> bool

      Is the graph (visually) empty? 
              
      :returns: true if there are no visible nodes



   .. py:method:: exists(node: int) -> bool

      Is the node visible?

      :param node: the node number
      :returns: success



   .. py:method:: get_node_representative(node: int) -> int

      Get the node that currently visually represents 'node'. This will find the "closest" parent group node that's visible, by attempting to walk up the group nodes that contain 'node', and will stop when it finds a node that is currently visible.
      See also get_group_node() 
              
      :param node: the node
      :returns: the node that represents 'node', or 'node' if it's not part of any group



   .. py:method:: get_node_group(node: int) -> int


   .. py:method:: set_node_group(node: int, group: int) -> None


   .. py:method:: is_deleted_node(node: int) -> bool


   .. py:method:: set_deleted_node(node: int) -> None


   .. py:method:: is_subgraph_node(node: int) -> bool


   .. py:method:: is_dot_node(node: int) -> bool


   .. py:method:: is_group_node(node: int) -> bool


   .. py:method:: is_displayable_node(node: int) -> bool


   .. py:method:: is_simple_node(node: int) -> bool


   .. py:method:: is_collapsed_node(node: int) -> bool


   .. py:method:: is_uncollapsed_node(node: int) -> bool


   .. py:method:: is_visible_node(node: int) -> bool

      Is the node currently visible?
      An invisible node is a node that's part of a group that's currently collapsed.

      :param node: the node
      :returns: success



   .. py:method:: get_first_subgraph_node(group: int) -> int


   .. py:method:: get_next_subgraph_node(group: int, current: int) -> int


   .. py:method:: create_group(nodes: intvec_t const &) -> int

      Create a new group node, that will contain all the nodes in 'nodes'.

      :param nodes: the nodes that will be part of the group
      :returns: the group node, or -1 in case of error



   .. py:method:: delete_group(group: int) -> bool

      Delete a group node.
      This deletes the group node only; it does not delete nodes that are part of the group.

      :param group: the group node
      :returns: success



   .. py:method:: change_group_visibility(group: int, expand: bool) -> bool

      Expand/collapse a group node

      :param group: the group node
      :param expand: whether to expand or collapse
      :returns: success



   .. py:method:: nsucc(b: int) -> int


   .. py:method:: npred(b: int) -> int


   .. py:method:: succ(b: int, i: int) -> int


   .. py:method:: pred(b: int, i: int) -> int


   .. py:method:: succset(b: int) -> intvec_t const &


   .. py:method:: predset(b: int) -> intvec_t const &


   .. py:method:: reset() -> None


   .. py:method:: redo_layout() -> bool

      Recompute the layout, according to the value of 'current_layout'.

      :returns: success



   .. py:method:: resize(n: int) -> None

      Resize the graph to 'n' nodes

      :param n: the new size



   .. py:method:: add_node(r: rect_t) -> int

      Add a node, possibly with a specific geometry

      :param r: the node geometry (can be nullptr)
      :returns: the new node



   .. py:method:: del_node(n: int) -> ssize_t

      Delete a node

      :param n: the node to delete
      :returns: the number of deleted edges



   .. py:method:: add_edge(i: int, j: int, ei: edge_info_t) -> bool


   .. py:method:: del_edge(i: int, j: int) -> bool


   .. py:method:: replace_edge(i: int, j: int, x: int, y: int) -> bool


   .. py:method:: refresh() -> bool

      Refresh the graph
      A graph needs refreshing when it's "backing data". E.g., if the number (or contents) of the objects in the above example, change.
      Let's say the user's plugin ends up finding a 5th piece of scattered data. It should then add it to its internal list of known objects, and tell IDA that the graph needs to be refreshed, using refresh_viewer(). This will cause IDA to:
      * discard all its internal rendering information,
      * call interactive_graph_t::refresh() on the graph so that the user's plugin has a chance to "sync" the number of nodes & edges that this graph contains, to the information that the plugin has collected so far
      * re-create internal rendering information, and
      * repaint the view



      :returns: success



   .. py:method:: set_nrect(n: int, r: rect_t) -> bool


   .. py:method:: set_edge(e: edge_t, ei: edge_info_t) -> bool


   .. py:method:: create_digraph_layout() -> bool


   .. py:method:: del_custom_layout() -> None


   .. py:method:: get_custom_layout() -> bool


   .. py:method:: set_custom_layout() -> None


   .. py:method:: get_graph_groups() -> bool


   .. py:method:: set_graph_groups() -> None


   .. py:method:: calc_group_ea(arg2: intvec_t const &) -> ida_idaapi.ea_t


   .. py:method:: is_user_graph() -> bool


.. py:data:: MTG_GROUP_NODE

   is group node?


.. py:data:: MTG_DOT_NODE

   is dot node?


.. py:data:: MTG_NON_DISPLAYABLE_NODE

   for disassembly graphs - non-displayable nodes have a visible area that is too large to generate disassembly lines for without IDA slowing down significantly (see MAX_VISIBLE_NODE_AREA) 
           


.. py:data:: COLLAPSED_NODE

.. py:class:: graph_visitor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: visit_node(arg2: int, arg3: rect_t) -> int


   .. py:method:: visit_edge(arg2: edge_t, arg3: edge_info_t) -> int


.. py:data:: grcode_calculating_layout

   calculating user-defined graph layout. 
             


.. py:data:: grcode_layout_calculated

   graph layout calculated. 
             


.. py:data:: grcode_changed_graph

   new graph has been set. 
             


.. py:data:: grcode_reserved

.. py:data:: grcode_clicked

   graph is being clicked. this callback allows you to ignore some clicks. it occurs too early, internal graph variables are not updated yet. current_item1, current_item2 point to the same thing. item2 has more information. see also: custom_viewer_click_t 
             


.. py:data:: grcode_dblclicked

   a graph node has been double clicked. 
             


.. py:data:: grcode_creating_group

   a group is being created. this provides an opportunity for the graph to forbid creation of the group. Note that groups management is done by the interactive_graph_t instance itself: there is no need to modify the graph in this callback. 
             


.. py:data:: grcode_deleting_group

   a group is being deleted. this provides an opportunity for the graph to forbid deletion of the group. Note that groups management is done by the interactive_graph_t instance itself: there is no need to modify the graph in this callback. 
             


.. py:data:: grcode_group_visibility

   a group is being collapsed/uncollapsed this provides an opportunity for the graph to forbid changing the visibility of the group. Note that groups management is done by the interactive_graph_t instance itself: there is no need to modify the graph in this callback. 
             


.. py:data:: grcode_gotfocus

   a graph viewer got focus. 
             


.. py:data:: grcode_lostfocus

   a graph viewer lost focus. 
             


.. py:data:: grcode_user_refresh

   refresh user-defined graph nodes and edges This is called when the UI considers that it is necessary to recreate the graph layout, and thus has to ensure that the 'interactive_graph_t' instance it is using, is up-to-date. For example:
   * at graph creation-time
   * if a refresh_viewer() call was made



.. py:data:: grcode_reserved2

.. py:data:: grcode_user_text

   retrieve text for user-defined graph node. NB: do not use anything calling GDI! 
             


.. py:data:: grcode_user_size

   calculate node size for user-defined graph. 
             


.. py:data:: grcode_user_title

   render node title of a user-defined graph. 
             


.. py:data:: grcode_user_draw

   render node of a user-defined graph. NB: draw only on the specified DC and nowhere else! 
             


.. py:data:: grcode_user_hint

   retrieve hint for the user-defined graph. 
             


.. py:data:: grcode_destroyed

   graph is being destroyed. Note that this doesn't mean the graph viewer is being destroyed; this only means that the graph that is being displayed by it is being destroyed, and that, e.g., any possibly cached data should be invalidated (this event can happen when, for example, the user decides to group nodes together: that operation will effectively create a new graph, that will replace the old one.) To be notified when the graph viewer itself is being destroyed, please see notification 'view_close', in kernwin.hpp 
             


.. py:data:: grcode_create_graph_viewer

   use create_graph_viewer()


.. py:data:: grcode_get_graph_viewer

   use get_graph_viewer()


.. py:data:: grcode_get_viewer_graph

   use get_viewer_graph()


.. py:data:: grcode_create_interactive_graph

   use create_interactive_graph()


.. py:data:: grcode_set_viewer_graph

   use set_viewer_graph()


.. py:data:: grcode_refresh_viewer

   use refresh_viewer()


.. py:data:: grcode_fit_window

   use viewer_fit_window()


.. py:data:: grcode_get_curnode

   use viewer_get_curnode()


.. py:data:: grcode_center_on

   use viewer_center_on()


.. py:data:: grcode_get_selection

   use viewer_get_selection()


.. py:data:: grcode_del_custom_layout

   use interactive_graph_t::del_custom_layout()


.. py:data:: grcode_set_custom_layout

   use interactive_graph_t::set_custom_layout()


.. py:data:: grcode_set_graph_groups

   use interactive_graph_t::set_graph_groups()


.. py:data:: grcode_clear

   use interactive_graph_t::clear()


.. py:data:: grcode_create_digraph_layout

   use interactive_graph_t::create_digraph_layout()


.. py:data:: grcode_create_tree_layout

   use drawable_graph_t::create_tree_layout()


.. py:data:: grcode_create_circle_layout

   use drawable_graph_t::create_circle_layout()


.. py:data:: grcode_get_node_representative

   use interactive_graph_t::get_node_representative()


.. py:data:: grcode_find_subgraph_node

   use interactive_graph_t::_find_subgraph_node()


.. py:data:: grcode_create_group

   use interactive_graph_t::create_group()


.. py:data:: grcode_get_custom_layout

   use interactive_graph_t::get_custom_layout()


.. py:data:: grcode_get_graph_groups

   use interactive_graph_t::get_graph_groups()


.. py:data:: grcode_empty

   use interactive_graph_t::empty()


.. py:data:: grcode_is_visible_node

   use interactive_graph_t::is_visible_node()


.. py:data:: grcode_delete_group

   use interactive_graph_t::delete_group()


.. py:data:: grcode_change_group_visibility

   use interactive_graph_t::change_group_visibility()


.. py:data:: grcode_set_edge

   use interactive_graph_t::set_edge()


.. py:data:: grcode_node_qty

   use interactive_graph_t::node_qty()


.. py:data:: grcode_nrect

   use interactive_graph_t::nrect()


.. py:data:: grcode_set_titlebar_height

   use viewer_set_titlebar_height()


.. py:data:: grcode_create_user_graph_place

   use create_user_graph_place()


.. py:data:: grcode_create_disasm_graph1

   use create_disasm_graph(ea_t ea)


.. py:data:: grcode_create_disasm_graph2

   use create_disasm_graph(const rangevec_t &ranges)


.. py:data:: grcode_set_node_info

   use viewer_set_node_info()


.. py:data:: grcode_get_node_info

   use viewer_get_node_info()


.. py:data:: grcode_del_node_info

   use viewer_del_node_info()


.. py:data:: grcode_viewer_create_groups

.. py:data:: grcode_viewer_delete_groups

.. py:data:: grcode_viewer_groups_visibility

.. py:data:: grcode_viewer_create_groups_vec

   use viewer_create_groups()


.. py:data:: grcode_viewer_delete_groups_vec

   use viewer_delete_groups()


.. py:data:: grcode_viewer_groups_visibility_vec

   use viewer_set_groups_visibility()


.. py:data:: grcode_delete_interactive_graph

   use delete_interactive_graph()


.. py:data:: grcode_edge_infos_wrapper_copy

   use edge_infos_wrapper_t::operator=()


.. py:data:: grcode_edge_infos_wrapper_clear

   use edge_infos_wrapper_t::clear()


.. py:data:: grcode_attach_menu_item

.. py:data:: grcode_set_gli

   use viewer_set_gli()


.. py:data:: grcode_get_gli

   use viewer_get_gli()


.. py:class:: group_crinfo_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: nodes
      :type:  intvec_t


   .. py:attribute:: text
      :type:  str


.. py:function:: create_graph_viewer(title: str, id: int, callback: hook_cb_t *, ud: void *, title_height: int, parent: TWidget * = None) -> graph_viewer_t *

   Create a custom graph viewer. 
           
   :param title: the widget title
   :param id: graph id
   :param callback: callback to handle graph notifications (graph_notification_t)
   :param ud: user data passed to callback
   :param title_height: node title height
   :param parent: the parent widget of the graph viewer
   :returns: new viewer


.. py:function:: get_graph_viewer(parent: TWidget *) -> graph_viewer_t *

   Get custom graph viewer for given form.


.. py:function:: create_interactive_graph(id: int) -> interactive_graph_t *

   Create a new empty graph with given id.


.. py:function:: create_disasm_graph(*args) -> interactive_graph_t *

   This function has the following signatures:

       0. create_disasm_graph(ea: ida_idaapi.ea_t) -> interactive_graph_t *
       1. create_disasm_graph(ranges: const rangevec_t &) -> interactive_graph_t *

   # 0: create_disasm_graph(ea: ida_idaapi.ea_t) -> interactive_graph_t *

   Create a graph for the function that contains 'ea'.


   # 1: create_disasm_graph(ranges: const rangevec_t &) -> interactive_graph_t *

   Create a graph using an arbitrary set of ranges.


.. py:function:: get_viewer_graph(gv: graph_viewer_t *) -> interactive_graph_t *

   Get graph object for given custom graph viewer.


.. py:function:: set_viewer_graph(gv: graph_viewer_t *, g: interactive_graph_t) -> None

   Set the underlying graph object for the given viewer.


.. py:function:: refresh_viewer(gv: graph_viewer_t *) -> None

   Redraw the graph in the given view.


.. py:function:: viewer_fit_window(gv: graph_viewer_t *) -> None

   Fit graph viewer to its parent form.


.. py:function:: viewer_get_curnode(gv: graph_viewer_t *) -> int

   Get number of currently selected node (-1 if none)


.. py:function:: viewer_center_on(gv: graph_viewer_t *, node: int) -> None

   Center the graph view on the given node.


.. py:function:: viewer_set_gli(gv: graph_viewer_t *, gli: graph_location_info_t const *, flags: int = 0) -> None

   Set location info for given graph view If flags contains GLICTL_CENTER, then the gli will be set to be the center of the view. Otherwise it will be the top-left. 
           


.. py:function:: viewer_get_gli(out: graph_location_info_t *, gv: graph_viewer_t *, flags: int = 0) -> bool

   Get location info for given graph view If flags contains GLICTL_CENTER, then the gli that will be retrieved, will be the one at the center of the view. Otherwise it will be the top-left. 
           


.. py:function:: viewer_set_node_info(gv: graph_viewer_t *, n: int, ni: node_info_t, flags: int) -> None

   Set node info for node in given viewer (see set_node_info())


.. py:function:: viewer_get_node_info(gv: graph_viewer_t *, out: node_info_t, n: int) -> bool

   Get node info for node in given viewer (see get_node_info())


.. py:function:: viewer_del_node_info(gv: graph_viewer_t *, n: int) -> None

   Delete node info for node in given viewer (see del_node_info())


.. py:function:: viewer_create_groups(gv: graph_viewer_t *, out_group_nodes: intvec_t *, gi: groups_crinfos_t const &) -> bool

   This will perform an operation similar to what happens when a user manually selects a set of nodes, right-clicks and selects "Create group". This is a wrapper around interactive_graph_t::create_group that will, in essence:
   * clone the current graph
   * for each group_crinfo_t, attempt creating group in that new graph
   * if all were successful, animate to that new graph.



.. py:function:: viewer_delete_groups(gv: graph_viewer_t *, groups: intvec_t const &, new_current: int = -1) -> bool

   Wrapper around interactive_graph_t::delete_group. This function will:
   * clone the current graph
   * attempt deleting the groups in that new graph
   * if successful, animate to that new graph. 


           


.. py:function:: viewer_set_groups_visibility(gv: graph_viewer_t *, groups: intvec_t const &, expand: bool, new_current: int = -1) -> bool

   Wrapper around interactive_graph_t::change_visibility. This function will:
   * clone the current graph
   * attempt changing visibility of the groups in that new graph
   * if successful, animate to that new graph. 


           


.. py:function:: viewer_attach_menu_item(g: graph_viewer_t *, name: str) -> bool

   Attach a previously-registered action to the view's context menu. See kernwin.hpp for how to register actions. 
           
   :param g: graph viewer
   :param name: action name
   :returns: success


.. py:function:: viewer_get_selection(gv: graph_viewer_t *, sgs: screen_graph_selection_t) -> bool

   Get currently selected items for graph viewer.


.. py:function:: viewer_set_titlebar_height(gv: graph_viewer_t *, height: int) -> int

   Set height of node title bars (grcode_set_titlebar_height)


.. py:function:: delete_interactive_graph(g: interactive_graph_t) -> None

   Delete graph object. 
           


.. py:class:: user_graph_place_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: node
      :type:  int


.. py:function:: create_user_graph_place(node: int, lnnum: int) -> user_graph_place_t *

   Get a copy of a user_graph_place_t (returns a pointer to static storage)


.. py:function:: pyg_close(_self: PyObject *) -> None

.. py:function:: pyg_select_node(_self: PyObject *, nid: int) -> None

.. py:function:: pyg_show(_self: PyObject *) -> bool

.. py:data:: edge_t

.. py:data:: node_ordering_t

.. py:data:: abstract_graph_t

.. py:data:: mutable_graph_t

.. py:data:: create_mutable_graph

.. py:data:: delete_mutable_graph

.. py:data:: grcode_create_mutable_graph

.. py:data:: grcode_create_mutable_graph

.. py:class:: GraphViewer(title, close_open=False)

   Bases: :py:obj:`ida_kernwin.CustomIDAMemo`


   .. py:class:: UI_Hooks_Trampoline(v)

      Bases: :py:obj:`ida_kernwin.UI_Hooks`


      .. py:attribute:: v


      .. py:method:: populating_widget_popup(w, popup_handle)

         IDA is populating the context menu for a widget. This is your chance to attach_action_to_popup().
         Have a look at ui_finish_populating_widget_popup, if you want to augment the context menu with your own actions after the menu has had a chance to be properly populated by the owning component or plugin (which typically does it on ui_populating_widget_popup.)

         :param widget: (TWidget *)
         :param popup_handle: (TPopupMenu *)
         :param ctx: (const action_activation_ctx_t *)
         :returns: void




   .. py:attribute:: ui_hooks_trampoline


   .. py:method:: AddNode(obj)

      Creates a node associated with the given object and returns the node id



   .. py:method:: AddEdge(src_node, dest_node)

      Creates an edge between two given node ids



   .. py:method:: Clear()

      Clears all the nodes and edges



   .. py:method:: Count()

      Returns the node count



   .. py:method:: Close()

      Closes the graph.
      It is possible to call Show() again (which will recreate the graph)



   .. py:method:: Show()

      Shows an existing graph or creates a new one

      :returns: Boolean



   .. py:method:: Select(node_id)

      Selects a node on the graph



   .. py:method:: OnRefresh()

      Event called when the graph is refreshed or first created.
      From this event you are supposed to create nodes and edges.
      This callback is mandatory.

      NOTE: ***It is important to clear previous nodes before adding nodes.***

      :returns: Returning True tells the graph viewer to use the items. Otherwise old items will be used.



   .. py:method:: AddCommand(title, shortcut)


   .. py:method:: OnPopup(widget, popup_handle)


   .. py:method:: OnCommand(cmd_id)



# ida_graph

Graph view management - custom graph visualization and interaction (medium priority for typical reverse engineering).

## Key Classes

### GraphViewer
Pythonic class for creating custom graph views.
- Override `OnRefresh()` - Populate graph nodes/edges
- Override `OnGetText(node)` - Get node display text
- Override `OnDblClick(node)` - Handle double-click
- Override `OnClick(node)` - Handle single-click
- `Show()` - Display graph viewer
- `Close()` - Close graph viewer

### interactive_graph_t
Low-level interactive graph implementation (use GraphViewer instead for Python).

### mutable_graph_t
Abstract graph structure for manipulation.
- `create_mutable_graph()` - Create new graph
- `delete_mutable_graph(g)` - Delete graph

## Key Functions

### Graph Creation
- `create_graph_viewer(title, gid, callback)` - Create graph viewer widget
- `create_interactive_graph(title)` - Create interactive graph
- `create_disasm_graph(ea)` - Create disassembly graph at address

### Graph Manipulation
- `get_node_info(graph, node)` - Get node display info (color, text, etc.)
- `set_node_info(graph, node, info, flags)` - Set node properties
- `del_node_info(graph, node)` - Delete node info
- `viewer_set_node_info(viewer, node, info, flags)` - Set node info in viewer

### Graph Navigation
- `viewer_get_curnode(viewer)` - Get currently selected node
- `viewer_center_on(viewer, node)` - Center view on node
- `viewer_fit_window(viewer)` - Zoom to fit
- `viewer_get_selection(viewer)` - Get selected items

### Graph Groups
- `viewer_create_groups(viewer, groups)` - Create node groups
- `viewer_delete_groups(viewer, groups)` - Delete groups
- `viewer_set_groups_visibility(viewer, groups, visible)` - Show/hide groups

## Constants

**Node info flags**: NIF_BG_COLOR, NIF_FRAME_COLOR, NIF_EA, NIF_TEXT, NIF_FLAGS, NIF_ALL

**Layout types**: layout_digraph, layout_tree, layout_circle, layout_polar_tree, layout_orthogonal, layout_radial_tree

**Graph item types**: git_none, git_edge, git_node, git_tool, git_text

## See Also
Full docs: skill/docs/ida_graph.rst

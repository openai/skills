# ida_moves

Navigation history, bookmarks, and location tracking in IDA views.

## Key Classes

### lochist_entry_t
Location history entry combining place and renderer info.
- `rinfo` - Renderer information (renderer_info_t)
- `plce` - Place pointer (place_t*)
- `place()` / `set_place(p)` - Get/set place
- `is_valid()` - Check if entry is valid
- `renderer_info()` - Get renderer info reference

### navstack_entry_t
Navigation stack entry extending lochist_entry_t.
- `widget_id` - Widget identifier
- `ud_str` - User-defined string
- Inherits all lochist_entry_t members

### navstack_t
Navigation history stack (back/forward navigation).
- `init(defpos, stream_name, flags)` - Initialize stack
- `set_current(e, in_charge)` / `get_current(out, widget_id)` - Set/get current position
- `stack_jump(try_to_unhide, e)` - Jump to entry
- `stack_back(out, cnt, try_to_unhide)` / `stack_forward(out, cnt, try_to_unhide)` - Navigate backward/forward
- `stack_nav(out, forward, cnt, try_to_unhide)` - Generic navigation
- `stack_index()` / `stack_size()` - Get current index/size
- `stack_clear(new_tip)` - Clear stack with new tip
- `get_stack_entry(out, index)` / `set_stack_entry(index, e)` - Get/set entry at index
- `is_history_enabled()` - Check if history is enabled

### bookmarks_t
Bookmark management (static methods).
- `mark(e, index, title, desc, ud)` - Create/update bookmark
- `get(out, index, ud)` - Get bookmark entry
- `get_desc(e, index, ud)` - Get bookmark description
- `find_index(e, ud)` - Find bookmark index
- `size(e, ud)` - Get bookmark count
- `erase(e, index, ud)` - Delete bookmark
- `get_dirtree_id(e, ud)` - Get dirtree ID for bookmark

### renderer_info_t
View renderer state (graph position, zoom, cursor).
- `rtype` - Renderer type (tcc_renderer_type_t)
- `gli` - Graph location info (graph_location_info_t)
- `pos` - Position info (renderer_info_pos_t)

### graph_location_info_t
Graph view location and zoom state.
- `zoom` - Zoom level
- `orgx` / `orgy` - Origin coordinates

### segm_move_info_t / segm_move_infos_t
Segment relocation tracking (for when segments move).
- `to` - Target address
- `size` - Size moved
- `find(ea)` - Find move info for address

## Constants

### Location State Flags (LSEF_*)
- `LSEF_PLACE` - Place component
- `LSEF_RINFO` - Renderer info component
- `LSEF_PTYPE` - Place type component
- `LSEF_ALL` - All components

### Unhide Flags (UNHID_*)
- `UNHID_SEGM` - Unhid segment at target
- `UNHID_FUNC` - Unhid function at target
- `UNHID_RANGE` - Unhid range at target

### Other Constants
- `MAX_MARK_SLOT` - Maximum bookmark slot number
- `LHF_HISTORY_DISABLED` - History disabled flag
- `DEFAULT_CURSOR_Y` / `DEFAULT_LNNUM` - Default cursor position

## See Also
Full docs: skill/docs/ida_moves.rst

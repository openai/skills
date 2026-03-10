# ida_kernwin

Interface between kernel and UI - dialogs, menus, choosers, custom viewers, and UI utilities.

## Key Functions

### User Interaction
- `msg(fmt, ...)` - print to output window
- `warning(fmt, ...)` / `error(fmt, ...)` - show warning/error dialog
- `ask_yn(defval, fmt, ...)` - yes/no question
- `ask_str(defval, hist, fmt, ...)` - string input
- `ask_long(defval, fmt, ...)` - integer input
- `ask_addr(defval, fmt, ...)` - address input
- `ask_file(forsave, defval, fmt, ...)` - file chooser

### Navigation
- `jumpto(ea, opnum=-1, uijmp_flags=0)` - jump to address
- `get_screen_ea()` - current cursor address
- `read_selection()` - get selected address range
- `choose_func(title)` - let user choose a function
- `choose_name(ea, title)` - let user choose a name

### UI Elements
- `find_widget(title)` - find widget by title
- `activate_widget(widget, take_focus)` - activate widget
- `close_widget(widget, flags)` - close widget
- `open_*_window(ea)` - open disasm/hex/exports/imports/etc window

### Actions
- `register_action(desc)` - register menu action
- `unregister_action(name)` - unregister action
- `attach_action_to_menu(path, name, flags)` - add action to menu
- `attach_action_to_toolbar(toolbar, name)` - add to toolbar
- `update_action_*()` - update action state/label/icon/etc

### Choosers (Lists)
- `Choose` class - create custom list windows
- `choose_refresh()` - refresh chooser
- `get_chooser_obj(title)` - get chooser Python object

### Custom Viewers
- `create_empty_widget(title)` - empty widget
- `create_code_viewer(widget, custviewer, flags)` - code viewer
- `simplecustviewer_t` - simple text viewer

### Misc
- `execute_sync(func, reqf)` - execute in UI thread
- `refresh_idaview()` / `refresh_idaview_anyway()` - refresh disassembly
- `beep(type)` - system beep
- `get_highlight(viewer)` - get highlighted identifier
- `set_highlight(viewer, text, flags)` - set highlight

## Widget Types (BWN_*)
DISASM, HEXVIEW, OUTPUT, FUNCS, NAMES, STRINGS, SEGS, IMPORTS, EXPORTS, PSEUDOCODE, etc.

## See Also
Full docs: skill/docs/ida_kernwin.rst

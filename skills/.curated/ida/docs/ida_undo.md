# ida_undo

Database undo/redo operations for IDA changes.

## Key Functions

### create_undo_point(bytes, size)
Create restore point. User can undo to this point later. Returns False if undo disabled.

### perform_undo()
Undo last action. Returns True on success.

### perform_redo()
Redo previously undone action. Returns True on success.

### get_undo_action_label()
Get description of action that will be undone (for UI display).

### get_redo_action_label()
Get description of action that will be redone (for UI display).

## Usage

Rarely needed in plugins - IDA automatically creates undo points for most operations. Use `create_undo_point()` only for custom atomic operations requiring explicit undo boundaries.

## See Also
Full docs: skill/docs/ida_undo.rst

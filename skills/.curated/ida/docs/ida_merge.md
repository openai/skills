# ida_merge

IDA Teams merge functionality - 3-way merging of IDB files (not available in IDA Pro).

## Overview

Low-priority module for IDA Teams only. Handles merging of base_idb, local_idb, and remote_idb databases with conflict resolution.

## Key Concepts

- **base_idb**: Common ancestor database (middle pane in UI)
- **local_idb**: Local database receiving merge result (left pane)
- **remote_idb**: Remote database merging into local (right pane)

## Merge Phases
Merges occur in phases: global settings, segmentation, bytes, names, functions, types, debugger settings, etc.

## Key Functions

- `is_diff_merge_mode()` - Check if in merge/diff mode
- `create_nodeval_merge_handler()` / `create_nodeval_merge_handlers()` - Create merge handlers for custom data
- `destroy_moddata_merge_handlers()` - Destroy module data merge handlers
- `get_ea_diffpos_name()` - Get name of EA difference position

## Key Classes

### merge_data_t
Merge operation data container.

### merge_handler_params_t
Parameters for creating merge handlers.

### merge_node_helper_t / merge_node_info_t
Helpers for merging netnode data.

## Merge Kinds (MERGE_KIND_*)
Extensive list including: NETNODE, INF, SEGMENTS, FUNC, FRAME, EXPORTS, IMPORTS, ENUMS, STRUCTS, TILS, TINFO, BYTEVAL, FLAGS, CREFS, DREFS, BPTS, DEBUGGER, etc.

## See Also
Full docs: skill/docs/ida_merge.rst

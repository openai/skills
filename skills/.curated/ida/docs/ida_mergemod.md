# ida_mergemod

Helper functions for plugin/processor module merging in IDA Teams (not available in IDA Pro).

## Overview

Low-priority module for plugin/processor developers needing to merge custom module data. Used in response to `ev_create_merge_handlers` event.

## Key Function

- `create_std_modmerge_handlers(mhp, helper, merge_node_info=None)` - Create standard merge handlers for module data

## Merge Sources Supported
1. Data fields inside moddata (plugmod_t/procmod_t)
2. Values in module netnode
3. Values in arbitrary netnodes
4. Data fields in auxiliary structures
5. Indexed arrays in netnodes

## See Also
Full docs: skill/docs/ida_mergemod.rst
Examples: plugins/mex1, plugins/mex2, plugins/mex3, plugins/ex_merge_ldrdata

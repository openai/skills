# ida_segment

Segment management (memory regions with addressing modes, permissions, and types).

## Key Classes

### segment_t
Core segment structure (inherits from range_t).

**Address Range:**
- `start_ea` - Start address (included)
- `end_ea` - End address (excluded)

**Addressing:**
- `bitness` - 0=16-bit, 1=32-bit, 2=64-bit
- `is_16bit()`, `is_32bit()`, `is_64bit()` - Check addressing mode
- `abits()`, `abytes()` - Get address bits/bytes
- `set_segm_addressing(s, bitness)` - Change addressing (deletes instructions/data)

**Attributes:**
- `sel` - Segment selector (must be unique)
- `type` - Segment type (SEG_CODE/SEG_DATA/SEG_BSS/SEG_XTRN/etc)
- `perm` - Permissions (SEGPERM_READ/WRITE/EXEC)
- `align` - Alignment (saRelByte/saRelWord/saRelPara/etc)
- `comb` - Combination (scPriv/scPub/scStack/scCommon)
- `color` - Segment color
- `defsr[16]` - Default segment register values

**Methods:**
- `update()` - Commit segment changes to database

## Key Functions

### Segment Lookup
- `get_segm_qty()` - Get number of segments
- `getseg(ea)` - Get segment containing address
- `getnseg(n)` - Get segment by index (0..qty-1)
- `get_segm_num(ea)` - Get segment index by address
- `get_segm_by_name(name)` - Get segment by name
- `get_segm_by_sel(selector)` - Get segment by selector
- `get_first_seg()`, `get_last_seg()` - Get first/last segment
- `get_next_seg(ea)`, `get_prev_seg(ea)` - Get adjacent segments

### Creating/Deleting
- `add_segm(para, start, end, name, sclass, flags=0)` - Add segment (allocates selector)
- `add_segm_ex(s, name, sclass, flags)` - Add segment (selector pre-allocated)
- `del_segm(ea, flags)` - Delete segment

### Modifying Bounds
- `set_segm_start(ea, newstart, flags)` - Change start (trims previous)
- `set_segm_end(ea, newend, flags)` - Change end (trims next)
- `move_segm_start(ea, newstart, mode)` - Change start (may expand previous)
- `move_segm(s, to, flags=0)` - Move entire segment (fixes relocations)
- `rebase_program(delta, flags)` - Rebase all segments

### Properties
- `get_segm_name(s, flags=0)` - Get name
- `set_segm_name(s, name, flags=0)` - Set name
- `get_segm_class(s)`, `set_segm_class(s, sclass, flags=0)` - Get/set class
- `get_segment_cmt(s, repeatable)`, `set_segment_cmt(s, cmt, repeatable)` - Get/set comment
- `segtype(ea)` - Get segment type at address
- `get_segm_base(s)` - Get base linear address
- `get_segm_para(s)` - Get base paragraph
- `set_segm_base(s, newbase)` - Set base (internal)

### Selectors
- `setup_selector(segbase)` - Allocate selector if needed
- `allocate_selector(segbase)` - Unconditionally allocate selector
- `find_free_selector()` - Find unused selector (>=1)
- `set_selector(selector, paragraph)` - Map selector to paragraph
- `del_selector(selector)` - Delete selector mapping
- `sel2para(selector)`, `sel2ea(selector)` - Get selector mapping
- `find_selector(base)` - Find selector by paragraph

### Visibility/Locking
- `is_visible_segm(s)`, `set_visible_segm(s, visible)` - Hide/show segment
- `is_spec_segm(seg_type)`, `is_spec_ea(ea)` - Check special types
- `lock_segm(segm, lock)`, `is_segm_locked(segm)` - Lock pointer (prevents deletion/move)

### Debugger Integration
- `change_segment_status(s, is_deb_segm)` - Convert debugger/regular segment
- `take_memory_snapshot(type)` - Snapshot running process (SNAP_ALL_SEG/SNAP_LOAD_SEG/SNAP_CUR_SEG)
- `is_miniidb()` - Check if IDB is debugger-created

### Segment Groups (OMF)
- `set_group_selector(grp, sel)` - Create segment group
- `get_group_selector(grpsel)` - Get group's common selector

### Segment Translations
- `add_segment_translation(segstart, mappedseg)` - Add overlay mapping
- `del_segment_translations(segstart)` - Delete translation list
- `get_segment_translations(transmap, segstart)` - Get translation list
- `set_segment_translations(segstart, transmap)` - Set translation list

## Segment Types

- `SEG_NORM` - Normal segment (no assumptions)
- `SEG_CODE` - Code segment
- `SEG_DATA` - Data segment
- `SEG_BSS` - Uninitialized data
- `SEG_XTRN` - External definitions (no instructions)
- `SEG_GRP` - Segment group
- `SEG_NULL` - Zero-length segment
- `SEG_ABSSYM` - Absolute symbols
- `SEG_COMM` - Communal definitions
- `SEG_IMEM` - Internal processor memory/SFRs

## Add Segment Flags

- `ADDSEG_NOSREG` - Set default sregs to BADSEL
- `ADDSEG_OR_DIE` - qexit() on failure
- `ADDSEG_NOTRUNC` - Destroy/truncate old segments instead
- `ADDSEG_QUIET` - Silent mode
- `ADDSEG_FILLGAP` - Fill gap with previous segment
- `ADDSEG_SPARSE` - Use sparse storage
- `ADDSEG_NOAA` - Don't mark for auto-analysis
- `ADDSEG_IDBENC` - Name/class in IDB encoding

## Segment Modification Flags

- `SEGMOD_KILL` - Disable addresses when shrinking
- `SEGMOD_KEEP` - Keep code/data
- `SEGMOD_SILENT` - Silent mode
- `SEGMOD_KEEPSEL` - Don't delete unused selector
- `SEGMOD_NOMOVE` - Don't move info when changing start
- `SEGMOD_SPARSE` - Use sparse storage when extending

## See Also
Full docs: skill/docs/ida_segment.rst

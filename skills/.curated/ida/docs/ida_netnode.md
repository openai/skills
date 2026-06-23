# ida_netnode

Low-priority: Low-level database storage using B-tree structures. Most reverse engineering tasks use higher-level abstractions instead.

## Key Classes/Functions

### netnode
Persistent storage object in IDA database. Each netnode has unique ID and may have name, value, and multiple sparse arrays.

- `exist(name)` - check if named netnode exists
- `create()` - create new netnode
- `kill()` - delete netnode
- `get_name()` - retrieve netnode name
- `rename(newname)` - change netnode name
- `altval(idx, tag)` - read 32-bit value from altvals array
- `altset(idx, val, tag)` - write 32-bit value to altvals array
- `supval(idx, tag)` - read arbitrary-sized object from supvals array
- `supset(idx, value, tag)` - write arbitrary-sized object to supvals array
- `hashval(key, tag)` - read value from hash by string key
- `hashset(key, value, tag)` - write value to hash by string key
- `getblob(start, tag)` - read large object spanning multiple indexes
- `setblob(buf, start, tag)` - write large object

Arrays use tags to organize data: 'A' for altvals, 'S' for supvals, 'H' for hashvals.

## See Also
Full docs: skill/docs/ida_netnode.rst

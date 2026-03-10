ida_netnode
===========

.. py:module:: ida_netnode

.. autoapi-nested-parse::

   Functions that provide the lowest level public interface to the database. Namely, we use Btree. To learn more about BTree:

   [https://en.wikipedia.org/wiki/B-tree](https://en.wikipedia.org/wiki/B-tree)
   We do not use Btree directly. Instead, we have another layer built on the top of Btree. Here is a brief explanation of this layer.
   An object called "netnode" is modeled on the top of Btree. Each netnode has a unique id: a 32-bit value (64-bit for ida64). Initially there is a trivial mapping of the linear addresses used in the program to netnodes (later this mapping may be modified using ea2node and node2ea functions; this is used for fast database rebasings). If we have additional information about an address (for example, a comment is attached to it), this information is stored in the corresponding netnode. See nalt.hpp to see how the kernel uses netnodes. Also, some netnodes have no corresponding linear address (however, they still have an id). They are used to store information not related to a particular address.
   Each netnode _may_ have the following attributes:

   * a name: an arbitrary non-empty string, up to 255KB-1 bytes
   * a value: arbitrary sized object, max size is MAXSPECSIZE
   * altvals: a sparse array of 32-bit values. indexes in this array may be 8-bit or 32-bit values
   * supvals: an array of arbitrary sized objects. (size of each object is limited by MAXSPECSIZE) indexes in this array may be 8-bit or 32-bit values
   * charvals: a sparse array of 8-bit values. indexes in this array may be 8-bit or 32-bit values
   * hashvals: a hash (an associative array). indexes in this array are strings values are arbitrary sized (max size is MAXSPECSIZE)


   Initially a new netnode contains no information at all so no disk space is used for it. As you add new information, the netnode grows.
   All arrays that are attached to the netnode behave in the same manner. Initially:
   * all members of altvals/charvals array are zeroes
   * all members of supvals/hashvals array are undefined


   If you need to store objects bigger that MAXSPECSIZE, please note that there are high-level functions to store arbitrary sized objects in supvals. See setblob/getblob and other blob-related functions.
   You may use netnodes to store additional information about the program. Limitations on the use of netnodes are the following:

   * use netnodes only if you could not find a kernel service to store your type of information
   * do not create netnodes with valid identifier names. Use the "$ " prefix (or any other prefix with characters not allowed in the identifiers for the names of your netnodes. Although you will probably not destroy anything by accident, using already defined names for the names of your netnodes is still discouraged.
   * you may create as many netnodes as you want (creation of an unnamed netnode does not increase the size of the database). however, since each netnode has a number, creating too many netnodes could lead to the exhaustion of the netnode numbers (the numbering starts at 0xFF000000)
   * remember that netnodes are automatically saved to the disk by the kernel.


   Advanced info:
   In fact a netnode may contain up to 256 arrays of arbitrary sized objects (not only the 4 listed above). Each array has an 8-bit tag. Usually tags are represented by character constants. For example, altvals and supvals are simply 2 of 256 arrays, with the tags 'A' and 'S' respectively. 
       



Attributes
----------

.. autoapisummary::

   ida_netnode.BADNODE
   ida_netnode.SIZEOF_nodeidx_t
   ida_netnode.cvar
   ida_netnode.MAXNAMESIZE
   ida_netnode.MAX_NODENAME_SIZE
   ida_netnode.MAXSPECSIZE
   ida_netnode.atag
   ida_netnode.stag
   ida_netnode.htag
   ida_netnode.vtag
   ida_netnode.ntag
   ida_netnode.ltag
   ida_netnode.NETMAP_IDX
   ida_netnode.NETMAP_VAL
   ida_netnode.NETMAP_STR
   ida_netnode.NETMAP_X8
   ida_netnode.NETMAP_V8
   ida_netnode.NETMAP_VAL_NDX
   ida_netnode.netnode_exist


Classes
-------

.. autoapisummary::

   ida_netnode.netnode


Functions
---------

.. autoapisummary::

   ida_netnode.exist


Module Contents
---------------

.. py:data:: BADNODE

   A number to represent a bad netnode reference.


.. py:data:: SIZEOF_nodeidx_t

.. py:class:: netnode(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: exist(_name: str) -> bool
      :staticmethod:


      Does the netnode with the specified name exist?



   .. py:method:: create(*args) -> bool


   .. py:method:: kill() -> None


   .. py:method:: get_name() -> ssize_t


   .. py:method:: rename(newname: str, namlen: size_t = 0) -> bool


   .. py:method:: valobj(*args) -> ssize_t


   .. py:method:: valstr() -> ssize_t


   .. py:method:: set(value: void const *) -> bool


   .. py:method:: delvalue() -> bool


   .. py:method:: set_long(x: nodeidx_t) -> bool


   .. py:method:: value_exists() -> bool


   .. py:method:: long_value() -> nodeidx_t


   .. py:method:: altval(*args) -> nodeidx_t


   .. py:method:: altval_ea(*args) -> nodeidx_t


   .. py:method:: altset(*args) -> bool


   .. py:method:: altset_ea(*args) -> bool


   .. py:method:: altdel_ea(*args) -> bool


   .. py:method:: easet(ea: ida_idaapi.ea_t, addr: ida_idaapi.ea_t, tag: uchar) -> bool


   .. py:method:: eaget(ea: ida_idaapi.ea_t, tag: uchar) -> ida_idaapi.ea_t


   .. py:method:: eadel(ea: ida_idaapi.ea_t, tag: uchar) -> bool


   .. py:method:: easet_idx(idx: nodeidx_t, addr: ida_idaapi.ea_t, tag: uchar) -> bool


   .. py:method:: eaget_idx(idx: nodeidx_t, tag: uchar) -> ida_idaapi.ea_t


   .. py:method:: easet_idx8(idx: uchar, addr: ida_idaapi.ea_t, tag: uchar) -> bool


   .. py:method:: eaget_idx8(idx: uchar, tag: uchar) -> ida_idaapi.ea_t


   .. py:method:: eadel_idx8(idx: uchar, tag: uchar) -> bool


   .. py:method:: altfirst(*args) -> nodeidx_t


   .. py:method:: altnext(*args) -> nodeidx_t


   .. py:method:: altlast(*args) -> nodeidx_t


   .. py:method:: altprev(*args) -> nodeidx_t


   .. py:method:: altshift(*args) -> size_t


   .. py:method:: charval(alt: nodeidx_t, tag: uchar) -> uchar


   .. py:method:: charset(alt: nodeidx_t, val: uchar, tag: uchar) -> bool


   .. py:method:: chardel(alt: nodeidx_t, tag: uchar) -> bool


   .. py:method:: charval_ea(ea: ida_idaapi.ea_t, tag: uchar) -> uchar


   .. py:method:: charset_ea(ea: ida_idaapi.ea_t, val: uchar, tag: uchar) -> bool


   .. py:method:: chardel_ea(ea: ida_idaapi.ea_t, tag: uchar) -> bool


   .. py:method:: charfirst(tag: uchar) -> nodeidx_t


   .. py:method:: charnext(cur: nodeidx_t, tag: uchar) -> nodeidx_t


   .. py:method:: charlast(tag: uchar) -> nodeidx_t


   .. py:method:: charprev(cur: nodeidx_t, tag: uchar) -> nodeidx_t


   .. py:method:: charshift(_from: nodeidx_t, to: nodeidx_t, size: nodeidx_t, tag: uchar) -> size_t


   .. py:method:: altval_idx8(alt: uchar, tag: uchar) -> nodeidx_t


   .. py:method:: altset_idx8(alt: uchar, val: nodeidx_t, tag: uchar) -> bool


   .. py:method:: altdel_idx8(alt: uchar, tag: uchar) -> bool


   .. py:method:: altfirst_idx8(tag: uchar) -> nodeidx_t


   .. py:method:: altnext_idx8(cur: uchar, tag: uchar) -> nodeidx_t


   .. py:method:: altlast_idx8(tag: uchar) -> nodeidx_t


   .. py:method:: altprev_idx8(cur: uchar, tag: uchar) -> nodeidx_t


   .. py:method:: charval_idx8(alt: uchar, tag: uchar) -> uchar


   .. py:method:: charset_idx8(alt: uchar, val: uchar, tag: uchar) -> bool


   .. py:method:: chardel_idx8(alt: uchar, tag: uchar) -> bool


   .. py:method:: charfirst_idx8(tag: uchar) -> nodeidx_t


   .. py:method:: charnext_idx8(cur: uchar, tag: uchar) -> nodeidx_t


   .. py:method:: charlast_idx8(tag: uchar) -> nodeidx_t


   .. py:method:: charprev_idx8(cur: uchar, tag: uchar) -> nodeidx_t


   .. py:method:: altdel(*args) -> bool


   .. py:method:: altdel_all(*args) -> bool


   .. py:method:: supval(*args) -> ssize_t


   .. py:method:: supval_ea(*args) -> ssize_t


   .. py:method:: supstr(*args) -> ssize_t


   .. py:method:: supstr_ea(*args) -> ssize_t


   .. py:method:: supdel_ea(*args) -> bool


   .. py:method:: lower_bound(*args) -> nodeidx_t


   .. py:method:: lower_bound_ea(*args) -> nodeidx_t


   .. py:method:: supfirst(*args) -> nodeidx_t


   .. py:method:: supnext(*args) -> nodeidx_t


   .. py:method:: suplast(*args) -> nodeidx_t


   .. py:method:: supprev(*args) -> nodeidx_t


   .. py:method:: supshift(*args) -> size_t


   .. py:method:: supval_idx8(*args) -> ssize_t


   .. py:method:: supstr_idx8(alt: uchar, tag: uchar) -> ssize_t


   .. py:method:: supset_idx8(alt: uchar, value: void const *, tag: uchar) -> bool


   .. py:method:: supdel_idx8(alt: uchar, tag: uchar) -> bool


   .. py:method:: lower_bound_idx8(alt: uchar, tag: uchar) -> nodeidx_t


   .. py:method:: supfirst_idx8(tag: uchar) -> nodeidx_t


   .. py:method:: supnext_idx8(alt: uchar, tag: uchar) -> nodeidx_t


   .. py:method:: suplast_idx8(tag: uchar) -> nodeidx_t


   .. py:method:: supprev_idx8(alt: uchar, tag: uchar) -> nodeidx_t


   .. py:method:: supdel(*args) -> bool


   .. py:method:: supdel_all(tag: uchar) -> bool


   .. py:method:: supdel_range(idx1: nodeidx_t, idx2: nodeidx_t, tag: uchar) -> int


   .. py:method:: supdel_range_idx8(idx1: uchar, idx2: uchar, tag: uchar) -> int


   .. py:method:: hashval(*args) -> ssize_t


   .. py:method:: hashstr(*args) -> ssize_t


   .. py:method:: hashval_long(*args) -> nodeidx_t


   .. py:method:: hashset(*args) -> bool


   .. py:method:: hashset_idx(*args) -> bool


   .. py:method:: hashdel(*args) -> bool


   .. py:method:: hashfirst(*args) -> ssize_t


   .. py:method:: hashnext(*args) -> ssize_t


   .. py:method:: hashlast(*args) -> ssize_t


   .. py:method:: hashprev(*args) -> ssize_t


   .. py:method:: hashdel_all(*args) -> bool


   .. py:method:: blobsize(_start: nodeidx_t, tag: uchar) -> size_t


   .. py:method:: blobsize_ea(ea: ida_idaapi.ea_t, tag: uchar) -> size_t


   .. py:method:: setblob(buf: void const *, _start: nodeidx_t, tag: uchar) -> bool


   .. py:method:: setblob_ea(buf: void const *, ea: ida_idaapi.ea_t, tag: uchar) -> bool


   .. py:method:: delblob(_start: nodeidx_t, tag: uchar) -> int


   .. py:method:: delblob_ea(ea: ida_idaapi.ea_t, tag: uchar) -> int


   .. py:method:: blobshift(_from: nodeidx_t, to: nodeidx_t, size: nodeidx_t, tag: uchar) -> size_t


   .. py:method:: start() -> bool


   .. py:method:: end() -> bool


   .. py:method:: next() -> bool


   .. py:method:: prev() -> bool


   .. py:method:: copyto(destnode: netnode, count: nodeidx_t = 1) -> size_t


   .. py:method:: moveto(destnode: netnode, count: nodeidx_t = 1) -> size_t


   .. py:method:: index() -> nodeidx_t


   .. py:method:: getblob(start, tag) -> Union[bytes, None]

      Get a blob from a netnode.

      :param start: the index where the blob starts (it may span on multiple indexes)
      :param tag: the netnode tag
      :returns: a blob, or None



   .. py:method:: getclob(start, tag) -> Union[str, None]

      Get a large amount of text from a netnode.

      :param start: the index where the clob starts (it may span on multiple indexes)
      :param tag: the netnode tag
      :returns: a clob, or None



   .. py:method:: getblob_ea(ea: ida_idaapi.ea_t, tag: char) -> PyObject *


   .. py:method:: hashstr_buf(*args) -> PyObject *


   .. py:method:: hashset_buf(*args) -> bool


   .. py:method:: supset(*args) -> bool


   .. py:method:: supset_ea(*args) -> bool


.. py:data:: cvar

.. py:data:: MAXNAMESIZE

   Maximum length of a netnode name. WILL BE REMOVED IN THE FUTURE.


.. py:data:: MAX_NODENAME_SIZE

   Maximum length of a name. We permit names up to 32KB-1 bytes.


.. py:data:: MAXSPECSIZE

   Maximum length of strings or objects stored in a supval array element.


.. py:data:: atag

   Array of altvals.


.. py:data:: stag

   Array of supvals.


.. py:data:: htag

   Array of hashvals.


.. py:data:: vtag

   Value of netnode.


.. py:data:: ntag

   Name of netnode.


.. py:data:: ltag

   Links between netnodes.


.. py:data:: NETMAP_IDX

.. py:data:: NETMAP_VAL

.. py:data:: NETMAP_STR

.. py:data:: NETMAP_X8

.. py:data:: NETMAP_V8

.. py:data:: NETMAP_VAL_NDX

.. py:function:: exist(n: netnode) -> bool

.. py:data:: netnode_exist


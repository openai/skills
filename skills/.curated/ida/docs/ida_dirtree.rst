ida_dirtree
===========

.. py:module:: ida_dirtree

.. autoapi-nested-parse::

   Types involved in grouping of item into folders.

   The dirtree_t class is used to organize a directory tree on top of any collection that allows for accessing its elements by an id (inode).
   No requirements are imposed on the inodes apart from the forbidden value -1 (used to denote a bad inode).
   The dirspec_t class is used to specialize the dirtree. It can be used to introduce a directory structure for:
   * local types
   * structs
   * enums
   * functions
   * names
   * etc




Attributes
----------

.. autoapisummary::

   ida_dirtree.DTN_FULL_NAME
   ida_dirtree.DTN_DISPLAY_NAME
   ida_dirtree.DTE_OK
   ida_dirtree.DTE_ALREADY_EXISTS
   ida_dirtree.DTE_NOT_FOUND
   ida_dirtree.DTE_NOT_DIRECTORY
   ida_dirtree.DTE_NOT_EMPTY
   ida_dirtree.DTE_BAD_PATH
   ida_dirtree.DTE_CANT_RENAME
   ida_dirtree.DTE_OWN_CHILD
   ida_dirtree.DTE_MAX_DIR
   ida_dirtree.DTE_LAST
   ida_dirtree.DIRTREE_LOCAL_TYPES
   ida_dirtree.DIRTREE_FUNCS
   ida_dirtree.DIRTREE_NAMES
   ida_dirtree.DIRTREE_IMPORTS
   ida_dirtree.DIRTREE_IDAPLACE_BOOKMARKS
   ida_dirtree.DIRTREE_BPTS
   ida_dirtree.DIRTREE_LTYPES_BOOKMARKS
   ida_dirtree.DIRTREE_END


Classes
-------

.. autoapisummary::

   ida_dirtree.direntry_vec_t
   ida_dirtree.dirtree_cursor_vec_t
   ida_dirtree.direntry_t
   ida_dirtree.dirspec_t
   ida_dirtree.dirtree_cursor_t
   ida_dirtree.dirtree_selection_t
   ida_dirtree.dirtree_iterator_t
   ida_dirtree.dirtree_visitor_t
   ida_dirtree.dirtree_t


Functions
---------

.. autoapisummary::

   ida_dirtree.get_std_dirtree


Module Contents
---------------

.. py:class:: direntry_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> direntry_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> direntry_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: direntry_vec_t) -> None


   .. py:method:: extract() -> direntry_t *


   .. py:method:: inject(s: direntry_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< direntry_t >::const_iterator


   .. py:method:: end(*args) -> qvector< direntry_t >::const_iterator


   .. py:method:: insert(it: direntry_t, x: direntry_t) -> qvector< direntry_t >::iterator


   .. py:method:: erase(*args) -> qvector< direntry_t >::iterator


   .. py:method:: find(*args) -> qvector< direntry_t >::const_iterator


   .. py:method:: has(x: direntry_t) -> bool


   .. py:method:: add_unique(x: direntry_t) -> bool


   .. py:method:: append(x: direntry_t) -> None


   .. py:method:: extend(x: direntry_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: dirtree_cursor_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> dirtree_cursor_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> dirtree_cursor_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: dirtree_cursor_vec_t) -> None


   .. py:method:: extract() -> dirtree_cursor_t *


   .. py:method:: inject(s: dirtree_cursor_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< dirtree_cursor_t >::const_iterator


   .. py:method:: end(*args) -> qvector< dirtree_cursor_t >::const_iterator


   .. py:method:: insert(it: dirtree_cursor_t, x: dirtree_cursor_t) -> qvector< dirtree_cursor_t >::iterator


   .. py:method:: erase(*args) -> qvector< dirtree_cursor_t >::iterator


   .. py:method:: find(*args) -> qvector< dirtree_cursor_t >::const_iterator


   .. py:method:: has(x: dirtree_cursor_t) -> bool


   .. py:method:: add_unique(x: dirtree_cursor_t) -> bool


   .. py:method:: append(x: dirtree_cursor_t) -> None


   .. py:method:: extend(x: dirtree_cursor_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: direntry_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: idx
      :type:  int

      diridx_t or inode_t



   .. py:attribute:: isdir
      :type:  bool

      is 'idx' a diridx_t, or an inode_t



   .. py:attribute:: BADIDX


   .. py:attribute:: ROOTIDX


   .. py:method:: valid() -> bool


.. py:data:: DTN_FULL_NAME

   use long form of the entry name. That name is unique. 
             


.. py:data:: DTN_DISPLAY_NAME

   use short, displayable form of the entry name. for example, 'std::string' instead of 'std::basic_string<char, ...>'. Note that more than one "full name" can have the same displayable name. 
             


.. py:class:: dirspec_t(nm: str = None, f: int = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: flags
      :type:  int


   .. py:attribute:: DSF_INODE_EA


   .. py:attribute:: DSF_PRIVRANGE


   .. py:attribute:: DSF_ORDERABLE


   .. py:attribute:: id
      :type:  str


   .. py:method:: get_name(inode: inode_t, name_flags: int = DTN_FULL_NAME) -> bool

      get the entry name. for example, the structure name 
              
      :param inode: inode number of the entry
      :param name_flags: how exactly the name should be retrieved. combination of bits for get_...name() methods bits
      :returns: false if the entry does not exist.



   .. py:method:: get_inode(dirpath: str, name: str) -> inode_t

      get the entry inode in the specified directory 
              
      :param dirpath: the absolute directory path with trailing slash
      :param name: the entry name in the directory
      :returns: the entry inode



   .. py:method:: get_attrs(inode: inode_t) -> str


   .. py:method:: rename_inode(inode: inode_t, newname: str) -> bool

      rename the entry 
              
      :returns: success



   .. py:method:: unlink_inode(inode: inode_t) -> None

      event: unlinked an inode 
              



   .. py:method:: is_orderable() -> bool


   .. py:attribute:: nodename


.. py:class:: dirtree_cursor_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: parent
      :type:  diridx_t

      the parent directory



   .. py:attribute:: rank
      :type:  size_t

      the index into the parent directory



   .. py:method:: valid() -> bool


   .. py:method:: is_root_cursor() -> bool


   .. py:method:: set_root_cursor() -> None


   .. py:method:: root_cursor() -> dirtree_cursor_t
      :staticmethod:



   .. py:method:: compare(r: dirtree_cursor_t) -> int


.. py:class:: dirtree_selection_t

   Bases: :py:obj:`dirtree_cursor_vec_t`


   .. py:attribute:: thisown


.. py:class:: dirtree_iterator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: pattern
      :type:  str


   .. py:attribute:: cursor
      :type:  dirtree_cursor_t


.. py:data:: DTE_OK

   ok


.. py:data:: DTE_ALREADY_EXISTS

   item already exists


.. py:data:: DTE_NOT_FOUND

   item not found


.. py:data:: DTE_NOT_DIRECTORY

   item is not a directory


.. py:data:: DTE_NOT_EMPTY

   directory is not empty


.. py:data:: DTE_BAD_PATH

   invalid path


.. py:data:: DTE_CANT_RENAME

   failed to rename an item


.. py:data:: DTE_OWN_CHILD

   moving inside subdirectory of itself


.. py:data:: DTE_MAX_DIR

   maximum directory count achieved


.. py:data:: DTE_LAST

.. py:class:: dirtree_visitor_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: visit(c: dirtree_cursor_t, de: direntry_t) -> ssize_t

      Will be called for each entry in the dirtree_t If something other than 0 is returned, iteration will stop. 
              
      :param c: the current cursor
      :param de: the current entry
      :returns: 0 to keep iterating, or anything else to stop



.. py:class:: dirtree_t(ds: dirspec_t)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: errstr(err: dterr_t) -> str
      :staticmethod:


      Get textual representation of the error code.



   .. py:method:: is_orderable() -> bool

      Is dirtree orderable? 
              
      :returns: true if the dirtree is orderable



   .. py:method:: chdir(path: str) -> dterr_t

      Change current directory 
              
      :param path: new current directory
      :returns: dterr_t error code



   .. py:method:: getcwd() -> str

      Get current directory 
              
      :returns: the current working directory



   .. py:method:: get_abspath(*args) -> str

      This function has the following signatures:

          0. get_abspath(cursor: const dirtree_cursor_t &, name_flags: int=DTN_FULL_NAME) -> str
          1. get_abspath(relpath: str) -> str

      # 0: get_abspath(cursor: const dirtree_cursor_t &, name_flags: int=DTN_FULL_NAME) -> str

      Get absolute path pointed by the cursor 
              
      :returns: path; empty string if error

      # 1: get_abspath(relpath: str) -> str

      Construct an absolute path from the specified relative path. This function verifies the directory part of the specified path. The last component of the specified path is not verified. 
              
      :returns: path. empty path means wrong directory part of RELPATH



   .. py:method:: resolve_cursor(cursor: dirtree_cursor_t) -> direntry_t

      Resolve cursor 
              
      :param cursor: to analyze
      :returns: directory entry; if the cursor is bad, the resolved entry will be invalid.



   .. py:method:: resolve_path(path: str) -> direntry_t

      Resolve path 
              
      :param path: to analyze
      :returns: directory entry



   .. py:method:: isdir(*args) -> bool

      This function has the following signatures:

          0. isdir(path: str) -> bool
          1. isdir(de: const direntry_t &) -> bool

      # 0: isdir(path: str) -> bool

      Is a directory? 
              
      :returns: true if the specified path is a directory

      # 1: isdir(de: const direntry_t &) -> bool



   .. py:method:: isfile(*args) -> bool

      This function has the following signatures:

          0. isfile(path: str) -> bool
          1. isfile(de: const direntry_t &) -> bool

      # 0: isfile(path: str) -> bool

      Is a file? 
              
      :returns: true if the specified path is a file

      # 1: isfile(de: const direntry_t &) -> bool



   .. py:method:: get_entry_name(de: direntry_t, name_flags: int = DTN_FULL_NAME) -> str

      Get entry name 
              
      :param de: directory entry
      :param name_flags: how exactly the name should be retrieved. combination of bits for get_...name() methods bits
      :returns: name



   .. py:method:: is_dir_ordered(diridx: diridx_t) -> bool

      Is dir ordered? 
              
      :returns: true if the dirtree has natural ordering



   .. py:method:: set_natural_order(diridx: diridx_t, enable: bool) -> bool

      Enable/disable natural inode order in a directory. 
              
      :param diridx: directory index
      :param enable: action to do TRUE - enable ordering: re-order existing entries so that all subdirs are at the to beginning of the list, file entries are sorted and placed after the subdirs FALSE - disable ordering, no changes to existing entries
      :returns: SUCCESS



   .. py:method:: get_dir_size(diridx: diridx_t) -> ssize_t

      Get dir size 
              
      :param diridx: directory index
      :returns: number of entries under this directory; if error, return -1



   .. py:method:: get_entry_attrs(de: direntry_t) -> str

      Get entry attributes 
              
      :param de: directory entry
      :returns: name



   .. py:method:: findfirst(ff: dirtree_iterator_t, pattern: str) -> bool

      Start iterating over files in a directory 
              
      :param ff: directory iterator. it will be initialized by the function
      :param pattern: pattern to search for
      :returns: success



   .. py:method:: findnext(ff: dirtree_iterator_t) -> bool

      Continue iterating over files in a directory 
              
      :param ff: directory iterator
      :returns: success



   .. py:method:: mkdir(path: str) -> dterr_t

      Create a directory. 
              
      :param path: directory to create
      :returns: dterr_t error code



   .. py:method:: rmdir(path: str) -> dterr_t

      Remove a directory. 
              
      :param path: directory to delete
      :returns: dterr_t error code



   .. py:method:: link(*args) -> dterr_t

      This function has the following signatures:

          0. link(path: str) -> dterr_t
          1. link(inode: inode_t) -> dterr_t

      # 0: link(path: str) -> dterr_t

      Add a file item into a directory. 
              
      :returns: dterr_t error code

      # 1: link(inode: inode_t) -> dterr_t

      Add an inode into the current directory 
              
      :returns: dterr_t error code



   .. py:method:: unlink(*args) -> dterr_t

      This function has the following signatures:

          0. unlink(path: str) -> dterr_t
          1. unlink(inode: inode_t) -> dterr_t

      # 0: unlink(path: str) -> dterr_t

      Remove a file item from a directory. 
              
      :returns: dterr_t error code

      # 1: unlink(inode: inode_t) -> dterr_t

      Remove an inode from the current directory 
              
      :returns: dterr_t error code



   .. py:method:: rename(_from: str, to: str) -> dterr_t

      Rename a directory entry. 
              
      :param to: destination path
      :returns: dterr_t error code



   .. py:method:: get_rank(diridx: diridx_t, de: direntry_t) -> ssize_t

      Get ordering rank of an item. 
              
      :param diridx: index of the parent directory
      :param de: directory entry
      :returns: number in a range of [0..n) where n is the number of entries in the parent directory. -1 if error



   .. py:method:: change_rank(path: str, rank_delta: ssize_t) -> dterr_t

      Change ordering rank of an item. 
              
      :param path: path to the item
      :param rank_delta: the amount of the change. positive numbers mean to move down in the list; negative numbers mean to move up.
      :returns: dterr_t error code



   .. py:method:: get_parent_cursor(cursor: dirtree_cursor_t) -> dirtree_cursor_t

      Get parent cursor. 
              
      :param cursor: a valid ditree cursor
      :returns: cursor's parent



   .. py:method:: load() -> bool

      Load the tree structure from the netnode. If dirspec_t::id is empty, the operation will be considered a success. In addition, calling load() more than once will not do anything, and will be considered a success. 
              
      :returns: success



   .. py:method:: save() -> bool

      Save the tree structure to the netnode. 
              
      :returns: success



   .. py:method:: get_id() -> str

      netnode name



   .. py:method:: set_id(nm: str) -> None


   .. py:method:: notify_dirtree(added: bool, inode: inode_t) -> None

      Notify dirtree about a change of an inode. 
              
      :param added: are we adding or deleting an inode?
      :param inode: inode in question



   .. py:method:: traverse(v: dirtree_visitor_t) -> ssize_t

      Traverse dirtree, and be notified at each entry If the the visitor returns anything other than 0, iteration will stop, and that value returned. The tree is traversed using a depth-first algorithm. It is forbidden to modify the dirtree_t during traversal; doing so will result in undefined behavior. 
              
      :param v: the callback
      :returns: 0, or whatever the visitor returned



   .. py:method:: find_entry(de: direntry_t) -> dirtree_cursor_t

      Find the cursor corresponding to an entry of a directory 
              
      :param de: directory entry
      :returns: cursor corresponding to the directory entry



   .. py:attribute:: get_nodename


   .. py:attribute:: set_nodename


.. py:data:: DIRTREE_LOCAL_TYPES

.. py:data:: DIRTREE_FUNCS

.. py:data:: DIRTREE_NAMES

.. py:data:: DIRTREE_IMPORTS

.. py:data:: DIRTREE_IDAPLACE_BOOKMARKS

.. py:data:: DIRTREE_BPTS

.. py:data:: DIRTREE_LTYPES_BOOKMARKS

.. py:data:: DIRTREE_END

.. py:function:: get_std_dirtree(id: dirtree_id_t) -> dirtree_t *


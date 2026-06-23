ida_registry
============

.. py:module:: ida_registry

.. autoapi-nested-parse::

   Registry related functions.

   IDA uses the registry to store global configuration options that must persist after IDA has been closed.
   On Windows, IDA uses the Windows registry directly. On Unix systems, the registry is stored in a file (typically ~/.idapro/ida.reg).
   The root key for accessing IDA settings in the registry is defined by ROOT_KEY_NAME. 
       



Attributes
----------

.. autoapisummary::

   ida_registry.IDA_REGISTRY_NAME
   ida_registry.HVUI_REGISTRY_NAME
   ida_registry.ROOT_KEY_NAME
   ida_registry.reg_unknown
   ida_registry.reg_sz
   ida_registry.reg_binary
   ida_registry.reg_dword


Functions
---------

.. autoapisummary::

   ida_registry.reg_read_string
   ida_registry.reg_data_type
   ida_registry.reg_read_binary
   ida_registry.reg_write_binary
   ida_registry.reg_subkey_subkeys
   ida_registry.reg_subkey_values
   ida_registry.reg_delete_subkey
   ida_registry.reg_delete_tree
   ida_registry.reg_delete
   ida_registry.reg_subkey_exists
   ida_registry.reg_exists
   ida_registry.reg_read_strlist
   ida_registry.reg_write_strlist
   ida_registry.reg_update_strlist
   ida_registry.reg_write_string
   ida_registry.reg_read_int
   ida_registry.reg_write_int
   ida_registry.reg_read_bool
   ida_registry.reg_write_bool
   ida_registry.reg_update_filestrlist
   ida_registry.set_registry_name


Module Contents
---------------

.. py:function:: reg_read_string(name: str, subkey: str = None, _def: str = None) -> PyObject *

   Read a string from the registry. 
           
   :param name: value name
   :param subkey: key name
   :returns: success


.. py:function:: reg_data_type(name: str, subkey: str = None) -> regval_type_t

   Get data type of a given value. 
           
   :param name: value name
   :param subkey: key name
   :returns: false if the [key+]value doesn't exist


.. py:function:: reg_read_binary(name: str, subkey: str = None) -> PyObject *

   Read binary data from the registry. 
           
   :param name: value name
   :param subkey: key name
   :returns: false if 'data' is not large enough to hold all data present. in this case 'data' is left untouched.


.. py:function:: reg_write_binary(name: str, py_bytes: PyObject *, subkey: str = None) -> PyObject *

   Write binary data to the registry. 
           
   :param name: value name
   :param subkey: key name


.. py:function:: reg_subkey_subkeys(name: str) -> PyObject *

   Get all subkey names of given key.


.. py:function:: reg_subkey_values(name: str) -> PyObject *

   Get all value names under given key.


.. py:data:: IDA_REGISTRY_NAME

.. py:data:: HVUI_REGISTRY_NAME

.. py:data:: ROOT_KEY_NAME

   Default key used to store IDA settings in registry (Windows version). 
           


.. py:data:: reg_unknown

   unknown


.. py:data:: reg_sz

   utf8 string


.. py:data:: reg_binary

   binary data


.. py:data:: reg_dword

   32-bit number


.. py:function:: reg_delete_subkey(name: str) -> bool

   Delete a key from the registry.


.. py:function:: reg_delete_tree(name: str) -> bool

   Delete a subtree from the registry.


.. py:function:: reg_delete(name: str, subkey: str = None) -> bool

   Delete a value from the registry. 
           
   :param name: value name
   :param subkey: parent key
   :returns: success


.. py:function:: reg_subkey_exists(name: str) -> bool

   Is there already a key with the given name?


.. py:function:: reg_exists(name: str, subkey: str = None) -> bool

   Is there already a value with the given name? 
           
   :param name: value name
   :param subkey: parent key


.. py:function:: reg_read_strlist(subkey: str) -> List[str]

   Retrieve all string values associated with the given key.

   :param subkey: a key from which to read the list of items
   :returns: the list of items


.. py:function:: reg_write_strlist(items: List[str], subkey: str)

   Write string values associated with the given key.

   :param items: the list of items to write
   :param subkey: a key under which to write the list of items


.. py:function:: reg_update_strlist(subkey: str, add: Union[str, None], maxrecs: int, rem: Union[str, None] = None, ignorecase: bool = False)

   Add and/or remove items from the list, and possibly trim that list.

   :param subkey: the key under which the list is located
   :param add: an item to add to the list, or None
   :param maxrecs: the maximum number of items the list should hold
   :param rem: an item to remove from the list, or None
   :param ignorecase: ignore case for 'add' and 'rem'


.. py:function:: reg_write_string(name: str, utf8: str, subkey: str = None) -> None

   Write a string to the registry. 
           
   :param name: value name
   :param utf8: utf8-encoded string
   :param subkey: key name


.. py:function:: reg_read_int(name: str, defval: int, subkey: str = None) -> int

   Read integer value from the registry. 
           
   :param name: value name
   :param defval: default value
   :param subkey: key name
   :returns: the value read from the registry, or 'defval' if the read failed


.. py:function:: reg_write_int(name: str, value: int, subkey: str = None) -> None

   Write integer value to the registry. 
           
   :param name: value name
   :param value: value to write
   :param subkey: key name


.. py:function:: reg_read_bool(name: str, defval: bool, subkey: str = None) -> bool

   Read boolean value from the registry. 
           
   :param name: value name
   :param defval: default value
   :param subkey: key name
   :returns: boolean read from registry, or 'defval' if the read failed


.. py:function:: reg_write_bool(name: str, value: int, subkey: str = None) -> None

   Write boolean value to the registry. 
           
   :param name: value name
   :param value: boolean to write (nonzero = true)
   :param subkey: key name


.. py:function:: reg_update_filestrlist(subkey: str, add: str, maxrecs: size_t, rem: str = None) -> None

   Update registry with a file list. Case sensitivity will vary depending on the target OS. 
           


.. py:function:: set_registry_name(name: str) -> bool


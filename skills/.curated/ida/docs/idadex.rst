idadex
======

.. py:module:: idadex


Attributes
----------

.. autoapisummary::

   idadex.uint8
   idadex.char
   idadex.uint32
   idadex.uint64
   idadex.uint16
   idadex.ushort
   idadex.ea_t
   idadex.dex


Classes
-------

.. autoapisummary::

   idadex.dex_method
   idadex.dex_field
   idadex.longname_director_t
   idadex.Dex


Functions
---------

.. autoapisummary::

   idadex.to_uint32
   idadex.get_struct
   idadex.unpack_db
   idadex.get_dw
   idadex.unpack_dw
   idadex.unpack_dd
   idadex.unpack_dq
   idadex.unpack_ea
   idadex.unpack_eavec


Module Contents
---------------

.. py:data:: uint8

.. py:data:: char

.. py:data:: uint32

.. py:data:: uint64

.. py:data:: uint16

.. py:data:: ushort

.. py:data:: ea_t

.. py:function:: to_uint32(v)

.. py:function:: get_struct(str_, off, struct)

.. py:function:: unpack_db(buf, off)

.. py:function:: get_dw(buf, off)

.. py:function:: unpack_dw(buf, off)

.. py:function:: unpack_dd(buf, off)

.. py:function:: unpack_dq(buf, off)

.. py:function:: unpack_ea(buf, off)

.. py:function:: unpack_eavec(buf, base_ea)

.. py:class:: dex_method

   Bases: :py:obj:`ctypes.LittleEndianStructure`


   Structure base class


   .. py:attribute:: IS_LOCAL
      :value: 1



   .. py:attribute:: HAS_CODE
      :value: 2



   .. py:method:: is_local()


.. py:class:: dex_field

   Bases: :py:obj:`ctypes.LittleEndianStructure`


   Structure base class


.. py:class:: longname_director_t

   Bases: :py:obj:`ctypes.LittleEndianStructure`


   Structure base class


.. py:class:: Dex

   Bases: :py:obj:`object`


   .. py:attribute:: HASHVAL_MAGIC
      :value: 'version'



   .. py:attribute:: HASHVAL_OPTIMIZED
      :value: 'optimized'



   .. py:attribute:: HASHVAL_DEXVERSION
      :value: 'dex_version'



   .. py:attribute:: META_BASEADDRS
      :value: 1



   .. py:attribute:: DEXCMN_STRING_ID


   .. py:attribute:: DEXCMN_METHOD_ID


   .. py:attribute:: DEXCMN_TRY_TYPES


   .. py:attribute:: DEXCMN_TRY_IDS


   .. py:attribute:: DEXCMN_DEBINFO


   .. py:attribute:: DEXCMN_DEBSTR


   .. py:attribute:: DEXVAR_STRING_IDS


   .. py:attribute:: DEXVAR_TYPE_IDS


   .. py:attribute:: DEXVAR_TYPE_STR


   .. py:attribute:: DEXVAR_TYPE_STRO


   .. py:attribute:: DEXVAR_METHOD


   .. py:attribute:: DEXVAR_METH_STR


   .. py:attribute:: DEXVAR_METH_STRO


   .. py:attribute:: DEXVAR_FIELD


   .. py:attribute:: DEXVAR_TRYLIST


   .. py:attribute:: DEBINFO_LINEINFO
      :value: 1



   .. py:attribute:: nn_meta


   .. py:attribute:: nn_cmn


   .. py:attribute:: baseaddrs
      :value: []



   .. py:attribute:: nn_vars
      :value: []



   .. py:method:: get_dexnum(from_ea)


   .. py:method:: get_nn_var(from_ea)


   .. py:attribute:: ACCESS_FLAGS


   .. py:method:: access_string(flags)
      :staticmethod:



   .. py:method:: as_string(s)
      :staticmethod:



   .. py:method:: idx_to_ea(from_ea, idx, tag)


   .. py:method:: get_string(from_ea, string_idx)


   .. py:method:: get_method_idx(ea)


   .. py:method:: get_method(from_ea, method_idx)


   .. py:method:: get_string_by_index(node, idx, tag)
      :staticmethod:



   .. py:attribute:: PRIMITVE_TYPES


   .. py:method:: is_wide_type(typechar)
      :staticmethod:



   .. py:method:: decorate_java_typename(desc)
      :staticmethod:



   .. py:method:: get_type_string(from_ea, type_idx)


   .. py:method:: get_method_name(from_ea, method_idx)


   .. py:method:: get_parameter_name(from_ea, idx)


   .. py:method:: get_short_type_name(longname)
      :staticmethod:



   .. py:method:: get_full_type_name(longname)
      :staticmethod:



   .. py:method:: get_short_method_name(method)


   .. py:method:: get_full_method_name(method)


   .. py:method:: get_call_method_name(method)


   .. py:method:: get_field(from_ea, field_idx)


   .. py:method:: get_field_name(from_ea, field_idx)


   .. py:method:: get_full_field_name(field_idx, field, field_name)


   .. py:method:: get_short_field_name(field_idx, field, field_name)


.. py:data:: dex


ida_tryblks
===========

.. py:module:: ida_tryblks

.. autoapi-nested-parse::

   Architecture independent exception handling info.

   Try blocks have the following general properties:
   * A try block specifies a possibly fragmented guarded code region.
   * Each try block has always at least one catch/except block description
   * Each catch block contains its boundaries and a filter.
   * Additionally a catch block can hold sp adjustment and the offset to the exception object offset (C++).
   * Try blocks can be nested. Nesting is automatically calculated at the retrieval time.
   * There may be (nested) multiple try blocks starting at the same address.


   See examples in tests/input/src/eh_tests. 
       



Attributes
----------

.. autoapisummary::

   ida_tryblks.TBERR_OK
   ida_tryblks.TBERR_START
   ida_tryblks.TBERR_END
   ida_tryblks.TBERR_ORDER
   ida_tryblks.TBERR_EMPTY
   ida_tryblks.TBERR_KIND
   ida_tryblks.TBERR_NO_CATCHES
   ida_tryblks.TBERR_INTERSECT
   ida_tryblks.TBEA_TRY
   ida_tryblks.TBEA_CATCH
   ida_tryblks.TBEA_SEHTRY
   ida_tryblks.TBEA_SEHLPAD
   ida_tryblks.TBEA_SEHFILT
   ida_tryblks.TBEA_ANY
   ida_tryblks.TBEA_FALLTHRU


Classes
-------

.. autoapisummary::

   ida_tryblks.tryblks_t
   ida_tryblks.catchvec_t
   ida_tryblks.try_handler_t
   ida_tryblks.seh_t
   ida_tryblks.catch_t
   ida_tryblks.tryblk_t


Functions
---------

.. autoapisummary::

   ida_tryblks.get_tryblks
   ida_tryblks.del_tryblks
   ida_tryblks.add_tryblk
   ida_tryblks.find_syseh
   ida_tryblks.is_ea_tryblks


Module Contents
---------------

.. py:class:: tryblks_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> tryblk_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> tryblk_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: tryblks_t) -> None


   .. py:method:: extract() -> tryblk_t *


   .. py:method:: inject(s: tryblk_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< tryblk_t >::const_iterator


   .. py:method:: end(*args) -> qvector< tryblk_t >::const_iterator


   .. py:method:: insert(it: tryblk_t, x: tryblk_t) -> qvector< tryblk_t >::iterator


   .. py:method:: erase(*args) -> qvector< tryblk_t >::iterator


   .. py:method:: find(*args) -> qvector< tryblk_t >::const_iterator


   .. py:method:: has(x: tryblk_t) -> bool


   .. py:method:: add_unique(x: tryblk_t) -> bool


   .. py:method:: append(x: tryblk_t) -> None


   .. py:method:: extend(x: tryblks_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: catchvec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> catch_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> catch_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: catchvec_t) -> None


   .. py:method:: extract() -> catch_t *


   .. py:method:: inject(s: catch_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< catch_t >::const_iterator


   .. py:method:: end(*args) -> qvector< catch_t >::const_iterator


   .. py:method:: insert(it: catch_t, x: catch_t) -> qvector< catch_t >::iterator


   .. py:method:: erase(*args) -> qvector< catch_t >::iterator


   .. py:method:: find(*args) -> qvector< catch_t >::const_iterator


   .. py:method:: has(x: catch_t) -> bool


   .. py:method:: add_unique(x: catch_t) -> bool


   .. py:method:: append(x: catch_t) -> None


   .. py:method:: extend(x: catchvec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: try_handler_t

   Bases: :py:obj:`ida_range.rangevec_t`


   .. py:attribute:: thisown


   .. py:attribute:: disp
      :type:  int


   .. py:attribute:: fpreg
      :type:  int


   .. py:method:: clear() -> None


.. py:class:: seh_t

   Bases: :py:obj:`try_handler_t`


   .. py:attribute:: thisown


   .. py:attribute:: filter
      :type:  rangevec_t


   .. py:attribute:: seh_code
      :type:  ida_idaapi.ea_t


   .. py:method:: clear() -> None


.. py:class:: catch_t

   Bases: :py:obj:`try_handler_t`


   .. py:attribute:: thisown


   .. py:attribute:: obj
      :type:  int


   .. py:attribute:: type_id
      :type:  int


.. py:class:: tryblk_t(*args)

   Bases: :py:obj:`ida_range.rangevec_t`


   .. py:attribute:: thisown


   .. py:attribute:: level
      :type:  uchar


   .. py:method:: cpp() -> catchvec_t &


   .. py:method:: seh() -> seh_t &


   .. py:method:: get_kind() -> uchar


   .. py:method:: empty() -> bool


   .. py:method:: is_seh() -> bool


   .. py:method:: is_cpp() -> bool


   .. py:method:: clear() -> None


   .. py:method:: set_seh() -> seh_t &


   .. py:method:: set_cpp() -> catchvec_t &


.. py:function:: get_tryblks(tbv: tryblks_t, range: range_t) -> size_t

   ------------------------------------------------------------------------- Retrieve try block information from the specified address range. Try blocks are sorted by starting address and their nest levels calculated. 
           
   :param tbv: output buffer; may be nullptr
   :param range: address range to change
   :returns: number of found try blocks


.. py:function:: del_tryblks(range: range_t) -> None

   Delete try block information in the specified range. 
           
   :param range: the range to be cleared


.. py:function:: add_tryblk(tb: tryblk_t) -> int

   Add one try block information. 
           
   :param tb: try block to add.
   :returns: error code; 0 means good


.. py:data:: TBERR_OK

   ok


.. py:data:: TBERR_START

   bad start address


.. py:data:: TBERR_END

   bad end address


.. py:data:: TBERR_ORDER

   bad address order


.. py:data:: TBERR_EMPTY

   empty try block


.. py:data:: TBERR_KIND

   illegal try block kind


.. py:data:: TBERR_NO_CATCHES

   no catch blocks at all


.. py:data:: TBERR_INTERSECT

   range would intersect inner tryblk


.. py:function:: find_syseh(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

   Find the start address of the system eh region including the argument. 
           
   :param ea: search address
   :returns: start address of surrounding tryblk, otherwise BADADDR


.. py:data:: TBEA_TRY

   is EA within a c++ try block?


.. py:data:: TBEA_CATCH

   is EA the start of a c++ catch/cleanup block?


.. py:data:: TBEA_SEHTRY

   is EA within a seh try block


.. py:data:: TBEA_SEHLPAD

   is EA the start of a seh finally/except block?


.. py:data:: TBEA_SEHFILT

   is EA the start of a seh filter?


.. py:data:: TBEA_ANY

.. py:data:: TBEA_FALLTHRU

   is there a fall through into provided ea from an unwind region


.. py:function:: is_ea_tryblks(ea: ida_idaapi.ea_t, flags: int) -> bool

   Check if the given address ea is part of tryblks description. 
           
   :param ea: address to check
   :param flags: combination of flags for is_ea_tryblks()



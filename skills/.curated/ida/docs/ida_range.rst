ida_range
=========

.. py:module:: ida_range

.. autoapi-nested-parse::

   Contains the definition of range_t.

   A range is a non-empty continuous range of addresses (specified by its start and end addresses, the end address is excluded from the range).
   Ranges are stored in the Btree part of the IDA database. To learn more about Btrees (Balanced Trees): [http://www.bluerwhite.org/btree/](http://www.bluerwhite.org/btree/) 
       



Attributes
----------

.. autoapisummary::

   ida_range.RANGE_KIND_UNKNOWN
   ida_range.RANGE_KIND_FUNC
   ida_range.RANGE_KIND_SEGMENT
   ida_range.RANGE_KIND_HIDDEN_RANGE


Classes
-------

.. autoapisummary::

   ida_range.rangevec_base_t
   ida_range.array_of_rangesets
   ida_range.range_t
   ida_range.rangevec_t
   ida_range.rangeset_t


Functions
---------

.. autoapisummary::

   ida_range.range_t_print


Module Contents
---------------

.. py:class:: rangevec_base_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> range_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> range_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: rangevec_base_t) -> None


   .. py:method:: extract() -> range_t *


   .. py:method:: inject(s: range_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< range_t >::const_iterator


   .. py:method:: end(*args) -> qvector< range_t >::const_iterator


   .. py:method:: insert(it: range_t, x: range_t) -> qvector< range_t >::iterator


   .. py:method:: erase(*args) -> qvector< range_t >::iterator


   .. py:method:: find(*args) -> qvector< range_t >::const_iterator


   .. py:method:: has(x: range_t) -> bool


   .. py:method:: add_unique(x: range_t) -> bool


   .. py:method:: append(x: range_t) -> None


   .. py:method:: extend(x: rangevec_base_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: array_of_rangesets(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> rangeset_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> rangeset_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: array_of_rangesets) -> None


   .. py:method:: extract() -> rangeset_t *


   .. py:method:: inject(s: rangeset_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< rangeset_t >::const_iterator


   .. py:method:: end(*args) -> qvector< rangeset_t >::const_iterator


   .. py:method:: insert(it: rangeset_t, x: rangeset_t) -> qvector< rangeset_t >::iterator


   .. py:method:: erase(*args) -> qvector< rangeset_t >::iterator


   .. py:method:: find(*args) -> qvector< rangeset_t >::const_iterator


   .. py:method:: has(x: rangeset_t) -> bool


   .. py:method:: add_unique(x: rangeset_t) -> bool


   .. py:method:: append(x: rangeset_t) -> None


   .. py:method:: extend(x: array_of_rangesets) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: range_t(ea1: ida_idaapi.ea_t = 0, ea2: ida_idaapi.ea_t = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: start_ea
      :type:  ida_idaapi.ea_t

      start_ea included



   .. py:attribute:: end_ea
      :type:  ida_idaapi.ea_t

      end_ea excluded



   .. py:method:: compare(r: range_t) -> int


   .. py:method:: contains(*args) -> bool

      This function has the following signatures:

          0. contains(ea: ida_idaapi.ea_t) -> bool
          1. contains(r: const range_t &) -> bool

      # 0: contains(ea: ida_idaapi.ea_t) -> bool

      Compare two range_t instances, based on the start_ea.

      Is 'ea' in the address range? 
              

      # 1: contains(r: const range_t &) -> bool

      Is every ea in 'r' also in this range_t?



   .. py:method:: overlaps(r: range_t) -> bool

      Is there an ea in 'r' that is also in this range_t?



   .. py:method:: clear() -> None

      Set start_ea, end_ea to 0.



   .. py:method:: empty() -> bool

      Is the size of the range_t <= 0?



   .. py:method:: size() -> asize_t

      Get end_ea - start_ea.



   .. py:method:: intersect(r: range_t) -> None

      Assign the range_t to the intersection between the range_t and 'r'.



   .. py:method:: extend(ea: ida_idaapi.ea_t) -> None

      Ensure that the range_t includes 'ea'.



.. py:function:: range_t_print(cb: range_t) -> str

   Helper function. Should not be called directly!


.. py:class:: rangevec_t

   Bases: :py:obj:`rangevec_base_t`


   .. py:attribute:: thisown


.. py:data:: RANGE_KIND_UNKNOWN

.. py:data:: RANGE_KIND_FUNC

   func_t


.. py:data:: RANGE_KIND_SEGMENT

   segment_t


.. py:data:: RANGE_KIND_HIDDEN_RANGE

   hidden_range_t


.. py:class:: rangeset_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: swap(r: rangeset_t) -> None

      Set this = 'r' and 'r' = this. See qvector::swap()



   .. py:method:: add(*args) -> bool

      This function has the following signatures:

          0. add(range: const range_t &) -> bool
          1. add(start: ida_idaapi.ea_t, _end: ida_idaapi.ea_t) -> bool
          2. add(aset: const rangeset_t &) -> bool

      # 0: add(range: const range_t &) -> bool

      Add an address range to the set. If 'range' intersects an existing element e, then e is extended to include 'range', and any superfluous elements (subsets of e) are removed. 
              
      :returns: false if 'range' was not added (the set was unchanged)

      # 1: add(start: ida_idaapi.ea_t, _end: ida_idaapi.ea_t) -> bool

      Create a new range_t from 'start' and 'end' and add it to the set.


      # 2: add(aset: const rangeset_t &) -> bool

      Add each element of 'aset' to the set. 
              
      :returns: false if no elements were added (the set was unchanged)



   .. py:method:: sub(*args) -> bool

      This function has the following signatures:

          0. sub(range: const range_t &) -> bool
          1. sub(ea: ida_idaapi.ea_t) -> bool
          2. sub(aset: const rangeset_t &) -> bool

      # 0: sub(range: const range_t &) -> bool

      Subtract an address range from the set. All subsets of 'range' will be removed, and all elements that intersect 'range' will be truncated/split so they do not include 'range'. 
              
      :returns: false if 'range' was not subtracted (the set was unchanged)

      # 1: sub(ea: ida_idaapi.ea_t) -> bool

      Subtract an ea (an range of size 1) from the set. See sub(const range_t &)


      # 2: sub(aset: const rangeset_t &) -> bool

      Subtract each range in 'aset' from the set 
              
      :returns: false if nothing was subtracted (the set was unchanged)



   .. py:method:: includes(range: range_t) -> bool

      Is every ea in 'range' contained in the rangeset?



   .. py:method:: getrange(idx: int) -> range_t const &

      Get the range_t at index 'idx'.



   .. py:method:: lastrange() -> range_t const &

      Get the last range_t in the set.



   .. py:method:: nranges() -> size_t

      Get the number of range_t elements in the set.



   .. py:method:: empty() -> bool

      Does the set have zero elements.



   .. py:method:: clear() -> None

      Delete all elements from the set. See qvector::clear()



   .. py:method:: has_common(*args) -> bool

      This function has the following signatures:

          0. has_common(range: const range_t &) -> bool
          1. has_common(aset: const rangeset_t &) -> bool

      # 0: has_common(range: const range_t &) -> bool

      Is there an ea in 'range' that is also in the rangeset?


      # 1: has_common(aset: const rangeset_t &) -> bool

      Does any element of 'aset' overlap with an element in this rangeset?. See range_t::overlaps()



   .. py:method:: contains(*args) -> bool

      This function has the following signatures:

          0. contains(ea: ida_idaapi.ea_t) -> bool
          1. contains(aset: const rangeset_t &) -> bool

      # 0: contains(ea: ida_idaapi.ea_t) -> bool

      Does an element of the rangeset contain 'ea'? See range_t::contains(ea_t)


      # 1: contains(aset: const rangeset_t &) -> bool

      Is every element in 'aset' contained in an element of this rangeset?. See range_t::contains(range_t)



   .. py:method:: intersect(aset: rangeset_t) -> bool

      Set the rangeset to its intersection with 'aset'. 
              
      :returns: false if the set was unchanged



   .. py:method:: is_subset_of(aset: rangeset_t) -> bool

      Is every element in the rangeset contained in an element of 'aset'?



   .. py:method:: is_equal(aset: rangeset_t) -> bool

      Do this rangeset and 'aset' have identical elements?



   .. py:method:: begin() -> rangeset_t::iterator

      Get an iterator that points to the first element in the set.



   .. py:method:: end() -> rangeset_t::iterator

      Get an iterator that points to the end of the set. (This is NOT the last element)



   .. py:method:: find_range(ea: ida_idaapi.ea_t) -> range_t const *

      Get the element from the set that contains 'ea'. 
              
      :returns: nullptr if there is no such element



   .. py:method:: cached_range() -> range_t const *

      When searching the rangeset, we keep a cached element to help speed up searches. 
              
      :returns: a pointer to the cached element



   .. py:method:: next_addr(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

      Get the smallest ea_t value greater than 'ea' contained in the rangeset.



   .. py:method:: prev_addr(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

      Get the largest ea_t value less than 'ea' contained in the rangeset.



   .. py:method:: next_range(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

      Get the smallest ea_t value greater than 'ea' that is not in the same range as 'ea'.



   .. py:method:: prev_range(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t

      Get the largest ea_t value less than 'ea' that is not in the same range as 'ea'.



   .. py:method:: as_rangevec() -> rangevec_t const &

      Return underlying rangevec_t object.




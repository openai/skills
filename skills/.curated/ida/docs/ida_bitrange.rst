ida_bitrange
============

.. py:module:: ida_bitrange

.. autoapi-nested-parse::

   Definition of the bitrange_t class.



Classes
-------

.. autoapisummary::

   ida_bitrange.bitrange_t


Module Contents
---------------

.. py:class:: bitrange_t(bit_ofs: uint16 = 0, size_in_bits: uint16 = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: init(bit_ofs: uint16, size_in_bits: uint16) -> None

      Initialize offset and size to given values.



   .. py:method:: reset() -> None

      Make the bitrange empty.



   .. py:method:: empty() -> bool

      Is the bitrange empty?



   .. py:method:: bitoff() -> uint

      Get offset of 1st bit.



   .. py:method:: bitsize() -> uint

      Get size of the value in bits.



   .. py:method:: bytesize() -> uint

      Size of the value in bytes.



   .. py:method:: mask64() -> uint64

      Convert to mask of 64 bits.



   .. py:method:: has_common(r: bitrange_t) -> bool

      Does have common bits with another bitrange?



   .. py:method:: apply_mask(subrange: bitrange_t) -> bool

      Apply mask to a bitrange 
              
      :param subrange: range *inside* the main bitrange to keep After this operation the main bitrange will be truncated to have only the bits that are specified by subrange. Example: [off=8,nbits=4], subrange[off=1,nbits=2] => [off=9,nbits=2]
      :returns: success



   .. py:method:: intersect(r: bitrange_t) -> None

      Intersect two ranges.



   .. py:method:: create_union(r: bitrange_t) -> None

      Create union of 2 ranges including the hole between them.



   .. py:method:: sub(r: bitrange_t) -> bool

      Subtract a bitrange.



   .. py:method:: shift_down(cnt: uint) -> None

      Shift range down (left)



   .. py:method:: shift_up(cnt: uint) -> None

      Shift range up (right)



   .. py:method:: extract(src: void const *, is_mf: bool) -> bool


   .. py:method:: inject(dst: void *, src: bytevec_t const &, is_mf: bool) -> bool


   .. py:method:: compare(r: bitrange_t) -> int



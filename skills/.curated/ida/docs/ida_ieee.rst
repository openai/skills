ida_ieee
========

.. py:module:: ida_ieee

.. autoapi-nested-parse::

   IEEE floating point functions.



Attributes
----------

.. autoapisummary::

   ida_ieee.FPVAL_NWORDS
   ida_ieee.FPV_BADARG
   ida_ieee.FPV_NORM
   ida_ieee.FPV_NAN
   ida_ieee.FPV_PINF
   ida_ieee.FPV_NINF
   ida_ieee.REAL_ERROR_OK
   ida_ieee.REAL_ERROR_FORMAT
   ida_ieee.REAL_ERROR_RANGE
   ida_ieee.REAL_ERROR_BADDATA
   ida_ieee.REAL_ERROR_FPOVER
   ida_ieee.REAL_ERROR_BADSTR
   ida_ieee.REAL_ERROR_ZERODIV
   ida_ieee.REAL_ERROR_INTOVER
   ida_ieee.cvar
   ida_ieee.MAXEXP_FLOAT
   ida_ieee.MAXEXP_DOUBLE
   ida_ieee.MAXEXP_LNGDBL
   ida_ieee.IEEE_EXONE
   ida_ieee.E_SPECIAL_EXP
   ida_ieee.IEEE_NI
   ida_ieee.IEEE_E
   ida_ieee.IEEE_M
   ida_ieee.EZERO
   ida_ieee.EONE
   ida_ieee.ETWO


Classes
-------

.. autoapisummary::

   ida_ieee.fpvalue_shorts_array_t
   ida_ieee.fpvalue_t


Functions
---------

.. autoapisummary::

   ida_ieee.ecleaz


Module Contents
---------------

.. py:class:: fpvalue_shorts_array_t(data: unsigned short (&)[FPVAL_NWORDS])

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: data
      :type:  unsigned short (&)[FPVAL_NWORDS]


   .. py:attribute:: bytes


.. py:data:: FPVAL_NWORDS

   number of words in fpvalue_t


.. py:data:: FPV_BADARG

   wrong value of max_exp


.. py:data:: FPV_NORM

   regular value


.. py:data:: FPV_NAN

   NaN.


.. py:data:: FPV_PINF

   positive infinity


.. py:data:: FPV_NINF

   negative infinity


.. py:data:: REAL_ERROR_OK

   no error


.. py:data:: REAL_ERROR_FORMAT

   realcvt: not supported format for current .idp


.. py:data:: REAL_ERROR_RANGE

   realcvt: number too big (small) for store (mem NOT modified)


.. py:data:: REAL_ERROR_BADDATA

   realcvt: illegal real data for load (IEEE data not filled)


.. py:data:: REAL_ERROR_FPOVER

   floating overflow or underflow


.. py:data:: REAL_ERROR_BADSTR

   asctoreal: illegal input string


.. py:data:: REAL_ERROR_ZERODIV

   ediv: divide by 0


.. py:data:: REAL_ERROR_INTOVER

   eetol*: integer overflow


.. py:class:: fpvalue_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: w
      :type:  uint16 [8]


   .. py:method:: clear() -> None


   .. py:method:: compare(r: fpvalue_t) -> int


   .. py:method:: from_10bytes(fpval: void const *) -> fpvalue_error_t

      Conversions for 10-byte floating point values.



   .. py:method:: to_10bytes(fpval: void *) -> fpvalue_error_t


   .. py:method:: from_12bytes(fpval: void const *) -> fpvalue_error_t

      Conversions for 12-byte floating point values.



   .. py:method:: to_12bytes(fpval: void *) -> fpvalue_error_t


   .. py:method:: to_str(*args) -> None

      Convert IEEE to string. 
              
      :param buf: the output buffer
      :param bufsize: the size of the output buffer
      :param mode: broken down into:
      * low byte: number of digits after '.'
      * second byte: FPNUM_LENGTH
      * third byte: FPNUM_DIGITS



   .. py:method:: from_sval(x: int) -> None

      Convert integer to IEEE.



   .. py:method:: from_int64(x: int64) -> None


   .. py:method:: from_uint64(x: uint64) -> None


   .. py:method:: to_sval(round: bool = False) -> fpvalue_error_t

      Convert IEEE to integer (+-0.5 if round)



   .. py:method:: to_int64(round: bool = False) -> fpvalue_error_t


   .. py:method:: to_uint64(round: bool = False) -> fpvalue_error_t


   .. py:method:: fadd(y: fpvalue_t) -> fpvalue_error_t

      Arithmetic operations.



   .. py:method:: fsub(y: fpvalue_t) -> fpvalue_error_t


   .. py:method:: fmul(y: fpvalue_t) -> fpvalue_error_t


   .. py:method:: fdiv(y: fpvalue_t) -> fpvalue_error_t


   .. py:method:: mul_pow2(power_of_2: int) -> fpvalue_error_t

      Multiply by a power of 2.



   .. py:method:: eabs() -> None

      Calculate absolute value.



   .. py:method:: is_negative() -> bool

      Is negative value?



   .. py:method:: negate() -> None

      Negate.



   .. py:method:: get_kind() -> fpvalue_kind_t

      Get value kind.



   .. py:method:: copy() -> fpvalue_t


   .. py:method:: new_from_str(p: str) -> fpvalue_t
      :staticmethod:



   .. py:method:: from_str(p: str) -> fpvalue_error_t

      Convert string to IEEE. 
              



   .. py:method:: assign(r: fpvalue_t) -> None


   .. py:attribute:: bytes


   .. py:attribute:: shorts


   .. py:attribute:: float


   .. py:property:: sval


   .. py:property:: int64


   .. py:property:: uint64


.. py:data:: cvar

.. py:data:: MAXEXP_FLOAT

.. py:data:: MAXEXP_DOUBLE

.. py:data:: MAXEXP_LNGDBL

.. py:data:: IEEE_EXONE

   The exponent of 1.0.


.. py:data:: E_SPECIAL_EXP

   Exponent in fpvalue_t for NaN and Inf.


.. py:data:: IEEE_NI

   Number of 16 bit words in eNI.


.. py:data:: IEEE_E

   Array offset to exponent.


.. py:data:: IEEE_M

   Array offset to high guard word 
           


.. py:function:: ecleaz(x: eNI) -> None

.. py:data:: EZERO
   :value: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


.. py:data:: EONE
   :value: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xff?'


.. py:data:: ETWO
   :value: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00@'



ida_libfuncs
============

.. py:module:: ida_libfuncs


Attributes
----------

.. autoapisummary::

   ida_libfuncs.SIGN_HEADER_MAGIC
   ida_libfuncs.SIGN_HEADER_VERSION
   ida_libfuncs.OSTYPE_MSDOS
   ida_libfuncs.OSTYPE_WIN
   ida_libfuncs.OSTYPE_OS2
   ida_libfuncs.OSTYPE_NETW
   ida_libfuncs.OSTYPE_UNIX
   ida_libfuncs.OSTYPE_OTHER
   ida_libfuncs.APPT_CONSOLE
   ida_libfuncs.APPT_GRAPHIC
   ida_libfuncs.APPT_PROGRAM
   ida_libfuncs.APPT_LIBRARY
   ida_libfuncs.APPT_DRIVER
   ida_libfuncs.APPT_1THREAD
   ida_libfuncs.APPT_MTHREAD
   ida_libfuncs.APPT_16BIT
   ida_libfuncs.APPT_32BIT
   ida_libfuncs.APPT_64BIT
   ida_libfuncs.LS_STARTUP
   ida_libfuncs.LS_CTYPE
   ida_libfuncs.LS_CTYPE2
   ida_libfuncs.LS_CTYPE_ALT
   ida_libfuncs.LS_ZIP
   ida_libfuncs.LS_CTYPE_3V


Classes
-------

.. autoapisummary::

   ida_libfuncs.idasgn_header_t


Functions
---------

.. autoapisummary::

   ida_libfuncs.get_idasgn_header_by_short_name
   ida_libfuncs.get_idasgn_path_by_short_name


Module Contents
---------------

.. py:class:: idasgn_header_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: magic
      :type:  char [6]


   .. py:attribute:: version
      :type:  uchar


   .. py:attribute:: processor_id
      :type:  uchar


   .. py:attribute:: file_formats
      :type:  int


   .. py:attribute:: ostype
      :type:  uint16


   .. py:attribute:: apptype
      :type:  uint16


   .. py:attribute:: flags
      :type:  uint16


   .. py:attribute:: number_of_modules_v5
      :type:  uint16


   .. py:attribute:: ctype_crc
      :type:  uint16


   .. py:attribute:: ctype_name
      :type:  char [12]


   .. py:attribute:: libname_length
      :type:  uchar


   .. py:attribute:: ctype_crc_alt
      :type:  uint16


   .. py:attribute:: number_of_modules
      :type:  int


   .. py:attribute:: pattern_length
      :type:  uint16


   .. py:attribute:: ctype_crc_3v
      :type:  uint16


.. py:data:: SIGN_HEADER_MAGIC

.. py:data:: SIGN_HEADER_VERSION

.. py:data:: OSTYPE_MSDOS

.. py:data:: OSTYPE_WIN

.. py:data:: OSTYPE_OS2

.. py:data:: OSTYPE_NETW

.. py:data:: OSTYPE_UNIX

.. py:data:: OSTYPE_OTHER

.. py:data:: APPT_CONSOLE

.. py:data:: APPT_GRAPHIC

.. py:data:: APPT_PROGRAM

.. py:data:: APPT_LIBRARY

.. py:data:: APPT_DRIVER

.. py:data:: APPT_1THREAD

.. py:data:: APPT_MTHREAD

.. py:data:: APPT_16BIT

.. py:data:: APPT_32BIT

.. py:data:: APPT_64BIT

.. py:data:: LS_STARTUP

.. py:data:: LS_CTYPE

.. py:data:: LS_CTYPE2

.. py:data:: LS_CTYPE_ALT

.. py:data:: LS_ZIP

.. py:data:: LS_CTYPE_3V

.. py:function:: get_idasgn_header_by_short_name(out_header: idasgn_header_t, name: str) -> str

   Get idasgn header by a short signature name. 
           
   :param out_header: buffer for the signature file header
   :param name: short name of a signature
   :returns: true in case of success


.. py:function:: get_idasgn_path_by_short_name(name: str) -> str

   Get idasgn full path by a short signature name. 
           
   :param name: short name of a signature
   :returns: true in case of success



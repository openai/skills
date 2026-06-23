ida_fpro
========

.. py:module:: ida_fpro

.. autoapi-nested-parse::

   System independent counterparts of FILE* related functions from Clib.

   You should not use C standard I/O functions in your modules. The reason: Each module compiled with Borland (and statically linked to Borland's library) will host a copy of the FILE * information.
   So, if you open a file in the plugin and pass the handle to the kernel, the kernel will not be able to use it.
   If you really need to use the standard functions, define USE_STANDARD_FILE_FUNCTIONS. In this case do not mix them with q... functions. 
       



Attributes
----------

.. autoapisummary::

   ida_fpro.QMOVE_CROSS_FS
   ida_fpro.QMOVE_OVERWRITE
   ida_fpro.QMOVE_OVR_RO
   ida_fpro.qfile_t_from_fp
   ida_fpro.qfile_t_from_capsule
   ida_fpro.qfile_t_tmpfile


Classes
-------

.. autoapisummary::

   ida_fpro.qfile_t


Functions
---------

.. autoapisummary::

   ida_fpro.qfclose


Module Contents
---------------

.. py:class:: qfile_t(*args)

   Bases: :py:obj:`object`


   A helper class to work with FILE related functions.


   .. py:attribute:: thisown


   .. py:method:: opened()

      Checks if the file is opened or not



   .. py:method:: close()

      Closes the file



   .. py:method:: open(filename, mode)

      Opens a file

      :param filename: the file name
      :param mode: The mode string, ala fopen() style
      :returns: Boolean



   .. py:method:: from_fp(fp: FILE *) -> qfile_t *
      :staticmethod:



   .. py:method:: from_capsule(pycapsule: PyObject *) -> qfile_t *
      :staticmethod:



   .. py:method:: tmpfile()
      :staticmethod:


      A static method to construct an instance using a temporary file



   .. py:method:: get_fp() -> FILE *


   .. py:method:: seek(offset, whence=ida_idaapi.SEEK_SET)

      Set input source position

      :param offset: the seek offset
      :param whence: the position to seek from
      :returns: the new position (not 0 as fseek!)



   .. py:method:: tell()

      Returns the current position



   .. py:method:: readbytes(size, big_endian)

      Similar to read() but it respect the endianness

      :param size: the maximum number of bytes to read
      :param big_endian: endianness
      :returns: a str, or None



   .. py:method:: read(size)

      Reads from the file. Returns the buffer or None

      :param size: the maximum number of bytes to read
      :returns: a str, or None



   .. py:method:: gets(len)

      Reads a line from the input file. Returns the read line or None

      :param len: the maximum line length



   .. py:method:: writebytes(size, big_endian)

      Similar to write() but it respect the endianness

      :param buf: the str to write
      :param big_endian: endianness
      :returns: result code



   .. py:method:: write(buf)

      Writes to the file. Returns 0 or the number of bytes written

      :param buf: the str to write
      :returns: result code



   .. py:method:: puts(str: qfile_t.puts.str) -> int


   .. py:method:: size() -> int64


   .. py:method:: flush()


   .. py:method:: filename() -> PyObject *


   .. py:method:: get_byte()

      Reads a single byte from the file. Returns None if EOF or the read byte



   .. py:method:: put_byte()

      Writes a single byte to the file

      :param chr: the byte value



.. py:function:: qfclose(fp: FILE *) -> int

.. py:data:: QMOVE_CROSS_FS

.. py:data:: QMOVE_OVERWRITE

.. py:data:: QMOVE_OVR_RO

.. py:data:: qfile_t_from_fp

.. py:data:: qfile_t_from_capsule

.. py:data:: qfile_t_tmpfile


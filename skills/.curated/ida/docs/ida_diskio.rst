ida_diskio
==========

.. py:module:: ida_diskio

.. autoapi-nested-parse::

   File I/O functions for IDA.

   You should not use standard C file I/O functions in modules. Use functions from this header, pro.h and fpro.h instead.
   This file also declares a call_system() function. 
       



Attributes
----------

.. autoapisummary::

   ida_diskio.VAULT_CACHE_SUBDIR
   ida_diskio.VAULT_CACHE_FNAME
   ida_diskio.CFG_SUBDIR
   ida_diskio.IDC_SUBDIR
   ida_diskio.IDS_SUBDIR
   ida_diskio.IDP_SUBDIR
   ida_diskio.LDR_SUBDIR
   ida_diskio.SIG_SUBDIR
   ida_diskio.TIL_SUBDIR
   ida_diskio.PLG_SUBDIR
   ida_diskio.THM_SUBDIR
   ida_diskio.IDA_SUBDIR_IDP
   ida_diskio.IDA_SUBDIR_IDADIR_FIRST
   ida_diskio.IDA_SUBDIR_ONLY_EXISTING
   ida_diskio.CSIDL_APPDATA
   ida_diskio.CSIDL_LOCAL_APPDATA
   ida_diskio.CSIDL_PROGRAM_FILES
   ida_diskio.CSIDL_PROGRAM_FILES_COMMON
   ida_diskio.CSIDL_PROGRAM_FILESX86
   ida_diskio.LINPUT_NONE
   ida_diskio.LINPUT_LOCAL
   ida_diskio.LINPUT_RFILE
   ida_diskio.LINPUT_PROCMEM
   ida_diskio.LINPUT_GENERIC
   ida_diskio.LOC_CLOSE
   ida_diskio.LOC_UNMAKE
   ida_diskio.LOC_KEEP


Classes
-------

.. autoapisummary::

   ida_diskio.file_enumerator_t
   ida_diskio.ioports_fallback_t
   ida_diskio.choose_ioport_parser_t
   ida_diskio.generic_linput_t


Functions
---------

.. autoapisummary::

   ida_diskio.idadir
   ida_diskio.getsysfile
   ida_diskio.get_user_idadir
   ida_diskio.get_ida_subdirs
   ida_diskio.get_special_folder
   ida_diskio.fopenWT
   ida_diskio.fopenWB
   ida_diskio.fopenRT
   ida_diskio.fopenRB
   ida_diskio.fopenM
   ida_diskio.fopenA
   ida_diskio.read_ioports
   ida_diskio.choose_ioport_device2
   ida_diskio.qlgetz
   ida_diskio.open_linput
   ida_diskio.create_generic_linput
   ida_diskio.create_memory_linput
   ida_diskio.get_linput_type
   ida_diskio.enumerate_files
   ida_diskio.create_bytearray_linput
   ida_diskio.close_linput


Module Contents
---------------

.. py:data:: VAULT_CACHE_SUBDIR

   subdir name for cached deltas and old files


.. py:data:: VAULT_CACHE_FNAME

   to store file caches


.. py:function:: idadir(subdir: str) -> str

   Get IDA directory (if subdir==nullptr) or the specified subdirectory (see IDA subdirectories) 
           


.. py:function:: getsysfile(filename: str, subdir: str) -> str

   Search for IDA system file. This function searches for a file in:
   0. each directory specified by IDAUSR%
   1. ida directory [+ subdir]


   and returns the first match. 
           
   :param filename: name of file to search
   :param subdir: if specified, the file is looked for in the specified subdirectory of the ida directory first (see IDA subdirectories)
   :returns: nullptr if not found, otherwise a pointer to full file name.


.. py:data:: CFG_SUBDIR

.. py:data:: IDC_SUBDIR

.. py:data:: IDS_SUBDIR

.. py:data:: IDP_SUBDIR

.. py:data:: LDR_SUBDIR

.. py:data:: SIG_SUBDIR

.. py:data:: TIL_SUBDIR

.. py:data:: PLG_SUBDIR

.. py:data:: THM_SUBDIR

.. py:function:: get_user_idadir() -> str

   Get user ida related directory. 
   if $IDAUSR is defined:
      - the first element in $IDAUSR
   else
      - default user directory ($HOME/.idapro or %APPDATA%Hex-Rays/IDA Pro)


      


.. py:function:: get_ida_subdirs(subdir: str, flags: int = 0) -> qstrvec_t *

   Get list of directories in which to find a specific IDA resource (see IDA subdirectories). The order of the resulting list is as follows: 
        [$IDAUSR/subdir (0..N entries)]
        $IDADIR/subdir


           
   :param subdir: name of the resource to list (can be nullptr)
   :param flags: Subdirectory modification flags bits
   :returns: number of directories appended to 'dirs'


.. py:data:: IDA_SUBDIR_IDP

   append the processor name as a subdirectory


.. py:data:: IDA_SUBDIR_IDADIR_FIRST

   $IDADIR/subdir will be first, not last


.. py:data:: IDA_SUBDIR_ONLY_EXISTING

   only existing directories will be present


.. py:function:: get_special_folder(csidl: int) -> str

   Get a folder location by CSIDL (see Common CSIDLs). Path should be of at least MAX_PATH size 
           


.. py:data:: CSIDL_APPDATA

.. py:data:: CSIDL_LOCAL_APPDATA

.. py:data:: CSIDL_PROGRAM_FILES

.. py:data:: CSIDL_PROGRAM_FILES_COMMON

.. py:data:: CSIDL_PROGRAM_FILESX86

.. py:class:: file_enumerator_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: visit_file(file: str) -> int


.. py:function:: fopenWT(file: str) -> FILE *

.. py:function:: fopenWB(file: str) -> FILE *

.. py:function:: fopenRT(file: str) -> FILE *

.. py:function:: fopenRB(file: str) -> FILE *

.. py:function:: fopenM(file: str) -> FILE *

.. py:function:: fopenA(file: str) -> FILE *

.. py:class:: ioports_fallback_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: handle(ports: ioports_t const &, line: str) -> bool

      :param ports: i/o port definitions
      :param line: input line to parse
      :returns: success or fills ERRBUF with an error message



.. py:function:: read_ioports(ports: ioports_t *, device: str, file: str, callback: ioports_fallback_t = None) -> ssize_t

.. py:class:: choose_ioport_parser_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: parse(param: str, line: str) -> bool

      :returns: true: and fill PARAM with a displayed string
      :returns: false: and empty PARAM to skip the current device
      :returns: false: and fill PARAM with an error message



.. py:function:: choose_ioport_device2(_device: str, file: str, parse_params: choose_ioport_parser_t) -> bool

.. py:data:: LINPUT_NONE

.. py:data:: LINPUT_LOCAL

.. py:data:: LINPUT_RFILE

.. py:data:: LINPUT_PROCMEM

.. py:data:: LINPUT_GENERIC

.. py:function:: qlgetz(li: linput_t *, fpos: int64) -> str

.. py:function:: open_linput(file: str, remote: bool) -> linput_t *

.. py:class:: generic_linput_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: filesize
      :type:  uint64


   .. py:attribute:: blocksize
      :type:  int


   .. py:method:: read(off: qoff64_t, buffer: void *, nbytes: size_t) -> ssize_t


.. py:function:: create_generic_linput(gl: generic_linput_t) -> linput_t *

.. py:function:: create_memory_linput(start: ida_idaapi.ea_t, size: asize_t) -> linput_t *

.. py:function:: get_linput_type(li: linput_t *) -> linput_type_t

.. py:data:: LOC_CLOSE

   close the inner linput


.. py:data:: LOC_UNMAKE

   unmake the inner linput


.. py:data:: LOC_KEEP

   do nothing


.. py:function:: enumerate_files(path, fname, callback)

   Enumerate files in the specified directory while the callback returns 0.

   :param path: directory to enumerate files in
   :param fname: mask of file names to enumerate
   :param callback: a callable object that takes the filename as
                    its first argument and it returns 0 to continue
                    enumeration or non-zero to stop enumeration.
   :returns: tuple(code, fname) : If the callback returns non-zero, or None in case of script errors


.. py:function:: create_bytearray_linput(s: str) -> linput_t *

.. py:function:: close_linput(li: linput_t *) -> None


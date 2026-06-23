ida_srclang
===========

.. py:module:: ida_srclang

.. autoapi-nested-parse::

   Third-party compiler support.



Attributes
----------

.. autoapisummary::

   ida_srclang.SRCLANG_C
   ida_srclang.SRCLANG_CPP
   ida_srclang.SRCLANG_OBJC
   ida_srclang.SRCLANG_SWIFT
   ida_srclang.SRCLANG_GO


Functions
---------

.. autoapisummary::

   ida_srclang.select_parser_by_name
   ida_srclang.select_parser_by_srclang
   ida_srclang.get_selected_parser_name
   ida_srclang.set_parser_argv
   ida_srclang.parse_decls_for_srclang
   ida_srclang.parse_decls_with_parser_ext
   ida_srclang.get_parser_option
   ida_srclang.set_parser_option
   ida_srclang.parse_decls_with_parser


Module Contents
---------------

.. py:data:: SRCLANG_C

   C.


.. py:data:: SRCLANG_CPP

   C++.


.. py:data:: SRCLANG_OBJC

   Objective-C.


.. py:data:: SRCLANG_SWIFT

   Swift (not supported yet)


.. py:data:: SRCLANG_GO

   Golang (not supported yet)


.. py:function:: select_parser_by_name(name: str) -> bool

   Set the parser with the given name as the current parser. Pass nullptr or an empty string to select the default parser. 
           
   :returns: false if no parser was found with the given name


.. py:function:: select_parser_by_srclang(lang: srclang_t) -> bool

   Set the parser that supports the given language(s) as the current parser. The selected parser must support all languages specified by the given srclang_t. 
           
   :returns: false if no such parser was found


.. py:function:: get_selected_parser_name() -> str

   Get current parser name. 
           
   :returns: success


.. py:function:: set_parser_argv(parser_name: str, argv: str) -> int

   Set the command-line args to use for invocations of the parser with the given name 
           
   :param parser_name: name of the target parser
   :param argv: argument list
   :returns: -1: no parser was found with the given name
   :returns: -2: the operation is not supported by the given parser
   :returns: 0: success


.. py:function:: parse_decls_for_srclang(lang: srclang_t, til: til_t, input: str, is_path: bool) -> int

   Parse type declarations in the specified language 
           
   :param lang: the source language(s) expected in the input
   :param til: type library to store the types
   :param input: input source. can be a file path or decl string
   :param is_path: true if input parameter is a path to a source file, false if the input is an in-memory source snippet
   :returns: -1: no parser was found that supports the given source language(s)
   :returns: else: the number of errors encountered in the input source


.. py:function:: parse_decls_with_parser_ext(parser_name: str, til: til_t, input: str, hti_flags: int) -> int

   Parse type declarations using the parser with the specified name 
           
   :param parser_name: name of the target parser
   :param til: type library to store the types
   :param input: input source. can be a file path or decl string
   :param hti_flags: combination of Type formatting flags
   :returns: -1: no parser was found with the given name
   :returns: else: the number of errors encountered in the input source


.. py:function:: get_parser_option(parser_name: str, option_name: str) -> str

   Get option for the parser with the specified name 
           
   :param parser_name: name of the target parser
   :param option_name: parser option name
   :returns: success


.. py:function:: set_parser_option(parser_name: str, option_name: str, option_value: str) -> bool

   Set option for the parser with the specified name 
           
   :param parser_name: name of the target parser
   :param option_name: parser option name
   :param option_value: parser option value
   :returns: success


.. py:function:: parse_decls_with_parser(parser_name: str, til: til_t, input: str, is_path: bool) -> int

   Parse type declarations using the parser with the specified name 
           
   :param parser_name: name of the target parser
   :param til: type library to store the types
   :param input: input source. can be a file path or decl string
   :param is_path: true if input parameter is a path to a source file, false if the input is an in-memory source snippet
   :returns: -1: no parser was found with the given name
   :returns: else: the number of errors encountered in the input source



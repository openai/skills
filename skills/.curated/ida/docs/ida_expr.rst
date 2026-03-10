ida_expr
========

.. py:module:: ida_expr

.. autoapi-nested-parse::

   Functions that deal with C-like expressions and built-in IDC language.

   Functions marked THREAD_SAFE may be called from any thread. No simultaneous calls should be made for the same variable. We protect only global structures, individual variables must be protected manually. 
       



Attributes
----------

.. autoapisummary::

   ida_expr.IDC_LANG_EXT
   ida_expr.VARSLICE_SINGLE
   ida_expr.VREF_LOOP
   ida_expr.VREF_ONCE
   ida_expr.VREF_COPY
   ida_expr.VT_LONG
   ida_expr.VT_FLOAT
   ida_expr.VT_WILD
   ida_expr.VT_OBJ
   ida_expr.VT_FUNC
   ida_expr.VT_STR
   ida_expr.VT_PVOID
   ida_expr.VT_INT64
   ida_expr.VT_REF
   ida_expr.eExecThrow
   ida_expr.HF_DEFAULT
   ida_expr.HF_KEYWORD1
   ida_expr.HF_KEYWORD2
   ida_expr.HF_KEYWORD3
   ida_expr.HF_STRING
   ida_expr.HF_COMMENT
   ida_expr.HF_PREPROC
   ida_expr.HF_NUMBER
   ida_expr.HF_USER1
   ida_expr.HF_USER2
   ida_expr.HF_USER3
   ida_expr.HF_USER4
   ida_expr.HF_MAX
   ida_expr.CPL_DEL_MACROS
   ida_expr.CPL_USE_LABELS
   ida_expr.CPL_ONLY_SAFE
   ida_expr.EXTFUN_BASE
   ida_expr.EXTFUN_NORET
   ida_expr.EXTFUN_SAFE


Classes
-------

.. autoapisummary::

   ida_expr.idc_value_t
   ida_expr.idc_global_t
   ida_expr.highlighter_cbs_t
   ida_expr.idc_values_t


Functions
---------

.. autoapisummary::

   ida_expr.compile_idc_file
   ida_expr.compile_idc_text
   ida_expr.py_get_call_idc_func
   ida_expr.pyw_register_idc_func
   ida_expr.pyw_unregister_idc_func
   ida_expr.pyw_convert_defvals
   ida_expr.py_add_idc_func
   ida_expr.eval_expr
   ida_expr.eval_idc_expr
   ida_expr.idcv_long
   ida_expr.idcv_int64
   ida_expr.idcv_num
   ida_expr.idcv_string
   ida_expr.idcv_float
   ida_expr.idcv_object
   ida_expr.move_idcv
   ida_expr.copy_idcv
   ida_expr.deep_copy_idcv
   ida_expr.free_idcv
   ida_expr.swap_idcvs
   ida_expr.get_idcv_class_name
   ida_expr.get_idcv_attr
   ida_expr.set_idcv_attr
   ida_expr.del_idcv_attr
   ida_expr.first_idcv_attr
   ida_expr.last_idcv_attr
   ida_expr.next_idcv_attr
   ida_expr.prev_idcv_attr
   ida_expr.print_idcv
   ida_expr.get_idcv_slice
   ida_expr.set_idcv_slice
   ida_expr.add_idc_class
   ida_expr.find_idc_class
   ida_expr.deref_idcv
   ida_expr.create_idcv_ref
   ida_expr.add_idc_gvar
   ida_expr.find_idc_gvar
   ida_expr.find_idc_func
   ida_expr.set_header_path
   ida_expr.get_idc_filename
   ida_expr.exec_system_script
   ida_expr.compile_idc_snippet
   ida_expr.exec_idc_script
   ida_expr.throw_idc_exception
   ida_expr.del_idc_func
   ida_expr.add_idc_func


Module Contents
---------------

.. py:function:: compile_idc_file(nonnul_line: str) -> str

.. py:function:: compile_idc_text(nonnul_line: str) -> str

.. py:function:: py_get_call_idc_func() -> size_t

.. py:function:: pyw_register_idc_func(name: str, args: str, py_fp: PyObject *) -> size_t

.. py:function:: pyw_unregister_idc_func(ctxptr: size_t) -> bool

.. py:function:: pyw_convert_defvals(out: idc_values_t, py_seq: PyObject *) -> bool

.. py:function:: py_add_idc_func(name: str, fp_ptr: size_t, args: str, defvals: idc_values_t, flags: int) -> bool

.. py:function:: eval_expr(rv: idc_value_t, where: ida_idaapi.ea_t, line: str) -> str

   Compile and calculate an expression. 
           
   :param rv: pointer to the result
   :param where: the current linear address in the addressing space of the program being disassembled. If will be used to resolve names of local variables etc. if not applicable, then should be BADADDR.
   :param line: the expression to evaluate
   :returns: true: ok
   :returns: false: error, see errbuf


.. py:function:: eval_idc_expr(rv: idc_value_t, where: ida_idaapi.ea_t, line: str) -> str

   Same as eval_expr(), but will always use the IDC interpreter regardless of the currently installed extlang. 
           


.. py:data:: IDC_LANG_EXT

   IDC script extension.


.. py:function:: idcv_long(v: idc_value_t) -> error_t

   Convert IDC variable to a long (32/64bit) number. 
           
   :returns: v = 0 if impossible to convert to long


.. py:function:: idcv_int64(v: idc_value_t) -> error_t

   Convert IDC variable to a 64bit number. 
           
   :returns: v = 0 if impossible to convert to int64


.. py:function:: idcv_num(v: idc_value_t) -> error_t

   Convert IDC variable to a long number. 
           
   :returns: * v = 0 if IDC variable = "false" string
   * v = 1 if IDC variable = "true" string
   * v = number if IDC variable is number or string containing a number
   * eTypeConflict if IDC variable = empty string


.. py:function:: idcv_string(v: idc_value_t) -> error_t

   Convert IDC variable to a text string.


.. py:function:: idcv_float(v: idc_value_t) -> error_t

   Convert IDC variable to a floating point.


.. py:function:: idcv_object(v: idc_value_t, icls: idc_class_t const * = None) -> error_t

   Create an IDC object. The original value of 'v' is discarded (freed). 
           
   :param v: variable to hold the object. any previous value will be cleaned
   :param icls: ptr to the desired class. nullptr means "object" class this ptr must be returned by add_idc_class() or find_idc_class()
   :returns: always eOk


.. py:function:: move_idcv(dst: idc_value_t, src: idc_value_t) -> error_t

   Move 'src' to 'dst'. This function is more effective than copy_idcv since it never copies big amounts of data. 
           


.. py:function:: copy_idcv(dst: idc_value_t, src: idc_value_t) -> error_t

   Copy 'src' to 'dst'. For idc objects only a reference is copied. 
           


.. py:function:: deep_copy_idcv(dst: idc_value_t, src: idc_value_t) -> error_t

   Deep copy an IDC object. This function performs deep copy of idc objects. If 'src' is not an object, copy_idcv() will be called 
           


.. py:function:: free_idcv(v: idc_value_t) -> None

   Free storage used by VT_STR/VT_OBJ IDC variables. After this call the variable has a numeric value 0 
           


.. py:function:: swap_idcvs(v1: idc_value_t, v2: idc_value_t) -> None

   Swap 2 variables.


.. py:function:: get_idcv_class_name(obj: idc_value_t) -> str

   Retrieves the IDC object class name. 
           
   :param obj: class instance variable
   :returns: error code, eOk on success


.. py:function:: get_idcv_attr(res: idc_value_t, obj: idc_value_t, attr: str, may_use_getattr: bool = False) -> error_t

   Get an object attribute. 
           
   :param res: buffer for the attribute value
   :param obj: variable that holds an object reference. if obj is nullptr it searches global variables, then user functions
   :param attr: attribute name
   :param may_use_getattr: may call getattr functions to calculate the attribute if it does not exist
   :returns: error code, eOk on success


.. py:function:: set_idcv_attr(obj: idc_value_t, attr: str, value: idc_value_t, may_use_setattr: bool = False) -> error_t

   Set an object attribute. 
           
   :param obj: variable that holds an object reference. if obj is nullptr then it tries to modify a global variable with the attribute name
   :param attr: attribute name
   :param value: new attribute value
   :param may_use_setattr: may call setattr functions for the class
   :returns: error code, eOk on success


.. py:function:: del_idcv_attr(obj: idc_value_t, attr: str) -> error_t

   Delete an object attribute. 
           
   :param obj: variable that holds an object reference
   :param attr: attribute name
   :returns: error code, eOk on success


.. py:function:: first_idcv_attr(obj: idc_value_t) -> str

.. py:function:: last_idcv_attr(obj: idc_value_t) -> str

.. py:function:: next_idcv_attr(obj: idc_value_t, attr: str) -> str

.. py:function:: prev_idcv_attr(obj: idc_value_t, attr: str) -> str

.. py:function:: print_idcv(v: idc_value_t, name: str = None, indent: int = 0) -> str

   Get text representation of idc_value_t.


.. py:function:: get_idcv_slice(res: idc_value_t, v: idc_value_t, i1: int, i2: int, flags: int = 0) -> error_t

   Get slice. 
           
   :param res: output variable that will contain the slice
   :param v: input variable (string or object)
   :param i1: slice start index
   :param i2: slice end index (excluded)
   :param flags: IDC variable slice flags or 0
   :returns: eOk if success


.. py:data:: VARSLICE_SINGLE

   return single index (i2 is ignored)


.. py:function:: set_idcv_slice(v: idc_value_t, i1: int, i2: int, _in: idc_value_t, flags: int = 0) -> error_t

   Set slice. 
           
   :param v: variable to modify (string or object)
   :param i1: slice start index
   :param i2: slice end index (excluded)
   :param flags: IDC variable slice flags or 0
   :returns: eOk on success


.. py:function:: add_idc_class(name: str, super: idc_class_t const * = None) -> idc_class_t *

   Create a new IDC class. 
           
   :param name: name of the new class
   :param super: the base class for the new class. if the new class is not based on any other class, pass nullptr
   :returns: pointer to the created class. If such a class already exists, a pointer to it will be returned. Pointers to other existing classes may be invalidated by this call.


.. py:function:: find_idc_class(name: str) -> idc_class_t *

   Find an existing IDC class by its name. 
           
   :param name: name of the class
   :returns: pointer to the class or nullptr. The returned pointer is valid until a new call to add_idc_class()


.. py:function:: deref_idcv(v: idc_value_t, vref_flags: int) -> idc_value_t *

   Dereference a VT_REF variable. 
           
   :param v: variable to dereference
   :param vref_flags: Dereference IDC variable flags
   :returns: pointer to the dereference result or nullptr. If returns nullptr, qerrno is set to eExecBadRef "Illegal variable reference"


.. py:data:: VREF_LOOP

   dereference until we get a non VT_REF


.. py:data:: VREF_ONCE

   dereference only once, do not loop


.. py:data:: VREF_COPY

   copy the result to the input var (v)


.. py:function:: create_idcv_ref(ref: idc_value_t, v: idc_value_t) -> bool

   Create a variable reference. Currently only references to global variables can be created. 
           
   :param ref: ptr to the result
   :param v: variable to reference
   :returns: success


.. py:function:: add_idc_gvar(name: str) -> idc_value_t *

   Add global IDC variable. 
           
   :param name: name of the global variable
   :returns: pointer to the created variable or existing variable. NB: the returned pointer is valid until a new global var is added.


.. py:function:: find_idc_gvar(name: str) -> idc_value_t *

   Find an existing global IDC variable by its name. 
           
   :param name: name of the global variable
   :returns: pointer to the variable or nullptr. NB: the returned pointer is valid until a new global var is added. FIXME: it is difficult to use this function in a thread safe manner


.. py:class:: idc_value_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: vtype
      :type:  char

      IDC value types



   .. py:attribute:: num
      :type:  int

      VT_LONG



   .. py:attribute:: e
      :type:  fpvalue_t

      VT_FLOAT



   .. py:attribute:: obj
      :type:  idc_object_t *


   .. py:attribute:: funcidx
      :type:  int

      VT_FUNC



   .. py:attribute:: pvoid
      :type:  void *

      VT_PVOID



   .. py:attribute:: i64
      :type:  int64

      VT_INT64



   .. py:attribute:: reserve
      :type:  uchar [sizeof(qstring)]

      VT_STR.



   .. py:method:: clear() -> None

      See free_idcv()



   .. py:method:: qstr() -> str

      VT_STR



   .. py:method:: c_str() -> str

      VT_STR



   .. py:method:: u_str() -> uchar const *

      VT_STR



   .. py:method:: swap(v: idc_value_t) -> None

      Set this = r and v = this.



   .. py:method:: is_zero() -> bool

      Does value represent the integer 0?



   .. py:method:: is_integral() -> bool

      Does value represent a whole number? 
              



   .. py:method:: is_convertible() -> bool

      Convertible types are VT_LONG, VT_FLOAT, VT_INT64, and VT_STR.



   .. py:method:: create_empty_string() -> None


   .. py:method:: set_string(*args) -> None


   .. py:method:: set_long(v: int) -> None


   .. py:method:: set_pvoid(p: void *) -> None


   .. py:method:: set_int64(v: int64) -> None


   .. py:method:: set_float(f: fpvalue_t const &) -> None


   .. py:attribute:: str


.. py:data:: VT_LONG

   Integer (see idc_value_t::num)


.. py:data:: VT_FLOAT

   Floating point (see idc_value_t::e)


.. py:data:: VT_WILD

   Function with arbitrary number of arguments. The actual number of arguments will be passed in idc_value_t::num. This value should not be used for idc_value_t. 
           


.. py:data:: VT_OBJ

   Object (see idc_value_t::obj)


.. py:data:: VT_FUNC

   Function (see idc_value_t::funcidx)


.. py:data:: VT_STR

   String (see qstr() and similar functions)


.. py:data:: VT_PVOID

   void *


.. py:data:: VT_INT64

   i64


.. py:data:: VT_REF

   Reference.


.. py:class:: idc_global_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: name
      :type:  str


   .. py:attribute:: value
      :type:  idc_value_t


.. py:data:: eExecThrow

   See return value of idc_func_t.


.. py:function:: find_idc_func(prefix: str, n: int = 0) -> str

.. py:data:: HF_DEFAULT

.. py:data:: HF_KEYWORD1

.. py:data:: HF_KEYWORD2

.. py:data:: HF_KEYWORD3

.. py:data:: HF_STRING

.. py:data:: HF_COMMENT

.. py:data:: HF_PREPROC

.. py:data:: HF_NUMBER

.. py:data:: HF_USER1

.. py:data:: HF_USER2

.. py:data:: HF_USER3

.. py:data:: HF_USER4

.. py:data:: HF_MAX

.. py:class:: highlighter_cbs_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: set_style(arg0: int, arg1: int, arg2: syntax_highlight_style) -> None


   .. py:method:: prev_block_state() -> int


   .. py:method:: cur_block_state() -> int


   .. py:method:: set_block_state(arg0: int) -> None


.. py:function:: set_header_path(path: str, add: bool) -> bool

   Set or append a header path. IDA looks for the include files in the appended header paths, then in the ida executable directory. 
           
   :param path: list of directories to add (separated by ';') may be nullptr, in this case nothing is added
   :param add: true: append. false: remove old paths.
   :returns: true: success
   :returns: false: no memory


.. py:function:: get_idc_filename(file: str) -> str

   Get full name of IDC file name. Search for file in list of include directories, IDCPATH directory and system directories. 
           
   :param file: file name without full path
   :returns: nullptr is file not found. otherwise returns pointer to buf


.. py:function:: exec_system_script(file: str, complain_if_no_file: bool = True) -> bool

   Compile and execute "main" function from system file. 
           
   :param file: file name with IDC function(s). The file will be searched using get_idc_filename().
   :param complain_if_no_file: * 1: display warning if the file is not found
   * 0: don't complain if file doesn't exist
   :returns: 1: ok, file is compiled and executed
   :returns: 0: failure, compilation or execution error, warning is displayed


.. py:data:: CPL_DEL_MACROS

   delete macros at the end of compilation


.. py:data:: CPL_USE_LABELS

   allow program labels in the script


.. py:data:: CPL_ONLY_SAFE

   allow calls of only thread-safe functions


.. py:function:: compile_idc_snippet(func: str, text: str, resolver: idc_resolver_t * = None, only_safe_funcs: bool = False) -> str

   Compile text with IDC statements. 
           
   :param func: name of the function to create out of the snippet
   :param text: text to compile
   :param resolver: callback object to get values of undefined variables This object will be called if IDC function contains references to undefined variables. May be nullptr.
   :param only_safe_funcs: if true, any calls to functions without EXTFUN_SAFE flag will lead to a compilation error.
   :returns: true: ok
   :returns: false: error, see errbuf


.. py:function:: exec_idc_script(result: idc_value_t, path: str, func: str, args: idc_value_t, argsnum: size_t) -> str

   Compile and execute IDC function(s) from file. 
           
   :param result: ptr to idc_value_t to hold result of the function. If execution fails, this variable will contain the exception information. You may pass nullptr if you are not interested in the returned value.
   :param path: text file containing text of IDC functions
   :param func: function name to execute
   :param args: array of parameters
   :param argsnum: number of parameters to pass to 'fname' This number should be equal to number of parameters the function expects.
   :returns: true: ok
   :returns: false: error, see errbuf


.. py:function:: throw_idc_exception(r: idc_value_t, desc: str) -> error_t

   Create an idc execution exception object. This helper function can be used to return an exception from C++ code to IDC. In other words this function can be called from idc_func_t() callbacks. Sample usage: if ( !ok ) return throw_idc_exception(r, "detailed error msg"); 
           
   :param r: object to hold the exception object
   :param desc: exception description
   :returns: eExecThrow


.. py:class:: idc_values_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> idc_value_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> idc_value_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: idc_values_t) -> None


   .. py:method:: extract() -> idc_value_t *


   .. py:method:: inject(s: idc_value_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< idc_value_t >::const_iterator


   .. py:method:: end(*args) -> qvector< idc_value_t >::const_iterator


   .. py:method:: insert(it: idc_value_t, x: idc_value_t) -> qvector< idc_value_t >::iterator


   .. py:method:: erase(*args) -> qvector< idc_value_t >::iterator


   .. py:method:: append(x: idc_value_t) -> None


   .. py:method:: extend(x: idc_values_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:data:: EXTFUN_BASE
   :value: 1


   requires open database.


.. py:data:: EXTFUN_NORET
   :value: 2


   does not return. the interpreter may clean up its state before calling it. 
           


.. py:data:: EXTFUN_SAFE
   :value: 4


   thread safe function. may be called from any thread. 
           


.. py:function:: del_idc_func(name)

   Delete an IDC function 
           


.. py:function:: add_idc_func(name, fp, args, defvals=(), flags=0)

   Add an IDC function. This function does not modify the predefined kernel functions. Example: 
        error_t idaapi myfunc5(idc_value_t *argv, idc_value_t *res)
       
         msg("myfunc is called with arg0=%a and arg1=%s\n", argv[0].num, argv[1].str);
         res->num = 5;     // let's return 5
         return eOk;
       
        const char myfunc5_args[] = { VT_LONG, VT_STR, 0 };
        const ext_idcfunc_t myfunc_desc = { "MyFunc5", myfunc5, myfunc5_args, nullptr, 0, EXTFUN_BASE };
       
        after this:
       
       
        there is a new IDC function which can be called like this:
        "test");


           
   :returns: success



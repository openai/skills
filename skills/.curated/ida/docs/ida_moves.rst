ida_moves
=========

.. py:module:: ida_moves


Attributes
----------

.. autoapisummary::

   ida_moves.LSEF_PLACE
   ida_moves.LSEF_RINFO
   ida_moves.LSEF_PTYPE
   ida_moves.LSEF_ALL
   ida_moves.UNHID_SEGM
   ida_moves.UNHID_FUNC
   ida_moves.UNHID_RANGE
   ida_moves.DEFAULT_CURSOR_Y
   ida_moves.DEFAULT_LNNUM
   ida_moves.CURLOC_LIST
   ida_moves.MAX_MARK_SLOT
   ida_moves.LHF_HISTORY_DISABLED
   ida_moves.BOOKMARKS_PROMPT_WITH_HINT_PREFIX
   ida_moves.bookmarks_t_erase
   ida_moves.bookmarks_t_find_index
   ida_moves.bookmarks_t_get
   ida_moves.bookmarks_t_get_desc
   ida_moves.bookmarks_t_get_dirtree_id
   ida_moves.bookmarks_t_mark
   ida_moves.bookmarks_t_size


Classes
-------

.. autoapisummary::

   ida_moves.segm_move_info_vec_t
   ida_moves.graph_location_info_t
   ida_moves.segm_move_info_t
   ida_moves.segm_move_infos_t
   ida_moves.renderer_info_pos_t
   ida_moves.renderer_info_t
   ida_moves.lochist_entry_t
   ida_moves.navstack_entry_t
   ida_moves.navstack_t
   ida_moves.bookmarks_t


Module Contents
---------------

.. py:class:: segm_move_info_vec_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: push_back(*args) -> segm_move_info_t &


   .. py:method:: pop_back() -> None


   .. py:method:: size() -> size_t


   .. py:method:: empty() -> bool


   .. py:method:: at(_idx: size_t) -> segm_move_info_t const &


   .. py:method:: qclear() -> None


   .. py:method:: clear() -> None


   .. py:method:: resize(*args) -> None


   .. py:method:: grow(*args) -> None


   .. py:method:: capacity() -> size_t


   .. py:method:: reserve(cnt: size_t) -> None


   .. py:method:: truncate() -> None


   .. py:method:: swap(r: segm_move_info_vec_t) -> None


   .. py:method:: extract() -> segm_move_info_t *


   .. py:method:: inject(s: segm_move_info_t, len: size_t) -> None


   .. py:method:: begin(*args) -> qvector< segm_move_info_t >::const_iterator


   .. py:method:: end(*args) -> qvector< segm_move_info_t >::const_iterator


   .. py:method:: insert(it: segm_move_info_t, x: segm_move_info_t) -> qvector< segm_move_info_t >::iterator


   .. py:method:: erase(*args) -> qvector< segm_move_info_t >::iterator


   .. py:method:: find(*args) -> qvector< segm_move_info_t >::const_iterator


   .. py:method:: has(x: segm_move_info_t) -> bool


   .. py:method:: add_unique(x: segm_move_info_t) -> bool


   .. py:method:: append(x: segm_move_info_t) -> None


   .. py:method:: extend(x: segm_move_info_vec_t) -> None


   .. py:attribute:: front


   .. py:attribute:: back


.. py:class:: graph_location_info_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: zoom
      :type:  double


   .. py:attribute:: orgx
      :type:  double


   .. py:attribute:: orgy
      :type:  double


.. py:class:: segm_move_info_t(_from: ida_idaapi.ea_t = 0, _to: ida_idaapi.ea_t = 0, _sz: size_t = 0)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: to
      :type:  ida_idaapi.ea_t


   .. py:attribute:: size
      :type:  size_t


.. py:class:: segm_move_infos_t

   Bases: :py:obj:`segm_move_info_vec_t`


   .. py:attribute:: thisown


   .. py:method:: find(ea: ida_idaapi.ea_t) -> segm_move_info_t const *


.. py:class:: renderer_info_pos_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: node
      :type:  int


   .. py:attribute:: cx
      :type:  short


   .. py:attribute:: cy
      :type:  short


.. py:class:: renderer_info_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: gli
      :type:  graph_location_info_t


   .. py:attribute:: pos
      :type:  renderer_info_t::pos_t


   .. py:attribute:: rtype
      :type:  tcc_renderer_type_t


.. py:data:: LSEF_PLACE

.. py:data:: LSEF_RINFO

.. py:data:: LSEF_PTYPE

.. py:data:: LSEF_ALL

.. py:class:: lochist_entry_t(*args)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: rinfo
      :type:  renderer_info_t


   .. py:attribute:: plce
      :type:  place_t *


   .. py:method:: renderer_info() -> renderer_info_t &


   .. py:method:: place() -> place_t *


   .. py:method:: set_place(p: place_t) -> None


   .. py:method:: is_valid() -> bool


   .. py:method:: acquire_place(in_p: place_t) -> None


.. py:class:: navstack_entry_t(*args)

   Bases: :py:obj:`lochist_entry_t`


   .. py:attribute:: thisown


   .. py:attribute:: widget_id
      :type:  str


   .. py:attribute:: ud_str
      :type:  str


.. py:data:: UNHID_SEGM

   unhid a segment at 'target'


.. py:data:: UNHID_FUNC

   unhid a function at 'target'


.. py:data:: UNHID_RANGE

   unhid an range at 'target'


.. py:data:: DEFAULT_CURSOR_Y

.. py:data:: DEFAULT_LNNUM

.. py:data:: CURLOC_LIST

.. py:data:: MAX_MARK_SLOT

.. py:class:: navstack_t

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:attribute:: flags
      :type:  int


   .. py:method:: is_history_enabled() -> bool


   .. py:method:: init(defpos: navstack_entry_t, stream_name: str, _flags: int) -> bool


   .. py:method:: perform_move(stream_name: str, source_stream_name: str, widget_id: str, move_stack: bool) -> bool
      :staticmethod:



   .. py:method:: netcode() -> nodeidx_t


   .. py:method:: set_current(e: navstack_entry_t, in_charge: bool) -> None


   .. py:method:: get_current(out: navstack_entry_t, widget_id: str) -> bool


   .. py:method:: get_all_current(out: navstack_entry_vec_t *) -> None


   .. py:method:: stack_jump(try_to_unhide: bool, e: navstack_entry_t) -> None


   .. py:method:: stack_index() -> int


   .. py:method:: stack_seek(out: navstack_entry_t, index: int, try_to_unhide: bool) -> bool


   .. py:method:: stack_forward(out: navstack_entry_t, cnt: int, try_to_unhide: bool) -> bool


   .. py:method:: stack_back(out: navstack_entry_t, cnt: int, try_to_unhide: bool) -> bool


   .. py:method:: stack_nav(out: navstack_entry_t, forward: bool, cnt: int, try_to_unhide: bool) -> bool


   .. py:method:: stack_clear(new_tip: navstack_entry_t) -> None


   .. py:method:: set_stack_entry(index: int, e: navstack_entry_t) -> None


   .. py:method:: get_stack_entry(out: navstack_entry_t, index: int) -> bool


   .. py:method:: get_current_stack_entry(out: navstack_entry_t) -> bool


   .. py:method:: stack_size() -> int


.. py:data:: LHF_HISTORY_DISABLED

.. py:class:: bookmarks_t(*args, **kwargs)

   Bases: :py:obj:`object`


   .. py:attribute:: thisown


   .. py:method:: mark(e: lochist_entry_t, index: int, title: str, desc: str, ud: void *) -> int
      :staticmethod:



   .. py:method:: get_desc(e: lochist_entry_t, index: int, ud: void *) -> str
      :staticmethod:



   .. py:method:: find_index(e: lochist_entry_t, ud: void *) -> int
      :staticmethod:



   .. py:method:: size(e: lochist_entry_t, ud: void *) -> int
      :staticmethod:



   .. py:method:: erase(e: lochist_entry_t, index: int, ud: void *) -> bool
      :staticmethod:



   .. py:method:: get_dirtree_id(e: lochist_entry_t, ud: void *) -> dirtree_id_t
      :staticmethod:



   .. py:method:: get(out: lochist_entry_t, _index: int, ud: void *) -> PyObject *
      :staticmethod:



   .. py:attribute:: widget


   .. py:attribute:: userdata


   .. py:attribute:: template


.. py:data:: BOOKMARKS_PROMPT_WITH_HINT_PREFIX

.. py:data:: bookmarks_t_erase

.. py:data:: bookmarks_t_find_index

.. py:data:: bookmarks_t_get

.. py:data:: bookmarks_t_get_desc

.. py:data:: bookmarks_t_get_dirtree_id

.. py:data:: bookmarks_t_mark

.. py:data:: bookmarks_t_size


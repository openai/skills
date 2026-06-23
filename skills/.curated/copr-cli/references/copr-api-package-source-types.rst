Package Source Type
===================

Read more about source types in the
`User Documentation <https://docs.pagure.org/copr.copr/user_documentation.html#build-source-types>`__.


SCM
---

Parameters when ``source_type=scm`` is used.
See `User Documentation <https://docs.pagure.org/copr.copr/user_documentation.html#scm>`__ for more information.

=====================  ==================== ===============
Field                  Type                 Description
=====================  ==================== ===============
clone_url              str
committish             str
subdirectory           str
spec                   str
scm_type               str                  "git", "svn"
source_build_method    str                  See `User documentation <https://docs.pagure.org/copr.copr/user_documentation.html#scm>`__ for more info
=====================  ==================== ===============


Rubygems
--------

Parameters when ``source_type=rubygems`` is used.
See `User Documentation <https://docs.pagure.org/copr.copr/user_documentation.html#rubygems>`__ for more information.

==================  ==================== ===============
Field               Type                 Description
==================  ==================== ===============
gem_name            str
==================  ==================== ===============


PyPI
----

Parameters when ``source_type=pypi`` is used.
See `User Documentation <https://docs.pagure.org/copr.copr/user_documentation.html#pypi>`__ for more information.

=====================  ==================== ===============
Field                  Type                 Description
=====================  ==================== ===============
pypi_package_name      str
pypi_package_version   str
spec_template          str
python_versions        list of int
=====================  ==================== ===============


Custom
------

Parameters when ``source_type=custom`` is used.
See `User Documentation <https://docs.pagure.org/copr.copr/custom_source_method.html#custom-source-method>`__ for more information.

=====================  ==================== ===============
Field                  Type                 Description
=====================  ==================== ===============
script                 str
builddeps              str
resultdir              str
chroot                 str
=====================  ==================== ===============


Example Usage
-------------

.. code-block:: python

    client.package_proxy.add("@copr", "foo", "mypackage",
                             source_type="rubygems",
                             source={"gem_name": "mygem"})

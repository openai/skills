Client version 3
================

This documentation describes the third version of python Copr client, which officially supports APIv3. This version
addresses the problems that we had with previous versions and therefore obsoletes them.

Operations are separated among multiple proxy classes. All methods are just tiny wrappers around API endpoints. When
a method is successful, it returns Munch with data as a result. Otherwise, an exception is raised.


Example usage
-------------

.. code-block:: python

    from copr.v3 import Client

    # Create an API client from config file
    client = Client.create_from_config_file()

    # Create a new project
    chroots = ["fedora-rawhide-x86_64", "fedora-rawhide-i386"]
    client.project_proxy.add("@copr", "foo", chroots, description="Some desc")

    # Build a package
    url = "http://foo.ex/bar.src.rpm"
    build = client.build_proxy.create_from_url("@copr", "foo", url)
    print(build.id)


Quick overview
--------------

.. toctree::
    :maxdepth: 1

    client_v3/client_initialization.rst
    client_v3/data_structures.rst
    client_v3/error_handling.rst
    client_v3/pagination.rst
    client_v3/utilities.rst
    client_v3/working_with_proxies_directly.rst


Resources info
--------------

.. toctree::
    :maxdepth: 2

    client_v3/proxies.rst


Parameters
----------

.. toctree::
    :maxdepth: 1

    client_v3/build_options.rst
    client_v3/package_source_types.rst

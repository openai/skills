Build Options
=============

When submitting a new build, it is possible to specify some options in ``buildopts`` parameter.
Those are common for all build methods.

==================  ==================== ===============
Field               Type                 Description
==================  ==================== ===============
timeout             int                  build timeout
chroots             list of strings      build only for given chroots
background          bool                 mark the build as a background job
progress_callback   callable             function that receives a ``MultipartEncoderMonitor`` instance for each chunck of uploaded data
bootstrap           string               configure the Mock's bootstrap feature for this build, possible values are
                                         ``untouched`` (the default, project/chroot configuration is used) , ``default``
                                         (the mock-core-configs default is used), ``image`` (the default image is used
                                         to initialize bootstrap), ``on`` and ``off``
with_build_id       int                  put the new build into a build batch toghether with the specified build ID
after_build_id      int                  put the new build into a new build batch, and process it once the batch with
                                         the specified build ID is processed
==================  ==================== ===============


Example usage
-------------

.. code-block:: python

    url = "http://foo.ex/baz.src.rpm"
    client.build_proxy.create_from_url(url, buildopts={
        "chroots": ["fedora-rawhide-x86_64"],
        "background": True,
    })



Conf File
=========

You can enter API keys and set preferences in the file ``isbntools.conf`` in your
``$HOME\.isbntools`` directory (UNIX). For Windows, you should look at
``%APPDATA%/isbntools/isbntools.conf``.
(**create these, directory and file, if don't exist**). The file should look like:


.. code-block:: bash

    [SYS]
    SOCKETS_TIMEOUT=15
    THREADS_TIMEOUT=12

    [SERVICES]
    DEFAULT_SERVICE=merge
    VIAS_MERGE=parallel
    ISBNDB_API_KEY=your_api_key_here_or_DELETEME


The values are self-explanatory!


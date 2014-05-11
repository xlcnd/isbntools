
isbndb Plugin
=============


Is a metadata provider that uses the service **isbndb.com**. It is installed by default,
but the user **must** supply an **API KEY**.


Usage
^^^^^

This plugin adds a new option to ``isbn_meta``:


.. code-block:: bash

    $ isbn_meta ISBN isbndb [bibtex|msword|endnote|refworks|json] [YOUR_APIKEY_TO_SERVICE]


You can get an API key for the *isbndb.com service* here_.

The output can be formatted as ``bibtex``, ``msword``, ``endnote``, ``refworks`` or
``json`` (BibJSON) bibliographic formats.

You can access it programatically:

.. code-block:: python

    from isbntools.contrib.plugins.isbndb import query as q_isbndb
    ...


Conf File
^^^^^^^^^

You can enter API keys and set preferences in the file ``isbntools.conf`` in your
``$HOME\.isbntools`` directory (UNIX). For Windows, you should look at
``%APPDATA%/isbntools/isbntools.conf``
(**create these, directory and file, if don't exist**). The file should look like:


.. code-block:: bash

    [SYS]
    SOCKETS_TIMEOUT=15
    THREADS_TIMEOUT=12

    [SERVICES]
    DEFAULT_SERVICE=merge
    VIAS_MERGE=serial
    ISBNDB_API_KEY=yOuRshERe

    [PLUGINS]
    isbndb=isbndb.py


The values are self-explanatory!


    **NOTE** If you are running ``isbntools`` inside a virtual environment, the
    ``isbntools.conf`` file will be at the root of the environment.


.. _here: http://isbndb.com/api/v2/docs


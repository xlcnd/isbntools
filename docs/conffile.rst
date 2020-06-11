

Conf File
=========

You can enter API keys and set preferences in the file ``isbntools.conf`` in your
``$HOME/.isbntools`` directory (UNIX). For Windows, you should look at
``%APPDATA%/isbntools/isbntools.conf``
(**create these, directory and file, if don't exist**  [Now just enter ``isbn_conf make``]).
The file should look like:

.. code-block:: bash

    [MISC]
    REN_FORMAT={firstAuthorLastName}{year}_{title}_{isbn}
    DEBUG=False

    [SYS]
    URLOPEN_TIMEOUT=10
    THREADS_TIMEOUT=12
    LOAD_METADATA_PLUGINS=True
    LOAD_FORMATTER_PLUGINS=True

    [SERVICES]
    DEFAULT_SERVICE=goob
    VIAS_MERGE=parallel


The values are self-explanatory!


    **NOTE** If you are running ``isbntools`` inside a virtual environment, the
    ``isbntools.conf`` file will be inside folder ``isbntools``
    at the root of the environment.

The easier way to manipulate these files is by using the script ``isbn_conf``.
At a terminal enter:

.. code-block:: bash

   $ isbn_conf show

to see the current conf file.

This script has many options that allow a controlled editing of the conf file.
Just enter ``isbn_conf`` for help.

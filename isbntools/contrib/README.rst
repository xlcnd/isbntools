The ``contrib`` directory contains plugins (metadata service providers) and 
modules (anything that is not a plugin),
which are not part of the core functionality of ``isbntools``.

This is the prefered place to put *your* contributions to the project.

You have two possibilities:

1. Write your code in a folder inside ``modules`` or in **one** file inside ``plugins`` and submit 
   a pull request to the project. Your code must be pure python, and run in py26, py27, py33, py34 and pypy,
   with **no** external dependencies. If approved will be installed with the main library. 
   **You don't have to write the install script**!  

2. Write your code using the namespace ``isbntools.contrib`` as prefix and call your package 
   ``isbntools.contrib.yourpackagename``, then upload it to **pypi**. You will have to write the
   install script. You can **download a template for a plugin** here_.

   Note that to hook up your code you need to register it in the ``isbntools.conf`` file. 
   This is **not** a system file, but is usually in the home directory of the user (or at the root
   of the virtual environmnent).

   This poses an extra difficulty when the user installs your package with ``sudo pip install ...``!
   Take a look at the setup_ file for the main library and at the methods of ``isbntools.conf`` for editing 
   the conf file.

   Another way to hook up the code (*just for the case of plugins*) is to use setuptools's 'entry_points'. **See
   the template above for an example**.



.. _setup: https://github.com/xlcnd/isbntools/blob/dev/setup.py

.. _here: https://github.com/xlcnd/isbntools/raw/dev/PLUGIN.zip

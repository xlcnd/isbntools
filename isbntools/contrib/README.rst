The ``contrib`` directory contains modules (extra functionality, except new 
metadata providers and formatters) and 
apps (console scripts),
which are not part of the core functionality of ``isbntools``.

This is the prefered place to put *your* contributions to the project.

You have three possibilities:

1. Write your code in a folder inside ``modules`` and submit 
   a pull request to the project (dev branch). Your code must be pure python, and run in 
   py26, py27, py33, py34, py35, pypy and pypy3,
   with **no** external dependencies. If approved will be installed with the main package. 
   **You don't have to write the install script**!  

2. Write your code using the namespace ``isbntools.contrib.modules`` as prefix and call your package 
   ``isbntools.contrib.modules.yourpackagename``, then upload it to **pypi**. You will have to write the
   install script.

   Note that to hook up your code you *usually* need to register it in the ``isbntools.conf`` file. 
   This is **not** a system file, but is usually in the home directory of the user (or at the root
   of the virtual environmnent). Use the methods of ``isbntools.conf`` 
   for editing the conf file (see_) [probably ``reg_mod`` thats all you need!].

   The package datafolder_ could be useful too.


3. If the functionality of your module is exposed by a console script, put that script inside the folder ``apps``
   and use *entry_points* 'console_scripts' (take a look at setup_). The (entry_points) name of the script 
   must be something like ``isbn_myscript`` (prefixed by 'isbn\_'). 


   
  **NOTE**
  For new metadata providers and new formatters use **isbnlib plugins**.




.. _initapp: https://github.com/xlcnd/isbntools/blob/dev/isbntools/_initapp.py

.. _setup: https://github.com/xlcnd/isbntools/blob/dev/setup.py#L164

.. _see: https://github.com/xlcnd/isbntools/blob/dev/isbntools/_conf.py

.. _datafolder: https://pypi.python.org/pypi/datafolder

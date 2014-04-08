
.. image:: https://pypip.in/d/isbntools/badge.png
    :target: https://pypi.python.org/pypi/isbntools/
    :alt: Downloads

.. image:: https://pypip.in/v/isbntools/badge.png
    :target: https://pypi.python.org/pypi/isbntools/
    :alt: Latest Version

.. image:: https://pypip.in/format/isbntools/badge.png
    :target: https://pypi.python.org/pypi/isbntools/
    :alt: Download format

.. image:: https://pypip.in/license/isbntools/badge.png
    :target: https://pypi.python.org/pypi/isbntools/
    :alt: License

.. image:: https://travis-ci.org/xlcnd/isbntools.png?branch=v3.0.1
    :target: https://travis-ci.org/xlcnd/isbntools
    :alt: Built Status



Info
====

``isbntools`` provides several useful methods and functions
to validate, clean, transform, hyphenate and
get metadata for ISBN strings.

Typical usage (as library):

.. code-block:: python

    #!/usr/bin/env python
    import isbntools
    ...

**For the end user** several scripts are provided to use **from the command line**:

.. code-block:: bash

    $ to_isbn10 ISBN13

transforms an ISBN13 number to ISBN10.

.. code-block:: bash

    $ to_isbn13 ISBN10

transforms an ISBN10 number to ISBN13.

.. code-block:: bash

    $ isbn_info ISBN

gives you the *group identifier* of the ISBN.

.. code-block:: bash

    $ isbn_mask ISBN

*masks* (hyphenate) an ISBN (split it by identifiers).

.. code-block:: bash

    $ isbn_meta ISBN [wcat|goob|openl|isbndb|merge] [bibtex|msword|endnote|refworks] [YOUR_APIKEY_TO_SERVICE]

gives you the main metadata associated with the ISBN, ``wcat`` uses **worldcat.org**
(**no key is needed**), ``goob`` uses the **Google Books service** (**no key is needed**),
``isbndb`` uses the **isbndb.com** service (**an api key is needed**),
``openl`` uses the **OpenLibrary.org** api (**no key is needed**), ``merge`` uses
a mergeded record of ``wcat`` and ``goob`` records (**no key is needed**) and
**is the default option** (you only have to enter, e.g. ``isbn_meta 9780321534965``).
You can get an API key for the *isbndb.com service* here_.  You can enter API keys and 
set preferences in the file ``isbntools.conf`` in your
``$HOME\.isbntools`` directory (UNIX). For Windows, you should look at
``%APPDATA%/isbntools/isbntools.conf``. The output can be formated as ``bibtex``, 
``msword``, ``endnote`` or ``refworks`` bibliographic formats.


.. code-block:: bash

    $ isbn_editions ISBN

gives the collection of ISBNs that represent a given book (uses worldcat.org).

.. code-block:: bash

    $ isbn_validate ISBN

validates ISBN10 and ISBN13.

.. code-block:: bash

    $ ... | isbn_stdin_validate

to use with *posix pipes* (e.g. ``cat FILE_WITH_ISBNs | isbn_stdin_validate``).

.. code-block:: bash

    $ isbn_from_words "words from title and author name"

a *fuzzy* script that returns the *most probable* ISBN from a set of words!
(You can verify the result with ``isbn_meta``)!

.. code-block:: bash

    $ isbntools

writes version and copyright notice and **checks if there are updates**.

Many more scripts could be written with the ``isbntools`` library,
using the methods for extraction, cleaning, validation and standardization of ISBNs.

Just for fun, suppose I want the *most spoken about* book with certain words in his title.
For a *quick-and-dirty solution*, enter the following code in a file
and save it as ``isbn_tmsa_book.py``.

.. code-block:: python

    #!/usr/bin/env python
    import sys
    from isbntools import *

    query = sys.argv[1].replace(' ', '+')
    isbn = isbn_from_words(query)

    print("The ISBN of the most `spoken-about` book with this title is %s" % isbn)
    print("")
    print("... and the book is:")
    print("")
    print((meta(isbn)))

Then in a command line (in the same directory):

.. code-block:: bash

    $ python isbn_tmsa_book.py 'noise'

In my case I get::


    The ISBN of the most `spoken-about` book with this title is 9780143105985

    ... and the book is:

    {'Publisher': u'Penguin Books', 'Language': u'eng', 'Title': u'White noise',
    'Year': u'2009', 'ISBN-13': '9780143105985', 'Authors': u'Don DeLillo ;
    introduction by Richard Powers.'}


Have fun!


Install
=======

From the command line enter (in some cases you have to preced the
command by ``sudo``):


.. code-block:: bash

    $ pip install isbntools

or:

.. code-block:: bash

    $ easy_install isbntools

or:

.. code-block:: bash

    $ pip install isbntools-3.0.1.tar.gz

(first you have to download the file!)

You should check if the install was successful, by enter:

.. code-block:: bash

    $ isbntools


Windows (NEW)
-------------

    **If you are on a Windows system and the scripts don't work**, here are some help_ **or**
    you can download a standalone_ version that **doesn't need python** and gives you
    access to the scripts. However, doesn't support add-ins or customization!

    **Intructions**:
    1. unzip the file and put the file ``isbn.exe`` in a folder.
    2. go to that folder and open a command line.
    3. run ``isbn help`` to get further instructions.



For Devs
========

In the namespace ``isbntools`` you have access to the core methods:
``is_isbn10``, ``is_isbn13``, ``to_isbn10``, ``to_isbn13``, ``canonical``,
``clean``, ``notisbn``, ``get_isbnlike``, ``get_canonical_isbn``, ``mask``,
``meta``, ``info``, ``editions``, and ``isbn_from_words``.

You can extend the lib by using the classes and functions exposed in
namespace ``isbntools.dev``, namely:

* ``WEBService`` a class that handles the access to web
  services (just by passing an url) and supports ``gzip``.
  You can subclass it to extend the functionality... but
  probably you don't need to use it! It is used in the next class.

* ``WEBQuery`` a class that uses ``WEBService`` to retrive and parse
  data from a web service. You can build a new provider of metadata
  by subclassing this class. The following classes do that
  (by using the *call pattern*). His main methods allow passing custom
  functions (*handlers*) that specialize them to specific needs
  (``data_checker`` and ``parser``).

* ``GOOBQuery`` a class that retrives and parses book metadata,
  using **Google Books API** (you only have to provide an ISBN).
  The main features can be implemented by a call to ``goob.query`` function!

* ``WCATQuery`` a class that retrives and parses book metadata,
  using the **worldcat.org xisbn service** (you only have to provide an ISBN).
  The main features can be implemented by a call to ``wcat.query`` function!

* ``WCATEdQuery`` a class that retrives and parses collections of ISBNs related
  with a given book, using the **worldcat.org xisbn service**
  (you only have to provide an ISBN).
  The main features can be implemented by a call to ``wcated.query`` function!

* ``ISBNDBQuery`` a class that retrives and parses book metadata,
  using the **isbndb.org service**. However you have to provide an **API key** (in the
  command line you can enter ``isbn_meta 9780321534965 isbndb YOURAPIKEY`` or,
  programatically, use ``isbntools.config.add_apikey`` before a call to
  ``ISBNDBQuery`` or to ``isbndb.query``).
  The main features can be implemented by a call to ``isbndb.query`` function!
  You can get an API key for the *isbndb.com service* here_.

* ``OPENLQuery`` a class that retrives and parses book metadata,
  using **openlibrary.org** (you only have to provide an ISBN).
  The main features can be implemented by a call to ``openl.query`` function!

* ``Metadata`` a class that structures, cleans and 'validates' records of
  metadata. His method ``merge`` allows to implement a simple merging
  procedure for records from different sources. The main features can be
  implemented by a call to ``stdmeta`` function!

* ``vias.parallel`` allows to put theaded calls to services, just by passing the name and
  a pointer to the service ``query`` function. However doesn't implement
  throttling! You can use ``vias.serial`` to make serial calls.

All these classes follow a simple design pattern and, if you follow it, will be
very easy to integrate your classes with the rest of the lib.

One easy way to do that, is to write a new metadata provider that will work as a **plugin**.
(You can use as source a web service, a database, ... ). We just had to follow these steps:

1. Write a python file with a short name, let us say ``goodr.py``. You can
   follow as models wcat_ or isbndb_, but the only **mandatory** requirement is
   that it **must** have a function called ``query``, with signature
   ``query(isbn)``, and that **must** return records in a standard form (like ``wcat`` for
   example). One way to garantee that, is by *returning* with ``return
   stdmeta(records)``.

2. Create a new section called ``[PLUGINS]`` in ``isbntools.conf`` and, for the
   example above, enter a new line like this ``goodr=/full/path/to/directory/of/py/file``.

3. If your plugin uses a service with an API key (e.g. qWeRTY), you must enter a new line in
   the ``[SERVICES]`` section like this ``GOODR_API_KEY=qWeRTY``.

Now you could use ``isbn_meta 9780321534965 goodr`` to get the metadata of ``9780321534965``.

The original quality of metadata, at the several services, is not very good!
If you need high quality metadata in your app, the only solution is to use
*polling & merge* of several providers **and** a **lot** of cleanning and standardization
for fields like ``Authors`` and ``Publisher``.
A *simple merge* provider is now the default in ``isbn_meta`` (and ``isbntools.meta``).
It gives priority to ``wcat`` but overwrites the ``Authors`` field with the value from ``goob``.
Uses the ``merge`` method of ``Metadata`` and *threaded* calls to services
by default (faster for slow internet connections).
You can change that, by setting ``VIAS_MERGE=serial`` (see note below).
You can write your own *merging scheme* by creating a new provider (see_ ``dev.merge`` for an example).

    **Take Note**: These classes are optimized for one-calls to services and not for batch calls.


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


Known Issues
============

1. The ``meta`` method and the ``isbn_meta`` script sometimes give a wrong result
   (this is due to errors on the chosen service), in alternative you could
   try one of the others services.

2. The ``isbntools`` works internally with unicode, however this doesn't
   solve errors of lost information due to bad encode/decode at the origin!

3. Periodically, agencies, issue new blocks of ISBNs. The
   range_ of these blocks is on a database that ``mask`` uses. So it could happen,
   if you have a version of ``isbntools`` that is too old, ``mask`` doesn't work for
   valid (recent) issued ISBNs. The solution? **Update isbntools often**!

4. With some python installations on Windows (e.g. anaconda) the scripts
   only work if you are in the ``.../Anaconda/Scripts`` directory! Can you help_?


Any issue that you would like to report, please do it at github_.


ISBN
====

To know about ISBN:

*  http://en.wikipedia.org/wiki/International_Standard_Book_Number

*  http://www.isbn-international.org/



.. _github: https://github.com/xlcnd/isbntools/issues

.. _range: https://www.isbn-international.org/range_file_generation

.. _here: http://isbndb.com/api/v2/docs

.. _wcat: https://github.com/xlcnd/isbntools/blob/master/isbntools/dev/wcat.py

.. _isbndb: https://github.com/xlcnd/isbntools/blob/master/isbntools/dev/isbndb.py

.. _dev.merge: https://github.com/xlcnd/isbntools/blob/master/isbntools/dev/merge.py

.. _help: https://github.com/xlcnd/isbntools/issues/8

.. _see: https://sourceforge.net/projects/isbntools/files/isbntools-3.0.1-win.zip/download


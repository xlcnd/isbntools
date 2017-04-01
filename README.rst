
.. image:: https://readthedocs.org/projects/isbntools/badge/?version=latest
    :target: http://isbntools.readthedocs.org/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/Sourcegraph-Status-blue.svg
    :target: https://sourcegraph.com/github.com/xlcnd/isbntools
    :alt: Graph

.. image:: https://coveralls.io/repos/xlcnd/isbntools/badge.svg?branch=v4.3.5
    :target: https://coveralls.io/r/xlcnd/isbntools?branch=v4.3.5
    :alt: Coverage

.. image:: https://travis-ci.org/xlcnd/isbntools.svg?branch=v4.3.5
    :target: https://travis-ci.org/xlcnd/isbntools
    :alt: Built Status

.. image:: https://ci.appveyor.com/api/projects/status/github/xlcnd/isbntools?branch=v4.3.5&svg=true
    :target: https://ci.appveyor.com/project/xlcnd/isbntools
    :alt: Windows Built Status




Info
====

``isbntools`` provides several useful methods and functions
to validate, clean, transform, hyphenate and
get metadata for ISBN strings.


**For the end user** several scripts are provided to use **from the command line**:

.. code-block:: console

    $ to_isbn10 ISBN13

transforms an ISBN13 number to ISBN10.

.. code-block:: console

    $ to_isbn13 ISBN10

transforms an ISBN10 number to ISBN13.

.. code-block:: console

    $ isbn_info ISBN

gives you the *group identifier* of the ISBN.

.. code-block:: console

    $ isbn_mask ISBN

*masks* (hyphenate) an ISBN (split it by identifiers).

.. code-block:: console

    $ isbn_meta ISBN [wcat|goob|openl|isbndb|merge] [bibtex|msword|endnote|refworks|opf|json] [YOUR_APIKEY_TO_SERVICE]

gives you the main metadata associated with the ISBN, ``wcat`` uses **worldcat.org**
(**no key is needed**), ``goob`` uses the **Google Books service** (**no key is needed**),
``isbndb`` uses the **isbndb.com** service (**an api key is needed**),
``openl`` uses the **OpenLibrary.org** api (**no key is needed**), ``merge`` uses
a merged record of ``wcat`` and ``goob`` records (**no key is needed**) and
**is the default option** (you only have to enter, e.g. ``isbn_meta 9780321534965``).
You can get an API key for the *isbndb.com service* here_.  You can enter API keys and
set preferences in the file ``isbntools.conf`` in your
``$HOME\.isbntools`` directory (UNIX). For Windows, you should look at
``%APPDATA%/isbntools/isbntools.conf``. The output can be formatted as ``bibtex``,
``msword``, ``endnote``, ``refworks``, ``opf`` or ``json`` (BibJSON) bibliographic formats.

    **NOTE**
    You can apply this command to many ISBNs by using *posix pipes*
    (e.g. ``type FILE_WITH_ISBNs.txt | isbn_meta [SERVICE] [FORMAT] [APIKEY]`` in Windows)


.. code-block:: console

    $ isbn_editions ISBN

gives the collection of ISBNs that represent a given book (uses **Open Library** and **LibraryThing**).

.. code-block:: console

    $ isbn_validate ISBN

validates ISBN10 and ISBN13.

.. code-block:: console

    $ ... | isbn_validate

to use with *posix pipes* (e.g. ``cat FILE_WITH_ISBNs | isbn_validate`` in OSX or Linux).

    **TIP** Suppose you want to extract the ISBN of a pdf eboook (MYEBOOK.pdf).
    Install pdfminer_ and then enter in a command line::

    $ pdf2txt.py -m 5 MYEBOOK.pdf | isbn_validate


.. code-block:: console

    $ isbn_from_words "words from title and author name"

a *fuzzy* script that returns the *most probable* ISBN from a set of words!
(You can verify the result with ``isbn_meta``)!


.. code-block:: console

    $ isbn_goom "words from title and author name" [bibtex|msword|endnote|refworks|json]

a script that returns from **Google Books multiple references**.


.. code-block:: console

    $ isbn_doi ISBN

returns the doi's ISBN-A code of a given ISBN.


.. code-block:: console

    $ isbn_ean13 ISBN

returns the EAN13 code of a given ISBN.


.. code-block:: console

    $ isbn_ren FILENAME

renames (using metadata) files in the **current directory** that have ISBNs in their
filename (e.g. ``isbn_ren 1783559284_book.epub``, ``isbn_ren "*.pdf"``).

    Enter ``isbn_ren`` to see many other options.


.. code-block:: console

    $ isbntools

writes version and copyright notice and **checks if there are updates**.

With

.. code-block:: console

    $ isbn_repl

you will get a **REPL with history, autocompletion, fuzzy options,
redirection and access to the shell**.

Following is a typical session:

.. code-block:: console

    $ isbn_repl

        Welcome to the isbntools 4.3.5 REPL.
        ** For help type 'help' or '?'
        ** To exit type 'exit' :)
        ** To run a shell command, type '!<shellcmnd>'
        ** Use '#' in place of the last ISBN

    $ isbn> ?

    Commands available (type ?<command> to get help):
    -------------------------------------------------
    BIBFORMATS  audit  desc     editions    goom  mask   to_isbn10
    EAN13       conf   doi      exit        help  meta   to_isbn13
    PROVIDERS   cover  doi2tex  from_words  info  shell  validate

    $ isbn> meta 9780156001311 tex
    @book{9780156001311,
         title = {The Name Of The Rose},
        author = {Umberto Eco},
          isbn = {9780156001311},
          year = {1994},
     publisher = {Harcourt Brace}
    }
    $ isbn> meta 9780156001311 tex >>myreferences.bib
    $ isbn> !ls
    myreferences.bib
    $ isbn> desc #
    It is the year 1327. Franciscans in an Italian abbey are suspected of
    heresy, but Brother William of Baskerville's investigation is suddenly
    overshadowed by seven bizarre deaths. Translated by William Weaver. A Helen
    and Kurt Wolff Book
    $ isbn> cover #
         thumbnail:  http://books.google.com/books/content?id=PVVyuD1UY1wC&printsec=frontcover&img=1&zoom=1
    smallThumbnail:  http://books.google.com/books/content?id=PVVyuD1UY1wC&printsec=frontcover&img=1&zoom=5
    $ isbn> exit
    bye


**Within REPL many of the operations are faster.**

Many more scripts could be written with the ``isbntools`` and ``isbnlib`` library,
using the methods for extraction, cleaning, validation and standardization of ISBNs.

Just for fun, suppose I want the *most spoken about* book with certain words in his title.
For a *quick-and-dirty solution*, enter the following code in a file
and save it as ``isbn_tmsa_book.py``.

.. code-block:: python

    #!/usr/bin/env python
    import sys
    from isbntools.app import *

    query = sys.argv[1].replace(' ', '+')
    isbn = isbn_from_words(query)

    print("The ISBN of the most `spoken-about` book with this title is %s" % isbn)
    print("")
    print("... and the book is:")
    print("")
    print((meta(isbn)))

Then in a command line (in the same directory):

.. code-block:: console

    $ python isbn_tmsa_book.py 'noise'

In my case I get::


    The ISBN of the most `spoken-about` book with this title is 9780143105985

    ... and the book is:

    {'Publisher': u'Penguin Books', 'Language': u'eng', 'Title': u'White noise',
    'Year': u'2009', 'ISBN-13': u'9780143105985', 'Authors': u'Don DeLillo ;
    introduction by Richard Powers.'}


Have fun!


Install
=======

From the command line enter (in some cases you have to precede the
command with ``sudo``):


.. code-block:: console

    $ pip install isbntools

or:

.. code-block:: console

    $ easy_install isbntools

or:

.. code-block:: console

    $ pip install isbntools-4.3.5.tar.gz

(first you have to download the file!)

If you use linux systems, you can install using your distribution package
manager (packages ``python-isbntools`` and ``python3-isbntools``), however 
usually these packages are **very old and don't work well anymore**!



For Devs
========

If all you want is to add ``isbntools`` to the requirements of your project,
probably you will better served with isbnlib_, it implements the basic functionality
of ``isbntools`` without end user scripts and configuration files!

If you think that that is not enough, please read_ at least this page of the documentation.

If you would like to contribute to the project please read the guidelines_.


Conf File
=========

You can enter API keys and set preferences in the file ``isbntools.conf`` in your
``$HOME/.isbntools`` directory (UNIX). For Windows, you should look at
``%APPDATA%/isbntools/isbntools.conf``
(**create these, directory and file, if don't exist** [Now just enter ``isbn_conf make``!]).
The file should look like:

.. code-block:: console

    ...

    [MISC]
    REN_FORMAT={firstAuthorLastName}{year}_{title}_{isbn}
    DEBUG=False

    [SYS]
    URLOPEN_TIMEOUT=10
    THREADS_TIMEOUT=12

    [SERVICES]
    DEFAULT_SERVICE=merge
    VIAS_MERGE=parallel
    ISBNDB_API_KEY=

    ...


The values are self-explanatory!


    **NOTE** If you are running ``isbntools`` inside a virtual environment, the
    ``isbntools.conf`` file will be inside folder ``isbntools``
    at the root of the environment.

The easier way to manipulate these files is by using the script ``isbn_conf``.
At a terminal enter:

.. code-block:: console

   $ isbn_conf show

to see the current conf file.

This script has many options that allow a controlled editing of the conf file.
Just enter ``isbn_conf`` for help.



isbntools.contrib
=================

To get extra functionality, search_ pypi for packages starting with ``isbntools.contrib``
**or** type at a terminal:

.. code-block:: console

    $ pip search isbntools


for a nice formated report!



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

4. Calls to metadata services are cached by default. If you don't want this
   feature, just enter ``isbn_conf setopt cache no``. If by any reason you need
   to clear the cache, just enter ``isbn_conf delcache``.

Any issue that you would like to report, (if you are a developer) please do it at github_
or at stackoverflow_ with tag **isbntools**,
(if you are an end user) at twitter_.


--------------------------------

.. class:: center

More documentation at Read the Docs_.

--------------------------------

.. _github: https://github.com/xlcnd/isbntools/issues

.. _range: https://www.isbn-international.org/range_file_generation

.. _here: http://isbndb.com/api/v2/docs

.. _read: http://isbntools.readthedocs.org/en/latest/devs.html

.. _guidelines: http://bit.ly/1jcxq8W

.. _twitter: https://twitter.com/isbntools

.. _pdfminer: https://pypi.python.org/pypi/pdfminer

.. _isbnlib: http://bit.ly/ISBNlib

.. _search: https://pypi.python.org/pypi?%3Aaction=search&term=isbntools.contrib&submit=search

.. _Docs: http://bit.ly/1l0W4In

.. _stackoverflow: http://stackoverflow.com/questions/tagged/isbntools

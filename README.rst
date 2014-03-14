

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

.. image:: https://travis-ci.org/xlcnd/isbntools.png?branch=v2.0.7
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

Several scripts are provided to use **from the command line**:

.. code-block:: bash

    $ to_isbn10 ISBN13

transforms an ISBN10 number to ISBN13.

.. code-block:: bash

    $ to_isbn13 ISBN10

transforms an ISBN13 number to ISBN10.

.. code-block:: bash

    $ isbn_info ISBN

gives you the *group identifier* of the ISBN.

.. code-block:: bash

    $ isbn_mask ISBN

*masks* (hyphenate) an ISBN (split it by identifiers).

.. code-block:: bash

    $ isbn_meta ISBN

gives you the main metadata associated with the ISBN (uses worldcat.org), to
use the Google Books service enter ``isbn_meta ISBN goob``.

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

writes version and copyright notice.

Many more scripts could be written with the ``isbntools`` library,
using the methods for extraction, cleaning, validation and standardization of ISBNs.

Just for fun, suppose I want the *most spoken about* book with certain words in his title.
For a *quick-and-dirty solution*, enter the following code in a file
and save it as ``isbn_tmsa_book.py``.

.. code-block:: python

    #!/usr/bin/env python
    import sys
    import urllib2
    from isbntools import *

    query = sys.argv[1].replace(' ', '+')
    SEARCH_URL = "http://www.google.com/search?q=%s+ISBN" % query

    headers = {'User-Agent': 'w3m/0.5.2'}
    request = urllib2.Request(SEARCH_URL, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read()

    isbns = get_isbnlike(content)

    for item in isbns:
        ib = get_canonical_isbn(item, output='isbn13')
        if ib: break

    print("The ISBN of the most `spoken-about` book with this title is %s" % ib)
    print("")
    print("... and the book is:")
    print("")
    print((meta(ib)))

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

    $ pip install isbntools-2.0.7.tar.gz

(first you have to download the file!)


For Devs
========

If you need high quality metadata in your app, the only solution is to use
*polling* of several providers.

You can extend the lib by using the classes and functions exposed in
``isbntools.dev``, namely:

* ``WEBService`` a class that handles the access to web
  services (just by passing an url) and supports ``gzip``.
  You can subclass it to extend the functionality... but
  probably you don't need to use it! It is used in the next class.

* ``WEBQuery`` a class that uses ``WEBService`` to retrive and parse
  data from a web service. You can build a new provider of metadata
  by subclassing this class. The following classes do that
  (by using the *call pattern*). His main methods allow passing custom
  functions (*handlers*) that specialize them to specific needs (``data_checker`` and
  ``parser``).

* ``GOOBQuery`` a class that retrives and parses book metadata,
  using Google Books API (you only have to provide an ISBN).
  The main features can be implemented by a call to ``googlebooks.query`` function!

* ``WCATQuery`` a class that retrives and parses book metadata,
  using the ``worldcat.org xisbn service`` (you only have to provide an ISBN).
  The main features can be implemented by a call to ``wcat.query`` function!

* ``WCATEdQuery`` a class that retrives and parses collections of ISBNs related
  with a given book, using the ``worldcat.org xisbn service``
  (you only have to provide an ISBN).
  The main features can be implemented by a call to ``wcated.query`` function!

* ``ISBNDBQuery`` a class that retrives and parses book metadata,
  using the ``isbndb.org service`` (you only have to provide an ISBN and an
  **API key**).
  The main features can be implemented by a call to ``isbndb.query`` function!

* ``Metadata`` a class that structures, cleans and 'validates' records of
  metadata. The main features can be implemented by a call to ``stdmeta``
  function!

All these classes follow a simple design pattern and, if you follow it, will be
very easy to integrate your classes with the rest of the lib.



Known Issues
============

1. The ``meta`` method and the ``isbn_meta`` script sometimes give a wrong result
   (this is due to errors on the worldcat.org service), in alternative you could
   use the Google Books service (e.g. ``isbn_meta 9780143105985 goob``).

2. The ``isbntools`` works internally with unicode, however this doesn't
   solve errors of lost information due to bad encode/decode at the origin!

3. Periodically new blocks of ISBNs are issued to agencies. The ``range`` of
   these blocks is on a database that ``mask`` uses. So it could happen, if you
   have a version of ``isbntools`` that is too old, ``mask`` doesn't work for
   valid (recent) issued ISBNs. The solution? **Update isbntools often**!


ISBN
====

To know about ISBN:

*  http://en.wikipedia.org/wiki/International_Standard_Book_Number

*  http://www.isbn-international.org/



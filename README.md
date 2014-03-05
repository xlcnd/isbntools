
[![Downloads](https://pypip.in/d/isbntools/badge.png)](https://pypi.python.org/pypi/isbntools/)
[![Latest Version](https://pypip.in/v/isbntools/badge.png)](https://pypi.python.org/pypi/isbntools/)
[![Download format](https://pypip.in/format/isbntools/badge.png)](https://pypi.python.org/pypi/isbntools/)
[![License](https://pypip.in/license/isbntools/badge.png)](https://pypi.python.org/pypi/isbntools/)
[![Build Status](https://travis-ci.org/xlcnd/isbntools.png?branch=v1.0.2)](https://travis-ci.org/xlcnd/isbntools)


ISBN tools
==========

Info
----

`isbntools` provides several useful methods and functions
to validate, clean, transform, hyphenate and
get metadata for ISBN strings.

Typical usage (as library):

```python

    #!/usr/bin/env python
    import isbntools
    ...
```

Several scripts are provided to use from the command line:

```bash

    $ to_isbn10 ISBN13
```
transforms an ISBN10 number to ISBN13.

```bash

    $ to_isbn13 ISBN10
```
transforms an ISBN13 number to ISBN10.

```bash

    $ isbn_info ISBN
```
gives you the *group identifier* of the ISBN.

```bash

    $ isbn_mask ISBN
```
*masks* (hyphenate) an ISBN (split it by identifiers).

```bash

    $ isbn_meta ISBN
```
gives you the main metadata associated with the ISBN (uses worldcat.org).

```bash

    $ isbn_validate ISBN
```
validates ISBN10 and ISBN13.

```bash

    $ ... | isbn_stdin_validate
```
to use with *posix pipes* (e.g. `cat FILE_WITH_ISBNs | isbn_stdin_validate`).

```bash

    $ isbn_from_words "words from title and author name"
```
a *fuzzy* script that returns the *most probable* ISBN from a set of words.
You could verify the result with `isbn_meta`!

```bash

    $ isbntools
```
writes version and copyright notice.

Many more scripts could be written with the `isbntools` library,
using the methods for extraction, cleaning, validation and standardization of ISBNs.

Just for fun, suppose I want the *most spoken about* book with certain words in his title.
For a *quick-and-dirty solution*, enter the following code in a file
and save it as `isbn_tmsa_book.py`.

```python

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
        ib = get_canonical_isbn(item, output='ISBN-13')
        if ib: break

    print("The ISBN of the most `spoken-about` book with this title is %s" % ib)
    print("")
    print("... and the book is:")
    print("")
    print((meta(ib)))
```

Then in a command line (in the same directory):

```bash

    $ python isbn_tmsa_book.py 'noise'
```

In my case I get:

```

    The ISBN of the most `spoken-about` book with this title is 9780143105985

    ... and the book is:

    {'Publisher': u'Penguin Books', 'Language': u'eng', 'Title': u'White noise',
    'Year': u'2009', 'ISBN-13': '9780143105985', 'Authors': u'Don DeLillo ;
    introduction by Richard Powers.'}
```

Have fun!

Install
-------

From the command line enter:

```bash

    $ pip install isbntools
```
or:

```bash

    $ easy_install isbntools
```
or:

```bash

    $ pip install isbntools-1.0.2.zip
```
(first you have to download the file and in some cases you have to preced the
command by `sudo`!)


Known Issues
------------

1. The `meta` method and the `isbn_meta` script sometimes give a wrong result
   (this is due to errors on the worldcat.org service), in alternative you could
   use the Google Books service (e.g. `isbn_meta 9781.0.208267 goob`)


ISBN
----

To know about ISBN:

* http://en.wikipedia.org/wiki/International_Standard_Book_Number
* http://www.isbn-international.org/


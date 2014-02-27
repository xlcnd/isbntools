ISBN tools
==========

Info
----

`isbntools` provides several useful methods and functions
to validate, clean and transform ISBN strings.

Typical usage:

```python

    #!/usr/bin/env python
    import isbntools
```

Several scripts are provided to use from the command line:

* `to_isbn10 ISBN13` : transforms an ISBN10 number to ISBN13
* `to_isbn13 ISBN10` : transforms an ISBN13 number to ISBN10
* `isbn_info ISBN`   : gives you the *group identifier* of the ISBN
* `isbn_mask ISBN`   : *masks* (hyphenate) an ISBN (split it by identifiers)
* `isbn_meta ISBN`   : gives you the main metadata associated with the ISBN (uses wcat.org)
* `isbn_validate ISBN`     : validates ISBN10 and ISBN13
* `isbn_stdin_validate`    : to use with *posix pipes* (e.g. `cat ISBNs | isbn_stdin_validate`)
* `isbntools`        : writes version and copyright notice


Install
-------

```
pip install isbntools
     or
easy_install isbntools
     or
pip install isbntools-0.7.2.zip (first you have to download the file!)
```

Known Issues
------------

1. Some of the methods don't work with ISBNs with group identifier `979`
   (will be fixed in the next major version)
2. The `meta` method and the `isbn_meta` script sometimes give a wrong result
   (this is due to errors on the wcat.org service)


ISBN
----

To know about ISBN:

* http://en.wikipedia.org/wiki/International_Standard_Book_Number
* http://www.isbn-international.org/



[![Downloads](https://pypip.in/d/isbntools/badge.png)](https://pypi.python.org/pypi/isbntools/)
[![Latest Version](https://pypip.in/v/isbntools/badge.png)](https://pypi.python.org/pypi/isbntools/)
[![Download format](https://pypip.in/format/isbntools/badge.png)](https://pypi.python.org/pypi/isbntools/)
[![License](https://pypip.in/license/isbntools/badge.png)](https://pypi.python.org/pypi/isbntools/)
[![Coverage Status](https://coveralls.io/repos/xlcnd/isbntools/badge.png?branch=master)](https://coveralls.io/r/xlcnd/isbntools?branch=master)
[![Graph](https://sourcegraph.com/api/repos/github.com/xlcnd/isbntools/badges/status.png)](https://sourcegraph.com/github.com/xlcnd/isbntools)
[![Build Status](https://travis-ci.org/xlcnd/isbntools.png?branch=v3.1.4)](https://travis-ci.org/xlcnd/isbntools)


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

**For the end user** several scripts are provided to use **from the command line**:

```bash
$ to_isbn10 ISBN13
```
transforms an ISBN13 number to ISBN10.

```bash
$ to_isbn13 ISBN10
```
transforms an ISBN10 number to ISBN13.

```bash
$ isbn_info ISBN
```
gives you the *group identifier* of the ISBN.

```bash
$ isbn_mask ISBN
```
*masks* (hyphenate) an ISBN (split it by identifiers).

```bash
$ isbn_meta ISBN [wcat|goob|openl|isbndb|merge] [bibtex|...] [YOUR_APIKEY_TO_SERVICE]
```
gives you the main metadata associated with the ISBN, `wcat` uses **worldcat.org**
(**no key is needed**), `goob` uses the **Google Books service** (**no key is needed**),
`isbndb` uses the **isbndb.com** service (**an api key is needed**),
`openl` uses the **OpenLibrary.org** api (**no key is needed**), `merge` uses
a mergeded record of `wcat` and `goob` records (**no key is needed**) and
**is the default option** (you only have to enter, e.g. `isbn_meta 9780321534965`).
You can get an API key for the *isbndb.com service* [here](http://isbndb.com/api/v2/docs).
You can enter API keys and set preferences in the file `isbntools.conf` in your
`$HOME\.isbntools` directory (UNIX). For Windows, you should look at
`%APPDATA%/isbntools/isbntools.conf`.
The output can be formatted as `bibtex`, `msword`,  `endnote`, `refworks`, or
`json` (BibJSON) bibliographic formats.


```bash
$ isbn_editions ISBN
```
gives the collection of ISBNs that represent a given book (uses worldcat.org).

```bash
$ isbn_validate ISBN
```
validates ISBN10 and ISBN13.

```bash
$ ... | isbn_stdin_validate
```
to use with *pipes* (e.g. `cat FILE_WITH_ISBNs | isbn_stdin_validate`).

```bash
$ isbn_from_words "words from title and author name"
```
a *fuzzy* script that returns the *most probable* ISBN from a set of words.
(You can verify the result with `isbn_meta`)!

```bash
$ isbn_goom "words from title and author name" [bibtex|msword|endnote|refworks|json]
```
a script that returns from **Google Books multiple references**.


```bash
$ isbntools
```
writes version and copyright notice and **checks if there are updates**.

Many more scripts could be written with the `isbntools` library,
using the methods for extraction, cleaning, validation and standardization of ISBNs.

Just for fun, suppose I want the *most spoken about* book with certain words in his title.
For a *quick-and-dirty solution*, enter the following code in a file
and save it as `isbn_tmsa_book.py`.

```python
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

From the command line enter (in some cases you have to preced the
command by `sudo`):

```bash
$ pip install isbntools
```
this installs from [pypi](https://pypi.python.org/pypi/isbntools) or:

```bash
$ easy_install isbntools
```
this installs from [pypi](https://pypi.python.org/pypi/isbntools) too, or (to install locally in *Linux* or *Mac OS X*):

```bash
$ pip install isbntools-3.1.4.tar.gz
```
but first you have to [download](https://pypi.python.org/packages/source/i/isbntools/isbntools-3.1.4.tar.gz) the file!


You should check if the install was successful, by enter:

```bash
$ isbntools
```


### Windows

>**If you are on a Windows system**,
you can download a
[standalone version](http://bit.ly/1i8qatY)
that **doesn't need python** and gives you
access to the scripts. However, doesn't support add-ins or customization!

>**Intructions**:
1. unzip the file and put the file `isbn.exe` in a folder
2. go to that folder and open a command line
3. run `isbn help` to get further instructions


For Devs
--------

In the namespace `isbntools` you have access to the core methods:
`is_isbn10`, `is_isbn13`, `to_isbn10`, `to_isbn13`, `canonical`,
`clean`, `notisbn`, `get_isbnlike`, `get_canonical_isbn`, `mask`,
`meta`, `info`, `editions`, and `isbn_from_words`.

You can extend the lib by using the classes and functions exposed in
namespace `isbntools.dev`, namely:

* `WEBService` a class that handles the access to web
  services (just by passing an url) and supports `gzip`.
  You can subclass it to extend the functionality... but
  probably you don't need to use it! It is used in the next class.

* `WEBQuery` a class that uses `WEBService` to retrive and parse
  data from a web service. You can build a new provider of metadata
  by subclassing this class.
  His main methods allow passing custom
  functions (*handlers*) that specialize them to specific needs (`data_checker` and
  `parser`).

* `Metadata` a class that structures, cleans and 'validates' records of
  metadata. His method `merge` allows to implement a simple merging
  procedure for records from different sources. The main features can be
  implemented by a call to `stdmeta` function!

* `vias` exposes several functions to put calls to services, just by passing the name and
  a pointer to the service's `query` function.
  `vias.parallel` allows to put theaded calls, however doesn't implement
  throttling! You can use `vias.serial` to make serial calls and
  `vias.multi` to use several cores. The default is `vias.serial`, but
  you can change that in the conf file.

All these classes follow a simple design pattern and, if you follow it, will be
very easy to integrate your classes with the rest of the lib.

One easy way to do that, is to write a new metadata provider that will work as a **plugin**.
(You can use as source a web service, a database, ... ). We just had to follow these steps:

1. Write a python file with a short name, let us say `goodr.py`. You can
   follow as models [wcat](https://github.com/xlcnd/isbntools/blob/master/isbntools/dev/wcat.py)
   or [isbndb](https://github.com/xlcnd/isbntools/blob/master/isbntools/dev/isbndb.py),
   but the only **mandatory** requirement is
   that it **must** have a function called `query`, with signature
   `query(isbn)`, and that **must** return records in a standard form (like `wcat` for
   example). One way to garantee that, is by *returning* with `return
   stdmeta(records)`.

2. Create a new section called `[PLUGINS]` in `isbntools.conf` and, for the
   example above, enter a new line like this `goodr=/full/path/to/directory/of/py/file`.

3. If your plugin uses a service with an API key (e.g. qWeRTY), you must enter a new line in
   the `[SERVICES]` section like this `GOODR_API_KEY=qWeRTY`.

Now you could use `isbn_meta 9780321534965 goodr` to get the metadata of `9780321534965`.

The original quality of metadata, at the several services, is not very good!
If you need high quality metadata in your app, the only solution is to use
*polling & merge* of several providers **and** a **lot** of cleanning and standardization
for fields like `Authors` and `Publisher`.
A *simple merge* provider is now the default in `isbn_meta` (and `isbntools.meta`).
It gives priority to `wcat` but overwrites the `Authors` field with the value from `goob`.
Uses the ``merge`` method of ``Metadata`` and *serial* calls to services
by default (faster for faster internet connections).
You can change that, by setting `VIAS_MERGE=parallel` or `VIAS_MERGE=multi` (see note below).
You can write your own *merging scheme* by creating a new provider (see_ `dev.merge` for an example).

> **Take Note**: These classes are optimized for one-calls to services and not for batch calls.

You can browse the code, in a very structured way, at [sourcegraph](http://bit.ly/1k14kHi).

If you like to contribute to the project, please read the [guidelines](http://bit.ly/1jcxq8W).


Conf File
---------

You can enter API keys and set preferences in the file `isbntools.conf` in your
`$HOME\.isbntools` directory (UNIX). For Windows, you should look at
`%APPDATA%/isbntools/isbntools.conf`
(**create these, directory and file, if don't exist**). The file should look like:

```bash
[SYS]
SOCKETS_TIMEOUT=15
THREADS_TIMEOUT=12

[SERVICES]
DEFAULT_SERVICE=merge
VIAS_MERGE=serial
ISBNDB_API_KEY=your_api_key_here_or_DELETEME
```

The values are self-explanatory!


Known Issues
------------

1. The `meta` method and the `isbn_meta` script sometimes give a wrong result
   (this is due to errors on the chosen service), in alternative you could
   try one of the others services.

2. The `isbntools` works internally with unicode, however this doesn't
   solve errors of lost information due to bad encode/decode at the origin!

3. Periodically, agencies, issue new blocks of ISBNs. The
   [*range*](https://www.isbn-international.org/range_file_generation) of
   these blocks is on a database that `mask` uses. So it could happen, if you
   have a version of `isbntools` that is too old, `mask` doesn't work for
   valid (recent) issued ISBNs. The solution? **Update `isbntools` often**!


Any issue that you would like to report, please do it at
[github](https://github.com/xlcnd/isbntools/issues) (if you are a developer)
or at [twitter](https://twitter.com/isbntools) (if you are and end user).


ISBN
----

To know about ISBN:

* http://en.wikipedia.org/wiki/International_Standard_Book_Number
* http://www.isbn-international.org/


---
More documentation at [http://isbntools.readthedocs.org](http://bit.ly/1l0W4In)

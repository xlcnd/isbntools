
For Devs
========


API's Main Namespaces
---------------------

In the namespace ``isbntools.app`` you have access to the core methods:
``is_isbn10``, ``is_isbn13``, ``to_isbn10``, ``to_isbn13``, ``canonical``,
``clean``, ``notisbn``, ``get_isbnlike``, ``get_canonical_isbn``, ``mask``,
``meta``, ``info``, ``editions``, and ``isbn_from_words``.
The exceptions raised by these methods can all be catched using ``ISBNToolsException``.

You can use advanced features by using the classes and functions exposed in
namespace ``isbnlib.dev``, namely:

* ``WEBService`` a class that handles the access to web
  services (just by passing an url) and supports ``gzip``.
  You can subclass it to extend the functionality... but
  probably you don't need to use it! It is used in the next class.

* ``WEBQuery`` a class that uses ``WEBService`` to retrieve and parse
  data from a web service. You can build a new provider of metadata
  by subclassing this class.
  His main methods allow passing custom
  functions (*handlers*) that specialize them to specific needs (``data_checker`` and
  ``parser``).

* ``Metadata`` a class that structures, cleans and 'validates' records of
  metadata. His method ``merge`` allows to implement a simple merging
  procedure for records from different sources. The main features can be
  implemented by a call to ``stdmeta`` function!

* ``vias`` exposes several functions to put calls to services, just by passing the name and
  a pointer to the service's ``query`` function.
  ``vias.parallel`` allows to put threaded calls, however doesn't implement
  throttling! You can use ``vias.serial`` to make serial calls and
  ``vias.multi`` to use several cores. The default is ``vias.serial``, but
  you can change that in the conf file.


The exceptions raised by these methods can all be catched using ``ISBNLibDevException``.


In ``isbnlib.dev.helpers`` you can find several methods, that we found very useful,
but you should consider them as beta software. They can change a lot in
the future.


Finally, ``isbntools.conf`` provides methods to edit the configuration file and
helpers to work with isbntools's modules.


    **WARNING**: If you inspect the library, you will see that there are a lot of
    private modules (their name starts with '_'). These modules **should not**
    be accessed directly since, with high probability, your program will break
    with a further version of the library!

    You should access only methods in the API's ``isbntools``, ``isbnlib.dev``,
    ``isbnlib.dev.helpers`` and ``isbntools.conf``



All these classes follow a simple design pattern and, if you follow it, will be
very easy to integrate your classes with the rest of the lib.


Plugins
-------

The support for pluggins **was dropped** from ``isbntools``, however continues to support modules!
The reason is that ``isbnlib`` now supports plugins for metadata and new formatters.


Just an ISBN lib!
-----------------

If you just want to integrate the lib in your project, you have several options,
depending on your needs...

1. If you need only basic manipulation of ISBNs (validation, transforming,
   extraction, hyphenation, ...) but not custom metadata or file renaming,
   then you don't need a conf file. Just use the methods in ``isbntools``.
   But probably you are better served with isbnlib_.

2. If you rely heavily in metadata (or file renaming) and don't want to
   implement caching yourself, then you **need** an ``isbntools.conf`` file in a
   directory were your program could write.  You can use ``isbntools.conf`` to
   programatically manipulate the conf file.

3. If you want to vendorize the lib you should take a careful look at
   ``setup.py`` and maybe this package (datafolder_) could help!

Anyway, you could use the ``isbn_...`` scripts in the ``isbntools/bin`` directory
as examples on how to use the library and as debugger tools for your implementation.

  **Don't forget** to take a look at isbnlib_.

---------------------------------------------------------------------------------

You can browse the code at GitHub_.




.. _GitHub: http://bit.ly/1oTm5ze

.. _isbnlib: http://bit.ly/ISBNlib

.. _datafolder: https://pypi.python.org/pypi/datafolder

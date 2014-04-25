

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
  by subclassing this class.
  His main methods allow passing custom
  functions (*handlers*) that specialize them to specific needs (``data_checker`` and
  ``parser``).

* ``Metadata`` a class that structures, cleans and 'validates' records of
  metadata. His method ``merge`` allows to implement a simple merging
  procedure for records from different sources. The main features can be
  implemented by a call to ``stdmeta`` function!

* ``vias`` exposes several functions to put calls to services, just by passing the name and
  a pointer to the service ``query`` function.
  ``vias.parallel`` allows to put theaded calls. However doesn't implement
  throttling! You can use ``vias.serial`` to make serial calls and
  ``vias.multi`` to use several cores. The default is ``vias.serial``, however
  you can change that in the conf file.

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
Uses the ``merge`` method of ``Metadata`` and *serial* calls to services
by default (faster for faster internet connections).
You can change that, by setting ``VIAS_MERGE=parallel`` or ``VIAS_MERGE=multi`` (see note below).
You can write your own *merging scheme* by creating a new provider (see_ ``dev.merge`` for an example).

    **Take Note**: These classes are optimized for one-calls to services and not for batch calls.

You can browse the code, in a very structured way, at sourcegraph_.


.. _wcat: https://github.com/xlcnd/isbntools/blob/master/isbntools/dev/wcat.py

.. _isbndb: https://github.com/xlcnd/isbntools/blob/master/isbntools/dev/isbndb.py

.. _see: https://github.com/xlcnd/isbntools/blob/master/isbntools/dev/merge.py

.. _sourcegraph: http://bit.ly/1k14kHi

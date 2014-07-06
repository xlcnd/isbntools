# -*- coding: utf-8 -*-
"""Query providers for metadata."""

import os
from ._core import EAN13
from .registry import services
from ._exceptions import NotRecognizedServiceError, NotValidISBNError
from .config import options, CONF_PATH, CACHE_FILE
from ._cache import Cache


if CONF_PATH:
    DEFAULT_CACHE = os.path.join(CONF_PATH, CACHE_FILE)
    writable = os.access(CONF_PATH, os.W_OK)
else:           # pragma: no cover
    try:
        # try write conf for the next time!
        from .contrib._hook import mk_conf
        mk_conf()
    except:
        pass
    # only useful for development
    DEFAULT_CACHE = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), CACHE_FILE)
    try:
        writable = os.access(DEFAULT_CACHE, os.W_OK)
    except:
        writable = False

DEFAULT_CACHE = DEFAULT_CACHE if writable else 'no'
CACHE = options.get('CACHE', DEFAULT_CACHE)
CACHE = None if CACHE.lower() == 'no' else CACHE


def query(isbn, service='default', cache=CACHE):
    """Query worldcat.org, Google Books (JSON API), ... for metadata."""
    ean = EAN13(isbn)
    if not ean:
        raise NotValidISBNError(isbn)
    isbn = ean
    if service != 'default' and service not in services:
        raise NotRecognizedServiceError(service)
    if cache is None:  # pragma: no cover
        return services[service](isbn)
    kache = Cache(cache)
    key = isbn + service
    if kache[key]:
        return kache[key]
    meta = services[service](isbn)
    if meta:
        kache[key] = meta
    return meta if meta else None

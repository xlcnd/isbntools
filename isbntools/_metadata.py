# -*- coding: utf-8 -*-
"""Query providers for metadata."""

import os
from .registry import services
from .exceptions import NotRecognizedServiceError
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
    if service != 'default' and service not in services:
        raise NotRecognizedServiceError(service)
    if cache is None:
        return services[service](isbn)
    kache = Cache() if cache == 'default' else Cache(cache)
    key = isbn + service
    if kache[key]:
        return kache[key]
    meta = services[service](isbn)
    if meta:
        kache[key] = meta
    return meta if meta else None

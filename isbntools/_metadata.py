# -*- coding: utf-8 -*-
"""Query providers for metadata."""

from .registry import services
from .exceptions import NotRecognizedServiceError
from ._cache import Cache
from .config import options

CACHE = options.get('CACHE', 'default')
CACHE = None if CACHE.lower() == 'no' else CACHE


def query(isbn, service='default', cache=CACHE):
    """Query worldcat.org, Google Books (JSON API), ... for metadata."""
    if service != 'default' and service not in services:
        raise NotRecognizedServiceError(service)
    if not cache:
        return services[service](isbn)
    kache = Cache() if cache == 'default' else Cache(cache)
    key = isbn + service
    if not kache[key]:
        meta = services[service](isbn)
        if meta:
            kache[key] = meta
        return meta if meta else None
    return kache[key]

# -*- coding: utf-8 -*-
"""Query providers for metadata."""

import os
from .registry import services
from .exceptions import NotRecognizedServiceError
from .config import options, CONF_PATH, CACHE_FILE
from ._cache import Cache
from . import in_virtual


if CONF_PATH:
    DEFAULT_CACHE = os.path.join(CONF_PATH, CACHE_FILE)
else:           # pragma: no cover
    if in_virtual():
        # This default cache location only makes sense for virtalenv installs
        DEFAULT_CACHE = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), CACHE_FILE)
    else:
        DEFAULT_CACHE = 'no'
CACHE = options.get('CACHE', DEFAULT_CACHE)
CACHE = None if CACHE.lower() == 'no' else CACHE


def query(isbn, service='default', cache=CACHE):
    """Query worldcat.org, Google Books (JSON API), ... for metadata."""
    if service != 'default' and service not in services:
        raise NotRecognizedServiceError(service)
    if not cache:
        return services[service](isbn)
    kache = Cache() if cache == 'default' else Cache(cache)
    key = isbn + service
    if kache[key]:
        return kache[key]
    meta = services[service](isbn)
    if meta:
        kache[key] = meta
    return meta if meta else None

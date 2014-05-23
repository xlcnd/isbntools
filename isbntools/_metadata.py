# -*- coding: utf-8 -*-
"""Query providers for metadata."""

from .registry import services
from .exceptions import NotRecognizedServiceError


def query(isbn, service='default'):
    """Query worldcat.org, Google Books (JSON API), ... for metadata."""
    if service != 'default' and service not in services:
        raise NotRecognizedServiceError(service)
    return services[service](isbn)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from regestry import services


def query(isbn, service='default'):
    """
    Queries worldcat.org or Google Books (JSON API) for metadata
    """
    if service not in services:
        print(('Error:%s is not a recognized service!' % service))
        return
    return services[service](isbn)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wcat
import googlebooks


def query(isbn, service='wcat'):
    """
    Queries worldcat.org or Google Books (JSON API) for metadata
    """
    if service == 'wcat':
        canonical = wcat.query(isbn)
    elif service == 'goob' or service == 'googlebooks':
        canonical = googlebooks.query(isbn)
    else:
        print(('Error:%s is not a recognized service!' % service))
        return
    return canonical

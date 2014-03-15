#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .data import Metadata
from .wcat import query as qwcat
from .googlebooks import query as qgoob


def query(isbn):
    """
    Query function for the `merge provider` (waterfall model)
    """
    rg, rw, md = None, None, None
    # TODO do the calls in parallel
    try:
        rw = qwcat(isbn)
        md = Metadata(rw)
    except:
        pass
    try:
        rg = qgoob(isbn)
    except:
        pass
    if rg and md:
        md.merge(rg, ('Authors'))
        return md.canonical
    if not md and rg:
        md = Metadata(rg)
        return md.canonical
    return md.canonical if not rg and rw else None

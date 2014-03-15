#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .data import Metadata
from .wcat import query as qwcat
from .googlebooks import query as qgoob


def query(isbn):
    """
    Query function for the `merge provider`
    """
    # TODO do this in parallel
    rw = qwcat(isbn)
    rg = qgoob(isbn)

    md = Metadata(rw)
    md.merge(rg, ('Authors'))

    return md.canonical

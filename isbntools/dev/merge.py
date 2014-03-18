#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .data import Metadata
from .wcat import query as qwcat
from .googlebooks import query as qgoob
from .parallel import vias


def query(isbn):
    """
    Query function for the `merge provider` (waterfall model)
    """
    named_tasks = (('wcat', qwcat), ('goob', qgoob))
    results = vias(named_tasks, isbn)

    rw = results.get('wcat')
    rg = results.get('goob')

    md = Metadata(rw) if rw else None

    if md and rg:
        md.merge(rg, ('Authors'))
        return md.canonical
    if not md and rg:
        md = Metadata(rg)
        return md.canonical
    return md.canonical if not rg and rw else None

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from .data import Metadata
from .wcat import query as qwcat
from .googlebooks import query as qgoob

results = {}


def worker(name, task, isbn):
    """
    Worker function for thread
    """
    try:
        results[name] = task(isbn)
    except:
        pass


def query(isbn):
    """
    Query function for the `merge provider` (waterfall model)
    """
    # threaded call to services
    for name, task in (('wcat', qwcat), ('goob', qgoob)):
        t = threading.Thread(target=worker, args=(name, task, isbn))
        t.start()
        t.join()

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

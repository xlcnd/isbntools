# -*- coding: utf-8 -*-

from .data import Metadata
from .wcat import query as qwcat
from .goob import query as qgoob
from . import vias
from .. import config


def query(isbn, processor='parallel'):
    """
    Query function for the `merge provider` (waterfall model)
    """
    processor = config.options.get('VIAS_MERGE', processor)
    named_tasks = (('wcat', qwcat), ('goob', qgoob))
    if processor == 'parallel':
        results = vias.parallel(named_tasks, isbn)
    else:
        results = vias.serial(named_tasks, isbn)

    rw = results.get('wcat')
    rg = results.get('goob')

    md = Metadata(rw) if rw else None

    if md and rg:
        md.merge(rg, ('Authors'))
        return md.value
    if not md and rg:
        md = Metadata(rg)
        return md.value
    return md.value if not rg and rw else None

# -*- coding: utf-8 -*-
"""Provide metadata by merging metadata from other providers."""

from isbnlib.dev import Metadata, vias
from .app import registry


def query(isbn, processor=None):
    """Query function for the 'merge provider' (waterfall model)."""
    if not processor:
        processor = config.options.get('VIAS_MERGE', processor).lower()
        if not processor:     # pragma: no cover
            processor = 'serial'

    qoclc = registry.services.get('oclc', None)
    qgoob = registry.services.get('goob', None)
    # TODO logger warning: no required service!!!
    # if not qoclc and qgoob:
    #     return qgoob(isbn)
    # if qoclc and not qgoob:
    #     return qoclc(isbn)
    if not qoclc or not qgoob:
        return {}

    named_tasks = (('oclc', qoclc), ('goob', qgoob))
    if processor == 'parallel':
        results = vias.parallel(named_tasks, isbn)
    elif processor == 'serial':
        results = vias.serial(named_tasks, isbn)
    elif processor == 'multi':
        results = vias.multi(named_tasks, isbn)

    ro = results.get('oclc')
    rg = results.get('goob')

    if not ro and not rg:
        return {}

    md = Metadata(ro) if ro else {}

    if md and rg:
        # Try to complete Authors, Publisher and Language from Google
        md.merge(rg, overwrite=('Authors', 'Publisher', 'Language'))
        return md.value
    if not md and rg:       # pragma: no cover
        md = Metadata(rg)
        return md.value
    return md.value if not rg and ro else {}  # pragma: no cover

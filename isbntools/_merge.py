# -*- coding: utf-8 -*-
"""Provide metadata by merging metadata from other providers."""

from . import config
from . import goob as qgoob
from . import oclc as qoclc
from isbnlib.dev import Metadata, vias


# TODO register new service 'merge' on import


def query(isbn, processor=None):
    """Query function for the 'merge provider' (waterfall model)."""
    if not processor:
        processor = config.options.get('VIAS_MERGE', processor).lower()
        if not processor:     # pragma: no cover
            processor = 'serial'

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
        return None

    md = Metadata(ro) if ro else None

    if md and rg:
        # Try to complete Authors, Publisher and Language from Google
        md.merge(rg, overwrite=('Authors', 'Publisher', 'Language'))
        return md.value
    if not md and rg:       # pragma: no cover
        md = Metadata(rg)
        return md.value
    return md.value if not rg and rw else None  # pragma: no cover

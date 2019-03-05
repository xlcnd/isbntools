# -*- coding: utf-8 -*-
"""Provide metadata by merging metadata from other providers."""

from isbnlib.dev import Metadata, vias
from .app import config


def query(isbn,
          qserv1,
          qserv2,
          overwrite=('Authors', 'Publisher', 'Language'),
          processor=None):
    """Query function for the 'merge provider' (waterfall model)."""
    if not processor:
        processor = config.options.get('VIAS_MERGE', processor).lower()
        if not processor:  # pragma: no cover
            processor = 'serial'

    named_tasks = (('serv1', qserv1), ('serv2', qserv2))
    if processor == 'parallel':
        results = vias.parallel(named_tasks, isbn)
    elif processor == 'serial':
        results = vias.serial(named_tasks, isbn)
    elif processor == 'multi':
        results = vias.multi(named_tasks, isbn)

    r1 = results.get('serv1')
    r2 = results.get('serv2')

    if not r1 and not r2:
        return {}

    md = Metadata(r1) if r1 else {}

    if md and r2:
        # Try to complete Authors, Publisher and Language from serv2
        md.merge(r2, overwrite=overwrite)
        return md.value
    if not md and r2:  # pragma: no cover
        md = Metadata(r2)
        return md.value
    return md.value if not r2 and r1 else {}  # pragma: no cover

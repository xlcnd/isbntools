# -*- coding: utf-8 -*-
"""Extra methods."""

from ._metadata import query
from ._infogroup import infogroup
from ._wcated import query as qed
from ._msk import msk
from ._words import goos
from ._core import EAN13


def mask(isbn, separator='-'):
    """`Mask` a canonical ISBN."""
    return msk(isbn, separator)


def meta(isbn, service='default'):
    """Get metadata from worldcat.org ('wcat'), Google Books ('goob') , ..."""
    return query(isbn, service)


def info(isbn):
    """Get language or country assigned to this ISBN."""
    return infogroup(isbn)


def editions(isbn):
    """Return the list of ISBNs of editions related with this ISBN."""
    return qed(isbn)


def isbn_from_words(words):
    """Return the most probable ISBN from a list of words."""
    return goos(words)


def doi(isbn):
    """Return a DOI's ISBN-A from a ISBN-13."""
    return "10.%s.%s%s/%s%s" % \
           tuple(msk(EAN13(isbn), '-').split('-'))

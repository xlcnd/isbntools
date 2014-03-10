#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .metadata import query
from .infogroup import infogroup
from .dev.wcated import query as qed
from .mask import mask as msk


def mask(isbn, separator='-'):
    """ `Masks` a canonical ISBN """
    return msk(isbn, separator)


def meta(isbn, service='default'):
    """ Metadata from worldcat.org ('wcat'), Google Books ('goob') , ..."""
    return query(isbn, service)


def info(isbn):
    """ Language or country assigned to this ISBN """
    return infogroup(isbn)


def editions(isbn):
    """ Returns the list of ISBNs of editions related with this ISBN """
    return qed(isbn)

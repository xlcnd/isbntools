# -*- coding: utf-8 -*-


from .metadata import query
from .infogroup import infogroup
from .dev.wcated import query as qed
from .mask import mask as msk
from .words import goos


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


def isbn_from_words(words):
    """ Returns the most probable ISBN from a list of words from title
        and author's name (uses Google Search)
    """
    return goos(words)

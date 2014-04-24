# -*- coding: utf-8 -*-
"""
Queries the worldcat.org service for metadata
"""

import logging
from .webquery import query as wquery
from .data import stdmeta
from ..bouth23 import u
from .exceptions import (DataWrongShapeError, NoDataForSelectorError,
                         RecordMappingError)


UA = 'isbntools (gzip)'
SERVICE_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?'\
    'method=getMetadata&format=json&fl=*'
LOGGER = logging.getLogger(__name__)


def _mapper(isbn, records):
    """
    Mapping canonical <- records
    """
    # canonical:
    # -> ISBN-13, Title, Authors, Publisher, Year, Language
    try:
        # mapping: canonical <- records
        canonical = {}
        canonical['ISBN-13'] = u(isbn)
        canonical['Title'] = records.get('title', u('')).replace(' :', ':')
        canonical['Authors'] = [records.get('author', u(''))]
        canonical['Publisher'] = records.get('publisher', u(''))
        canonical['Year'] = records.get('year', u(''))
        canonical['Language'] = records.get('lang', u(''))
    except:
        raise RecordMappingError(isbn)
    # call stdmeta for extra cleanning and validation
    return stdmeta(canonical)


def _records(isbn, data):
    """
    Classifies (canonically) the parsed data
    """
    try:
        # put the selected data in records
        recs = data['list'][0]
    except:
        try:
            extra = data['stat']
            LOGGER.debug('DataWrongShapeError for %s with data %s',
                         isbn, extra)
        except:
            raise DataWrongShapeError(isbn)
        raise NoDataForSelectorError(isbn)

    # map canonical <- records
    return _mapper(isbn, recs)


def query(isbn):
    """
    Queries the worldcat.org service for metadata
    """
    data = wquery(SERVICE_URL % isbn, UA)
    return _records(isbn, data)

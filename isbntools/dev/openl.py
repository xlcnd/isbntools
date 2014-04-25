# -*- coding: utf-8 -*-
"""
Queries the openlibrary.org service for metadata
"""

import logging
from .webquery import query as wquery
from .data import stdmeta
from ..bouth23 import u
from .exceptions import NoDataForSelectorError, RecordMappingError


UA = 'isbntools (gzip)'
SERVICE_URL = 'http://openlibrary.org/api/books?bibkeys='\
    'ISBN:%s&format=json&jscmd=data'
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
        canonical['Authors'] = [a['name'] for a in
                                records.get('authors', ({'name': u('')},))]
        canonical['Publisher'] = records.get('publishers',
                                             [{'name': u('')}, ])[0]['name']
        canonical['Year'] = records.get('publish_date', u(',')).split(',')[1]
    except:   # pragma: no cover
        raise RecordMappingError(isbn)
    # call stdmeta for extra cleanning and validation
    return stdmeta(canonical)


def _records(isbn, data):
    """
    Classifies (canonically) the parsed data
    """
    try:
        # put the selected data in records
        records = data['ISBN:%s' % isbn]
    except:   # pragma: no cover
        raise NoDataForSelectorError(isbn)

    # map canonical <- records
    return _mapper(isbn, records)


def query(isbn):
    """
    Queries the openlibrary.org service for metadata
    """
    data = wquery(SERVICE_URL % isbn, UA)
    return _records(isbn, data)

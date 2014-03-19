#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from .webquery import WEBQuery
from .data import stdmeta
from .exceptions import (DataWrongShapeError, DataNotFoundError,
                         RecordMappingError)

UA = 'isbntools (gzip)'
SERVICE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn+%s&fields='\
    'items/volumeInfo(title,authors,publisher,publishedDate,language)'\
    '&maxResults=1'

logger = logging.getLogger(__name__)


class GOOBQuery(WEBQuery):
    """
    Queries the Google Books (JSON API v1) for metadata
    """

    def __init__(self, isbn):
        """
        Initializer & call webservice & handle errors
        """
        self.isbn = isbn
        WEBQuery.__init__(self, SERVICE_URL % isbn, UA)
        # lets us go with the default raw data_checker
        WEBQuery.check_data(self)

    def mapper(self, records):
        """
        Mapping canonical <- records
        """
        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        try:
            # mapping: canonical <- records
            canonical = {}
            canonical['ISBN-13'] = unicode(self.isbn)
            canonical['Title'] = records.get('title', u'').replace(' :', ':')
            canonical['Authors'] = records.get('authors', [])
            canonical['Publisher'] = records.get('publisher', u'')
            if 'publishedDate' in records \
               and len(records['publishedDate']) >= 4:
                canonical['Year'] = records['publishedDate'][0:4]
            else:         # pragma: no cover
                canonical['Year'] = u''
            canonical['Language'] = records.get('language', u'')
        except:
            raise RecordMappingError(self.isbn)
        # call stdmeta for extra cleanning and validation
        return stdmeta(canonical)

    def records(self):
        """
        Classifies (canonically) the parsed data
        """
        # this service uses JSON, so stay with the default parser
        data = WEBQuery.parse_data(self)
        try:
            # put the selected data in records
            records = data['items'][0]['volumeInfo']
        except:             # pragma: no cover
            try:
                extra = data['stat']
                logger.debug('DataWrongShapeError for % with data %s' %
                             (self.isbn, extra))
            except:
                raise DataWrongShapeError(self.isbn)
            raise DataNotFoundError(self.isbn)

        # map canonical <- records
        return self.mapper(records)


def query(isbn):
    """
    Function API to the class
    """
    q = GOOBQuery(isbn)
    return q.records()

# -*- coding: utf-8 -*-

import logging
from .webquery import WEBQuery
from .data import stdmeta
from .exceptions import (DataWrongShapeError, NoDataForSelectorError,
                         RecordMappingError)

UA = 'isbntools (gzip)'
SERVICE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn+%s&fields='\
    'items/volumeInfo(title,authors,publisher,publishedDate,language)'\
    '&maxResults=1'

LOGGER = logging.getLogger(__name__)


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

    @staticmethod
    def mapper(isbn, records):
        """
        Mapping canonical <- records
        """
        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        try:
            # mapping: canonical <- records
            canonical = {}
            canonical['ISBN-13'] = unicode(isbn)
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
            raise RecordMappingError(isbn)
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
                LOGGER.debug('DataWrongShapeError for %s with data %s',
                             self.isbn, extra)
            except:
                raise DataWrongShapeError(self.isbn)
            raise NoDataForSelectorError(self.isbn)

        # map canonical <- records
        return self.mapper(self.isbn, records)


def query(isbn):
    """
    Function API to the class
    """
    q = GOOBQuery(isbn)
    return q.records()

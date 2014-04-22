# -*- coding: utf-8 -*-

import logging
from .webquery import WEBQuery
from .data import stdmeta
from .exceptions import (DataWrongShapeError, NoDataForSelectorError,
                         RecordMappingError)


UA = 'isbntools (gzip)'
SERVICE_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?'\
    'method=getMetadata&format=json&fl=*'
LOGGER = logging.getLogger(__name__)


class WCATQuery(WEBQuery):
    """
    Queries the worldcat.org service for metadata
    """

    def __init__(self, isbn):
        """
        Initializer
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
            canonical['Authors'] = [records.get('author', u'')]
            canonical['Publisher'] = records.get('publisher', u'')
            canonical['Year'] = records.get('year', u'')
            canonical['Language'] = records.get('lang', u'')
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
            records = data['list'][0]
        except:
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
    q = WCATQuery(isbn)
    return q.records()

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import re
from .webquery import WEBQuery
from .data import stdmeta
from ..config import apikeys
from .exceptions import (WPDataWrongShapeError, WPDataNotFoundError,
                         WPRecordMappingError, WPNoAPIKeyError)


UA = 'isbntools (gzip)'
SERVICE_URL = 'http://isbndb.com/api/v2/json/%s/book/%s'

PATT_YEAR = re.compile(r'\d{4}')

logger = logging.getLogger(__name__)


class ISBNDBQuery(WEBQuery):
    """
    Queries the isbndb.org service for metadata
    """

    def __init__(self, isbn):
        """
        Initializer & call webservice & handle errors
        """
        self.isbn = isbn
        if not apikeys.get('isbndb'):
            raise WPNoAPIKeyError
        WEBQuery.__init__(self, SERVICE_URL %
                          (apikeys['isbndb'], isbn), UA)
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
            # assert self.isbn == records['isbn13'], "isbn was mungled!"
            canonical['Title'] = records.get('title', u'')
            authors = [a['name'] for a in records['author_data']]
            canonical['Authors'] = authors
            canonical['Publisher'] = records.get('publisher_name', u'')
            canonical['Year'] = u''
            if 'edition_info' in records:
                match = re.search(PATT_YEAR, records['edition_info'])
                if match:
                    canonical['Year'] = unicode(match.group(0))
            canonical['Language'] = records.get('language', u'')
        except:
            raise WPRecordMappingError(self.isbn)
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
            records = data['data'][0]
        except:
            try:
                extra = data['error']
                logger.debug('WPDataWrongShapeError for % with data %s' %
                             (self.isbn, extra))
            except:
                raise WPDataWrongShapeError(self.isbn)
            raise WPDataNotFoundError(self.isbn)

        # map canonical <- records
        return self.mapper(records)


def query(isbn):
    """
    Function API to the class
    """
    q = ISBNDBQuery(isbn)
    return q.records()

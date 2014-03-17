#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from .webquery import WEBQuery
from .data import stdmeta
from .exceptions import WPDataNotFoundError, WPRecordMappingError


UA = 'isbntools (gzip)'
SERVICE_URL = 'http://openlibrary.org/api/books?bibkeys='\
    'ISBN:%s&format=json&jscmd=data'

logger = logging.getLogger(__name__)


class OPENLQuery(WEBQuery):
    """
    Queries the openlibrary.org service for metadata
    """

    def __init__(self, isbn):
        """
        Initializer
        """
        self.isbn = isbn
        WEBQuery.__init__(self, SERVICE_URL % isbn, UA)
        # lets us go with the default raw data_checker
        WEBQuery.check_data(self)

    def records(self):
        """
        Classifies (canonically) the parsed data
        """
        # this service uses JSON, so stay with the default parser
        data = WEBQuery.parse_data(self)
        try:
            # put the selected data in records
            records = data['ISBN:%s' % self.isbn]
        except:
            raise WPDataNotFoundError(self.isbn)

        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        try:
            canonical = {}
            canonical['ISBN-13'] = unicode(self.isbn)
            canonical['Title'] = records.get('title', u'').replace(' :', ':')
            canonical['Authors'] = [a['name'] for a in records['authors']]
            canonical['Publisher'] = records['publishers'][0]['name']
            canonical['Year'] = records['publish_date'].split(',')[1]
        except:
            raise WPRecordMappingError(self.isbn)
        # call stdmeta for extra cleanning and validation
        return stdmeta(canonical)


def query(isbn):
    """
    Function API to the class
    """
    q = OPENLQuery(isbn)
    return q.records()

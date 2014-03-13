#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from .webquery import WEBQuery
from .exceptions import WPDataWrongShapeError


UA = 'isbntools (gzip)'
SERVICE_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?'\
    'method=getMetadata&format=json&fl=*'

logger = logging.getLogger(__name__)


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
                logger.debug('WPDataWrongShapeError for % with data %s' %
                             (self.isbn, extra))
            except:
                pass
            raise WPDataWrongShapeError(self.isbn)

        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        canonical = {}
        canonical['ISBN-13'] = self.isbn
        canonical['Title'] = records['title'].replace(' :', ':')
        canonical['Authors'] = '[%s]' % records.get('author', '')
        canonical['Publisher'] = records['publisher']
        canonical['Year'] = records['year']
        canonical['Language'] = records['lang']

        return canonical


def query(isbn):
    """
    Function API to the class
    """
    q = WCATQuery(isbn)
    return q.records()

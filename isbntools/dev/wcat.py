#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .webquery import WEBQuery

UA = 'isbntools (gzip)'
SERVICE_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?'\
    'method=getMetadata&format=json&fl=*'


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

    def records(self):
        """
        Classifies (canonically) the parsed data
        """
        WEBQuery.check_data(self)
        data = WEBQuery.parse_data(self)
        if 'list' in data:
            # put the selected data in records 
            records = data['list'][0]
        else:
            raise Exception('Error:%s' % data['stat'])

        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        canonical = {}
        canonical['Title'] = records['title'].replace(' :', ':')
        canonical['Language'] = records['lang']
        canonical['Publisher'] = records['publisher']
        canonical['Year'] = records['year']
        canonical['ISBN-13'] = self.isbn
        canonical['Authors'] = '[%s]' % records.get('author', '')
        
        return canonical


def query(isbn):
    """
    Function API to the class
    """
    q = WCATQuery(isbn)
    return q.records()

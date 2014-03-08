#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import webservice
from .webquery import WEBQuery


UA = 'isbntools (gzip)'

SERVICE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn+%s&fields='\
    'items/volumeInfo(title,authors,publisher,publishedDate,language)'\
    '&maxResults=1'


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

    def records(self):
        """
        Classifies (canonically) the parsed data
        """
        WEBQuery.check_data(self)
        data = WEBQuery.parse_data(self)
        if 'items' in data:
            records = data['items'][0]['volumeInfo']
        else:
            raise Exception('Error:no data for %s' % self.isbn)

        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        canonical = {}
        canonical['Title'] = records['title'].replace(' :', ':')
        canonical['Language'] = records['language']
        canonical['Publisher'] = records.get('publisher', '')
        if 'publishedDate' in records and len(records['publishedDate']) >= 4:
            canonical['Year'] = records['publishedDate'][0:4]
        else:
            canonical['Year'] = ''
        canonical['ISBN-13'] = self.isbn
        canonical['Authors'] = repr(records.get('authors', []))
        return canonical


def query(isbn):
    """
    Function API to the class
    """
    q = GOOBQuery(isbn)
    return q.records()

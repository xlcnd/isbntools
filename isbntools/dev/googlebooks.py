#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from . import webservice


UA = 'isbntools (gzip)'

SERVICE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn+%s&fields='\
    'items/volumeInfo(title,authors,publisher,publishedDate,language)'\
    '&maxResults=1'

OUT_OF_SERVICE = 'out of service'


class GOOBQuery(object):
    """
    Queries the Google Books (JSON API v1) for metadata
    """

    def __init__(self, isbn):
        """
        Initializer & call webservice & handle errors
        """
        self.isbn = isbn
        data = webservice.query(SERVICE_URL % isbn, UA)

        if data == '{}':
            raise Exception('Book not found! Check the isbn...%s' % isbn)
        if OUT_OF_SERVICE in data:
            raise Exception('Temporarily out of service. Try later!')
        self.data = data

    def _parse_data(self):
        """
        Parse the data from JSON -> PY
        """
        data = json.loads(self.data)
        if 'items' in data:
            return data['items'][0]['volumeInfo']
        else:
            raise Exception('Error:no data for %s' % self.isbn)

    def records(self):
        """
        Classifies canonically the records from the parsed response
        """
        records = self._parse_data()

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

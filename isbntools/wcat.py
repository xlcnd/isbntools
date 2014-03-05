#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import webservice


UA = 'isbntools (gzip)'
# TODO use format=python?
SERVICE_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?'\
    'method=getMetadata&format=json&fl=*'
OUT_OF_SERVICE = 'Temporarily out of service'
BOOK_NOT_FOUND = 'No results match your search'


class WCATQuery(object):
    """
    Queries the Google Books (JSON API v1) for metadata
    """

    def __init__(self, isbn):
        """
        Constructor
        """
        self.isbn = isbn
        data = webservice.query(SERVICE_URL % isbn, UA)

        if BOOK_NOT_FOUND in data:
            raise Exception('Book not found! Check the isbn...%s' % isbn)
        if OUT_OF_SERVICE in data:
            raise Exception('Temporarily out of service. Try later!')
        self.data = data

    def _parse_data(self):
        """
        Parse the data from the service (JSON -> py obj)
        """
        data = json.loads(self.data)
        if 'list' in data:
            return data['list'][0]
        else:
            raise Exception('Error:%s' % data['stat'])

    def records(self):
        """
        Classifies canonically the records from the parsed response
        """
        records = self._parse_data()

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
    Command Line API to the class
    """
    query = WCATQuery(isbn)
    return query.records()

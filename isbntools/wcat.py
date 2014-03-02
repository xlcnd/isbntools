#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import sys
import json
import webservice


UA = 'isbntools (gzip)'
SERVICE_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?method=getMetadata&format=json&fl=*'
OUT_OF_SERVICE = 'Temporarily out of service'
BOOK_NOT_FOUND = 'No results match your search'
PATT_YEAR = re.compile(r'\d{4}')


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

        if 'author' in records:
            canonical['Authors'] = '[%s]' % records['author']
        else:
            canonical['Authors'] = []
        return canonical


def query(isbn):
    """
    Command Line API to the class
    """
    query = WCATQuery(isbn)
    return query.records()


if __name__ == "__main__":
    r = query(sys.argv[1].replace('-', ''))
    sys.stdout.write('ISBN-13: %s\nTitle: %s\nAuthors: %s\nPublisher: %s\nYear: %s\n' %
          (r['ISBN-13'], r['Title'], r['Authors'], r['Publisher'], r['Year']))

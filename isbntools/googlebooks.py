#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import re
import sys
import json
import webservice


UA = 'isbntools (gzip)'
SERVICE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn+%s'\
              '&fields=items/volumeInfo(title,authors,publisher,publishedDate,language)'
OUT_OF_SERVICE = 'Temporarily out of service'
BOOK_NOT_FOUND = 'No results match your search'
PATT_YEAR = re.compile(r'\d{4}')


class GOOBQuery(object):
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
        Parse the data from the service
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
        if 'publisher' in records:
            canonical['Publisher'] = records['publisher']
        else:
            canonical['Publisher'] = ''
        if 'publishedDate' in records and len(records['publishedDate']) >= 4:
            canonical['Year'] = records['publishedDate'][0:4]
        else:
            canonical['Year'] = ''
        canonical['ISBN-13'] = self.isbn
        if 'authors' in records:
            canonical['Authors'] = repr(records['authors'])
        else:
            canonical['Authors'] = []
        return canonical


def query(isbn):
    """
    Command Line API to the class
    """
    query = GOOBQuery(isbn)
    return query.records()


if __name__ == "__main__":
    r = query(sys.argv[1].replace('-', ''))
    sys.stdout.write('ISBN-13: %s\nTitle: %s\nAuthors: %s\nPublisher: %s\nYear: %s\n' %
          (r['ISBN-13'], r['Title'], r['Authors'], r['Publisher'], r['Year']))

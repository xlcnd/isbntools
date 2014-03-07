#!/usr/bin/env python
# -*- coding: utf-8 -*-


# To use the `isbndb.com` web service you should get an **API KEY** that you
# should write in the file `keys.py`.

# It is very easy to add *new* providers of metadata. Just write a file
# following the pattern of `wcat.py`, `googlebooks.py`, ... in the `isbntools`
# folder. Then you have to register it in the `registry.py`, and *thats all*!


import re
import json
from . import webservice
from .keys import keys

UA = 'isbntools (gzip)'

SERVICE_URL = 'http://isbndb.com/api/v2/json/%s/book/%s'
OUT_OF_SERVICE = 'Temporarily out of service'
BOOK_NOT_FOUND = 'No results match your search'

PATT_YEAR = re.compile(r'\d{4}')


class ISBNDBQuery():
    """
    Queries the isbndb.org service for metadata
    """

    def __init__(self, isbn):
        """
        Initializer & call webservice & handle errors
        """
        self.isbn = isbn
        data = webservice.query(SERVICE_URL % (keys['isbndb'], isbn), UA)

        if BOOK_NOT_FOUND in data:
            raise Exception('Book not found! Check the isbn...%s' % isbn)
        if OUT_OF_SERVICE in data:
            raise Exception('Temporarily out of service. Try later!')
        self.data = data

    def _parse_data(self):
        """
        Parse the data from JSON -> PY
        """
        data = json.loads(self.data)  # <-- data is now unicode
        if 'data' in data:
            return data['data'][0]
        else:
            raise Exception('ERROR:%s' % data['error'])

    def records(self):
        """
        Classifies canonically the records from the parsed response
        """
        records = self._parse_data()

        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        canonical = {}

        canonical['Title'] = records['title']
        canonical['Language'] = records['language'] or 'English'
        canonical['Publisher'] = records['publisher_name']
        canonical['ISBN-13'] = self.isbn
        assert self.isbn == records['isbn13'], "isbn was mungled!"
        canonical['Year'] = ''
        if 'edition_info' in records:
            match = re.search(PATT_YEAR, records['edition_info'])
            if match:
                canonical['Year'] = match.group(0)

        authors = [a['name'] for a in records['author_data']]
        canonical['Authors'] = repr(authors)

        return canonical


def query(isbn):
    """
    Function API to the class
    """
    q = ISBNDBQuery(isbn)
    return q.records()

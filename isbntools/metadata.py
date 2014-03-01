#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Queries worldcat.org for metadata

NOTE: uses the xisbn service
"""

import httplib2
import re
import sys
import json

OUT_OF_SERVICE = 'Temporarily out of service'
BOOK_NOT_FOUND = 'No results match your search'
SIGN_UA = 'isbntools (python)'
SEARCH_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?method=getMetadata&format=json&fl=*'
PATT_YEAR = re.compile(r'\d{4}')


class WCATQuery():

    def __init__(self):
        """
        Constructor
        """
        self.http = httplib2.Http()

    def _request(self, isbn):
        """
        Puts the request to the service
        """
        headers = {'connection': 'keep-alive', 'User-Agent': SIGN_UA}
        resp, content = self.http.request(SEARCH_URL % isbn, headers=headers)
        if resp['status'] != '200':
            raise Exception('Server error! Check the url...%s' % resp)
        if BOOK_NOT_FOUND in content:
            raise Exception('Book not found! Check the isbn...%s' % isbn)
        if OUT_OF_SERVICE in content:
            raise Exception('Temporarily out of service. Try later!')
        self.response = content

    def _parse_response(self, isbn):
        """
        Parse the response from the service
        """
        data = json.loads(self.response)
        if 'list' in data:
            return data['list'][0]
        else:
            raise Exception('Error:%s' % data['stat'])

    def records(self, isbn):
        """
        Classifies canonically the records from the parsed response
        """
        self._request(isbn)
        records = self._parse_response(isbn)

        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        canonical = {}
        canonical['Title'] = records['title'].replace(' :', ':')
        canonical['Language'] = records['lang']
        canonical['Publisher'] = records['publisher']
        canonical['Year'] = records['year']
        canonical['ISBN-13'] = isbn

        if 'author' in records:
            canonical['Authors'] = records['author']
        else:
            canonical['Authors'] = []
        return canonical


def query(isbn):
    """
    Command Line API to the class
    """
    query = WCATQuery()
    return query.records(isbn)




if __name__ == "__main__":
    r = query(sys.argv[1].replace('-',''))
    sys.stdout.write('ISBN-13: %s\nTitle: %s\nAuthors: %s\nPublisher: %s\nYear: %s\n' %
          (r['ISBN-13'], r['Title'], r['Authors'], r['Publisher'], r['Year']))

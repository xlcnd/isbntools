#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Queries worldcat.org for metadata

NOTE: uses the xisbn service
"""

import urllib2
import re
import sys
import json

OUT_OF_SERVICE = 'Temporarily out of service'
BOOK_NOT_FOUND = 'No results match your search'
SIGN_UA = 'isbntools (python)'
SEARCH_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?method=getMetadata&format=json&fl=*'
PATT_YEAR = re.compile(r'\d{4}')


class WCATQuery(object):

    def __init__(self, isbn):
        """
        Constructor
        """
        self.isbn = isbn
        headers = {'User-Agent': SIGN_UA}
        request = urllib2.Request(SEARCH_URL % isbn, headers=headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            raise Exception('Error:%s' % e.code)
        except urllib2.URLError as e:
            raise Exception('Error:%s' % e.reason)

        content = response.read()
        if BOOK_NOT_FOUND in content:
            raise Exception('Book not found! Check the isbn...%s' % isbn)
        if OUT_OF_SERVICE in content:
            raise Exception('Temporarily out of service. Try later!')
        self.content = content

    def _parse_content(self):
        """
        Parse the content from the service
        """
        data = json.loads(self.content)
        if 'list' in data:
            return data['list'][0]
        else:
            raise Exception('Error:%s' % data['stat'])

    def records(self):
        """
        Classifies canonically the records from the parsed response
        """
        records = self._parse_content()

        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        canonical = {}
        canonical['Title'] = records['title'].replace(' :', ':')
        canonical['Language'] = records['lang']
        canonical['Publisher'] = records['publisher']
        canonical['Year'] = records['year']
        canonical['ISBN-13'] = self.isbn

        if 'author' in records:
            canonical['Authors'] = records['author']
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

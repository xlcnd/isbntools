#!/usr/bin/env python
# -*- coding: utf-8 -*-


import webservice
from ast import literal_eval


UA = 'isbntools (gzip)'

SERVICE_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?'\
              'method=getEditions&format=python'

OUT_OF_SERVICE = 'Temporarily out of service'
BOOK_NOT_FOUND = 'No results match your search'


class WCATEdQuery(object):
    """
    Queries the worldcat.org service for related ISBNs
    """

    def __init__(self, isbn):
        """
        Initializer
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
        Parse the data from the service (repr -> obj)
        """
        data = literal_eval(self.data)
        if 'list' in data:
            return [ib['isbn'][0] for ib in data['list']]
        else:
            raise Exception('Error:%s' % data['stat'])

    def records(self):
        """
        Returns the records from the parsed response
        """
        records = self._parse_data()
        return records


def query(isbn):
    """
    Command Line API to the class
    """
    q = WCATEdQuery(isbn)
    return q.records()

#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ast import literal_eval
from .webquery import WEBQuery

UA = 'isbntools (gzip)'
SERVICE_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?'\
              'method=getEditions&format=python'


class WCATEdQuery(WEBQuery):
    """
    Queries the worldcat.org service for related ISBNs
    """

    def __init__(self, isbn):
        """
        Initializer & call webservice & handle errors
        """
        self.isbn = isbn
        WEBQuery.__init__(self, SERVICE_URL % isbn, UA)

    def records(self):
        """
        Returns the records from the parsed response
        """
        WEBQuery.check_data(self)
        data = WEBQuery.parse_data(self, parser=literal_eval)

        if 'list' in data:
            records = [ib['isbn'][0] for ib in data['list']]
        else:
            raise Exception('Error:%s' % data['stat'])
        return records


def query(isbn):
    """
    Function API to the class
    """
    q = WCATEdQuery(isbn)
    return q.records()

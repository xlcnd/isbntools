# -*- coding: utf-8 -*-

import logging
from ast import literal_eval
from .webquery import WEBQuery
from .exceptions import DataWrongShapeError, NoDataForSelectorError

LOGGER = logging.getLogger(__name__)
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
        # lets us go with the default raw data_checker
        WEBQuery.check_data(self)

    def records(self):
        """
        Returns the records from the parsed response
        """
        # this service sends Python, so pass the ast.literal_eval parser
        data = WEBQuery.parse_data(self, parser=literal_eval)
        try:
            # put the selected data in records
            records = [ib['isbn'][0] for ib in data['list']]
        except:    # pragma: no cover
            try:
                extra = data['stat']
                LOGGER.debug('DataWrongShapeError for %s with data %s',
                             self.isbn, extra)
            except:
                raise DataWrongShapeError(self.isbn)
            raise NoDataForSelectorError(self.isbn)
        return records


def query(isbn):
    """
    Function API to the class
    """
    q = WCATEdQuery(isbn)
    return q.records()

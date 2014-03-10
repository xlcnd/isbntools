#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from . import webservice
from .exceptions import WQDataNotFoundError, WQServiceIsDownError

UA = 'isbntools (gzip)'

OUT_OF_SERVICE = 'Temporarily out of service'
BOOK_NOT_FOUND = 'No results match your search'


class WEBQuery(object):
    """
    Base class to query a webservice and parse the result to py objects
    """

    def __init__(self, service_url, ua=UA):
        """
        Initializer & call webservice
        """
        self.data = webservice.query(service_url, ua)

    def check_data(self):
        """
        Checks the data & handle errors
        """
        if self.data == '{}':
            raise WQDataNotFoundError()
        if BOOK_NOT_FOUND in self.data:
            raise WQDataNotFoundError()
        if OUT_OF_SERVICE in self.data:
            raise WQServiceIsDownError()

    def parse_data(self, parser=json.loads):
        """
        Parse the data (default JSON -> PY)
        """
        return parser(self.data)   # <-- data is now unicode

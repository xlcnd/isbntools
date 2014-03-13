#!/usr/bin/env python
# -*- coding: utf-8 -*-


# To use the `isbndb.com` web service you should get an **API KEY** that you
# should write in the file `keys.py`.

# It is very easy to add *new* providers of metadata. Just write a file
# following the pattern of `wcat.py`, `googlebooks.py`, ...
# in the `isbntools/dev` folder. Then you have to register it in the
# `registry.py`, and *thats all*!


import logging
import re
from .webquery import WEBQuery
from .keys import keys
from .exceptions import WPDataWrongShapeError


UA = 'isbntools (gzip)'
SERVICE_URL = 'http://isbndb.com/api/v2/json/%s/book/%s'

PATT_YEAR = re.compile(r'\d{4}')

logger = logging.getLogger(__name__)


class ISBNDBQuery(WEBQuery):
    """
    Queries the isbndb.org service for metadata
    """

    def __init__(self, isbn):
        """
        Initializer & call webservice & handle errors
        """
        self.isbn = isbn
        WEBQuery.__init__(self, SERVICE_URL % (keys['isbndb'], isbn), UA)
        # lets us go with the default raw data_checker
        WEBQuery.check_data(self)

    def records(self):
        """
        Classifies (canonically) the parsed data
        """
        # this service uses JSON, so stay with the default parser
        data = WEBQuery.parse_data(self)
        try:
            # put the selected data in records
            records = data['data'][0]
        except:
            try:
                extra = data['error']
                logger.debug('WPDataWrongShapeError for % with data %s' %
                             (self.isbn, extra))
            except:
                pass
            raise WPDataWrongShapeError(self.isbn)

        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        canonical = {}
        canonical['ISBN-13'] = self.isbn
        assert self.isbn == records['isbn13'], "isbn was mungled!"
        canonical['Title'] = records['title']
        authors = [a['name'] for a in records['author_data']]
        canonical['Authors'] = repr(authors)
        canonical['Publisher'] = records['publisher_name']
        canonical['Year'] = ''
        if 'edition_info' in records:
            match = re.search(PATT_YEAR, records['edition_info'])
            if match:
                canonical['Year'] = match.group(0)
        canonical['Language'] = records.get('language', 'English')

        return canonical


def query(isbn):
    """
    Function API to the class
    """
    q = ISBNDBQuery(isbn)
    return q.records()

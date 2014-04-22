# -*- coding: utf-8 -*-

import logging
from .webquery import WEBQuery
from .data import stdmeta
from .exceptions import (DataWrongShapeError, NoDataForSelectorError,
                         RecordMappingError)

UA = 'isbntools (gzip)'
SERVICE_URL = 'https://www.googleapis.com/books/v1/volumes?q=%s&fields='\
    'items/volumeInfo(title,authors,publisher,publishedDate,language,industryIdentifiers)'\
    '&maxResults=10'

LOGGER = logging.getLogger(__name__)


class GOOMQuery(WEBQuery):
    """
    Queries the Google Books (JSON API v1) for metadata
    """

    def __init__(self, words):
        """
        Initializer & call webservice & handle errors
        """
        self.words = words
        WEBQuery.__init__(self, SERVICE_URL % words, UA)
        # lets us go with the default raw data_checker
        WEBQuery.check_data(self)

    @staticmethod
    def mapper(record):
        """
        Mapping canonical <- record
        """
        # canonical:
        # -> ISBN-13, Title, Authors, Publisher, Year, Language
        try:
            # mapping: canonical <- records
            canonical = {}
            isbn = None
            for id in record['industryIdentifiers']:
                if id['type'] == 'ISBN_13':
                    isbn = id['identifier']
                    break
            if not isbn:
                return
            canonical['ISBN-13'] = isbn
            canonical['Title'] = record.get('title', u'').replace(' :', ':')
            canonical['Authors'] = record.get('authors', [])
            canonical['Publisher'] = record.get('publisher', u'')
            if 'publishedDate' in record \
               and len(record['publishedDate']) >= 4:
                canonical['Year'] = record['publishedDate'][0:4]
            else:         # pragma: no cover
                canonical['Year'] = u''
            canonical['Language'] = record.get('language', u'')
        except:
            raise RecordMappingError(isbn)
        # call stdmeta for extra cleanning and validation
        return stdmeta(canonical)

    def records(self):
        """
        Classifies (canonically) the parsed data
        """
        # this service uses JSON, so stay with the default parser
        data = WEBQuery.parse_data(self)
        try:
            # put the selected data in records
            records = [d['volumeInfo'] for d in data['items']]
        except:             # pragma: no cover
            try:
                extra = data['stat']
                LOGGER.debug('DataWrongShapeError for %s with data %s',
                             self.words, extra)
            except:
                raise DataWrongShapeError(self.words)
            raise NoDataForSelectorError(self.words)

        # map canonical <- records
        return [self.mapper(r) for r in records if self.mapper(r)]


def query(words):
    """
    Function API to the class
    """
    q = GOOMQuery(words.replace(' ', '+'))
    return q.records()

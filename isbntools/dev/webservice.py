# -*- coding: utf-8 -*-


import logging
import urllib
import urllib2
import gzip
from StringIO import StringIO
from .exceptions import ISBNToolsHTTPError, ISBNToolsURLError

UA = 'webservice (gzip)'

LOGGER = logging.getLogger(__name__)


class WEBService(object):
    """
    Class to query web services
    """

    def __init__(self, url, user_agent=UA, values=None):
        """
        Initializer (KISS without subclassing urllib2.BaseHandler!)
        """
        self._url = url
        # headers to accept gzipped content
        headers = {'Accept-Encoding': 'gzip', 'User-Agent': user_agent}
        # if 'data' it does a PUT request (data must be urlencoded)
        data = urllib.urlencode(values) if values else None
        self._request = urllib2.Request(url, data, headers=headers)
        self.response = None

    def _response(self):
        try:
            self.response = urllib2.urlopen(self._request)
        except urllib2.HTTPError as e:
            LOGGER.critical('ISBNToolsHTTPError for %s with code %s',
                            self._url, e.code)
            raise ISBNToolsHTTPError(e.code)
        except urllib2.URLError as e:
            LOGGER.critical('ISBNToolsURLError for %s with reason %s',
                            self._url, e.reason)
            raise ISBNToolsURLError(e.reason)

    def data(self):
        """
        Returns the uncompressed data
        """
        self._response()
        if self.response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(self.response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = self.response.read()
        return data


def query(url, user_agent=UA, values=None):
    """
    Query to a web service
    """
    service = WEBService(url, user_agent, values)
    return service.data()

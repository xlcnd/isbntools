#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import urllib
import urllib2
import gzip
from StringIO import StringIO

UA = 'webservice (gzip)'

# socket timeout is not exposed at urllib2 level
# so I had to import the module and set a default
# value for all the sockets (timeout in seconds) 
timeout = 10
socket.setdefaulttimeout(timeout)


class WEBQuery(object):
    """
    Class to query web services
    """

    def __init__(self, url, user_agent=UA, values=None):
        """
        Initializer (KISS without subclassing urllib2.BaseHandler!)
        """
        # headers to accept gzipped content
        headers = {'Accept-Encoding': 'gzip', 'User-Agent': user_agent}
        # if 'data' it does a PUT request (data must be urlencoded)
        if values:
            data = urllib.urlencode(values)
        else:
            data = None
        request = urllib2.Request(url, data, headers=headers)
        try:
            self.response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            raise Exception('Error:%s' % e.code)
        except urllib2.URLError as e:
            raise Exception('Error:%s' % e.reason)

    def data(self):
        """
        Returns the uncompressed data
        """
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
        service = WEBQuery(url, user_agent, values)
        return service.data()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket 
from .registry import services

# socket timeout is not exposed at urllib2 level so I had to import the 
# module and set a default value for all the sockets (timeout in seconds)
# however this should be done at top level due to strong side effects...
socket.setdefaulttimeout(10)

def query(isbn, service='default', udf=None):
    """
    Queries worldcat.org, Google Books (JSON API), ... for metadata
    """
    if udf:
        return udf(service, isbn)
    if service not in services:
        raise Exception(('Error:%s is not a recognized service!' % service))
    return services[service](isbn)

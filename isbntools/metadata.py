#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket 
from .registry import services

# socket timeout is not exposed at urllib2 level so I had to import the 
# module and set a default value for all the sockets (timeout in seconds)
# however this should be done at top level due to strong side effects...
socket.setdefaulttimeout(10)

def query(isbn, service='default'):
    """
    Queries worldcat.org, Google Books (JSON API), ... for metadata
    """
    if service not in services:
        print(('Error:%s is not a recognized service!' % service))
        return
    return services[service](isbn)

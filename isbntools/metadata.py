#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ConfigParser
import socket
from . import config
from .registry import services, setdefaultservice
from .exceptions import NotRecognizedServiceError

# defaults parameters are in config.py they can be overwritten in
# .isbntools.conf at users's $HOME directory (UNIX)

# get defaults
SOCKETS_TIMEOUT = float(config.SOCKETS_TIMEOUT)
THREADS_TIMEOUT = float(config.THREADS_TIMEOUT)

if os.name == 'nt':
    # WINDOWS -- conf NOT IMPLEMENTED (sorry)!
    pass
else:
    # UNIX -- including Mac OSX
    try:
        # read conf file
        conf = ConfigParser.ConfigParser()
        conf.read(['/etc/isbntools/.isbntools.conf',
                  os.path.expanduser('~/.isbntools.conf')])

        if conf.has_section('SYS'):
            # get user defined values for timeouts
            SOCKETS_TIMEOUT = float(conf.get('SYS', 'SOCKETS_TIMEOUT'))
            THREADS_TIMEOUT = float(conf.get('SYS', 'THREADS_TIMEOUT'))

        if conf.has_section('SERVICES'):
            # register API KEY
            ISBNDB_API_KEY = conf.get('SERVICES', 'ISBNDB_API_KEY')
            config.add_apikey('isbndb', ISBNDB_API_KEY)
            # set default service
            DEFAULT_SERVICE = conf.get('SERVICES', 'DEFAULT_SERVICE')
            if DEFAULT_SERVICE:
                setdefaultservice(DEFAULT_SERVICE)
    except:
        pass

# socket timeout is not exposed at urllib2 level so I had to import the
# module and set a default value for all the sockets (timeout in seconds)
# however this should be done at top level due to strong side effects...
socket.setdefaulttimeout(SOCKETS_TIMEOUT)
config.setthreadstimeout(THREADS_TIMEOUT)


def query(isbn, service='default'):
    """
    Queries worldcat.org, Google Books (JSON API), ... for metadata
    """
    if service != 'default' and service not in services:
        raise NotRecognizedServiceError(service)
    return services[service](isbn)

# -*- coding: utf-8 -*-

import os
import sys
try:                                 # pragma: no cover
    import configparser
except ImportError:                  # pragma: no cover
    import ConfigParser as configparser
import socket
from . import config
from . import registry

# NOTE: THIS CODE RUNS ON IMPORT!

# defaults parameters are in config.py they can be overwritten in
# isbntools.conf at users's $HOME/.isbntools directory (UNIX)

# get defaults
SOCKETS_TIMEOUT = float(config.SOCKETS_TIMEOUT)
THREADS_TIMEOUT = float(config.THREADS_TIMEOUT)


def is_virtual():
    import sys
    return True if hasattr(sys, 'real_prefix') else False


try:
    # read conf file
    conf = configparser.ConfigParser()
    if is_virtual():
        conf.read([os.path.join(sys.prefix, 'isbntools.conf')])
    else:
        if os.name == 'nt':          # pragma: no cover
            conf.read([os.path.join(os.getenv('APPDATA'),
                      'isbntools/isbntools.conf')])
        else:                        # pragma: no cover
            conf.read(['/etc/isbntools/.isbntools.conf',
                       '/usr/local/.isbntools.conf',
                       '/usr/local/bin/.isbntools.conf',
                      os.path.expanduser('~/.isbntools.conf'),
                      os.path.expanduser('~/.isbntools/isbntools.conf')])

    if conf.has_section('SYS'):
        # get user defined values for timeouts
        SOCKETS_TIMEOUT = float(conf.get('SYS', 'SOCKETS_TIMEOUT'))
        THREADS_TIMEOUT = float(conf.get('SYS', 'THREADS_TIMEOUT'))

    if conf.has_section('SERVICES'):
        for o, v in conf.items('SERVICES'):
            if o.upper() == 'DEFAULT_SERVICE':
                registry.setdefaultservice(v)
                continue
            if 'api_key' in o:       # pragma: no cover
                name = o[:-8]
                config.add_apikey(name, v)
            else:
                config.set_option(o.upper(), v)

    if conf.has_section('PLUGINS'):  # pragma: no cover
        for o, v in conf.items('PLUGINS'):
            plugin = registry.load_plugin(o, v)
            if plugin:
                registry.add_service(o, plugin.query)

except:                              # pragma: no cover
    pass

# socket timeout is not exposed at urllib2 level so I had to import the
# module and set a default value for all the sockets (timeout in seconds)
# however this should be done at top level due to strong side effects...
socket.setdefaulttimeout(SOCKETS_TIMEOUT)
config.setthreadstimeout(THREADS_TIMEOUT)

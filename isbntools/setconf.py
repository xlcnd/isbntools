# -*- coding: utf-8 -*-
"""Read and set config parameters."""

import os
import sys
try:                                 # pragma: no cover
    import configparser
except ImportError:                  # pragma: no cover
    import ConfigParser as configparser
import socket
from . import config
from . import registry
from .dev.lab import in_virtual

# NOTE: THIS CODE RUNS ON IMPORT!

# defaults parameters are in config.py they can be overwritten in
# isbntools.conf at users's $HOME/.isbntools directory (UNIX)

# get defaults
SOCKETS_TIMEOUT = float(config.SOCKETS_TIMEOUT)
THREADS_TIMEOUT = float(config.THREADS_TIMEOUT)

# setup paths for contrib
pkg_path = os.path.dirname(registry.__file__)
plugins_path = os.path.join(pkg_path, 'contrib/plugins')

try:
    # read conf file
    conf = configparser.ConfigParser()
    # read defaults
    with open(os.path.join(pkg_path, 'isbntools.conf.py'), 'r') as f:
        conf.readfp(f)
    # read user options
    if in_virtual():                 # pragma: no cover
        conf.files = conf.read([os.path.join(sys.prefix, 'isbntools.conf')])
    else:
        if os.name == 'nt':          # pragma: no cover
            conf.files = conf.read([
                os.path.join(os.getenv('APPDATA'), 'isbntools/isbntools.conf')
            ])
        else:                        # pragma: no cover
            conf.files = conf.read([
                '/etc/.isbntools/isbntools.conf',
                '/usr/local/bin/isbntools.conf',
                '/usr/local/isbntools.conf',
                os.path.expanduser('~/.isbntools.conf'),
                os.path.expanduser('~/.local/.isbntools/isbntools.conf'),
                os.path.expanduser('~/.isbntools/isbntools.conf'),
            ])

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
            path = v if '/' in v or '\\' in v else plugins_path
            plugin = registry.load_plugin(o, path)
            if plugin:
                registry.add_service(o, plugin.query)

    if conf.has_section('MISC'):     # pragma: no cover
        for o, v in conf.items('MISC'):
            config.set_option(o.upper(), v)

    if conf.has_section('MODULES'):  # pragma: no cover
        for o, v in conf.items('MODULES'):
            config.set_option(o.upper(), v)

except:                              # pragma: no cover
    pass

# socket timeout is not exposed at urllib2 level so I had to import the
# module and set a default value for all the sockets (timeout in seconds)
# however this should be done at top level due to strong side effects...
socket.setdefaulttimeout(SOCKETS_TIMEOUT)
config.setthreadstimeout(THREADS_TIMEOUT)

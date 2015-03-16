# -*- coding: utf-8 -*-
"""Read and set config parameters."""

try:                                 # pragma: no cover
    import configparser
except ImportError:                  # pragma: no cover
    import ConfigParser as configparser
import logging
import os
import socket
import sys

from pkg_resources import iter_entry_points

from isbnlib import config
from isbnlib import registry

from ._exceptions import PluginNotLoadedError


# <--- NOTE: THIS CODE RUNS ON IMPORT! --->


# env
VIRTUAL = True if hasattr(sys, 'real_prefix') else False
WINDOWS = os.name == 'nt'

# defaults parameters can be overwritten in
# isbntools.conf at users's $HOME/.isbntools directory (UNIX)

DEFAULTS = r"""
[MISC]
REN_FORMAT={firstAuthorLastName}{year}_{title}_{isbn}
DEBUG=False
[SYS]
SOCKETS_TIMEOUT=12
THREADS_TIMEOUT=11
[SERVICES]
DEFAULT_SERVICE=merge
VIAS_MERGE=serial
[PLUGINS]
[MODULES]
"""

# get defaults
SOCKETS_TIMEOUT = float(config.SOCKETS_TIMEOUT)
THREADS_TIMEOUT = float(config.THREADS_TIMEOUT)

# setup paths for contrib
pkg_path = os.path.dirname(os.path.abspath(__file__))
plugins_path = os.path.join(pkg_path, 'contrib/plugins')


# set conf path
CONF_PATH = None


def setconfpath(confpath):
    """Set the directory of the conf file."""
    global CONF_PATH
    CONF_PATH = confpath
    config.set_option('CONF_PATH', confpath)


# read/set conf file
conf = configparser.ConfigParser()
# read DEFAULTS (in memory)
try:                             # pragma: no cover
    conf.read_string(DEFAULTS)            # PY3
except:                          # pragma: no cover
    import io
    conf.readfp(io.BytesIO(DEFAULTS))     # PY2
# read user options
if VIRTUAL:                    # pragma: no cover
    conf.files = conf.read(
        [os.path.join(sys.prefix,
         os.path.join('isbntools', 'isbntools.conf'))
         ])
else:
    if WINDOWS:                # pragma: no cover
        conf.files = conf.read(
            [os.path.join(os.getenv('APPDATA'),
                          os.path.join('isbntools', 'isbntools.conf'))
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
try:
    setconfpath(os.path.dirname(conf.files[0]))
except:
    pass


# set options
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

if conf.has_section('MISC'):     # pragma: no cover
    for o, v in conf.items('MISC'):
        config.set_option(o.upper(), v)

if conf.has_section('MODULES'):  # pragma: no cover
    for o, v in conf.items('MODULES'):
        config.set_option(o.upper(), v)

if conf.has_section('PLUGINS'):  # pragma: no cover
    for o, v in conf.items('PLUGINS'):
        path = v if '/' in v or '\\' in v else plugins_path
        try:
            plugin = registry.load_plugin(v, path)
            if plugin:
                registry.add_service(o.lower(), plugin.query)
        except:
            # See issue #85!
            if v in ('isbndb.py', 'openl.py'):
                print("*** WARNING: plugin {} is now in the core! Check {}."
                      .format(v, 'isbntools.conf'))
            else:
                raise PluginNotLoadedError(v)


# get plugins from entry_points
try:                                 # pragma: no cover
    for entry in iter_entry_points(group='isbntools.plugins'):
        registry.add_service(entry.name, entry.load())
except:                              # pragma: no cover
    pass

# get formatters from entry_points
try:                                 # pragma: no cover
    for entry in iter_entry_points(group='isbntools.formatters'):
        registry.add_bibformatter(entry.name, entry.load())
except:                              # pragma: no cover
    pass


# socket timeout is not exposed at urllib2 level so I had to import the
# module and set a default value for all the sockets (timeout in seconds)
# however this should be done at top level due to strong side effects...
socket.setdefaulttimeout(SOCKETS_TIMEOUT)

# THREADS_TIMEOUT is a parameter used downstream by Thread calls (see vias.py)
config.setthreadstimeout(THREADS_TIMEOUT)

# set CONF_PATH
if CONF_PATH is None:
    if VIRTUAL:
        CONF_PATH = os.path.join(sys.prefix, 'isbntools')
    else:
        CONF_PATH = os.path.expanduser('~/isbntools')

# set metadata cache
if config.options.get('CACHE', 'UNDEFINED').lower() == 'no':
    registry.set_cache(None)
else:
    CACHE_FILE = '.metacache'
    cache_path = os.path.join(CONF_PATH, CACHE_FILE)
    from isbnlib.dev.helpers import ShelveCache
    try:
        registry.set_cache(ShelveCache(cache_path))
    except:
        # stay with the default in-memory cache
        pass


# set covers cache
if config.options.get('COVERSCACHE', 'UNDEFINED').lower() == 'no':
    registry.set_covers_cache(None)
else:
    CACHE_FOLDER = '.covers'
    cache_path = os.path.join(CONF_PATH, CACHE_FOLDER)
    from isbnlib.dev.helpers import CoversCache
    registry.set_covers_cache(CoversCache(cache_path))


# set logger
fmt = "%(asctime)s;%(levelname)s;%(message)s"
if CONF_PATH:
    log_path = os.path.join(CONF_PATH, 'isbntools.log')
    debug = config.options.get('DEBUG', 'False')
    level = logging.DEBUG if debug == 'True' else logging.CRITICAL
    log_file = 'isbntools.DEBUG.log' if debug == 'True' else 'isbntools.log'
    log_path = os.path.join(CONF_PATH, log_file)
    logging.basicConfig(filename=log_path, level=level, format=fmt)
else:
    logging.basicConfig(level=logging.CRITICAL, format=fmt)


# setup Windows console
if WINDOWS:
    from ._console import set_msconsole
    set_msconsole()

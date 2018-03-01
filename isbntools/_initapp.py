# -*- coding: utf-8 -*-
"""Read and set config parameters."""

try:  # pragma: no cover
    import configparser
except ImportError:  # pragma: no cover
    import ConfigParser as configparser
import logging
import os
import sys

from isbnlib import config
from isbnlib import registry

# env
PY2 = sys.version < '3'
PY3 = not PY2
VIRTUAL = getattr(sys, 'base_prefix', sys.prefix) != sys.prefix \
   or hasattr(sys, 'real_prefix')
WINDOWS = os.name == 'nt'

# defaults parameters can be overwritten in
# isbntools.conf at users's $HOME/.isbntools directory (UNIX)

DEFAULTS = r"""
[MISC]
REN_FORMAT={firstAuthorLastName}{year}_{title}_{isbn}
DEBUG=False
[SYS]
URLOPEN_TIMEOUT=10
THREADS_TIMEOUT=12
[SERVICES]
DEFAULT_SERVICE=merge
VIAS_MERGE=parallel
[MODULES]
"""

# get defaults
URLOPEN_TIMEOUT = float(config.URLOPEN_TIMEOUT)
THREADS_TIMEOUT = float(config.THREADS_TIMEOUT)

# set conf path
CONF_PATH = None


# pylint: disable=global-statement
def setconfpath(confpath):
    """Set the directory of the conf file."""
    global CONF_PATH
    CONF_PATH = confpath
    config.set_option('CONF_PATH', confpath)


# read/set conf file
conf = configparser.ConfigParser()
# read DEFAULTS (in memory)
try:  # pragma: no cover
    conf.read_string(DEFAULTS)  # PY3
except:  # pragma: no cover
    import io
    # pylint: disable=deprecated-method
    conf.readfp(io.BytesIO(DEFAULTS))  # PY2
# read user options
if VIRTUAL:  # pragma: no cover
    conf.files = conf.read([
        os.path.join(sys.prefix, os.path.join('isbntools', 'isbntools.conf'))
    ])
else:
    if WINDOWS:  # pragma: no cover
        conf.files = conf.read([
            os.path.join(
                os.getenv('APPDATA'),
                os.path.join('isbntools', 'isbntools.conf'))
        ])
    else:  # pragma: no cover
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
    URLOPEN_TIMEOUT = float(conf.get('SYS', 'URLOPEN_TIMEOUT'))
    THREADS_TIMEOUT = float(conf.get('SYS', 'THREADS_TIMEOUT'))

if conf.has_section('SERVICES'):
    for o, v in conf.items('SERVICES'):
        if o.upper() == 'DEFAULT_SERVICE':
            registry.setdefaultservice(v)
            continue
        if 'api_key' in o:  # pragma: no cover
            name = o[:-8]
            config.add_apikey(name, v)
        else:
            config.set_option(o.upper(), v)

if conf.has_section('MISC'):  # pragma: no cover
    for o, v in conf.items('MISC'):
        config.set_option(o.upper(), v)

if conf.has_section('MODULES'):  # pragma: no cover
    for o, v in conf.items('MODULES'):
        config.set_option(o.upper(), v)

# URLOPEN_TIMEOUT is used by webservice.py
config.seturlopentimeout(URLOPEN_TIMEOUT)

# THREADS_TIMEOUT is used by vias.py
config.setthreadstimeout(THREADS_TIMEOUT)

# set CONF_PATH
if CONF_PATH is None:
    if VIRTUAL:
        CONF_PATH = os.path.join(sys.prefix, 'isbntools')
    else:
        CONF_PATH = os.path.join(os.getenv('APPDATA'), 'isbntools') \
                    if WINDOWS else os.path.expanduser('~/.isbntools')

# set metadata cache
if config.options.get('CACHE', 'UNDEFINED').lower() == 'no':
    registry.set_cache(None)
else:
    CACHE_FILE = '.metacache'
    cache_path = os.path.join(CONF_PATH, CACHE_FILE)
    from ._shelvecache import ShelveCache
    try:
        registry.set_cache(ShelveCache(cache_path))
    except:
        # stay with the default in-memory cache
        pass

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

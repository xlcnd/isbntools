# -*- coding: utf-8 -*-
# isort:skip_file
"""Read and set config parameters."""

try:  # pragma: no cover
    import configparser
except ImportError:  # pragma: no cover
    import ConfigParser as configparser
import logging
import os
import sys

from isbnlib import config

# env
PY2 = sys.version < '3'
PY3 = not PY2
VIRTUAL = getattr(sys, 'base_prefix', sys.prefix) != sys.prefix or hasattr(
    sys, 'real_prefix')
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
LOAD_METADATA_PLUGINS=True
LOAD_FORMATTER_PLUGINS=True
[SERVICES]
DEFAULT_SERVICE=goob
VIAS_MERGE=parallel
[MODULES]
"""

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
            os.path.join(os.getenv('APPDATA'),
                         os.path.join('isbntools', 'isbntools.conf'))
        ])
    else:  # pragma: no cover
        conf.files = conf.read([
            '/etc/.isbntools/isbntools.conf',
            '/usr/local/bin/isbntools.conf',
            '/usr/local/isbntools.conf',
            os.path.expanduser('~/.isbntools.conf'),
            os.path.expanduser('~/.local/isbntools/isbntools.conf'),
            os.path.expanduser('~/.config/isbntools/isbntools.conf'),
            os.path.expanduser('~/.isbntools/isbntools.conf'),
        ])
try:  # pragma: no cover
    setconfpath(os.path.dirname(conf.files[0]))
except:
    pass

# set options
if conf.has_section('SYS'):
    # get user defined values for timeouts
    URLOPEN_TIMEOUT = float(conf.get('SYS', 'URLOPEN_TIMEOUT'))
    THREADS_TIMEOUT = float(conf.get('SYS', 'THREADS_TIMEOUT'))
    # URLOPEN_TIMEOUT is used by webservice.py and is a number
    config.seturlopentimeout(URLOPEN_TIMEOUT)
    # THREADS_TIMEOUT is used by vias.py and is a number
    config.setthreadstimeout(THREADS_TIMEOUT)
    # LOAD_METADATA_PLUGINS
    LOAD_METADATA_PLUGINS = bool(
        conf.get('SYS', 'LOAD_METADATA_PLUGINS') == 'True')
    config.set_option('LOAD_METADATA_PLUGINS', LOAD_METADATA_PLUGINS)
    # LOAD_FORMATTER_PLUGINS
    LOAD_FORMATTER_PLUGINS = bool(
        conf.get('SYS', 'LOAD_FORMATTER_PLUGINS') == 'True')
    config.set_option('LOAD_FORMATTER_PLUGINS', LOAD_FORMATTER_PLUGINS)

# only now we can import registry!
# pylint: disable=wrong-import-position
from isbnlib import registry

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

# set CONF_PATH
if not CONF_PATH:
    if VIRTUAL:
        CONF_PATH = os.path.join(sys.prefix, 'isbntools')
    else:
        CONF_PATH = (os.path.join(os.getenv('APPDATA'), 'isbntools')
                     if WINDOWS else os.path.expanduser('~/.isbntools'))
    # make the folder if it doesn't exist (see issue #101)!
    try:  # pragma: no cover
        os.mkdir(CONF_PATH)
    except:
        pass

# set metadata cache
if config.options.get('CACHE', 'UNDEFINED').lower() == 'none':
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
fmt = '%(asctime)s;%(levelname)s;%(message)s'
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

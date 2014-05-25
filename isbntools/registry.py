# -*- coding: utf-8 -*-
"""Registry for metadata services."""

import imp
import sys
from . import _wcat as wcat
from . import _goob as goob
from . import _merge as merge
from .exceptions import PluginNotLoadedError

services = {'default': merge.query,
            'wcat': wcat.query,
            'goob': goob.query,
            'merge': merge.query,
            }


def setdefaultservice(name):
    """Set the default service."""
    global services
    services['default'] = services[name]


def add_service(name, query):         # pragma: no cover
    """Add a new service to services."""
    global services
    services[name] = query


def load_plugin(name, plugin_dir):    # pragma: no cover
    """Load pluggins."""
    try:
        return sys.modules[name]
    except KeyError:
        # not yet loaded so continue...
        pass

    try:
        fp, pathname, description = imp.find_module(name, [plugin_dir])
    except:
        raise PluginNotLoadedError(pathname)
    try:
        return imp.load_module(name, fp, pathname, description)
    finally:
        if fp:
            fp.close()

# -*- coding: utf-8 -*-


import imp
import sys
from .dev import wcat
from .dev import goob
from .dev import merge
from .dev import isbndb
from .dev import openl
from .exceptions import PluginNotLoadedError

"""
Registry for metadata services
"""
services = {'default': merge.query,
            'wcat': wcat.query,
            'goob': goob.query,
            'merge': merge.query,
            'isbndb': isbndb.query,
            'openl': openl.query,
            }


def setdefaultservice(name):
    """
    Sets the default service
    """
    global services
    services['default'] = services[name]


def add_service(name, query):
    """
    Add a new service to services
    """
    global services
    services[name] = query


def load_plugin(name, plugin_dir):
    """
    Loads pluggins
    """
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

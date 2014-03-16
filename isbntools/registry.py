#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dev import wcat
from .dev import googlebooks
from .dev import merge
from .dev import isbndb
from .dev import openl


"""
Config file for metadata services
"""
services = {'default': merge.query,   # <-- mandatory
            'wcat': wcat.query,
            'goob': googlebooks.query,
            'merge': merge.query,
            'isbndb': isbndb.query,
            'openl': openl.query,
            }

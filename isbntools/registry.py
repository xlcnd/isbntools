#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wcat
import googlebooks
import isbndb
# <-- put your service here


"""
Registry for metadata services
"""
services = {'default': wcat.query,   # <-- you have to define a default service
            'wcat': wcat.query,
            'isbndb': isbndb.query,
            'goob': googlebooks.query,
            # <-- put your service here
            }

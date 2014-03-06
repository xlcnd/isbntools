#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wcat
import googlebooks
# import isbndb                      # <-- HERE

"""
Registry for metadata services
"""
services = {'default': wcat.query,   # <-- mandatory
            'wcat': wcat.query,
            'goob': googlebooks.query,
            #'isbndb': isbndb.query  # <-- HERE
            }

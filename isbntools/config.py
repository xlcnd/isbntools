#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Config file for isbntools
"""


"""
Timeouts
"""
SOCKETS_TIMEOUT = 12    # seconds
THREADS_TIMEOUT = 11    # seconds


"""
Your API keys
"""
apikeys = {}


def add_apikey(service, apikey):
    """
    Add API keys

    add_apikey('isbndb', 'JuHytr6') [is fake!]
    """
    apikeys[service] = apikey

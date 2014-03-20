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


def setthreadstimeout(seconds):
    """
    Sets the value of THREADS_TIMEOUT (in seconds)
    """
    global THREADS_TIMEOUT
    THREADS_TIMEOUT = seconds

"""
API keys
"""
apikeys = {}


def add_apikey(service, apikey):
    """
    Add API keys

    add_apikey('isbndb', 'JuHytr6') [is fake!]
    """
    apikeys[service] = apikey

"""
Services preferences
"""
VIAS_MERGE = None

def setvias(var):
    """
    Set the value of variables of the type VIAS_???
    """
    global VIAS_MERGE
    VIAS_MERGE = var

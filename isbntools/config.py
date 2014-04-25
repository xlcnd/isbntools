# -*- coding: utf-8 -*-
"""
Config file for isbntools
"""


""" Timeouts """
SOCKETS_TIMEOUT = 12    # seconds
THREADS_TIMEOUT = 11    # seconds


def setthreadstimeout(seconds):
    """
    Sets the value of THREADS_TIMEOUT (in seconds)
    """
    global THREADS_TIMEOUT
    THREADS_TIMEOUT = seconds


""" API keys """
apikeys = {}


def add_apikey(service, apikey):  # pragma: no cover
    """
    Add API keys

    add_apikey('isbndb', 'JuHytr6') [is fake!]
    """
    apikeys[service] = apikey


""" Generic Options """
options = {}


def set_option(option, value):
    """
    Set the value for option
    """
    options[option] = value

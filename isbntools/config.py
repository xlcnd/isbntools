#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your API keys
"""
apikeys = {}


def add_apikey(service, apikey):
    """
    Add API keys

    ex: add_apikey('isbndb', 'JuHytr6') [is fake!]
    """
    apikeys[service] = apikey

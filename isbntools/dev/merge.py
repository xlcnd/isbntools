#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .exceptions import WPNotImplementedError


class Merge(object):
    """
    Class for merge metadata records
    """
    def __init__(self, isbn):
        raise WPNotImplementedError()
    

def query(isbn):
    """
    Function API to the class
    """
    # mmd = Merge(isbn)
    pass
    
# flake8: noqa

# -*- coding: utf-8 -*-
"""Rename files using metadata."""

import sys
import logging
from difflib import get_close_matches
from isbnlib import (canonical, clean, config, get_canonical_isbn,
                     registry, quiet_errors)

FORMAT = '%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)




def parse_args(args):
    """Parse and return a tuple of the command line arguments."""
    fn = args[-1]
    service = None
    key = None
    isbn = None
    pattern = None
    if len(args) == 1:
        return (isbn, service, key, pattern, fn)
    isbn = get_canonical_isbn(canonical(clean(args[0])))
    providers = list(registry.services.keys())
    if isbn:
        args.pop(0)
    if args[0] != fn:
        service = args[0]
        match = get_close_matches(service, providers)
        if len(match) == 1 and '{' not in args[0]:  # <- rule out placeholders
            service = match[0]
        else:
            service = None
            pattern = args[0]
        key = None if args[1] == fn else args[1]
        if key and '{' in key:
            pattern = key
            key = None
        if not args[1] == fn:
            pattern = pattern if args[2] == fn else args[2]
    return (isbn, service, key, pattern, fn)


def is_fnpatt(filename):
    """Check if filename is a fnpattern."""
    return True if '*' in filename or '?' in filename else False


def reg_apikey(service, apikey):
    """Register API-KEY."""
    try:
        config.add_apikey(service, apikey)
    except:
        pass


def ren(args):
    """Rename files."""
    from ._rename import (checkpattern, rencwdfiles,
                          renfile, get_isbn)
    isbn, service, apikey, pattern, filename = parse_args(args)

    if pattern and not checkpattern(pattern):
        return

    if apikey:
        reg_apikey(service, apikey)

    if not isbn:
        if is_fnpatt(filename):
            return rencwdfiles(filename, service, pattern)
        isbn = get_isbn(filename)
        if not isbn:
            return
    return renfile(filename, isbn, service, pattern)

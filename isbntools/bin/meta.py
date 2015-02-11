#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from difflib import get_close_matches

from isbnlib.dev.helpers import fmtbib, fmts
from isbntools._lab import sprint
from isbntools.app import (canonical, clean, config, get_canonical_isbn, meta,
                           quiet_errors, registry)

PREFIX = 'isbn_'


def usage(prefix, wservs="wcat|goob|...", ofmts="labels"):
    sys.stderr.write('Usage: %smeta ISBN [%s] [%s] [apikey]\n  '
                     '...  or try with '
                     'another service in list!\n' % (prefix, wservs, ofmts))
    return 1


def parse_args(args):
    service = None
    api = None
    fmt = None
    isbn = get_canonical_isbn(canonical(clean(args[0])))
    if len(args) == 1 or not isbn:
        return (isbn, service, fmt, api)
    del args[0]
    providers = list(registry.services.keys())
    for a in args:
        match = get_close_matches(a, fmts)
        if len(match) == 1:
            fmt = match[0]
            args.remove(a)
            break
    for a in args:
        match = get_close_matches(a, providers)
        if len(match) == 1:
            service = match[0]
            args.remove(a)
            break
    api = args[0] if args else None
    return (isbn, service, fmt, api)


def main(args=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv[1:] if not args else args[1:]
        isbn, service, fmt, apikey = parse_args(args)
        if not isbn:
            raise
        service = service if service else 'default'
        fmt = fmt if fmt else 'labels'
        if apikey:
            try:
                config.add_apikey(service, apikey)
            except:
                pass
        r = meta(isbn, service)
        sprint((fmtbib(fmt, r)))
    except:
        providers = list(registry.services.keys())[:]
        try:
            providers.remove('default')
        except:
            pass
        available = '|'.join(sorted(providers))
        bibf = fmts[:]
        try:
            bibf.remove('labels')
        except:
            pass
        ofmts = '|'.join(sorted(bibf))
        return usage(prefix, available, ofmts)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from difflib import get_close_matches
from isbntools import (meta, clean, canonical, get_canonical_isbn,
                       config, registry, quiet_errors)
from isbntools.dev.lab import fmtbib, fmts

logging.basicConfig(level=logging.CRITICAL)


def usage(wservs="wcat|goob|...", ofmts="labels"):
    sys.stderr.write('Usage: isbn_meta ISBN [%s] [%s] [apikey]\n  '
                     '...  or try with '
                     'another service in list!\n' % (wservs, ofmts))
    sys.exit(1)


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


def main():
    sys.excepthook = quiet_errors
    try:
        isbn, service, fmt, apikey = parse_args(sys.argv[1:])
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
        print((fmtbib(fmt, r)))
    except:
        providers = list(registry.services.keys())
        providers.remove('default')
        available = '|'.join(providers)
        fmts.remove('labels')
        ofmts = '|'.join(fmts)
        usage(available, ofmts)

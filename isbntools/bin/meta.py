# -*- coding: utf-8 -*-

import sys
from difflib import get_close_matches

from ..app import (canonical, clean, config, get_canonical_isbn, meta,
                   quiet_errors, registry, uprint)

PREFIX = 'isbn_'

fmtbib = lambda x, y: registry.bibformatters[x](y)
fmts = list(registry.bibformatters.keys())


def usage(prefix, wservs="wcat|goob|...", ofmts="labels"):
    """Usage message."""
    sys.stderr.write('Usage: %smeta ISBN [%s] [%s] [apikey]\n  '
                     '...  or try with '
                     'another service in list!\n' % (prefix, wservs, ofmts))
    return 1


def parse_args(args):
    """Parse args from command line."""
    service = None
    api = None
    fmt = None
    isbn = get_canonical_isbn(canonical(clean(args[0])))
    if len(args) == 1 and isbn:
        return (isbn, service, fmt, api)
    if isbn:
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


def do_pipe():
    """Read isbn from pipe."""
    if sys.stdin.isatty():
        return
    service, fmt, apikey = (None, None, None)
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        _, service, fmt, apikey = parse_args(args)
    service = service if service else 'default'
    fmt = fmt if fmt else 'labels'
    if apikey:
        try:
            config.add_apikey(service, apikey)
        except:
            pass
    for line in sys.stdin:
        line = line.strip()
        uprint((fmtbib(fmt, meta(line, service))))
    return 0


def do_terminal(args=None):
    """Read isbn from terminal."""
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
    uprint((fmtbib(fmt, r)))
    return 0


def main(args=None, prefix=PREFIX):
    """Metadata for a given ISBN."""
    sys.excepthook = quiet_errors
    try:
        return do_terminal(args) if sys.stdin.isatty() else do_pipe()
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

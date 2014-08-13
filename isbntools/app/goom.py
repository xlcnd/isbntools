#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from difflib import get_close_matches
from isbntools import quiet_errors
from isbntools.contrib.modules.goom import goom
from isbntools.dev.lab import fmtbib, fmts

logging.basicConfig(level=logging.CRITICAL)


def usage(ofmts="labels"):
    sys.stderr.write('Usage: isbn_goom "words" [%s] \n' % ofmts)
    sys.exit(1)


def parse_args(args):
    fmt = None
    words = args[0]
    if len(args) == 1:
        return (words, fmt)
    del args[0]
    for f in fmts:
        if f in args:
            fmt = f
            args.remove(f)
            break
    return (words, fmt)


def main():
    sys.excepthook = quiet_errors
    try:
        words, fmt = parse_args(sys.argv[1:])
        if not words:
            raise
        match = get_close_matches(fmt, fmts)
        if len(match) == 1:
            fmt = match[0]
        fmt = fmt if fmt else 'labels'
        for r in goom.query(words):
            print((fmtbib(fmt, r)))
            print("---")
    except:
        fmts.remove('labels')
        ofmts = '|'.join(fmts)
        usage(ofmts)

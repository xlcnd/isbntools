#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from difflib import get_close_matches

from isbnlib.dev.helpers import fmtbib, fmts

from isbntools.app import goom, quiet_errors
from isbntools._lab import sprint


logging.basicConfig(level=logging.CRITICAL)


def usage(ofmts="labels"):
    sys.stderr.write('Usage: isbn_goom "words" [%s] \n' % ofmts)
    return 1


def main(args=None):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv if not args else args
        if len(args) > 2:
            words, fmt = (args[1], args[2])
        elif len(args) == 1:
            raise
        else:
            words, fmt = (args[1], None)
        if fmt:
            match = get_close_matches(fmt, fmts)
            if len(match) == 1:
                fmt = match[0]
        fmt = fmt if fmt else 'labels'
        for r in goom(words):
            sprint((fmtbib(fmt, r)))
    except:
        fmts.remove('labels')
        ofmts = '|'.join(fmts)
        return usage(ofmts)

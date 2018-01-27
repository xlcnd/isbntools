# -*- coding: utf-8 -*-

import sys
from difflib import get_close_matches

from isbnlib.dev.helpers import fmtbib, fmts

from ..app import goom, quiet_errors, uprint

PREFIX = 'isbn_'


def usage(ofmts="labels", prefix=PREFIX):
    sys.stderr.write('Usage: %sgoom "words" [%s] \n' % (prefix, ofmts))
    return 1


def main(args=None, prefix=PREFIX):
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
            uprint((fmtbib(fmt, r)))
            print('')
        return 0
    except:
        bibf = fmts[:]
        try:
            bibf.remove('labels')
        except:
            pass
        ofmts = '|'.join(sorted(bibf))
        return usage(ofmts, prefix)

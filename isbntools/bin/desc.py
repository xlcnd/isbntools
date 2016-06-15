# -*- coding: utf-8 -*-

import sys

from textwrap import fill

from ..app import desc, quiet_errors, uprint

PREFIX = 'isbn_'


def usage(prefix=PREFIX):
    print('Usage: %sdesc ISBN' % prefix)
    return 1


def main(args=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv[1] if not args else args[1]
        content = desc(args)
        content = fill(content, width=75) if content else None
        if content:
            uprint(content)
    except:
        usage(prefix)

# -*- coding: utf-8 -*-

import sys

from ..app import desc, quiet_errors

PREFIX = 'isbn_'


def usage(prefix=PREFIX):
    print('Usage: %scover ISBN' % prefix)
    return 1


def main(args=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv[1] if not args else args[1]
        print(desc(args))
    except:
        usage(prefix)

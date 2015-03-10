# -*- coding: utf-8 -*-

import sys

from ..app import doi, quiet_errors

PREFIX = 'isbn_'


def usage(prefix=PREFIX):
    print('Usage: %sdoi ISBN' % prefix)
    return 1


def main(args=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv[1] if not args else args[1]
        print(doi(args))
    except:
        usage(prefix)

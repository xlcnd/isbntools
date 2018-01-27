# -*- coding: utf-8 -*-

import sys

from ..app import mask, quiet_errors

PREFIX = 'isbn_'


def usage(prefix=PREFIX):
    print('Usage: %smask ISBN' % prefix)
    return 1


def main(isbn=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        output = mask(isbn)
        if output:
            print(output)
    except:
        usage(prefix)
